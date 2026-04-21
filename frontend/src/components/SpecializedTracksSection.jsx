import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, Sparkles } from 'lucide-react';
import { SPECIALIZED_TRACKS } from '../data/specializedTracks';

export default function SpecializedTracksSection() {
  const navigate = useNavigate();

  return (
    <section id="pro" className="relative py-20 md:py-28" style={{ background: '#070A14' }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-end justify-between flex-wrap gap-4 mb-10">
          <div className="max-w-2xl">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-bold tracking-wider uppercase mb-3" style={{ background: 'rgba(163, 230, 53, 0.12)', color: '#A3E635', border: '1px solid rgba(163, 230, 53, 0.25)' }}>
              <Sparkles size={12} />
              Trilhas Especializadas
            </div>
            <h2 className="font-display text-4xl md:text-5xl font-bold text-white leading-tight">
              Sem restrição de idade. <br />
              <span className="text-[#A3E635]">Domine o avançado.</span>
            </h2>
            <p className="mt-4 text-slate-300 text-lg">
              Para alunos a partir de 15 anos e adultos que querem carreira profissional, projetos reais ou aprofundar em áreas específicas.
            </p>
          </div>
          <button onClick={() => navigate('/catalogo')} className="text-sm font-bold text-[#A3E635] hover:underline flex items-center gap-1">
            Ver todas as trilhas <ArrowRight size={14} />
          </button>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {SPECIALIZED_TRACKS.slice(0, 8).map((track) => {
            const Icon = track.icon;
            return (
              <div
                key={track.id}
                onClick={() => navigate('/catalogo')}
                className="relative cf-card cf-card-hover p-5 overflow-hidden group cursor-pointer"
              >
                <div className="absolute -top-14 -right-14 w-32 h-32 rounded-full blur-3xl opacity-60 group-hover:opacity-90 transition" style={{ background: track.color }} />
                <div className="relative">
                  <div className="flex items-center justify-between">
                    <div className="w-11 h-11 rounded-xl flex items-center justify-center" style={{ background: `${track.color}22`, color: track.color }}>
                      <Icon size={20} />
                    </div>
                    <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-[#1C2235] text-slate-300">
                      {track.level}
                    </span>
                  </div>
                  <h3 className="mt-4 font-display text-lg font-bold text-white">{track.name}</h3>
                  <p className="mt-1.5 text-xs text-slate-400 leading-relaxed">{track.desc}</p>
                  <div className="mt-4 pt-3 border-t flex items-center justify-between text-xs text-slate-400" style={{ borderColor: 'var(--cf-border)' }}>
                    <span className="font-bold">{track.lessons} lições · ~{track.hours}h</span>
                    <ArrowRight size={14} style={{ color: track.color }} />
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
