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
    next: 'python-zero-comparadores',
    instruction: {
      pt: 'Às vezes o programa precisa tomar decisões. O `if` executa um bloco de código quando uma condição é verdadeira; o `else` executa quando ela é falsa.\n\nSeu programa deve:\n1. Ler a idade pelo `input()`\n2. Imprimir `Adulto` se a idade for maior ou igual a `18`\n3. Imprimir `Menor de idade` caso contrário\n\nExemplos:\n- Entrada: `20` → Saída: `Adulto`\n- Entrada: `15` → Saída: `Menor de idade`',
      en: 'Read age with input(), print "Adulto" if >=18 else "Menor de idade".',
      es: 'Lee la edad con input(), imprime "Adulto" si >=18 o "Menor de idade".',
    },
    starter: "idade = int(input(\"Digite sua idade: \"))\n\nif ___:\n    print(___)\nelse:\n    print(___)\n",
    hint: "O `if` em Python usa dois-pontos no final da condição e o bloco dentro deve ser indentado (4 espaços). O `else:` fica no mesmo nível do `if`. Lembre de converter o valor do `input()` para inteiro com `int()`.",
    tests: [
      { id: 1, stdin: '20', expected: 'Adulto' },
      { id: 2, stdin: '15', expected: 'Menor de idade' },
    ],
  },

  'python-zero-comparadores': {
    slug: 'python-zero-comparadores',
    title: 'Comparadores',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 2: Controle de Fluxo',
    order: 6,
    next: 'python-zero-elif',
    instruction: {
      pt: 'Comparadores são operadores que comparam dois valores e retornam `True` (verdadeiro) ou `False` (falso). São muito usados em condições `if`!\n\nOs principais comparadores são:\n- `==` → igual a\n- `!=` → diferente de\n- `>` → maior que\n- `<` → menor que\n- `>=` → maior ou igual a\n- `<=` → menor ou igual a\n\nExemplo:\n```python\na = 10\nb = 5\nprint(a > b)   # True, pois 10 é maior que 5\nprint(a == b)  # False, pois 10 não é igual a 5\n```\n\nAgora é a sua vez! Com `a = 10` e `b = 5`, complete o código para imprimir:\n1. `True` — usando o comparador "maior que"\n2. `False` — usando o comparador "igual a"\n3. `True` — usando o comparador "diferente de"\n\nSaída esperada:\n```\nTrue\nFalse\nTrue\n```',
      en: 'Use comparison operators ==, > and != with a=10 and b=5 to print True, False, True.',
      es: 'Usa los operadores ==, > y != con a=10 y b=5 para imprimir True, False, True.',
    },
    starter: 'a = 10\nb = 5\n\nprint(a ___ b)   # deve imprimir True\nprint(a ___ b)   # deve imprimir False\nprint(a ___ b)   # deve imprimir True\n',
    hint: "Pensa no significado de cada operador: `>` compara se o lado esquerdo é maior, `==` verifica se os dois lados são iguais, e `!=` verifica se eles são diferentes. Substitua cada `___` pelo operador correto.",
    tests: [
      { id: 1, stdin: '', expected: 'True\nFalse\nTrue' },
    ],
  },

  'python-zero-elif': {
    slug: 'python-zero-elif',
    title: 'Múltiplas condições com elif',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 2: Controle de Fluxo',
    order: 7,
    next: 'python-zero-for',
    instruction: {
      pt: 'Às vezes temos mais de duas possibilidades e o `if`/`else` não é suficiente. É aí que entra o `elif` (abreviação de "else if") — ele permite verificar várias condições em sequência!\n\nVamos criar um sistema de notas escolares. Dado uma nota, o programa deve imprimir:\n- `"Aprovado"` se a nota for maior ou igual a `7`\n- `"Recuperação"` se a nota for maior ou igual a `5` e menor que `7`\n- `"Reprovado"` se a nota for menor que `5`\n\nExemplos:\n- Entrada: `8` → Saída: `Aprovado`\n- Entrada: `6` → Saída: `Recuperação`\n- Entrada: `3` → Saída: `Reprovado`\n\nBoa sorte — você consegue! 🎯',
      en: 'Use if/elif/else to print Aprovado (>=7), Recuperação (>=5) or Reprovado (<5) based on user input.',
      es: 'Usa if/elif/else para imprimir Aprovado (>=7), Recuperação (>=5) o Reprovado (<5) según la nota.',
    },
    starter: 'nota = float(input("Digite a nota: "))\n\nif ___:\n    print("Aprovado")\nelif ___:\n    print("Recuperação")\nelse:\n    print(___)\n',
    hint: "Dica 1: Use `float()` em vez de `int()` para aceitar notas com decimais, como `6.5`. Assim o programa fica mais completo!\n\nDica 2: A ordem das condições importa! Verifique primeiro se a nota é >= 7 (Aprovado), depois se é >= 5 (Recuperação). Se colocar a ordem errada, o resultado pode sair diferente do esperado.",
    tests: [
      { id: 1, stdin: '8', expected: 'Aprovado' },
      { id: 2, stdin: '6', expected: 'Recuperação' },
      { id: 3, stdin: '3', expected: 'Reprovado' },
    ],
  },

  'python-zero-for': {
    slug: 'python-zero-for',
    title: 'Repetindo com for',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 2: Controle de Fluxo',
    order: 8,
    next: 'python-zero-listas',
    instruction: {
      pt: 'O `for` com `range()` repete um bloco de código um número fixo de vezes — muito útil quando você sabe quantas repetições quer fazer!\n\nVamos usar isso para imprimir a tabuada do 5 de 1 a 5. Complete o loop para que a saída seja:\n```\n5 x 1 = 5\n5 x 2 = 10\n5 x 3 = 15\n5 x 4 = 20\n5 x 5 = 25\n```\n\nDica de estrutura:\n```python\nfor i in range(inicio, fim):\n    print(f"5 x {i} = {resultado}")\n```\n\nVocê já sabe fazer isso, vai lá! 💪',
      en: 'Complete the for loop with range() to print the 5 times table from 1 to 5.',
      es: 'Completa el bucle for con range() para imprimir la tabla del 5 del 1 al 5.',
    },
    starter: 'for i in range(___, ___):\n    print(f"5 x {i} = {___}")\n',
    hint: "Dica 1: `range(inicio, fim)` gera números começando em `inicio` e terminando em `fim - 1`. Para ir de 1 a 5, use `range(1, 6)`.\n\nDica 2: Dentro da f-string, você pode fazer contas! Para calcular o resultado da tabuada, multiplique `5` por `i` dentro das chaves: `{5 * i}`.",
    tests: [
      { id: 1, stdin: '', expected: '5 x 1 = 5\n5 x 2 = 10\n5 x 3 = 15\n5 x 4 = 20\n5 x 5 = 25' },
    ],
  },

  'python-zero-listas': {
    slug: 'python-zero-listas',
    title: 'Listas',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 2: Controle de Fluxo',
    order: 9,
    next: 'while',
    instruction: {
      pt: 'Listas são uma das estruturas mais usadas em Python! Elas guardam vários valores em uma só variável — é como uma prateleira onde você organiza itens em sequência.\n\nVamos criar uma lista de compras com frutas. Seu programa deve:\n1. Criar uma lista com 3 frutas: `"maçã"`, `"banana"` e `"uva"`\n2. Imprimir cada fruta usando um loop `for`\n3. Imprimir o total de itens da lista com `len()`\n\nSaída esperada:\n```\nmaçã\nbanana\nuva\nTotal: 3\n```\n\nSimplesmente demais! 🛒',
      en: 'Create a list with 3 fruits, print each item with a for loop, then print the total using len().',
      es: 'Crea una lista con 3 frutas, imprime cada item con un for y luego imprime el total con len().',
    },
    starter: 'frutas = [___, ___, ___]\n\nfor fruta in frutas:\n    print(___)\n\nprint(f"Total: {___}")\n',
    hint: "Dica 1: Listas em Python usam colchetes `[]` e os itens ficam separados por vírgulas. Textos precisam estar entre aspas: `[\"maçã\", \"banana\", \"uva\"]`.\n\nDica 2: A função `len()` retorna o número de itens de uma lista. Por exemplo, `len([\"a\", \"b\"])` retorna `2`. Use ela dentro da f-string para mostrar o total!",
    tests: [
      { id: 1, stdin: '', expected: 'maçã\nbanana\nuva\nTotal: 3' },
    ],
  },

  'while': {
    slug: 'while',
    title: 'Loop while',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 2: Controle de Fluxo',
    order: 10,
    next: null,
    instruction: {
      pt: 'Um laço `while` repete um bloco de código enquanto uma condição for verdadeira — assim que a condição vira falsa, o laço para.\n\nO código abaixo tem um **erro proposital** na condição do `while`. Seu desafio é encontrar e corrigir esse erro para que o programa imprima os números de `1` a `5`, um por linha.\n\nSaída esperada:\n```\n1\n2\n3\n4\n5\n```',
      en: 'Fix the broken while condition so it prints 1 to 5, each on a new line.',
      es: 'Corrige la condición del while roto para que imprima del 1 al 5, uno por línea.',
    },
    starter: "i = 1\n\n# Este loop tem um erro — corrija a condição para ele imprimir de 1 a 5\nwhile i > 10:  # ← condição errada\n    print(i)\n    i += 1\n",
    hint: "Pensa assim: o loop deve rodar enquanto `i` ainda não passou de 5. Qual sinal de comparação faz isso? Lembre que `>` significa 'maior que' e `<=` significa 'menor ou igual a'.",
    tests: [
      { id: 1, stdin: '', expected: '1\n2\n3\n4\n5' },
    ],
  },
};

