import React, { useState } from 'react';

/* ─── Keyframes injetados uma vez no <head> ─────────────────────────────────── */
const STYLES = `
@keyframes byte-float {
  0%, 100% { transform: translateY(0px); }
  50%       { transform: translateY(-6px); }
}
@keyframes byte-wiggle {
  0%,100% { transform: rotate(0deg); }
  20%     { transform: rotate(-8deg); }
  40%     { transform: rotate(8deg); }
  60%     { transform: rotate(-5deg); }
  80%     { transform: rotate(5deg); }
}
@keyframes byte-blink {
  0%,90%,100% { transform: scaleY(1); }
  95%         { transform: scaleY(0.1); }
}
@keyframes byte-pulse-eye {
  0%,100% { opacity: 1; }
  50%     { opacity: 0.6; }
}
`;

if (typeof document !== 'undefined' && !document.getElementById('byte-styles')) {
  const el = document.createElement('style');
  el.id = 'byte-styles';
  el.textContent = STYLES;
  document.head.appendChild(el);
}

/* ─── ByteMascot — robô completo ────────────────────────────────────────────── */
export default function ByteMascot({ size = 120, className = '', onClick }) {
  const [hovered, setHovered] = useState(false);

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 200 200"
      className={className}
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-label="Byte, mascote CodeFuturo"
      onClick={onClick}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        cursor: onClick ? 'pointer' : 'default',
        animation: hovered
          ? 'byte-wiggle 0.6s ease-in-out'
          : 'byte-float 3s ease-in-out infinite',
        display: 'block',
      }}
    >
      {/* antena */}
      <line x1="100" y1="20" x2="100" y2="40" stroke="#A3E635" strokeWidth="4" strokeLinecap="round" />
      <circle cx="100" cy="18" r="6" fill="#A3E635">
        <animate attributeName="r" values="6;8;6" dur="2s" repeatCount="indefinite" />
      </circle>

      {/* corpo */}
      <rect x="50" y="40" width="100" height="90" rx="22" fill="#1C2235" stroke="#A3E635" strokeWidth="3" />

      {/* tela */}
      <rect x="62" y="55" width="76" height="56" rx="12" fill="#0A0F1E" />

      {/* olhos — piscam */}
      <g style={{ animation: 'byte-blink 4s ease-in-out infinite' }}>
        <circle cx="84" cy="82" r="7" fill="#A3E635" />
        <circle cx="116" cy="82" r="7" fill="#A3E635" />
      </g>
      {/* brilho nos olhos */}
      <circle cx="87" cy="79" r="2" fill="white" opacity="0.7" />
      <circle cx="119" cy="79" r="2" fill="white" opacity="0.7" />

      {/* sorriso — vira surpresa no hover */}
      {hovered ? (
        <circle cx="100" cy="103" r="7" fill="#A3E635" />
      ) : (
        <path d="M 82 100 Q 100 112 118 100" stroke="#A3E635" strokeWidth="3" strokeLinecap="round" fill="none" />
      )}

      {/* braços */}
      <rect x="42" y="70" width="10" height="24" rx="3" fill="#1C2235" stroke="#A3E635" strokeWidth="2" />
      <rect x="148" y="70" width="10" height="24" rx="3" fill="#1C2235" stroke="#A3E635" strokeWidth="2" />

      {/* pescoço */}
      <rect x="92" y="130" width="16" height="10" fill="#1C2235" stroke="#A3E635" strokeWidth="2" />

      {/* base */}
      <rect x="58" y="140" width="84" height="44" rx="14" fill="#141824" stroke="#A3E635" strokeWidth="3" />

      {/* botões coloridos — pulsam */}
      <circle cx="78" cy="162" r="4" fill="#34D399">
        <animate attributeName="opacity" values="1;0.5;1" dur="1.5s" begin="0s" repeatCount="indefinite" />
      </circle>
      <circle cx="100" cy="162" r="4" fill="#3B82F6">
        <animate attributeName="opacity" values="1;0.5;1" dur="1.5s" begin="0.5s" repeatCount="indefinite" />
      </circle>
      <circle cx="122" cy="162" r="4" fill="#F97316">
        <animate attributeName="opacity" values="1;0.5;1" dur="1.5s" begin="1s" repeatCount="indefinite" />
      </circle>
    </svg>
  );
}

