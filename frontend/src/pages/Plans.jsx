import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Check, Crown, Sparkles, Zap, Award, Infinity, Star, Loader2 } from 'lucide-react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { Button } from '../components/ui/button';
import { subscriptionApi, isAuthed } from '../lib/api';
import { logError } from '../lib/logger';
import { toast } from 'sonner';

const FEATURES = {
  free: [
    { ok: true, text: 'Primeiras 3 lições de cada trilha' },
    { ok: true, text: '5 energias por dia' },
    { ok: true, text: '1 trilha ativa por vez' },
    { ok: false, text: 'Certificados em PDF' },
    { ok: false, text: 'Múltiplas trilhas simultâneas' },
    { ok: false, text: 'Suporte prioritário' },
  ],
  pro: [
    { ok: true, text: 'Todas as lições desbloqueadas' },
    { ok: true, text: 'Energia ilimitada' },
    { ok: true, text: 'Múltiplas trilhas simultâneas' },
    { ok: true, text: 'Certificados em PDF para LinkedIn' },
    { ok: true, text: 'Streak Freeze (2/mês)' },
    { ok: true, text: 'Suporte prioritário' },
    { ok: true, text: 'Sem anúncios' },
  ],
  lifetime: [
    { ok: true, text: 'Tudo do Pro, para sempre' },
    { ok: true, text: 'Sem renovação anual' },
    { ok: true, text: 'Acesso vitalício a todo conteúdo novo' },
    { ok: true, text: 'Badge "Founding Member"' },
    { ok: true, text: 'Suporte prioritário VIP' },
    { ok: true, text: 'Trilhas ao vivo trimestrais' },
  ],
};

export default function Plans() {
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(false);
  const [meSubscription, setMeSubscription] = useState(null);

  useEffect(() => {
    if (params.get('canceled') === '1') {
      toast.info('Pagamento cancelado. Você pode tentar novamente quando quiser.');
    }
  }, [params]);

  useEffect(() => {
    (async () => {
      try {
        const r = await subscriptionApi.plans();
        setPlans(r.plans || []);
      } catch (err) {
        logError('Plans.loadPlans', err);
      }
      if (isAuthed()) {
        try {
          const s = await subscriptionApi.me();
          setMeSubscription(s);
        } catch (err) {
          logError('Plans.loadMe', err);
        }
      }
    })();
  }, []);

  const subscribe = async (planId) => {
    if (!isAuthed()) {
      toast.info('Crie uma conta para assinar');
      navigate('/register');
      return;
    }
    setLoading(planId);
    try {
      const res = await subscriptionApi.checkout(planId);
      window.location.href = res.url;
    } catch (err) {
      logError('Plans.checkout', err, { planId });
      toast.error(err.response?.data?.detail || 'Erro ao iniciar pagamento. Tente novamente.');
      setLoading(false);
    }
  };

  const findPlan = (id) => plans.find((p) => p.id === id);

  const proPlan = findPlan('pro_annual');
  const pioneerPlan = findPlan('pro_pioneer');
  const lifetimePlan = findPlan('lifetime');

  const monthlyEquivalent = (yearly) => (yearly / 12).toFixed(2).replace('.', ',');

  return (
    <div className="min-h-screen" style={{ background: 'var(--cf-space)' }}>
      <Navbar />
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-10">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-bold tracking-wider uppercase mb-4" style={{ background: 'rgba(163, 230, 53, 0.12)', color: '#A3E635', border: '1px solid rgba(163, 230, 53, 0.25)' }}>
            <Sparkles size={12} /> Planos & Preços
          </div>
          <h1 className="font-display text-4xl md:text-5xl font-bold text-white">
            Escolha o plano <span className="text-[#A3E635]">ideal pra você</span>
          </h1>
          <p className="mt-4 text-slate-300 text-lg max-w-2xl mx-auto">
            Comece grátis. Faça upgrade quando quiser desbloquear todas as trilhas, certificados e energia ilimitada.
          </p>
          {meSubscription?.is_pro && (
            <div className="mt-5 inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-bold" style={{ background: 'rgba(163, 230, 53, 0.15)', color: '#A3E635', border: '1px solid rgba(163, 230, 53, 0.4)' }}>
              <Crown size={14} /> Você já é {meSubscription.tier === 'lifetime' ? 'Lifetime' : 'Pro'}!
            </div>
          )}
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-5">
          {/* FREE */}
          <PlanCard
            color="#64748B"
            name="Grátis"
            tagline="Para experimentar"
            priceLine={<><span className="text-4xl font-display font-bold text-white">R$ 0</span><span className="text-slate-400 text-sm">/sempre</span></>}
            features={FEATURES.free}
            cta={<Button onClick={() => navigate('/register')} variant="outline" className="w-full h-11 rounded-full border-slate-600 text-slate-200 hover:bg-[#1C2235] bg-transparent">Começar grátis</Button>}
          />

          {/* PIONEERS (limited promo) */}
          {pioneerPlan && (
            <PlanCard
              color="#3B82F6"
              name="Pioneiros"
              badge="Edição limitada"
              tagline="Só os 500 primeiros"
              priceLine={
                <>
                  <span className="text-4xl font-display font-bold text-white">R$ {monthlyEquivalent(pioneerPlan.price_brl)}</span>
                  <span className="text-slate-400 text-sm">/mês</span>
                  <div className="text-xs text-slate-500 mt-1">cobrado R$ {pioneerPlan.price_brl.toFixed(2).replace('.', ',')}/ano</div>
                </>
              }
              features={FEATURES.pro}
              highlight={false}
              cta={
                <Button onClick={() => subscribe('pro_pioneer')} disabled={loading === 'pro_pioneer' || meSubscription?.is_pro} className="cf-btn-lime w-full h-11 rounded-full disabled:opacity-50">
                  {loading === 'pro_pioneer' ? <Loader2 size={16} className="animate-spin" /> : '7 dias grátis →'}
                </Button>
              }
            />
          )}

          {/* PRO ANNUAL (default) */}
          {proPlan && (
            <PlanCard
              color="#A3E635"
              name="Pro"
              badge="Mais popular"
              tagline="Recomendado"
              priceLine={
                <>
                  <span className="text-4xl font-display font-bold text-white">R$ {monthlyEquivalent(proPlan.price_brl)}</span>
                  <span className="text-slate-400 text-sm">/mês</span>
                  <div className="text-xs text-slate-500 mt-1">cobrado R$ {proPlan.price_brl.toFixed(2).replace('.', ',')}/ano</div>
                </>
              }
              features={FEATURES.pro}
              highlight={true}
              cta={
                <Button onClick={() => subscribe('pro_annual')} disabled={loading === 'pro_annual' || meSubscription?.is_pro} className="cf-btn-lime w-full h-11 rounded-full disabled:opacity-50">
                  {loading === 'pro_annual' ? <Loader2 size={16} className="animate-spin" /> : '7 dias grátis →'}
                </Button>
              }
            />
          )}

          {/* LIFETIME */}
          {lifetimePlan && (
            <PlanCard
              color="#7C3AED"
              name="Lifetime"
              tagline="Pague uma vez, use pra sempre"
              priceLine={
                <>
                  <span className="text-4xl font-display font-bold text-white">R$ {lifetimePlan.price_brl.toFixed(2).replace('.', ',')}</span>
                  <span className="text-slate-400 text-sm"> uma vez</span>
                  <div className="text-xs text-slate-500 mt-1">sem renovações</div>
                </>
              }
              features={FEATURES.lifetime}
              cta={
                <Button onClick={() => subscribe('lifetime')} disabled={loading === 'lifetime' || meSubscription?.tier === 'lifetime'} className="w-full h-11 rounded-full font-bold disabled:opacity-50" style={{ background: '#7C3AED', color: 'white' }}>
                  {loading === 'lifetime' ? <Loader2 size={16} className="animate-spin" /> : 'Quero o Lifetime →'}
                </Button>
              }
            />
          )}
        </div>

        <div className="mt-10 grid md:grid-cols-3 gap-4 text-center">
          <Reassure icon={<Award size={18} />} title="7 dias grátis" desc="Cancele dentro do trial sem cobrança" />
          <Reassure icon={<Star size={18} />} title="Reembolso integral" desc="Devolvemos 100% nos 7 dias após a cobrança (Art. 49 CDC)" />
          <Reassure icon={<Zap size={18} />} title="Pagamento 100% seguro" desc="Processado pelo Stripe — Pix, cartão e boleto" />
        </div>

        <div className="mt-10 text-center text-xs text-slate-500 max-w-2xl mx-auto">
          Ao assinar você concorda com os <a href="#" className="text-[#A3E635] hover:underline">Termos de Uso</a> e a <a href="#" className="text-[#A3E635] hover:underline">Política de Privacidade</a>. Os valores acima incluem todos os impostos. Você pode cancelar a qualquer momento pelo seu painel.
        </div>
      </main>
      <Footer />
    </div>
  );
}

