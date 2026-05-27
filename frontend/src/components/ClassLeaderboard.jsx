import React, { useEffect, useState } from 'react';
import { Trophy, Flame, Star, Crown, Loader2, Medal } from 'lucide-react';
import { classesApi } from '../lib/api';
import { logError } from '../lib/logger';

const medalFor = (rank) => {
  if (rank === 1) return { color: '#FACC15', label: 'Ouro' };
  if (rank === 2) return { color: '#CBD5E1', label: 'Prata' };
  if (rank === 3) return { color: '#FB923C', label: 'Bronze' };
  return null;
};

export default function ClassLeaderboard({ classId }) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!classId) return;
    (async () => {
      setLoading(true);
      try {
        const data = await classesApi.leaderboard(classId);
        setItems(data.items || []);
      } catch (err) {
        logError('ClassLeaderboard.load', err, { classId });
      } finally {
        setLoading(false);
      }
    })();
  }, [classId]);

  return (
    <div className="cf-card overflow-hidden" data-testid="class-leaderboard">
      <div className="px-5 py-4 flex items-center gap-2 border-b" style={{ borderColor: 'var(--cf-border)' }}>
        <Trophy size={18} className="text-[#A3E635]" />
        <h3 className="font-display text-lg font-bold text-white">Ranking da turma</h3>
      </div>

      {loading ? (
        <div className="p-6 flex items-center gap-2 text-slate-400 text-sm">
          <Loader2 size={14} className="animate-spin" /> Carregando ranking...
        </div>
      ) : items.length === 0 ? (
        <div className="p-6 text-center text-slate-400 text-sm">Sem alunos no ranking ainda.</div>
      ) : (
        <ul>
          {items.map((r) => {
            const medal = medalFor(r.rank);
            return (
              <li
                key={r.user_id}
                data-testid={`leaderboard-row-${r.user_id}`}
                className={`flex items-center gap-3 px-5 py-3 border-t transition ${r.is_me ? 'bg-[#A3E635]/5' : ''}`}
                style={{ borderColor: 'var(--cf-border)' }}
              >
                <div className="w-8 text-center">
                  {medal ? (
                    <Medal size={20} style={{ color: medal.color }} className="inline" />
                  ) : (
                    <span className="text-xs font-bold text-slate-500">#{r.rank}</span>
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className={`font-semibold truncate ${r.is_me ? 'text-[#A3E635]' : 'text-white'}`}>
                      {r.name}
                    </span>
                    {r.is_me && (
                      <span className="px-1.5 py-0.5 rounded bg-[#A3E635] text-[#0A0F1E] text-[9px] font-bold tracking-wider">VOCÊ</span>
                    )}
                    {r.role === 'teacher' && (
                      <span className="px-1.5 py-0.5 rounded bg-violet-500/20 text-violet-300 text-[9px] font-bold tracking-wider">PROF</span>
                    )}
                    {r.is_pro && (
                      <span className="px-1.5 py-0.5 rounded bg-[#A3E635]/20 text-[#A3E635] text-[9px] font-bold tracking-wider inline-flex items-center gap-0.5">
                        <Crown size={9} /> PRO
                      </span>
                    )}
                  </div>
                  <div className="text-xs text-slate-500">{r.completed}/{r.total} lições</div>
                </div>
                <div className="flex items-center gap-3 text-xs">
                  <span className="inline-flex items-center gap-1 font-bold text-[#A3E635]"><Star size={12} /> {r.xp_total}</span>
                  <span className="inline-flex items-center gap-1 font-bold text-orange-400"><Flame size={12} /> {r.streak}</span>
                </div>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
