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
      pt: 'Use a função `print()` para exibir a mensagem `Olá, Mundo!` na tela. A saída deve ser exatamente: `Olá, Mundo!` — com acento, vírgula e ponto de exclamação.\n\nExemplo de saída esperada:\n```\nOlá, Mundo!\n```',
      en: 'Use `print()` to show the message `Hello, World!`.',
      es: 'Usa `print()` para mostrar `¡Hola, Mundo!`.',
    },
    starter: "# Escreva seu código aqui\n",
    hint: "A função `print()` exibe texto na tela. Coloque o texto que quer mostrar entre parênteses e aspas.",
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
      pt: 'Crie uma variável chamada `nome` com o valor `"Ana"` e outra chamada `idade` com o valor `12`. Depois imprima na tela a frase exata: `Ana tem 12 anos`.\n\nExemplo de saída esperada:\n```\nAna tem 12 anos\n```',
      en: 'Create `nome = "Ana"` and `idade = 12` then print `Ana tem 12 anos`.',
      es: 'Crea `nome = "Ana"` y `idade = 12` y muestra `Ana tem 12 anos`.',
    },
    starter: 'nome = "Ana"\nidade = 12\n\n# Imprima a frase completa aqui\n',
    hint: "Para combinar texto e variáveis em uma frase, experimente usar f-string — coloque `f` antes das aspas e use `{}` para inserir o valor de cada variável.",
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
      pt: 'Em Python, cada valor tem um tipo. A função `type()` revela qual é esse tipo. Complete o código abaixo para imprimir o tipo de três valores diferentes:\n- O número inteiro `42`\n- O número decimal `3.14`\n- O texto `"Python"`\n\nExemplo de saída esperada (3 linhas):\n```\n<class \'int\'>\n<class \'float\'>\n<class \'str\'>\n```',
      en: 'Print the type of 42, 3.14 and "Python" using type().',
      es: 'Imprime el tipo de 42, 3.14 y "Python" usando type().',
    },
    starter: "# Complete: imprima o tipo de cada valor\nprint(type(___))\nprint(type(___))\nprint(type(___))\n",
    hint: "A função `type()` recebe um valor como argumento e retorna o tipo dele. Por exemplo, `type(True)` retorna `<class 'bool'>`.",
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
      pt: 'Calcule e imprima, cada resultado em uma linha separada:\n- A soma de `15 + 7`\n- A multiplicação de `8 * 6`\n- O resto da divisão de `17 % 5` (o operador `%` retorna o que sobra após a divisão inteira)\n\nExemplo de saída esperada:\n```\n22\n48\n2\n```',
      en: 'Print 15+7, 8*6 and 17%5 each on a new line.',
      es: 'Imprime 15+7, 8*6 y 17%5 cada uno en una línea.',
    },
    starter: "# Linha 1: soma\n# Linha 2: multiplicação\n# Linha 3: resto da divisão\n",
    hint: "Você pode passar uma expressão matemática diretamente dentro do `print()`. Por exemplo, `print(3 + 2)` imprime `5`.",
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
      pt: 'Às vezes o programa precisa tomar decisões. O `if` executa um bloco de código quando uma condição é verdadeira; o `else` executa quando ela é falsa.\n\nDada a variável `idade = 15`, escreva um `if/else` que imprima:\n- `Adulto` se `idade` for maior ou igual a `18`\n- `Menor` caso contrário\n\nExemplos:\n- `idade = 15` → `Menor`\n- `idade = 20` → `Adulto`',
      en: 'Given idade = 15, print "Adulto" if >=18 else "Menor".',
      es: 'Dado idade = 15, imprime "Adulto" si >=18 o "Menor".',
    },
    starter: "idade = 15\n\n# Escreva o if/else aqui\n",
    hint: "O `if` em Python usa dois-pontos no final da condição e o bloco dentro deve ser indentado (4 espaços). O `else:` fica no mesmo nível do `if`.",
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
      pt: 'Um laço `while` repete um bloco de código enquanto uma condição for verdadeira. Use um laço `while` para imprimir os números de `1` até `5`, cada um em uma linha.\n\nDica de estrutura:\n```\ni = 1\nwhile i <= 5:\n    # seu código aqui\n```\n\nSaída esperada:\n```\n1\n2\n3\n4\n5\n```',
      en: 'Use while to print 1 to 5, each on a new line.',
      es: 'Usa while para imprimir del 1 al 5, uno por línea.',
    },
    starter: "i = 1\nwhile i <= 5:\n    print(i)\n    i += 1\n",
    hint: "Lembre-se de incrementar a variável `i` dentro do laço — sem isso, a condição nunca muda e o programa fica em loop eterno. O operador `+=` soma e já atribui o resultado.",
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
