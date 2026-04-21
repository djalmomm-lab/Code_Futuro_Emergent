import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Flame, Zap, Star, Trophy, Play, BookOpen, Target, ChevronRight } from 'lucide-react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { useLanguage } from '../context/LanguageContext';
import { USER_MOCK, PATHS_MOCK, MODULES, LEADERBOARD } from '../data/mockData';
import { Button } from '../components/ui/button';
import { authApi, leaderboardApi, isAuthed } from '../lib/api';

export default function Dashboard() {
  const { t } = useLanguage();
  const navigate = useNavigate();
  const [user, setUser] = useState({ name: USER_MOCK.name });
  const [progress, setProgress] = useState(USER_MOCK);
  const [board, setBoard] = useState(LEADERBOARD);

  useEffect(() => {
    if (!isAuthed()) { navigate('/login'); return; }
    (async () => {
      try {
        const me = await authApi.me();
        setUser(me.user);
        if (me.progress) {
          setProgress({
            name: me.user.name,
            streak: me.progress.streak,
            xpToday: me.progress.xp_today,
            dailyGoal: me.progress.daily_goal,
            energy: me.progress.energy,
            maxEnergy: me.progress.max_energy,
            level: me.progress.level,
            xpTotal: me.progress.xp_total,
            tokens: me.progress.tokens,
          });
        }
        const lb = await leaderboardApi.get('week');
        if (lb.rows?.length > 0) {
          setBoard(lb.rows.slice(0, 5).map((r, i) => ({
            rank: i + 1,
            name: r.name,
            xp: r.xp,
            streak: r.streak >= 7 ? '7+' : String(r.streak),
            avatar: `https://api.dicebear.com/7.x/identicon/svg?seed=${r.user_id}`,
          })));
        }
      } catch (e) {
        // fallback to mocks
      }
    })();
  }, [navigate]);

  const progressPct = Math.min(100, (progress.xpToday / progress.dailyGoal) * 100);

  const currentPath = PATHS_MOCK[0];
  const moduleColor = MODULES.find((m) => m.id === currentPath.module)?.color || '#7C3AED';

  return (
    <div className="min-h-screen" style={{ background: 'var(--cf-space)' }}>
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="flex items-end justify-between flex-wrap gap-4">
          <div>
            <div className="text-sm text-slate-400 font-semibold">{t('dashboard.today')}</div>
            <h1 className="font-display text-3xl md:text-4xl font-bold text-white">{t('dashboard.greeting')}, {user.name} 👋</h1>
          </div>
          <div className="flex items-center gap-3">
            <StatPill icon={<Flame size={16} />} value={progress.streak} label={t('dashboard.streak')} color="#F97316" />
            <StatPill icon={<Zap size={16} />} value={`${progress.energy}/${progress.maxEnergy}`} label={t('dashboard.energy')} color="#3B82F6" />
            <StatPill icon={<Star size={16} />} value={progress.xpTotal} label="XP" color="#A3E635" />
            <StatPill icon={<Trophy size={16} />} value={progress.level} label={t('dashboard.level')} color="#7C3AED" />
          </div>
        </div>

        {/* Continue learning */}
        <div className="mt-8 grid lg:grid-cols-3 gap-5">
          <div className="lg:col-span-2 cf-card overflow-hidden relative">
            <div className="absolute -top-20 -right-20 w-60 h-60 rounded-full blur-3xl opacity-40" style={{ background: moduleColor }} />
            <div className="relative p-6 md:p-8">
              <div className="text-xs font-bold uppercase tracking-wider" style={{ color: moduleColor }}>{t('dashboard.continueLearning')}</div>
              <h2 className="mt-2 font-display text-2xl md:text-3xl font-bold text-white">{currentPath.name}</h2>
              <p className="text-sm text-slate-400 mt-1">Capítulo 1 · Lição 3 de {currentPath.lessons}</p>

              <div className="mt-5">
                <div className="flex items-center justify-between text-xs text-slate-400 font-semibold mb-2">
                  <span>{t('dashboard.progress')}</span>
                  <span>{currentPath.completed}/{currentPath.lessons}</span>
                </div>
                <div className="h-2 rounded-full bg-[#1C2235] overflow-hidden">
                  <div className="h-full rounded-full transition-all" style={{ width: `${(currentPath.completed / currentPath.lessons) * 100}%`, background: moduleColor }} />
                </div>
              </div>

              <Button onClick={() => navigate('/licao/ola-mundo')} className="mt-6 cf-btn-lime h-12 px-6 rounded-full inline-flex items-center gap-2">
                <Play size={16} /> {t('dashboard.resume')}
              </Button>
            </div>
          </div>

          <div className="cf-card p-6">
            <div className="flex items-center gap-2 text-sm font-bold text-white">
              <Target size={16} className="text-[#A3E635]" /> {t('dashboard.dailyGoal')}
            </div>
            <div className="mt-4 relative w-full flex justify-center">
              <svg width="180" height="180" viewBox="0 0 180 180" className="-rotate-90">
                <circle cx="90" cy="90" r="70" fill="none" stroke="#1C2235" strokeWidth="14" />
                <circle cx="90" cy="90" r="70" fill="none" stroke="#A3E635" strokeWidth="14" strokeLinecap="round" strokeDasharray={`${2 * Math.PI * 70}`} strokeDashoffset={`${2 * Math.PI * 70 * (1 - progressPct / 100)}`} style={{ transition: 'stroke-dashoffset 1s ease' }} />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <div className="font-display text-3xl font-bold text-white">{progress.xpToday}</div>
                <div className="text-xs text-slate-400">/ {progress.dailyGoal} XP</div>
              </div>
            </div>
            <div className="mt-4 text-center text-xs text-slate-400">{t('dashboard.xpToday')}</div>
          </div>
        </div>

        {/* Paths + Leaderboard */}
        <div className="mt-8 grid lg:grid-cols-3 gap-5">
          <div className="lg:col-span-2">
            <h3 className="font-display text-xl font-bold text-white mb-4 flex items-center gap-2">
              <BookOpen size={18} /> {t('dashboard.yourPaths')}
            </h3>
            <div className="grid sm:grid-cols-2 gap-4">
              {PATHS_MOCK.map((p) => {
                const color = MODULES.find((m) => m.id === p.module)?.color || '#A3E635';
                const pct = (p.completed / p.lessons) * 100;
                return (
                  <Link key={p.id} to={`/jornada/${p.id}`} className="cf-card cf-card-hover p-5 flex flex-col">
                    <div className="flex items-center justify-between">
                      <div className="w-10 h-10 rounded-xl flex items-center justify-center font-display font-bold text-white text-sm" style={{ background: color }}>
                        {p.name.substring(0, 2).toUpperCase()}
                      </div>
                      <ChevronRight size={18} className="text-slate-500" />
                    </div>
                    <h4 className="mt-4 font-display font-bold text-white">{p.name}</h4>
                    <div className="mt-3 text-xs text-slate-400">{p.completed}/{p.lessons} lições</div>
                    <div className="mt-2 h-1.5 rounded-full bg-[#1C2235] overflow-hidden">
                      <div className="h-full rounded-full" style={{ width: `${pct}%`, background: color }} />
                    </div>
                  </Link>
                );
              })}
            </div>
          </div>

          <div>
            <h3 className="font-display text-xl font-bold text-white mb-4 flex items-center gap-2">
              <Trophy size={18} /> Leaderboard
            </h3>
            <div className="cf-card p-4">
              <ul className="space-y-1">
                {board.slice(0, 5).map((p) => (
                  <li key={p.rank} className="flex items-center gap-3 px-2 py-2">
                    <span className="w-6 text-slate-400 font-bold text-sm text-center">{p.rank}</span>
                    <img src={p.avatar} alt={p.name} className="w-8 h-8 rounded-full" />
                    <span className="flex-1 text-sm font-bold text-white truncate">{p.name}</span>
                    <span className="text-sm font-display font-bold text-[#A3E635]">{p.xp}</span>
                  </li>
                ))}
              </ul>
              <Link to="/leaderboard" className="mt-3 block text-center text-xs font-bold text-[#A3E635] hover:underline">
                Ver ranking completo →
              </Link>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}

function StatPill({ icon, value, label, color }) {
  return (
    <div className="flex items-center gap-2 px-3 py-2 rounded-full cf-card">
      <span className="w-7 h-7 rounded-full flex items-center justify-center" style={{ background: `${color}22`, color }}>{icon}</span>
      <div className="leading-tight">
        <div className="font-display font-bold text-white text-sm">{value}</div>
        <div className="text-[10px] uppercase text-slate-400 font-bold tracking-wider">{label}</div>
      </div>
    </div>
  );
}
