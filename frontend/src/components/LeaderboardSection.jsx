import React from 'react';
import { Flame, Trophy, TrendingUp, Crown, Medal, Award } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { LEADERBOARD } from '../data/mockData';

const rankIcon = (rank) => {
  if (rank === 1) return <Crown size={18} className="text-yellow-400" />;
  if (rank === 2) return <Medal size={18} className="text-slate-300" />;
  if (rank === 3) return <Award size={18} className="text-orange-400" />;
  return <span className="text-slate-400 font-bold text-sm">{rank}</span>;
};

export default function LeaderboardSection() {
  const { t } = useLanguage();

  return (
    <section className="relative py-20 md:py-28">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-14 items-center">
          <div className="cf-card p-6 max-w-md mx-auto w-full">
            <div className="flex items-center gap-3 pb-4 border-b" style={{ borderColor: 'var(--cf-border)' }}>
              <div className="w-12 h-12 rounded-2xl flex items-center justify-center" style={{ background: 'rgba(163,230,53,0.15)' }}>
                <Trophy size={22} className="text-[#A3E635]" />
              </div>
              <div>
                <div className="font-display font-bold text-white text-lg">{t('leaderboard.league')}</div>
                <div className="text-xs text-slate-400">{t('leaderboard.topAdvance')}</div>
              </div>
            </div>

            <ul className="mt-4 space-y-2">
              {LEADERBOARD.slice(0, 5).map((p) => (
                <li
                  key={p.rank}
                  className={`flex items-center gap-3 px-3 py-2.5 rounded-xl ${p.rank <= 3 ? 'bg-[#1C2235]' : ''}`}
                >
                  <div className="w-7 flex justify-center">{rankIcon(p.rank)}</div>
                  <img src={p.avatar} alt={p.name} className="w-9 h-9 rounded-full ring-2 ring-[#0A0F1E]" />
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-bold text-white truncate">{p.name}</div>
                    <div className="flex items-center gap-1 text-[11px] text-orange-400">
                      <Flame size={10} className="fill-current" />
                      <span>{p.streak} {t('leaderboard.days')}</span>
                    </div>
                  </div>
                  <div className="text-sm font-display font-bold text-[#A3E635]">{p.xp.toLocaleString('pt-BR')}</div>
                </li>
              ))}
            </ul>

            <div className="mt-4 py-3 rounded-xl text-center text-[11px] font-bold uppercase tracking-wider flex items-center justify-center gap-1.5" style={{ background: 'rgba(163,230,53,0.1)', color: '#A3E635' }}>
              <TrendingUp size={12} />
              {t('leaderboard.promotion')}
              <TrendingUp size={12} />
            </div>
          </div>

          <div className="order-first lg:order-last">
            <h2 className="font-display text-4xl md:text-5xl font-bold text-white leading-tight">{t('leaderboard.title')}</h2>
            <p className="mt-5 text-slate-300 text-lg max-w-lg">{t('leaderboard.subtitle')}</p>
          </div>
        </div>
      </div>
    </section>
  );
}
