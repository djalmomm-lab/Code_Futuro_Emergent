import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Menu, X, Globe, ChevronDown } from 'lucide-react';
import { useLanguage, LANGUAGES } from '../context/LanguageContext';
import { ByteLogo } from './ByteMascot';
import { Button } from './ui/button';

export default function Navbar() {
  const { t, lang, setLang } = useLanguage();
  const [open, setOpen] = useState(false);
  const [langOpen, setLangOpen] = useState(false);
  const navigate = useNavigate();

  const current = LANGUAGES.find((l) => l.code === lang);

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
            <Link to="/dashboard" className="text-slate-300 hover:text-white transition-colors text-sm font-semibold">{t('nav.catalog')}</Link>
            <Link to="/jornada/python-zero" className="text-slate-300 hover:text-white transition-colors text-sm font-semibold">{t('nav.paths')}</Link>
            <Link to="/leaderboard" className="text-slate-300 hover:text-white transition-colors text-sm font-semibold">Leaderboard</Link>
            <a href="#pro" className="text-slate-300 hover:text-white transition-colors text-sm font-semibold">{t('nav.pro')}</a>
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

            <Link to="/login" className="hidden md:inline text-slate-300 hover:text-white text-sm font-semibold px-3 py-2">{t('nav.login')}</Link>
            <Button onClick={() => navigate('/onboard')} className="cf-btn-lime hidden md:inline-flex h-10 px-5 rounded-full">
              {t('nav.start')}
            </Button>

            <button onClick={() => setOpen((v) => !v)} className="md:hidden p-2 text-slate-300" aria-label="Menu">
              {open ? <X size={22} /> : <Menu size={22} />}
            </button>
          </div>
        </div>
      </div>

      {open && (
        <div className="md:hidden border-t" style={{ borderColor: 'var(--cf-border)', background: 'var(--cf-panel)' }}>
          <div className="px-4 py-3 flex flex-col gap-1">
            <Link to="/dashboard" onClick={() => setOpen(false)} className="py-2 text-slate-200 font-semibold">{t('nav.catalog')}</Link>
            <Link to="/jornada/python-zero" onClick={() => setOpen(false)} className="py-2 text-slate-200 font-semibold">{t('nav.paths')}</Link>
            <Link to="/leaderboard" onClick={() => setOpen(false)} className="py-2 text-slate-200 font-semibold">Leaderboard</Link>
            <Link to="/login" onClick={() => setOpen(false)} className="py-2 text-slate-200 font-semibold">{t('nav.login')}</Link>
            <Button onClick={() => { setOpen(false); navigate('/onboard'); }} className="cf-btn-lime mt-2 h-11 rounded-full">
              {t('nav.start')}
            </Button>
          </div>
        </div>
      )}
    </header>
  );
}
