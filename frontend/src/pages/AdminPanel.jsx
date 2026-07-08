import { useState, useEffect, useCallback } from 'react';
import { toast } from 'sonner';

const API = process.env.REACT_APP_API_URL || 'https://codefuturoemergent-production.up.railway.app/api';
const SECRET_KEY = 'cf_admin_secret';

export default function AdminPanel() {
  const [secret, setSecret] = useState(() => sessionStorage.getItem(SECRET_KEY) || '');
  const [authed, setAuthed] = useState(false);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState('');
  const [emailInput, setEmailInput] = useState('');
  const [promoting, setPromoting] = useState(null);

  const headers = { 'x-admin-secret': secret, 'Content-Type': 'application/json' };

  const fetchUsers = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API}/admin/users?limit=200`, { headers });
      if (res.status === 403) { setAuthed(false); toast.error('Senha incorreta'); return; }
      const data = await res.json();
      setUsers(data.users || []);
      setAuthed(true);
      sessionStorage.setItem(SECRET_KEY, secret);
    } catch {
      toast.error('Erro ao conectar com a API');
    } finally {
      setLoading(false);
    }
  }, [secret]); // eslint-disable-line react-hooks/exhaustive-deps

  async function setPro(email, isPro) {
    setPromoting(email);
    try {
      const res = await fetch(`${API}/admin/set-pro`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ email, is_pro: isPro }),
      });
      const data = await res.json();
      if (!data.ok) { toast.error(data.message || 'Erro'); return; }
      toast.success(isPro ? `${email} promovido a Pro` : `${email} revertido para Free`);
      setUsers(prev => prev.map(u => u.email === email ? { ...u, is_pro: isPro, plan: isPro ? 'admin' : null } : u));
    } catch {
      toast.error('Erro ao atualizar usuário');
    } finally {
      setPromoting(null);
    }
  }

  async function promoteByEmail() {
    if (!emailInput.trim()) return;
    await setPro(emailInput.trim().toLowerCase(), true);
    setEmailInput('');
    await fetchUsers();
  }

  const filtered = users.filter(u =>
    !search || u.email?.includes(search.toLowerCase()) || u.name?.toLowerCase().includes(search.toLowerCase())
  );
  const pros = filtered.filter(u => u.is_pro);
  const frees = filtered.filter(u => !u.is_pro);

  if (!authed) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center">
        <div className="bg-gray-900 border border-gray-700 rounded-2xl p-8 w-full max-w-sm space-y-4">
          <h1 className="text-white text-2xl font-bold text-center">Painel Admin</h1>
          <p className="text-gray-400 text-sm text-center">CodeFuturo</p>
          <input
            type="password"
            placeholder="Senha de admin"
            value={secret}
            onChange={e => setSecret(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && fetchUsers()}
            className="w-full bg-gray-800 border border-gray-600 rounded-lg px-4 py-2.5 text-white placeholder-gray-500 focus:outline-none focus:border-purple-500"
          />
          <button
            onClick={fetchUsers}
            disabled={loading}
            className="w-full bg-purple-600 hover:bg-purple-500 text-white font-semibold py-2.5 rounded-lg transition disabled:opacity-50"
          >
            {loading ? 'Entrando...' : 'Entrar'}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white p-6">
      <div className="max-w-4xl mx-auto space-y-6">

        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">Painel Admin</h1>
            <p className="text-gray-400 text-sm">{users.length} usuários · {users.filter(u => u.is_pro).length} Pro</p>
          </div>
          <button
            onClick={() => { setAuthed(false); sessionStorage.removeItem(SECRET_KEY); }}
            className="text-gray-500 hover:text-red-400 text-sm transition"
          >
            Sair
          </button>
        </div>

        {/* Promover por e-mail */}
        <div className="bg-gray-900 border border-gray-700 rounded-xl p-4 flex gap-3">
          <input
            type="email"
            placeholder="E-mail para promover a Pro"
            value={emailInput}
            onChange={e => setEmailInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && promoteByEmail()}
            className="flex-1 bg-gray-800 border border-gray-600 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 text-sm"
          />
          <button
            onClick={promoteByEmail}
            disabled={!emailInput.trim() || promoting}
            className="bg-purple-600 hover:bg-purple-500 text-white font-semibold px-5 py-2 rounded-lg transition disabled:opacity-40 text-sm whitespace-nowrap"
          >
            Promover Pro
          </button>
        </div>

        {/* Busca */}
        <input
          type="text"
          placeholder="Buscar por nome ou e-mail..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-2.5 text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 text-sm"
        />

        {/* Usuários Pro */}
        {pros.length > 0 && (
          <section>
            <h2 className="text-sm font-semibold text-purple-400 uppercase tracking-wider mb-2">Pro ({pros.length})</h2>
            <div className="space-y-2">
              {pros.map(u => (
                <UserRow key={u.id || u.email} user={u} promoting={promoting} onToggle={setPro} />
              ))}
            </div>
          </section>
        )}

        {/* Usuários Free */}
        {frees.length > 0 && (
          <section>
            <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Free ({frees.length})</h2>
            <div className="space-y-2">
              {frees.map(u => (
                <UserRow key={u.id || u.email} user={u} promoting={promoting} onToggle={setPro} />
              ))}
            </div>
          </section>
        )}

        {loading && <p className="text-gray-500 text-sm text-center">Carregando...</p>}
      </div>
    </div>
  );
}

function UserRow({ user, promoting, onToggle }) {
  const busy = promoting === user.email;
  return (
    <div className="flex items-center justify-between bg-gray-900 border border-gray-800 rounded-xl px-4 py-3 hover:border-gray-700 transition">
      <div>
        <p className="text-white text-sm font-medium">{user.name || '—'}</p>
        <p className="text-gray-400 text-xs">{user.email}</p>
      </div>
      <div className="flex items-center gap-3">
        <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${user.is_pro ? 'bg-purple-900 text-purple-300' : 'bg-gray-800 text-gray-500'}`}>
          {user.is_pro ? 'Pro' : 'Free'}
        </span>
        <button
          onClick={() => onToggle(user.email, !user.is_pro)}
          disabled={busy}
          className={`text-xs px-3 py-1.5 rounded-lg font-medium transition disabled:opacity-40 ${
            user.is_pro
              ? 'bg-gray-800 hover:bg-red-900 text-gray-400 hover:text-red-300'
              : 'bg-purple-800 hover:bg-purple-700 text-purple-200'
          }`}
        >
          {busy ? '...' : user.is_pro ? 'Revogar Pro' : 'Tornar Pro'}
        </button>
      </div>
    </div>
  );
}
