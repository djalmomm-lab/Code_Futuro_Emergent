import React, { useState } from 'react';
import { Play, Sparkles, CheckCircle2, XCircle, ChevronDown } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

const CODE_SAMPLE = [
  { n: 1, kw: 'const', rest: ' greeting = "Hello, CodeFuturo!"' },
  { n: 2, kw: 'function', rest: ' sayHi(name) {' },
  { n: 3, kw: '', rest: '  return greeting + " " + name', purple: 'return' },
  { n: 4, kw: '', rest: '}' },
  { n: 5, kw: '', rest: '' },
];

export default function LearnByDoingSection() {
  const { t } = useLanguage();
  const [tab, setTab] = useState('code');
  const [bottomTab, setBottomTab] = useState('tests');

  const tabs = [
    { id: 'code', label: t('learn.tabs.code') },
    { id: 'web', label: t('learn.tabs.web') },
    { id: 'ai', label: t('learn.tabs.ai') },
    { id: 'terminal', label: t('learn.tabs.terminal') },
  ];

  return (
    <section className="relative py-20 md:py-28">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-14 items-center">
          <div>
            <h2 className="font-display text-4xl md:text-5xl font-bold text-white leading-tight">{t('learn.title')}</h2>
            <p className="mt-5 text-slate-300 text-lg max-w-lg">{t('learn.subtitle')}</p>

            <div className="mt-6 flex flex-wrap gap-2">
              {tabs.map((t2) => (
                <button
                  key={t2.id}
                  onClick={() => setTab(t2.id)}
                  className={`px-4 py-2 rounded-full text-sm font-bold transition ${
                    tab === t2.id ? 'bg-[#A3E635] text-[#0A0F1E]' : 'bg-[#141824] text-slate-300 border hover:text-white'
                  }`}
                  style={tab === t2.id ? {} : { borderColor: 'var(--cf-border)' }}
                >
                  {t2.label}
                </button>
              ))}
            </div>
          </div>

          <div className="cf-card overflow-hidden">
            <div className="flex items-center justify-between px-4 py-2.5 border-b" style={{ borderColor: 'var(--cf-border)' }}>
              <div className="flex items-center gap-1.5">
                <span className="w-3 h-3 rounded-full bg-red-500/70" />
                <span className="w-3 h-3 rounded-full bg-yellow-500/70" />
                <span className="w-3 h-3 rounded-full bg-green-500/70" />
                <span className="ml-3 text-xs text-slate-400 font-code">playground.js</span>
              </div>
              <span className="text-xs text-slate-500 hidden sm:inline">Code Editor</span>
            </div>

            <div className="p-4 font-code text-sm bg-[#0A0F1E]">
              {CODE_SAMPLE.map((line) => (
                <div key={line.n} className="flex gap-4 leading-7">
                  <span className="text-slate-600 select-none w-6 text-right">{line.n}</span>
                  <span>
                    {line.kw && <span className="text-[#A3E635]">{line.kw}</span>}
                    {line.purple && <span className="text-purple-400">{line.purple}</span>}
                    <span className="text-slate-200">{line.purple ? line.rest.replace(line.purple, '') : line.rest}</span>
                  </span>
                </div>
              ))}
            </div>

            <div className="flex items-center gap-2 px-4 py-3 border-t border-b" style={{ borderColor: 'var(--cf-border)' }}>
              <button className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#1C2235] text-slate-200 text-xs font-bold hover:bg-[#242b44] transition">
                <Sparkles size={14} className="text-[#A3E635]" /> {t('learn.askAi')}
              </button>
              <button className="ml-auto inline-flex items-center gap-1.5 px-4 py-1.5 rounded-lg cf-btn-lime text-xs">
                <Play size={14} /> {t('learn.runCode')}
              </button>
            </div>

            <div className="flex items-center border-b text-xs font-bold" style={{ borderColor: 'var(--cf-border)' }}>
              <button onClick={() => setBottomTab('tests')} className={`px-4 py-2.5 ${bottomTab === 'tests' ? 'text-[#A3E635] border-b-2 border-[#A3E635]' : 'text-slate-400'}`}>
                {t('learn.testCases')}
              </button>
              <button onClick={() => setBottomTab('console')} className={`px-4 py-2.5 ${bottomTab === 'console' ? 'text-[#A3E635] border-b-2 border-[#A3E635]' : 'text-slate-400'}`}>
                {t('learn.console')}
              </button>
              <button className="ml-auto p-2 text-slate-500"><ChevronDown size={14} /></button>
            </div>

            <div className="p-4 space-y-2 min-h-[140px] bg-[#0A0F1E]">
              {bottomTab === 'tests' ? (
                <>
                  {[1, 2, 3].map((i) => (
                    <div key={i} className="flex items-center gap-3 text-sm">
                      {i === 3 ? <XCircle size={16} className="text-red-400" /> : <CheckCircle2 size={16} className="text-[#A3E635]" />}
                      <span className="text-slate-200 font-semibold">{t('learn.test')} #{i}</span>
                    </div>
                  ))}
                </>
              ) : (
                <div className="font-code text-xs text-slate-300">
                  <div className="text-slate-500">{`> running playground.js`}</div>
                  <div className="text-[#A3E635]">Hello, CodeFuturo! Alex</div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
