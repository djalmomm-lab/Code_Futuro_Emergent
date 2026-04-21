import React from 'react';
import { Lock, Check, Play } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { JOURNEY_NODES } from '../data/mockData';

// Hexagonal-stepped journey map preview (Duolingo-like)
export default function JourneyMapSection() {
  const { t } = useLanguage();

  return (
    <section className="relative py-20 md:py-28" style={{ background: '#070A14' }}>
      <div className="absolute inset-0 cf-grid-bg opacity-30 pointer-events-none" />
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-14 items-center">
          <div>
            <h2 className="font-display text-4xl md:text-5xl font-bold text-white leading-tight">{t('journey.title')}</h2>
            <p className="mt-5 text-slate-300 text-lg max-w-lg">{t('journey.subtitle')}</p>

            <div className="mt-8 grid grid-cols-3 gap-3 max-w-md">
              <div className="cf-card p-4 text-center">
                <div className="text-2xl font-display font-bold text-[#A3E635]">7</div>
                <div className="text-[11px] uppercase text-slate-400 font-bold mt-1">Streak</div>
              </div>
              <div className="cf-card p-4 text-center">
                <div className="text-2xl font-display font-bold text-white">250</div>
                <div className="text-[11px] uppercase text-slate-400 font-bold mt-1">XP</div>
              </div>
              <div className="cf-card p-4 text-center">
                <div className="text-2xl font-display font-bold text-orange-400">5</div>
                <div className="text-[11px] uppercase text-slate-400 font-bold mt-1">Energia</div>
              </div>
            </div>
          </div>

          {/* Journey nodes */}
          <div className="cf-card p-8 relative">
            <div className="absolute top-4 right-4 flex items-center gap-2 text-xs font-bold text-slate-400 uppercase">
              <span className="w-2 h-2 rounded-full bg-[#7C3AED]" />
              Python — Cap. 1
            </div>
            <div className="flex flex-col items-center gap-0 py-6">
              {JOURNEY_NODES.map((node, i) => {
                const offsets = ['ml-0', '-ml-24', 'ml-0', 'ml-24', 'ml-0'];
                const isDone = node.status === 'done';
                const isActive = node.status === 'active';
                const isLocked = node.status === 'locked';
                return (
                  <div key={node.id} className={`${offsets[i % offsets.length]} relative`}>
                    {i > 0 && (
                      <div className="absolute left-1/2 -translate-x-1/2 -top-8 w-1 h-8" style={{ background: isLocked && i > 2 ? 'var(--cf-border)' : '#A3E635' }} />
                    )}
                    <div className="flex flex-col items-center">
                      <button
                        className={`relative w-20 h-20 rounded-2xl flex items-center justify-center transition transform hover:scale-105 ${
                          isDone
                            ? 'bg-[#A3E635] shadow-[0_8px_0_#84CC16]'
                            : isActive
                            ? 'bg-[#7C3AED] shadow-[0_8px_0_#5B21B6] animate-pulse'
                            : 'bg-[#1C2235] shadow-[0_8px_0_#0f1425]'
                        }`}
                        style={{ clipPath: 'polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%)' }}
                      >
                        {isDone ? (
                          <Check size={28} className="text-[#0A0F1E]" strokeWidth={3} />
                        ) : isActive ? (
                          <Play size={24} className="text-white fill-white" />
                        ) : (
                          <Lock size={22} className="text-slate-500" />
                        )}
                      </button>
                      {isActive && (
                        <span className="mt-3 px-3 py-1 rounded-full text-[10px] font-bold tracking-wider" style={{ background: '#7C3AED', color: 'white' }}>
                          {t('journey.continue')}
                        </span>
                      )}
                      <span className="mt-2 text-[11px] text-slate-400 font-semibold">{node.title}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
