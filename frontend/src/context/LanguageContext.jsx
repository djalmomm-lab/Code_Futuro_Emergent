import React, { createContext, useContext, useState, useEffect } from 'react';
import { translations } from '../data/translations';

const LanguageContext = createContext();

export const LANGUAGES = [
  { code: 'pt', name: 'Português', flag: '\u{1F1E7}\u{1F1F7}' },
  { code: 'en', name: 'English', flag: '\u{1F1FA}\u{1F1F8}' },
  { code: 'es', name: 'Español', flag: '\u{1F1EA}\u{1F1F8}' },
];

export const LanguageProvider = ({ children }) => {
  const [lang, setLang] = useState(() => {
    const saved = localStorage.getItem('cf_lang');
    return saved || 'pt';
  });

  useEffect(() => {
    localStorage.setItem('cf_lang', lang);
    document.documentElement.lang = lang;
  }, [lang]);

  const t = (key) => {
    const keys = key.split('.');
    let value = translations[lang];
    for (const k of keys) {
      value = value?.[k];
    }
    if (value === undefined) {
      let fallback = translations.pt;
      for (const k of keys) {
        fallback = fallback?.[k];
      }
      return fallback || key;
    }
    return value;
  };

  return (
    <LanguageContext.Provider value={{ lang, setLang, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const ctx = useContext(LanguageContext);
  if (!ctx) throw new Error('useLanguage must be used within LanguageProvider');
  return ctx;
};
