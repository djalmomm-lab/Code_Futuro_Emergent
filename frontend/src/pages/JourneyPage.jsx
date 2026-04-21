import React from 'react';
import { Link, useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Lock, Check, Play, Flame, Star, Zap } from 'lucide-react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { useLanguage } from '../context/LanguageContext';
import { USER_MOCK } from '../data/mockData';

const CHAPTERS = [
  {
    title: 'Capítulo 1: Fundamentos',
    color: '#7C3AED',
    lessons: [
      { id: 1, title: 'Olá, Mundo!', slug: 'ola-mundo', status: 'done' },
      { id: 2, title: 'Variáveis', slug: 'variaveis', status: 'done' },
      { id: 3, title: 'Tipos de Dados', slug: 'tipos', status: 'active' },
      { id: 4, title: 'Operadores', slug: 'operadores', status: 'locked' },
    ],
  },
  {
    title: 'Capítulo 2: Controle de Fluxo',
    color: '#3B82F6',
    lessons: [
      { id: 5, title: 'if / else', slug: 'if-else', status: 'locked' },
      { id: 6, title: 'Loop while', slug: 'while', status: 'locked' },
    ],
  },
];

export default function JourneyPage() {
  const { slug } = useParams();
  const navigate = useNavigate();
  const { t } = useLanguage();

  const total = CHAPTERS.reduce((a, c) => a + c.lessons.length, 0);
  const done = CHAPTERS.reduce((a, c) => a + c.lessons.filter((l) => l.status === 'done').length, 0);
  const pct = (done / total) * 100;

  return (
    <div className="min-h-screen" style={{ background: 'var(--cf-space)' }}>
      <Navbar />
      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <button onClick={() => navigate('/dashboard')} className="text-slate-400 hover:text-white flex items-center gap-2 text-sm font-semibold mb-6">
          <ArrowLeft size={16} /> Dashboard
        </button>

        <div className="cf-card p-6 md:p-8 relative overflow-hidden">
          <div className="absolute -top-20 -right-20 w-60 h-60 rounded-full blur-3xl opacity-50" style={{ background: '#7C3AED' }} />
          <div className="relative flex items-start justify-between flex-wrap gap-4">
            <div>
              <div className="text-xs text-slate-400 font-bold uppercase tracking-wider">Python</div>
              <h1 className="font-display text-3xl md:text-4xl font-bold text-white mt-1">Python do Zero</h1>
              <p className="mt-2 text-sm text-slate-400 max-w-xl">Aprenda Python do absoluto zero com lições interativas, testes automáticos e projetos práticos.</p>
            </div>
            <div className="flex items-center gap-3">
              <span className="flex items-center gap-1.5 text-orange-400 font-bold text-sm"><Flame size={14} /> {USER_MOCK.streak}</span>
              <span className="flex items-center gap-1.5 text-[#A3E635] font-bold text-sm"><Star size={14} /> {USER_MOCK.xpTotal}</span>
              <span className="flex items-center gap-1.5 text-blue-400 font-bold text-sm"><Zap size={14} /> {USER_MOCK.energy}</span>
            </div>
          </div>

          <div className="relative mt-6">
            <div className="flex items-center justify-between text-xs text-slate-400 font-semibold mb-2">
              <span>Progresso da jornada</span>
              <span>{done}/{total} lições ({Math.round(pct)}%)</span>
            </div>
            <div className="h-2.5 rounded-full bg-[#1C2235] overflow-hidden">
              <div className="h-full rounded-full" style={{ width: `${pct}%`, background: 'linear-gradient(90deg, #A3E635, #7C3AED)' }} />
            </div>
          </div>
        </div>

        <div className="mt-8 space-y-8">
          {CHAPTERS.map((chap, ci) => (
            <div key={ci}>
              <div className="flex items-center gap-3 mb-5">
                <div className="w-2 h-8 rounded-full" style={{ background: chap.color }} />
                <h2 className="font-display text-xl font-bold text-white">{chap.title}</h2>
              </div>

              <div className="flex flex-col items-center">
                {chap.lessons.map((lesson, i) => {
                  const isDone = lesson.status === 'done';
                  const isActive = lesson.status === 'active';
                  const isLocked = lesson.status === 'locked';
                  const offsetX = [0, -80, 80, -40, 40][i % 5];
                  return (
                    <div key={lesson.id} style={{ marginLeft: offsetX }} className="relative flex flex-col items-center">
                      {i > 0 && (
                        <div className="w-1 h-8" style={{ background: isLocked && !chap.lessons[i - 1].status === 'done' ? 'var(--cf-border)' : chap.color }} />
                      )}
                      <Link
                        to={isLocked ? '#' : `/licao/${lesson.slug}`}
                        className={`relative w-20 h-20 flex items-center justify-center transform transition hover:scale-110 ${isLocked ? 'cursor-not-allowed' : ''}`}
                        onClick={(e) => { if (isLocked) e.preventDefault(); }}
                      >
                        <div
                          className={`w-20 h-20 flex items-center justify-center ${isDone ? 'bg-[#A3E635]' : isActive ? 'animate-pulse' : 'bg-[#1C2235]'}`}
                          style={{
                            clipPath: 'polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%)',
                            background: isDone ? '#A3E635' : isActive ? chap.color : '#1C2235',
                            boxShadow: isDone ? '0 8px 0 #84CC16' : isActive ? `0 8px 0 ${chap.color}99` : '0 8px 0 #0f1425',
                          }}
                        >
                          {isDone ? <Check size={28} className="text-[#0A0F1E]" strokeWidth={3} /> : isActive ? <Play size={24} className="text-white fill-white" /> : <Lock size={22} className="text-slate-500" />}
                        </div>
                      </Link>
                      <span className={`mt-3 text-sm font-bold ${isLocked ? 'text-slate-500' : 'text-white'}`}>{lesson.title}</span>
                      {isActive && (
                        <span className="mt-1.5 px-3 py-1 rounded-full text-[10px] font-bold tracking-wider text-white" style={{ background: chap.color }}>
                          CONTINUAR
                        </span>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </main>
      <Footer />
    </div>
  );
}
