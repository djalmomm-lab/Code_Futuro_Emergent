import React from 'react';
import { CheckCircle2, Smartphone, Star, Linkedin } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { ByteNavbar } from './ByteMascot';

export function AnywhereSection() {
  const { t } = useLanguage();
  return (
    <section className="relative py-20 md:py-28" style={{ background: '#070A14' }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-14 items-center">
          <div>
            <h2 className="font-display text-4xl md:text-5xl font-bold text-white leading-tight">{t('anywhere.title')}</h2>
            <p className="mt-5 text-slate-300 text-lg max-w-lg">{t('anywhere.subtitle')}</p>

            <div className="mt-7 flex flex-wrap gap-3">
              <a href="#" className="flex items-center gap-3 px-5 py-3 rounded-xl bg-[#141824] border hover:border-[#A3E635] transition" style={{ borderColor: 'var(--cf-border)' }}>
                <Smartphone size={26} className="text-white" />
                <div className="leading-tight">
                  <div className="text-[10px] text-slate-400 uppercase">{t('anywhere.appStore')}</div>
                  <div className="text-sm font-display font-bold text-white">App Store</div>
                </div>
              </a>
              <a href="#" className="flex items-center gap-3 px-5 py-3 rounded-xl bg-[#141824] border hover:border-[#A3E635] transition" style={{ borderColor: 'var(--cf-border)' }}>
                <Smartphone size={26} className="text-white" />
                <div className="leading-tight">
                  <div className="text-[10px] text-slate-400 uppercase">{t('anywhere.googlePlay')}</div>
                  <div className="text-sm font-display font-bold text-white">Google Play</div>
                </div>
              </a>
            </div>

            <div className="mt-6 flex items-center gap-3">
              <span className="text-3xl font-display font-bold text-[#A3E635]">4.9</span>
              <div>
                <div className="flex gap-0.5">
                  {['s1', 's2', 's3', 's4', 's5'].map((id) => <Star key={id} size={14} className="text-yellow-400 fill-yellow-400" />)}
                </div>
                <div className="text-xs text-slate-400 mt-0.5">{t('anywhere.rating')}</div>
              </div>
            </div>
          </div>

          {/* Phone mock */}
          <div className="flex justify-center">
            <div className="relative">
              <div className="w-64 h-[520px] rounded-[42px] p-3 border-[6px] border-[#1C2235] bg-[#0A0F1E] shadow-2xl relative overflow-hidden">
                <div className="absolute top-3 left-1/2 -translate-x-1/2 w-28 h-5 bg-black rounded-full" />
                <div className="h-full rounded-[30px] flex flex-col" style={{ background: '#0A0F1E' }}>
                  <div className="flex items-center justify-between px-4 pt-8 pb-3 text-xs">
                    <span className="flex items-center gap-1 text-orange-400 font-bold">🔥 7</span>
                    <span className="flex items-center gap-1 text-[#A3E635] font-bold">⭐ 250</span>
                    <span className="flex items-center gap-1 text-blue-400 font-bold">⚡ 5</span>
                  </div>
                  <div className="px-4 pt-2">
                    <div className="text-xs text-slate-400 font-bold uppercase">Python</div>
                    <div className="text-lg font-display font-bold text-white">Variáveis</div>
                  </div>
                  <div className="flex-1 flex flex-col items-center justify-center gap-3 px-4">
                    {[0, 1, 2, 3].map((i) => (
                      <div key={i} className={`${i % 2 === 0 ? '' : 'ml-16'} relative`}>
                        <div
                          className={`w-16 h-16 rounded-2xl flex items-center justify-center ${
                            i === 0 || i === 1 ? 'bg-[#A3E635]' : i === 2 ? 'bg-[#7C3AED]' : 'bg-[#1C2235]'
                          }`}
                          style={{ clipPath: 'polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%)' }}
                        >
                          {i <= 1 && <CheckCircle2 size={22} className="text-[#0A0F1E]" strokeWidth={3} />}
                          {i === 2 && <span className="text-white font-bold">▶</span>}
                        </div>
                      </div>
                    ))}
                  </div>
                  <div className="h-14 border-t flex items-center justify-around" style={{ borderColor: 'var(--cf-border)' }}>
                    <div className="text-[#A3E635] text-xs font-bold">📚</div>
                    <div className="text-slate-500 text-xs">🎯</div>
                    <div className="text-slate-500 text-xs">🏆</div>
                    <div className="text-slate-500 text-xs">👤</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export function CertificateSection() {
  const { t } = useLanguage();
  return (
    <section className="relative py-20 md:py-28">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-14 items-center">
          <div>
            <h2 className="font-display text-4xl md:text-5xl font-bold text-white leading-tight">{t('cert.title')}</h2>
            <p className="mt-5 text-slate-300 text-lg max-w-lg">{t('cert.subtitle')}</p>

            <button className="mt-6 inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-[#0A66C2] text-white font-bold text-sm hover:bg-[#0356a3] transition">
              <Linkedin size={16} /> {t('cert.addLinkedIn')}
            </button>
          </div>

          <div className="cf-card p-8 relative overflow-hidden">
            <div className="absolute inset-0 cf-shimmer opacity-50 pointer-events-none" />
            <div className="relative">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <ByteNavbar size={32} />
                  <span className="font-display font-bold text-white">CodeFuturo</span>
                </div>
                <span className="text-[10px] uppercase tracking-widest text-slate-400 font-bold">{t('cert.certOf')}</span>
              </div>

              <div className="mt-8 text-center">
                <p className="text-sm text-slate-400">{t('cert.certifies')}</p>
                <h3 className="mt-2 font-display text-3xl font-bold text-white">João Silva</h3>
                <p className="mt-2 text-sm text-slate-400">{t('cert.completed')}</p>
                <div className="mt-4 inline-flex items-center gap-2 px-4 py-2 rounded-full" style={{ background: 'rgba(124,58,237,0.15)', border: '1px solid rgba(124,58,237,0.4)' }}>
                  <span className="w-6 h-6 rounded-md bg-[#7C3AED] flex items-center justify-center text-xs font-bold text-white">Py</span>
                  <span className="font-display font-bold text-white">Python Fundamentos</span>
                </div>
              </div>

              <div className="mt-8 pt-6 border-t flex items-center justify-between" style={{ borderColor: 'var(--cf-border)' }}>
                <div>
                  <div className="text-[10px] uppercase text-slate-400 font-bold">{t('cert.date')}</div>
                  <div className="text-sm font-display font-bold text-white">Jan 2026</div>
                </div>
                <CheckCircle2 size={28} className="text-[#A3E635]" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export function CTASection() {
  const { t } = useLanguage();
  return (
    <section className="relative py-24 overflow-hidden">
      <div
        className="absolute inset-0 pointer-events-none"
        style={{ background: 'radial-gradient(ellipse at center, rgba(163,230,53,0.2) 0%, transparent 60%)' }}
      />
      <div className="relative max-w-5xl mx-auto text-center px-4">
        <h2 className="font-display text-4xl md:text-6xl font-bold text-white leading-tight">{t('cta.title')}</h2>
        <a
          href="/onboard"
          className="mt-10 inline-flex items-center gap-2 cf-btn-lime h-16 px-10 rounded-full text-lg"
        >
          {t('cta.button')} →
        </a>
      </div>
    </section>
  );
}
