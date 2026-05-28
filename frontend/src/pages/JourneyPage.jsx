import React, { useEffect, useState } from 'react';
import { Link, useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Lock, Check, Play, Flame, Star, Zap, Crown, RefreshCw, AlertCircle } from 'lucide-react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { useLanguage } from '../context/LanguageContext';
import { pathsApi, authApi, isAuthed } from '../lib/api';
import { logError } from '../lib/logger';

const LOAD_TIMEOUT_MS = 10_000;

export default function JourneyPage() {
  const { slug } = useParams();
  const navigate = useNavigate();
  const { t } = useLanguage();

  const [path, setPath] = useState(null);
  const [lessons, setLessons] = useState([]);
  const [stats, setStats] = useState({ streak: 0, xp: 0, energy: 5 });
  const [completed, setCompleted] = useState(new Set());
  const [isPro, setIsPro] = useState(false);
  const [freeLimit, setFreeLimit] = useState(3);
  const [loadError, setLoadError] = useState(null);
  const [loadKey, setLoadKey] = useState(0); // increment to retry

  useEffect(() => {
    let cancelled = false;
    setLoadError(null);
    setPath(null);

    const timeout = setTimeout(() => {
      if (!cancelled) setLoadError('timeout');
    }, LOAD_TIMEOUT_MS);

    (async () => {
      try {
        const res = await pathsApi.get(slug);
        if (cancelled) return;
        clearTimeout(timeout);
        setPath(res.path);
        const lessonList = res.lessons || [];
        setLessons(lessonList);
        setIsPro(!!res.is_pro);
        setFreeLimit(res.free_limit || 3);
        // Bug 3: populate completed set from backend is_completed flag
        setCompleted(new Set(lessonList.filter((l) => l.is_completed).map((l) => l.slug)));
      } catch (err) {
        if (cancelled) return;
        clearTimeout(timeout);
        logError('JourneyPage.loadPath', err, { slug });
        setLoadError('api');
      }
      if (!cancelled && isAuthed()) {
        try {
          const me = await authApi.me();
          if (!cancelled && me.progress) {
            setStats({
              streak: me.progress.streak,
              xp: me.progress.xp_total,
              energy: me.progress.energy,
            });
          }
        } catch (err) {
          logError('JourneyPage.loadProgress', err);
        }
      }
    })();

    return () => { cancelled = true; clearTimeout(timeout); };
  }, [slug, loadKey]);

  if (loadError) {
    return (
      <div className="min-h-screen" style={{ background: 'var(--cf-space)' }}>
        <Navbar />
        <div className="max-w-5xl mx-auto px-4 py-20 flex flex-col items-center gap-4 text-center">
          <AlertCircle size={40} className="text-slate-500" />
          <div className="text-white font-bold text-lg">
            {loadError === 'timeout' ? 'A trilha demorou demais para carregar.' : 'Não foi possível carregar a trilha.'}
          </div>
          <div className="text-slate-400 text-sm">Verifique sua conexão e tente novamente.</div>
          <button
            onClick={() => setLoadKey((k) => k + 1)}
            className="mt-2 flex items-center gap-2 px-5 py-2.5 rounded-lg cf-btn-lime text-sm font-bold"
          >
            <RefreshCw size={14} /> Tentar novamente
          </button>
          <button onClick={() => navigate('/catalogo')} className="text-slate-400 hover:text-white text-sm">
            ← Voltar ao catálogo
          </button>
        </div>
        <Footer />
      </div>
    );
  }

  if (!path) {
    return (
      <div className="min-h-screen" style={{ background: 'var(--cf-space)' }}>
        <Navbar />
        <div className="max-w-5xl mx-auto px-4 py-20 flex flex-col items-center gap-3">
          {/* Skeleton cards enquanto carrega */}
          <div className="w-full animate-pulse space-y-4">
            <div className="h-32 rounded-2xl bg-[#1C2235]" />
            <div className="h-8 w-48 rounded-lg bg-[#1C2235]" />
            <div className="flex flex-col items-center gap-6 pt-4">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="w-20 h-20 rounded-full bg-[#1C2235]" />
              ))}
            </div>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  // Group lessons by chapter
  const chapters = {};
  lessons.forEach((l) => {
    const key = l.chapter || 'Capítulo 1';
    if (!chapters[key]) chapters[key] = [];
    chapters[key].push(l);
  });
  const chapterOrder = Object.keys(chapters);

  // Figure out first incomplete = active (only among unlocked lessons)
  const firstIncompleteOrder = lessons.find((l) => !completed.has(l.slug) && !l.requires_pro)?.order;

  const statusOf = (lesson) => {
    if (completed.has(lesson.slug)) return 'done';
    if (lesson.requires_pro) return 'locked';
    if (lesson.order === firstIncompleteOrder) return 'active';
    return 'unlocked';
  };

  const done = completed.size;
  const total = lessons.length || 1;
  const pct = (done / total) * 100;

  return (
    <div className="min-h-screen" style={{ background: 'var(--cf-space)' }}>
      <Navbar />
      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <button onClick={() => navigate('/catalogo')} className="text-slate-400 hover:text-white flex items-center gap-2 text-sm font-semibold mb-6">
          <ArrowLeft size={16} /> Catálogo
        </button>

        <div className="cf-card p-6 md:p-8 relative overflow-hidden">
          <div className="absolute -top-20 -right-20 w-60 h-60 rounded-full blur-3xl opacity-50" style={{ background: path.color }} />
          <div className="relative flex items-start justify-between flex-wrap gap-4">
            <div className="flex gap-4 items-center">
              <div className="w-16 h-16 rounded-2xl flex items-center justify-center font-display font-bold text-white text-xl shrink-0" style={{ background: path.color }}>
                {path.name.substring(0, 2).toUpperCase()}
              </div>
              <div>
                <div className="text-xs text-slate-400 font-bold uppercase tracking-wider">Trilha</div>
                <h1 className="font-display text-3xl md:text-4xl font-bold text-white mt-1">{path.name}</h1>
                <p className="mt-1 text-sm text-slate-400 max-w-xl">{path.desc}</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <span className="flex items-center gap-1.5 text-orange-400 font-bold text-sm"><Flame size={14} /> {stats.streak}</span>
              <span className="flex items-center gap-1.5 text-[#A3E635] font-bold text-sm"><Star size={14} /> {stats.xp}</span>
              <span className="flex items-center gap-1.5 text-blue-400 font-bold text-sm"><Zap size={14} /> {stats.energy}</span>
            </div>
          </div>

          <div className="relative mt-6">
            <div className="flex items-center justify-between text-xs text-slate-400 font-semibold mb-2">
              <span>Progresso</span>
              <span>{done}/{total} lições ({Math.round(pct)}%)</span>
            </div>
            <div className="h-2.5 rounded-full bg-[#1C2235] overflow-hidden">
              <div className="h-full rounded-full transition-all" style={{ width: `${pct}%`, background: path.color }} />
            </div>
          </div>
        </div>

        {!isPro && lessons.some((l) => l.requires_pro) && (
          <button
            onClick={() => navigate('/planos')}
            data-testid="journey-upgrade-banner"
            className="mt-6 w-full text-left cf-card p-5 flex items-center gap-4 hover:scale-[1.01] transition group"
            style={{
              background: 'linear-gradient(90deg, rgba(163,230,53,0.08), rgba(124,58,237,0.08))',
              border: '1px solid rgba(163,230,53,0.25)',
            }}
          >
            <div className="w-12 h-12 rounded-xl flex items-center justify-center shrink-0"
                 style={{ background: 'rgba(163,230,53,0.15)', border: '1px solid rgba(163,230,53,0.3)' }}>
              <Crown size={22} className="text-[#A3E635]" />
            </div>
            <div className="flex-1 min-w-0">
              <div className="font-display font-bold text-white text-base">Desbloqueie a trilha completa</div>
              <div className="text-sm text-slate-400 mt-0.5">
                As {freeLimit} primeiras lições são gratuitas. Ative o <span className="text-[#A3E635] font-semibold">Pro</span> para acessar tudo.
              </div>
            </div>
            <span className="px-4 py-2 rounded-lg cf-btn-lime text-xs font-bold shrink-0 group-hover:translate-x-0.5 transition">
              Ver planos
            </span>
          </button>
        )}

        <div className="mt-8 space-y-10">
          {chapterOrder.map((chapKey, ci) => {
            const chapLessons = chapters[chapKey];
            return (
              <div key={chapKey}>
                <div className="flex items-center gap-3 mb-5">
                  <div className="w-2 h-8 rounded-full" style={{ background: path.color }} />
                  <h2 className="font-display text-xl font-bold text-white">{chapKey}</h2>
                </div>

                <div className="flex flex-col items-center">
                  {chapLessons.map((lesson, i) => {
                    const status = statusOf(lesson);
                    const isDone = status === 'done';
                    const isActive = status === 'active';
                    const isUnlocked = status === 'unlocked';
                    const isLocked = status === 'locked';
                    const offsetX = [0, -80, 80, -40, 40, 0, -60, 60][i % 8];
                    return (
                      <div key={lesson.slug} style={{ marginLeft: offsetX }} className="relative flex flex-col items-center">
                        {i > 0 && (
                          <div className="w-1 h-8" style={{ background: isLocked ? 'var(--cf-border)' : path.color }} />
                        )}
                        <Link
                          to={isLocked ? '/planos' : `/licao/${lesson.slug}`}
                          data-testid={isLocked ? `lesson-locked-${lesson.slug}` : `lesson-node-${lesson.slug}`}
                          className={`relative w-20 h-20 flex items-center justify-center transform transition hover:scale-110`}
                          title={isLocked ? 'Lição Pro — clique para ver planos' : lesson.title}
                        >
                          <div
                            className="w-20 h-20 flex items-center justify-center"
                            style={{
                              clipPath: 'polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%)',
                              background: isDone ? '#A3E635' : isActive ? path.color : isUnlocked ? `${path.color}66` : '#1C2235',
                              boxShadow: isDone ? '0 8px 0 #84CC16' : isActive ? `0 8px 0 ${path.color}99` : isUnlocked ? `0 8px 0 ${path.color}44` : '0 8px 0 #0f1425',
                            }}
                          >
                            {isDone ? <Check size={28} className="text-[#0A0F1E]" strokeWidth={3} /> : (isActive || isUnlocked) ? <Play size={24} className="text-white fill-white" /> : <Lock size={22} className="text-slate-500" />}
                          </div>
                          {isLocked && (
                            <span
                              className="absolute -top-1 -right-1 px-1.5 py-0.5 rounded-md text-[9px] font-bold tracking-wider"
                              style={{ background: '#A3E635', color: '#0A0F1E' }}
                            >
                              PRO
                            </span>
                          )}
                        </Link>
                        <span className={`mt-3 text-sm font-bold max-w-[220px] text-center ${isLocked ? 'text-slate-500' : 'text-white'}`}>{lesson.title}</span>
                        {isActive && (
                          <span className="mt-1.5 px-3 py-1 rounded-full text-[10px] font-bold tracking-wider text-white" style={{ background: path.color }}>
                            CONTINUAR
                          </span>
                        )}                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>
      </main>
      <Footer />
    </div>
  );
}
