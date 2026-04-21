import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { User, Shield, Download, Trash2, Flame, Zap, Star, Trophy, AlertTriangle, Mail } from 'lucide-react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { Button } from '../components/ui/button';
import { authApi, privacyApi, isAuthed, logout } from '../lib/api';
import { toast } from 'sonner';

export default function Profile() {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    if (!isAuthed()) { navigate('/login'); return; }
    (async () => {
      try {
        const me = await authApi.me();
        setData(me);
      } catch {
        toast.error('Erro ao carregar perfil');
      } finally {
        setLoading(false);
      }
    })();
  }, [navigate]);

  const handleExport = async () => {
    try {
      const exportData = await privacyApi.export();
      const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `codefuturo-meus-dados-${new Date().toISOString().split('T')[0]}.json`;
      a.click();
      URL.revokeObjectURL(url);
      toast.success('Dados exportados! Baixe o arquivo JSON.');
    } catch {
      toast.error('Erro ao exportar dados');
    }
  };

  const handleDelete = async () => {
    setDeleting(true);
    try {
      await privacyApi.delete();
      logout();
      toast.success('Conta excluída. Até mais!');
      setTimeout(() => navigate('/'), 800);
    } catch {
      toast.error('Erro ao excluir conta');
      setDeleting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ background: 'var(--cf-space)' }}>
        <div className="text-slate-400">Carregando...</div>
      </div>
    );
  }

  const user = data?.user;
  const profile = data?.profile;
  const progress = data?.progress;

  return (
    <div className="min-h-screen" style={{ background: 'var(--cf-space)' }}>
      <Navbar />
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="flex items-center gap-4 mb-8">
          <div className="w-16 h-16 rounded-2xl flex items-center justify-center text-xl font-bold text-[#0A0F1E] bg-[#A3E635]">
            {(user?.name || 'CF').split(' ').map((s) => s[0]).slice(0, 2).join('').toUpperCase()}
          </div>
          <div>
            <h1 className="font-display text-3xl font-bold text-white">{user?.name}</h1>
            <div className="text-sm text-slate-400 flex items-center gap-1.5 mt-0.5">
              <Mail size={13} /> {user?.email}
            </div>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <Stat icon={<Flame size={18} />} value={progress?.streak || 0} label="Sequência" color="#F97316" />
          <Stat icon={<Star size={18} />} value={progress?.xp_total || 0} label="XP Total" color="#A3E635" />
          <Stat icon={<Zap size={18} />} value={`${progress?.energy || 0}/${progress?.max_energy || 5}`} label="Energia" color="#3B82F6" />
          <Stat icon={<Trophy size={18} />} value={progress?.level || 1} label="Nível" color="#7C3AED" />
        </div>

        {/* Profile info */}
        {profile && (
          <div className="cf-card p-6 mb-6">
            <div className="flex items-center gap-2 mb-4">
              <User size={18} className="text-[#A3E635]" />
              <h2 className="font-display text-lg font-bold text-white">Informações do Perfil</h2>
            </div>
            <div className="grid sm:grid-cols-2 gap-4 text-sm">
              <InfoRow label="Data de nascimento" value={profile.birth_date} />
              <InfoRow label="Idade" value={`${profile.age} anos`} />
              <InfoRow label="Interesse principal" value={profile.interest} />
              <InfoRow label="Score diagnóstico" value={profile.diagnostic_score} />
              {profile.parent_name && <InfoRow label="Responsável" value={profile.parent_name} />}
              {profile.parent_email && <InfoRow label="E-mail do responsável" value={profile.parent_email} />}
              {profile.consent_at && <InfoRow label="Consentimento em" value={new Date(profile.consent_at).toLocaleString('pt-BR')} />}
              <InfoRow label="Onboarded em" value={profile.onboarded_at ? new Date(profile.onboarded_at).toLocaleDateString('pt-BR') : '—'} />
            </div>
          </div>
        )}

        {/* LGPD privacy controls */}
        <div className="cf-card p-6 mb-6">
          <div className="flex items-center gap-2 mb-4">
            <Shield size={18} className="text-[#A3E635]" />
            <h2 className="font-display text-lg font-bold text-white">Privacidade & LGPD</h2>
          </div>
          <p className="text-sm text-slate-400 leading-relaxed mb-5">
            Conforme a Lei Geral de Proteção de Dados (LGPD), você tem direito de acessar, corrigir e excluir seus dados a qualquer momento. Para menores de 13 anos, esses direitos são exercidos pelo responsável legal.
          </p>

          <div className="grid sm:grid-cols-2 gap-3">
            <button
              onClick={handleExport}
              className="flex items-start gap-3 p-4 rounded-xl border hover:border-[#A3E635] text-left transition"
              style={{ borderColor: 'var(--cf-border)', background: 'var(--cf-panel-light)' }}
            >
              <div className="w-10 h-10 rounded-xl flex items-center justify-center bg-[#A3E635]/15 text-[#A3E635] shrink-0">
                <Download size={18} />
              </div>
              <div>
                <div className="font-bold text-white text-sm">Exportar meus dados</div>
                <div className="text-xs text-slate-400 mt-0.5">Baixe em JSON todos os dados que temos sobre você — portabilidade LGPD.</div>
              </div>
            </button>

            <button
              onClick={() => setConfirmDelete(true)}
              className="flex items-start gap-3 p-4 rounded-xl border hover:border-red-400 text-left transition"
              style={{ borderColor: 'var(--cf-border)', background: 'var(--cf-panel-light)' }}
            >
              <div className="w-10 h-10 rounded-xl flex items-center justify-center bg-red-500/15 text-red-400 shrink-0">
                <Trash2 size={18} />
              </div>
              <div>
                <div className="font-bold text-white text-sm">Excluir minha conta</div>
                <div className="text-xs text-slate-400 mt-0.5">Remove permanentemente todos seus dados (direito ao esquecimento).</div>
              </div>
            </button>
          </div>

          <div className="mt-4 p-3 rounded-lg text-[11px] text-slate-400 leading-relaxed" style={{ background: 'rgba(59,130,246,0.08)', border: '1px solid rgba(59,130,246,0.2)' }}>
            Em caso de dúvidas sobre tratamento de dados, envie e-mail para <span className="text-[#A3E635] font-bold">privacidade@codefuturo.com</span> ou consulte nossa <a href="#" className="text-[#A3E635] underline">Política de Privacidade</a>.
          </div>
        </div>
      </main>

      {/* Confirm delete modal */}
      {confirmDelete && (
        <div className="fixed inset-0 z-50 flex items-center justify-center px-4" style={{ background: 'rgba(0,0,0,0.7)' }}>
          <div className="cf-card p-6 max-w-md w-full">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 rounded-2xl flex items-center justify-center bg-red-500/15 text-red-400">
                <AlertTriangle size={22} />
              </div>
              <h3 className="font-display text-xl font-bold text-white">Excluir conta?</h3>
            </div>
            <p className="text-sm text-slate-300 leading-relaxed">
              Esta ação é <strong className="text-white">permanente e irreversível</strong>. Todos os seus dados — incluindo XP, progresso, lições concluídas e consentimentos — serão apagados.
            </p>
            <div className="mt-6 flex items-center justify-end gap-3">
              <Button variant="ghost" onClick={() => setConfirmDelete(false)} className="text-slate-300 hover:text-white hover:bg-[#1C2235]">
                Cancelar
              </Button>
              <Button onClick={handleDelete} disabled={deleting} className="bg-red-500 hover:bg-red-600 text-white disabled:opacity-60">
                {deleting ? 'Excluindo...' : 'Sim, excluir'}
              </Button>
            </div>
          </div>
        </div>
      )}

      <Footer />
    </div>
  );
}

function Stat({ icon, value, label, color }) {
  return (
    <div className="cf-card p-4">
      <div className="flex items-center gap-2">
        <span className="w-9 h-9 rounded-xl flex items-center justify-center" style={{ background: `${color}22`, color }}>{icon}</span>
        <div>
          <div className="font-display font-bold text-white text-xl">{value}</div>
          <div className="text-[10px] uppercase text-slate-400 font-bold tracking-wider">{label}</div>
        </div>
      </div>
    </div>
  );
}

function InfoRow({ label, value }) {
  return (
    <div>
      <div className="text-[11px] uppercase text-slate-400 font-bold tracking-wider">{label}</div>
      <div className="text-sm text-white mt-0.5">{value || '—'}</div>
    </div>
  );
}
