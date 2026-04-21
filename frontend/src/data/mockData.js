// Mock data for CodeFuturo landing + app previews

export const LANGUAGES_STACK = [
  { id: 'python', name: 'Python', color: '#3776AB', icon: 'python' },
  { id: 'html', name: 'HTML', color: '#E34F26', icon: 'html' },
  { id: 'javascript', name: 'JavaScript', color: '#F7DF1E', icon: 'js' },
  { id: 'java', name: 'Java', color: '#EA2D2E', icon: 'java' },
  { id: 'cpp', name: 'C++', color: '#00599C', icon: 'cpp' },
  { id: 'sql', name: 'SQL', color: '#CC2927', icon: 'sql' },
  { id: 'c', name: 'C', color: '#A8B9CC', icon: 'c' },
  { id: 'css', name: 'CSS', color: '#1572B6', icon: 'css' },
  { id: 'csharp', name: 'C#', color: '#239120', icon: 'csharp' },
  { id: 'php', name: 'PHP', color: '#777BB4', icon: 'php' },
  { id: 'dart', name: 'Dart', color: '#00C4B3', icon: 'dart' },
  { id: 'go', name: 'Go', color: '#00ADD8', icon: 'go' },
  { id: 'r', name: 'R', color: '#276DC3', icon: 'r' },
  { id: 'rust', name: 'Rust', color: '#CE422B', icon: 'rust' },
  { id: 'lua', name: 'Lua', color: '#000080', icon: 'lua' },
  { id: 'ruby', name: 'Ruby', color: '#CC342D', icon: 'ruby' },
  { id: 'swift', name: 'Swift', color: '#FA7343', icon: 'swift' },
  { id: 'prompts', name: 'AI Prompts', color: '#A3E635', icon: 'ai' },
  { id: 'terminal', name: 'Terminal', color: '#64748B', icon: 'terminal' },
];

export const MODULES = [
  { id: 'm1', slug: 'modulo-1', color: '#34D399', bg: 'rgba(52, 211, 153, 0.12)', lessons: 42, minXp: 0 },
  { id: 'm2', slug: 'modulo-2', color: '#3B82F6', bg: 'rgba(59, 130, 246, 0.12)', lessons: 48, minXp: 210 },
  { id: 'm3', slug: 'modulo-3', color: '#7C3AED', bg: 'rgba(124, 58, 237, 0.12)', lessons: 60, minXp: 410 },
  { id: 'm4', slug: 'modulo-4', color: '#F97316', bg: 'rgba(249, 115, 22, 0.12)', lessons: 72, minXp: 610 },
];

export const TOTAL_CODERS = 3761162;

export const LEADERBOARD = [
  { rank: 1, name: 'Alex', xp: 2840, streak: '7+', avatar: 'https://i.pravatar.cc/120?img=12' },
  { rank: 2, name: 'Jordan', xp: 2650, streak: '7+', avatar: 'https://i.pravatar.cc/120?img=32' },
  { rank: 3, name: 'Sam', xp: 2420, streak: '7+', avatar: 'https://i.pravatar.cc/120?img=45' },
  { rank: 4, name: 'Casey', xp: 2180, streak: '4', avatar: 'https://i.pravatar.cc/120?img=28' },
  { rank: 5, name: 'Morgan', xp: 1950, streak: '7+', avatar: 'https://i.pravatar.cc/120?img=8' },
  { rank: 6, name: 'Riley', xp: 1720, streak: '3', avatar: 'https://i.pravatar.cc/120?img=14' },
  { rank: 7, name: 'Taylor', xp: 1520, streak: '2', avatar: 'https://i.pravatar.cc/120?img=22' },
];

export const PATHS_MOCK = [
  { id: 'python-zero', name: 'Python do Zero', module: 'm3', lessons: 30, completed: 8, color: '#7C3AED' },
  { id: 'html-css', name: 'HTML & CSS', module: 'm3', lessons: 30, completed: 12, color: '#3B82F6' },
  { id: 'scratch-games', name: 'Jogos com Scratch', module: 'm2', lessons: 24, completed: 3, color: '#3B82F6' },
  { id: 'algoritmos', name: 'Algoritmos Essenciais', module: 'm4', lessons: 36, completed: 0, color: '#F97316' },
];

export const JOURNEY_NODES = [
  { id: 1, status: 'done', title: 'Olá, Mundo!' },
  { id: 2, status: 'done', title: 'Variáveis' },
  { id: 3, status: 'active', title: 'Tipos de Dados' },
  { id: 4, status: 'locked', title: 'Entrada e Saída' },
  { id: 5, status: 'locked', title: 'Operadores' },
];

export const USER_MOCK = {
  name: 'João',
  streak: 7,
  xpToday: 120,
  dailyGoal: 200,
  energy: 5,
  maxEnergy: 5,
  level: 4,
  xpTotal: 840,
  tokens: 10,
};

export const DEFAULT_LESSON = {
  slug: 'ola-mundo',
  title: 'Olá, Mundo!',
  path: 'Python do Zero',
  chapter: 'Capítulo 1: Fundamentos',
  instruction: {
    pt: 'Use a função `print()` para exibir a mensagem `Olá, Mundo!` na tela.',
    en: 'Use the `print()` function to display the message `Hello, World!` on screen.',
    es: 'Usa la función `print()` para mostrar el mensaje `¡Hola, Mundo!` en pantalla.',
  },
  starter: "# Escreva seu código aqui\nprint('...')\n",
  expected: 'Olá, Mundo!',
  tests: [
    { id: 1, input: '', expected: 'Olá, Mundo!', passed: false },
    { id: 2, input: '', expected: 'Olá, Mundo!', passed: false },
    { id: 3, input: '', expected: 'Olá, Mundo!', passed: false },
  ],
};