// ── JavaScript do Zero ────────────────────────────────────────────────────────

LESSONS['js-ola-mundo'] = {
  slug: 'js-ola-mundo',
  title: 'Olá, Mundo!',
  path: 'JavaScript do Zero',
  pathSlug: 'javascript-zero',
  chapter: 'Capítulo 1: Primeiros Passos',
  order: 1,
  next: 'js-variaveis',
  instruction: {
    pt: 'Bem-vindo ao JavaScript! 🎉 A primeira coisa que todo programador aprende é como exibir uma mensagem na tela.\n\nEm JavaScript, usamos `console.log()` para isso. Tudo que você colocar dentro dos parênteses (entre aspas, se for texto) vai aparecer no console.\n\nSua tarefa: use `console.log()` para exibir exatamente a mensagem abaixo:\n\n```\nOlá, Mundo!\n```\n\nExemplo de como funciona:\n- Entrada: (nenhuma)\n- Saída: `Olá, Mundo!`',
    en: 'Use console.log() to display "Olá, Mundo!".',
    es: 'Usa console.log() para mostrar "Olá, Mundo!".',
  },
  starter: '// Escreva seu código aqui\nconsole.log(___)\n',
  hints: [
    '`console.log()` em JavaScript é como o `print()` do Python — exibe texto no console. Coloque o texto entre aspas dentro dos parênteses.',
    'Substitua `___` pelo texto entre aspas: `"Olá, Mundo!"` — não esqueça a vírgula, o espaço e o ponto de exclamação!',
  ],
  tests: [
    { id: 1, stdin: '', expected: 'Olá, Mundo!' },
  ],
};

