import React from 'react';
import { Flame, Snowflake, Calendar } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export default function StreakSection() {
  const { t } = useLanguage();
  const days = Array.from({ length: 30 }, (_, i) => i + 1);
  const streakDays = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];

  return (
    <section className="relative py-20 md:py-28" style={{ background: '#070A14' }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-14 items-center">
          <div className="cf-card p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-2xl flex items-center justify-center" style={{ background: 'rgba(249,115,22,0.15)' }}>
                  <Flame size={22} className="text-orange-400" />
                </div>
                <div>
                  <div className="font-display font-bold text-white text-xl">12 {t('streak.daysStreak')}</div>
                  <div className="text-xs text-slate-400">{t('streak.returnTomorrow')}</div>
                </div>
              </div>
            </div>

            <div className="rounded-xl p-4 mb-4" style={{ background: 'var(--cf-panel-light)' }}>
              <div className="flex items-center justify-between mb-3">
                <button className="text-slate-400 hover:text-white"><Calendar size={14} /></button>
                <span className="text-sm font-bold text-white">Janeiro 2026</span>
                <button className="text-slate-400 hover:text-white">›</button>
              </div>
              <div className="grid grid-cols-7 gap-1.5">
                {['D', 'S', 'T', 'Q', 'Q', 'S', 'S'].map((d, i) => (
                  <div key={i} className="text-center text-[10px] font-bold text-slate-500 pb-1">{d}</div>
                ))}
                {days.map((d) => {
                  const inStreak = streakDays.includes(d);
                  const isToday = d === 12;
                  return (
                    <div
                      key={d}
                      className={`aspect-square rounded-md flex items-center justify-center text-xs font-bold ${
                        isToday
                          ? 'bg-[#A3E635] text-[#0A0F1E] ring-2 ring-[#A3E635]/40'
                          : inStreak
                          ? 'bg-orange-500/25 text-orange-300'
                          : 'text-slate-500'
                      }`}
                    >
                      {d}
                    </div>
                  );
                })}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="rounded-xl p-4 flex items-center gap-3" style={{ background: 'rgba(163,230,53,0.08)', border: '1px solid rgba(163,230,53,0.25)' }}>
                <div className="w-10 h-10 rounded-full bg-[#A3E635]/20 flex items-center justify-center">
                  <Flame size={18} className="text-[#A3E635]" />
                </div>
                <div>
                  <div className="text-[11px] text-slate-400 uppercase font-bold">{t('streak.doubleOrNothing')}</div>
                  <div className="text-sm text-white font-bold">{t('streak.dayOf')} 5 {t('streak.of')} 7</div>
                </div>
              </div>
              <div className="rounded-xl p-4 flex items-center gap-3" style={{ background: 'rgba(59,130,246,0.08)', border: '1px solid rgba(59,130,246,0.25)' }}>
                <div className="w-10 h-10 rounded-full bg-blue-500/20 flex items-center justify-center">
                  <Snowflake size={18} className="text-blue-400" />
                </div>
                <div>
                  <div className="text-[11px] text-slate-400 uppercase font-bold">{t('streak.streakFreeze')}</div>
                  <div className="text-sm text-white font-bold">2 {t('streak.left')}</div>
                </div>
              </div>
            </div>
          </div>

          <div className="order-first lg:order-last">
            <h2 className="font-display text-4xl md:text-5xl font-bold text-white leading-tight">{t('streak.title')}</h2>
            <p className="mt-5 text-slate-300 text-lg max-w-lg">{t('streak.subtitle')}</p>
            <ul className="mt-6 space-y-3">
              {[
                { icon: Flame, color: 'text-orange-400', bg: 'bg-orange-500/15', text: 'Sequência diária que motiva' },
                { icon: Snowflake, color: 'text-blue-400', bg: 'bg-blue-500/15', text: 'Streak Freeze protege seu progresso' },
                { icon: Calendar, color: 'text-[#A3E635]', bg: 'bg-[#A3E635]/15', text: 'Metas semanais e recompensas' },
              ].map((item, i) => (
                <li key={i} className="flex items-center gap-3 text-slate-200">
                  <span className={`w-10 h-10 rounded-xl flex items-center justify-center ${item.bg}`}>
                    <item.icon size={18} className={item.color} />
                  </span>
                  <span className="font-semibold">{item.text}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}
