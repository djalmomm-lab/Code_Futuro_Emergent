import React, { useEffect, useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { CheckCircle2, XCircle, Loader2, Crown, ArrowRight } from 'lucide-react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { Button } from '../components/ui/button';
import { subscriptionApi, authApi } from '../lib/api';
import { logError } from '../lib/logger';

const MAX_ATTEMPTS = 8;
const POLL_INTERVAL = 2000;

export default function PaymentSuccess() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const sessionId = params.get('session_id');
  const [state, setState] = useState({ status: 'polling', payment_status: null, attempts: 0 });

  useEffect(() => {
    if (!sessionId) {
      setState({ status: 'error', payment_status: null });
      return;
    }
    let cancelled = false;
    let attempt = 0;

    const poll = async () => {
      attempt += 1;
      try {
        const res = await subscriptionApi.status(sessionId);
        if (cancelled) return;
        if (res.payment_status === 'paid' || res.status === 'complete') {
          // Refresh user info to capture is_pro from /auth/me
          try { await authApi.me(); } catch (e) { logError('PaymentSuccess.refreshUser', e); }
          setState({ status: 'paid', payment_status: res.payment_status });
          return;
        }
        if (res.status === 'expired') {
          setState({ status: 'expired', payment_status: res.payment_status });
          return;
        }
        if (attempt >= MAX_ATTEMPTS) {
          setState({ status: 'timeout', payment_status: res.payment_status });
          return;
        }
        setState({ status: 'polling', payment_status: res.payment_status, attempts: attempt });
        setTimeout(poll, POLL_INTERVAL);
      } catch (err) {
        logError('PaymentSuccess.poll', err);
        if (!cancelled) setState({ status: 'error', payment_status: null });
      }
    };
    poll();
    return () => { cancelled = true; };
  }, [sessionId]);

  return (
    <div className="min-h-screen flex flex-col" style={{ background: 'var(--cf-space)' }}>
      <Navbar />
      <main className="flex-1 flex items-center justify-center px-4 py-12">
        <div className="cf-card p-8 md:p-12 max-w-lg w-full text-center relative overflow-hidden">
          <div className="absolute -top-20 left-1/2 -translate-x-1/2 w-72 h-72 rounded-full blur-3xl opacity-30 pointer-events-none" style={{ background: state.status === 'paid' ? '#A3E635' : '#3B82F6' }} />
          <div className="relative">
            {state.status === 'polling' && (
              <>
                <Loader2 size={56} className="text-[#A3E635] animate-spin mx-auto" />
                <h1 className="mt-5 font-display text-2xl font-bold text-white">Confirmando seu pagamento...</h1>
                <p className="mt-2 text-sm text-slate-400">
                  Estamos validando com o Stripe. Isso costuma levar alguns segundos. <br />
                  Tentativa {state.attempts || 1} de {MAX_ATTEMPTS}.
                </p>
              </>
            )}

            {state.status === 'paid' && (
              <>
                <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-[#A3E635]/15 mb-3">
                  <CheckCircle2 size={48} className="text-[#A3E635]" strokeWidth={2.5} />
                </div>
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold tracking-wider uppercase mb-3" style={{ background: 'rgba(163, 230, 53, 0.15)', color: '#A3E635', border: '1px solid rgba(163, 230, 53, 0.3)' }}>
                  <Crown size={12} /> Você é Pro!
                </div>
                <h1 className="font-display text-3xl font-bold text-white">Tudo certo! 🎉</h1>
                <p className="mt-3 text-slate-300">
                  Sua assinatura está ativa. Todas as trilhas, certificados e energia ilimitada estão liberadas. Bora codar!
                </p>
                <div className="mt-7 flex flex-col sm:flex-row gap-3 justify-center">
                  <Button onClick={() => navigate('/dashboard')} className="cf-btn-lime h-12 px-6 rounded-full inline-flex items-center gap-2">
                    Ir para o Dashboard <ArrowRight size={16} />
                  </Button>
                  <Button onClick={() => navigate('/catalogo')} variant="outline" className="h-12 px-6 rounded-full border-slate-600 text-slate-200 bg-transparent hover:bg-[#1C2235]">
                    Explorar trilhas
                  </Button>
                </div>
                <p className="mt-5 text-xs text-slate-500">
                  Você receberá um e-mail de confirmação em instantes. Direito de arrependimento de 7 dias garantido (Art. 49 CDC).
                </p>
              </>
            )}

            {(state.status === 'expired' || state.status === 'error' || state.status === 'timeout') && (
              <>
                <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-red-500/15 mb-3">
                  <XCircle size={48} className="text-red-400" strokeWidth={2.5} />
                </div>
                <h1 className="font-display text-2xl font-bold text-white">
                  {state.status === 'expired' ? 'Sessão expirada' : 'Não conseguimos confirmar'}
                </h1>
                <p className="mt-3 text-slate-300 text-sm">
                  {state.status === 'timeout'
                    ? 'O pagamento ainda pode estar sendo processado. Cheque seu e-mail ou volte ao painel em alguns minutos.'
                    : 'Algo deu errado. Se você foi cobrado, o acesso libera automaticamente em até 1 minuto. Caso contrário, tente novamente.'}
                </p>
                <div className="mt-6 flex flex-col sm:flex-row gap-3 justify-center">
                  <Button onClick={() => navigate('/planos')} className="cf-btn-lime h-12 px-6 rounded-full">Ver planos</Button>
                  <Link to="/perfil" className="h-12 px-6 rounded-full border-slate-600 text-slate-200 hover:bg-[#1C2235] flex items-center justify-center text-sm font-bold">Ir ao perfil</Link>
                </div>
              </>
            )}
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}
