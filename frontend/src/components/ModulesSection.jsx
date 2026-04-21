import React from 'react';
import { ArrowRight, Sparkles } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { MODULES } from '../data/mockData';
import { useNavigate } from 'react-router-dom';

export default function ModulesSection() {
  const { t } = useLanguage();
  const navigate = useNavigate();

  return (
    <section className="relative py-20 md:py-28">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-2xl">
          <h2 className="font-display text-4xl md:text-5xl font-bold text-white leading-tight">{t('modules.title')}</h2>
          <p className="mt-5 text-slate-300 text-lg">{t('modules.subtitle')}</p>
        </div>

        <div className="mt-10 grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {MODULES.map((m, idx) => {
            const tkey = `modules.m${idx + 1}`;
            return (
              <div
                key={m.id}
                className="relative cf-card cf-card-hover p-6 overflow-hidden group cursor-pointer"
                onClick={() => navigate('/dashboard')}
              >
                <div
                  className="absolute -top-16 -right-16 w-40 h-40 rounded-full blur-3xl opacity-70 group-hover:opacity-100 transition"
                  style={{ background: m.color }}
                />
                <div className="relative">
                  <div className="flex items-center justify-between">
                    <div
                      className="w-12 h-12 rounded-2xl flex items-center justify-center font-display font-bold text-white text-xl"
                      style={{ background: m.color }}
                    >
                      0{idx + 1}
                    </div>
                    <span className="text-[11px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full" style={{ background: m.bg, color: m.color }}>
                      {t(`${tkey}.age`)}
                    </span>
                  </div>
                  <h3 className="mt-5 font-display text-xl font-bold text-white">{t(`${tkey}.name`)}</h3>
                  <p className="mt-2 text-sm text-slate-400 leading-relaxed">{t(`${tkey}.desc`)}</p>

                  <div className="mt-5 pt-4 border-t flex items-center justify-between" style={{ borderColor: 'var(--cf-border)' }}>
                    <div className="flex items-center gap-1.5 text-xs text-slate-400">
                      <Sparkles size={14} style={{ color: m.color }} />
                      <span className="font-bold">{m.lessons} {t('modules.lessons')}</span>
                    </div>
                    <span className="text-xs font-bold flex items-center gap-1 transition" style={{ color: m.color }}>
                      {t('modules.start')} <ArrowRight size={14} />
                    </span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
