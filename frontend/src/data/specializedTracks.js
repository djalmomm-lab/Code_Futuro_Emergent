// Specialized tracks - no age restriction, for adults or advanced learners
import { Database, Smartphone, Gamepad2, Shield, Brain, Cloud, Globe, LineChart } from 'lucide-react';

export const SPECIALIZED_TRACKS = [
  { id: 'webfs', name: 'Web Full Stack', desc: 'React, Node.js, APIs REST, banco de dados', icon: Globe, color: '#A3E635', lessons: 86, hours: 60, level: 'Intermediário' },
  { id: 'datasci', name: 'Ciência de Dados', desc: 'Python, Pandas, NumPy, visualizações e estatística', icon: LineChart, color: '#3B82F6', lessons: 72, hours: 50, level: 'Intermediário' },
  { id: 'ml', name: 'Machine Learning', desc: 'Scikit-learn, TensorFlow, redes neurais e IA aplicada', icon: Brain, color: '#7C3AED', lessons: 64, hours: 55, level: 'Avançado' },
  { id: 'mobile', name: 'Mobile Dev', desc: 'React Native e Flutter para iOS e Android', icon: Smartphone, color: '#F97316', lessons: 58, hours: 45, level: 'Intermediário' },
  { id: 'gamedev', name: 'Desenvolvimento de Jogos', desc: 'Unity, Godot, mecânicas e game design', icon: Gamepad2, color: '#EC4899', lessons: 70, hours: 55, level: 'Intermediário' },
  { id: 'cyber', name: 'Cybersecurity', desc: 'Segurança, criptografia, ethical hacking e defesa', icon: Shield, color: '#EF4444', lessons: 54, hours: 40, level: 'Avançado' },
  { id: 'devops', name: 'DevOps & Cloud', desc: 'Docker, Kubernetes, AWS, CI/CD e infraestrutura', icon: Cloud, color: '#06B6D4', lessons: 62, hours: 48, level: 'Avançado' },
  { id: 'dba', name: 'Banco de Dados', desc: 'SQL avançado, NoSQL, modelagem e performance', icon: Database, color: '#84CC16', lessons: 48, hours: 36, level: 'Intermediário' },
];

// Diagnostic questions - simple age-appropriate scoring
export const DIAGNOSTIC = {
  kids: [
    { q: 'Você já usou um computador sozinho antes?', options: ['Nunca', 'Poucas vezes', 'Sim, bastante'] },
    { q: 'Você sabe o que é uma pasta/arquivo?', options: ['Não sei', 'Mais ou menos', 'Sim, sei usar'] },
    { q: 'Você já brincou com jogos de programação (Scratch, Code.org)?', options: ['Nunca', 'Um pouco', 'Sim, várias vezes'] },
  ],
  teens: [
    { q: 'Você já escreveu algum código?', options: ['Nunca', 'Scratch/blocos', 'Sim, código em texto'] },
    { q: 'Conhece variáveis e tipos de dados?', options: ['Não', 'Já ouvi falar', 'Sim, uso bem'] },
    { q: 'Já criou algum projeto sozinho?', options: ['Não', 'Tutoriais', 'Projetos próprios'] },
    { q: 'Conhece HTML/CSS?', options: ['Nada', 'O básico', 'Sei criar páginas'] },
    { q: 'Conhece lógica (if/else, loops)?', options: ['Não', 'Básico', 'Domino bem'] },
  ],
  adults: [
    { q: 'Qual sua experiência com programação?', options: ['Zero', 'Iniciante (<1 ano)', 'Intermediário (1-3 anos)', 'Avançado (3+ anos)'] },
    { q: 'Já trabalhou profissionalmente com código?', options: ['Não', 'Freelance/projetos', 'Sim, CLT/contratos'] },
    { q: 'Conhece algum framework web?', options: ['Não', 'Só já ouvi falar', 'Já usei em projetos'] },
    { q: 'Conhece estruturas de dados e algoritmos?', options: ['Não', 'Básico', 'Sólido'] },
    { q: 'Qual seu principal objetivo agora?', options: ['Mudar de carreira', 'Primeiro emprego', 'Evoluir na área', 'Projeto pessoal'] },
  ],
};

export const INTERESTS = [
  { id: 'web', label: 'Sites e Web', icon: '🌐' },
  { id: 'games', label: 'Jogos', icon: '🎮' },
  { id: 'mobile', label: 'Apps Mobile', icon: '📱' },
  { id: 'ai', label: 'Inteligência Artificial', icon: '🤖' },
  { id: 'data', label: 'Dados e Análise', icon: '📊' },
  { id: 'security', label: 'Cybersegurança', icon: '🛡️' },
  { id: 'creative', label: 'Projetos Criativos', icon: '🎨' },
  { id: 'career', label: 'Carreira Profissional', icon: '💼' },
];

// Recommend track based on age + diagnostic score + interest
export function recommendTrack({ age, score, interest, hasParentConsent }) {
  // Child (6-12) - forced to age-based module
  if (age < 9) return { type: 'module', id: 'm1', reason: 'Seu perfil combina com o Explorador Digital. Vamos começar pelo básico de informática, mouse, teclado e jogos educativos.' };
  if (age < 12) return { type: 'module', id: 'm2', reason: 'O Criador de Blocos é perfeito pra você! Vamos programar jogos e animações com Scratch.' };
  if (age < 15) {
    if (score >= 6) return { type: 'module', id: 'm3', reason: 'Você já tem base! Vamos direto para Python e Web no Programador Iniciante.' };
    return { type: 'module', id: 'm2', reason: 'Vamos começar pelo Criador de Blocos para fortalecer sua lógica.' };
  }
  if (age < 18) {
    if (score >= 8) return { type: 'module', id: 'm4', reason: 'Pelo seu nível, o módulo Desenvolvedor é ideal. Python avançado, algoritmos e C++.' };
    return { type: 'module', id: 'm3', reason: 'O Programador Iniciante vai te dar a base sólida em Python e Web.' };
  }
  // Adult (18+)
  const interestMap = {
    web: 'webfs', games: 'gamedev', mobile: 'mobile', ai: 'ml', data: 'datasci', security: 'cyber', creative: 'gamedev', career: 'webfs',
  };
  const trackId = interestMap[interest] || 'webfs';
  return { type: 'track', id: trackId, reason: 'Escolhemos sua trilha baseado no seu objetivo e experiência. Você pode explorar outras no catálogo a qualquer momento.' };
}
