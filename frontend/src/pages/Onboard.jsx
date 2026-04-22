import React, { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, ArrowRight, Check, ShieldCheck, Calendar, User, Mail, Lock, Sparkles } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { ByteLogo } from '../components/ByteMascot';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Checkbox } from '../components/ui/checkbox';
import { toast } from 'sonner';
import { onboardApi, pathsApi, isAuthed, getErrorMessage } from '../lib/api';
import { logError } from '../lib/logger';

function calcAge(birthDate) {
  if (!birthDate) return null;
  const bd = new Date(birthDate);
  if (isNaN(bd.getTime())) return null;
  const today = new Date();
  let age = today.getFullYear() - bd.getFullYear();
  const m = today.getMonth() - bd.getMonth();
  if (m < 0 || (m === 0 && today.getDate() < bd.getDate())) age--;
  return age;
}

export default function Onboard() {
  const navigate = useNavigate();
  const { t } = useLanguage();

  const [step, setStep] = useState('age');
  const [birthDate, setBirthDate] = useState('');
  const [studentName, setStudentName] = useState('');
  const [parentName, setParentName] = useState('');
  const [parentEmail, setParentEmail] = useState('');
  const [consentData, setConsentData] = useState(false);
  const [consentComm, setConsentComm] = useState(false);
  const [pickedPath, setPickedPath] = useState(null);
  const [level, setLevel] = useState(null);
  const [paths, setPaths] = useState([]);

  useEffect(() => {
    (async () => {
      try {
        const r = await pathsApi.list();
        setPaths(r.paths || []);
      } catch (err) {
        logError('Onboard.loadPaths', err);
      }
    })();
  }, []);

  const age = useMemo(() => calcAge(birthDate), [birthDate]);
  const needsParent = age !== null && age < 13;

  const activeSteps = useMemo(() => {
    if (needsParent) return ['age', 'consent', 'path', 'level'];
    return ['age', 'path', 'level'];
  }, [needsParent]);

  const stepIndex = activeSteps.indexOf(step);
  const progress = ((stepIndex + 1) / activeSteps.length) * 100;

  const canNext = () => {
    if (step === 'age') return age !== null && age >= 5 && age <= 99 && studentName.trim().length > 1;
    if (step === 'consent') return consentData && parentName.trim().length > 1 && /\S+@\S+\.\S+/.test(parentEmail);
    if (step === 'path') return !!pickedPath;
    if (step === 'level') return !!level;
    return true;
  };

  const next = () => {
    if (!canNext()) { toast.error('Preencha todos os campos para continuar'); return; }
    const nextIdx = stepIndex + 1;
    if (nextIdx >= activeSteps.length) { finish(); return; }
    setStep(activeSteps[nextIdx]);
  };

  const back = () => {
    if (stepIndex <= 0) { navigate('/'); return; }
    setStep(activeSteps[stepIndex - 1]);
  };

  const finish = async () => {
    const payload = {
      birth_date: birthDate,
      parent_name: needsParent ? parentName : null,
      parent_email: needsParent ? parentEmail : null,
      consent_data: needsParent ? consentData : null,
      consent_comm: needsParent ? consentComm : null,
      interest: pickedPath,
      diagnostic_score: level === 'beginner' ? 0 : level === 'intermediate' ? 5 : 10,
      recommendation: { type: 'path', id: pickedPath, reason: 'Escolha do usuário' },
    };
    if (!isAuthed()) {
      localStorage.setItem('cf_pending_onboard', JSON.stringify({ ...payload, studentName }));
      toast.info('Crie sua conta para salvar a jornada');
      setTimeout(() => navigate('/register'), 500);
      return;
    }
    try {
      await onboardApi.save(payload);
      toast.success('Pronto! Vamos começar sua jornada 🚀');
      setTimeout(() => navigate(`/jornada/${pickedPath}`), 600);
    } catch (err) {
      toast.error(getErrorMessage(err));
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center px-4 py-10 relative overflow-hidden">
      <div className="absolute inset-0 cf-grid-bg opacity-40 pointer-events-none" />

      <div className="relative w-full max-w-2xl">
        <div className="flex items-center justify-center gap-2 mb-6">
          <ByteLogo size={40} />
          <span className="font-display text-xl font-bold text-white">CodeFuturo</span>
        </div>

        <div className="mb-6">
          <div className="flex items-center justify-between text-xs text-slate-400 font-semibold mb-2">
            <span>Passo {stepIndex + 1} de {activeSteps.length}</span>
            <span>{Math.round(progress)}%</span>
          </div>
          <div className="h-2 rounded-full bg-[#1C2235] overflow-hidden">
            <div className="h-full bg-[#A3E635] transition-all duration-500" style={{ width: `${progress}%` }} />
          </div>
        </div>

        <div className="cf-card p-6 md:p-10">
          {step === 'age' && (
            <AgeStep studentName={studentName} setStudentName={setStudentName} birthDate={birthDate} setBirthDate={setBirthDate} age={age} />
          )}
          {step === 'consent' && (
            <ConsentStep
              parentName={parentName} setParentName={setParentName}
              parentEmail={parentEmail} setParentEmail={setParentEmail}
              consentData={consentData} setConsentData={setConsentData}
              consentComm={consentComm} setConsentComm={setConsentComm}
              studentName={studentName} age={age}
            />
          )}
          {step === 'path' && (
            <PathStep paths={paths} pickedPath={pickedPath} setPickedPath={setPickedPath} />
          )}
          {step === 'level' && (
            <LevelStep level={level} setLevel={setLevel} />
          )}

          <div className="mt-8 flex items-center justify-between">
            <Button variant="ghost" onClick={back} className="text-slate-300 hover:text-white hover:bg-[#1C2235]">
              <ArrowLeft size={16} className="mr-1" /> Voltar
            </Button>
            <Button onClick={next} className="cf-btn-lime h-11 px-6 rounded-full">
              {step === 'level' ? 'Começar' : 'Próximo'}
              <ArrowRight size={16} className="ml-1" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}

function AgeStep({ studentName, setStudentName, birthDate, setBirthDate, age }) {
  return (
    <div>
      <h1 className="font-display text-2xl md:text-3xl font-bold text-white">Bem-vindo ao CodeFuturo!</h1>
      <p className="mt-1 text-sm text-slate-400">Conta pra gente quem é você. Só pedimos a idade para cumprir a LGPD.</p>

      <div className="mt-6 space-y-4">
        <div>
          <Label className="text-slate-300 text-sm font-semibold">Seu nome</Label>
          <div className="mt-1.5 relative">
            <User size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
            <Input value={studentName} onChange={(e) => setStudentName(e.target.value)} placeholder="Como você quer ser chamado(a)" className="pl-10 h-11 bg-[#1C2235] border-[#1E293B] text-white" />
          </div>
        </div>
        <div>
          <Label className="text-slate-300 text-sm font-semibold">Data de nascimento</Label>
          <div className="mt-1.5 relative">
            <Calendar size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
            <Input type="date" value={birthDate} onChange={(e) => setBirthDate(e.target.value)} max={new Date().toISOString().split('T')[0]} className="pl-10 h-11 bg-[#1C2235] border-[#1E293B] text-white" />
          </div>
          {age !== null && age >= 0 && (
            <div className="mt-2 text-xs text-slate-400">
              {age < 13 && <span className="text-[#A3E635]">Como você tem menos de 13 anos, precisaremos do consentimento do responsável (LGPD).</span>}
              {age >= 13 && <span>Pronto — você tem {age} anos.</span>}
            </div>
          )}
        </div>
      </div>

      <div className="mt-6 p-4 rounded-xl flex items-start gap-3" style={{ background: 'rgba(163,230,53,0.08)', border: '1px solid rgba(163,230,53,0.22)' }}>
        <ShieldCheck size={18} className="text-[#A3E635] mt-0.5 shrink-0" />
        <div className="text-xs text-slate-300 leading-relaxed">
          <div className="font-bold text-white">Seus dados estão protegidos</div>
          Seguimos a LGPD. Dados de menores de 13 anos exigem autorização do responsável legal.
        </div>
      </div>
    </div>
  );
}

function ConsentStep({ parentName, setParentName, parentEmail, setParentEmail, consentData, setConsentData, consentComm, setConsentComm, studentName, age }) {
  return (
    <div>
      <div className="flex items-center gap-2 mb-1">
        <Lock size={18} className="text-[#A3E635]" />
        <span className="text-[11px] font-bold uppercase tracking-wider text-[#A3E635]">Consentimento LGPD</span>
      </div>
      <h1 className="font-display text-2xl md:text-3xl font-bold text-white">Consentimento do responsável</h1>
      <p className="mt-1 text-sm text-slate-400">
        Como {studentName || 'o aluno'} tem {age} anos, precisamos que um responsável legal autorize o cadastro.
      </p>

      <div className="mt-6 space-y-4">
        <div>
          <Label className="text-slate-300 text-sm font-semibold">Nome do responsável</Label>
          <div className="mt-1.5 relative">
            <User size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
            <Input value={parentName} onChange={(e) => setParentName(e.target.value)} placeholder="Nome completo" className="pl-10 h-11 bg-[#1C2235] border-[#1E293B] text-white" />
          </div>
        </div>
        <div>
          <Label className="text-slate-300 text-sm font-semibold">E-mail do responsável</Label>
          <div className="mt-1.5 relative">
            <Mail size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
            <Input type="email" value={parentEmail} onChange={(e) => setParentEmail(e.target.value)} placeholder="seu@email.com" className="pl-10 h-11 bg-[#1C2235] border-[#1E293B] text-white" />
          </div>
        </div>
      </div>

      <div className="mt-5 space-y-3">
        <label className="flex items-start gap-3 p-3 rounded-xl cursor-pointer" style={{ background: 'var(--cf-panel-light)' }}>
          <Checkbox checked={consentData} onCheckedChange={setConsentData} className="mt-0.5 border-slate-500 data-[state=checked]:bg-[#A3E635] data-[state=checked]:border-[#A3E635] data-[state=checked]:text-[#0A0F1E]" />
          <span className="text-xs text-slate-200 leading-relaxed">
            <span className="font-bold text-white">Autorizo o tratamento dos dados</span> conforme a <a href="#" className="text-[#A3E635] underline">Política de Privacidade</a> e os <a href="#" className="text-[#A3E635] underline">Termos de Uso</a>. <span className="text-red-400">*obrigatório</span>
          </span>
        </label>
        <label className="flex items-start gap-3 p-3 rounded-xl cursor-pointer" style={{ background: 'var(--cf-panel-light)' }}>
          <Checkbox checked={consentComm} onCheckedChange={setConsentComm} className="mt-0.5 border-slate-500 data-[state=checked]:bg-[#A3E635] data-[state=checked]:border-[#A3E635] data-[state=checked]:text-[#0A0F1E]" />
          <span className="text-xs text-slate-200 leading-relaxed">
            Aceito receber e-mails sobre o progresso do aluno. <span className="text-slate-500">(opcional)</span>
          </span>
        </label>
      </div>

      <div className="mt-5 p-3 rounded-xl text-[11px] text-slate-400 leading-relaxed" style={{ background: 'rgba(59,130,246,0.08)', border: '1px solid rgba(59,130,246,0.2)' }}>
        <strong className="text-white">Seus direitos (LGPD):</strong> você pode a qualquer momento solicitar acesso, correção ou exclusão dos dados em <span className="text-[#A3E635]">perfil → privacidade</span>.
      </div>
    </div>
  );
}

function PathStep({ paths, pickedPath, setPickedPath }) {
  return (
    <div>
      <h1 className="font-display text-2xl md:text-3xl font-bold text-white">Qual linguagem você quer aprender primeiro?</h1>
      <p className="mt-1 text-sm text-slate-400">Você pode trocar depois e explorar outras no catálogo.</p>

      <div className="mt-6 grid grid-cols-2 sm:grid-cols-3 gap-3">
        {paths.map((p) => {
          const selected = pickedPath === p.slug;
          return (
            <button
              key={p.slug}
              onClick={() => setPickedPath(p.slug)}
              className={`relative p-4 rounded-2xl border-2 transition text-left overflow-hidden ${selected ? 'bg-[#1C2235]' : 'bg-[#141824] hover:border-slate-600'}`}
              style={{ borderColor: selected ? p.color : 'var(--cf-border)' }}
            >
              <div className="absolute -top-10 -right-10 w-24 h-24 rounded-full blur-2xl opacity-60" style={{ background: p.color }} />
              <div className="relative">
                <div className="w-10 h-10 rounded-xl flex items-center justify-center font-display font-bold text-white text-sm" style={{ background: p.color }}>
                  {p.name.substring(0, 2).toUpperCase()}
                </div>
                <div className="mt-3 font-display font-bold text-white text-sm">{p.name}</div>
                <div className="text-[11px] text-slate-400 mt-0.5">{p.total_lessons} lições</div>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}

function LevelStep({ level, setLevel }) {
  return (
    <div>
      <div className="flex items-center gap-2 mb-1">
        <Sparkles size={18} className="text-[#A3E635]" />
        <span className="text-[11px] font-bold uppercase tracking-wider text-[#A3E635]">Seu nível</span>
      </div>
      <h1 className="font-display text-2xl md:text-3xl font-bold text-white">Qual seu nível atual?</h1>
      <p className="mt-1 text-sm text-slate-400">Vamos começar a trilha do ponto certo para você.</p>

      <div className="mt-6 space-y-3">
        {[
          { id: 'beginner', emoji: '🌱', title: 'Iniciante', desc: 'Estou começando do zero' },
          { id: 'intermediate', emoji: '🚀', title: 'Intermediário', desc: 'Já sei o básico' },
          { id: 'advanced', emoji: '🏆', title: 'Avançado', desc: 'Quero aprofundar e projetos' },
        ].map((l) => {
          const selected = level === l.id;
          return (
            <button
              key={l.id}
              onClick={() => setLevel(l.id)}
              className={`w-full flex items-center gap-4 p-4 rounded-2xl border-2 transition ${selected ? 'bg-[#1C2235] border-[#A3E635]' : 'bg-[#141824] hover:border-slate-600'}`}
              style={selected ? {} : { borderColor: 'var(--cf-border)' }}
            >
              <span className="text-3xl">{l.emoji}</span>
              <div className="flex-1 text-left">
                <div className="font-display font-bold text-white">{l.title}</div>
                <div className="text-xs text-slate-400">{l.desc}</div>
              </div>
              {selected && <Check size={20} className="text-[#A3E635]" />}
            </button>
          );
        })}
      </div>
    </div>
  );
}
