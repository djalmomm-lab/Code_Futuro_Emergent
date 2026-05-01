import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, Check, X, Crown, ArrowRight, Lock } from 'lucide-react';

/**
 * Celebration modal triggered when a free user completes the last free lesson
 * (3rd of every track). Designed as a high-converting upgrade nudge:
 * it celebrates the milestone first, then previews the next locked lessons.
 */
export default function UpgradeCelebration({ open, onClose, trackName, upcomingLessons = [], totalRemaining = 0 }) {
  const navigate = useNavigate();

  useEffect(() => {
    if (!open) return;
    const onKey = (e) => { if (e.key === 'Escape') onClose?.(); };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div
      data-testid="upgrade-celebration"
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      style={{ background: 'rgba(5, 8, 18, 0.85)', backdropFilter: 'blur(12px)' }}
      onClick={onClose}
    >
      {/* confetti dots — pure CSS */}
      <div aria-hidden className="absolute inset-0 overflow-hidden pointer-events-none">
        {Array.from({ length: 24 }).map((_, i) => (
          <span
            key={i}
            className="absolute rounded-full"
            style={{
              width: 6 + (i % 3) * 3,
              height: 6 + (i % 3) * 3,
              top: `${(i * 37) % 100}%`,
              left: `${(i * 53) % 100}%`,
              background: ['#A3E635', '#7C3AED', '#F59E0B', '#3776AB'][i % 4],
              opacity: 0.5,
              animation: `cf-floaty ${2 + (i % 4) * 0.4}s ease-in-out infinite alternate`,
            }}
          />
        ))}
      </div>

      <div
        className="cf-card relative w-full max-w-xl mx-auto p-7 md:p-9 overflow-hidden"
        style={{
          background: 'linear-gradient(180deg, rgba(28,34,53,0.98) 0%, rgba(10,15,30,0.98) 100%)',
          border: '1px solid rgba(163,230,53,0.3)',
          boxShadow: '0 30px 100px -20px rgba(163,230,53,0.35)',
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <button
          onClick={onClose}
          className="absolute top-3 right-3 text-slate-500 hover:text-white p-1.5 rounded-lg hover:bg-[#1C2235] transition"
          data-testid="upgrade-celebration-close"
          aria-label="Fechar"
        >
          <X size={18} />
        </button>

        <div className="absolute -top-24 -right-24 w-72 h-72 rounded-full blur-3xl opacity-30" style={{ background: '#A3E635' }} />

        <div className="relative">
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center justify-center w-10 h-10 rounded-2xl"
                  style={{ background: 'rgba(163,230,53,0.15)', border: '1px solid rgba(163,230,53,0.35)' }}>
              <Sparkles size={20} className="text-[#A3E635]" />
            </span>
            <span className="text-[11px] font-bold uppercase tracking-wider text-[#A3E635]">Marco desbloqueado</span>
          </div>

          <h2 className="mt-4 font-display text-2xl md:text-3xl font-bold text-white leading-tight">
            Mandou bem! 🎉
          </h2>
          <p className="mt-2 text-slate-300 text-sm md:text-base">
            Você concluiu as <span className="text-[#A3E635] font-semibold">3 lições gratuitas</span>
            {trackName ? <> da trilha <span className="text-white font-semibold">{trackName}</span></> : null}.
            {totalRemaining > 0 && (
              <> Faltam <span className="text-white font-semibold">{totalRemaining} lições</span> para você dominar tudo.</>
            )}
          </p>

          {upcomingLessons.length > 0 && (
            <div className="mt-5 rounded-xl p-4" style={{ background: 'rgba(124,58,237,0.08)', border: '1px solid rgba(124,58,237,0.25)' }}>
              <div className="text-[11px] font-bold uppercase tracking-wider text-violet-300 flex items-center gap-1.5">
                <Lock size={12} /> O que vem com o Pro
              </div>
              <ul className="mt-2.5 space-y-1.5">
                {upcomingLessons.slice(0, 4).map((l) => (
                  <li key={l.slug} className="flex items-center gap-2 text-sm text-slate-200">
                    <span className="w-5 h-5 rounded-md flex items-center justify-center text-[10px] font-bold shrink-0"
                          style={{ background: 'rgba(163,230,53,0.18)', color: '#A3E635' }}>
                      {l.order}
                    </span>
                    <span className="truncate">{l.title}</span>
                  </li>
                ))}
                {upcomingLessons.length > 4 && (
                  <li className="text-xs text-slate-400 pl-7">+ {upcomingLessons.length - 4} lições adicionais…</li>
                )}
              </ul>
            </div>
          )}

          <ul className="mt-5 space-y-2 text-sm text-slate-200">
            <li className="flex items-center gap-2">
              <Check size={14} className="text-[#A3E635] shrink-0" /> Acesso a TODAS as lições e trilhas
            </li>
            <li className="flex items-center gap-2">
              <Check size={14} className="text-[#A3E635] shrink-0" /> Energia ilimitada — sem esperar
            </li>
            <li className="flex items-center gap-2">
              <Check size={14} className="text-[#A3E635] shrink-0" /> Certificado em PDF ao concluir trilha
            </li>
          </ul>

          <div className="mt-7 flex flex-col sm:flex-row gap-3">
            <button
              data-testid="upgrade-celebration-cta"
              onClick={() => navigate('/planos')}
              className="cf-btn-lime inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl font-bold text-sm flex-1"
            >
              <Crown size={16} /> Liberar tudo com Pro <ArrowRight size={16} />
            </button>
            <button
              onClick={onClose}
              data-testid="upgrade-celebration-later"
              className="px-6 py-3 rounded-xl font-bold text-sm text-slate-300 hover:text-white hover:bg-[#1C2235] transition"
            >
              Mais tarde
            </button>
          </div>

          <p className="mt-3 text-[11px] text-slate-500">
            Pagamento seguro via Stripe · Cancele quando quiser
          </p>
        </div>
      </div>

      <style>{`
        @keyframes cf-floaty {
          0% { transform: translateY(0) }
          100% { transform: translateY(-14px) }
        }
      `}</style>
    </div>
  );
}
