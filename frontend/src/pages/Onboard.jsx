import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, ArrowRight, Check } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { ByteLogo } from '../components/ByteMascot';
import { MODULES } from '../data/mockData';
import { Button } from '../components/ui/button';
import { toast } from 'sonner';

export default function Onboard() {
  const { t } = useLanguage();
  const [step, setStep] = useState(0);
  const [module, setModule] = useState(null);
  const [language, setLanguage] = useState(null);
  const [level, setLevel] = useState(null);
  const navigate = useNavigate();

  const steps = [t('onboard.step1Title'), t('onboard.step2Title'), t('onboard.step3Title')];
  const progress = ((step + 1) / steps.length) * 100;

  const canContinue = (step === 0 && module) || (step === 1 && language) || (step === 2 && level);

  const next = () => {
    if (!canContinue) { toast.error('Selecione uma opção'); return; }
    if (step < steps.length - 1) setStep(step + 1);
    else {
      localStorage.setItem('cf_onboard', JSON.stringify({ module, language, level }));
      toast.success('Vamos começar sua jornada!');
      setTimeout(() => navigate('/dashboard'), 600);
    }
  };

  const back = () => { if (step > 0) setStep(step - 1); };

  return (
    <div className="min-h-screen flex flex-col items-center px-4 py-10 relative overflow-hidden">
      <div className="absolute inset-0 cf-grid-bg opacity-40 pointer-events-none" />

      <div className="relative w-full max-w-2xl">
        <div className="flex items-center justify-center gap-2 mb-8">
          <ByteLogo size={40} />
          <span className="font-display text-xl font-bold text-white">CodeFuturo</span>
        </div>

        <div className="mb-6">
          <div className="flex items-center justify-between text-xs text-slate-400 font-semibold mb-2">
            <span>Passo {step + 1} de {steps.length}</span>
            <span>{Math.round(progress)}%</span>
          </div>
          <div className="h-2 rounded-full bg-[#1C2235] overflow-hidden">
            <div className="h-full bg-[#A3E635] transition-all duration-500" style={{ width: `${progress}%` }} />
          </div>
        </div>

        <div className="cf-card p-6 md:p-10">
          <h1 className="font-display text-2xl md:text-3xl font-bold text-white">{steps[step]}</h1>
          <p className="mt-1 text-sm text-slate-400">{step === 0 ? 'Encontre o módulo ideal para você.' : step === 1 ? 'Escolha sua primeira linguagem.' : 'Conta pra gente seu nível atual.'}</p>

          {step === 0 && (
            <div className="mt-6 grid sm:grid-cols-2 gap-3">
              {MODULES.map((m, i) => {
                const selected = module === m.id;
                return (
                  <button
                    key={m.id}
                    onClick={() => setModule(m.id)}
                    className={`text-left p-4 rounded-2xl border-2 transition ${selected ? 'bg-[#1C2235]' : 'bg-[#141824] hover:border-slate-600'}`}
                    style={{ borderColor: selected ? m.color : 'var(--cf-border)' }}
                  >
                    <div className="flex items-center justify-between">
                      <div className="w-10 h-10 rounded-xl flex items-center justify-center font-display font-bold text-white text-sm" style={{ background: m.color }}>0{i + 1}</div>
                      {selected && <Check size={18} style={{ color: m.color }} />}
                    </div>
                    <div className="mt-3 font-display font-bold text-white">{t(`modules.m${i + 1}.name`)}</div>
                    <div className="text-xs text-slate-400 mt-0.5">{t(`modules.m${i + 1}.age`)}</div>
                  </button>
                );
              })}
            </div>
          )}

          {step === 1 && (
            <div className="mt-6 grid grid-cols-2 sm:grid-cols-3 gap-3">
              {['Python', 'JavaScript', 'HTML & CSS', 'Scratch', 'Java', 'C++'].map((lg) => {
                const selected = language === lg;
                return (
                  <button
                    key={lg}
                    onClick={() => setLanguage(lg)}
                    className={`py-6 rounded-2xl border-2 font-display font-bold text-sm transition ${selected ? 'bg-[#A3E635] text-[#0A0F1E] border-[#A3E635]' : 'bg-[#141824] text-white hover:border-slate-600'}`}
                    style={selected ? {} : { borderColor: 'var(--cf-border)' }}
                  >
                    {lg}
                  </button>
                );
              })}
            </div>
          )}

          {step === 2 && (
            <div className="mt-6 space-y-3">
              {[
                { id: 'beginner', key: 'beginner', emoji: '🌱' },
                { id: 'intermediate', key: 'intermediate', emoji: '🚀' },
                { id: 'advanced', key: 'advanced', emoji: '🏆' },
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
                    <span className="flex-1 text-left font-display font-bold text-white">{t(`onboard.level.${l.key}`)}</span>
                    {selected && <Check size={20} className="text-[#A3E635]" />}
                  </button>
                );
              })}
            </div>
          )}

          <div className="mt-8 flex items-center justify-between">
            <Button
              variant="ghost"
              onClick={back}
              disabled={step === 0}
              className="text-slate-300 hover:text-white hover:bg-[#1C2235] disabled:opacity-40"
            >
              <ArrowLeft size={16} className="mr-1" /> {t('onboard.back')}
            </Button>
            <Button onClick={next} className="cf-btn-lime h-11 px-6 rounded-full">
              {step === steps.length - 1 ? t('onboard.finish') : t('onboard.next')}
              <ArrowRight size={16} className="ml-1" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
