import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { Play, RotateCcw, ChevronRight, CheckCircle2, XCircle, Flame, Zap, Star, Lightbulb, ArrowLeft, Loader2, Code2 } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { toast } from 'sonner';
import { progressApi, authApi, isAuthed, lessonsApi, pathsApi } from '../lib/api';
import { usePyodide } from '../hooks/usePyodide';
import { logError } from '../lib/logger';
import Paywall from '../components/Paywall';
import UpgradeCelebration from '../components/UpgradeCelebration';
import { runJavaScript, mountHTMLPreview, normalizeHTML } from '../lib/runners';

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
  const [showHint, setShowHint] = useState(false);
  const [stats, setStats] = useState({ streak: 0, xp: 0, energy: 5, maxEnergy: 5 });
  const [isPro, setIsPro] = useState(false);
  const [celebrationOpen, setCelebrationOpen] = useState(false);
  const [upcomingLessons, setUpcomingLessons] = useState([]);
  const [totalRemaining, setTotalRemaining] = useState(0);
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
          <div className="max-w-7xl mx-auto px-4 h-14 flex items-center gap-4">
            <button onClick={() => navigate(`/jornada/${lesson.path_slug}`)} className="text-slate-300 hover:text-white flex items-center gap-1 text-sm font-semibold" data-testid="paywall-back-trail">
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

  const doValidate = (out, error) => {
    const newTests = tests.map((t) => {
      const exp = (t.expected_stdout || t.expected || '').trim();
      const actual = (out || '').trim();
      let passed = false;
      if (!error) {
        if (isHTML) {
          passed = normalizeHTML(actual) === normalizeHTML(exp);
        } else {
          passed = actual === exp;
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
    if (stats.energy <= 0) { toast.error('Sem energia! Aguarde o reset ou faça upgrade Pro.'); return; }
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
      const result = await py.run(code);
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
      // Fallback validation mode for other languages (SQL, etc.)
      setOutput(code.trim() || '(sem saída)');
      const target = (tests[0]?.expected_stdout || '').trim();
      const codeHas = code.includes(target);
      out = codeHas ? target : code.trim();
    }

    const allPassed = doValidate(out, error);
    setRunning(false);

    if (allPassed) {
      if (isAuthed()) {
        try {
          const res = await progressApi.completeLesson({ lesson_slug: lesson.slug, path_slug: lesson.path_slug });
          if (res.already_completed) toast.success('🎉 Lição já concluída!');
          else {
            toast.success(`🎉 Lição concluída! +${res.xp_earned} XP`);
            setStats((s) => ({ ...s, xp: res.progress.xp_total, streak: res.progress.streak }));
            // Trigger celebration if this was the last free lesson
            if (!res.already_completed) await triggerCelebrationIfMilestone();
          }
        } catch { toast.success('🎉 Lição concluída! +50 XP'); }
      } else {
        toast.success('🎉 Lição concluída! Faça login para salvar.');
      }
      setTab('tests');
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

  const passedCount = tests.filter((t) => t.passed).length;
  const nextSlug = lesson.next?.slug;

  return (
    <div className="min-h-screen flex flex-col" style={{ background: 'var(--cf-space)' }}>
      <header className="border-b sticky top-0 z-40 backdrop-blur-md" style={{ background: 'rgba(10,15,30,0.92)', borderColor: 'var(--cf-border)' }}>
        <div className="max-w-7xl mx-auto px-4 h-14 flex items-center gap-4">
          <button onClick={() => navigate(`/jornada/${lesson.path_slug}`)} className="text-slate-300 hover:text-white flex items-center gap-1 text-sm font-semibold">
            <ArrowLeft size={16} /> Trilha
          </button>
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

      <main className="flex-1 max-w-7xl w-full mx-auto p-4 grid md:grid-cols-2 gap-4">
        <div className="cf-card p-6 overflow-auto">
          <div className="text-xs font-bold uppercase tracking-wider text-[#A3E635]">{t('lesson.instruction')}</div>
          <h2 className="mt-2 font-display text-2xl font-bold text-white">{lesson.title}</h2>
          <p className="mt-4 text-slate-300 leading-relaxed whitespace-pre-line">{instruction}</p>

          {expected && (
            <div className="mt-5 p-4 rounded-xl font-code text-sm" style={{ background: 'var(--cf-panel-light)' }}>
              <div className="text-slate-400 text-xs mb-2">Saída esperada:</div>
              <pre className="text-[#A3E635] whitespace-pre-wrap">{expected}</pre>
            </div>
          )}

          {lesson.hint && (
            <>
              <button onClick={() => setShowHint((v) => !v)} className="mt-4 inline-flex items-center gap-2 text-sm font-bold text-[#A3E635] hover:underline">
                <Lightbulb size={16} /> {t('lesson.hint')}
              </button>
              {showHint && (
                <div className="mt-3 p-3 rounded-lg text-sm text-slate-300" style={{ background: 'rgba(163,230,53,0.08)', border: '1px solid rgba(163,230,53,0.2)' }}>
                  💡 {lesson.hint}
                </div>
              )}
            </>
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
      </main>
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
