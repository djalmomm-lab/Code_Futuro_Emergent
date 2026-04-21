// Real Python lesson library - used by /licao/:slug
// Each lesson has tests that validate output against expected strings.

export const LESSONS = {
  'ola-mundo': {
    slug: 'ola-mundo',
    title: 'Olá, Mundo!',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 1: Fundamentos',
    order: 1,
    next: 'variaveis',
    instruction: {
      pt: 'Use a função `print()` para exibir a mensagem `Olá, Mundo!` na tela. Atenção às aspas e ao ponto de exclamação.',
      en: 'Use `print()` to show the message `Hello, World!`.',
      es: 'Usa `print()` para mostrar `¡Hola, Mundo!`.',
    },
    starter: "# Escreva seu código aqui\n",
    hint: "Use `print('Olá, Mundo!')` com aspas simples ou duplas.",
    tests: [
      { id: 1, stdin: '', expected: 'Olá, Mundo!' },
    ],
  },

  'variaveis': {
    slug: 'variaveis',
    title: 'Variáveis',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 1: Fundamentos',
    order: 2,
    next: 'tipos',
    instruction: {
      pt: 'Crie uma variável `nome` com o valor `"Ana"` e uma variável `idade` com o valor `12`. Depois imprima na tela a frase exata: `Ana tem 12 anos`.',
      en: 'Create `nome = "Ana"` and `idade = 12` then print `Ana tem 12 anos`.',
      es: 'Crea `nome = "Ana"` y `idade = 12` y muestra `Ana tem 12 anos`.',
    },
    starter: "nome = \nidade = \n\n# Imprima a frase completa aqui\n",
    hint: "Use f-string: `print(f'{nome} tem {idade} anos')`",
    tests: [
      { id: 1, stdin: '', expected: 'Ana tem 12 anos' },
    ],
  },

  'tipos': {
    slug: 'tipos',
    title: 'Tipos de Dados',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 1: Fundamentos',
    order: 3,
    next: 'operadores',
    instruction: {
      pt: 'Imprima na tela o tipo das seguintes variáveis usando `type()`:\n- `42` (inteiro)\n- `3.14` (decimal)\n- `"Python"` (texto)\n\nA saída deve ser exatamente 3 linhas, uma para cada tipo.',
      en: 'Print the type of 42, 3.14 and "Python" using type().',
      es: 'Imprime el tipo de 42, 3.14 y "Python" usando type().',
    },
    starter: "print(type(42))\nprint(type(3.14))\nprint(type('Python'))\n",
    hint: "Basta executar o código inicial — ele já está correto!",
    tests: [
      { id: 1, stdin: '', expected: "<class 'int'>\n<class 'float'>\n<class 'str'>" },
    ],
  },

  'operadores': {
    slug: 'operadores',
    title: 'Operadores',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 1: Fundamentos',
    order: 4,
    next: 'if-else',
    instruction: {
      pt: 'Calcule e imprima, cada um em uma linha:\n- A soma de 15 + 7\n- A multiplicação de 8 * 6\n- O resto da divisão 17 % 5',
      en: 'Print 15+7, 8*6 and 17%5 each on a new line.',
      es: 'Imprime 15+7, 8*6 y 17%5 cada uno en una línea.',
    },
    starter: "# Linha 1: soma\n# Linha 2: multiplicação\n# Linha 3: resto da divisão\n",
    hint: "print(15 + 7) na primeira linha, depois print(8 * 6), depois print(17 % 5)",
    tests: [
      { id: 1, stdin: '', expected: '22\n48\n2' },
    ],
  },

  'if-else': {
    slug: 'if-else',
    title: 'if / else',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 2: Controle de Fluxo',
    order: 5,
    next: 'while',
    instruction: {
      pt: 'Dada uma variável `idade = 15`, escreva um código que imprima:\n- `Adulto` se idade for maior ou igual a 18\n- `Menor` caso contrário',
      en: 'Given idade = 15, print "Adulto" if >=18 else "Menor".',
      es: 'Dado idade = 15, imprime "Adulto" si >=18 o "Menor".',
    },
    starter: "idade = 15\n\n# Escreva o if/else aqui\n",
    hint: "Use `if idade >= 18:` e `else:`",
    tests: [
      { id: 1, stdin: '', expected: 'Menor' },
    ],
  },

  'while': {
    slug: 'while',
    title: 'Loop while',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 2: Controle de Fluxo',
    order: 6,
    next: null,
    instruction: {
      pt: 'Use um laço `while` para imprimir os números de 1 até 5, cada um em uma linha.',
      en: 'Use while to print 1 to 5, each on a new line.',
      es: 'Usa while para imprimir del 1 al 5, uno por línea.',
    },
    starter: "i = 1\nwhile i <= 5:\n    # imprima i e incremente\n    pass\n",
    hint: "Dentro do while: `print(i)` e depois `i += 1`",
    tests: [
      { id: 1, stdin: '', expected: '1\n2\n3\n4\n5' },
    ],
  },
};

export const getLesson = (slug) => LESSONS[slug] || LESSONS['ola-mundo'];

export const getLessonList = (pathSlug = 'python-zero') => {
  return Object.values(LESSONS)
    .filter((l) => l.pathSlug === pathSlug)
    .sort((a, b) => a.order - b.order);
};