/* ─── ByteLogo — hexágono compacto (mantido para compatibilidade) ────────────── */
export function ByteLogo({ size = 36, className = '' }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 64 64"
      className={className}
      xmlns="http://www.w3.org/2000/svg"
      aria-label="CodeFuturo"
    >
      <defs>
        <linearGradient id="cfhex" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#A3E635" />
          <stop offset="100%" stopColor="#84CC16" />
        </linearGradient>
      </defs>
      <polygon points="32,4 58,18 58,46 32,60 6,46 6,18" fill="url(#cfhex)" />
      <text x="50%" y="58%" textAnchor="middle" dominantBaseline="middle" fill="#0A0F1E" fontFamily="Space Grotesk, sans-serif" fontWeight="800" fontSize="22">{`</>`}</text>
    </svg>
  );
}

/* ─── ByteNavbar — versão compacta animada para o Navbar ────────────────────── */
export function ByteNavbar({ size = 38, onClick }) {
  const [hovered, setHovered] = useState(false);

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 200 200"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-label="Byte"
      onClick={onClick}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        cursor: 'pointer',
        animation: hovered
          ? 'byte-wiggle 0.5s ease-in-out'
          : 'byte-float 3s ease-in-out infinite',
        display: 'block',
        flexShrink: 0,
      }}
    >
      {/* antena */}
      <line x1="100" y1="20" x2="100" y2="40" stroke="#A3E635" strokeWidth="5" strokeLinecap="round" />
      <circle cx="100" cy="18" r="7" fill="#A3E635">
        <animate attributeName="r" values="7;9;7" dur="2s" repeatCount="indefinite" />
      </circle>

      {/* corpo */}
      <rect x="50" y="40" width="100" height="90" rx="22" fill="#1C2235" stroke="#A3E635" strokeWidth="4" />
      <rect x="62" y="55" width="76" height="56" rx="12" fill="#0A0F1E" />

      {/* olhos */}
      <g style={{ animation: 'byte-blink 4s ease-in-out infinite' }}>
        <circle cx="84" cy="82" r="8" fill="#A3E635" />
        <circle cx="116" cy="82" r="8" fill="#A3E635" />
      </g>
      <circle cx="87" cy="79" r="2.5" fill="white" opacity="0.8" />
      <circle cx="119" cy="79" r="2.5" fill="white" opacity="0.8" />

      {/* sorriso / surpresa */}
      {hovered ? (
        <circle cx="100" cy="103" r="7" fill="#A3E635" />
      ) : (
        <path d="M 82 100 Q 100 112 118 100" stroke="#A3E635" strokeWidth="3.5" strokeLinecap="round" fill="none" />
      )}

      {/* braços */}
      <rect x="40" y="68" width="12" height="26" rx="4" fill="#1C2235" stroke="#A3E635" strokeWidth="3" />
      <rect x="148" y="68" width="12" height="26" rx="4" fill="#1C2235" stroke="#A3E635" strokeWidth="3" />

      {/* pescoço + base */}
      <rect x="92" y="130" width="16" height="10" fill="#1C2235" stroke="#A3E635" strokeWidth="2" />
      <rect x="58" y="140" width="84" height="44" rx="14" fill="#141824" stroke="#A3E635" strokeWidth="3" />

      {/* botões */}
      <circle cx="78" cy="162" r="5" fill="#34D399">
        <animate attributeName="opacity" values="1;0.4;1" dur="1.5s" begin="0s" repeatCount="indefinite" />
      </circle>
      <circle cx="100" cy="162" r="5" fill="#3B82F6">
        <animate attributeName="opacity" values="1;0.4;1" dur="1.5s" begin="0.5s" repeatCount="indefinite" />
      </circle>
      <circle cx="122" cy="162" r="5" fill="#F97316">
        <animate attributeName="opacity" values="1;0.4;1" dur="1.5s" begin="1s" repeatCount="indefinite" />
      </circle>
    </svg>
  );
}
