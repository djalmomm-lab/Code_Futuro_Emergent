import React, { useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Filter, Sparkles, ArrowRight } from 'lucide-react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { SPECIALIZED_TRACKS } from '../data/specializedTracks';
import { MODULES } from '../data/mockData';
import { useLanguage } from '../context/LanguageContext';
import { Input } from '../components/ui/input';

const LEVELS = ['Todos', 'Iniciante', 'Intermediário', 'Avançado'];
const TYPES = ['Todos', 'Por idade', 'Especializadas'];

export default function Catalog() {
  const navigate = useNavigate();
  const { t } = useLanguage();
  const [search, setSearch] = useState('');
  const [level, setLevel] = useState('Todos');
  const [type, setType] = useState('Todos');

  const ageTracks = MODULES.map((m, i) => ({
    id: m.id,
    name: ['Explorador Digital', 'Criador de Blocos', 'Programador Iniciante', 'Desenvolvedor'][i],
    desc: ['Primeiros passos em informática', 'Programação visual com Scratch', 'Python e Web do zero', 'Python avançado, algoritmos e C++'][i],
    color: m.color,
    lessons: m.lessons,
    level: ['Iniciante', 'Iniciante', 'Intermediário', 'Avançado'][i],
    isModule: true,
    badge: ['6-8 anos', '9-11 anos', '12-14 anos', '15-17 anos'][i],
  }));

  const specializedWithMeta = SPECIALIZED_TRACKS.map((s) => ({ ...s, isModule: false, badge: '15+ anos' }));

  const all = [...ageTracks, ...specializedWithMeta];

  const filtered = useMemo(() => {
    return all.filter((item) => {
      if (search && !item.name.toLowerCase().includes(search.toLowerCase())) return false;
      if (level !== 'Todos' && item.level !== level) return false;
      if (type === 'Por idade' && !item.isModule) return false;
      if (type === 'Especializadas' && item.isModule) return false;
      return true;
    });
  }, [all, search, level, type]);

  return (
    <div className="min-h-screen" style={{ background: 'var(--cf-space)' }}>
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="mb-8">
          <h1 className="font-display text-4xl md:text-5xl font-bold text-white">Catálogo de Trilhas</h1>
          <p className="mt-2 text-slate-400">Explore módulos por idade e trilhas especializadas para todos os níveis.</p>
        </div>

        {/* Filters */}
        <div className="cf-card p-4 mb-6">
          <div className="flex flex-col md:flex-row gap-3">
            <div className="flex-1 relative">
              <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
              <Input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Buscar trilha..."
                className="pl-10 h-11 bg-[#1C2235] border-[#1E293B] text-white"
              />
            </div>
            <div className="flex gap-2 flex-wrap">
              {TYPES.map((tp) => (
                <button
                  key={tp}
                  onClick={() => setType(tp)}
                  className={`px-4 py-2 rounded-full text-xs font-bold transition ${type === tp ? 'bg-[#A3E635] text-[#0A0F1E]' : 'bg-[#1C2235] text-slate-300 border hover:text-white'}`}
                  style={type === tp ? {} : { borderColor: 'var(--cf-border)' }}
                >
                  {tp}
                </button>
              ))}
            </div>
            <div className="flex gap-2 flex-wrap">
              {LEVELS.map((lv) => (
                <button
                  key={lv}
                  onClick={() => setLevel(lv)}
                  className={`px-4 py-2 rounded-full text-xs font-bold transition ${level === lv ? 'bg-white text-[#0A0F1E]' : 'bg-[#1C2235] text-slate-300 border hover:text-white'}`}
                  style={level === lv ? {} : { borderColor: 'var(--cf-border)' }}
                >
                  {lv}
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="text-sm text-slate-400 mb-4">{filtered.length} trilha{filtered.length !== 1 ? 's' : ''} encontrada{filtered.length !== 1 ? 's' : ''}</div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {filtered.map((track) => {
            const Icon = track.icon;
            return (
              <div
                key={track.id}
                onClick={() => navigate(track.isModule ? '/jornada/python-zero' : '/jornada/python-zero')}
                className="relative cf-card cf-card-hover p-6 overflow-hidden group cursor-pointer"
              >
                <div className="absolute -top-14 -right-14 w-32 h-32 rounded-full blur-3xl opacity-50 group-hover:opacity-80 transition" style={{ background: track.color }} />
                <div className="relative">
                  <div className="flex items-center justify-between">
                    <div className="w-12 h-12 rounded-2xl flex items-center justify-center text-white font-display font-bold" style={{ background: track.color }}>
                      {Icon ? <Icon size={20} /> : track.name.substring(0, 2).toUpperCase()}
                    </div>
                    <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-1 rounded-full" style={{ background: `${track.color}22`, color: track.color }}>
                      {track.badge}
                    </span>
                  </div>
                  <h3 className="mt-4 font-display text-xl font-bold text-white">{track.name}</h3>
                  <p className="mt-1.5 text-sm text-slate-400 leading-relaxed">{track.desc}</p>
                  <div className="mt-4 pt-3 border-t flex items-center justify-between text-xs" style={{ borderColor: 'var(--cf-border)' }}>
                    <span className="text-slate-400 font-bold">{track.lessons} lições · {track.level}</span>
                    <ArrowRight size={14} style={{ color: track.color }} />
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {filtered.length === 0 && (
          <div className="cf-card p-12 text-center">
            <Filter size={32} className="mx-auto text-slate-500 mb-3" />
            <div className="text-white font-bold">Nenhuma trilha encontrada</div>
            <div className="text-sm text-slate-400 mt-1">Tente ajustar os filtros ou limpar a busca.</div>
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
}