LESSONS['js-variaveis'] = {
  slug: 'js-variaveis',
  title: 'Variáveis',
  path: 'JavaScript do Zero',
  pathSlug: 'javascript-zero',
  chapter: 'Capítulo 1: Primeiros Passos',
  order: 2,
  next: 'js-tipos',
  instruction: {
    pt: 'Em JavaScript temos duas formas modernas de criar variáveis:\n\n- `let` → para variáveis que podem mudar de valor\n- `const` → para valores que não mudam (constantes)\n\nSua tarefa: complete o código para que a saída seja exatamente:\n```\nOlá, meu nome é Carlos e tenho 15 anos.\n```\n\nExemplo:\n- Entrada: (nenhuma)\n- Saída: `Olá, meu nome é Carlos e tenho 15 anos.`',
    en: 'Use let and const to store a name and age, then print the phrase.',
    es: 'Usa let y const para guardar nombre y edad, luego imprime la frase.',
  },
  starter: 'const nome = ___\nlet idade = ___\n\n// Complete o console.log com os valores corretos\nconsole.log(`Olá, meu nome é ${nome} e tenho ${idade} anos.`)\n',
  hints: [
    '`const` é usado para valores que não mudam — declare `const nome = "Carlos"`. `let` é para valores que podem mudar — declare `let idade = 15`.',
    'As variáveis já aparecem no template literal `${nome}` e `${idade}` — você só precisa atribuir os valores corretos: `"Carlos"` e `15`.',
  ],
  tests: [
    { id: 1, stdin: '', expected: 'Olá, meu nome é Carlos e tenho 15 anos.' },
  ],
};

