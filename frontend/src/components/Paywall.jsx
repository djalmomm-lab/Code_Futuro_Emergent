import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Lock, Sparkles, Check, Crown, Zap, Award, Code2, ArrowRight } from 'lucide-react';
import { ByteNavbar } from './ByteMascot';

/**
 * Paywall overlay shown when a free user tries to access a Pro lesson.
 * Variants:
 *   - "modal":  full-page blurred lesson preview + centered card (used in Lesson.jsx)
 *   - "inline": compact card (used elsewhere if needed)
 */
export default function Paywall({ lesson, freeLimit = 3, variant = 'modal' }) {
  const navigate = useNavigate();
  const goPlans = () => navigate('/planos');

  const benefits = [
    { icon: Code2, label: 'Acesso a TODAS as lições e trilhas' },
    { icon: Zap, label: 'Energia ilimitada — pratique sem limites' },
    { icon: Award, label: 'Certificados em PDF ao concluir trilhas' },
    { icon: Sparkles, label: 'Conteúdo novo todo mês + suporte prioritário' },
  ];

  const card = (
    <div
      data-testid="paywall-card"
      className="cf-card relative w-full max-w-xl mx-auto p-8 md:p-10 overflow-hidden"
      style={{
        background: 'linear-gradient(180deg, rgba(28,34,53,0.95) 0%, rgba(10,15,30,0.98) 100%)',
        border: '1px solid rgba(163,230,53,0.25)',
        boxShadow: '0 30px 80px -20px rgba(163,230,53,0.25)',
      }}
    >
      {/* glow */}
      <div className="absolute -top-24 -right-24 w-72 h-72 rounded-full blur-3xl opacity-30" style={{ background: '#A3E635' }} />
      <div className="absolute -bottom-32 -left-24 w-72 h-72 rounded-full blur-3xl opacity-20" style={{ background: '#7C3AED' }} />

      <div className="relative">
        <div className="flex items-center gap-3 mb-2">
          <ByteNavbar size={48} />
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-[11px] font-bold tracking-wider uppercase"
               style={{ background: 'rgba(163,230,53,0.12)', color: '#A3E635', border: '1px solid rgba(163,230,53,0.3)' }}>
            <Crown size={12} /> CodeFuturo Pro
          </div>
        </div>

        <h2 className="mt-4 font-display text-3xl md:text-4xl font-bold text-white leading-tight">
          Esta lição está bloqueada
        </h2>
        <p className="mt-3 text-slate-300 text-sm md:text-base leading-relaxed">
          As <span className="font-bold text-[#A3E635]">{freeLimit} primeiras lições</span> de cada trilha são gratuitas.
          {lesson?.title && (
            <> Para continuar com <span className="text-white font-semibold">"{lesson.title}"</span> e desbloquear todo o conteúdo, ative o <span className="text-white font-semibold">Pro</span>.</>
          )}
        </p>

        <ul className="mt-6 space-y-2.5">
          {benefits.map((b, i) => {
            const Icon = b.icon;
            return (
              <li key={i} className="flex items-center gap-3 text-sm text-slate-200">
                <span className="w-7 h-7 rounded-lg flex items-center justify-center shrink-0"
                      style={{ background: 'rgba(163,230,53,0.12)', border: '1px solid rgba(163,230,53,0.25)' }}>
                  <Icon size={14} className="text-[#A3E635]" />
                </span>
                <span>{b.label}</span>
              </li>
            );
          })}
        </ul>

        <div className="mt-8 flex flex-col sm:flex-row gap-3">
          <button
            data-testid="paywall-cta-upgrade"
            onClick={goPlans}
            className="cf-btn-lime inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl font-bold text-sm flex-1"
          >
            Ver planos Pro <ArrowRight size={16} />
          </button>
          <button
            data-testid="paywall-cta-back"
            onClick={() => navigate(-1)}
            className="px-6 py-3 rounded-xl font-bold text-sm text-slate-300 hover:text-white hover:bg-[#1C2235] transition flex-1 sm:flex-none"
          >
            Voltar
          </button>
        </div>

        <p className="mt-4 text-[11px] text-slate-500">
          Cancele quando quiser · Pagamento seguro via Stripe
        </p>
      </div>
    </div>
  );

  if (variant === 'inline') return card;

  return (
    <div
      data-testid="paywall-overlay"
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      style={{ background: 'rgba(5, 8, 18, 0.85)', backdropFilter: 'blur(14px)' }}
    >
      {/* Decorative locked code preview behind */}
      <div aria-hidden className="absolute inset-0 overflow-hidden pointer-events-none opacity-40">
        <div className="absolute inset-0" style={{
          backgroundImage: 'repeating-linear-gradient(0deg, rgba(255,255,255,0.04) 0px, rgba(255,255,255,0.04) 1px, transparent 1px, transparent 24px)',
        }} />
        <Lock size={400} className="absolute -bottom-24 -right-24 text-[#A3E635]/5" />
      </div>
      {card}
    </div>
  );
}
