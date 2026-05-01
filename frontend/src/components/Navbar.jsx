import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Menu, X, Globe, ChevronDown, User as UserIcon, LogOut, Settings, LayoutDashboard, Crown, Award, GraduationCap } from 'lucide-react';
import { useLanguage, LANGUAGES } from '../context/LanguageContext';
import { ByteLogo } from './ByteMascot';
import { Button } from './ui/button';
import { isAuthed, getStoredUser, logout as doLogout, authApi } from '../lib/api';

export default function Navbar() {
  const { t, lang, setLang } = useLanguage();
  const [open, setOpen] = useState(false);
  const [langOpen, setLangOpen] = useState(false);
  const [userOpen, setUserOpen] = useState(false);
  const [user, setUser] = useState(getStoredUser());
  const [isPro, setIsPro] = useState(false);
  const navigate = useNavigate();

  // Sync auth state on route changes + fetch fresh subscription status
  useEffect(() => {
    const sync = () => setUser(getStoredUser());
    window.addEventListener('storage', sync);
    if (isAuthed()) {
      authApi.me().then((me) => {
        if (me?.user) {
          setUser(me.user);
          setIsPro(!!me.user.is_pro);
        }
      }).catch(() => {});
    }
    return () => window.removeEventListener('storage', sync);
  }, []);

  const authed = isAuthed();
  const current = LANGUAGES.find((l) => l.code === lang);

  const handleLogout = () => {
    doLogout();
    setUser(null);
    setUserOpen(false);
    navigate('/');
  };

  const initials = (user?.name || 'CF').split(' ').map((s) => s[0]).slice(0, 2).join('').toUpperCase();

  return (
    <header className="sticky top-0 z-50 backdrop-blur-md" style={{ background: 'rgba(10,15,30,0.85)', borderBottom: '1px solid var(--cf-border)' }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-2" aria-label="CodeFuturo">
            <ByteLogo size={36} />
            <div className="hidden sm:block leading-none">
              <div className="font-display text-[19px] font-bold text-white">CodeFuturo</div>
              <div className="text-[10px] text-slate-400 tracking-wider uppercase">{t('footer.tagline')}</div>
            </div>
          </Link>

          <nav className="hidden md:flex items-center gap-8">
            <Link to="/catalogo" className="text-slate-300 hover:text-white transition-colors text-sm font-semibold">{t('nav.catalog')}</Link>
            {authed && <Link to="/dashboard" className="text-slate-300 hover:text-white transition-colors text-sm font-semibold">{t('nav.dashboard')}</Link>}
            <Link to="/jornada/python-zero" className="text-slate-300 hover:text-white transition-colors text-sm font-semibold">{t('nav.paths')}</Link>
            <Link to="/leaderboard" className="text-slate-300 hover:text-white transition-colors text-sm font-semibold">Leaderboard</Link>
            <Link to="/planos" className="text-slate-300 hover:text-white transition-colors text-sm font-semibold">{t('nav.pro')}</Link>
          </nav>

          <div className="flex items-center gap-2">
            <div className="relative">
              <button
                onClick={() => setLangOpen((v) => !v)}
                className="flex items-center gap-1.5 px-3 py-2 rounded-lg text-slate-300 hover:text-white hover:bg-[#1C2235] transition"
                aria-label="Change language"
              >
                <Globe size={16} />
                <span className="text-sm font-semibold hidden sm:inline">{current?.flag} {current?.code.toUpperCase()}</span>
                <span className="text-sm font-semibold sm:hidden">{current?.flag}</span>
                <ChevronDown size={14} />
              </button>
              {langOpen && (
                <div
                  className="absolute right-0 mt-2 w-44 py-1 rounded-xl border shadow-xl"
                  style={{ background: 'var(--cf-panel)', borderColor: 'var(--cf-border)' }}
                  onMouseLeave={() => setLangOpen(false)}
                >
                  {LANGUAGES.map((l) => (
                    <button
                      key={l.code}
                      onClick={() => { setLang(l.code); setLangOpen(false); }}
                      className={`w-full flex items-center gap-2 px-3 py-2 text-sm text-left hover:bg-[#1C2235] transition ${lang === l.code ? 'text-[#A3E635]' : 'text-slate-200'}`}
                    >
                      <span>{l.flag}</span>
                      <span className="font-semibold">{l.name}</span>
                    </button>
                  ))}
                </div>
              )}
            </div>

            {!authed ? (
              <>
                <Link to="/login" className="hidden md:inline text-slate-300 hover:text-white text-sm font-semibold px-3 py-2">{t('nav.login')}</Link>
                <Button onClick={() => navigate('/onboard')} className="cf-btn-lime hidden md:inline-flex h-10 px-5 rounded-full">
                  {t('nav.start')}
                </Button>
              </>
            ) : (
              <div className="relative hidden md:block">
                <button
                  onClick={() => setUserOpen((v) => !v)}
                  className="flex items-center gap-2 pl-1.5 pr-2 py-1.5 rounded-full border hover:border-[#A3E635] transition relative"
                  style={{ borderColor: isPro ? '#A3E635' : 'var(--cf-border)', background: 'var(--cf-panel)' }}
                >
                  <span className="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold text-[#0A0F1E] bg-[#A3E635] relative">
                    {initials}
                    {isPro && (
                      <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-[#0A0F1E] flex items-center justify-center" title="Pro">
                        <Crown size={9} className="text-[#A3E635]" fill="#A3E635" />
                      </span>
                    )}
                  </span>
                  <span className="text-sm font-bold text-white max-w-[120px] truncate">{user?.name}</span>
                  {isPro && <span className="text-[9px] font-bold tracking-wider px-1.5 py-0.5 rounded bg-[#A3E635] text-[#0A0F1E]">PRO</span>}
                  <ChevronDown size={14} className="text-slate-400" />
                </button>
                {userOpen && (
                  <div
                    className="absolute right-0 mt-2 w-52 py-1 rounded-xl border shadow-xl"
                    style={{ background: 'var(--cf-panel)', borderColor: 'var(--cf-border)' }}
                    onMouseLeave={() => setUserOpen(false)}
                  >
                    <Link to="/dashboard" onClick={() => setUserOpen(false)} className="flex items-center gap-2 px-3 py-2 text-sm text-slate-200 hover:bg-[#1C2235]">
                      <LayoutDashboard size={14} /> {t('nav.dashboard')}
                    </Link>
                    <Link to="/perfil" onClick={() => setUserOpen(false)} className="flex items-center gap-2 px-3 py-2 text-sm text-slate-200 hover:bg-[#1C2235]">
                      <UserIcon size={14} /> Perfil
                    </Link>
                    <Link to="/certificados" onClick={() => setUserOpen(false)} className="flex items-center gap-2 px-3 py-2 text-sm text-slate-200 hover:bg-[#1C2235]" data-testid="nav-certificates">
                      <Award size={14} /> Certificados
                    </Link>
                    <Link to="/escolas" onClick={() => setUserOpen(false)} className="flex items-center gap-2 px-3 py-2 text-sm text-slate-200 hover:bg-[#1C2235]" data-testid="nav-schools">
                      <GraduationCap size={14} /> Escolas
                    </Link>
                    {!isPro && (
                      <Link to="/planos" onClick={() => setUserOpen(false)} className="flex items-center gap-2 px-3 py-2 text-sm font-bold text-[#A3E635] hover:bg-[#1C2235]">
                        <Crown size={14} /> Fazer upgrade
                      </Link>
                    )}
                    {isPro && (
                      <Link to="/planos" onClick={() => setUserOpen(false)} className="flex items-center gap-2 px-3 py-2 text-sm text-slate-200 hover:bg-[#1C2235]">
                        <Crown size={14} className="text-[#A3E635]" /> Minha assinatura
                      </Link>
                    )}
                    <Link to="/configuracoes" onClick={() => setUserOpen(false)} className="flex items-center gap-2 px-3 py-2 text-sm text-slate-200 hover:bg-[#1C2235]">
                      <Settings size={14} /> Configurações
                    </Link>
                    <div className="my-1 h-px bg-[#1E293B]" />
                    <button onClick={handleLogout} className="w-full flex items-center gap-2 px-3 py-2 text-sm text-red-400 hover:bg-[#1C2235]">
                      <LogOut size={14} /> Sair
                    </button>
                  </div>
                )}
              </div>
            )}

            <button onClick={() => setOpen((v) => !v)} className="md:hidden p-2 text-slate-300" aria-label="Menu">
              {open ? <X size={22} /> : <Menu size={22} />}
            </button>
          </div>
        </div>
      </div>

      {open && (
        <div className="md:hidden border-t" style={{ borderColor: 'var(--cf-border)', background: 'var(--cf-panel)' }}>
          <div className="px-4 py-3 flex flex-col gap-1">
            <Link to="/catalogo" onClick={() => setOpen(false)} className="py-2 text-slate-200 font-semibold">{t('nav.catalog')}</Link>
            <Link to="/jornada/python-zero" onClick={() => setOpen(false)} className="py-2 text-slate-200 font-semibold">{t('nav.paths')}</Link>
            <Link to="/leaderboard" onClick={() => setOpen(false)} className="py-2 text-slate-200 font-semibold">Leaderboard</Link>
            {authed ? (
              <>
                <Link to="/dashboard" onClick={() => setOpen(false)} className="py-2 text-slate-200 font-semibold">{t('nav.dashboard')}</Link>
                <Link to="/perfil" onClick={() => setOpen(false)} className="py-2 text-slate-200 font-semibold">Perfil</Link>
                <Link to="/certificados" onClick={() => setOpen(false)} className="py-2 text-slate-200 font-semibold">Certificados</Link>
                <Link to="/escolas" onClick={() => setOpen(false)} className="py-2 text-slate-200 font-semibold">Escolas</Link>
                <button onClick={() => { setOpen(false); handleLogout(); }} className="py-2 text-left text-red-400 font-semibold">Sair</button>
              </>
            ) : (
              <>
                <Link to="/login" onClick={() => setOpen(false)} className="py-2 text-slate-200 font-semibold">{t('nav.login')}</Link>
                <Button onClick={() => { setOpen(false); navigate('/onboard'); }} className="cf-btn-lime mt-2 h-11 rounded-full">
                  {t('nav.start')}
                </Button>
              </>
            )}
          </div>
        </div>
      )}
    </header>
  );
}
