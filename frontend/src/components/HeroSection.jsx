import React, { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from './ui/button';
import { useLanguage } from '../context/LanguageContext';
import { LANGUAGES_STACK, TOTAL_CODERS } from '../data/mockData';
import ByteMascot from './ByteMascot';

export default function HeroSection() {
  const { t } = useLanguage();
  const navigate = useNavigate();
  const scrollerRef = useRef(null);
  const [count, setCount] = useState(TOTAL_CODERS - 42000);

  useEffect(() => {
    const target = TOTAL_CODERS;
    const start = TOTAL_CODERS - 42000;
    const duration = 2200;
    const startTime = performance.now();
    let raf;
    const tick = (now) => {
      const p = Math.min(1, (now - startTime) / duration);
      const eased = 1 - Math.pow(1 - p, 3);
      setCount(Math.floor(start + (target - start) * eased));
      if (p < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, []);

  const scroll = (dir) => {
    const el = scrollerRef.current;
    if (!el) return;
    el.scrollBy({ left: dir * 320, behavior: 'smooth' });
  };

  return (
    <section className="relative overflow-hidden">
      <div className="absolute inset-0 cf-grid-bg opacity-60 pointer-events-none" />
      <div
        className="absolute -top-40 left-1/2 -translate-x-1/2 w-[800px] h-[800px] rounded-full pointer-events-none"
        style={{ background: 'radial-gradient(circle, rgba(163,230,53,0.18) 0%, transparent 60%)' }}
      />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 md:pt-24 pb-12">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div className="relative z-10">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-bold tracking-wider uppercase" style={{ background: 'rgba(163, 230, 53, 0.12)', color: '#A3E635', border: '1px solid rgba(163, 230, 53, 0.25)' }}>
              <span className="w-1.5 h-1.5 rounded-full bg-[#A3E635] animate-pulse-dot" />
              {t('hero.tagline')}
            </div>
            <h1 className="mt-5 font-display text-white font-bold leading-[1.05] text-4xl sm:text-5xl md:text-6xl">
              {t('hero.title')}
            </h1>
            <p className="mt-5 text-slate-300 text-lg max-w-xl">{t('hero.subtitle')}</p>

            <div className="mt-7 flex items-center gap-3 flex-wrap">
              <span className="text-sm text-slate-400">{t('hero.join')}</span>
              <span className="font-display font-bold text-2xl text-white tabular-nums">{count.toLocaleString('pt-BR')}</span>
              <span className="text-sm text-slate-400">{t('hero.coders')}</span>
            </div>

            <div className="mt-7 flex flex-col sm:flex-row gap-3">
              <Button onClick={() => navigate('/onboard')} className="cf-btn-lime h-14 px-8 rounded-full text-base inline-flex items-center gap-2">
                {t('hero.getStarted')}
                <ArrowRight size={18} />
              </Button>
              <Button onClick={() => navigate('/login')} variant="outline" className="h-14 px-8 rounded-full text-base border-slate-600 text-slate-200 hover:bg-[#1C2235] hover:text-white bg-transparent">
                {t('hero.hasAccount')}
              </Button>
            </div>
          </div>

          <div className="relative flex justify-center lg:justify-end">
            <div className="relative">
              <div className="absolute inset-0 rounded-full blur-3xl" style={{ background: 'radial-gradient(circle, rgba(163,230,53,0.35) 0%, transparent 70%)' }} />
              <div className="relative animate-float">
                <ByteMascot size={320} />
              </div>
              <div className="hidden md:block absolute -left-10 top-8 cf-card px-3 py-2 font-code text-xs text-[#A3E635] animate-float" style={{ animationDelay: '0.4s' }}>
                {"print('Olá, Mundo!')"}
              </div>
              <div className="hidden md:block absolute -right-4 bottom-16 cf-card px-3 py-2 text-xs animate-float" style={{ animationDelay: '1s' }}>
                <div className="flex items-center gap-2">
                  <span className="text-orange-400">🔥</span>
                  <span className="text-slate-200 font-semibold">7 dias</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-12 relative">
          <button onClick={() => scroll(-1)} aria-label="Scroll left" className="absolute left-0 top-1/2 -translate-y-1/2 z-10 w-10 h-10 rounded-full bg-[#141824] border flex items-center justify-center text-slate-300 hover:text-white hover:border-[#A3E635] transition" style={{ borderColor: 'var(--cf-border)' }}>
            <ChevronLeft size={18} />
          </button>
          <div ref={scrollerRef} className="no-scrollbar flex gap-3 overflow-x-auto py-2 px-12 snap-x">
            {LANGUAGES_STACK.map((l) => (
              <a key={l.id} href="#" className="snap-start shrink-0 flex flex-col items-center justify-center w-24 h-24 rounded-2xl cf-card cf-card-hover">
                <div className="w-10 h-10 rounded-xl flex items-center justify-center font-display font-bold text-white text-sm mb-2" style={{ background: l.color }}>
                  {l.name.substring(0, 2).toUpperCase()}
                </div>
                <span className="text-[11px] font-semibold text-slate-300">{l.name}</span>
              </a>
            ))}
          </div>
          <button onClick={() => scroll(1)} aria-label="Scroll right" className="absolute right-0 top-1/2 -translate-y-1/2 z-10 w-10 h-10 rounded-full bg-[#141824] border flex items-center justify-center text-slate-300 hover:text-white hover:border-[#A3E635] transition" style={{ borderColor: 'var(--cf-border)' }}>
            <ChevronRight size={18} />
          </button>
        </div>
      </div>
    </section>
  );
}
