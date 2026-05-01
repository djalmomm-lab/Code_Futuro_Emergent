import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { GraduationCap, Plus, Users, KeyRound, Loader2, Building2, ChevronRight, Copy, Check } from 'lucide-react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { classesApi, isAuthed, getErrorMessage } from '../lib/api';
import { logError } from '../lib/logger';
import { toast } from 'sonner';

export default function Schools() {
  const navigate = useNavigate();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [joining, setJoining] = useState(false);
  const [showCreate, setShowCreate] = useState(false);
  const [showJoin, setShowJoin] = useState(false);
  const [copied, setCopied] = useState('');

  // form state
  const [form, setForm] = useState({ name: '', school_name: '', seats: 30 });
  const [inviteCode, setInviteCode] = useState('');

  useEffect(() => {
    if (!isAuthed()) { navigate('/login'); return; }
    refresh();
  }, [navigate]);

  const refresh = async () => {
    setLoading(true);
    try {
      const data = await classesApi.list();
      setItems(data.items || []);
    } catch (err) {
      logError('Schools.list', err);
      toast.error('Erro ao carregar turmas');
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    setCreating(true);
    try {
      const c = await classesApi.create(form);
      toast.success(`Turma "${c.name}" criada!`);
      setShowCreate(false);
      setForm({ name: '', school_name: '', seats: 30 });
      await refresh();
    } catch (err) {
      logError('Schools.create', err);
      toast.error(getErrorMessage(err));
    } finally {
      setCreating(false);
    }
  };

  const handleJoin = async (e) => {
    e.preventDefault();
    setJoining(true);
    try {
      const res = await classesApi.join(inviteCode);
      if (res.already_member) toast.info('Você já era membro dessa turma.');
      else toast.success('Bem-vindo à turma!');
      setShowJoin(false);
      setInviteCode('');
      await refresh();
    } catch (err) {
      logError('Schools.join', err);
      toast.error(getErrorMessage(err));
    } finally {
      setJoining(false);
    }
  };

  const copy = async (text, label) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(label);
      toast.success('Código copiado!');
      setTimeout(() => setCopied(''), 1800);
    } catch {
      toast.error('Não foi possível copiar.');
    }
  };

  return (
    <div className="min-h-screen" style={{ background: 'var(--cf-space)' }}>
      <Navbar />
      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex items-center gap-3 mb-2">
          <GraduationCap size={28} className="text-[#A3E635]" />
          <h1 className="font-display text-3xl md:text-4xl font-bold text-white">CodeFuturo Escolas</h1>
        </div>
        <p className="text-slate-400 text-sm md:text-base max-w-2xl">
          Crie turmas, convide alunos com um código e acompanhe o progresso de cada um em tempo real.
        </p>

        <div className="mt-6 flex flex-wrap gap-3">
          <button
            onClick={() => setShowCreate(true)}
            className="cf-btn-lime inline-flex items-center gap-2 px-5 py-3 rounded-xl text-sm font-bold"
            data-testid="schools-btn-create"
          >
            <Plus size={16} /> Criar turma
          </button>
          <button
            onClick={() => setShowJoin(true)}
            className="inline-flex items-center gap-2 px-5 py-3 rounded-xl text-sm font-bold text-slate-200 hover:bg-[#1C2235] transition border"
            style={{ borderColor: 'var(--cf-border)' }}
            data-testid="schools-btn-join"
          >
            <KeyRound size={16} /> Entrar com código
          </button>
        </div>

        {loading ? (
          <div className="mt-10 flex items-center gap-2 text-slate-400">
            <Loader2 size={16} className="animate-spin" /> Carregando...
          </div>
        ) : items.length === 0 ? (
          <div className="mt-10 cf-card p-8 text-center">
            <Building2 size={32} className="text-slate-500 mx-auto mb-3" />
            <div className="font-display text-lg font-bold text-white">Você ainda não tem turmas</div>
            <div className="mt-1 text-sm text-slate-400">
              Crie uma como professor ou entre em uma com o código fornecido.
            </div>
          </div>
        ) : (
          <div className="mt-8 grid sm:grid-cols-2 gap-4">
            {items.map((c) => (
              <div key={c.id} className="cf-card p-5 flex flex-col" data-testid={`schools-card-${c.id}`}>
                <div className="flex items-start gap-3">
                  <div className="w-12 h-12 rounded-xl flex items-center justify-center shrink-0"
                       style={{ background: c.role === 'teacher' ? 'rgba(163,230,53,0.15)' : 'rgba(124,58,237,0.15)',
                                border: `1px solid ${c.role === 'teacher' ? 'rgba(163,230,53,0.35)' : 'rgba(124,58,237,0.35)'}` }}>
                    <GraduationCap size={22} className={c.role === 'teacher' ? 'text-[#A3E635]' : 'text-violet-300'} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="font-display text-lg font-bold text-white truncate">{c.name}</div>
                    {c.school_name && <div className="text-xs text-slate-400 truncate">{c.school_name}</div>}
                    <div className="mt-1 flex items-center gap-2 text-xs">
                      <span className={`px-2 py-0.5 rounded-md font-bold tracking-wider ${c.role === 'teacher' ? 'bg-[#A3E635] text-[#0A0F1E]' : 'bg-violet-500/20 text-violet-300'}`}>
                        {c.role === 'teacher' ? 'PROFESSOR' : 'ALUNO'}
                      </span>
                      <span className="text-slate-400 inline-flex items-center gap-1"><Users size={12} /> {c.total_members}</span>
                    </div>
                  </div>
                </div>

                {c.role === 'teacher' && c.invite_code && (
                  <div className="mt-4 rounded-lg p-3 flex items-center justify-between"
                       style={{ background: 'var(--cf-panel-light)' }}>
                    <div>
                      <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Código de convite</div>
                      <div className="font-code text-base font-bold text-[#A3E635] mt-0.5">{c.invite_code}</div>
                    </div>
                    <button
                      onClick={() => copy(c.invite_code, c.id)}
                      className="text-slate-400 hover:text-white p-2 rounded-lg hover:bg-[#1C2235]"
                      data-testid={`schools-copy-${c.id}`}
                      aria-label="Copiar código"
                    >
                      {copied === c.id ? <Check size={14} className="text-[#A3E635]" /> : <Copy size={14} />}
                    </button>
                  </div>
                )}

                <button
                  onClick={() => navigate(`/escolas/${c.id}`)}
                  className="mt-4 inline-flex items-center justify-between text-xs font-bold text-slate-300 hover:text-white px-3 py-2 rounded-lg hover:bg-[#1C2235] transition"
                  data-testid={`schools-open-${c.id}`}
                >
                  Abrir turma <ChevronRight size={14} />
                </button>
              </div>
            ))}
          </div>
        )}
      </main>

      {/* Create Class Modal */}
      {showCreate && (
        <Modal onClose={() => !creating && setShowCreate(false)} testId="schools-modal-create">
          <h3 className="font-display text-2xl font-bold text-white">Criar turma</h3>
          <p className="text-sm text-slate-400 mt-1">Você será o professor desta turma e receberá um código de convite para enviar aos alunos.</p>
          <form onSubmit={handleCreate} className="mt-5 space-y-3">
            <Field label="Nome da turma">
              <input
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                required
                placeholder="Ex.: 8º ano A — Programação"
                className="w-full h-11 px-3 rounded-lg bg-[#1C2235] border border-[#1E293B] text-white text-sm outline-none focus:border-[#A3E635]"
                data-testid="schools-input-name"
              />
            </Field>
            <Field label="Escola (opcional)">
              <input
                value={form.school_name}
                onChange={(e) => setForm({ ...form, school_name: e.target.value })}
                placeholder="Ex.: Escola Estadual de SP"
                className="w-full h-11 px-3 rounded-lg bg-[#1C2235] border border-[#1E293B] text-white text-sm outline-none focus:border-[#A3E635]"
              />
            </Field>
            <Field label="Vagas">
              <input
                type="number"
                min={1}
                max={500}
                value={form.seats}
                onChange={(e) => setForm({ ...form, seats: Number(e.target.value) })}
                className="w-full h-11 px-3 rounded-lg bg-[#1C2235] border border-[#1E293B] text-white text-sm outline-none focus:border-[#A3E635]"
              />
            </Field>
            <div className="flex gap-3 pt-2">
              <button type="submit" disabled={creating} className="cf-btn-lime flex-1 px-5 py-3 rounded-xl text-sm font-bold disabled:opacity-50" data-testid="schools-submit-create">
                {creating ? <Loader2 size={14} className="animate-spin inline" /> : 'Criar turma'}
              </button>
              <button type="button" onClick={() => setShowCreate(false)} className="px-5 py-3 rounded-xl text-sm font-bold text-slate-300 hover:bg-[#1C2235]">
                Cancelar
              </button>
            </div>
          </form>
        </Modal>
      )}

      {/* Join Modal */}
      {showJoin && (
        <Modal onClose={() => !joining && setShowJoin(false)} testId="schools-modal-join">
          <h3 className="font-display text-2xl font-bold text-white">Entrar com código</h3>
          <p className="text-sm text-slate-400 mt-1">Cole abaixo o código de 6 caracteres que o seu professor enviou.</p>
          <form onSubmit={handleJoin} className="mt-5 space-y-3">
            <Field label="Código de convite">
              <input
                value={inviteCode}
                onChange={(e) => setInviteCode(e.target.value.toUpperCase())}
                required
                placeholder="EX.: 8H4M5J"
                className="w-full h-11 px-3 rounded-lg bg-[#1C2235] border border-[#1E293B] text-white text-sm outline-none focus:border-[#A3E635] font-code tracking-widest"
                maxLength={12}
                data-testid="schools-input-code"
              />
            </Field>
            <div className="flex gap-3 pt-2">
              <button type="submit" disabled={joining} className="cf-btn-lime flex-1 px-5 py-3 rounded-xl text-sm font-bold disabled:opacity-50" data-testid="schools-submit-join">
                {joining ? <Loader2 size={14} className="animate-spin inline" /> : 'Entrar na turma'}
              </button>
              <button type="button" onClick={() => setShowJoin(false)} className="px-5 py-3 rounded-xl text-sm font-bold text-slate-300 hover:bg-[#1C2235]">
                Cancelar
              </button>
            </div>
          </form>
        </Modal>
      )}

      <Footer />
    </div>
  );
}

const Field = ({ label, children }) => (
  <label className="block">
    <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">{label}</span>
    <div className="mt-1.5">{children}</div>
  </label>
);

const Modal = ({ children, onClose, testId }) => (
  <div
    data-testid={testId}
    className="fixed inset-0 z-50 flex items-center justify-center p-4"
    style={{ background: 'rgba(5,8,18,0.85)', backdropFilter: 'blur(12px)' }}
    onClick={onClose}
  >
    <div
      className="cf-card relative w-full max-w-md p-6 md:p-7"
      style={{ background: 'var(--cf-panel)', border: '1px solid var(--cf-border)' }}
      onClick={(e) => e.stopPropagation()}
    >
      {children}
    </div>
  </div>
);
