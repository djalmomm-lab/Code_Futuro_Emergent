import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ArrowLeft, Mail, Lock, Eye, EyeOff } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { ByteLogo } from '../components/ByteMascot';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { toast } from 'sonner';
import { authApi, saveAuth, getErrorMessage } from '../lib/api';

export default function Login() {
  const { t } = useLanguage();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [show, setShow] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    if (!email || !password) { toast.error('Preencha todos os campos'); return; }
    setLoading(true);
    try {
      const data = await authApi.login({ email, password });
      saveAuth(data);
      toast.success('Bem-vindo de volta!');
      setTimeout(() => navigate('/dashboard'), 400);
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12 relative overflow-hidden">
      <div className="absolute inset-0 cf-grid-bg opacity-50 pointer-events-none" />
      <div className="absolute -top-40 left-1/2 -translate-x-1/2 w-[600px] h-[600px] rounded-full pointer-events-none" style={{ background: 'radial-gradient(circle, rgba(163,230,53,0.15) 0%, transparent 60%)' }} />

      <Link to="/" className="absolute top-6 left-6 text-slate-400 hover:text-white flex items-center gap-2 text-sm font-semibold">
        <ArrowLeft size={16} /> Voltar
      </Link>

      <div className="relative w-full max-w-md">
        <Link to="/" className="flex items-center justify-center gap-2 mb-8">
          <ByteLogo size={48} />
          <div className="leading-none">
            <div className="font-display text-2xl font-bold text-white">CodeFuturo</div>
            <div className="text-[11px] text-slate-400 tracking-wider uppercase">Do zero ao deploy</div>
          </div>
        </Link>

        <div className="cf-card p-8">
          <h1 className="font-display text-2xl font-bold text-white text-center">{t('auth.login')}</h1>
          <p className="text-center text-sm text-slate-400 mt-1">Continue sua jornada de código</p>

          <form onSubmit={submit} className="mt-6 space-y-4">
            <div>
              <Label htmlFor="email" className="text-slate-300 text-sm font-semibold">{t('auth.email')}</Label>
              <div className="mt-1.5 relative">
                <Mail size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
                <Input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} className="pl-10 h-11 bg-[#1C2235] border-[#1E293B] text-white" placeholder="voce@exemplo.com" />
              </div>
            </div>
            <div>
              <div className="flex items-center justify-between">
                <Label htmlFor="password" className="text-slate-300 text-sm font-semibold">{t('auth.password')}</Label>
                <a href="#" className="text-xs text-[#A3E635] font-semibold hover:underline">{t('auth.forgot')}</a>
              </div>
              <div className="mt-1.5 relative">
                <Lock size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
                <Input id="password" type={show ? 'text' : 'password'} value={password} onChange={(e) => setPassword(e.target.value)} className="pl-10 pr-10 h-11 bg-[#1C2235] border-[#1E293B] text-white" placeholder="••••••••" />
                <button type="button" onClick={() => setShow((v) => !v)} className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-white">
                  {show ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>

            <Button type="submit" disabled={loading} className="cf-btn-lime w-full h-12 rounded-full text-base disabled:opacity-60">
              {loading ? 'Entrando...' : t('auth.login')}
            </Button>
          </form>

          <div className="my-6 flex items-center gap-3">
            <div className="flex-1 h-px bg-[#1E293B]" />
            <span className="text-xs text-slate-500 uppercase font-bold">{t('auth.or')}</span>
            <div className="flex-1 h-px bg-[#1E293B]" />
          </div>

          <button className="w-full h-12 rounded-xl bg-[#1C2235] border hover:bg-[#242b44] text-white font-semibold text-sm flex items-center justify-center gap-2" style={{ borderColor: 'var(--cf-border)' }}>
            <svg width="18" height="18" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
            {t('auth.continueWith')} Google
          </button>

          <p className="mt-6 text-center text-sm text-slate-400">
            {t('auth.noAccount')} <Link to="/register" className="text-[#A3E635] font-bold hover:underline">{t('auth.createOne')}</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