function PlanCard({ color, name, tagline, badge, priceLine, features, cta, highlight }) {
  return (
    <div
      className={`relative cf-card p-6 flex flex-col overflow-hidden ${highlight ? 'cf-glow-lime' : ''}`}
      style={highlight ? { borderColor: color } : {}}
    >
      <div className="absolute -top-16 -right-16 w-40 h-40 rounded-full blur-3xl opacity-50 pointer-events-none" style={{ background: color }} />
      {badge && (
        <div className="absolute top-3 right-3 px-2.5 py-1 rounded-full text-[10px] font-bold tracking-wider uppercase" style={{ background: color, color: '#0A0F1E' }}>
          {badge}
        </div>
      )}
      <div className="relative">
        <h3 className="font-display text-2xl font-bold text-white">{name}</h3>
        <p className="text-xs text-slate-400 mt-0.5">{tagline}</p>
        <div className="mt-5 flex items-baseline gap-1 flex-wrap">
          {priceLine}
        </div>
        <ul className="mt-5 space-y-2.5">
          {features.map((f) => (
            <li key={f.text} className="flex items-start gap-2 text-sm">
              {f.ok ? <Check size={15} className="text-[#A3E635] mt-0.5 shrink-0" strokeWidth={3} /> : <span className="text-slate-600 mt-0.5 shrink-0 text-base leading-none">—</span>}
              <span className={f.ok ? 'text-slate-200' : 'text-slate-500 line-through'}>{f.text}</span>
            </li>
          ))}
        </ul>
        <div className="mt-6">{cta}</div>
      </div>
    </div>
  );
}

function Reassure({ icon, title, desc }) {
  return (
    <div className="flex flex-col items-center gap-2">
      <span className="w-10 h-10 rounded-full flex items-center justify-center bg-[#A3E635]/15 text-[#A3E635]">{icon}</span>
      <div className="font-bold text-white text-sm">{title}</div>
      <div className="text-xs text-slate-400">{desc}</div>
    </div>
  );
}
