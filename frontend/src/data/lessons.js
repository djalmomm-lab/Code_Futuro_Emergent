// Real Python lesson library - used by /licao/:slug
// Each lesson has tests that validate output against expected strings.
//
// PADRÃO PARA NOVAS LIÇÕES:
// Toda nova lição DEVE incluir o campo `theory` com conteúdo markdown explicativo
// em pt-BR, informal e encorajador. O campo aparece na fase de introdução antes
// do exercício. Use ##, ```, **negrito**, listas e emojis para enriquecer o conteúdo.
// Inclua: explicação do conceito, 2-3 exemplos de código comentados, e uma seção
// "Por que isso importa?" com contexto do mundo real brasileiro.
// Se theory não estiver presente, o fallback é instruction_pt.

export const LESSONS = {
  'ola-mundo': {
    slug: 'ola-mundo',
    title: 'Olá, Mundo!',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 1: Fundamentos',
    order: 1,
    next: 'variaveis',
    theory: `## O que é print()?

A função \`print()\` é a primeira coisa que todo programador aprende. Ela serve para **exibir texto na tela** — como se o seu programa estivesse falando com você!

\`\`\`python
print("Olá, Mundo!")
# Saída: Olá, Mundo!
\`\`\`

Você pode imprimir qualquer texto colocando-o entre aspas dentro do \`print()\`:

\`\`\`python
print("Meu primeiro programa")
print("Python é incrível!")
\`\`\`

### Por que isso importa?
\`print()\` é usado o tempo todo para mostrar resultados, mensagens de erro, informações para o usuário e muito mais. É a sua janela de comunicação com o mundo! 🌍`,
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
    quiz: [
      { question: 'Qual função usamos para exibir texto na tela em Python?', options: ['input()', 'print()', 'show()', 'display()'], correct: 1 },
      { question: 'O que acontece se você esquecer as aspas em print(Olá)?', options: ['Exibe Olá normalmente', 'Ocorre um erro — Python trata Olá como variável', 'Exibe (Olá)', 'Nada acontece'], correct: 1 },
    ],
  },

  'variaveis': {
    slug: 'variaveis',
    title: 'Variáveis',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 1: Fundamentos',
    order: 2,
    next: 'python-zero-fstrings',
    theory: `## O que são variáveis?

Variáveis são como **caixas com etiquetas** onde você guarda informações para usar depois. Em Python, criar uma variável é simples:

\`\`\`python
nome = "Carlos"
idade = 15
altura = 1.75
\`\`\`

Você pode guardar diferentes tipos de dados:
- **Texto** (string): entre aspas — \`"Carlos"\`
- **Número inteiro**: sem aspas — \`15\`
- **Número decimal**: com ponto — \`1.75\`

### Usando variáveis
Depois de criar, é só usar o nome da variável onde precisar:

\`\`\`python
nome = "Ana"
print(nome)
# Saída: Ana
\`\`\`

### Por que isso importa?
Sem variáveis, você teria que repetir os mesmos valores em todo o código. Com elas, muda em um lugar e funciona em todo lugar! 💡`,
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
    quiz: [
      { question: 'Como atribuir o valor "Ana" à variável nome em Python?', options: ['var nome = "Ana"', 'nome = "Ana"', 'let nome = "Ana"', 'string nome = "Ana"'], correct: 1 },
      { question: 'O que é uma f-string em Python?', options: ['Uma string de formato fixo', 'Uma string que permite inserir variáveis com {}', 'Uma string de arquivo', 'Uma string numérica'], correct: 1 },
    ],
  },

  'python-zero-fstrings': {
    slug: 'python-zero-fstrings',
    title: 'Usando f-strings',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 1: Fundamentos',
    order: 3,
    next: 'python-zero-input-concat',
    theory: `## O que são f-strings?

As **f-strings** são a forma mais prática de inserir variáveis dentro de textos em Python. Basta colocar a letra \`f\` antes das aspas e usar \`{variavel}\` onde o valor deve aparecer.

\`\`\`python
nome = "Ana"
print(f"Olá, {nome}!")
\`\`\`
\`\`\`
Olá, Ana!
\`\`\`

---

## Como funciona, passo a passo

**1. Declare suas variáveis:**
\`\`\`python
nome = "Carlos"
idade = 16
\`\`\`

**2. Use f-string no print():**
\`\`\`python
print(f"Meu nome é {nome} e tenho {idade} anos")
\`\`\`

**3. Resultado:**
\`\`\`
Meu nome é Carlos e tenho 16 anos
\`\`\`

---

## Comparando com a forma antiga

Antes das f-strings, o código ficava assim:

\`\`\`python
# Forma antiga com concatenação:
print("Meu nome é " + nome + " e tenho " + str(idade) + " anos")

# Com f-string (muito mais simples! ✨):
print(f"Meu nome é {nome} e tenho {idade} anos")
\`\`\`

---

## O que você vai praticar

No exercício, as variáveis \`nome\` e \`idade\` já estão declaradas. Você vai completar o \`print()\` usando f-string para exibir:

\`\`\`
Meu nome é Ana e tenho 16 anos
\`\`\``,
    instruction: {
      pt: 'Você já sabe criar variáveis. Agora vamos aprender a usá-las dentro de textos! 🎉\n\nAs **f-strings** permitem colocar variáveis diretamente em uma frase. Basta colocar a letra `f` antes das aspas e usar `{variável}` onde o valor deve aparecer.\n\n**Exemplo:**\n```python\nnome = "Bia"\nprint(f"Olá, {nome}!")\n```\n**Saída:** `Olá, Bia!`\n\n---\n\nAs variáveis `nome` e `idade` já estão declaradas. Complete o `print()` usando f-string para exibir exatamente:\n\n**Meu nome é Ana e tenho 16 anos**',
    },
    starter: 'nome = "Ana"\nidade = 16\n# Use f-string para exibir: "Meu nome é Ana e tenho 16 anos"\nprint(...)\n',
    hints: [
      'Coloque a letra `f` antes das aspas: `print(f"...")`',
      'Use `{nome}` e `{idade}` dentro das aspas para inserir os valores das variáveis',
    ],
    tests: [
      { id: 1, stdin: '', expected: 'Meu nome é Ana e tenho 16 anos' },
    ],
    quiz: [
      { question: 'O que a letra `f` antes das aspas indica em Python?', options: ['Que o texto é falso', 'Que é uma f-string e pode usar {variáveis}', 'Que o texto é um float', 'Que é uma função'], correct: 1 },
      { question: 'Como você insere o valor de uma variável `cidade` dentro de uma f-string?', options: ["`print(f'Eu moro em cidade')`", "`print(f'Eu moro em (cidade)')`", "`print(f'Eu moro em {cidade}')`", "`print('Eu moro em' + f{cidade})`"], correct: 2 },
    ],
  },

  'python-zero-input-concat': {
    slug: 'python-zero-input-concat',
    title: 'Lendo dados do usuário',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 1: Fundamentos',
    order: 4,
    next: 'python-zero-input-fstring',
    theory: `## Como ler dados do usuário?

Todo programa útil precisa conversar com quem está usando. Em Python, usamos a função \`input()\` para isso — ela **pausa o programa e espera o usuário digitar algo**.

\`\`\`python
nome = input()
\`\`\`

Quando o usuário digita \`Carlos\` e pressiona Enter, a variável \`nome\` passa a guardar o valor \`"Carlos"\`.

---

## Exibindo o resultado com concatenação

O operador \`+\` junta dois textos. Isso se chama **concatenação**:

\`\`\`python
nome = input()
print("Olá, " + nome)
\`\`\`

**Se o usuário digitar \`Carlos\`:**
\`\`\`
Olá, Carlos
\`\`\`

**Se o usuário digitar \`Maria\`:**
\`\`\`
Olá, Maria
\`\`\`

---

## Regra importante

Deixe o \`input()\` **sem texto dentro dos parênteses**:

\`\`\`python
nome = input()        # ✅ correto
nome = input("Nome:") # ⚠️ não use neste exercício
\`\`\`

Por quê? Porque os testes automáticos fornecem a entrada diretamente — qualquer texto dentro do \`input()\` apareceria na saída e quebraria o teste.

---

## O que você vai praticar

No exercício, você vai escrever um programa que:
1. Lê um nome com \`input()\`
2. Exibe \`Olá, \` seguido do nome usando \`+\`

**Resultado esperado** (quando o sistema fornecer \`Carlos\`):
\`\`\`
Olá, Carlos
\`\`\``,
    instruction: {
      pt: 'Agora vamos aprender a fazer o programa **conversar com o usuário**! 💬\n\nA função `input()` lê o que o usuário digita e guarda em uma variável. Use-a **sem texto dentro dos parênteses** por enquanto.\n\n**Exemplo:**\n```python\nnome = input()\nprint("Olá, " + nome)\n```\nSe o usuário digitar `Maria`, a saída será: `Olá, Maria`\n\n---\n\nEscreva um programa que:\n1. Leia um nome com `input()`\n2. Exiba `Olá, ` seguido do nome usando o operador `+` (concatenação)\n\n**Exemplo:**\n- Entrada: `Carlos`\n- Saída: `Olá, Carlos`\n\n> 💡 Atenção: deixe o `input()` sem texto dentro dos parênteses!',
    },
    starter: 'nome = input()\nprint( ... )\n',
    hints: [
      'O operador `+` junta dois textos. Ex: `"Olá, " + nome` — atenção ao espaço depois da vírgula!',
      'Não coloque nada dentro do `input()`. Deixe assim: `nome = input()`',
    ],
    tests: [
      { id: 1, stdin: 'Carlos', expected: 'Olá, Carlos' },
    ],
    quiz: [
      { question: 'Para que serve a função `input()` em Python?', options: ['Para imprimir texto na tela', 'Para ler o que o usuário digitou', 'Para criar variáveis automaticamente', 'Para calcular valores'], correct: 1 },
      { question: "Se `nome = 'Ana'`, o que `'Olá, ' + nome` produz?", options: ['`Olá,Ana`', '`Olá, Ana`', '`Olá, + Ana`', 'Erro de sintaxe'], correct: 1 },
    ],
  },

  'python-zero-input-fstring': {
    slug: 'python-zero-input-fstring',
    title: 'Entrada e formatação com f-string',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 1: Fundamentos',
    order: 5,
    next: 'tipos',
    theory: `## Unindo input() e f-string

Você já sabe usar \`input()\` para ler dados e f-strings para formatar texto. Agora vamos combinar as duas coisas — essa é a forma mais elegante de criar programas interativos!

\`\`\`python
nome = input()
print(f"Bem-vindo, {nome}!")
\`\`\`

**Se o usuário digitar \`Carlos\`:**
\`\`\`
Bem-vindo, Carlos!
\`\`\`

---

## Por que f-string é melhor que concatenação?

Compare as duas formas:

\`\`\`python
# Com concatenação (funciona, mas é trabalhoso):
print("Bem-vindo, " + nome + "!")

# Com f-string (mais limpo e moderno ✨):
print(f"Bem-vindo, {nome}!")
\`\`\`

A f-string fica ainda mais vantajosa quando você tem várias variáveis:

\`\`\`python
nome = input()
cidade = "Recife"
print(f"{nome} é de {cidade}!")
# Carlos é de Recife!
\`\`\`

---

## Checklist antes de começar

- ✅ Coloque \`f\` antes das aspas: \`f"..."\`
- ✅ Use \`{variavel}\` dentro do texto
- ✅ Deixe \`input()\` sem texto dentro

---

## O que você vai praticar

No exercício, você vai escrever um programa que lê um nome com \`input()\` e exibe \`Bem-vindo, <nome>!\` usando f-string.

**Resultado esperado** (quando o sistema fornecer \`Carlos\`):
\`\`\`
Bem-vindo, Carlos!
\`\`\``,
    instruction: {
      pt: 'Que tal unir tudo que você aprendeu? Vamos usar `input()` para ler um nome **e** f-string para formatar a mensagem! 🚀\n\n**Exemplo:**\n```python\nnome = input()\nprint(f"Bem-vindo, {nome}!")\n```\n- Entrada: `Carlos`\n- Saída: `Bem-vindo, Carlos!`\n\n---\n\nEscreva um programa que:\n1. Leia um nome com `input()` (sem texto dentro)\n2. Exiba `Bem-vindo, <nome>!` usando **f-string**\n\n**Exemplo:**\n- Entrada: `Carlos`\n- Saída: `Bem-vindo, Carlos!`',
    },
    starter: 'nome = input()\nprint( ... )\n',
    hints: [
      'Lembre-se do `f` antes das aspas: `print(f"...")`',
      'Use `{nome}` dentro da f-string para inserir o valor da variável',
      'Não coloque nada dentro do `input()`. Deixe assim: `nome = input()`',
    ],
    tests: [
      { id: 1, stdin: 'Carlos', expected: 'Bem-vindo, Carlos!' },
    ],
    quiz: [
      { question: "Qual das opções lê um nome e exibe 'Bem-vindo, nome' usando f-string?", options: ["`nome = input('Bem-vindo'); print(nome)`", "`nome = input(); print('Bem-vindo, ' + nome)`", "`nome = input(); print(f'Bem-vindo, {nome}')`", "`input(nome); print('Bem-vindo, {nome}')`"], correct: 2 },
      { question: 'Por que não devemos colocar texto dentro do `input()` neste exercício?', options: ['Porque causa erro de sintaxe', 'Porque o texto apareceria na saída e quebraria o teste', 'Porque input() não aceita texto', 'Porque só funciona com números'], correct: 1 },
    ],
  },

  'tipos': {
    slug: 'tipos',
    title: 'Tipos de Dados',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 1: Fundamentos',
    order: 6,
    next: 'operadores',
    theory: `## Tipos de dados em Python

Em Python, cada valor tem um **tipo**. Os principais são:

\`\`\`python
nome = "Carlos"      # str — texto (string)
idade = 15           # int — número inteiro
altura = 1.75        # float — número decimal
ativo = True         # bool — verdadeiro ou falso
\`\`\`

### Descobrindo o tipo com type()
A função \`type()\` revela o tipo de qualquer valor:

\`\`\`python
print(type("Carlos"))   # <class 'str'>
print(type(15))         # <class 'int'>
print(type(1.75))       # <class 'float'>
print(type(True))       # <class 'bool'>
\`\`\`

### Por que os tipos importam?
Você não pode somar texto com número diretamente:
\`\`\`python
print("5" + 3)      # ❌ Erro!
print(int("5") + 3) # ✅ Saída: 8
\`\`\`

Conhecer os tipos evita erros e ajuda a entender o que o Python espera em cada situação. 🔍`,
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
    quiz: [
      { question: 'Qual função revela o tipo de um valor em Python?', options: ['typeof()', 'type()', 'kind()', 'gettype()'], correct: 1 },
      { question: 'Qual é o tipo de 3.14 em Python?', options: ['int', 'str', 'float', 'number'], correct: 2 },
      { question: 'Qual é o tipo de True em Python?', options: ['str', 'int', 'bool', 'flag'], correct: 2 },
    ],
  },

  'operadores': {
    slug: 'operadores',
    title: 'Operadores',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 1: Fundamentos',
    order: 7,
    next: 'if-else',
    theory: `## Operadores aritméticos em Python

Python funciona como uma calculadora poderosa:

\`\`\`python
print(10 + 3)   # 13 — soma
print(10 - 3)   # 7  — subtração
print(10 * 3)   # 30 — multiplicação
print(10 / 3)   # 3.333... — divisão
print(10 // 3)  # 3  — divisão inteira
print(10 % 3)   # 1  — resto da divisão
print(10 ** 2)  # 100 — potência
\`\`\`

### Operador % (módulo) — o mais especial!
O \`%\` retorna o **resto** da divisão. É muito útil para saber se um número é par ou ímpar:

\`\`\`python
print(10 % 2)  # 0 — 10 é par!
print(7 % 2)   # 1 — 7 é ímpar!
\`\`\`

### Ordem das operações
Python respeita a ordem matemática (PEMDAS):
\`\`\`python
print(2 + 3 * 4)    # 14 (multiplicação primeiro)
print((2 + 3) * 4)  # 20 (parênteses primeiro)
\`\`\``,
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
    quiz: [
      { question: 'O que o operador % faz em Python?', options: ['Divide dois números', 'Retorna o resto da divisão inteira', 'Calcula a porcentagem', 'Multiplica por 100'], correct: 1 },
      { question: 'Qual é o resultado de 17 // 5 em Python?', options: ['3', '3.4', '2', '5'], correct: 0 },
    ],
  },

  'if-else': {
    slug: 'if-else',
    title: 'if / else',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 2: Controle de Fluxo',
    order: 8,
    next: 'python-zero-comparadores',
    theory: `## Tomando decisões com if/else

O \`if\` permite que seu programa tome **decisões** baseadas em condições:

\`\`\`python
idade = 18

if idade >= 18:
    print("Adulto")
else:
    print("Menor de idade")
# Saída: Adulto
\`\`\`

### Como funciona?
1. O Python avalia a condição (\`idade >= 18\`)
2. Se for **verdadeira** → executa o bloco do \`if\`
3. Se for **falsa** → executa o bloco do \`else\`

### ⚠️ Indentação é obrigatória!
O código dentro do \`if\` e \`else\` deve ter **4 espaços** (ou 1 tab) no início:

\`\`\`python
if True:
    print("Isso está dentro do if")  # ✅
print("Isso está fora do if")        # ✅

if True:
print("Erro!")  # ❌ IndentationError
\`\`\`

### Por que isso importa?
Sem condicionais, todo programa faria sempre a mesma coisa. Com \`if/else\`, seu código pode reagir a diferentes situações! 🎯`,
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
    quiz: [
      { question: 'O que o bloco else executa?', options: ['Sempre executa, independente da condição', 'Executa quando a condição do if é falsa', 'Executa antes do if', 'Executa quando há erro'], correct: 1 },
      { question: 'Por que usar int(input()) ao ler uma idade?', options: ['Para formatar o texto', 'Porque input() retorna string e precisamos de número inteiro', 'Para tornar a leitura mais rápida', 'Porque int() é obrigatório com input()'], correct: 1 },
    ],
  },

  'python-zero-comparadores': {
    slug: 'python-zero-comparadores',
    title: 'Comparadores',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 2: Controle de Fluxo',
    order: 9,
    next: 'python-zero-elif',
    theory: `## Comparadores em Python

Comparadores comparam dois valores e retornam \`True\` (verdadeiro) ou \`False\` (falso):

\`\`\`python
print(10 > 5)   # True  — 10 é maior que 5?
print(10 < 5)   # False — 10 é menor que 5?
print(10 == 10) # True  — 10 é igual a 10?
print(10 != 5)  # True  — 10 é diferente de 5?
print(10 >= 10) # True  — 10 é maior ou igual a 10?
print(10 <= 9)  # False — 10 é menor ou igual a 9?
\`\`\`

### ⚠️ = vs ==
- \`=\` **atribui** um valor a uma variável: \`idade = 15\`
- \`==\` **compara** dois valores: \`idade == 15\`

\`\`\`python
idade = 15         # atribuição
print(idade == 15) # True — comparação
print(idade == 16) # False
\`\`\`

### Comparadores com texto
\`\`\`python
nome = "Ana"
print(nome == "Ana")    # True
print(nome == "carlos") # False (maiúsculas importam!)
\`\`\``,
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
    quiz: [
      { question: 'Qual operador verifica se dois valores são iguais em Python?', options: ['=', '==', '===', 'eq'], correct: 1 },
      { question: 'O que a comparação 10 != 5 retorna?', options: ['False', 'True', '5', 'Error'], correct: 1 },
      { question: 'Qual comparador verifica se um valor é maior ou igual a outro?', options: ['>', '<', '>=', '=>'], correct: 2 },
    ],
  },

  'python-zero-elif': {
    slug: 'python-zero-elif',
    title: 'Múltiplas condições com elif',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 2: Controle de Fluxo',
    order: 10,
    next: 'python-zero-for',
    theory: `## Múltiplas condições com elif

Quando você precisa verificar mais de duas possibilidades, use \`elif\` (abreviação de "else if"):

\`\`\`python
nota = 7.5

if nota >= 7:
    print("Aprovado")
elif nota >= 5:
    print("Recuperação")
else:
    print("Reprovado")
# Saída: Aprovado
\`\`\`

### Como o Python avalia?
Ele verifica as condições **em ordem**, de cima para baixo, e executa apenas o primeiro bloco que for verdadeiro:

\`\`\`python
x = 15

if x > 20:
    print("Maior que 20")    # falso, pula
elif x > 10:
    print("Maior que 10")    # verdadeiro! executa e para
elif x > 5:
    print("Maior que 5")     # nem chega aqui
else:
    print("5 ou menos")      # nem chega aqui
# Saída: Maior que 10
\`\`\`

### Dica importante
A ordem das condições importa muito! Sempre coloque as condições mais específicas primeiro. 🎯`,
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
    quiz: [
      { question: 'O que elif significa em Python?', options: ['end if — encerra o bloco', 'else if — nova condição quando a anterior é falsa', 'error if — trata erros', 'eval if — avalia expressão'], correct: 1 },
      { question: 'Quantos elif podemos ter em uma cadeia if/elif/else?', options: ['Apenas 1', 'No máximo 3', 'Quantos forem necessários', 'Nenhum — elif não existe'], correct: 2 },
    ],
  },

  'python-zero-for': {
    slug: 'python-zero-for',
    title: 'Repetindo com for',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 2: Controle de Fluxo',
    order: 11,
    next: 'python-zero-listas',
    theory: `## Repetindo com for

O loop \`for\` com \`range()\` repete um bloco de código um número específico de vezes:

\`\`\`python
for i in range(5):
    print(i)
# Saída:
# 0
# 1
# 2
# 3
# 4
\`\`\`

### Entendendo o range()
\`\`\`python
range(5)        # 0, 1, 2, 3, 4 (começa em 0)
range(1, 6)     # 1, 2, 3, 4, 5 (de 1 até 5)
range(0, 10, 2) # 0, 2, 4, 6, 8 (de 2 em 2)
\`\`\`

### Usando o for com cálculos
\`\`\`python
for i in range(1, 6):
    print(f"5 x {i} = {5 * i}")
# Saída:
# 5 x 1 = 5
# 5 x 2 = 10
# ...
\`\`\`

### Por que usar for e não while?
Use \`for\` quando você sabe **quantas vezes** quer repetir. Use \`while\` quando a repetição depende de uma condição. 🔄`,
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
    quiz: [
      { question: 'O que range(1, 6) gera em Python?', options: ['1, 2, 3, 4, 5, 6', '1, 2, 3, 4, 5', '0, 1, 2, 3, 4, 5', '2, 3, 4, 5, 6'], correct: 1 },
      { question: 'Quantas vezes "for i in range(4)" executa?', options: ['5 vezes', '3 vezes', '4 vezes', '1 vez'], correct: 2 },
    ],
  },

  'python-zero-listas': {
    slug: 'python-zero-listas',
    title: 'Listas',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 2: Controle de Fluxo',
    order: 12,
    next: 'while',
    theory: `## Listas em Python

Listas guardam **vários valores em uma única variável**, como uma coleção:

\`\`\`python
frutas = ["maçã", "banana", "uva"]
numeros = [1, 2, 3, 4, 5]
misturado = ["Ana", 15, True, 3.14]
\`\`\`

### Acessando itens (índice começa em 0!)
\`\`\`python
frutas = ["maçã", "banana", "uva"]
print(frutas[0])  # maçã
print(frutas[1])  # banana
print(frutas[2])  # uva
\`\`\`

### Percorrendo uma lista com for
\`\`\`python
frutas = ["maçã", "banana", "uva"]
for fruta in frutas:
    print(fruta)
# Saída:
# maçã
# banana
# uva
\`\`\`

### Tamanho da lista com len()
\`\`\`python
print(len(frutas))  # 3
\`\`\`

### Por que usar listas?
Imagine guardar 100 nomes em 100 variáveis diferentes... Com listas você faz isso com uma linha! 📦`,
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
    quiz: [
      { question: 'Qual é o índice do primeiro elemento de uma lista Python?', options: ['1', '0', '-1', 'Depende da lista'], correct: 1 },
      { question: 'Qual função retorna o número de itens de uma lista?', options: ['size()', 'count()', 'len()', 'length()'], correct: 2 },
    ],
  },

  'while': {
    slug: 'while',
    title: 'Loop while',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 2: Controle de Fluxo',
    order: 13,
    next: 'python-zero-funcoes',
    theory: `## Loop while

O \`while\` repete um bloco **enquanto** uma condição for verdadeira:

\`\`\`python
i = 1
while i <= 5:
    print(i)
    i += 1
# Saída: 1, 2, 3, 4, 5
\`\`\`

### Como funciona?
1. Verifica a condição (\`i <= 5\`)
2. Se verdadeira → executa o bloco
3. Volta para o passo 1
4. Se falsa → para o loop

### ⚠️ Cuidado com loop infinito!
Sempre garanta que a condição vai se tornar falsa em algum momento:

\`\`\`python
# ❌ Loop infinito — nunca para!
i = 1
while i <= 5:
    print(i)
    # Esqueceu o i += 1 !

# ✅ Correto
i = 1
while i <= 5:
    print(i)
    i += 1  # incrementa i a cada repetição
\`\`\`

### Quando usar while vs for?
- **for**: quando sabe quantas vezes repetir
- **while**: quando repete até uma condição mudar 🔁`,
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
    quiz: [
      { question: 'Quando um loop while para de executar?', options: ['Após 100 iterações', 'Quando a condição se torna False', 'Após 1 segundo', 'Quando return é chamado'], correct: 1 },
      { question: 'O que é um loop infinito?', options: ['Um loop que executa exatamente 1000 vezes', 'Um loop cuja condição nunca se torna False', 'Um loop com range(infinity)', 'Um loop aninhado'], correct: 1 },
    ],
  },
  'python-zero-funcoes': {
    slug: 'python-zero-funcoes',
    title: 'Funções',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 3: Funções',
    order: 14,
    next: 'python-zero-parametros',
    theory: `## Funções em Python

Funções são blocos de código que você escreve **uma vez** e pode chamar quantas vezes quiser — como uma receita que você pode repetir sempre que precisar!

\`\`\`python
def cumprimentar():
    print("Olá, CodeFuturo!")

cumprimentar()  # chama a função
cumprimentar()  # pode chamar de novo!
# Saída:
# Olá, CodeFuturo!
# Olá, CodeFuturo!
\`\`\`

### Funções que retornam valores
O \`return\` faz a função **devolver** um resultado para quem chamou:

\`\`\`python
def dobrar(numero):
    return numero * 2

resultado = dobrar(5)
print(resultado)  # 10
\`\`\`

### Por que usar funções?
Sem funções, você repetiria o mesmo código várias vezes. Com elas, o código fica **organizado, reutilizável e fácil de corrigir**. É o jeito profissional de programar! 🏆`,
    instruction: {
      pt: 'Funções são blocos de código que você escreve uma vez e pode usar quantas vezes quiser! Em Python, criamos uma função com a palavra `def`, seguida do nome e parênteses.\n\nExemplo:\n```python\ndef cumprimentar():\n    print("Oi!")\n\ncumprimentar()  # chama a função\n```\n\nO `return` faz a função **devolver** um valor para quem chamou ela.\n\nSua tarefa: complete a função `saudacao(nome)` que recebe um nome e **retorna** a mensagem `"Olá, {nome}!"`.\n\nExemplo:\n- `print(saudacao("Ana"))` → `Olá, Ana!`',
      en: 'Create a function saudacao(nome) that returns "Olá, {nome}!".',
      es: 'Crea una función saudacao(nome) que retorne "Olá, {nome}!".',
    },
    starter: 'def saudacao(___):\n    return ___\n\nprint(saudacao("Ana"))\n',
    hints: [
      'A palavra `def` define a função. Dentro dos parênteses coloque o nome do parâmetro — aqui é `nome`.',
      'Use uma f-string para montar a mensagem: `return f"Olá, {nome}!"` — lembre das chaves em volta de `nome`.',
    ],
    tests: [
      { id: 1, stdin: '', expected: 'Olá, Ana!' },
    ],
    quiz: [
      { question: 'Qual palavra-chave define uma função em Python?', options: ['function', 'def', 'func', 'fn'], correct: 1 },
      { question: 'O que return faz dentro de uma função?', options: ['Imprime o resultado na tela', 'Devolve um valor e encerra a função', 'Chama outra função', 'Reinicia a função'], correct: 1 },
    ],
  },

  'python-zero-parametros': {
    slug: 'python-zero-parametros',
    title: 'Parâmetros e argumentos',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 3: Funções',
    order: 15,
    next: 'python-zero-listas-avancado',
    theory: `## Parâmetros e argumentos

**Parâmetro** é o nome que você coloca na definição da função. **Argumento** é o valor que você passa quando chama a função.

\`\`\`python
def saudar(nome):         # nome é o parâmetro
    print(f"Olá, {nome}!")

saudar("Fernanda")        # "Fernanda" é o argumento
saudar("João")            # "João" é outro argumento
# Saída:
# Olá, Fernanda!
# Olá, João!
\`\`\`

### Múltiplos parâmetros
Você pode ter quantos parâmetros precisar, separados por vírgula:

\`\`\`python
def calcular_imc(peso, altura):
    imc = peso / (altura ** 2)
    return round(imc, 1)

print(calcular_imc(70, 1.75))  # 22.9
\`\`\`

### Por que isso importa?
Parâmetros tornam suas funções **flexíveis e reutilizáveis**. Em vez de criar uma função diferente para cada nome, você usa uma só função que aceita qualquer nome! 🎯`,
    instruction: {
      pt: '**Parâmetro** é o nome que você coloca na definição da função. **Argumento** é o valor que você passa quando chama a função.\n\nExemplo:\n```python\ndef dobrar(numero):   # numero é o parâmetro\n    return numero * 2\n\nprint(dobrar(5))      # 5 é o argumento → imprime 10\n```\n\nAgora você vai calcular a **área de um triângulo**! A fórmula é: `base × altura / 2`.\n\nCrie a função `calcular_area(base, altura)` que retorna a área do triângulo.\n\nExemplos:\n- `calcular_area(10, 5)` → `25.0`\n- `calcular_area(6, 4)` → `12.0`',
      en: 'Create calcular_area(base, altura) that returns base * altura / 2.',
      es: 'Crea calcular_area(base, altura) que retorna base * altura / 2.',
    },
    starter: 'def calcular_area(___, ___):\n    return ___ * ___ / 2\n\nprint(calcular_area(10, 5))\nprint(calcular_area(6, 4))\n',
    hints: [
      'Coloque os dois parâmetros separados por vírgula: `def calcular_area(base, altura):`.',
      'No corpo da função, substitua os `___` pelos nomes dos parâmetros: `return base * altura / 2`.',
    ],
    tests: [
      { id: 1, stdin: '', expected: '25.0\n12.0' },
    ],
    quiz: [
      { question: 'Qual é a diferença entre parâmetro e argumento?', options: ['São a mesma coisa', 'Parâmetro está na definição; argumento é o valor passado na chamada', 'Argumento está na definição; parâmetro é o valor passado', 'Parâmetro só existe em funções recursivas'], correct: 1 },
      { question: 'Uma função pode ter mais de um parâmetro?', options: ['Não, apenas um', 'Sim, separados por vírgula', 'Sim, mas apenas dois', 'Depende do tipo de dado'], correct: 1 },
    ],
  },

  'python-zero-listas-avancado': {
    slug: 'python-zero-listas-avancado',
    title: 'Listas avançadas',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 3: Funções',
    order: 16,
    next: 'python-zero-dicionarios',
    theory: `## Manipulando listas

Listas têm métodos poderosos para gerenciar seus itens de forma dinâmica:

\`\`\`python
lista = ["Ana", "Bruno"]

lista.append("Carlos")   # adiciona no final
# lista = ["Ana", "Bruno", "Carlos"]

lista.remove("Bruno")    # remove a primeira ocorrência
# lista = ["Ana", "Carlos"]

print(len(lista))        # 2 — conta os itens
\`\`\`

### Outros métodos úteis
\`\`\`python
numeros = [3, 1, 4, 1, 5]

numeros.sort()           # ordena a lista
print(numeros)           # [1, 1, 3, 4, 5]

numeros.reverse()        # inverte a ordem
print(numeros)           # [5, 4, 3, 1, 1]

print(numeros.count(1))  # 2 — conta quantos "1" existem
\`\`\`

### Por que isso importa?
No dia a dia de um programador, você vai constantemente adicionar, remover e organizar dados em listas — como um carrinho de compras, uma fila de espera ou a lista de posts de uma rede social! 🛒`,
    instruction: {
      pt: 'Listas têm métodos poderosos para gerenciar seus itens:\n- `lista.append(item)` → adiciona um item no final\n- `lista.remove(item)` → remove a primeira ocorrência do item\n- `len(lista)` → retorna o número de itens\n\nVocê está organizando a **lista de convidados de uma festa**! Comece com `["Ana", "Bruno"]`, adicione `"Carlos"` com `append`, remova `"Bruno"` com `remove`, depois imprima cada nome e o total.\n\nSaída esperada:\n```\nAna\nCarlos\nTotal: 2\n```',
      en: 'Manage a guest list using append, remove, len and a for loop.',
      es: 'Gestiona una lista de invitados usando append, remove, len y for.',
    },
    starter: 'convidados = ["Ana", "Bruno"]\n\nconvidados.___(___)\nconvidados.___(___)\n\nfor convidado in convidados:\n    print(___)\n\nprint(f"Total: {___}")\n',
    hints: [
      'Use `convidados.append("Carlos")` para adicionar e `convidados.remove("Bruno")` para remover.',
      'No `for`, imprima a variável do loop: `print(convidado)`. Para o total, use `len(convidados)` dentro da f-string.',
    ],
    tests: [
      { id: 1, stdin: '', expected: 'Ana\nCarlos\nTotal: 2' },
    ],
    quiz: [
      { question: 'Qual método adiciona um item ao final de uma lista?', options: ['add()', 'insert()', 'push()', 'append()'], correct: 3 },
      { question: 'O que lista.remove("Bruno") faz?', options: ['Remove todos os itens iguais a "Bruno"', 'Remove a primeira ocorrência de "Bruno"', 'Remove o último item da lista', 'Apaga a lista inteira'], correct: 1 },
    ],
  },

  'python-zero-dicionarios': {
    slug: 'python-zero-dicionarios',
    title: 'Dicionários',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 3: Funções',
    order: 17,
    next: 'python-zero-strings',
    theory: `## Dicionários em Python

Dicionários guardam informações em pares **chave: valor** — como uma ficha de cadastro onde cada campo tem um nome!

\`\`\`python
aluno = {
    "nome": "Beatriz",
    "idade": 14,
    "cidade": "Recife"
}

print(aluno["nome"])    # Beatriz
print(aluno["cidade"])  # Recife
\`\`\`

### Adicionando e alterando dados
\`\`\`python
aluno["nota"] = 9.5       # adiciona nova chave
aluno["idade"] = 15       # atualiza valor existente
print(aluno["nota"])      # 9.5
\`\`\`

### Verificando se uma chave existe
\`\`\`python
if "nota" in aluno:
    print("Tem nota!")
\`\`\`

### Por que usar dicionários?
Imagine um app de delivery — cada pedido tem cliente, endereço, itens, preço total. Dicionários são perfeitos para guardar essas informações relacionadas! 🍕`,
    instruction: {
      pt: 'Dicionários guardam informações em pares **chave: valor** — como uma ficha com campos!\n\nExemplo:\n```python\npessoa = {"nome": "Ana", "idade": 20}\nprint(pessoa["nome"])  # Ana\n```\n\nVocê vai criar a **ficha de um aluno** com três informações: nome, idade e nota.\n\nSaída esperada:\n```\nNome: Carlos\nIdade: 15\nNota: 8.5\n```',
      en: 'Create a student dict with name, age and grade, then print each value.',
      es: 'Crea un diccionario de alumno con nombre, edad y nota, luego imprime cada valor.',
    },
    starter: 'aluno = {\n    "nome": ___,\n    "idade": ___,\n    "nota": ___\n}\n\nprint(f"Nome: {aluno[___]}")\nprint(f"Idade: {aluno[___]}")\nprint(f"Nota: {aluno[___]}")\n',
    hints: [
      'Preencha os valores do dicionário: `"Carlos"` para nome, `15` para idade, `8.5` para nota. Strings precisam de aspas, números não.',
      'Para acessar um valor, use o nome da chave entre aspas e colchetes: `aluno["nome"]`. Substitua os `___` nos prints.',
    ],
    tests: [
      { id: 1, stdin: '', expected: 'Nome: Carlos\nIdade: 15\nNota: 8.5' },
    ],
    quiz: [
      { question: 'Como acessar o valor da chave "nome" em um dicionário aluno?', options: ['aluno.nome', 'aluno["nome"]', 'aluno->nome', 'aluno.get_nome()'], correct: 1 },
      { question: 'O que um dicionário Python armazena?', options: ['Apenas valores numéricos', 'Pares de chave: valor', 'Listas ordenadas', 'Apenas strings'], correct: 1 },
      { question: 'Como verificar se "idade" é uma chave no dicionário d?', options: ['"idade" in d', 'd.has("idade")', 'd.exists("idade")', 'check(d, "idade")'], correct: 0 },
    ],
  },

  'python-zero-strings': {
    slug: 'python-zero-strings',
    title: 'Manipulando texto',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 3: Funções',
    order: 18,
    next: 'python-zero-projeto',
    theory: `## Manipulando strings em Python

Strings têm métodos incríveis para transformar texto do jeito que você precisar:

\`\`\`python
nome = "  Gabriela Silva  "

print(nome.strip())    # "Gabriela Silva" — remove espaços extras
print(nome.upper())    # "  GABRIELA SILVA  " — tudo maiúsculo
print(nome.lower())    # "  gabriela silva  " — tudo minúsculo
\`\`\`

### Substituindo e dividindo
\`\`\`python
frase = "Python é difícil"
print(frase.replace("difícil", "incrível"))
# Python é incrível

cpf = "123.456.789-00"
partes = cpf.split(".")
print(partes)  # ['123', '456', '789-00']
\`\`\`

### Contando e verificando
\`\`\`python
texto = "CodeFuturo é incrível!"
print(len(texto))              # 22 — número de caracteres
print(texto.count("i"))        # 3 — quantas letras "i"
print(texto.startswith("Code")) # True
\`\`\`

### Por que isso importa?
Processar texto é uma das tarefas mais comuns na programação — validar formulários, formatar relatórios, analisar dados. Dominar strings é essencial! 📝`,
    instruction: {
      pt: 'Strings têm métodos incríveis para transformar texto:\n- `.upper()` → TUDO EM MAIÚSCULAS\n- `.lower()` → tudo em minúsculas\n- `.strip()` → remove espaços extras nas bordas\n- `.replace(a, b)` → substitui `a` por `b`\n\nSua tarefa: leia um nome com `input()`, depois imprima:\n1. O nome em **MAIÚSCULAS**\n2. O nome em **minúsculas**\n3. O **número de caracteres** do nome\n\nExemplo — entrada `ana`:\n```\nANA\nana\n3\n```',
      en: 'Read a name with input() and print it in uppercase, lowercase and its length.',
      es: 'Lee un nombre con input() e imprime en mayúsculas, minúsculas y su longitud.',
    },
    starter: 'nome = input("Digite seu nome: ")\n\nprint(nome.___())\nprint(nome.___())\nprint(___)\n',
    hints: [
      'Use `.upper()` para maiúsculas e `.lower()` para minúsculas: `nome.upper()` e `nome.lower()`.',
      'Para contar os caracteres, use `len(nome)` — a função `len()` funciona tanto em listas quanto em strings!',
    ],
    tests: [
      { id: 1, stdin: 'ana', expected: 'ANA\nana\n3' },
      { id: 2, stdin: 'Carlos', expected: 'CARLOS\ncarlos\n6' },
    ],
    quiz: [
      { question: 'Qual método converte uma string para maiúsculas em Python?', options: ['capitalize()', 'toUpperCase()', 'upper()', 'uppercase()'], correct: 2 },
      { question: 'O que o método strip() faz em uma string?', options: ['Remove todos os espaços da string', 'Remove espaços do início e do fim', 'Divide a string em pedaços', 'Substitui caracteres especiais'], correct: 1 },
    ],
  },

  'python-zero-projeto': {
    slug: 'python-zero-projeto',
    title: 'Projeto final',
    path: 'Python do Zero',
    pathSlug: 'python-zero',
    chapter: 'Capítulo 3: Funções',
    order: 19,
    next: null,
    theory: `## Projeto Final — Sistema de Notas

Chegou a hora de juntar tudo que você aprendeu! Neste projeto, você vai criar um sistema completo que combina:

- **input()** — para ler dados do usuário
- **float()** — para converter a nota
- **if/elif/else** — para classificar o resultado
- **listas** — para guardar os aprovados
- **in** — para verificar se está na lista

### Revisão rápida dos conceitos
\`\`\`python
# Lendo e convertendo entrada
nota = float(input())  # converte string para decimal

# Classificação com if/elif/else
if nota >= 7:
    print("Aprovado")
elif nota >= 5:
    print("Recuperação")
else:
    print("Reprovado")

# Trabalhando com lista
aprovados = []
aprovados.append("Ana")   # adiciona
print("Ana" in aprovados) # True — verifica
\`\`\`

### Você já sabe tudo isso!
Este projeto não tem nada de novo — é só combinar o que você já domina. Respira fundo e vai com confiança! Você chegou longe. 🚀`,
    instruction: {
      pt: 'Chegou a hora de combinar tudo que você aprendeu! Vamos criar um **sistema de cadastro de alunos**.\n\nO programa deve:\n1. Ler o **nome** do aluno com `input()`\n2. Ler a **nota** com `input()` (converta para `float`)\n3. Imprimir o resultado:\n   - `"Aprovado"` se nota >= 7\n   - `"Recuperação"` se nota >= 5\n   - `"Reprovado"` se nota < 5\n4. Adicionar o nome à lista `aprovados` se foi aprovado\n5. Imprimir se o aluno está ou não na lista\n\nExemplo — nome `Carlos`, nota `8`:\n```\nAprovado\nCarlos está na lista de aprovados\n```',
      en: 'Build a student registration system combining input, if/elif, lists and functions.',
      es: 'Crea un sistema de registro de alumnos combinando input, if/elif, listas y funciones.',
    },
    starter: 'aprovados = []\n\nnome = input()\nnota = float(input())\n\nif nota >= ___:\n    print("Aprovado")\n    aprovados.___(___)\nelif nota >= ___:\n    print("Recuperação")\nelse:\n    print("Reprovado")\n\nif nome in aprovados:\n    print(f"{___} está na lista de aprovados")\nelse:\n    print(f"{___} não está na lista de aprovados")\n',
    hints: [
      'Para a condição de aprovação use `nota >= 7` e para recuperação `nota >= 5`. A ordem das condições importa — verifique do maior para o menor!',
      'Para adicionar o nome à lista de aprovados use `aprovados.append(nome)`. Isso deve ficar dentro do bloco `if` de Aprovado.',
      'No último `if/else`, substitua os `___` pelo nome da variável `nome` para montar a mensagem correta.',
    ],
    tests: [
      { id: 1, stdin: 'Carlos\n8', expected: 'Aprovado\nCarlos está na lista de aprovados' },
      { id: 2, stdin: 'Maria\n6', expected: 'Recuperação\nMaria não está na lista de aprovados' },
      { id: 3, stdin: 'João\n3', expected: 'Reprovado\nJoão não está na lista de aprovados' },
    ],
    quiz: [
      { question: 'Qual estrutura verifica se um nome está dentro de uma lista?', options: ['nome.in(lista)', 'nome in lista', 'lista.contains(nome)', 'lista.find(nome)'], correct: 1 },
      { question: 'Por que usamos float(input()) para ler a nota neste projeto?', options: ['Para aceitar notas com decimais como 6.5', 'Porque float é obrigatório com input()', 'Para arredondar a nota automaticamente', 'Para converter a nota em string'], correct: 0 },
      { question: 'O que lista.append(nome) faz neste projeto?', options: ['Verifica se o nome está na lista', 'Remove o nome da lista', 'Adiciona o nome ao final da lista de aprovados', 'Imprime o nome na tela'], correct: 2 },
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
  theory: `## Bem-vindo ao JavaScript!

JavaScript é a linguagem da web — ela roda no navegador e faz as páginas se tornarem interativas. Todo site moderno usa JavaScript!

A função \`console.log()\` é como o \`print()\` do Python: ela exibe mensagens no console do navegador.

\`\`\`js
console.log("Olá, Mundo!")
// Saída: Olá, Mundo!
\`\`\`

Você pode exibir números, textos e muito mais:

\`\`\`js
console.log("Bem-vindo ao JavaScript!")
console.log(42)
console.log(true)
\`\`\`

### Por que isso importa?
\`console.log()\` é sua ferramenta de depuração número 1. Todo dev JavaScript usa para entender o que está acontecendo no código. É o primeiro passo da sua jornada web! 🌐`,
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
  quiz: [
    { question: 'Como exibir texto no console em JavaScript?', options: ['print("texto")', 'echo("texto")', 'console.log("texto")', 'log("texto")'], correct: 2 },
    { question: 'console.log() em JavaScript é equivalente a qual função em Python?', options: ['input()', 'type()', 'print()', 'str()'], correct: 2 },
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
  theory: `## Variáveis em JavaScript

Em JavaScript moderno, temos duas formas de criar variáveis:

- **\`const\`** → para valores que **não mudam** (constantes)
- **\`let\`** → para valores que **podem mudar**

\`\`\`js
const nome = "Carlos"   // nome nunca vai mudar
let pontos = 0          // pontos vai aumentar com o tempo

pontos = pontos + 10    // ✅ pode reatribuir let
// nome = "João"        // ❌ erro! não pode reatribuir const
\`\`\`

### Exemplos do cotidiano
\`\`\`js
const cidade = "Fortaleza"   // cidade não muda
let temperatura = 32         // temperatura pode mudar

temperatura = 35             // atualiza normalmente
console.log(temperatura)     // 35
\`\`\`

### Por que não usar var?
O \`var\` é antigo e tem comportamentos confusos. Hoje em dia, todo código moderno usa \`const\` e \`let\`. Use sempre \`const\` por padrão e só troque para \`let\` quando precisar reatribuir. 💡`,
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
  quiz: [
    { question: 'Qual palavra-chave usar para uma variável que nunca muda em JavaScript?', options: ['let', 'var', 'const', 'static'], correct: 2 },
    { question: 'Qual é a diferença principal entre let e const?', options: ['let é mais rápido que const', 'const não pode ser reatribuído; let pode', 'let é para números; const é para texto', 'Não há diferença'], correct: 1 },
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
  theory: `## Tipos de dados em JavaScript

JavaScript tem alguns tipos básicos que você vai usar o tempo todo:

\`\`\`js
const nome = "Letícia"   // string — texto
const idade = 17         // number — número (int e float são o mesmo tipo!)
const aprovado = true    // boolean — verdadeiro ou falso
const sem_valor = null   // null — ausência intencional de valor
\`\`\`

### Descobrindo o tipo com typeof
O operador \`typeof\` revela o tipo de qualquer valor:

\`\`\`js
console.log(typeof "Letícia")  // string
console.log(typeof 17)         // number
console.log(typeof true)       // boolean
console.log(typeof 3.14)       // number (decimais são number também!)
\`\`\`

### Diferença do Python
No Python temos \`int\` e \`float\` separados. No JavaScript, **todo número é \`number\`** — não importa se tem casa decimal ou não!

### Por que isso importa?
Conhecer os tipos evita bugs chatos. Por exemplo, \`"5" + 3\` em JavaScript dá \`"53"\` (concatenação de texto), não \`8\`. Saber os tipos te salva de surpresas! 🔍`,
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
  quiz: [
    { question: 'O que typeof "Olá" retorna em JavaScript?', options: ['text', 'String', 'string', 'char'], correct: 2 },
    { question: 'Qual é o tipo de true em JavaScript?', options: ['string', 'number', 'Boolean', 'boolean'], correct: 3 },
    { question: 'O que typeof 42 retorna?', options: ['int', 'integer', 'number', 'num'], correct: 2 },
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
  theory: `## Operadores em JavaScript

JavaScript usa os mesmos operadores matemáticos que você já conhece:

\`\`\`js
console.log(10 + 3)   // 13 — soma
console.log(10 - 3)   // 7  — subtração
console.log(10 * 3)   // 30 — multiplicação
console.log(10 / 3)   // 3.333... — divisão
console.log(10 % 3)   // 1  — resto da divisão
console.log(10 ** 2)  // 100 — potência (ES2016+)
\`\`\`

### O operador % (módulo)
Muito útil para saber se um número é par ou ímpar:

\`\`\`js
console.log(10 % 2)  // 0 — par!
console.log(7 % 2)   // 1 — ímpar!
\`\`\`

### Atalhos de atribuição
\`\`\`js
let placar = 0
placar += 10   // placar = placar + 10 → 10
placar *= 2    // placar = placar * 2  → 20
placar++       // placar = placar + 1  → 21
console.log(placar)  // 21
\`\`\`

### Por que isso importa?
Você vai calcular preços, pontuações, distâncias, médias... Operadores são o coração de qualquer lógica matemática no código! 🧮`,
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
  quiz: [
    { question: 'O que o operador % faz em JavaScript?', options: ['Calcula porcentagem', 'Retorna o resto da divisão inteira', 'Divide e arredonda', 'Multiplica por 100'], correct: 1 },
    { question: 'Qual é o resultado de 7 * 6 em JavaScript?', options: ['13', '42', '76', '67'], correct: 1 },
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
  theory: `## Template Literals — textos dinâmicos

Template literals são o equivalente das f-strings do Python em JavaScript. Você usa **crases** (\` \` \`) em vez de aspas comuns, e \`\${}\` para inserir variáveis:

\`\`\`js
const produto = "Pastel de queijo"
const preco = 8
console.log(\`\${produto} custa R$ \${preco}\`)
// Saída: Pastel de queijo custa R$ 8
\`\`\`

### Comparando as formas:
\`\`\`js
const nome = "Rodrigo"
const cidade = "Curitiba"

// Com concatenação (mais trabalhoso):
console.log("Olá, " + nome + "! Você é de " + cidade + ".")

// Com template literal (muito mais limpo ✨):
console.log(\`Olá, \${nome}! Você é de \${cidade}.\`)
\`\`\`

### Você pode fazer cálculos dentro de ${}
\`\`\`js
const preco = 50
const desconto = 10
console.log(\`Preço final: R$ \${preco - desconto}\`)
// Saída: Preço final: R$ 40
\`\`\`

### Por que isso importa?
Template literals deixam o código muito mais legível. Em React e outros frameworks, você vai usá-los o tempo todo para montar textos dinâmicos! ⚡`,
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
  quiz: [
    { question: 'O que são template literals em JavaScript?', options: ['Strings com crase que permitem ${variável}', 'Modelos HTML prontos', 'Funções especiais de texto', 'Arrays de texto'], correct: 0 },
    { question: 'Qual caractere é usado para abrir um template literal?', options: ['Aspas simples \'', 'Aspas duplas "', 'Crase `', 'Til ~'], correct: 2 },
    { question: 'Como inserir uma variável dentro de um template literal?', options: ['#{variavel}', '${variavel}', '{variavel}', '{{variavel}}'], correct: 1 },
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
  theory: `## Comparadores em JavaScript

Comparadores comparam dois valores e retornam \`true\` ou \`false\`:

\`\`\`js
console.log(10 > 5)    // true  — maior que
console.log(10 < 5)    // false — menor que
console.log(10 == 10)  // true  — igual (valor)
console.log(10 === 10) // true  — igual (valor E tipo)
console.log(10 != 5)   // true  — diferente
console.log(10 >= 10)  // true  — maior ou igual
\`\`\`

### ⚠️ == vs === (importante!)
JavaScript tem dois operadores de igualdade:

\`\`\`js
console.log("5" == 5)   // true  — compara só o valor (converte tipo)
console.log("5" === 5)  // false — compara valor E tipo (string ≠ number)
\`\`\`

**Recomendação:** sempre use \`===\` para evitar surpresas!

### Comparadores com strings
\`\`\`js
const cidade = "São Paulo"
console.log(cidade === "São Paulo")  // true
console.log(cidade === "são paulo")  // false (maiúsculas importam!)
\`\`\`

### Por que isso importa?
Comparadores são a base de toda lógica condicional. Sem eles, seu código não consegue tomar nenhuma decisão! 🎯`,
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
  quiz: [
    { question: 'Qual operador verifica igualdade estrita (tipo e valor) em JavaScript?', options: ['==', '===', '=', 'eq'], correct: 1 },
    { question: 'O que 80 != 100 retorna em JavaScript?', options: ['false', 'true', '80', 'Error'], correct: 1 },
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
  theory: `## Decisões com if/else

O \`if/else\` em JavaScript funciona igual ao Python, mas usa **chaves** \`{}\` em vez de indentação:

\`\`\`js
const temperatura = 35

if (temperatura > 30) {
    console.log("Está muito quente!")
} else {
    console.log("Temperatura agradável.")
}
// Saída: Está muito quente!
\`\`\`

### Múltiplas condições com else if
\`\`\`js
const nota = 7.5

if (nota >= 7) {
    console.log("Aprovado!")
} else if (nota >= 5) {
    console.log("Recuperação")
} else {
    console.log("Reprovado")
}
// Saída: Aprovado!
\`\`\`

### Diferença do Python
- Python usa **indentação** (espaços) e dois-pontos \`:\`
- JavaScript usa **chaves** \`{}\` e parênteses na condição

\`\`\`js
// ✅ JavaScript correto:
if (x > 0) {
    console.log("positivo")
}
\`\`\`

### Por que isso importa?
Com if/else, seu código deixa de ser uma sequência fixa e passa a **responder** a diferentes situações. É aqui que a mágica começa! 🎯`,
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
  quiz: [
    { question: 'Em JavaScript, onde fica a condição do if?', options: ['Entre chaves {}', 'Entre parênteses ()', 'Após dois-pontos :', 'Entre colchetes []'], correct: 1 },
    { question: 'O que o bloco else executa?', options: ['Sempre, independente da condição', 'Quando a condição do if é verdadeira', 'Quando a condição do if é falsa', 'Quando há um erro no código'], correct: 2 },
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
  theory: `## Loop for em JavaScript

O loop \`for\` em JavaScript tem três partes separadas por ponto e vírgula:

\`\`\`js
for (let i = 1; i <= 5; i++) {
    console.log(i)
}
// Saída: 1, 2, 3, 4, 5
\`\`\`

- \`let i = 1\` → valor inicial
- \`i <= 5\` → condição de parada
- \`i++\` → incremento (equivale a \`i = i + 1\`)

### Usando o for com cálculos
\`\`\`js
for (let i = 1; i <= 5; i++) {
    console.log(\`2 x \${i} = \${2 * i}\`)
}
// Saída:
// 2 x 1 = 2
// 2 x 2 = 4
// ...
\`\`\`

### Comparando com Python
\`\`\`python
# Python:
for i in range(1, 6):
    print(i)
\`\`\`
\`\`\`js
// JavaScript:
for (let i = 1; i <= 5; i++) {
    console.log(i)
}
\`\`\`

### Por que isso importa?
Loops são essenciais para processar listas, gerar tabelas, repetir animações... qualquer tarefa repetitiva! Dominar o \`for\` é fundamental. 🔄`,
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
  quiz: [
    { question: 'No for tradicional do JavaScript, o que i++ faz?', options: ['Multiplica i por 2', 'Decrementa i em 1', 'Incrementa i em 1', 'Reinicia i para 0'], correct: 2 },
    { question: 'Qual é a estrutura correta de um for em JavaScript?', options: ['for i in range(5)', 'for (let i = 0; i < 5; i++)', 'for i = 0 to 5', 'foreach (0..5)'], correct: 1 },
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
  theory: `## Arrays em JavaScript

Arrays são listas de valores — o equivalente às listas do Python:

\`\`\`js
const estados = ["São Paulo", "Rio de Janeiro", "Bahia"]

console.log(estados[0])      // São Paulo (índice começa em 0!)
console.log(estados.length)  // 3 — número de itens
\`\`\`

### Percorrendo com for
\`\`\`js
const capitais = ["Brasília", "Salvador", "Manaus"]

for (let i = 0; i < capitais.length; i++) {
    console.log(capitais[i])
}
// Saída:
// Brasília
// Salvador
// Manaus
\`\`\`

### Métodos úteis de array
\`\`\`js
const times = ["Flamengo", "Corinthians"]

times.push("Palmeiras")    // adiciona no final
console.log(times.length)  // 3

times.pop()                // remove o último
console.log(times)         // ["Flamengo", "Corinthians"]
\`\`\`

### Por que isso importa?
Arrays são a estrutura de dados mais usada em JavaScript. Listas de produtos, posts, usuários, resultados de busca — tudo vive em arrays! 📦`,
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
  quiz: [
    { question: 'Como obter o número de elementos de um array em JavaScript?', options: ['array.size()', 'array.count', 'array.length', 'len(array)'], correct: 2 },
    { question: 'Qual é o índice do primeiro elemento de um array JavaScript?', options: ['1', '0', '-1', 'Depende do array'], correct: 1 },
    { question: 'Dado times = ["Flamengo", "Corinthians"], qual é times[1]?', options: ['"Flamengo"', '"Corinthians"', 'undefined', 'Error'], correct: 1 },
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
  theory: `## Funções em JavaScript

Funções são blocos de código reutilizáveis — você define uma vez e usa quantas vezes quiser!

\`\`\`js
function saudar(nome) {
    return \`Olá, \${nome}!\`
}

console.log(saudar("Beatriz"))  // Olá, Beatriz!
console.log(saudar("Pedro"))    // Olá, Pedro!
\`\`\`

### Arrow functions — a forma moderna
JavaScript tem uma sintaxe mais curta chamada **arrow function**:

\`\`\`js
// Função tradicional:
function dobrar(n) {
    return n * 2
}

// Arrow function equivalente:
const dobrar = (n) => n * 2

console.log(dobrar(5))   // 10
console.log(dobrar(15))  // 30
\`\`\`

### Funções com múltiplos parâmetros
\`\`\`js
function calcularDesconto(preco, percentual) {
    const desconto = preco * (percentual / 100)
    return preco - desconto
}

console.log(calcularDesconto(100, 10))  // 90
console.log(calcularDesconto(50, 20))   // 40
\`\`\`

### Por que isso importa?
Em JavaScript moderno (React, Node.js), funções são absolutamente centrais — você vai criar componentes, handlers de eventos, e muito mais usando funções! 🚀`,
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
  quiz: [
    { question: 'Como declarar uma função em JavaScript?', options: ['def somar() {}', 'func somar() {}', 'function somar() {}', 'fn somar() {}'], correct: 2 },
    { question: 'O que return faz em uma função JavaScript?', options: ['Imprime o valor no console', 'Devolve um valor e encerra a função', 'Chama a função novamente', 'Salva o valor em uma variável'], correct: 1 },
  ],
};

export const getLesson = (slug) => LESSONS[slug] || LESSONS['ola-mundo'];

export const getLessonList = (pathSlug = 'python-zero') => {
  return Object.values(LESSONS)
    .filter((l) => l.pathSlug === pathSlug)
    .sort((a, b) => a.order - b.order);
};
