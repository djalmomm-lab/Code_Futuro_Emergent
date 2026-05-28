import React, { useState, useMemo, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Filter, ArrowRight, Sparkles } from 'lucide-react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { Input } from '../components/ui/input';
import { pathsApi } from '../lib/api';
import { logError } from '../lib/logger';

export default function Catalog() {
  const navigate = useNavigate();
  const [search, setSearch] = useState('');
  const [paths, setPaths] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const res = await pathsApi.list();
        setPaths(res.paths || []);
      } catch (err) {
        logError('Catalog.loadPaths', err);
      }
      setLoading(false);
    })();
  }, []);

  const filtered = useMemo(() => {
    return paths.filter((p) => !search || p.name.toLowerCase().includes(search.toLowerCase()) || p.desc?.toLowerCase().includes(search.toLowerCase()));
  }, [paths, search]);

  return (
    <div className="min-h-screen" style={{ background: 'var(--cf-space)' }}>
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="mb-8">
          <h1 className="font-display text-4xl md:text-5xl font-bold text-white">Catálogo de Linguagens</h1>
          <p className="mt-2 text-slate-400 max-w-2xl">
            Escolha a linguagem que quer dominar. Cada trilha é completa: do básico ao projeto real, com testes automáticos, dicas e execução ao vivo.
          </p>
        </div>

        <div className="cf-card p-4 mb-6">
          <div className="relative">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
            <Input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Buscar linguagem (Python, JavaScript, SQL...)"
              className="pl-10 h-11 bg-[#1C2235] border-[#1E293B] text-white"
            />
          </div>
        </div>

        <div className="text-sm text-slate-400 mb-4">
          {loading ? ' ' : `${filtered.length} trilha${filtered.length !== 1 ? 's' : ''} disponíve${filtered.length !== 1 ? 'is' : 'l'}`}
        </div>

        {/* Skeleton cards while loading */}
        {loading && (
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5 animate-pulse">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="cf-card p-6 space-y-4">
                <div className="flex items-center justify-between">
                  <div className="w-14 h-14 rounded-2xl bg-[#1C2235]" />
                  <div className="w-16 h-6 rounded-full bg-[#1C2235]" />
                </div>
                <div className="h-5 w-3/4 rounded bg-[#1C2235]" />
                <div className="space-y-2">
                  <div className="h-3 rounded bg-[#1C2235]" />
                  <div className="h-3 w-5/6 rounded bg-[#1C2235]" />
                </div>
                <div className="pt-3 border-t flex items-center justify-between" style={{ borderColor: 'var(--cf-border)' }}>
                  <div className="h-3 w-24 rounded bg-[#1C2235]" />
                  <div className="h-3 w-4 rounded bg-[#1C2235]" />
                </div>
              </div>
            ))}
          </div>
        )}

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {!loading && filtered.map((p) => (
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
                  <span className="text-[11px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full bg-[#1C2235] text-slate-300">
                    {p.total_lessons || 0} lições
                  </span>
                </div>
                <h3 className="mt-4 font-display text-xl font-bold text-white">{p.name}</h3>
                <p className="mt-2 text-sm text-slate-400 leading-relaxed">{p.desc}</p>
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

        {!loading && filtered.length === 0 && (
          <div className="cf-card p-12 text-center">
            <Filter size={32} className="mx-auto text-slate-500 mb-3" />
            <div className="text-white font-bold">Nenhuma trilha encontrada</div>
            <div className="text-sm text-slate-400 mt-1">Tente outro termo.</div>
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
}