LESSONS['js-tipos'] = {
  slug: 'js-tipos',
  title: 'Tipos de Dados',
  path: 'JavaScript do Zero',
  pathSlug: 'javascript-zero',
  chapter: 'Capítulo 1: Primeiros Passos',
  order: 3,
  next: 'js-operadores',
  instruction: {
    pt: 'Em JavaScript, cada valor tem um tipo. Os mais comuns são:\n\n- `string` → texto entre aspas: `"Ana"`\n- `number` → número: `42` ou `3.14`\n- `boolean` → verdadeiro ou falso: `true` / `false`\n\nO operador `typeof` revela o tipo de um valor.\n\nSua tarefa: complete o código para que a saída seja:\n```\nstring\nnumber\nboolean\n```\n\nExemplo:\n- `typeof "texto"` retorna `string`\n- `typeof 99` retorna `number`',
    en: 'Use typeof to print the type of a string, number, and boolean.',
    es: 'Usa typeof para imprimir el tipo de un string, number y boolean.',
  },
  starter: '// Complete: imprima o tipo de cada valor usando typeof\nconsole.log(typeof ___)\nconsole.log(typeof ___)\nconsole.log(typeof ___)\n',
  hints: [
    '`typeof` é um operador que retorna o tipo como string. Por exemplo: `typeof true` retorna `"boolean"`. Experimente colocar um texto entre aspas no primeiro `___`.',
    'Para obter `string`, passe qualquer texto com aspas. Para `number`, passe um número. Para `boolean`, passe `true` ou `false`.',
  ],
  tests: [
    { id: 1, stdin: '', expected: 'string\nnumber\nboolean' },
  ],
};

LESSONS['js-operadores'] = {
  slug: 'js-operadores',
  title: 'Operadores',
  path: 'JavaScript do Zero',
  pathSlug: 'javascript-zero',
  chapter: 'Capítulo 1: Primeiros Passos',
  order: 4,
  next: 'js-template-literals',
  instruction: {
    pt: 'Vamos fazer contas com JavaScript! Os operadores matemáticos são:\n\n- `+` → soma\n- `-` → subtração\n- `*` → multiplicação\n- `/` → divisão\n- `%` → resto da divisão (ex: `10 % 3` = `1`)\n\nSua tarefa: calcule e imprima os resultados, cada um em uma linha:\n1. `20 + 8`\n2. `50 - 13`\n3. `7 * 6`\n4. `15 % 4`\n\nSaída esperada:\n```\n28\n37\n42\n3\n```',
    en: 'Calculate and print 20+8, 50-13, 7*6 and 15%4, each on a new line.',
    es: 'Calcula e imprime 20+8, 50-13, 7*6 y 15%4, cada uno en una línea.',
  },
  starter: '// Linha 1: soma de 20 + 8\n// Linha 2: subtração de 50 - 13\n// Linha 3: multiplicação de 7 * 6\n// Linha 4: resto de 15 % 4\n',
  hints: [
    'Você pode passar a expressão matemática diretamente dentro do `console.log()`. Por exemplo: `console.log(3 + 2)` imprime `5`.',
    'O operador `%` retorna o resto da divisão inteira. `15 % 4` é o que sobra quando você divide 15 por 4: 15 = 4×3 + 3, então o resto é `3`.',
  ],
  tests: [
    { id: 1, stdin: '', expected: '28\n37\n42\n3' },
  ],
};

LESSONS['js-template-literals'] = {
  slug: 'js-template-literals',
  title: 'Textos Dinâmicos',
  path: 'JavaScript do Zero',
  pathSlug: 'javascript-zero',
  chapter: 'Capítulo 1: Primeiros Passos',
  order: 5,
  next: 'js-comparadores',
  instruction: {
    pt: 'Template literals são uma forma super prática de montar textos com variáveis em JavaScript!\n\nEm vez de juntar strings com `+`, você usa crases (`` ` ``) e `${}` para inserir variáveis:\n\n```js\nconst cidade = "Recife"\nconsole.log(`Moro em ${cidade}!`) // Moro em Recife!\n```\n\nSua tarefa: complete o código para que a saída seja:\n```\nBife de frango custa R$ 25 e serve 2 pessoas.\n```\n\n- Entrada: (nenhuma)\n- Saída: `Bife de frango custa R$ 25 e serve 2 pessoas.`',
    en: 'Use template literals to build a dynamic string with product info.',
    es: 'Usa template literals para construir un texto dinámico con información del producto.',
  },
  starter: 'const produto = "Bife de frango"\nconst preco = 25\nconst porcoes = 2\n\n// Complete usando template literal com crases e ${}\nconsole.log(___)\n',
  hints: [
    'Template literals usam crases `` ` `` (não aspas comuns). Dentro delas, coloque `${variavel}` para inserir o valor de uma variável.',
    'Monte assim: `` `${produto} custa R$ ${preco} e serve ${porcoes} pessoas.` `` — substitua o `___` por isso dentro do `console.log()`.',
  ],
  tests: [
    { id: 1, stdin: '', expected: 'Bife de frango custa R$ 25 e serve 2 pessoas.' },
  ],
};

