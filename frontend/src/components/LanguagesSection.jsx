import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, Sparkles, Code2 } from 'lucide-react';
import { pathsApi } from '../lib/api';
import { LANGUAGES_STACK } from '../data/mockData';

export default function LanguagesSection() {
  const navigate = useNavigate();
  const [paths, setPaths] = useState([]);

  useEffect(() => {
    (async () => {
      try {
        const res = await pathsApi.list();
        setPaths(res.paths || []);
      } catch {}
    })();
  }, []);

  // Fallback while backend is seeding
  const fallback = LANGUAGES_STACK.slice(0, 9).map((l) => ({
    slug: l.id,
    name: l.name,
    color: l.color,
    desc: 'Em breve: trilha completa',
    total_lessons: 0,
  }));
  const display = paths.length > 0 ? paths : fallback;

  return (
    <section id="languages" className="relative py-20 md:py-28">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-end justify-between flex-wrap gap-4 mb-10">
          <div className="max-w-2xl">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-bold tracking-wider uppercase mb-3" style={{ background: 'rgba(163, 230, 53, 0.12)', color: '#A3E635', border: '1px solid rgba(163, 230, 53, 0.25)' }}>
              <Code2 size={12} /> Trilhas completas
            </div>
            <h2 className="font-display text-4xl md:text-5xl font-bold text-white leading-tight">
              Escolha uma linguagem e <span className="text-[#A3E635]">comece a programar</span>
            </h2>
            <p className="mt-4 text-slate-300 text-lg">
              Trilhas gamificadas do zero ao avançado. Todas escritas por especialistas, com testes automáticos, dicas contextuais e projetos práticos.
            </p>
          </div>
          <button onClick={() => navigate('/catalogo')} className="text-sm font-bold text-[#A3E635] hover:underline flex items-center gap-1">
            Ver todas as trilhas <ArrowRight size={14} />
          </button>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {display.slice(0, 6).map((p) => (
            <div
              key={p.slug}
              onClick={() => navigate(`/jornada/${p.slug}`)}
              className="relative cf-card cf-card-hover p-6 overflow-hidden group cursor-pointer"
            >
              <div className="absolute -top-16 -right-16 w-40 h-40 rounded-full blur-3xl opacity-50 group-hover:opacity-80 transition" style={{ background: p.color }} />
              <div className="relative">
                <div className="flex items-center justify-between">
                  <div className="w-14 h-14 rounded-2xl flex items-center justify-center font-display font-bold text-white text-lg" style={{ background: p.color }}>
                    {p.name.substring(0, 2).toUpperCase()}
                  </div>
                  {p.total_lessons > 0 && (
                    <span className="text-[11px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full bg-[#1C2235] text-slate-300">
                      {p.total_lessons} lições
                    </span>
                  )}
                </div>
                <h3 className="mt-4 font-display text-xl font-bold text-white">{p.name}</h3>
                <p className="mt-2 text-sm text-slate-400 leading-relaxed line-clamp-2">{p.desc}</p>
                <div className="mt-4 pt-3 border-t flex items-center justify-between text-xs" style={{ borderColor: 'var(--cf-border)' }}>
                  <span className="text-slate-400 font-bold flex items-center gap-1.5">
                    <Sparkles size={12} style={{ color: p.color }} /> Do zero ao avançado
                  </span>
                  <ArrowRight size={14} style={{ color: p.color }} />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
