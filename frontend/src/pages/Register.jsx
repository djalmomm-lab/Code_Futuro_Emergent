import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ArrowLeft, Mail, Lock, User } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { ByteLogo } from '../components/ByteMascot';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { toast } from 'sonner';
import { authApi, saveAuth, getErrorMessage } from '../lib/api';

export default function Register() {
  const { t } = useLanguage();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    if (!name || !email || !password) { toast.error('Preencha todos os campos'); return; }
    if (password.length < 8) { toast.error('Senha deve ter no mínimo 8 caracteres'); return; }
    setLoading(true);
    try {
      const data = await authApi.register({ name, email, password });
      saveAuth(data);
      toast.success('Conta criada! Vamos começar.');
      setTimeout(() => navigate('/onboard'), 400);
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
          <h1 className="font-display text-2xl font-bold text-white text-center">{t('auth.register')}</h1>
          <p className="text-center text-sm text-slate-400 mt-1">Comece grátis, sem cartão</p>

          <form onSubmit={submit} className="mt-6 space-y-4">
            <div>
              <Label htmlFor="name" className="text-slate-300 text-sm font-semibold">{t('auth.name')}</Label>
              <div className="mt-1.5 relative">
                <User size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
                <Input id="name" value={name} onChange={(e) => setName(e.target.value)} className="pl-10 h-11 bg-[#1C2235] border-[#1E293B] text-white" placeholder="Seu nome" />
              </div>
            </div>
            <div>
              <Label htmlFor="email" className="text-slate-300 text-sm font-semibold">{t('auth.email')}</Label>
              <div className="mt-1.5 relative">
                <Mail size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
                <Input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} className="pl-10 h-11 bg-[#1C2235] border-[#1E293B] text-white" placeholder="voce@exemplo.com" />
              </div>
            </div>
            <div>
              <Label htmlFor="password" className="text-slate-300 text-sm font-semibold">{t('auth.password')}</Label>
              <div className="mt-1.5 relative">
                <Lock size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
                <Input id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="pl-10 h-11 bg-[#1C2235] border-[#1E293B] text-white" placeholder="Mínimo 8 caracteres" />
              </div>
            </div>

            <Button type="submit" disabled={loading} className="cf-btn-lime w-full h-12 rounded-full text-base disabled:opacity-60">
              {loading ? 'Criando...' : t('auth.register')}
            </Button>
          </form>

          <p className="mt-6 text-center text-sm text-slate-400">
            {t('auth.hasAccount')} <Link to="/login" className="text-[#A3E635] font-bold hover:underline">{t('auth.loginHere')}</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