LESSONS['js-comparadores'] = {
  slug: 'js-comparadores',
  title: 'Comparadores',
  path: 'JavaScript do Zero',
  pathSlug: 'javascript-zero',
  chapter: 'Capítulo 2: Controle de Fluxo',
  order: 6,
  next: 'js-if-else',
  instruction: {
    pt: 'Comparadores comparam dois valores e retornam `true` (verdadeiro) ou `false` (falso):\n\n- `==` → igual (valor)\n- `!=` → diferente\n- `>` → maior que\n- `<` → menor que\n- `>=` → maior ou igual\n- `<=` → menor ou igual\n\nCom `pontos = 80` e `meta = 100`, complete o código para imprimir:\n```\nfalse\ntrue\ntrue\n```\n\nDica: a ordem é — pontos == meta, pontos < meta, pontos != meta',
    en: 'Use comparison operators to print false, true, true.',
    es: 'Usa operadores de comparación para imprimir false, true, true.',
  },
  starter: 'const pontos = 80\nconst meta = 100\n\nconsole.log(pontos ___ meta)  // deve imprimir false\nconsole.log(pontos ___ meta)  // deve imprimir true\nconsole.log(pontos ___ meta)  // deve imprimir true\n',
  hints: [
    'Para a primeira linha ser `false`: qual operador checa se `pontos` é igual a `meta`? 80 não é igual a 100, então retorna `false`.',
    'Para a segunda linha ser `true`: 80 é menor que 100? Sim! Use `<`. Para a terceira linha ser `true`: 80 é diferente de 100? Sim! Use `!=`.',
  ],
  tests: [
    { id: 1, stdin: '', expected: 'false\ntrue\ntrue' },
  ],
};

LESSONS['js-if-else'] = {
  slug: 'js-if-else',
  title: 'Decisões com if/else',
  path: 'JavaScript do Zero',
  pathSlug: 'javascript-zero',
  chapter: 'Capítulo 2: Controle de Fluxo',
  order: 7,
  next: 'js-for',
  instruction: {
    pt: 'Com `if/else`, seu programa pode tomar decisões!\n\n```js\nif (condição) {\n  // executa se verdadeiro\n} else {\n  // executa se falso\n}\n```\n\nSua tarefa: complete o código para verificar se a nota de Ana é suficiente para passar:\n- Se `nota >= 7`, imprima: `Ana foi aprovada!`\n- Caso contrário, imprima: `Ana ficou de recuperação.`\n\nExemplos:\n- `nota = 8` → `Ana foi aprovada!`\n- `nota = 5` → `Ana ficou de recuperação.`',
    en: 'Complete the if/else to check if nota >= 7 and print the right message.',
    es: 'Completa el if/else para verificar si nota >= 7 e imprimir el mensaje correcto.',
  },
  starter: 'const nota = 8\n\nif (___) {\n  console.log(___)\n} else {\n  console.log(___)\n}\n',
  hints: [
    'A condição do `if` fica entre parênteses. Para checar se `nota` é maior ou igual a 7, use: `nota >= 7`.',
    'Dentro das chaves `{}`, coloque o `console.log()` com a mensagem certa. Atenção aos acentos e pontuações — o texto deve ser exato!',
  ],
  tests: [
    { id: 1, stdin: '', expected: 'Ana foi aprovada!' },
  ],
};

LESSONS['js-for'] = {
  slug: 'js-for',
  title: 'Repetindo com for',
  path: 'JavaScript do Zero',
  pathSlug: 'javascript-zero',
  chapter: 'Capítulo 2: Controle de Fluxo',
  order: 8,
  next: 'js-arrays',
  instruction: {
    pt: 'O loop `for` repete um bloco de código várias vezes. Estrutura básica:\n\n```js\nfor (let i = 1; i <= 5; i++) {\n  console.log(i)\n}\n```\n\n- `let i = 1` → começa em 1\n- `i <= 5` → continua enquanto i for menor ou igual a 5\n- `i++` → incrementa i de 1 em 1\n\nSua tarefa: imprima a tabuada do 3 de 1 a 5:\n```\n3 x 1 = 3\n3 x 2 = 6\n3 x 3 = 9\n3 x 4 = 12\n3 x 5 = 15\n```',
    en: 'Complete the for loop to print the 3 times table from 1 to 5.',
    es: 'Completa el bucle for para imprimir la tabla del 3 del 1 al 5.',
  },
  starter: 'for (let i = ___; i <= ___; i++) {\n  console.log(`3 x ${i} = ${___}`)\n}\n',
  hints: [
    'O loop deve começar em `1` e ir até `5`. Preencha: `let i = 1` e `i <= 5`.',
    'Dentro do template literal, o resultado da tabuada é `3 * i`. Substitua o último `___` por `3 * i`.',
  ],
  tests: [
    { id: 1, stdin: '', expected: '3 x 1 = 3\n3 x 2 = 6\n3 x 3 = 9\n3 x 4 = 12\n3 x 5 = 15' },
  ],
};

