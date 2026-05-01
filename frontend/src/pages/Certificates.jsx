import React, { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Award, Download, Lock, Loader2, Crown, ChevronRight, CheckCircle2 } from 'lucide-react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { certificatesApi, isAuthed } from '../lib/api';
import { logError } from '../lib/logger';
import { toast } from 'sonner';

export default function Certificates() {
  const navigate = useNavigate();
  const [items, setItems] = useState([]);
  const [isPro, setIsPro] = useState(false);
  const [loading, setLoading] = useState(true);
  const [downloadingSlug, setDownloadingSlug] = useState(null);

  useEffect(() => {
    if (!isAuthed()) {
      navigate('/login');
      return;
    }
    (async () => {
      try {
        const data = await certificatesApi.list();
        setItems(data.items || []);
        setIsPro(!!data.is_pro);
      } catch (err) {
        logError('Certificates.load', err);
        toast.error('Erro ao carregar certificados');
      } finally {
        setLoading(false);
      }
    })();
  }, [navigate]);

  const handleDownload = async (item) => {
    if (!isPro) { navigate('/planos'); return; }
    if (!item.is_complete) {
      toast.error(`Conclua todas as ${item.total} lições da trilha primeiro.`);
      return;
    }
    setDownloadingSlug(item.path_slug);
    try {
      const res = await certificatesApi.download(item.path_slug);
      const blob = new Blob([res.data], { type: 'application/pdf' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      // Try to extract filename from headers, fall back
      const cd = res.headers?.['content-disposition'] || '';
      const match = cd.match(/filename="?([^";]+)"?/);
      a.download = match ? match[1] : `codefuturo-${item.path_slug}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
      toast.success('Certificado baixado!');
    } catch (err) {
      logError('Certificates.download', err, { path: item.path_slug });
      const code = err.response?.status;
      if (code === 402) toast.error('Ative o Pro para baixar certificados');
      else if (code === 403) toast.error('Conclua a trilha completa para gerar o certificado');
      else toast.error('Erro ao gerar certificado');
    } finally {
      setDownloadingSlug(null);
    }
  };

  return (
    <div className="min-h-screen" style={{ background: 'var(--cf-space)' }}>
      <Navbar />
      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex items-center gap-3 mb-2">
          <Award size={28} className="text-[#A3E635]" />
          <h1 className="font-display text-3xl md:text-4xl font-bold text-white">Meus certificados</h1>
        </div>
        <p className="text-slate-400 text-sm md:text-base max-w-2xl">
          Conclua todas as lições de uma trilha para liberar o certificado em PDF — pronto para o LinkedIn ou portfólio.
        </p>

        {!isPro && (
          <button
            onClick={() => navigate('/planos')}
            data-testid="cert-upgrade-banner"
            className="mt-6 w-full text-left cf-card p-5 flex items-center gap-4 hover:scale-[1.005] transition group"
            style={{
              background: 'linear-gradient(90deg, rgba(163,230,53,0.08), rgba(124,58,237,0.08))',
              border: '1px solid rgba(163,230,53,0.25)',
            }}
          >
            <div className="w-12 h-12 rounded-xl flex items-center justify-center shrink-0"
                 style={{ background: 'rgba(163,230,53,0.15)', border: '1px solid rgba(163,230,53,0.3)' }}>
              <Crown size={22} className="text-[#A3E635]" />
            </div>
            <div className="flex-1 min-w-0">
              <div className="font-display font-bold text-white text-base">Certificados são exclusivos do Pro</div>
              <div className="text-sm text-slate-400 mt-0.5">
                Faça upgrade para emitir certificados oficiais do CodeFuturo.
              </div>
            </div>
            <span className="px-4 py-2 rounded-lg cf-btn-lime text-xs font-bold shrink-0">
              Ver planos
            </span>
          </button>
        )}

        {loading ? (
          <div className="mt-10 flex items-center gap-2 text-slate-400">
            <Loader2 size={16} className="animate-spin" /> Carregando...
          </div>
        ) : (
          <div className="mt-8 grid sm:grid-cols-2 gap-4">
            {items.map((item) => {
              const pct = item.total ? Math.round((item.completed / item.total) * 100) : 0;
              const ready = isPro && item.is_complete;
              const downloading = downloadingSlug === item.path_slug;
              return (
                <div key={item.path_slug} className="cf-card p-5 flex flex-col" data-testid={`cert-card-${item.path_slug}`}>
                  <div className="flex items-start gap-3">
                    <div className="w-12 h-12 rounded-xl flex items-center justify-center font-display font-bold text-white shrink-0"
                         style={{ background: item.color || '#A3E635' }}>
                      {item.path_name.substring(0, 2).toUpperCase()}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="font-display text-lg font-bold text-white truncate">{item.path_name}</div>
                      <div className="text-xs text-slate-400 mt-0.5">{item.completed}/{item.total} lições · {pct}%</div>
                    </div>
                    {item.is_complete && (
                      <CheckCircle2 size={20} className="text-[#A3E635] shrink-0" />
                    )}
                  </div>

                  <div className="mt-4 h-1.5 rounded-full bg-[#1C2235] overflow-hidden">
                    <div className="h-full rounded-full transition-all" style={{ width: `${pct}%`, background: item.color || '#A3E635' }} />
                  </div>

                  <div className="mt-5 flex items-center justify-between gap-2">
                    <Link to={`/jornada/${item.path_slug}`} className="text-xs font-bold text-slate-400 hover:text-white inline-flex items-center gap-1">
                      Continuar trilha <ChevronRight size={12} />
                    </Link>
                    <button
                      onClick={() => handleDownload(item)}
                      disabled={downloading}
                      data-testid={`cert-download-${item.path_slug}`}
                      className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-bold transition ${
                        ready
                          ? 'cf-btn-lime'
                          : 'bg-[#1C2235] text-slate-400 hover:text-white'
                      } disabled:opacity-50`}
                    >
                      {downloading ? <Loader2 size={14} className="animate-spin" /> : ready ? <Download size={14} /> : <Lock size={14} />}
                      {downloading ? 'Gerando...' : ready ? 'Baixar PDF' : !isPro ? 'Pro' : 'Bloqueado'}
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
}
