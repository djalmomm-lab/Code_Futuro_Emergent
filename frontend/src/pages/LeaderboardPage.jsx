import React, { useState, useEffect } from 'react';
import { Flame, Trophy, TrendingUp, Crown, Medal, Award } from 'lucide-react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { useLanguage } from '../context/LanguageContext';
import { LEADERBOARD } from '../data/mockData';
import { leaderboardApi } from '../lib/api';
import { logError } from '../lib/logger';

const EXTENDED = [
  ...LEADERBOARD,
  { rank: 8, name: 'Drew', xp: 1380, streak: '1', avatar: 'https://i.pravatar.cc/120?img=48' },
  { rank: 9, name: 'Quinn', xp: 1210, streak: '5', avatar: 'https://i.pravatar.cc/120?img=33' },
  { rank: 10, name: 'Sage', xp: 1050, streak: '2', avatar: 'https://i.pravatar.cc/120?img=51' },
  { rank: 11, name: 'Rowan', xp: 920, streak: '7+', avatar: 'https://i.pravatar.cc/120?img=3' },
  { rank: 12, name: 'Parker', xp: 780, streak: '3', avatar: 'https://i.pravatar.cc/120?img=16' },
];

const rankIcon = (rank) => {
  if (rank === 1) return <Crown size={20} className="text-yellow-400" />;
  if (rank === 2) return <Medal size={20} className="text-slate-300" />;
  if (rank === 3) return <Award size={20} className="text-orange-400" />;
  return <span className="text-slate-400 font-bold text-sm">{rank}</span>;
};

export default function LeaderboardPage() {
  const { t } = useLanguage();
  const [tab, setTab] = useState('week');
  const [rows, setRows] = useState(EXTENDED);

  useEffect(() => {
    (async () => {
      try {
        const r = await leaderboardApi.get(tab);
        if (r.rows?.length) {
          setRows(r.rows.map((p, i) => ({
            rank: i + 1,
            name: p.name,
            xp: p.xp,
            streak: p.streak >= 7 ? '7+' : String(p.streak),
            avatar: `https://api.dicebear.com/7.x/identicon/svg?seed=${p.user_id}`,
          })));
        }
      } catch (err) {
        logError('LeaderboardPage.load', err, { tab });
      }
    })();
  }, [tab]);

  return (
    <div className="min-h-screen" style={{ background: 'var(--cf-space)' }}>
      <Navbar />
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="text-center mb-8">
          <div className="inline-flex w-20 h-20 rounded-3xl items-center justify-center mb-4" style={{ background: 'rgba(163,230,53,0.15)' }}>
            <Trophy size={36} className="text-[#A3E635]" />
          </div>
          <h1 className="font-display text-4xl font-bold text-white">{t('leaderboard.league')}</h1>
          <p className="mt-2 text-slate-400">{t('leaderboard.topAdvance')} para a Liga Mestre</p>
        </div>

        <div className="flex items-center justify-center gap-2 mb-6">
          {[
            { id: 'day', label: 'Hoje' },
            { id: 'week', label: 'Semana' },
            { id: 'all', label: 'Todos os tempos' },
          ].map((tb) => (
            <button key={tb.id} onClick={() => setTab(tb.id)} className={`px-4 py-2 rounded-full text-sm font-bold transition ${tab === tb.id ? 'bg-[#A3E635] text-[#0A0F1E]' : 'bg-[#141824] text-slate-300 border hover:text-white'}`} style={tab === tb.id ? {} : { borderColor: 'var(--cf-border)' }}>
              {tb.label}
            </button>
          ))}
        </div>

        <div className="cf-card p-2">
          <ul>
            {rows.map((p, i) => (
              <li key={p.rank}>
                {i === 7 && (
                  <div className="my-2 py-2 rounded-xl text-center text-[11px] font-bold uppercase tracking-wider flex items-center justify-center gap-1.5" style={{ background: 'rgba(163,230,53,0.1)', color: '#A3E635' }}>
                    <TrendingUp size={12} />
                    {t('leaderboard.promotion')}
                    <TrendingUp size={12} />
                  </div>
                )}
                <div className={`flex items-center gap-3 px-4 py-3 rounded-xl ${p.rank <= 3 ? 'bg-[#1C2235]' : ''}`}>
                  <div className="w-8 flex justify-center">{rankIcon(p.rank)}</div>
                  <img src={p.avatar} alt={p.name} className="w-11 h-11 rounded-full ring-2 ring-[#0A0F1E]" />
                  <div className="flex-1 min-w-0">
                    <div className="font-bold text-white truncate">{p.name}</div>
                    <div className="flex items-center gap-1 text-[11px] text-orange-400">
                      <Flame size={11} className="fill-current" />
                      <span>{p.streak} {t('leaderboard.days')}</span>
                    </div>
                  </div>
                  <div className="text-lg font-display font-bold text-[#A3E635]">{p.xp.toLocaleString('pt-BR')}</div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </main>
      <Footer />
    </div>
  );
}
