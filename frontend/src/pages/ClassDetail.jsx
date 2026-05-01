import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, Users, Crown, Trash2, Loader2, GraduationCap, Star, Flame, Copy, Check, AlertTriangle } from 'lucide-react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { classesApi, isAuthed, getErrorMessage } from '../lib/api';
import { logError } from '../lib/logger';
import { toast } from 'sonner';

export default function ClassDetail() {
  const navigate = useNavigate();
  const { classId } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState('');
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (!isAuthed()) { navigate('/login'); return; }
    refresh();
  }, [navigate, classId]);

  const refresh = async () => {
    setLoading(true);
    try {
      const res = await classesApi.detail(classId);
      setData(res);
    } catch (err) {
      logError('ClassDetail.load', err, { classId });
      toast.error(getErrorMessage(err));
      navigate('/escolas');
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveStudent = async (uid) => {
    setBusy(uid);
    try {
      await classesApi.removeStudent(classId, uid);
      toast.success('Aluno removido da turma.');
      await refresh();
    } catch (err) {
      logError('ClassDetail.removeStudent', err);
      toast.error(getErrorMessage(err));
    } finally {
      setBusy('');
    }
  };

  const handleDeleteClass = async () => {
    setBusy('delete');
    try {
      await classesApi.remove(classId);
      toast.success('Turma excluída.');
      navigate('/escolas');
    } catch (err) {
      logError('ClassDetail.delete', err);
      toast.error(getErrorMessage(err));
      setBusy('');
    }
  };

  const copyCode = async () => {
    if (!data?.class?.invite_code) return;
    try {
      await navigator.clipboard.writeText(data.class.invite_code);
      setCopied(true);
      toast.success('Código copiado!');
      setTimeout(() => setCopied(false), 1800);
    } catch { /* noop */ }
  };

  if (loading || !data) {
    return (
      <div className="min-h-screen" style={{ background: 'var(--cf-space)' }}>
        <Navbar />
        <div className="max-w-5xl mx-auto px-4 py-20 text-center text-slate-400">Carregando turma...</div>
        <Footer />
      </div>
    );
  }

  const klass = data.class;
  const isTeacher = data.is_teacher;

  return (
    <div className="min-h-screen" style={{ background: 'var(--cf-space)' }}>
      <Navbar />
      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <button onClick={() => navigate('/escolas')} className="text-slate-400 hover:text-white flex items-center gap-2 text-sm font-semibold mb-6">
          <ArrowLeft size={16} /> Minhas turmas
        </button>

        <div className="cf-card p-6 md:p-8 relative overflow-hidden">
          <div className="absolute -top-20 -right-20 w-60 h-60 rounded-full blur-3xl opacity-30" style={{ background: '#A3E635' }} />
          <div className="relative flex items-start justify-between flex-wrap gap-4">
            <div className="flex gap-4 items-center">
              <div className="w-16 h-16 rounded-2xl flex items-center justify-center shrink-0"
                   style={{ background: 'rgba(163,230,53,0.15)', border: '1px solid rgba(163,230,53,0.35)' }}>
                <GraduationCap size={28} className="text-[#A3E635]" />
              </div>
              <div>
                <div className="text-xs text-slate-400 font-bold uppercase tracking-wider">{isTeacher ? 'Você é o professor' : 'Você é aluno'}</div>
                <h1 className="font-display text-3xl md:text-4xl font-bold text-white mt-1">{klass.name}</h1>
                {klass.school_name && <p className="mt-1 text-sm text-slate-400">{klass.school_name}</p>}
              </div>
            </div>
            <div className="text-right">
              <div className="inline-flex items-center gap-2 text-sm text-slate-300">
                <Users size={14} /> {klass.total_members} membros
              </div>
            </div>
          </div>

          {isTeacher && klass.invite_code && (
            <div className="mt-6 rounded-xl p-4 flex items-center justify-between"
                 style={{ background: 'var(--cf-panel-light)', border: '1px solid var(--cf-border)' }}>
              <div>
                <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Código de convite</div>
                <div className="font-code text-2xl font-bold text-[#A3E635] mt-0.5 tracking-widest">{klass.invite_code}</div>
                <div className="text-xs text-slate-500 mt-1">Compartilhe este código com seus alunos.</div>
              </div>
              <button onClick={copyCode} className="cf-btn-lime inline-flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-bold" data-testid="class-copy-code">
                {copied ? <Check size={14} /> : <Copy size={14} />} {copied ? 'Copiado!' : 'Copiar'}
              </button>
            </div>
          )}
        </div>

        {isTeacher ? (
          <div className="mt-8">
            <h2 className="font-display text-xl font-bold text-white mb-4">Alunos ({data.students.length})</h2>
            {data.students.length === 0 ? (
              <div className="cf-card p-8 text-center text-slate-400">
                Nenhum aluno entrou ainda. Compartilhe o código <span className="font-code text-[#A3E635]">{klass.invite_code}</span> com a turma.
              </div>
            ) : (
              <div className="cf-card overflow-hidden">
                <table className="w-full text-sm">
                  <thead className="bg-[#1C2235] text-slate-400 text-[11px] uppercase tracking-wider">
                    <tr>
                      <th className="text-left px-4 py-3">Aluno</th>
                      <th className="text-left px-4 py-3">Progresso</th>
                      <th className="text-left px-4 py-3 hidden md:table-cell">XP</th>
                      <th className="text-left px-4 py-3 hidden md:table-cell">Streak</th>
                      <th className="px-4 py-3"></th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.students.map((s) => {
                      const pct = s.total ? Math.round((s.completed / s.total) * 100) : 0;
                      return (
                        <tr key={s.user_id} className="border-t" style={{ borderColor: 'var(--cf-border)' }} data-testid={`class-student-${s.user_id}`}>
                          <td className="px-4 py-3">
                            <div className="flex items-center gap-2">
                              <span className="text-white font-semibold">{s.name}</span>
                              {s.is_pro && <span className="px-1.5 py-0.5 rounded bg-[#A3E635] text-[#0A0F1E] text-[9px] font-bold tracking-wider"><Crown size={9} className="inline -mt-0.5" /> PRO</span>}
                            </div>
                            <div className="text-xs text-slate-500">{s.email}</div>
                          </td>
                          <td className="px-4 py-3">
                            <div className="flex items-center gap-2 max-w-[220px]">
                              <div className="flex-1 h-1.5 rounded-full bg-[#1C2235] overflow-hidden">
                                <div className="h-full rounded-full" style={{ width: `${pct}%`, background: '#A3E635' }} />
                              </div>
                              <span className="text-xs text-slate-400 font-bold whitespace-nowrap">{s.completed}/{s.total}</span>
                            </div>
                          </td>
                          <td className="px-4 py-3 hidden md:table-cell"><span className="text-[#A3E635] font-bold inline-flex items-center gap-1"><Star size={12} /> {s.xp_total}</span></td>
                          <td className="px-4 py-3 hidden md:table-cell"><span className="text-orange-400 font-bold inline-flex items-center gap-1"><Flame size={12} /> {s.streak}</span></td>
                          <td className="px-4 py-3 text-right">
                            <button
                              onClick={() => handleRemoveStudent(s.user_id)}
                              disabled={busy === s.user_id}
                              className="text-slate-400 hover:text-red-400 p-1.5 rounded-lg hover:bg-[#1C2235] disabled:opacity-50"
                              data-testid={`class-remove-${s.user_id}`}
                              title="Remover aluno"
                            >
                              {busy === s.user_id ? <Loader2 size={14} className="animate-spin" /> : <Trash2 size={14} />}
                            </button>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}

            <div className="mt-8 cf-card p-5 flex items-center justify-between gap-4"
                 style={{ border: '1px solid rgba(244,63,94,0.2)' }}>
              <div className="flex items-center gap-3">
                <AlertTriangle size={18} className="text-rose-400" />
                <div>
                  <div className="font-display font-bold text-white">Excluir turma</div>
                  <div className="text-xs text-slate-400">Esta ação não pode ser desfeita.</div>
                </div>
              </div>
              {confirmDelete ? (
                <div className="flex gap-2">
                  <button onClick={handleDeleteClass} disabled={busy === 'delete'} className="px-4 py-2 rounded-lg bg-rose-500 hover:bg-rose-600 text-white text-xs font-bold disabled:opacity-50" data-testid="class-confirm-delete">
                    {busy === 'delete' ? <Loader2 size={12} className="animate-spin inline" /> : 'Excluir definitivamente'}
                  </button>
                  <button onClick={() => setConfirmDelete(false)} className="px-4 py-2 rounded-lg text-xs font-bold text-slate-300 hover:bg-[#1C2235]">
                    Cancelar
                  </button>
                </div>
              ) : (
                <button onClick={() => setConfirmDelete(true)} className="px-4 py-2 rounded-lg text-xs font-bold text-rose-400 hover:bg-[#1C2235]" data-testid="class-delete-btn">
                  Excluir
                </button>
              )}
            </div>
          </div>
        ) : (
          <div className="mt-8 cf-card p-6">
            <h2 className="font-display text-lg font-bold text-white">Você está nesta turma</h2>
            <p className="mt-1 text-sm text-slate-400">Continue suas trilhas — seu professor acompanha o progresso aqui.</p>
            <button onClick={() => navigate('/catalogo')} className="mt-4 cf-btn-lime px-5 py-2.5 rounded-xl text-sm font-bold inline-flex items-center gap-2">
              Ir para as trilhas
            </button>
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
}
