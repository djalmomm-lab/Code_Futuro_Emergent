import React from 'react';

// Byte - CodeFuturo mascot. Friendly robot.
export default function ByteMascot({ size = 120, className = '' }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 200 200"
      className={className}
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-label="Byte, mascote CodeFuturo"
    >
      <line x1="100" y1="20" x2="100" y2="40" stroke="#A3E635" strokeWidth="4" strokeLinecap="round" />
      <circle cx="100" cy="18" r="6" fill="#A3E635" />
      <rect x="50" y="40" width="100" height="90" rx="22" fill="#1C2235" stroke="#A3E635" strokeWidth="3" />
      <rect x="62" y="55" width="76" height="56" rx="12" fill="#0A0F1E" />
      <circle cx="84" cy="82" r="7" fill="#A3E635" />
      <circle cx="116" cy="82" r="7" fill="#A3E635" />
      <path d="M 82 100 Q 100 110 118 100" stroke="#A3E635" strokeWidth="3" strokeLinecap="round" fill="none" />
      <rect x="42" y="70" width="10" height="24" rx="3" fill="#1C2235" stroke="#A3E635" strokeWidth="2" />
      <rect x="148" y="70" width="10" height="24" rx="3" fill="#1C2235" stroke="#A3E635" strokeWidth="2" />
      <rect x="92" y="130" width="16" height="10" fill="#1C2235" stroke="#A3E635" strokeWidth="2" />
      <rect x="58" y="140" width="84" height="44" rx="14" fill="#141824" stroke="#A3E635" strokeWidth="3" />
      <circle cx="78" cy="162" r="4" fill="#34D399" />
      <circle cx="100" cy="162" r="4" fill="#3B82F6" />
      <circle cx="122" cy="162" r="4" fill="#F97316" />
    </svg>
  );
}

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
