import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Award, CheckCircle2, XCircle, Loader2, Search, ArrowLeft, Linkedin, Share2 } from 'lucide-react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { api } from '../lib/api';
import { logError } from '../lib/logger';
import { toast } from 'sonner';

const buildLinkedInAddToProfileUrl = (cert) => {
  if (!cert?.cert_id) return '#';
  const issued = cert.issued_at ? new Date(cert.issued_at) : new Date();
  const params = new URLSearchParams({
    startTask: 'CERTIFICATION_NAME',
    name: `Trilha ${cert.track_name} — CodeFuturo`,
    organizationName: 'CodeFuturo',
    issueYear: String(issued.getFullYear()),
    issueMonth: String(issued.getMonth() + 1),
    certUrl: `${window.location.origin}/verificar/${cert.cert_id}`,
    certId: cert.cert_id,
  });
  return `https://www.linkedin.com/profile/add?${params.toString()}`;
};

const buildLinkedInSharePostUrl = (cert) => {
  if (!cert?.cert_id) return '#';
  const url = `${window.location.origin}/verificar/${cert.cert_id}`;
  return `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`;
};

export default function VerifyCertificate() {
  const { certId: paramId } = useParams();
  const navigate = useNavigate();
  const [input, setInput] = useState(paramId || '');
  const [loading, setLoading] = useState(!!paramId);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!paramId) return;
    (async () => {
      setLoading(true);
      setError('');
      try {
        const { data } = await api.get(`/verify/${paramId}`);
        setResult(data);
      } catch (err) {
        logError('Verify.load', err, { paramId });
        const code = err.response?.status;
        setError(code === 404 ? 'Certificado não encontrado ou inválido.' : 'Erro ao verificar certificado.');
        setResult(null);
      } finally {
        setLoading(false);
      }
    })();
  }, [paramId]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const id = input.trim();
    if (!id) return;
    navigate(`/verificar/${encodeURIComponent(id)}`);
  };

  return (
    <div className="min-h-screen" style={{ background: 'var(--cf-space)' }}>
      <Navbar />
      <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <button onClick={() => navigate(-1)} className="text-slate-400 hover:text-white flex items-center gap-2 text-sm font-semibold mb-6">
          <ArrowLeft size={16} /> Voltar
        </button>

        <div className="flex items-center gap-3 mb-2">
          <Award size={28} className="text-[#A3E635]" />
          <h1 className="font-display text-3xl md:text-4xl font-bold text-white">Verificar certificado</h1>
        </div>
        <p className="text-slate-400 text-sm md:text-base max-w-2xl">
          Cole o ID do certificado (ex.: <span className="font-code text-slate-300">CF-XXXXXXXXXXXX</span>) para confirmar a autenticidade.
        </p>

        <form onSubmit={handleSubmit} className="mt-6 flex gap-2" data-testid="verify-form">
          <div className="flex-1 cf-card flex items-center gap-2 px-4">
            <Search size={16} className="text-slate-400 shrink-0" />
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="CF-XXXXXXXXXXXX"
              className="flex-1 py-3 bg-transparent outline-none text-sm text-slate-100 font-code"
              data-testid="verify-input"
            />
          </div>
          <button type="submit" className="cf-btn-lime px-5 py-3 rounded-xl font-bold text-sm" data-testid="verify-submit">
            Verificar
          </button>
        </form>

        {loading && (
          <div className="mt-8 flex items-center gap-2 text-slate-400" data-testid="verify-loading">
            <Loader2 size={16} className="animate-spin" /> Verificando...
          </div>
        )}

        {!loading && error && (
          <div className="mt-8 cf-card p-6 flex items-start gap-4" data-testid="verify-invalid"
               style={{ border: '1px solid rgba(244,63,94,0.35)' }}>
            <XCircle size={28} className="text-rose-400 shrink-0 mt-0.5" />
            <div>
              <div className="font-display text-xl font-bold text-white">Não autenticado</div>
              <div className="text-slate-400 text-sm mt-1">{error}</div>
            </div>
          </div>
        )}

        {!loading && result?.valid && (
          <div className="mt-8 cf-card p-6 md:p-8 relative overflow-hidden" data-testid="verify-valid"
               style={{ border: '1px solid rgba(163,230,53,0.4)' }}>
            <div className="absolute -top-20 -right-20 w-60 h-60 rounded-full blur-3xl opacity-30" style={{ background: '#A3E635' }} />
            <div className="relative">
              <div className="flex items-center gap-3">
                <CheckCircle2 size={32} className="text-[#A3E635]" />
                <div>
                  <div className="text-[11px] font-bold uppercase tracking-wider text-[#A3E635]">Certificado autêntico</div>
                  <div className="font-display text-2xl font-bold text-white mt-0.5">{result.student_name}</div>
                </div>
              </div>

              <div className="mt-6 grid sm:grid-cols-2 gap-4">
                <Stat label="Trilha concluída" value={result.track_name} />
                <Stat label="Lições" value={String(result.total_lessons)} />
                <Stat label="XP conquistado" value={String(result.xp_earned)} />
                <Stat label="Data de emissão" value={formatDate(result.issued_at)} />
              </div>

              <div className="mt-6 pt-5 border-t" style={{ borderColor: 'var(--cf-border)' }}>
                <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400">ID do certificado</div>
                <div className="mt-1 font-code text-sm text-slate-200">{result.cert_id}</div>
              </div>

              <div className="mt-6 pt-5 border-t flex flex-wrap gap-3" style={{ borderColor: 'var(--cf-border)' }}>
                <a
                  href={buildLinkedInAddToProfileUrl(result)}
                  target="_blank"
                  rel="noopener noreferrer"
                  data-testid="verify-linkedin-add"
                  className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-bold text-white transition"
                  style={{ background: '#0A66C2' }}
                >
                  <Linkedin size={16} /> Adicionar ao LinkedIn
                </a>
                <a
                  href={buildLinkedInSharePostUrl(result)}
                  target="_blank"
                  rel="noopener noreferrer"
                  data-testid="verify-linkedin-share"
                  className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-bold text-slate-200 hover:bg-[#1C2235] transition border"
                  style={{ borderColor: 'var(--cf-border)' }}
                >
                  <Share2 size={16} /> Compartilhar post
                </a>
                <button
                  onClick={async () => {
                    try {
                      await navigator.clipboard.writeText(`${window.location.origin}/verificar/${result.cert_id}`);
                      toast.success('Link copiado!');
                    } catch { toast.error('Não foi possível copiar.'); }
                  }}
                  data-testid="verify-copy-link"
                  className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-bold text-slate-200 hover:bg-[#1C2235] transition border"
                  style={{ borderColor: 'var(--cf-border)' }}
                >
                  Copiar link
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
}

const Stat = ({ label, value }) => (
  <div className="rounded-xl p-4" style={{ background: 'var(--cf-panel-light)' }}>
    <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400">{label}</div>
    <div className="mt-1 font-display text-base font-bold text-white">{value}</div>
  </div>
);

const formatDate = (iso) => {
  if (!iso) return '—';
  try {
    const d = new Date(iso);
    return d.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' });
  } catch { return iso; }
};
