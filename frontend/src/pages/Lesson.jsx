import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { Play, RotateCcw, ChevronRight, CheckCircle2, XCircle, Flame, Zap, Star, Lightbulb, ArrowLeft, Loader2, Code2, HelpCircle } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { toast } from 'sonner';
import { progressApi, authApi, isAuthed, lessonsApi, pathsApi } from '../lib/api';
import { usePyodide } from '../hooks/usePyodide';
import { logError } from '../lib/logger';
import Paywall from '../components/Paywall';
import UpgradeCelebration from '../components/UpgradeCelebration';
import { runJavaScript, mountHTMLPreview, normalizeHTML, normalizeQuotes } from '../lib/runners';
import { ByteNavbar } from '../components/ByteMascot';

const FREE_LESSONS_PER_PATH = 3;

export default function Lesson() {
  const { t, lang } = useLanguage();
  const { slug } = useParams();
  const navigate = useNavigate();

  const [lesson, setLesson] = useState(null);
  const [loading, setLoading] = useState(true);
  const [code, setCode] = useState('');
  const [output, setOutput] = useState('');
  const [tab, setTab] = useState('tests');
  const [tests, setTests] = useState([]);
  const [running, setRunning] = useState(false);
  const [byteOpen, setByteOpen] = useState(false);
  const [hintIndex, setHintIndex] = useState(0);
  const [lessonDone, setLessonDone] = useState(false); // prevents duplicate toasts on re-run
  const [stats, setStats] = useState({ streak: 0, xp: 0, energy: 5, maxEnergy: 5 });
  const [isPro, setIsPro] = useState(false);
  const [celebrationOpen, setCelebrationOpen] = useState(false);
  const [upcomingLessons, setUpcomingLessons] = useState([]);
  const [totalRemaining, setTotalRemaining] = useState(0);
  const [phase, setPhase] = useState('intro'); // 'intro' | 'code' | 'quiz' | 'done'
  const [currentQuizIndex, setCurrentQuizIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState(null);
  const [quizFeedback, setQuizFeedback] = useState(null); // null | 'correct' | 'wrong'
  const previewRef = useRef(null);

  const py = usePyodide();

  // Load lesson from backend
  useEffect(() => {
    (async () => {
      setLoading(true);
      try {
        const les = await lessonsApi.get(slug);
        setLesson(les);
        setCode(les.starter_code || '');
        setTests((les.tests || []).map((t) => ({ ...t, passed: false })));
        setPhase('intro');
        setCurrentQuizIndex(0);
        setSelectedOption(null);
        setQuizFeedback(null);
        setByteOpen(false);
        setHintIndex(0);
        setLessonDone(false);
        setOutput('');
        setTab('tests');
      } catch (err) {
        logError('Lesson.load', err, { slug });
        toast.error('Lição não encontrada');
      } finally {
        setLoading(false);
      }
    })();
  }, [slug]);

  useEffect(() => {
    if (!isAuthed()) return;
    (async () => {
      try {
        const me = await authApi.me();
        setIsPro(!!me.user?.is_pro);
        if (me.progress) {
          setStats({
            streak: me.progress.streak,
            xp: me.progress.xp_total,
            energy: me.progress.energy,
            maxEnergy: me.progress.max_energy,
          });
        }
      } catch (err) {
        logError('Lesson.loadStats', err);
      }
    })();
  }, [slug]);

  if (loading || !lesson) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ background: 'var(--cf-space)' }}>
        <div className="text-slate-400 flex items-center gap-2"><Loader2 size={16} className="animate-spin" /> Carregando lição...</div>
      </div>
    );
  }

  // Paywall: backend returns minimal metadata with requires_pro=true for locked lessons.
  if (lesson.requires_pro) {
    return (
      <div className="min-h-screen relative" style={{ background: 'var(--cf-space)' }}>
        <header className="border-b sticky top-0 z-40 backdrop-blur-md" style={{ background: 'rgba(10,15,30,0.92)', borderColor: 'var(--cf-border)' }}>
          <div className="max-w-7xl mx-auto px-4 h-14 flex items-center gap-3">
            <Link to="/" className="shrink-0" title="CodeFuturo — início">
              <ByteNavbar size={36} />
            </Link>
            <button onClick={() => navigate(`/jornada/${lesson.path_slug}`)} className="text-slate-300 hover:text-white flex items-center gap-1 text-sm font-semibold shrink-0" data-testid="paywall-back-trail">
              <ArrowLeft size={16} /> Trilha
            </button>
            <div className="flex-1 min-w-0">
              <div className="text-xs text-slate-400 truncate">{lesson.path_slug} · {lesson.chapter}</div>
              <div className="font-display font-bold text-white truncate">{lesson.title}</div>
            </div>
          </div>
        </header>
        <Paywall lesson={lesson} freeLimit={lesson.free_limit || 3} />
      </div>
    );
  }

  const isPython = lesson.language === 'python';
  const isJS = lesson.language === 'javascript';
  const isHTML = lesson.language === 'html';
  const instruction = lesson[`instruction_${lang}`] || lesson.instruction_pt || '';
  const expected = tests[0]?.expected_stdout || tests[0]?.expected || '';
  const hints = lesson.hints?.length > 0 ? lesson.hints : (lesson.hint ? [lesson.hint] : []);

  const doValidate = (out, error) => {
    const newTests = tests.map((t) => {
      const exp = (t.expected_stdout || t.expected || '').trim();
      const actual = (out || '').trim();
      let passed = false;
      if (!error) {
        if (isHTML) {
          // HTML: check if user's code contains the expected snippet (normalized)
          passed = normalizeHTML(actual).includes(normalizeHTML(exp));
        } else if (isPython || isJS) {
          // Executed languages: output is plain text, no quotes in syntax
          passed = actual === exp;
        } else {
          // Static languages (SQL, TypeScript, Java, C++, Go, AI Prompts…)
          // Accept both ' and " as equivalent — e.g. 'Maria' == "Maria"
          passed = normalizeQuotes(actual) === normalizeQuotes(exp);
        }
      }
      return { ...t, passed };
    });
    setTests(newTests);
    return newTests.every((t) => t.passed);
  };

  const triggerCelebrationIfMilestone = async () => {
    if (isPro) return;
    if (!lesson || lesson.order !== FREE_LESSONS_PER_PATH) return;
    try {
      const res = await pathsApi.get(lesson.path_slug);
      const upcoming = (res.lessons || []).filter((le) => le.order > FREE_LESSONS_PER_PATH);
      setUpcomingLessons(upcoming);
      setTotalRemaining(upcoming.length);
      setCelebrationOpen(true);
    } catch (err) {
      logError('Lesson.celebration', err);
      setCelebrationOpen(true);
    }
  };

  const run = async () => {
    if (stats.energy <= 0) { toast.error('⚡ Sem energia! Ela recarrega 1 por hora automaticamente.'); return; }
    setRunning(true);
    setTab('console');

    if (isAuthed()) {
      try {
        const e = await progressApi.consumeEnergy();
        setStats((s) => ({ ...s, energy: e.energy }));
      } catch (err) {
        if (err.response?.status === 429) {
          setStats((s) => ({ ...s, energy: 0 }));
          toast.error('Sem energia!');
          setRunning(false);
          return;
        }
      }
    } else {
      setStats((s) => ({ ...s, energy: Math.max(0, s.energy - 1) }));
    }

    let out = '';
    let error = null;

    if (isPython) {
      if (!py.ready) {
        toast.error('Python ainda carregando...');
        setRunning(false);
        return;
      }
      setOutput('Executando...');
      if (tests.length > 1) {
        // Multi-test: run code once per test case with the correct stdin each time
        const tcResults = await py.runTests(code, tests);
        setTests(tcResults.map((r) => ({ ...r, passed: r.passed })));
        const allOk = tcResults.every((r) => r.passed);
        // Show last execution output in console
        const last = tcResults[tcResults.length - 1];
        out = last.stdout;
        error = last.error;
        setOutput(error ? `${out}\n${error}`.trim() : out || '(sem saída)');
        const passed = allOk;
        setRunning(false);
        if (passed) {
          if (lessonDone) { setTab('tests'); } else if (isAuthed()) {
            try {
              const res = await progressApi.completeLesson({ lesson_slug: lesson.slug, path_slug: lesson.path_slug });
              setLessonDone(true);
              if (!res.already_completed) { setStats((s) => ({ ...s, xp: res.progress.xp_total, streak: res.progress.streak })); await triggerCelebrationIfMilestone(); }
            } catch { setLessonDone(true); }
            if (lesson.quiz && lesson.quiz.length > 0) {
              setPhase('quiz'); setCurrentQuizIndex(0); setSelectedOption(null); setQuizFeedback(null);
            } else {
              setPhase('done');
            }
          } else {
            setLessonDone(true);
            if (lesson.quiz && lesson.quiz.length > 0) {
              setPhase('quiz'); setCurrentQuizIndex(0); setSelectedOption(null); setQuizFeedback(null);
            } else {
              setPhase('done');
            }
          }
        } else if (error) { toast.error('Erro no código — confira o console.'); }
        else { toast.error('Não foi dessa vez! Revise e tente novamente.'); }
        return; // early return — multi-test path handles everything
      }
      // Single test: run once with the test's stdin
      const stdinValue = tests[0]?.stdin ?? '';
      const result = await py.run(code, stdinValue);
      out = result.stdout;
      error = result.error;
      setOutput(error ? `${out}\n${error}`.trim() : out || '(sem saída)');
    } else if (isJS) {
      setOutput('Executando...');
      const result = await runJavaScript(code);
      out = result.stdout;
      error = result.error;
      setOutput(error ? `${out}\n${error}`.trim() : out || '(sem saída)');
    } else if (isHTML) {
      // Render preview + validate by comparing normalized HTML
      mountHTMLPreview(previewRef.current, code);
      out = code;
      setOutput('Pré-visualização atualizada — confira ao lado.');
    } else {
      // Fallback validation mode for other languages (SQL, TypeScript, Java, C++, Go…)
      // Normalize quotes so 'text' and "text" are treated as equivalent
      setOutput(code.trim() || '(sem saída)');
      const target = (tests[0]?.expected_stdout || '').trim();
      const codeHas = normalizeQuotes(code).includes(normalizeQuotes(target));
      out = codeHas ? target : code.trim();
    }

    const allPassed = doValidate(out, error);
    setRunning(false);

    if (allPassed) {
      // If already completed this session, skip API call
      if (lessonDone) {
        if (lesson.quiz && lesson.quiz.length > 0) {
          setPhase('quiz'); setCurrentQuizIndex(0); setSelectedOption(null); setQuizFeedback(null);
        } else {
          setPhase('done');
        }
      } else if (isAuthed()) {
        try {
          const res = await progressApi.completeLesson({ lesson_slug: lesson.slug, path_slug: lesson.path_slug });
          setLessonDone(true);
          if (!res.already_completed) {
            setStats((s) => ({ ...s, xp: res.progress.xp_total, streak: res.progress.streak }));
            await triggerCelebrationIfMilestone();
          }
        } catch { setLessonDone(true); }
        if (lesson.quiz && lesson.quiz.length > 0) {
          setPhase('quiz'); setCurrentQuizIndex(0); setSelectedOption(null); setQuizFeedback(null);
        } else {
          setPhase('done');
        }
      } else {
        setLessonDone(true);
        if (lesson.quiz && lesson.quiz.length > 0) {
          setPhase('quiz'); setCurrentQuizIndex(0); setSelectedOption(null); setQuizFeedback(null);
        } else {
          setPhase('done');
        }
      }
    } else if (error) {
      toast.error('Erro no código — confira o console.');
    } else {
      toast.error('Não foi dessa vez! Revise e tente novamente.');
    }
  };

  const reset = () => {
    setCode(lesson.starter_code || '');
    setOutput('');
    setTests((lesson.tests || []).map((t) => ({ ...t, passed: false })));
  };

  const handleQuizAnswer = () => {
    const q = lesson.quiz[currentQuizIndex];
    if (selectedOption === q.correct) {
      setQuizFeedback('correct');
      setTimeout(() => {
        if (currentQuizIndex + 1 < lesson.quiz.length) {
          setCurrentQuizIndex(i => i + 1);
          setSelectedOption(null);
          setQuizFeedback(null);
        } else {
          setPhase('done');
        }
      }, 800);
    } else {
      setQuizFeedback('wrong');
    }
  };

  const passedCount = tests.filter((t) => t.passed).length;
  const nextSlug = lesson.next?.slug;

  return (
    <div className="min-h-screen flex flex-col" style={{ background: 'var(--cf-space)' }}>
      <header className="border-b sticky top-0 z-40 backdrop-blur-md" style={{ background: 'rgba(10,15,30,0.92)', borderColor: 'var(--cf-border)' }}>
        <div className="max-w-7xl mx-auto px-4 h-14 flex items-center gap-3">
          <Link to="/" className="shrink-0" title="CodeFuturo — início">
            <ByteNavbar size={36} />
          </Link>
          <button onClick={() => navigate(`/jornada/${lesson.path_slug}`)} className="text-slate-300 hover:text-white flex items-center gap-1 text-sm font-semibold shrink-0">
            <ArrowLeft size={16} /> Trilha
          </button>
          {lesson.previous?.slug && (
            <button onClick={() => navigate(`/licao/${lesson.previous.slug}`)} className="text-slate-400 hover:text-white p-1.5 rounded-lg hover:bg-[#1C2235] shrink-0" title="Atividade anterior">
              <ArrowLeft size={16} />
            </button>
          )}
          <div className="flex-1 min-w-0">
            <div className="text-xs text-slate-400 truncate">{lesson.path_slug} · {lesson.chapter}</div>
            <div className="font-display font-bold text-white truncate">{lesson.title}</div>
          </div>
          <div className="flex items-center gap-3 text-sm">
            <span className="flex items-center gap-1.5 text-orange-400 font-bold"><Flame size={14} /> {stats.streak}</span>
            <span className="flex items-center gap-1.5 text-[#A3E635] font-bold"><Star size={14} /> {stats.xp}</span>
            <span className="flex items-center gap-1.5 text-blue-400 font-bold"><Zap size={14} /> {stats.energy}/{stats.maxEnergy}</span>
          </div>
        </div>
        {isPython && py.loading && (
          <div className="bg-[#1C2235] border-t" style={{ borderColor: 'var(--cf-border)' }}>
            <div className="max-w-7xl mx-auto px-4 py-1.5 text-[11px] text-slate-300 flex items-center gap-2">
              <Loader2 size={12} className="animate-spin text-[#A3E635]" />
              Carregando Python no navegador (primeira vez ~8MB)...
            </div>
          </div>
        )}
        {isJS && (
          <div className="bg-[#1C2235] border-t" style={{ borderColor: 'var(--cf-border)' }}>
            <div className="max-w-7xl mx-auto px-4 py-1.5 text-[11px] text-slate-300 flex items-center gap-2">
              <Code2 size={12} className="text-[#A3E635]" />
              Execução real de JavaScript no navegador (sandbox).
            </div>
          </div>
        )}
        {isHTML && (
          <div className="bg-[#1C2235] border-t" style={{ borderColor: 'var(--cf-border)' }}>
            <div className="max-w-7xl mx-auto px-4 py-1.5 text-[11px] text-slate-300 flex items-center gap-2">
              <Code2 size={12} className="text-[#A3E635]" />
              Pré-visualização ao vivo do HTML — clique em Executar para renderizar.
            </div>
          </div>
        )}
        {!isPython && !isJS && !isHTML && (
          <div className="bg-[#1C2235] border-t" style={{ borderColor: 'var(--cf-border)' }}>
            <div className="max-w-7xl mx-auto px-4 py-1.5 text-[11px] text-slate-300 flex items-center gap-2">
              <Code2 size={12} className="text-[#A3E635]" />
              Modo de validação textual — seu código é comparado com a saída esperada.
            </div>
          </div>
        )}
      </header>

      {phase === 'intro' && (
        <main className="flex-1 max-w-7xl w-full mx-auto p-4 grid md:grid-cols-[1fr_340px] gap-4 items-start">
          {/* Coluna esquerda: teoria rica */}
          <div className="cf-card overflow-auto">
            {/* Cabeçalho da lição */}
            <div className="px-8 pt-7 pb-5 border-b" style={{ borderColor: 'var(--cf-border)' }}>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xs font-bold uppercase tracking-wider text-[#A3E635]">Introdução</span>
              </div>
              <h2 className="font-display text-2xl font-bold text-white">{lesson.title}</h2>
            </div>

            {/* Learning goals */}
            {lesson.learning_goals?.length > 0 && (
              <div className="mx-8 mt-5 p-4 rounded-xl" style={{ background: 'rgba(163,230,53,0.08)', border: '1px solid rgba(163,230,53,0.25)' }}>
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-sm font-bold text-[#A3E635]">🎯 Nesta lição você vai aprender:</span>
                </div>
                <ul className="space-y-1">
                  {lesson.learning_goals.map((goal, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                      <span className="text-[#A3E635] mt-0.5 shrink-0">✓</span>
                      {goal}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Conteúdo teórico */}
            <div className="px-8 py-6 text-slate-300 leading-relaxed">
              <ReactMarkdown
                components={{
                  h2: ({node, ...p}) => <h2 className="text-lg font-bold text-white mt-6 mb-3 first:mt-0" {...p} />,
                  h3: ({node, ...p}) => <h3 className="text-base font-bold text-[#A3E635] mt-5 mb-2" {...p} />,
                  p:  ({node, ...p}) => <p className="mt-3 first:mt-0 leading-relaxed text-slate-300" {...p} />,
                  strong: ({node, ...p}) => <strong className="font-bold text-white" {...p} />,
                  em:     ({node, ...p}) => <em className="italic text-slate-200" {...p} />,
                  table: ({node, ...p}) => <div className="mt-4 mb-2 overflow-x-auto rounded-xl border" style={{ borderColor: 'rgba(163,230,53,0.2)' }}><table className="w-full text-sm" {...p} /></div>,
                  thead: ({node, ...p}) => <thead style={{ background: '#0d1425' }} {...p} />,
                  tbody: ({node, ...p}) => <tbody {...p} />,
                  tr:    ({node, ...p}) => <tr className="border-b" style={{ borderColor: 'rgba(163,230,53,0.1)' }} {...p} />,
                  th:    ({node, ...p}) => <th className="px-4 py-2.5 text-left text-xs font-bold uppercase tracking-wider text-[#A3E635]" {...p} />,
                  td:    ({node, ...p}) => <td className="px-4 py-2.5 text-slate-300 font-mono text-xs" {...p} />,
                  code:   ({node, inline, ...p}) =>
                    inline
                      ? <code className="bg-[#1C2235] rounded px-1.5 py-0.5 text-[#A3E635] font-mono text-[13px]" {...p} />
                      : <code className="block text-slate-200 text-sm leading-relaxed" {...p} />,
                  pre: ({node, children, ...p}) => {
                    const text = String(children?.props?.children || '');
                    const isOutput = text.trim().split('\n').every(l => l.trim().startsWith('#') || l.trim() === '');

                    if (isOutput) {
                      return (
                        <div className="my-3 rounded-xl overflow-hidden border" style={{ borderColor: 'rgba(100,200,100,0.3)' }}>
                          <div className="px-4 py-2 text-xs font-bold uppercase tracking-wider" style={{ background: '#0a1a0a', color: '#86efac' }}>
                            Resultado
                          </div>
                          <pre className="p-4 text-sm font-mono overflow-x-auto" style={{ background: '#071007', color: '#86efac' }} {...p}>{children}</pre>
                        </div>
                      );
                    }

                    return (
                      <div className="my-3 rounded-xl overflow-hidden border" style={{ borderColor: 'rgba(163,230,53,0.2)' }}>
                        <div className="flex items-center gap-1.5 px-4 py-2.5" style={{ background: '#0d1425' }}>
                          <span className="w-2.5 h-2.5 rounded-full bg-red-500/60" />
                          <span className="w-2.5 h-2.5 rounded-full bg-yellow-500/60" />
                          <span className="w-2.5 h-2.5 rounded-full bg-green-500/60" />
                          <span className="ml-2 text-[11px] text-slate-500 font-mono">código</span>
                        </div>
                        <pre className="p-4 text-sm font-mono overflow-x-auto" style={{ background: '#070d1a' }} {...p}>{children}</pre>
                      </div>
                    );
                  },
                  ul: ({node, ...p}) => <ul className="mt-3 mb-2 space-y-1.5 list-disc list-inside" {...p} />,
                  ol: ({node, ...p}) => <ol className="mt-3 mb-2 space-y-1.5 list-decimal list-inside" {...p} />,
                  li: ({node, ...p}) => <li className="text-slate-300 leading-relaxed" {...p} />,
                  hr: () => <hr className="border-slate-700/50 my-5" />,
                  blockquote: ({node, ...p}) => (
                    <blockquote className="border-l-4 border-[#A3E635]/40 pl-4 my-3 text-slate-400 italic" {...p} />
                  ),
                }}
              >
                {lesson.theory || lesson[`instruction_${lang}`] || lesson.instruction_pt || ''}
              </ReactMarkdown>
            </div>

            {/* Preview do exercício — o que o aluno vai escrever */}
            {lesson.starter_code && (
              <div className="mx-8 mb-8 rounded-xl overflow-hidden border" style={{ borderColor: 'rgba(163,230,53,0.2)' }}>
                <div className="flex items-center justify-between px-4 py-2.5" style={{ background: '#0d1425' }}>
                  <div className="flex items-center gap-1.5">
                    <span className="w-2.5 h-2.5 rounded-full bg-red-500/60" />
                    <span className="w-2.5 h-2.5 rounded-full bg-yellow-500/60" />
                    <span className="w-2.5 h-2.5 rounded-full bg-green-500/60" />
                    <span className="ml-2 text-[11px] text-slate-400 font-mono">seu exercício</span>
                  </div>
                  <span className="text-[10px] text-[#A3E635] font-bold uppercase tracking-wider">Complete o código abaixo ↓</span>
                </div>
                <pre className="p-4 text-sm font-mono text-slate-300 overflow-x-auto whitespace-pre-wrap" style={{ background: '#070d1a' }}>
                  {lesson.starter_code}
                </pre>
                {/* Saída esperada */}
                {hints.length > 0 && (
                  <div className="px-4 py-3 border-t flex items-start gap-2" style={{ background: '#0a1020', borderColor: 'rgba(163,230,53,0.1)' }}>
                    <span className="text-[#A3E635] text-xs mt-0.5">💡</span>
                    <span className="text-slate-400 text-xs">{hints[0]}</span>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Coluna direita: card de início fixo */}
          <div className="flex flex-col gap-3 sticky top-20">
            <div className="cf-card p-6 flex flex-col items-center text-center">
              <div className="w-16 h-16 rounded-2xl flex items-center justify-center mb-4" style={{ background: 'rgba(163,230,53,0.1)', border: '1.5px solid rgba(163,230,53,0.3)' }}>
                <ByteNavbar size={44} />
              </div>
              <h3 className="font-display text-lg font-bold text-white mb-1">
                Pronto para começar o exercício?
              </h3>
              <p className="text-slate-500 text-xs mb-6 leading-relaxed">
                Leia a explicação ao lado e clique quando estiver pronto!
              </p>
              <button
                onClick={() => setPhase('code')}
                className="w-full py-3.5 rounded-xl font-bold text-sm tracking-widest uppercase transition-all hover:opacity-90 active:scale-95"
                style={{ background: '#A3E635', color: '#0A0F1E' }}
              >
                INICIAR EXERCÍCIO
              </button>
            </div>

            {/* Info da lição */}
            <div className="cf-card p-4 space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-500">Trilha</span>
                <span className="text-slate-300 font-medium truncate ml-2">{lesson.path}</span>
              </div>
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-500">Lição</span>
                <span className="text-slate-300 font-medium">#{lesson.order}</span>
              </div>
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-500">Energia</span>
                <span className="text-blue-400 font-bold">{stats.energy}/{stats.maxEnergy} ⚡</span>
              </div>
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-500">XP disponível</span>
                <span className="text-[#A3E635] font-bold">+50 XP ⭐</span>
              </div>
            </div>

            {/* Dicas disponíveis */}
            {hints.length > 0 && (
              <div className="cf-card p-4">
                <div className="flex items-center gap-2 text-xs text-slate-400">
                  <Lightbulb size={13} className="text-[#A3E635]" />
                  <span>{hints.length} dica{hints.length > 1 ? 's' : ''} disponíve{hints.length > 1 ? 'is' : 'l'} durante o exercício</span>
                </div>
              </div>
            )}
          </div>
        </main>
      )}

      {phase === 'quiz' && (
        <main className="flex-1 flex items-center justify-center p-4">
          <div className="cf-card p-8 w-full max-w-xl">
            <div className="flex items-center gap-2 mb-6">
              <HelpCircle size={16} className="text-[#A3E635]" />
              <span className="text-xs font-bold uppercase tracking-wider text-[#A3E635]">
                Verificação de Aprendizado — Pergunta {currentQuizIndex + 1} de {lesson.quiz.length}
              </span>
            </div>
            <div className="w-full h-1.5 rounded-full bg-slate-700 mb-6">
              <div
                className="h-1.5 rounded-full bg-[#A3E635] transition-all duration-500"
                style={{ width: `${((currentQuizIndex) / lesson.quiz.length) * 100}%` }}
              />
            </div>
            <p className="text-lg font-bold text-white mb-5">
              {lesson.quiz[currentQuizIndex].question}
            </p>
            <div className="space-y-3">
              {lesson.quiz[currentQuizIndex].options.map((opt, oi) => {
                let cls = 'w-full text-left px-4 py-3 rounded-xl border transition-all text-sm font-medium ';
                if (quizFeedback) {
                  if (oi === lesson.quiz[currentQuizIndex].correct) cls += 'bg-green-900/30 border-green-500 text-green-300';
                  else if (oi === selectedOption && quizFeedback === 'wrong') cls += 'bg-red-900/30 border-red-500 text-red-300';
                  else cls += 'border-slate-700/30 text-slate-600';
                } else if (selectedOption === oi) {
                  cls += 'bg-[#1a2540] border-[#A3E635] text-white';
                } else {
                  cls += 'bg-[#0d1425] border-slate-700 text-slate-300 hover:border-slate-500 hover:text-white';
                }
                return (
                  <button key={oi} disabled={!!quizFeedback} onClick={() => setSelectedOption(oi)} className={cls}>
                    <span className="font-mono text-[#A3E635] mr-3 text-xs opacity-80">{String.fromCharCode(65 + oi)}.</span>
                    {opt}
                  </button>
                );
              })}
            </div>
            {quizFeedback === 'wrong' && (
              <p className="mt-4 text-sm text-red-400">❌ Não foi dessa vez! Tente outra opção.</p>
            )}
            {!quizFeedback && (
              <button
                onClick={handleQuizAnswer}
                disabled={selectedOption === null}
                className="mt-6 w-full py-3 rounded-xl cf-btn-lime font-bold text-sm disabled:opacity-40 disabled:cursor-not-allowed"
              >
                Confirmar resposta
              </button>
            )}
            {quizFeedback === 'wrong' && (
              <button
                onClick={() => { setSelectedOption(null); setQuizFeedback(null); }}
                className="mt-4 w-full py-3 rounded-xl border border-slate-600 text-slate-300 font-bold text-sm hover:border-slate-400"
              >
                Tentar novamente
              </button>
            )}
          </div>
        </main>
      )}

      {phase === 'done' && (
        <main className="flex-1 flex items-center justify-center p-4">
          <div className="cf-card p-10 w-full max-w-lg text-center">
            <div className="text-6xl mb-4">🎉</div>
            <h2 className="font-display text-3xl font-bold text-white mb-2">Atividade concluída!</h2>
            <p className="text-slate-400 mb-8">Você completou o exercício e respondeu todas as perguntas corretamente.</p>
            <div className="flex flex-col sm:flex-row gap-3 justify-center">
              {nextSlug && (
                <Link
                  to={`/licao/${nextSlug}`}
                  className="inline-flex items-center justify-center gap-2 px-8 py-3 rounded-xl font-bold text-base"
                  style={{ background: '#A3E635', color: '#0A0F1E' }}
                >
                  Próxima atividade <ChevronRight size={18} />
                </Link>
              )}
              <button
                onClick={() => navigate(`/jornada/${lesson.path_slug}`)}
                className="inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl border border-slate-600 text-slate-300 font-bold text-base hover:border-slate-400"
              >
                Ver trilha
              </button>
            </div>
          </div>
        </main>
      )}

      {phase === 'code' && <main className="flex-1 max-w-7xl w-full mx-auto p-4 grid md:grid-cols-2 gap-4">
        <div className="cf-card p-6 overflow-auto">
          <div className="flex items-center gap-2 mb-1">
            <ByteNavbar size={28} />
            <div className="text-xs font-bold uppercase tracking-wider text-[#A3E635]">{t('lesson.instruction')}</div>
          </div>
          <h2 className="mt-1 font-display text-2xl font-bold text-white">{lesson.title}</h2>
          <div className="mt-4 text-slate-300 leading-relaxed prose-instr">
            <ReactMarkdown
              components={{
                p:      ({node, ...p}) => <p className="mt-3 first:mt-0 leading-relaxed" {...p} />,
                strong: ({node, ...p}) => <strong className="font-bold text-white" {...p} />,
                em:     ({node, ...p}) => <em className="italic text-slate-200" {...p} />,
                code:   ({node, inline, ...p}) =>
                  inline
                    ? <code className="bg-slate-700 rounded px-1 py-0.5 text-[#A3E635] font-mono text-sm" {...p} />
                    : <code className="block text-slate-200 text-sm leading-relaxed" {...p} />,
                pre: ({node, children, ...p}) => (
                  <div className="my-3 rounded-xl overflow-hidden border" style={{ borderColor: 'rgba(163,230,53,0.2)' }}>
                    <div className="px-4 py-2 text-xs font-bold uppercase tracking-wider text-[#A3E635]" style={{ background: '#0d1425' }}>
                      Exemplo de programação
                    </div>
                    <pre className="p-4 text-sm font-mono overflow-x-auto" style={{ background: '#070d1a' }} {...p}>{children}</pre>
                  </div>
                ),
                ul:     ({node, ...p}) => <ul className="mt-2 mb-1 space-y-1 list-disc list-inside" {...p} />,
                ol:     ({node, ...p}) => <ol className="mt-2 mb-1 space-y-1 list-decimal list-inside" {...p} />,
                li:     ({node, ...p}) => <li className="text-slate-300" {...p} />,
                hr:     () => <hr className="border-slate-700 my-3" />,
              }}
            >
              {instruction}
            </ReactMarkdown>
          </div>

          {expected && (
            <div className="mt-5 rounded-xl overflow-hidden border" style={{ borderColor: 'rgba(163,230,53,0.2)' }}>
              <div className="px-4 py-2 text-xs font-bold uppercase tracking-wider text-[#A3E635]" style={{ background: '#0d1425' }}>
                Saída esperada
              </div>
              <div className="p-4 font-code text-sm" style={{ background: 'var(--cf-panel-light)' }}>
                <pre className="text-[#A3E635] whitespace-pre-wrap">{expected}</pre>
              </div>
            </div>
          )}

          {/* Byte hint button — aparece dentro do card como ponto de entrada */}
          {hints.length > 0 && (
            <button
              onClick={() => { setByteOpen(v => !v); setHintIndex(0); }}
              className="mt-5 inline-flex items-center gap-2 text-sm font-semibold text-slate-400 hover:text-[#A3E635] transition-colors"
            >
              <ByteNavbar size={22} />
              {byteOpen ? 'Fechar dicas do Byte' : `Ver dicas do Byte`}
              <span className="ml-1 px-1.5 py-0.5 rounded-full text-[10px] font-black" style={{ background: 'rgba(163,230,53,0.15)', color: '#A3E635' }}>
                {hints.length}
              </span>
            </button>
          )}

        </div>

        <div className="flex flex-col gap-4">
          <div className="cf-card overflow-hidden flex flex-col min-h-[300px]">
            <div className="flex items-center justify-between px-4 py-2.5 border-b" style={{ borderColor: 'var(--cf-border)' }}>
              <div className="flex items-center gap-1.5">
                <span className="w-3 h-3 rounded-full bg-red-500/70" />
                <span className="w-3 h-3 rounded-full bg-yellow-500/70" />
                <span className="w-3 h-3 rounded-full bg-green-500/70" />
                <span className="ml-3 text-xs text-slate-400 font-code">code.{lesson.language}</span>
              </div>
              <div className="flex items-center gap-2">
                <button onClick={reset} className="text-slate-400 hover:text-white p-1.5 rounded-lg hover:bg-[#1C2235]" title={t('lesson.reset')}>
                  <RotateCcw size={14} />
                </button>
                <button onClick={run} disabled={running || (isPython && !py.ready)} className="inline-flex items-center gap-1.5 px-4 py-1.5 rounded-lg cf-btn-lime text-xs disabled:opacity-50" data-testid="lesson-run-btn">
                  {running ? <Loader2 size={14} className="animate-spin" /> : <Play size={14} />}
                  {running ? 'Executando' : isPython && !py.ready ? 'Carregando' : t('lesson.run')}
                </button>
              </div>
            </div>
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              spellCheck={false}
              autoCorrect="off"
              autoCapitalize="off"
              autoComplete="off"
              data-gramm="false"
              data-gramm_editor="false"
              data-enable-grammarly="false"
              className="flex-1 p-4 font-code text-sm bg-[#0A0F1E] text-slate-100 outline-none resize-none min-h-[260px]"
              style={{ tabSize: 4 }}
            />
          </div>

          <div className="cf-card overflow-hidden">
            <div className="flex items-center border-b" style={{ borderColor: 'var(--cf-border)' }}>
              <button onClick={() => setTab('tests')} className={`px-4 py-2.5 text-xs font-bold ${tab === 'tests' ? 'text-[#A3E635] border-b-2 border-[#A3E635]' : 'text-slate-400'}`}>
                TEST CASES
                {passedCount > 0 && <span className="ml-2 text-[10px]">{passedCount}/{tests.length}</span>}
              </button>
              <button onClick={() => setTab('console')} className={`px-4 py-2.5 text-xs font-bold ${tab === 'console' ? 'text-[#A3E635] border-b-2 border-[#A3E635]' : 'text-slate-400'}`}>
                CONSOLE
              </button>
              {isHTML && (
                <button onClick={() => setTab('preview')} className={`px-4 py-2.5 text-xs font-bold ${tab === 'preview' ? 'text-[#A3E635] border-b-2 border-[#A3E635]' : 'text-slate-400'}`} data-testid="lesson-tab-preview">
                  PREVIEW
                </button>
              )}
              {passedCount === tests.length && nextSlug && (
                <Link to={`/licao/${nextSlug}`} className="ml-auto px-4 py-2 mr-2 text-xs font-bold rounded-full cf-btn-lime inline-flex items-center gap-1">
                  {t('lesson.nextLesson')} <ChevronRight size={14} />
                </Link>
              )}
            </div>
            <div className="p-4 space-y-2 min-h-[140px] bg-[#0A0F1E] max-h-[280px] overflow-auto">
              {tab === 'tests' && (
                tests.map((test, i) => (
                  <div key={`test-${test.id ?? i}`} className="flex items-start gap-3 text-sm">
                    {test.passed ? <CheckCircle2 size={16} className="text-[#A3E635] mt-0.5" /> : <XCircle size={16} className="text-slate-500 mt-0.5" />}
                    <div className="flex-1 min-w-0">
                      <div className="text-slate-200 font-semibold">Teste #{i + 1}</div>
                      <div className="text-xs text-slate-500 font-code mt-0.5 whitespace-pre-wrap">expected: {test.expected_stdout || test.expected}</div>
                    </div>
                  </div>
                ))
              )}
              {tab === 'console' && (
                <div className="font-code text-xs text-slate-300 whitespace-pre-wrap">
                  <div className="text-slate-500">$ run</div>
                  {output}
                </div>
              )}
              {tab === 'preview' && (
                <div ref={previewRef} className="bg-white rounded-lg min-h-[200px]" data-testid="lesson-preview-pane" />
              )}
            </div>
          </div>
        </div>
      </main>}
      {/* ─── Byte Instrutor flutuante ─────────────────────────────────────────── */}
      {hints.length > 0 && (
        <>
          {/* Balão de diálogo */}
          {byteOpen && (
            <div
              className="fixed bottom-[5.5rem] right-5 z-50 w-72 rounded-2xl shadow-2xl"
              style={{ background: '#141824', border: '1.5px solid rgba(163,230,53,0.3)' }}
            >
              {/* Cauda do balão apontando para o Byte abaixo */}
              <div className="absolute bottom-[-9px] right-11 w-0 h-0"
                style={{ borderLeft: '9px solid transparent', borderRight: '9px solid transparent', borderTop: '9px solid rgba(163,230,53,0.3)' }} />
              <div className="absolute bottom-[-7px] right-[45px] w-0 h-0"
                style={{ borderLeft: '8px solid transparent', borderRight: '8px solid transparent', borderTop: '8px solid #141824' }} />

              {/* Header */}
              <div className="flex items-center justify-between px-4 pt-3 pb-2">
                <div className="flex items-center gap-2">
                  <ByteNavbar size={26} />
                  <span className="font-bold text-sm text-white">Byte diz...</span>
                </div>
                <button
                  onClick={() => setByteOpen(false)}
                  className="text-slate-500 hover:text-white transition-colors text-2xl leading-none w-6 h-6 flex items-center justify-center"
                >
                  ×
                </button>
              </div>

              {/* Dots de progresso */}
              <div className="flex items-center gap-1.5 px-4 pb-2">
                {hints.map((_, i) => (
                  <button
                    key={i}
                    onClick={() => setHintIndex(i)}
                    className="rounded-full transition-all duration-200"
                    style={{
                      width: i === hintIndex ? 20 : 8,
                      height: 8,
                      background: i === hintIndex ? '#A3E635' : '#334155',
                    }}
                  />
                ))}
                <span className="ml-auto text-[11px] text-slate-500 font-mono">
                  {hintIndex + 1}/{hints.length}
                </span>
              </div>

              {/* Conteúdo da dica */}
              <div className="px-4 pb-3 text-sm text-slate-200 leading-relaxed min-h-[56px]">
                {hints[hintIndex]}
              </div>

              {/* Navegação */}
              {hints.length > 1 && (
                <div
                  className="flex items-center justify-between px-4 py-2.5 border-t"
                  style={{ borderColor: 'rgba(163,230,53,0.12)' }}
                >
                  <button
                    onClick={() => setHintIndex(i => Math.max(0, i - 1))}
                    disabled={hintIndex === 0}
                    className="text-xs text-slate-400 hover:text-[#A3E635] disabled:opacity-30 transition-colors"
                  >
                    ← Anterior
                  </button>
                  <button
                    onClick={() => setHintIndex(i => Math.min(hints.length - 1, i + 1))}
                    disabled={hintIndex === hints.length - 1}
                    className="text-xs text-slate-400 hover:text-[#A3E635] disabled:opacity-30 transition-colors"
                  >
                    Próxima →
                  </button>
                </div>
              )}
            </div>
          )}

          {/* Botão flutuante do Byte */}
          <button
            onClick={() => { setByteOpen(v => !v); if (!byteOpen) setHintIndex(0); }}
            className="fixed bottom-5 right-5 z-50 group relative"
            title={`${hints.length} dica${hints.length > 1 ? 's' : ''} do Byte`}
          >
            {/* Badge contador */}
            <span
              className="absolute -top-1.5 -right-1.5 z-10 flex items-center justify-center w-5 h-5 rounded-full text-[10px] font-black shadow-md"
              style={{ background: '#A3E635', color: '#0A0F1E' }}
            >
              {hints.length}
            </span>
            <div
              className="rounded-2xl p-2 transition-all duration-200 group-hover:scale-110 group-active:scale-95"
              style={{
                background: byteOpen ? 'rgba(163,230,53,0.12)' : 'rgba(14,18,36,0.97)',
                border: `1.5px solid ${byteOpen ? 'rgba(163,230,53,0.5)' : 'rgba(163,230,53,0.2)'}`,
                boxShadow: byteOpen
                  ? '0 0 0 3px rgba(163,230,53,0.15), 0 8px 32px rgba(0,0,0,0.6)'
                  : '0 4px 24px rgba(0,0,0,0.5)',
              }}
            >
              <ByteNavbar size={52} />
            </div>
          </button>
        </>
      )}

      <UpgradeCelebration
        open={celebrationOpen}
        onClose={() => setCelebrationOpen(false)}
        trackName={lesson.path_slug}
        upcomingLessons={upcomingLessons}
        totalRemaining={totalRemaining}
      />
    </div>
  );
}