LESSONS['js-arrays'] = {
  slug: 'js-arrays',
  title: 'Listas (Arrays)',
  path: 'JavaScript do Zero',
  pathSlug: 'javascript-zero',
  chapter: 'Capítulo 2: Controle de Fluxo',
  order: 9,
  next: 'js-funcoes',
  instruction: {
    pt: 'Arrays (listas) guardam vários valores em uma variável só!\n\n```js\nconst cidades = ["São Paulo", "Rio de Janeiro", "Fortaleza"]\nconsole.log(cidades[0])  // São Paulo\nconsole.log(cidades.length)  // 3\n```\n\nSua tarefa: crie um array com 3 nomes de times brasileiros, percorra a lista com `for` e imprima cada nome, depois o total:\n\n```\nFlamengo\nCorinthians\nPalmeiras\nTotal de times: 3\n```',
    en: 'Create an array with 3 Brazilian teams, print each with a for loop, then print the total.',
    es: 'Crea un array con 3 equipos brasileños, imprime cada uno con for y luego el total.',
  },
  starter: 'const times = [___, ___, ___]\n\nfor (let i = 0; i < times.___; i++) {\n  console.log(times[i])\n}\n\nconsole.log(`Total de times: ${___}`)\n',
  hints: [
    'Arrays em JavaScript usam colchetes `[]` com valores separados por vírgulas. Strings precisam de aspas: `["Flamengo", "Corinthians", "Palmeiras"]`.',
    '`array.length` retorna o número de elementos. Use `times.length` tanto na condição do loop quanto no template literal do total.',
  ],
  tests: [
    { id: 1, stdin: '', expected: 'Flamengo\nCorinthians\nPalmeiras\nTotal de times: 3' },
  ],
};

LESSONS['js-funcoes'] = {
  slug: 'js-funcoes',
  title: 'Funções',
  path: 'JavaScript do Zero',
  pathSlug: 'javascript-zero',
  chapter: 'Capítulo 3: Funções',
  order: 10,
  next: null,
  instruction: {
    pt: 'Funções são blocos de código reutilizáveis. Você define uma vez e chama quantas vezes quiser!\n\n```js\nfunction saudar(nome) {\n  return "Olá, " + nome + "!"\n}\nconsole.log(saudar("Bia"))  // Olá, Bia!\n```\n\nSua tarefa: complete a função `calcularDesconto` que recebe o preço e o percentual de desconto, e retorna o preço final. Depois chame ela e imprima o resultado:\n\n- Preço: `R$ 200`, desconto: `10%` → `Preço final: R$ 180`\n\nSaída esperada:\n```\nPreço final: R$ 180\n```',
    en: 'Complete the calcularDesconto function and print the final price.',
    es: 'Completa la función calcularDesconto e imprime el precio final.',
  },
  starter: 'function calcularDesconto(preco, percentual) {\n  // calcule o valor do desconto e retorne o preço final\n  const desconto = preco * (percentual / ___)\n  return ___\n}\n\nconst resultado = calcularDesconto(200, 10)\nconsole.log(`Preço final: R$ ${resultado}`)\n',
  hints: [
    'Para calcular `10%` de 200, divida o percentual por `100`: `preco * (percentual / 100)`. Preencha o primeiro `___` com `100`.',
    'O preço final é o preço original menos o desconto: `return preco - desconto`. Substitua o segundo `___` por isso.',
  ],
  tests: [
    { id: 1, stdin: '', expected: 'Preço final: R$ 180' },
  ],
};

export const getLesson = (slug) => LESSONS[slug] || LESSONS['ola-mundo'];

export const getLessonList = (pathSlug = 'python-zero') => {
  return Object.values(LESSONS)
    .filter((l) => l.pathSlug === pathSlug)
    .sort((a, b) => a.order - b.order);
};
