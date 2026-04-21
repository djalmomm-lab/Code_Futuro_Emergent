import React, { useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, ArrowRight, Check, ShieldCheck, Calendar, User, Mail, Sparkles, Lock } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { ByteLogo } from '../components/ByteMascot';
import { MODULES } from '../data/mockData';
import { SPECIALIZED_TRACKS, DIAGNOSTIC, INTERESTS, recommendTrack } from '../data/specializedTracks';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Checkbox } from '../components/ui/checkbox';
import { toast } from 'sonner';
import { onboardApi, isAuthed, getErrorMessage } from '../lib/api';

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

const STEPS = ['age', 'consent', 'interest', 'diagnostic', 'recommendation'];

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
  const [interest, setInterest] = useState(null);
  const [answers, setAnswers] = useState({});

  const age = useMemo(() => calcAge(birthDate), [birthDate]);
  const needsParent = age !== null && age < 13;
  const isAdult = age !== null && age >= 18;

  // Pick diagnostic set by age bucket
  const diagSet = useMemo(() => {
    if (age === null) return [];
    if (age < 12) return DIAGNOSTIC.kids;
    if (age < 18) return DIAGNOSTIC.teens;
    return DIAGNOSTIC.adults;
  }, [age]);

  const score = useMemo(() => {
    return Object.values(answers).reduce((a, v) => a + (typeof v === 'number' ? v : 0), 0);
  }, [answers]);

  // Build dynamic step list (consent only for <13)
  const activeSteps = useMemo(() => {
    if (needsParent) return ['age', 'consent', 'interest', 'diagnostic', 'recommendation'];
    return ['age', 'interest', 'diagnostic', 'recommendation'];
  }, [needsParent]);

  const stepIndex = activeSteps.indexOf(step);
  const progress = ((stepIndex + 1) / activeSteps.length) * 100;

  const recommendation = useMemo(() => {
    if (step !== 'recommendation') return null;
    return recommendTrack({ age, score, interest, hasParentConsent: consentData });
  }, [step, age, score, interest, consentData]);

  const canNext = () => {
    if (step === 'age') return age !== null && age >= 6 && age <= 99 && studentName.trim().length > 1;
    if (step === 'consent') return consentData && parentName.trim().length > 1 && /\S+@\S+\.\S+/.test(parentEmail);
    if (step === 'interest') return !!interest;
    if (step === 'diagnostic') return Object.keys(answers).length === diagSet.length;
    return true;
  };

  const next = () => {
    if (!canNext()) { toast.error('Preencha todos os campos para continuar'); return; }
    const nextIdx = stepIndex + 1;
    if (nextIdx >= activeSteps.length) {
      finish();
      return;
    }
    setStep(activeSteps[nextIdx]);
  };

  const back = () => {
    if (stepIndex <= 0) { navigate('/'); return; }
    setStep(activeSteps[stepIndex - 1]);
  };

  const finish = async () => {
    if (!isAuthed()) {
      // Store locally and send to register
      localStorage.setItem('cf_pending_onboard', JSON.stringify({
        name: studentName, birthDate, interest, score, recommendation,
        parentName: needsParent ? parentName : null,
        parentEmail: needsParent ? parentEmail : null,
        consentData: needsParent ? consentData : null,
        consentComm: needsParent ? consentComm : null,
      }));
      toast.info('Crie sua conta para salvar a jornada');
      setTimeout(() => navigate('/register'), 500);
      return;
    }
    try {
      await onboardApi.save({
        birth_date: birthDate,
        parent_name: needsParent ? parentName : null,
        parent_email: needsParent ? parentEmail : null,
        consent_data: needsParent ? consentData : null,
        consent_comm: needsParent ? consentComm : null,
        interest,
        diagnostic_score: score,
        recommendation,
      });
      toast.success('Pronto! Vamos começar sua jornada 🚀');
      setTimeout(() => navigate('/dashboard'), 700);
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
            <AgeStep
              studentName={studentName} setStudentName={setStudentName}
              birthDate={birthDate} setBirthDate={setBirthDate}
              age={age}
            />
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

          {step === 'interest' && (
            <InterestStep interest={interest} setInterest={setInterest} />
          )}

          {step === 'diagnostic' && (
            <DiagnosticStep questions={diagSet} answers={answers} setAnswers={setAnswers} />
          )}

          {step === 'recommendation' && recommendation && (
            <RecommendationStep rec={recommendation} age={age} isAdult={isAdult} studentName={studentName} />
          )}

          <div className="mt-8 flex items-center justify-between">
            <Button variant="ghost" onClick={back} className="text-slate-300 hover:text-white hover:bg-[#1C2235]">
              <ArrowLeft size={16} className="mr-1" /> Voltar
            </Button>
            <Button onClick={next} className="cf-btn-lime h-11 px-6 rounded-full">
              {step === 'recommendation' ? 'Começar jornada' : 'Próximo'}
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
      <p className="mt-1 text-sm text-slate-400">Vamos personalizar sua jornada. Primeiro, conta pra gente quem é você.</p>

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
            <div className="mt-2 text-xs text-slate-400">Idade: <span className="font-bold text-white">{age} anos</span>
              {age < 13 && <span className="ml-2 text-[#A3E635]">— precisaremos do consentimento do responsável</span>}
            </div>
          )}
        </div>
      </div>

      <div className="mt-6 p-4 rounded-xl flex items-start gap-3" style={{ background: 'rgba(163,230,53,0.08)', border: '1px solid rgba(163,230,53,0.22)' }}>
        <ShieldCheck size={18} className="text-[#A3E635] mt-0.5 shrink-0" />
        <div className="text-xs text-slate-300 leading-relaxed">
          <div className="font-bold text-white">Seus dados estão protegidos</div>
          Seguimos a LGPD (Lei Geral de Proteção de Dados). Dados de menores de 13 anos exigem consentimento de um responsável legal.
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
          <div className="mt-1.5 text-[11px] text-slate-500">Usaremos este e-mail para validações e avisos importantes sobre a conta da criança.</div>
        </div>
      </div>

      <div className="mt-5 space-y-3">
        <label className="flex items-start gap-3 p-3 rounded-xl cursor-pointer" style={{ background: 'var(--cf-panel-light)' }}>
          <Checkbox checked={consentData} onCheckedChange={setConsentData} className="mt-0.5 border-slate-500 data-[state=checked]:bg-[#A3E635] data-[state=checked]:border-[#A3E635] data-[state=checked]:text-[#0A0F1E]" />
          <span className="text-xs text-slate-200 leading-relaxed">
            <span className="font-bold text-white">Autorizo o tratamento dos dados</span> de acordo com a <a href="#" className="text-[#A3E635] underline">Política de Privacidade</a> e os <a href="#" className="text-[#A3E635] underline">Termos de Uso</a> do CodeFuturo, exclusivamente para fins educacionais. <span className="text-red-400">*obrigatório</span>
          </span>
        </label>
        <label className="flex items-start gap-3 p-3 rounded-xl cursor-pointer" style={{ background: 'var(--cf-panel-light)' }}>
          <Checkbox checked={consentComm} onCheckedChange={setConsentComm} className="mt-0.5 border-slate-500 data-[state=checked]:bg-[#A3E635] data-[state=checked]:border-[#A3E635] data-[state=checked]:text-[#0A0F1E]" />
          <span className="text-xs text-slate-200 leading-relaxed">
            Aceito receber e-mails sobre o progresso do aluno, dicas pedagógicas e novidades. <span className="text-slate-500">(opcional)</span>
          </span>
        </label>
      </div>

      <div className="mt-5 p-3 rounded-xl text-[11px] text-slate-400 leading-relaxed" style={{ background: 'rgba(59,130,246,0.08)', border: '1px solid rgba(59,130,246,0.2)' }}>
        <strong className="text-white">Seus direitos (LGPD):</strong> você pode a qualquer momento solicitar acesso, correção ou exclusão dos dados da criança em <span className="text-[#A3E635]">configurações → privacidade</span>, ou pelo e-mail <span className="text-[#A3E635]">privacidade@codefuturo.com</span>.
      </div>
    </div>
  );
}

