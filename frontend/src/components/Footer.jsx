import React from 'react';
import { Link } from 'react-router-dom';
import { Github, Twitter, Instagram, Youtube } from 'lucide-react';
import { ByteLogo } from './ByteMascot';
import { useLanguage } from '../context/LanguageContext';

export default function Footer() {
  const { t } = useLanguage();

  const links = [
    { title: t('footer.product'), items: ['Python', 'HTML & CSS', 'JavaScript', 'Scratch'] },
    { title: t('footer.company'), items: ['Sobre', 'Escolas', 'Blog', 'Contato'] },
    { title: t('footer.resources'), items: ['FAQ', 'Comunidade', 'Roadmap', 'Status'] },
    { title: t('footer.legal'), items: ['Termos', 'Privacidade', 'Cookies', 'LGPD'] },
  ];

  return (
    <footer className="border-t" style={{ borderColor: 'var(--cf-border)', background: '#070A14' }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
        <div className="grid grid-cols-2 md:grid-cols-6 gap-8">
          <div className="col-span-2">
            <Link to="/" className="flex items-center gap-2">
              <ByteLogo size={40} />
              <div className="leading-none">
                <div className="font-display text-[20px] font-bold text-white">CodeFuturo</div>
                <div className="text-[11px] text-slate-400 tracking-wider uppercase">{t('footer.tagline')}</div>
              </div>
            </Link>
            <p className="mt-4 text-sm text-slate-400 max-w-xs">Plataforma gratuita de programação para todas as idades. Do primeiro clique ao deploy.</p>
            <div className="flex gap-3 mt-5">
              {[
                { Icon: Github, name: 'github' },
                { Icon: Twitter, name: 'twitter' },
                { Icon: Instagram, name: 'instagram' },
                { Icon: Youtube, name: 'youtube' },
              ].map(({ Icon, name }) => (
                <a key={name} href="#" aria-label={name} className="w-9 h-9 rounded-full flex items-center justify-center text-slate-400 hover:text-[#A3E635] border transition" style={{ borderColor: 'var(--cf-border)' }}>
                  <Icon size={16} />
                </a>
              ))}
            </div>
          </div>
          {links.map((group) => (
            <div key={group.title}>
              <div className="text-sm font-bold text-white mb-3">{group.title}</div>
              <ul className="space-y-2">
                {group.items.map((item) => (
                  <li key={item}><a href="#" className="text-sm text-slate-400 hover:text-[#A3E635] transition">{item}</a></li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div className="mt-10 pt-6 border-t text-center text-xs text-slate-500" style={{ borderColor: 'var(--cf-border)' }}>
          © {new Date().getFullYear()} CodeFuturo. {t('footer.rights')}
        </div>
      </div>
    </footer>
  );
}
