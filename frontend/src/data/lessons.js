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

export const getLesson = (slug) => LESSONS[slug] || LESSONS['ola-mundo'];

export const getLessonList = (pathSlug = 'python-zero') => {
  return Object.values(LESSONS)
    .filter((l) => l.pathSlug === pathSlug)
    .sort((a, b) => a.order - b.order);
};