function InterestStep({ interest, setInterest }) {
  return (
    <div>
      <h1 className="font-display text-2xl md:text-3xl font-bold text-white">O que mais te anima?</h1>
      <p className="mt-1 text-sm text-slate-400">Escolha o que mais combina com você — vai ajudar a recomendar sua trilha ideal.</p>

      <div className="mt-6 grid grid-cols-2 sm:grid-cols-4 gap-3">
        {INTERESTS.map((it) => {
          const selected = interest === it.id;
          return (
            <button
              key={it.id}
              onClick={() => setInterest(it.id)}
              className={`p-4 rounded-2xl border-2 transition text-center ${selected ? 'bg-[#A3E635]/10 border-[#A3E635]' : 'bg-[#141824] hover:border-slate-600'}`}
              style={selected ? {} : { borderColor: 'var(--cf-border)' }}
            >
              <div className="text-3xl">{it.icon}</div>
              <div className={`mt-2 text-xs font-bold ${selected ? 'text-[#A3E635]' : 'text-white'}`}>{it.label}</div>
            </button>
          );
        })}
      </div>
    </div>
  );
}

function DiagnosticStep({ questions, answers, setAnswers }) {
  return (
    <div>
      <div className="flex items-center gap-2 mb-1">
        <Sparkles size={18} className="text-[#A3E635]" />
        <span className="text-[11px] font-bold uppercase tracking-wider text-[#A3E635]">Teste rápido de nivelamento</span>
      </div>
      <h1 className="font-display text-2xl md:text-3xl font-bold text-white">Conta sobre você</h1>
      <p className="mt-1 text-sm text-slate-400">Sem respostas certas ou erradas — isso nos ajuda a escolher a melhor trilha pra você.</p>

      <div className="mt-6 space-y-5 max-h-[50vh] overflow-y-auto pr-2">
        {questions.map((q, qi) => (
          <div key={qi}>
            <div className="text-sm font-bold text-white mb-2">{qi + 1}. {q.q}</div>
            <div className="grid sm:grid-cols-2 gap-2">
              {q.options.map((opt, oi) => {
                const selected = answers[qi] === oi;
                return (
                  <button
                    key={oi}
                    onClick={() => setAnswers({ ...answers, [qi]: oi })}
                    className={`text-left px-3 py-2.5 rounded-xl border text-sm transition ${selected ? 'bg-[#A3E635]/10 border-[#A3E635] text-white' : 'bg-[#141824] text-slate-300 hover:border-slate-600'}`}
                    style={selected ? {} : { borderColor: 'var(--cf-border)' }}
                  >
                    {opt}
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function RecommendationStep({ rec, age, isAdult, studentName }) {
  const isModule = rec.type === 'module';
  const data = isModule
    ? MODULES.find((m) => m.id === rec.id)
    : SPECIALIZED_TRACKS.find((t) => t.id === rec.id);
  const moduleIndex = isModule ? MODULES.findIndex((m) => m.id === rec.id) : -1;
  const moduleName = isModule ? ['Explorador Digital', 'Criador de Blocos', 'Programador Iniciante', 'Desenvolvedor'][moduleIndex] : data?.name;

  return (
    <div>
      <div className="flex items-center gap-2 mb-1">
        <Sparkles size={18} className="text-[#A3E635]" />
        <span className="text-[11px] font-bold uppercase tracking-wider text-[#A3E635]">Sua recomendação</span>
      </div>
      <h1 className="font-display text-2xl md:text-3xl font-bold text-white">
        {studentName ? `${studentName}, ` : ''}encontramos sua trilha ideal!
      </h1>

      <div
        className="mt-6 p-6 rounded-2xl border-2 relative overflow-hidden"
        style={{ borderColor: data?.color || '#A3E635', background: `linear-gradient(135deg, ${data?.color}22, transparent)` }}
      >
        <div className="absolute -top-16 -right-16 w-40 h-40 rounded-full blur-3xl opacity-60" style={{ background: data?.color }} />
        <div className="relative">
          <div className="flex items-center justify-between">
            <div className="w-14 h-14 rounded-2xl flex items-center justify-center font-display font-bold text-white text-lg" style={{ background: data?.color }}>
              {isModule ? `0${moduleIndex + 1}` : <Sparkles size={24} />}
            </div>
            <span className="text-[11px] font-bold uppercase tracking-wider px-3 py-1 rounded-full" style={{ background: `${data?.color}22`, color: data?.color }}>
              {isAdult ? 'Trilha Especializada' : 'Módulo por Idade'}
            </span>
          </div>
          <h2 className="mt-4 font-display text-2xl font-bold text-white">{moduleName}</h2>
          <p className="mt-2 text-sm text-slate-300 leading-relaxed">{rec.reason}</p>

          <div className="mt-4 flex flex-wrap gap-2">
            {isModule ? (
              <>
                <Pill>📚 {data?.lessons} lições</Pill>
                <Pill>🎮 Gamificado</Pill>
                <Pill>🏆 Certificado</Pill>
              </>
            ) : (
              <>
                <Pill>📚 {data?.lessons} lições</Pill>
                <Pill>⏱ ~{data?.hours}h</Pill>
                <Pill>📈 {data?.level}</Pill>
              </>
            )}
          </div>
        </div>
      </div>

      <div className="mt-5 p-4 rounded-xl flex items-start gap-3" style={{ background: 'var(--cf-panel-light)' }}>
        <Check size={18} className="text-[#A3E635] mt-0.5 shrink-0" />
        <div className="text-xs text-slate-300 leading-relaxed">
          Esta é só uma <strong className="text-white">sugestão</strong>. Você pode explorar outras trilhas no Catálogo a qualquer momento — a partir dos 15 anos, também tem acesso às Trilhas Especializadas (Ciência de Dados, Mobile, Web Full Stack etc).
        </div>
      </div>
    </div>
  );
}

function Pill({ children }) {
  return <span className="px-2.5 py-1 rounded-full text-[11px] font-bold bg-[#1C2235] text-slate-200">{children}</span>;
}
