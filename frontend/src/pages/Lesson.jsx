import React, { useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { Play, RotateCcw, ChevronRight, CheckCircle2, XCircle, Flame, Zap, Star, Lightbulb, ArrowLeft } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { DEFAULT_LESSON, USER_MOCK } from '../data/mockData';
import { Button } from '../components/ui/button';
import { toast } from 'sonner';
import { progressApi, isAuthed } from '../lib/api';

export default function Lesson() {
  const { t, lang } = useLanguage();
  const { slug } = useParams();
  const navigate = useNavigate();
  const lesson = DEFAULT_LESSON;

  const [code, setCode] = useState(lesson.starter);
  const [output, setOutput] = useState('');
  const [tab, setTab] = useState('tests');
  const [tests, setTests] = useState(lesson.tests);
  const [running, setRunning] = useState(false);
  const [energy, setEnergy] = useState(USER_MOCK.energy);
  const [showHint, setShowHint] = useState(false);

  const run = async () => {
    if (energy <= 0) { toast.error('Sem energia! Aguarde o reset ou faça upgrade Pro.'); return; }
    setRunning(true);
    // consume energy via API if logged in
    if (isAuthed()) {
      try {
        const e = await progressApi.consumeEnergy();
        setEnergy(e.energy);
      } catch (err) {
        if (err.response?.status !== 429) setEnergy((e) => e - 1);
      }
    } else {
      setEnergy((e) => e - 1);
    }
    setTimeout(async () => {
      let out = '';
      try {
        const match = code.match(/print\(\s*['"]([^'"]*)['"]\s*\)/);
        if (match) out = match[1];
        else out = 'Erro: nenhum print detectado';
      } catch (e) { out = 'Erro de execução'; }

      setOutput(out);
      const newTests = tests.map((t2) => ({ ...t2, passed: out.trim().toLowerCase() === t2.expected.trim().toLowerCase() }));
      setTests(newTests);
      const allPassed = newTests.every((t2) => t2.passed);
      setRunning(false);
      setTab('console');

      if (allPassed) {
        if (isAuthed()) {
          try {
            const res = await progressApi.completeLesson({ lesson_slug: slug || lesson.slug, path_slug: 'python-zero' });
            if (res.already_completed) toast.success('🎉 Lição já concluída!');
            else toast.success(`🎉 Lição concluída! +${res.xp_earned} XP`);
          } catch { toast.success('🎉 Lição concluída! +50 XP'); }
        } else {
          toast.success('🎉 Lição concluída! +50 XP');
        }
      } else {
        toast.error('Alguns testes falharam. Tente de novo!');
      }
    }, 600);
  };

  const reset = () => { setCode(lesson.starter); setOutput(''); setTests(lesson.tests.map((t) => ({ ...t, passed: false }))); };

  const passedCount = tests.filter((t) => t.passed).length;

  return (
    <div className="min-h-screen flex flex-col" style={{ background: 'var(--cf-space)' }}>
      {/* Compact header */}
      <header className="border-b sticky top-0 z-40 backdrop-blur-md" style={{ background: 'rgba(10,15,30,0.92)', borderColor: 'var(--cf-border)' }}>
        <div className="max-w-7xl mx-auto px-4 h-14 flex items-center gap-4">
          <button onClick={() => navigate(-1)} className="text-slate-300 hover:text-white flex items-center gap-1 text-sm font-semibold">
            <ArrowLeft size={16} /> Voltar
          </button>
          <div className="flex-1 min-w-0">
            <div className="text-xs text-slate-400 truncate">{lesson.path} · {lesson.chapter}</div>
            <div className="font-display font-bold text-white truncate">{lesson.title}</div>
          </div>
          <div className="flex items-center gap-3 text-sm">
            <span className="flex items-center gap-1.5 text-orange-400 font-bold"><Flame size={14} /> {USER_MOCK.streak}</span>
            <span className="flex items-center gap-1.5 text-[#A3E635] font-bold"><Star size={14} /> {USER_MOCK.xpTotal}</span>
            <span className="flex items-center gap-1.5 text-blue-400 font-bold"><Zap size={14} /> {energy}/{USER_MOCK.maxEnergy}</span>
          </div>
        </div>
      </header>

      <main className="flex-1 max-w-7xl w-full mx-auto p-4 grid md:grid-cols-2 gap-4">
        {/* Instruction panel */}
        <div className="cf-card p-6 overflow-auto">
          <div className="text-xs font-bold uppercase tracking-wider text-[#A3E635]">{t('lesson.instruction')}</div>
          <h2 className="mt-2 font-display text-2xl font-bold text-white">{lesson.title}</h2>
          <p className="mt-4 text-slate-300 leading-relaxed">
            {lesson.instruction[lang] || lesson.instruction.pt}
          </p>

          <div className="mt-5 p-4 rounded-xl font-code text-sm" style={{ background: 'var(--cf-panel-light)' }}>
            <div className="text-slate-400 text-xs mb-2">Saída esperada:</div>
            <div className="text-[#A3E635]">{lesson.expected}</div>
          </div>

          <button onClick={() => setShowHint((v) => !v)} className="mt-4 inline-flex items-center gap-2 text-sm font-bold text-[#A3E635] hover:underline">
            <Lightbulb size={16} /> {t('lesson.hint')}
          </button>
          {showHint && (
            <div className="mt-3 p-3 rounded-lg text-sm text-slate-300" style={{ background: 'rgba(163,230,53,0.08)', border: '1px solid rgba(163,230,53,0.2)' }}>
              💡 Use <code className="font-code text-[#A3E635]">print('Olá, Mundo!')</code> — lembre-se das aspas e do caractere <code className="text-[#A3E635]">!</code>.
            </div>
          )}
        </div>

        {/* Editor + console */}
        <div className="flex flex-col gap-4">
          <div className="cf-card overflow-hidden flex flex-col min-h-[300px]">
            <div className="flex items-center justify-between px-4 py-2.5 border-b" style={{ borderColor: 'var(--cf-border)' }}>
              <div className="flex items-center gap-1.5">
                <span className="w-3 h-3 rounded-full bg-red-500/70" />
                <span className="w-3 h-3 rounded-full bg-yellow-500/70" />
                <span className="w-3 h-3 rounded-full bg-green-500/70" />
                <span className="ml-3 text-xs text-slate-400 font-code">main.py</span>
              </div>
              <div className="flex items-center gap-2">
                <button onClick={reset} className="text-slate-400 hover:text-white p-1.5 rounded-lg hover:bg-[#1C2235]" title={t('lesson.reset')}>
                  <RotateCcw size={14} />
                </button>
                <button onClick={run} disabled={running} className="inline-flex items-center gap-1.5 px-4 py-1.5 rounded-lg cf-btn-lime text-xs disabled:opacity-50">
                  <Play size={14} /> {running ? '...' : t('lesson.run')}
                </button>
              </div>
            </div>
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              spellCheck={false}
              className="flex-1 p-4 font-code text-sm bg-[#0A0F1E] text-slate-100 outline-none resize-none min-h-[240px]"
              style={{ tabSize: 4 }}
            />
          </div>

          <div className="cf-card overflow-hidden">
            <div className="flex items-center border-b" style={{ borderColor: 'var(--cf-border)' }}>
              <button onClick={() => setTab('tests')} className={`px-4 py-2.5 text-xs font-bold ${tab === 'tests' ? 'text-[#A3E635] border-b-2 border-[#A3E635]' : 'text-slate-400'}`}>
                {t('learn.testCases')}
                {passedCount > 0 && <span className="ml-2 text-[10px]">{passedCount}/{tests.length}</span>}
              </button>
              <button onClick={() => setTab('console')} className={`px-4 py-2.5 text-xs font-bold ${tab === 'console' ? 'text-[#A3E635] border-b-2 border-[#A3E635]' : 'text-slate-400'}`}>
                {t('learn.console')}
              </button>
              {passedCount === tests.length && (
                <Link to="/licao/variaveis" className="ml-auto px-4 py-2 mr-2 text-xs font-bold rounded-full cf-btn-lime inline-flex items-center gap-1">
                  {t('lesson.nextLesson')} <ChevronRight size={14} />
                </Link>
              )}
            </div>
            <div className="p-4 space-y-2 min-h-[120px] bg-[#0A0F1E]">
              {tab === 'tests' ? (
                tests.map((test, i) => (
                  <div key={test.id} className="flex items-center gap-3 text-sm">
                    {test.passed ? <CheckCircle2 size={16} className="text-[#A3E635]" /> : <XCircle size={16} className="text-slate-500" />}
                    <span className="text-slate-200 font-semibold">{t('learn.test')} #{i + 1}</span>
                    <span className="ml-auto text-xs text-slate-500 font-code truncate">expected "{test.expected}"</span>
                  </div>
                ))
              ) : (
                <div className="font-code text-xs text-slate-300 whitespace-pre-wrap">
                  <div className="text-slate-500">{`> python main.py`}</div>
                  {output && <div className="text-[#A3E635]">{output}</div>}
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
