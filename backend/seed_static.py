"""Seed estático — popula MongoDB sem usar LLM.

Todas as lições estão embutidas neste arquivo.
Idempotente: usa upsert por (path_slug, order).

Uso:
    python seed_static.py           # todas as trilhas
    python seed_static.py python    # só Python
"""
import asyncio
import re
import sys
import unicodedata
import uuid
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import os

ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")

client = AsyncIOMotorClient(os.environ["MONGO_URL"])
db = client[os.environ.get("DB_NAME", "codefuturo")]

# ---------------------------------------------------------------------------
# Metadados das trilhas
# ---------------------------------------------------------------------------

PATHS = [
    {"slug": "python-zero",  "name": "Python",      "language": "python",     "color": "#3776AB", "real_exec": True,  "desc": "A linguagem mais popular para iniciantes. Base sólida para IA, web, dados e automação."},
    {"slug": "javascript",   "name": "JavaScript",   "language": "javascript", "color": "#F7DF1E", "real_exec": True,  "desc": "A linguagem da web. Interatividade, frameworks modernos e Node.js."},
    {"slug": "html-css",     "name": "HTML & CSS",   "language": "html",       "color": "#E34F26", "real_exec": False, "desc": "A base da web. Aprenda a estruturar páginas e criar layouts modernos."},
    {"slug": "sql",          "name": "SQL",          "language": "sql",        "color": "#CC2927", "real_exec": False, "desc": "Linguagem para consultar e manipular bancos de dados relacionais."},
    {"slug": "typescript",   "name": "TypeScript",   "language": "typescript", "color": "#3178C6", "real_exec": False, "desc": "JavaScript com tipos. Essencial para projetos profissionais em escala."},
    {"slug": "java",         "name": "Java",         "language": "java",       "color": "#EA2D2E", "real_exec": False, "desc": "Orientação a objetos robusta. Usada em Android, empresas e backend."},
    {"slug": "cpp",          "name": "C++",          "language": "cpp",        "color": "#00599C", "real_exec": False, "desc": "Performance e controle total. Base de jogos, sistemas e engenharia."},
    {"slug": "go",           "name": "Go",           "language": "go",         "color": "#00ADD8", "real_exec": False, "desc": "Linguagem simples e poderosa do Google. Ideal para backend e DevOps."},
    {"slug": "ai-prompts",   "name": "AI Prompts",   "language": "prompts",    "color": "#A3E635", "real_exec": False, "desc": "Aprenda a conversar com IA. Engenharia de prompts para GPT, Claude e Gemini."},
]

# ---------------------------------------------------------------------------
# Lições por trilha
# Campos: title, chapter, order, instruction_pt, instruction_en, instruction_es,
#         starter_code, hint, tests: [{stdin, expected_stdout}]
# ---------------------------------------------------------------------------

LESSONS = {

# ── Python ──────────────────────────────────────────────────────────────────
"python-zero": [
  {
    "order": 1,
    "slug": "ola-mundo",
    "title": "Olá, Mundo!",
    "chapter": "Capítulo 1: Fundamentos",
    "theory": "A função `print()` é a primeira coisa que todo programador aprende. Ela serve para **exibir texto na tela** — como se o seu programa estivesse falando com você!\n\n## Como funciona\n\n```python\nprint(\"Olá, Mundo!\")\n```\n\n```\n# Olá, Mundo!\n```\n\nVocê pode imprimir qualquer texto colocando-o entre aspas dentro do `print()`:\n\n```python\nprint(\"Meu primeiro programa\")\nprint(\"Python é incrível!\")\n```\n\n```\n# Meu primeiro programa\n# Python é incrível!\n```\n\n## No exercício\n\nVocê vai usar `print()` para exibir exatamente `Olá, Mundo!` — com acento, vírgula e ponto de exclamação.",
    "instruction_pt": "Complete o código para exibir exatamente: `Olá, Mundo!`\n\nVeja o modelo:\n\n```python\nprint(\"Oi, Python!\")\n```",
    "instruction_en": "Use `print()` to show the message `Hello, World!`.",
    "instruction_es": "Usa `print()` para mostrar `¡Hola, Mundo!`.",
    "starter_code": "# Escreva seu código aqui\n",
    "hint": "A função `print()` exibe texto na tela. Coloque o texto que quer mostrar entre parênteses e aspas.",
    "hints": ["Use `print()` com o texto entre aspas: `print(\"Ola, Mundo!\")`", "Atencao aos detalhes: virgula apos Ola, espaco antes de Mundo e ponto de exclamacao no final."],
    "tests": [{"stdin": "", "expected_stdout": "Olá, Mundo!"}],
    "quiz": [{"question": "Qual função usamos para exibir texto na tela em Python?", "options": ["input()", "print()", "show()", "display()"], "correct": 1}, {"question": "O que acontece se você esquecer as aspas em print(Olá)?", "options": ["Exibe Olá normalmente", "Ocorre um erro — Python trata Olá como variável", "Exibe (Olá)", "Nada acontece"], "correct": 1}],
  },
  {
    "order": 2,
    "slug": "variaveis",
    "title": "Variáveis",
    "chapter": "Capítulo 1: Fundamentos",
    "theory": "Variáveis são como **caixas com etiquetas** onde você guarda informações para usar depois. Em Python, criar uma variável é simples:\n\n## Como funciona\n\n```python\nnome = \"Carlos\"\nidade = 15\naltura = 1.75\n```\n\nVocê pode guardar diferentes tipos de dados:\n- **Texto** (string): entre aspas — `\"Carlos\"`\n- **Número inteiro**: sem aspas — `15`\n- **Número decimal**: com ponto — `1.75`\n\n## Usando variáveis\n\nDepois de criar, é só usar o nome da variável onde precisar:\n\n```python\nnome = \"Ana\"\nprint(nome)\n```\n\n```\n# Ana\n```\n\n## No exercício\n\nAs variáveis `nome` e `idade` já estão declaradas. Você vai completar o `print()` usando f-string para exibir `Ana tem 12 anos`.",
    "instruction_pt": "As variáveis `nome` e `idade` já estão declaradas. Complete o `print()` para exibir a frase exata usando f-string.\n\nVeja como funciona uma f-string:\n\n```python\nnome = \"Ana\"\nidade = 12\nprint(f\"{nome} tem {idade} anos\")\n```",
    "instruction_en": "The variables `nome` and `idade` are already declared. Complete the `print()` to display: Ana tem 12 anos",
    "instruction_es": "Las variables `nome` y `idade` ya están declaradas. Completa el `print()` para mostrar: Ana tem 12 anos",
    "starter_code": "nome = \"Ana\"\nidade = 12\n\n# Complete o print usando f-string\nprint(f\"...\")  # substitua ... pela expressão correta\n",
    "hint": "Para combinar texto e variáveis em uma frase, experimente usar f-string — coloque `f` antes das aspas e use `{}` para inserir o valor de cada variável.",
    "hints": ["A variavel `nome` precisa ser declarada com `nome = \"Ana\"` antes do `print()`.", "Use f-string: `print(f\"{nome} tem {idade} anos\")` -- coloque cada variavel entre `{}`."],
    "tests": [{"stdin": "", "expected_stdout": "Ana tem 12 anos"}],
    "quiz": [{"question": "Como atribuir o valor \"Ana\" à variável nome em Python?", "options": ["var nome = \"Ana\"", "nome = \"Ana\"", "let nome = \"Ana\"", "string nome = \"Ana\""], "correct": 1}, {"question": "O que é uma f-string em Python?", "options": ["Uma string de formato fixo", "Uma string que permite inserir variáveis com {}", "Uma string de arquivo", "Uma string numérica"], "correct": 1}],
  },
  {
    "order": 3,
    "slug": "python-zero-fstrings",
    "title": "Usando f-strings",
    "chapter": "Capítulo 1: Fundamentos",
    "theory": "As **f-strings** são a forma mais prática de inserir variáveis dentro de textos em Python. Basta colocar a letra `f` antes das aspas e usar `{variavel}` onde o valor deve aparecer.\n\n## Como funciona\n\n```python\nnome = \"Ana\"\nprint(f\"Olá, {nome}!\")\n```\n\n```\n# Olá, Ana!\n```\n\nCom mais de uma variável:\n\n```python\nnome = \"Carlos\"\nidade = 16\nprint(f\"Meu nome é {nome} e tenho {idade} anos\")\n```\n\n```\n# Meu nome é Carlos e tenho 16 anos\n```\n\n## Comparando com a forma antiga\n\n```python\n# Forma antiga com concatenação:\nprint(\"Meu nome é \" + nome + \" e tenho \" + str(idade) + \" anos\")\n\n# Com f-string (muito mais simples!):\nprint(f\"Meu nome é {nome} e tenho {idade} anos\")\n```\n\n## No exercício\n\nAs variáveis `nome` e `idade` já estão declaradas. Você vai completar o `print()` usando f-string para exibir `Meu nome é Ana e tenho 16 anos`.",
    "instruction_pt": "As variáveis `nome` e `idade` já estão declaradas. Complete o `print()` usando f-string para exibir exatamente:\n\n`Meu nome é Ana e tenho 16 anos`\n\nVeja como inserir variáveis em outro exemplo:\n\n```python\ncidade = \"Recife\"\nprint(f\"Moro em {cidade}\")\n```",
    "instruction_en": "The variables `nome` and `idade` are already declared. Complete the `print()` using an f-string to display: Meu nome é Ana e tenho 16 anos",
    "instruction_es": "Las variables `nome` e `idade` ya están declaradas. Completa el `print()` usando f-string para mostrar: Meu nome é Ana e tenho 16 anos",
    "starter_code": "nome = \"Ana\"\nidade = 16\n# Use f-string para exibir: \"Meu nome é Ana e tenho 16 anos\"\nprint(...)\n",
    "hint": "",
    "hints": ["Coloque a letra `f` antes das aspas: `print(f\"...\")`", "Use `{nome}` e `{idade}` dentro das aspas para inserir os valores das variáveis"],
    "tests": [{"stdin": "", "expected_stdout": "Meu nome é Ana e tenho 16 anos"}],
    "quiz": [{"question": "O que a letra `f` antes das aspas indica em Python?", "options": ["Que o texto é falso", "Que é uma f-string e pode usar {variáveis}", "Que o texto é um float", "Que é uma função"], "correct": 1}, {"question": "Como você insere o valor de uma variável `cidade` dentro de uma f-string?", "options": ["print(f'Eu moro em cidade')", "print(f'Eu moro em (cidade)')", "print(f'Eu moro em {cidade}')", "print('Eu moro em' + f{cidade})"], "correct": 2}],
  },
  {
    "order": 4,
    "slug": "python-zero-input-concat",
    "title": "Lendo dados do usuário",
    "chapter": "Capítulo 1: Fundamentos",
    "theory": "Todo programa útil precisa conversar com quem está usando. Em Python, usamos a função `input()` para isso — ela **pausa o programa e espera o usuário digitar algo**.\n\n## Como funciona\n\n```python\nnome = input()\nprint(\"Olá, \" + nome)\n```\n\n```\n# Olá, Carlos\n```\n\nO operador `+` junta dois textos — isso se chama **concatenação**.\n\n## Regra importante\n\nDeixe o `input()` **sem texto dentro dos parênteses**:\n\n```python\nnome = input()        # correto\nnome = input(\"Nome:\") # não use neste exercício\n```\n\nPor quê? Os testes automáticos fornecem a entrada diretamente — qualquer texto dentro do `input()` apareceria na saída e quebraria o teste.\n\n## No exercício\n\nEscreva um programa que lê um nome e exibe `Olá, ` seguido do nome usando o operador `+`.",
    "instruction_pt": "Escreva um programa que leia um nome e exiba `Olá, ` seguido do nome usando o operador `+`.\n\nExemplo:\n- Entrada: `Carlos` → Saída: `Olá, Carlos`\n\nAtenção: deixe o `input()` sem texto dentro dos parênteses.",
    "instruction_en": "Write a program that reads a name with input() and prints 'Olá, ' followed by the name using the + operator.",
    "instruction_es": "Escribe un programa que lea un nombre con input() e imprima 'Olá, ' seguido del nombre usando el operador +.",
    "starter_code": "nome = input()\nprint(___)\n",
    "hint": "",
    "hints": ["O operador `+` junta dois textos. Ex: `\"Olá, \" + nome` — atenção ao espaço depois da vírgula!", "Não coloque nada dentro do `input()`. Deixe assim: `nome = input()`"],
    "tests": [{"stdin": "Carlos", "expected_stdout": "Olá, Carlos"}],
    "quiz": [{"question": "Para que serve a função `input()` em Python?", "options": ["Para imprimir texto na tela", "Para ler o que o usuário digitou", "Para criar variáveis automaticamente", "Para calcular valores"], "correct": 1}, {"question": "Se `nome = 'Ana'`, o que `'Olá, ' + nome` produz?", "options": ["Olá,Ana", "Olá, Ana", "Olá, + Ana", "Erro de sintaxe"], "correct": 1}],
  },
  {
    "order": 5,
    "slug": "python-zero-input-fstring",
    "title": "Entrada e formatação com f-string",
    "chapter": "Capítulo 1: Fundamentos",
    "theory": "Você já sabe usar `input()` para ler dados e f-strings para formatar texto. Agora vamos combinar as duas coisas!\n\n## Como funciona\n\n```python\nnome = input()\nprint(f\"Bem-vindo, {nome}!\")\n```\n\n```\n# Bem-vindo, Carlos!\n```\n\n## Por que f-string é melhor que concatenação?\n\n```python\n# Com concatenação (mais trabalhoso):\nprint(\"Bem-vindo, \" + nome + \"!\")\n\n# Com f-string (mais limpo):\nprint(f\"Bem-vindo, {nome}!\")\n```\n\n## No exercício\n\nEscreva um programa que lê um nome com `input()` (sem texto dentro) e exibe `Bem-vindo, <nome>!` usando f-string.",
    "instruction_pt": "Escreva um programa que leia um nome com `input()` e exiba `Bem-vindo, <nome>!` usando f-string.\n\nExemplo:\n- Entrada: `Carlos` → Saída: `Bem-vindo, Carlos!`",
    "instruction_en": "Write a program that reads a name with input() and displays 'Bem-vindo, <name>!' using an f-string.",
    "instruction_es": "Escribe un programa que lea un nombre con input() y muestre 'Bem-vindo, <nombre>!' usando f-string.",
    "starter_code": "nome = input()\nprint(___)\n",
    "hint": "",
    "hints": ["Lembre-se do `f` antes das aspas: `print(f\"...\")`", "Use `{nome}` dentro da f-string para inserir o valor da variável", "Não coloque nada dentro do `input()`. Deixe assim: `nome = input()`"],
    "tests": [{"stdin": "Carlos", "expected_stdout": "Bem-vindo, Carlos!"}],
    "quiz": [{"question": "Qual das opções lê um nome e exibe 'Bem-vindo, nome' usando f-string?", "options": ["nome = input('Bem-vindo'); print(nome)", "nome = input(); print('Bem-vindo, ' + nome)", "nome = input(); print(f'Bem-vindo, {nome}')", "input(nome); print('Bem-vindo, {nome}')"], "correct": 2}, {"question": "Por que não devemos colocar texto dentro do `input()` neste exercício?", "options": ["Porque causa erro de sintaxe", "Porque o texto apareceria na saída e quebraria o teste", "Porque input() não aceita texto", "Porque só funciona com números"], "correct": 1}],
  },
  {
    "order": 6,
    "slug": "tipos",
    "title": "Tipos de Dados",
    "chapter": "Capítulo 1: Fundamentos",
    "theory": "Em Python, cada valor tem um **tipo**. Os principais são:\n\n```python\nnome = \"Carlos\"      # str — texto (string)\nidade = 15           # int — número inteiro\naltura = 1.75        # float — número decimal\nativo = True         # bool — verdadeiro ou falso\n```\n\n## Como funciona\n\nA função `type()` revela o tipo de qualquer valor:\n\n```python\nprint(type(\"Carlos\"))\nprint(type(15))\nprint(type(1.75))\n```\n\n```\n# <class 'str'>\n# <class 'int'>\n# <class 'float'>\n```\n\n## Por que os tipos importam?\n\nVocê não pode somar texto com número diretamente:\n\n```python\nprint(int(\"5\") + 3)\n```\n\n```\n# 8\n```\n\n## No exercício\n\nImprime o tipo de `42`, `3.14` e `\"Python\"` usando `type()`.",
    "instruction_pt": "Em Python, cada valor tem um tipo. A função `type()` revela qual é esse tipo. Complete o código abaixo para imprimir o tipo de três valores diferentes:\n- O número inteiro `42`\n- O número decimal `3.14`\n- O texto `\"Python\"`\n\nVeja como funciona:\n\n```python\nprint(type(42))\nprint(type(3.14))\nprint(type(\"Python\"))\n```",
    "instruction_en": "Print the type of 42, 3.14 and \"Python\" using type().",
    "instruction_es": "Imprime el tipo de 42, 3.14 y \"Python\" usando type().",
    "starter_code": "# Complete: imprima o tipo de cada valor\nprint(type(___))\nprint(type(___))\nprint(type(___))\n",
    "hint": "A função `type()` recebe um valor como argumento e retorna o tipo dele. Por exemplo, `type(True)` retorna `<class 'bool'>`.",
    "hints": ["Use `type(42)` para o inteiro, `type(3.14)` para o decimal e `type(\"Python\")` para o texto.", "A ordem importa: primeiro `42` (int), depois `3.14` (float), depois `\"Python\"` (str)."],
    "tests": [{"stdin": "", "expected_stdout": "<class 'int'>\n<class 'float'>\n<class 'str'>"}],
    "quiz": [{"question": "Qual função revela o tipo de um valor em Python?", "options": ["typeof()", "type()", "kind()", "gettype()"], "correct": 1}, {"question": "Qual é o tipo de 3.14 em Python?", "options": ["int", "str", "float", "number"], "correct": 2}, {"question": "Qual é o tipo de True em Python?", "options": ["str", "int", "bool", "flag"], "correct": 2}],
  },
  {
    "order": 7,
    "slug": "operadores",
    "title": "Operadores",
    "chapter": "Capítulo 1: Fundamentos",
    "theory": "Python funciona como uma calculadora poderosa. Os operadores aritméticos são:\n\n## Como funciona\n\n```python\nprint(10 + 3)\nprint(10 * 3)\nprint(10 % 3)\nprint(10 ** 2)\n```\n\n```\n# 13\n# 30\n# 1\n# 100\n```\n\n## Operador % (módulo)\n\nO `%` retorna o **resto** da divisão. É muito útil para saber se um número é par ou ímpar:\n\n```python\nprint(10 % 2)\nprint(7 % 2)\n```\n\n```\n# 0\n# 1\n```\n\n## Ordem das operações\n\nPython respeita a ordem matemática:\n\n```python\nprint(2 + 3 * 4)\nprint((2 + 3) * 4)\n```\n\n```\n# 14\n# 20\n```\n\n## No exercício\n\nCalcule e imprima `15 + 7`, `8 * 6` e `17 % 5` cada um em uma linha.",
    "instruction_pt": "Calcule e imprima, cada resultado em uma linha separada:\n- A soma de `15 + 7`\n- A multiplicação de `8 * 6`\n- O resto da divisão de `17 % 5`\n\nVeja como funciona:\n\n```python\nprint(15 + 7)\nprint(8 * 6)\nprint(17 % 5)\n```",
    "instruction_en": "Print 15+7, 8*6 and 17%5 each on a new line.",
    "instruction_es": "Imprime 15+7, 8*6 y 17%5 cada uno en una línea.",
    "starter_code": "# Linha 1: soma\n# Linha 2: multiplicação\n# Linha 3: resto da divisão\n",
    "hint": "Você pode passar uma expressão matemática diretamente dentro do `print()`. Por exemplo, `print(3 + 2)` imprime `5`.",
    "hints": ["Use `print(15 + 7)` na primeira linha, `print(8 * 6)` na segunda.", "O operador `%` e o resto da divisao: `17 % 5` = 2 (porque 17 = 3x5 + 2)."],
    "tests": [{"stdin": "", "expected_stdout": "22\n48\n2"}],
    "quiz": [{"question": "O que o operador % faz em Python?", "options": ["Divide dois números", "Retorna o resto da divisão inteira", "Calcula a porcentagem", "Multiplica por 100"], "correct": 1}, {"question": "Qual é o resultado de 17 // 5 em Python?", "options": ["3", "3.4", "2", "5"], "correct": 0}],
  },
  {
    "order": 8,
    "slug": "if-else",
    "title": "if / else",
    "chapter": "Capítulo 2: Controle de Fluxo",
    "theory": "O `if` permite que seu programa tome **decisões** baseadas em condições.\n\n## Como funciona\n\n```python\nidade = 18\n\nif idade >= 18:\n    print('Adulto')\nelse:\n    print('Menor de idade')\n```\n\n```\n# Adulto\n```\n\n1. O Python avalia a condição — ex: `idade >= 18`\n2. Se for **verdadeira**, executa o bloco do `if`\n3. Se for **falsa**, executa o bloco do `else`\n\n## Como digitar os símbolos de comparação\n\n- **Igual** → `==` (dois sinais de igual)\n- **Diferente** → `!=`\n- **Maior ou igual** → `>=` (sem espaço entre os dois caracteres)\n- **Menor ou igual** → `<=`\n\n## Indentação é obrigatória!\n\nO código dentro do `if` e `else` precisa ter **4 espaços** no início:\n\n```python\nif idade >= 18:\n    print('Adulto')  # 4 espaços — está DENTRO do if\nprint('Fim')         # sem espaço — está FORA do if\n```\n\n## No exercício\n\nLeia uma idade com `input()`, imprima `Adulto` se for maior ou igual a 18, ou `Menor de idade` caso contrário.",
    "instruction_pt": "Escreva um programa que leia uma idade e imprima `Adulto` se for maior ou igual a 18, ou `Menor de idade` caso contrário.\n\nExemplos:\n- Entrada: `20` → Saída: `Adulto`\n- Entrada: `15` → Saída: `Menor de idade`",
    "instruction_en": "Read age with input(), print \"Adulto\" if >=18 else \"Menor de idade\".",
    "instruction_es": "Lee la edad con input(), imprime \"Adulto\" si >=18 o \"Menor de idade\".",
    "starter_code": "idade = int(input())\n\n# Substitua os ___ pelos valores corretos\nif idade >= ___:\n    print('___')\nelse:\n    print('___')\n",
    "hint": "O `if` em Python usa dois-pontos no final da condição e o bloco dentro deve ter recuo (indentação) de 4 espaços — isso é como o Python sabe o que está 'dentro' do if. O `else:` fica no mesmo nível do `if`. Lembre de converter o valor do `input()` para inteiro com `int()`.",
    "hints": ["A condicao e `idade >= 18` -- use `>=` colado, sem espaco entre `>` e `=`.", "O texto dentro do `print` deve ser exatamente `'Adulto'` ou `'Menor de idade'` -- igual a saida esperada."],
    "tests": [{"stdin": "20", "expected_stdout": "Adulto"}, {"stdin": "15", "expected_stdout": "Menor de idade"}],
    "quiz": [{"question": "O comparador `>=` representa qual símbolo matemático?", "options": ["≠ (diferente)", "≤ (menor ou igual)", "= (igual)", "≥ (maior ou igual)"], "correct": 3}, {"question": "O bloco `else` executa em qual situação?", "options": ["Sempre, independente da condição", "Quando a condição do `if` é falsa", "Antes do `if`", "Quando há erro no código"], "correct": 1}, {"question": "Por que usamos `int(input())` ao ler uma idade?", "options": ["Para formatar o texto", "Para tornar a leitura mais rápida", "Porque `input()` retorna texto e precisamos de número inteiro", "Porque `int()` é obrigatório com `input()`"], "correct": 2}],
  },
  {
    "order": 9,
    "slug": "python-zero-comparadores",
    "title": "Comparadores",
    "chapter": "Capítulo 2: Controle de Fluxo",
    "theory": "Comparadores verificam a relação entre dois valores e retornam **`True`** (verdadeiro) ou **`False`** (falso).\n\n## Como funciona\n\n```python\nprint(10 == 10)\nprint(10 != 5)\nprint(10 > 5)\nprint(10 < 5)\nprint(10 >= 10)\nprint(10 <= 9)\n```\n\n```\n# True\n# True\n# True\n# False\n# True\n# False\n```\n\n## Cuidado: espaço estraga o comparador!\n\n```python\nif nota >= 7:   # certo — colado, sem espaço\nif nota > = 7:  # errado — espaço entre > e =\n```\n\n## Diferença entre = e ==\n\n- `=` **guarda** um valor na variável: `idade = 15`\n- `==` **compara** dois valores: `idade == 15`\n\n## No exercício\n\nCom `a = 10` e `b = 5`, use os comparadores para imprimir `True`, `False` e `True`.",
    "instruction_pt": "Com `a = 10` e `b = 5`, complete o código para imprimir `True`, `False` e `True`.\n\nVeja um exemplo diferente:\n\n```python\nx = 7\ny = 3\nprint(x > y)   # True\nprint(x == y)  # False\nprint(x != y)  # True\n```",
    "instruction_en": "Use comparison operators ==, > and != with a=10 and b=5 to print True, False, True.",
    "instruction_es": "Usa los operadores ==, > y != con a=10 y b=5 para imprimir True, False, True.",
    "starter_code": "a = 10\nb = 5\n\nprint(a ___ b)   # deve imprimir True\nprint(a ___ b)   # deve imprimir False\nprint(a ___ b)   # deve imprimir True\n",
    "hint": "Pensa no significado de cada operador: `>` compara se o lado esquerdo é maior, `==` verifica se os dois lados são iguais, e `!=` verifica se eles são diferentes.",
    "hints": ["Para `True` com a=10 e b=5: `a > b` (10 e maior que 5).", "Para `False`: `a == b` (10 nao e igual a 5). Para o ultimo `True`: `a != b` (sao diferentes)."],
    "tests": [{"stdin": "", "expected_stdout": "True\nFalse\nTrue"}],
    "quiz": [{"question": "O comparador `==` representa qual símbolo matemático?", "options": ["≠ (diferente)", "= (igual)", "≥ (maior ou igual)", "> (maior)"], "correct": 1}, {"question": "O comparador `!=` representa qual símbolo matemático?", "options": ["= (igual)", "≥ (maior ou igual)", "≠ (diferente)", "≤ (menor ou igual)"], "correct": 2}, {"question": "O comparador `>=` representa qual símbolo matemático?", "options": ["≤ (menor ou igual)", "> (maior)", "= (igual)", "≥ (maior ou igual)"], "correct": 3}],
  },
  {
    "order": 10,
    "slug": "python-zero-elif",
    "title": "Múltiplas condições com elif",
    "chapter": "Capítulo 2: Controle de Fluxo",
    "theory": "Quando temos mais de duas possibilidades, usamos `elif` (abreviação de else if).\n\n## Como funciona\n\n```python\nnota = float(input())\n\nif nota >= 7:\n    print('Aprovado')\nelif nota >= 5:\n    print('Recuperação')\nelse:\n    print('Reprovado')\n```\n\n```\n# Aprovado   (para nota 8)\n# Recuperação (para nota 6)\n# Reprovado  (para nota 3)\n```\n\nO Python verifica as condições **em ordem** e executa apenas o primeiro bloco verdadeiro.\n\n## A ordem das condições importa!\n\nSempre coloque as condições mais específicas primeiro (do maior para o menor):\n\n```python\nif nota >= 7:    # mais específico primeiro\n    print('Aprovado')\nelif nota >= 5:\n    print('Recuperação')\nelse:\n    print('Reprovado')\n```\n\n## No exercício\n\nCrie um sistema de notas: Aprovado (>= 7), Recuperação (>= 5) ou Reprovado (< 5).",
    "instruction_pt": "Use `if`, `elif` e `else` para criar um sistema de notas. Dado uma nota, o programa deve imprimir:\n- `Aprovado` se a nota for maior ou igual a `7`\n- `Recuperacao` se a nota for maior ou igual a `5` e menor que `7`\n- `Reprovado` se a nota for menor que `5`\n\nVeja como funciona:\n\n```python\nnota = float(input())\nif nota >= 7:\n    print('Aprovado')\nelif nota >= 5:\n    print('Recuperacao')\nelse:\n    print('Reprovado')\n```",
    "instruction_en": "Use if/elif/else to print Aprovado (>=7), Recuperacao (>=5) or Reprovado (<5) based on user input.",
    "instruction_es": "Usa if/elif/else para imprimir Aprovado (>=7), Recuperacao (>=5) o Reprovado (<5) segun la nota.",
    "starter_code": "nota = float(input())\n\n# Substitua ___ pelos numeros corretos\nif nota >= ___:\n    print('Aprovado')\nelif nota >= ___:\n    print('Recuperação')\nelse:\n    print('Reprovado')\n",
    "hint": "Use `float()` em vez de `int()` para aceitar notas com decimais, como `6.5`.\n\nA ordem das condições importa! Verifique primeiro se a nota é >= 7 (Aprovado), depois se é >= 5 (Recuperação).",
    "hints": ["Troque o primeiro `___` por `7` (condicao de aprovado) e o segundo `___` por `5` (recuperacao).", "A ordem importa: verifique `>= 7` primeiro. Se colocar `>= 5` antes, notas 7+ entrariam em Recuperacao."],
    "tests": [{"stdin": "8", "expected_stdout": "Aprovado"}, {"stdin": "6", "expected_stdout": "Recuperação"}, {"stdin": "3", "expected_stdout": "Reprovado"}],
    "quiz": [{"question": "O que elif significa em Python?", "options": ["end if — encerra o bloco", "else if — nova condição quando a anterior é falsa", "error if — trata erros", "eval if — avalia expressão"], "correct": 1}, {"question": "Quantos elif podemos ter em uma cadeia if/elif/else?", "options": ["Apenas 1", "No máximo 3", "Quantos forem necessários", "Nenhum — elif não existe"], "correct": 2}],
  },
  {
    "order": 11,
    "slug": "python-zero-for",
    "title": "Repetindo com for",
    "chapter": "Capítulo 2: Controle de Fluxo",
    "theory": "O loop `for` repete um bloco de código um número fixo de vezes.\n\n## Como funciona\n\n```python\nfor i in range(1, 4):\n    print(f\"3 x {i} = {3 * i}\")\n```\n\n```\n# 3 x 1 = 3\n# 3 x 2 = 6\n# 3 x 3 = 9\n```\n\nO `i` assume cada valor do range a cada repetição: primeiro 1, depois 2, até 3.\n\n## range(inicio, fim)\n\n- `range(1, 6)` gera os números **1, 2, 3, 4, 5**\n- O segundo valor não é incluído — `range(1, 6)` vai até 5, não até 6\n\n## No exercício\n\nComplete o loop para imprimir a tabuada do 5 de 1 a 5:\n\n```python\nfor i in range(1, 6):\n    print(f\"5 x {i} = {5 * i}\")\n```\n\n```\n# 5 x 1 = 5\n# 5 x 2 = 10\n# 5 x 3 = 15\n# 5 x 4 = 20\n# 5 x 5 = 25\n```",
    "instruction_pt": "Complete o loop `for` para imprimir a **tabuada do 5** de 1 a 5.\n\nO programa deve imprimir exatamente:\n- `5 x 1 = 5`\n- `5 x 2 = 10`\n- ... ate `5 x 5 = 25`\n\nVeja um exemplo com a tabuada do 2:\n\n```python\nfor i in range(1, 3):\n    print(f\"2 x {i} = {2 * i}\")\n```",
    "instruction_en": "Complete the for loop with range() to print the 5 times table from 1 to 5.",
    "instruction_es": "Completa el bucle for con range() para imprimir la tabla del 5 del 1 al 5.",
    "starter_code": "# Complete os valores do range e o calculo dentro da f-string\nfor i in range(___, ___):\n    print(f\"5 x {i} = {5 * i}\")\n",
    "hint": "`range(inicio, fim)` gera numeros de `inicio` ate `fim - 1`. Para ir de 1 a 5, use `range(1, 6)` — porque o ultimo numero nao e incluido!\n\nO calculo `5 * i` dentro da f-string ja esta pronto — so preencha os valores do range.",
    "hints": ["O range deve comecar em `1` e terminar em `6` (o ultimo valor nao e incluido): `range(1, 6)`.", "O calculo `5 * i` ja esta pronto dentro da f-string -- so complete os dois valores do `range`."],
    "tests": [{"stdin": "", "expected_stdout": "5 x 1 = 5\n5 x 2 = 10\n5 x 3 = 15\n5 x 4 = 20\n5 x 5 = 25"}],
    "quiz": [{"question": "O que range(1, 6) gera em Python?", "options": ["1, 2, 3, 4, 5, 6", "1, 2, 3, 4, 5", "0, 1, 2, 3, 4, 5", "2, 3, 4, 5, 6"], "correct": 1}, {"question": "Quantas vezes \"for i in range(4)\" executa?", "options": ["5 vezes", "3 vezes", "4 vezes", "1 vez"], "correct": 2}],
  },
  {
    "order": 12,
    "slug": "python-zero-listas",
    "title": "Listas",
    "chapter": "Capítulo 2: Controle de Fluxo",
    "theory": "Uma lista guarda vários valores em uma única variável, usando colchetes `[]`.\n\n## Como funciona\n\n```python\nfrutas = [\"maçã\", \"banana\", \"uva\"]\nfor fruta in frutas:\n    print(fruta)\nprint(f\"Total: {len(frutas)}\")\n```\n\n```\n# maçã\n# banana\n# uva\n# Total: 3\n```\n\n## Criando uma lista\n\nColoque os valores dentro de `[]` separados por vírgula:\n\n```python\nfrutas = [\"maçã\", \"banana\", \"uva\"]\nnumeros = [10, 20, 30]\n```\n\n## Contando itens com len()\n\n```python\nprint(len(frutas))\n```\n\n```\n# 3\n```\n\n## No exercício\n\nCrie uma lista com 3 frutas, imprima cada uma com `for` e mostre o total com `len()`.",
    "instruction_pt": "Crie uma lista com 3 frutas, imprima cada fruta com `for` e mostre o total de itens com `len()`.\n\nVeja um exemplo com cores:\n\n```python\ncores = [\"azul\", \"verde\", \"amarelo\"]\nfor cor in cores:\n    print(cor)\nprint(f\"Total: {len(cores)}\")\n```",
    "instruction_en": "Create a list with 3 fruits, print each item with a for loop, then print the total using len().",
    "instruction_es": "Crea una lista con 3 frutas, imprime cada item con un for y luego imprime el total con len().",
    "starter_code": "frutas = [___, ___, ___]\n\nfor fruta in frutas:\n    print(___)\n\nprint(f\"Total: {___}\")\n",
    "hint": "Listas em Python usam colchetes `[]` e os itens ficam separados por vírgulas. Textos precisam estar entre aspas: `[\"maçã\", \"banana\", \"uva\"]`.\n\nA função `len()` retorna o número de itens de uma lista. Por exemplo, `len([\"a\", \"b\"])` retorna `2`.",
    "hints": ["Preencha a lista com 3 frutas entre aspas: `[\"maca\", \"banana\", \"uva\"]`.", "No `for`, a variavel do loop e `fruta`. No total, use `len(frutas)` dentro da f-string."],
    "tests": [{"stdin": "", "expected_stdout": "maçã\nbanana\nuva\nTotal: 3"}],
    "quiz": [{"question": "Qual é o índice do primeiro elemento de uma lista Python?", "options": ["1", "0", "-1", "Depende da lista"], "correct": 1}, {"question": "Qual função retorna o número de itens de uma lista?", "options": ["size()", "count()", "len()", "length()"], "correct": 2}],
  },
  {
    "order": 13,
    "slug": "while",
    "title": "Loop while",
    "chapter": "Capítulo 2: Controle de Fluxo",
    "theory": "O `while` repete um bloco de código **enquanto** uma condição for verdadeira. Quando a condição vira falsa, o loop para.\n\n## Como funciona\n\n```python\ni = 1\nwhile i <= 5:\n    print(i)\n    i += 1\n```\n\n```\n# 1\n# 2\n# 3\n# 4\n# 5\n```\n\n- `i = 1` — valor inicial\n- `while i <= 5` — continua enquanto i for menor ou igual a 5\n- `i += 1` — aumenta i em 1 a cada repetição (sem isso, loop infinito!)\n\n## Cuidado: loop infinito!\n\nSe você esquecer de atualizar a variável, o loop nunca para.\n\n## No exercício\n\nO starter code tem um **erro proposital** na condição do `while`. Você vai identificar e corrigir para que o programa imprima de 1 a 5.",
    "instruction_pt": "O codigo abaixo tem um **erro proposital** — a condicao do `while` esta errada e o loop nao executa.\n\nEncontre e corrija o erro para que o programa imprima os numeros de 1 a 5, um por linha.\n\nVeja como deve ser o resultado:\n\n```python\ni = 1\nwhile i <= 5:\n    print(i)\n    i += 1\n# 1  2  3  4  5  (cada um em uma linha)\n```",
    "instruction_en": "Fix the broken while condition so it prints 1 to 5, each on a new line.",
    "instruction_es": "Corrige la condición del while roto para que imprima del 1 al 5, uno por línea.",
    "starter_code": "i = 1\n\n# Este loop tem um erro — corrija a condição para ele imprimir de 1 a 5\nwhile i > 10:  # ← condição errada\n    print(i)\n    i += 1\n",
    "hint": "Pensa assim: o loop deve rodar enquanto `i` ainda não passou de 5. Qual sinal de comparação faz isso? Lembre que `>` significa 'maior que' e `<=` significa 'menor ou igual a'.",
    "hints": ["A condicao `i > 10` nunca e verdadeira quando `i = 1`, entao o loop nao executa. Troque `>` por `<=`.", "O loop deve rodar **enquanto** `i` for menor ou igual a 5: `while i <= 5:`"],
    "tests": [{"stdin": "", "expected_stdout": "1\n2\n3\n4\n5"}],
    "quiz": [{"question": "Quando um loop while para de executar?", "options": ["Após 100 iterações", "Quando a condição se torna False", "Após 1 segundo", "Quando return é chamado"], "correct": 1}, {"question": "O que é um loop infinito?", "options": ["Um loop que executa exatamente 1000 vezes", "Um loop cuja condição nunca se torna False", "Um loop com range(infinity)", "Um loop aninhado"], "correct": 1}],
  },
  {
    "order": 14,
    "slug": "python-zero-funcoes",
    "title": "Funções",
    "chapter": "Capítulo 3: Funções",
    "theory": "Uma **função** é um bloco de código que você escreve uma vez e pode usar quantas vezes quiser — como uma receita que você salva e repete sempre que precisar.\n\n## Criando uma função com def\n\n```python\ndef saudar(nome):\n    return f\"Olá, {nome}!\"\n```\n\n- `def` — palavra que inicia a definição da função\n- `saudar` — nome da função (você escolhe)\n- `nome` — parâmetro: o valor que a função recebe\n- `return` — devolve o resultado para quem chamou\n\n## Usando (chamando) a função\n\n```python\ndef saudar(nome):\n    return f\"Olá, {nome}!\"\n\nprint(saudar(\"Carlos\"))  # Olá, Carlos!\nprint(saudar(\"Maria\"))   # Olá, Maria!\n```\n\nPerceba: escrevemos a função uma vez, mas podemos usá-la com qualquer nome!\n\n## return vs print\n\n```python\n# return devolve o valor — quem chamou decide o que fazer\ndef dobrar(n):\n    return n * 2\n\nresultado = dobrar(5)    # guarda o resultado\nprint(resultado)         # agora imprime: 10\nprint(dobrar(3))         # ou imprime direto: 6\n```\n\n## No exercício\n\nVocê vai completar uma função chamada `saudacao(nome)` que recebe um nome e retorna `\"Olá, {nome}!\"`.",
    "instruction_pt": "Complete os dois `___` no codigo para criar a funcao `saudacao(nome)`.\n\n**Exemplo de como funciona:**\n```python\ndef saudar(nome):\n    return f\"Ola, {nome}!\"\n\nprint(saudar(\"Ana\"))  # Ola, Ana!\n```",
    "instruction_en": "Create a function saudacao(nome) that returns \"Olá, {nome}!\".",
    "instruction_es": "Crea una función saudacao(nome) que retorne \"Olá, {nome}!\".",
    "starter_code": "def saudacao(___):\n    return ___\n\nprint(saudacao(\"Ana\"))\n",
    "hint": "",
    "hints": ["A palavra `def` define a função. Dentro dos parênteses coloque o nome do parâmetro — aqui é `nome`.", "Use uma f-string para montar a mensagem: `return f\"Olá, {nome}!\"` — lembre das chaves em volta de `nome`."],
    "tests": [{"stdin": "", "expected_stdout": "Olá, Ana!"}],
    "quiz": [{"question": "Qual palavra-chave define uma função em Python?", "options": ["function", "def", "func", "fn"], "correct": 1}, {"question": "O que return faz dentro de uma função?", "options": ["Imprime o resultado na tela", "Devolve um valor e encerra a função", "Chama outra função", "Reinicia a função"], "correct": 1}],
  },
  {
    "order": 15,
    "slug": "python-zero-parametros",
    "title": "Parâmetros e argumentos",
    "chapter": "Capítulo 3: Funções",
    "theory": "**Parâmetro** é o nome que você coloca na definição da função. **Argumento** é o valor que você passa quando chama a função.\n\n## Como funciona\n\n```python\ndef saudar(nome):         # nome é o parâmetro\n    print(f\"Olá, {nome}!\")\n\nsaudar(\"Fernanda\")        # \"Fernanda\" é o argumento\n```\n\n```\n# Olá, Fernanda!\n```\n\n## Múltiplos parâmetros\n\n```python\ndef calcular_imc(peso, altura):\n    imc = peso / (altura ** 2)\n    return round(imc, 1)\n\nprint(calcular_imc(70, 1.75))\n```\n\n```\n# 22.9\n```\n\n## No exercício\n\nCrie a função `calcular_area(base, altura)` que retorna `base * altura / 2` (área de um triângulo).",
    "instruction_pt": "Crie a função `calcular_area(base, altura)` que retorna a área de um triângulo (`base * altura / 2`).\n\nVeja como deve funcionar:\n\n```python\nprint(calcular_area(10, 5))  # deve imprimir: 25.0\nprint(calcular_area(6, 4))   # deve imprimir: 12.0\n```",
    "instruction_en": "Create calcular_area(base, altura) that returns base * altura / 2.",
    "instruction_es": "Crea calcular_area(base, altura) que retorna base * altura / 2.",
    "starter_code": "def calcular_area(___, ___):\n    return ___ * ___ / 2\n\nprint(calcular_area(10, 5))\nprint(calcular_area(6, 4))\n",
    "hint": "",
    "hints": ["Coloque os dois parâmetros separados por vírgula: `def calcular_area(base, altura):`.", "No corpo da função, substitua os `___` pelos nomes dos parâmetros: `return base * altura / 2`."],
    "tests": [{"stdin": "", "expected_stdout": "25.0\n12.0"}],
    "quiz": [{"question": "Qual é a diferença entre parâmetro e argumento?", "options": ["São a mesma coisa", "Parâmetro está na definição; argumento é o valor passado na chamada", "Argumento está na definição; parâmetro é o valor passado", "Parâmetro só existe em funções recursivas"], "correct": 1}, {"question": "Uma função pode ter mais de um parâmetro?", "options": ["Não, apenas um", "Sim, separados por vírgula", "Sim, mas apenas dois", "Depende do tipo de dado"], "correct": 1}],
  },
  {
    "order": 16,
    "slug": "python-zero-listas-avancado",
    "title": "Listas avançadas",
    "chapter": "Capítulo 3: Funções",
    "theory": "Uma **lista** em Python pode crescer e encolher durante a execução — você pode adicionar e remover itens usando métodos embutidos.\n\n## Adicionando com `append()`\n\n```python\nlista = [\"Ana\", \"Bruno\"]\nlista.append(\"Carlos\")   # adiciona ao final\nprint(lista)              # ['Ana', 'Bruno', 'Carlos']\n```\n\n- `append(valor)` — insere `valor` no **final** da lista\n- A lista original é **modificada** (não precisa reatribuir)\n\n## Removendo com `remove()`\n\n```python\nlista = [\"Ana\", \"Bruno\", \"Carlos\"]\nlista.remove(\"Bruno\")    # remove a primeira ocorrência\nprint(lista)              # ['Ana', 'Carlos']\n```\n\n- `remove(valor)` — apaga a **primeira ocorrência** do valor\n- Se o valor não existir, Python levanta um erro\n\n## Contando com `len()`\n\n```python\nlista = [\"Ana\", \"Carlos\"]\nprint(len(lista))   # 2\n```\n\n- `len(lista)` retorna o número de itens — funciona com qualquer lista\n\n## Exemplo completo\n\n```python\nconvidados = [\"Ana\", \"Bruno\"]\nconvidados.append(\"Carlos\")   # → [\"Ana\", \"Bruno\", \"Carlos\"]\nconvidados.remove(\"Bruno\")    # → [\"Ana\", \"Carlos\"]\n\nfor convidado in convidados:\n    print(convidado)\n\nprint(f\"Total: {len(convidados)}\")\n```\n\n```\nAna\nCarlos\nTotal: 2\n```\n\n## No exercício\n\nVocê vai partir de `[\"Ana\", \"Bruno\"]`, adicionar `\"Carlos\"` com `append`, remover `\"Bruno\"` com `remove` e imprimir cada nome e o total de convidados.",
    "instruction_pt": "Comece com `[\"Ana\", \"Bruno\"]`, adicione `\"Carlos\"` com `append`, remova `\"Bruno\"` com `remove`, depois imprima cada nome e o total.\n\nSaída esperada:\n```\nAna\nCarlos\nTotal: 2\n```",
    "instruction_en": "Manage a guest list using append, remove, len and a for loop.",
    "instruction_es": "Gestiona una lista de invitados usando append, remove, len y for.",
    "starter_code": "convidados = [\"Ana\", \"Bruno\"]\n\nconvidados.___(___)\nconvidados.___(___)\n\nfor convidado in convidados:\n    print(___)\n\nprint(f\"Total: {___}\")\n",
    "hint": "",
    "hints": ["Use `convidados.append(\"Carlos\")` para adicionar e `convidados.remove(\"Bruno\")` para remover.", "No `for`, imprima a variável do loop: `print(convidado)`. Para o total, use `len(convidados)` dentro da f-string."],
    "tests": [{"stdin": "", "expected_stdout": "Ana\nCarlos\nTotal: 2"}],
    "quiz": [{"question": "Qual método adiciona um item ao final de uma lista?", "options": ["add()", "insert()", "push()", "append()"], "correct": 3}, {"question": "O que lista.remove(\"Bruno\") faz?", "options": ["Remove todos os itens iguais a \"Bruno\"", "Remove a primeira ocorrência de \"Bruno\"", "Remove o último item da lista", "Apaga a lista inteira"], "correct": 1}],
  },
  {
    "order": 17,
    "slug": "python-zero-dicionarios",
    "title": "Dicionários",
    "chapter": "Capítulo 3: Funções",
    "theory": "Dicionarios guardam informacoes em pares **chave: valor** -- como uma ficha de cadastro onde cada campo tem um nome!\n\n## Como funciona\n\n```python\naluno = {\n    \"nome\": \"Beatriz\",\n    \"idade\": 14,\n    \"cidade\": \"Recife\"\n}\n\nprint(aluno[\"nome\"])    # Beatriz\nprint(aluno[\"cidade\"])  # Recife\n```\n\n## Criando e acessando\n\n- Chaves ficam entre `{}` com pares `\"chave\": valor` separados por virgula\n- Para acessar um valor: `dicionario[\"chave\"]` -- a chave **sempre entre aspas**\n\n```python\nproduto = {\"nome\": \"Notebook\", \"preco\": 2999}\nprint(produto[\"nome\"])   # Notebook\nprint(produto[\"preco\"])  # 2999\n```\n\n## Atualizando valores\n\n```python\naluno = {\"nome\": \"Ana\", \"nota\": 7.0}\naluno[\"nota\"] = 9.5   # atualiza o valor existente\nprint(aluno[\"nota\"])   # 9.5\n```\n\n## No exercicio\n\nCrie a ficha de um aluno com `nome`, `idade` e `nota`, depois imprima cada valor acessando pelas chaves.",
    "instruction_pt": "Crie o dicionário `aluno` com as chaves `nome`, `idade` e `nota`, depois imprima cada valor acessando pelas chaves.\n\nVeja um exemplo diferente:\n\n```python\nproduto = {\"nome\": \"Notebook\", \"preco\": 2999}\nprint(f\"Produto: {produto['nome']}\")\nprint(f\"Preco: {produto['preco']}\")\n```",
    "instruction_en": "Create a student dict with name, age and grade, then print each value.",
    "instruction_es": "Crea un diccionario de alumno con nombre, edad y nota, luego imprime cada valor.",
    "starter_code": "aluno = {\n    \"nome\": ___,\n    \"idade\": ___,\n    \"nota\": ___\n}\n\nprint(f\"Nome: {aluno[___]}\")\nprint(f\"Idade: {aluno[___]}\")\nprint(f\"Nota: {aluno[___]}\")\n",
    "hint": "",
    "hints": ["Preencha os valores do dicionário: `\"Carlos\"` para nome, `15` para idade, `8.5` para nota. Strings precisam de aspas, números não.", "Para acessar um valor, use o nome da chave entre aspas e colchetes: `aluno[\"nome\"]`. Substitua os `___` nos prints."],
    "tests": [{"stdin": "", "expected_stdout": "Nome: Carlos\nIdade: 15\nNota: 8.5"}],
    "quiz": [{"question": "Como acessar o valor da chave \"nome\" em um dicionário aluno?", "options": ["aluno.nome", "aluno[\"nome\"]", "aluno->nome", "aluno.get_nome()"], "correct": 1}, {"question": "O que um dicionário Python armazena?", "options": ["Apenas valores numéricos", "Pares de chave: valor", "Listas ordenadas", "Apenas strings"], "correct": 1}, {"question": "Como verificar se \"idade\" é uma chave no dicionário d?", "options": ["\"idade\" in d", "d.has(\"idade\")", "d.exists(\"idade\")", "check(d, \"idade\")"], "correct": 0}],
  },
  {
    "order": 18,
    "slug": "python-zero-strings",
    "title": "Manipulando texto",
    "chapter": "Capítulo 3: Funções",
    "theory": "Strings têm métodos incríveis para transformar texto do jeito que você precisar.\n\n## Como funciona\n\n```python\nnome = \"  Gabriela  \"\nprint(nome.strip())\nprint(nome.upper())\nprint(nome.lower())\n```\n\n```\n# Gabriela\n#   GABRIELA  \n#   gabriela  \n```\n\n## Substituindo texto\n\n```python\nfrase = \"Python é difícil\"\nprint(frase.replace(\"difícil\", \"incrível\"))\n```\n\n```\n# Python é incrível\n```\n\n## No exercício\n\nLeia um nome com `input()`, depois imprima em maiúsculas, em minúsculas e o número de caracteres.",
    "instruction_pt": "Leia um nome com `input()` e imprima o nome em maiúsculas, em minúsculas e o número de caracteres.\n\nVeja como deve funcionar:\n\n```python\n# Entrada: ana\nprint(nome.upper())  # ANA\nprint(nome.lower())  # ana\nprint(len(nome))     # 3\n```",
    "instruction_en": "Read a name with input() and print it in uppercase, lowercase and its length.",
    "instruction_es": "Lee un nombre con input() e imprime en mayúsculas, minúsculas y su longitud.",
    "starter_code": "nome = input()\n\nprint(nome.___())\nprint(nome.___())\nprint(___)\n",
    "hint": "",
    "hints": ["Use `.upper()` para maiúsculas e `.lower()` para minúsculas: `nome.upper()` e `nome.lower()`.", "Para contar os caracteres, use `len(nome)` — a função `len()` funciona tanto em listas quanto em strings!"],
    "tests": [{"stdin": "ana", "expected_stdout": "ANA\nana\n3"}, {"stdin": "Carlos", "expected_stdout": "CARLOS\ncarlos\n6"}],
    "quiz": [{"question": "Qual método converte uma string para maiúsculas em Python?", "options": ["capitalize()", "toUpperCase()", "upper()", "uppercase()"], "correct": 2}, {"question": "O que o método strip() faz em uma string?", "options": ["Remove todos os espaços da string", "Remove espaços do início e do fim", "Divide a string em pedaços", "Substitui caracteres especiais"], "correct": 1}],
  },
  {
    "order": 19,
    "slug": "python-zero-projeto",
    "title": "Projeto final",
    "chapter": "Capítulo 3: Funções",
    "theory": "Chegou a hora de juntar tudo que você aprendeu! Neste projeto você vai criar um sistema de cadastro de alunos combinando:\n\n- `input()` — para ler dados do usuário\n- `float()` — para converter a nota\n- `if/elif/else` — para classificar o resultado\n- listas — para guardar os aprovados\n- `in` — para verificar se está na lista\n\n## Como funciona\n\n```python\naprovados = []\nnome = input()\nnota = float(input())\nif nota >= 7:\n    print(\"Aprovado\")\n    aprovados.append(nome)\nelif nota >= 5:\n    print(\"Recuperação\")\nelse:\n    print(\"Reprovado\")\nif nome in aprovados:\n    print(f\"{nome} está na lista de aprovados\")\nelse:\n    print(f\"{nome} não está na lista de aprovados\")\n```\n\n```\n# Aprovado\n# Carlos está na lista de aprovados\n```\n\n## No exercício\n\nComplete os `___` no starter code para que o programa funcione corretamente.",
    "instruction_pt": "Complete os `___` no starter code para criar um sistema de cadastro de alunos que:\n1. Lê nome e nota do aluno\n2. Imprime `Aprovado` (nota >= 7), `Recuperação` (>= 5) ou `Reprovado`\n3. Adiciona o nome à lista `aprovados` se aprovado\n4. Imprime se o aluno está ou não na lista\n\nExemplos:\n- Entrada: `Carlos`, `8` → `Aprovado` / `Carlos está na lista de aprovados`\n- Entrada: `Maria`, `6` → `Recuperação` / `Maria não está na lista de aprovados`",
    "instruction_en": "Build a student registration system combining input, if/elif, lists and functions.",
    "instruction_es": "Crea un sistema de registro de alumnos combinando input, if/elif, listas y funciones.",
    "starter_code": "aprovados = []\n\nnome = input()\nnota = float(input())\n\nif nota >= ___:\n    print(\"Aprovado\")\n    aprovados.___(___)\nelif nota >= ___:\n    print(\"Recuperação\")\nelse:\n    print(\"Reprovado\")\n\nif nome in aprovados:\n    print(f\"{___} está na lista de aprovados\")\nelse:\n    print(f\"{___} não está na lista de aprovados\")\n",
    "hint": "",
    "hints": ["Para a condição de aprovação use `nota >= 7` e para recuperação `nota >= 5`. A ordem das condições importa — verifique do maior para o menor!", "Para adicionar o nome à lista de aprovados use `aprovados.append(nome)`. Isso deve ficar dentro do bloco `if` de Aprovado.", "No último `if/else`, substitua os `___` pelo nome da variável `nome` para montar a mensagem correta."],
    "tests": [{"stdin": "Carlos\n8", "expected_stdout": "Aprovado\nCarlos está na lista de aprovados"}, {"stdin": "Maria\n6", "expected_stdout": "Recuperação\nMaria não está na lista de aprovados"}, {"stdin": "João\n3", "expected_stdout": "Reprovado\nJoão não está na lista de aprovados"}],
    "quiz": [{"question": "Qual estrutura verifica se um nome está dentro de uma lista?", "options": ["nome.in(lista)", "nome in lista", "lista.contains(nome)", "lista.find(nome)"], "correct": 1}, {"question": "Por que usamos float(input()) para ler a nota neste projeto?", "options": ["Para aceitar notas com decimais como 6.5", "Porque float é obrigatório com input()", "Para arredondar a nota automaticamente", "Para converter a nota em string"], "correct": 0}, {"question": "O que lista.append(nome) faz neste projeto?", "options": ["Verifica se o nome está na lista", "Remove o nome da lista", "Adiciona o nome ao final da lista de aprovados", "Imprime o nome na tela"], "correct": 2}],
  }
],
# ── JavaScript ────────────────────────────────────────────────────────────
"javascript": [
  {
    "order": 1,
    "slug": "js-console-log",
    "title": "console.log",
    "chapter": "Capítulo 1: Fundamentos",
    "theory": "`console.log()` é o `print()` do JavaScript — exibe qualquer valor no terminal.\n\n## Como funciona\n\n```javascript\nconsole.log(\"Olá, JavaScript!\");  // Olá, JavaScript!\nconsole.log(42);                  // 42\nconsole.log(true);                // true\n```\n\n- Passe qualquer valor entre os parênteses\n- Textos ficam entre aspas duplas `\"` ou simples `'`\n- Você pode exibir números e booleanos sem aspas\n\n## Múltiplos valores\n\n```javascript\nconsole.log(\"Versão:\", 2024);     // Versão: 2024\n```\n\n## No exercício\n\nExiba exatamente `Olá, JavaScript!` no console usando `console.log()`.",
    "instruction_pt": "Use `console.log()` para exibir `Olá, JavaScript!` no terminal.\n\nVeja um exemplo:\n\n```javascript\nconsole.log(\"Aprendendo JS!\");\n```",
    "instruction_en": "Use `console.log()` to display `Hello, JavaScript!` in the terminal.",
    "instruction_es": "Usa `console.log()` para mostrar `¡Hola, JavaScript!` en la terminal.",
    "starter_code": "// Exiba \"Olá, JavaScript!\" no console\n// escreva aqui\n",
    "hint": "Use: console.log(\"Olá, JavaScript!\")",
    "hints": [
      "`console.log()` em JS é como `print()` em Python — exibe no terminal.",
      "Solução: `console.log(\"Olá, JavaScript!\")` — não esqueça a exclamação!",
    ],
    "tests": [
      {
        "stdin": "",
        "expected_stdout": "Olá, JavaScript!",
      },
    ],
    "quiz": [
      {
        "question": "Como exibir texto no console em JavaScript?",
        "options": [
          "print('texto')",
          "echo('texto')",
          "console.log('texto')",
          "log('texto')",
        ],
        "correct": 2,
      },
      {
        "question": "console.log() é útil principalmente para:",
        "options": [
          "Criar interfaces gráficas",
          "Depurar código e exibir resultados",
          "Enviar e-mails",
          "Salvar arquivos",
        ],
        "correct": 1,
      },
    ],
  },
  {
    "order": 2,
    "slug": "js-variaveis",
    "title": "let e const",
    "chapter": "Capítulo 1: Fundamentos",
    "theory": "Em JavaScript, variáveis são criadas com `let` (pode mudar) ou `const` (valor fixo).\n\n## Como funciona\n\n```javascript\nconst linguagem = \"JavaScript\";  // não pode mudar\nlet versao = 2024;               // pode mudar\n\nversao = 2025;                   // ok!\n// linguagem = \"Python\";         // ERRO — const não aceita reatribuição\n```\n\n- Use `const` como padrão — só troque por `let` quando precisar reatribuir\n- Textos ficam entre aspas `\"texto\"`, números sem aspas `42`\n\n## Concatenando com +\n\n```javascript\nconst nome = \"Ana\";\nconst idade = 16;\nconsole.log(nome + \" tem \" + idade + \" anos\");  // Ana tem 16 anos\n```\n\n## No exercício\n\nUse as variáveis `cidade` e `populacao` já declaradas e concatene-as para exibir a frase pedida.",
    "instruction_pt": "As variáveis `cidade` e `populacao` já estão declaradas.\n\nComplete o `console.log()` usando concatenação (`+`) para exibir:\n`São Paulo tem 12000000 habitantes`\n\nVeja um exemplo com outras variaveis:\n\n```javascript\nconst pais = \"Brasil\";\nlet habitantes = 200000000;\nconsole.log(pais + \" tem \" + habitantes + \" habitantes\");\n```",
    "instruction_en": "Complete the console.log() to display: `São Paulo has 12000000 inhabitants`",
    "instruction_es": "Completa el console.log() para mostrar: `São Paulo tiene 12000000 habitantes`",
    "starter_code": "const cidade = \"São Paulo\";\nlet populacao = 12000000;\n// Exiba: São Paulo tem 12000000 habitantes\nconsole.log(___);\n",
    "hint": "Use: console.log(cidade + \" tem \" + populacao + \" habitantes\");",
    "hints": [
      "Concatene com `+`: `cidade + \" tem \" + populacao + \" habitantes\"`.",
      "Resultado esperado: `São Paulo tem 12000000 habitantes` — sem vírgulas extras.",
    ],
    "tests": [
      {
        "stdin": "",
        "expected_stdout": "São Paulo tem 12000000 habitantes",
      },
    ],
    "quiz": [
      {
        "question": "Qual palavra-chave usar para uma variável que nunca muda em JS?",
        "options": [
          "let",
          "var",
          "const",
          "static",
        ],
        "correct": 2,
      },
      {
        "question": "O que acontece se você tentar reatribuir uma const?",
        "options": [
          "Ela muda normalmente",
          "O programa ignora a linha",
          "Ocorre um erro TypeError",
          "Ela vira let automaticamente",
        ],
        "correct": 2,
      },
    ],
  },
  {
    "order": 3,
    "slug": "js-tipos-de-dados",
    "title": "Tipos de Dados",
    "chapter": "Capítulo 1: Fundamentos",
    "theory": "JavaScript tem tipos primitivos que definem como os dados são armazenados e operados. `typeof` revela o tipo de qualquer valor.\n\n## Como funciona\n\n```javascript\nconsole.log(typeof 42);          // number\nconsole.log(typeof \"JavaScript\");// string\nconsole.log(typeof true);        // boolean\nconsole.log(typeof undefined);   // undefined\n```\n\n- **number** — inteiros e decimais: `42`, `3.14`, `-7`\n- **string** — textos entre aspas: `\"Olá\"`, `'mundo'`\n- **boolean** — verdadeiro ou falso: `true`, `false`\n- **undefined** — variável declarada sem valor\n\n## Comparando tipos\n\n```javascript\nconsole.log(typeof 3.14);   // number — decimais também são number\nconsole.log(typeof \"42\");   // string — número entre aspas é texto!\n```\n\n## No exercício\n\nUse `typeof` para revelar o tipo de três valores diferentes.",
    "instruction_pt": "Use `console.log(typeof ...)` para exibir o tipo de cada valor:\n\n- `100` → `number`\n- `\"JavaScript\"` → `string`\n- `false` → `boolean`\n\nVeja um exemplo com outros valores:\n\n```javascript\nconsole.log(typeof 10);\nconsole.log(typeof \"Ola\");\nconsole.log(typeof true);\n```",
    "instruction_en": "Use `console.log(typeof ...)` to show the type of 100, \"JavaScript\", and false.",
    "instruction_es": "Usa `console.log(typeof ...)` para mostrar el tipo de 100, \"JavaScript\" y false.",
    "starter_code": "console.log(typeof ___);\nconsole.log(typeof ___);\nconsole.log(typeof ___);\n",
    "hint": "Preencha os ___ com: 100, \"JavaScript\" e false (nessa ordem).",
    "hints": [
      "Preencha os três `___` com os valores: `100`, `\"JavaScript\"` e `false`.",
      "Resultado esperado (uma por linha): `number`, `string`, `boolean`.",
    ],
    "tests": [
      {
        "stdin": "",
        "expected_stdout": "number\nstring\nboolean",
      },
    ],
    "quiz": [
      {
        "question": "Qual é o tipo de `3.14` em JavaScript?",
        "options": [
          "float",
          "double",
          "number",
          "decimal",
        ],
        "correct": 2,
      },
      {
        "question": "O que `typeof \"42\"` retorna?",
        "options": [
          "number",
          "string",
          "integer",
          "char",
        ],
        "correct": 1,
      },
      {
        "question": "Qual operador revela o tipo de um valor em JS?",
        "options": [
          "typecheck",
          "type()",
          "typeof",
          "getType",
        ],
        "correct": 2,
      },
    ],
  },
  {
    "order": 4,
    "slug": "js-operadores",
    "title": "Operadores",
    "chapter": "Capítulo 1: Fundamentos",
    "theory": "Operadores aritméticos em JavaScript funcionam como na matemática — com um bônus: `%` para resto e `**` para potência.\n\n## Como funciona\n\n```javascript\nconsole.log(10 + 3);   // 13  — soma\nconsole.log(10 - 3);   //  7  — subtração\nconsole.log(10 * 3);   // 30  — multiplicação\nconsole.log(10 / 4);   //  2.5 — divisão\nconsole.log(10 % 3);   //  1  — resto da divisão\nconsole.log(2 ** 8);   // 256 — potência\n```\n\n- O operador `%` retorna o **resto** da divisão inteira: `17 % 5` = 2 (porque 17 = 3×5 + **2**)\n- `**` é o operador de potência: `2 ** 10` = 1024\n\n## No exercício\n\nCalcule três operações e exiba cada resultado com `console.log()`.",
    "instruction_pt": "Exiba o resultado de três operações (uma por linha):\n\n- `20 + 8` → `28`\n- `7 * 6` → `42`\n- `17 % 5` → `2`\n\nVeja um exemplo com outros numeros:\n\n```javascript\nconsole.log(10 + 5);\nconsole.log(4 * 3);\nconsole.log(10 % 3);\n```",
    "instruction_en": "Display the result of: 20 + 8, 7 * 6, and 17 % 5.",
    "instruction_es": "Muestra el resultado de: 20 + 8, 7 * 6 y 17 % 5.",
    "starter_code": "console.log(___);\nconsole.log(___);\nconsole.log(___);\n",
    "hint": "Preencha com: 20 + 8, depois 7 * 6, depois 17 % 5.",
    "hints": [
      "Preencha cada `___` com a operação: `20 + 8`, `7 * 6` e `17 % 5`.",
      "`17 % 5` = 2 porque 17 = 3×5 + 2 — o `%` retorna o resto da divisão.",
    ],
    "tests": [
      {
        "stdin": "",
        "expected_stdout": "28\n42\n2",
      },
    ],
    "quiz": [
      {
        "question": "O que o operador `%` calcula em JavaScript?",
        "options": [
          "Porcentagem",
          "Resto da divisão",
          "Potência",
          "Divisão decimal",
        ],
        "correct": 1,
      },
      {
        "question": "Qual o resultado de `2 ** 3` em JavaScript?",
        "options": [
          "6",
          "5",
          "8",
          "9",
        ],
        "correct": 2,
      },
    ],
  },
  {
    "order": 5,
    "slug": "js-template-literals",
    "title": "Template Literals",
    "chapter": "Capítulo 1: Fundamentos",
    "theory": "Template literals usam **crase** (`) e permitem inserir variáveis com `${}` — muito mais limpo do que concatenar com `+`.\n\n## Como funciona\n\n```javascript\nconst nome = \"Ana\";\nconst idade = 16;\n\n// Com concatenação (verboso)\nconsole.log(nome + \" tem \" + idade + \" anos\");\n\n// Com template literal (limpo)\nconsole.log(`${nome} tem ${idade} anos`);\n// Ana tem 16 anos\n```\n\n- Use crase `` ` `` (não aspas) para abrir e fechar o template\n- Coloque qualquer expressão dentro de `${  }`\n\n## Expressões dentro de ${}\n\n```javascript\nconst preco = 50;\nconst qtd = 3;\nconsole.log(`Total: R$ ${preco * qtd}`);  // Total: R$ 150\n```\n\n## No exercício\n\nUse um template literal para exibir a frase com as variáveis `nome` e `nota`.",
    "instruction_pt": "Use um template literal (crase + `${}`) para exibir:\n\n`Carlos tirou 9.5 na prova`\n\nVeja um exemplo:\n\n```javascript\nconst fruta = \"maca\";\nconst preco = 3.5;\nconsole.log(`A ${fruta} custa ${preco} reais`);\n```",
    "instruction_en": "Use a template literal to display: `Carlos got 9.5 on the test`",
    "instruction_es": "Usa un template literal para mostrar: `Carlos sacó 9.5 en el examen`",
    "starter_code": "const nome = \"Carlos\";\nconst nota = 9.5;\n// Exiba: Carlos tirou 9.5 na prova\n// Use template literal com crase e ${}\nconsole.log(___)\n",
    "hint": "Use crase: console.log(`${nome} tirou ${nota} na prova`)",
    "hints": [
      "Abra com crase `` ` ``, insira as variáveis com `${}`: `` `${nome} tirou ${nota} na prova` ``",
      "Solução: `console.log(\\`${nome} tirou ${nota} na prova\\`)`",
    ],
    "tests": [
      {
        "stdin": "",
        "expected_stdout": "Carlos tirou 9.5 na prova",
      },
    ],
    "quiz": [
      {
        "question": "Qual caractere delimita um template literal em JS?",
        "options": [
          "Aspas duplas \"",
          "Aspas simples '",
          "Crase `",
          "Colchetes []",
        ],
        "correct": 2,
      },
      {
        "question": "Como inserir uma variável dentro de um template literal?",
        "options": [
          "%(variavel)",
          "${variavel}",
          "#{variavel}",
          "{{variavel}}",
        ],
        "correct": 1,
      },
      {
        "question": "O que `console.log(`Resultado: ${2 + 3}`)` exibe?",
        "options": [
          "Resultado: 2 + 3",
          "Resultado: ${2 + 3}",
          "Resultado: 5",
          "Erro de sintaxe",
        ],
        "correct": 2,
      },
    ],
  },
  {
    "order": 6,
    "slug": "js-comparadores",
    "title": "Comparadores",
    "chapter": "Capítulo 1: Fundamentos",
    "theory": "Comparadores retornam `true` ou `false`. Em JS, use sempre `===` (igualdade estrita) em vez de `==` — ela compara valor **e** tipo.\n\n## Como funciona\n\n```javascript\nconst a = 10;\nconst b = 5;\n\nconsole.log(a > b);    // true  — maior que\nconsole.log(a < b);    // false — menor que\nconsole.log(a === b);  // false — igual (valor e tipo)\nconsole.log(a !== b);  // true  — diferente\n```\n\n- `>` e `<` comparam grandeza\n- `>=` e `<=` incluem a igualdade\n- `===` e `!==` são os comparadores de igualdade recomendados em JS\n\n## Operadores lógicos\n\n```javascript\nconsole.log(10 > 5 && 3 > 1);  // true  — E (ambos verdadeiros)\nconsole.log(10 > 5 || 1 > 9);  // true  — OU (um basta)\nconsole.log(!(10 > 5));         // false — NÃO (inverte)\n```\n\n## No exercício\n\nCompare `a = 15` e `b = 8` e exiba três resultados booleanos.",
    "instruction_pt": "Com `a = 15` e `b = 8`, exiba (uma por linha):\n\n- `a > b` → `true`\n- `a === b` → `false`\n- `a !== b` → `true`\n\nVeja um exemplo com outros valores:\n\n```javascript\nconst x = 10;\nconst y = 10;\nconsole.log(x > y);   // false\nconsole.log(x === y); // true\nconsole.log(x !== y); // false\n```",
    "instruction_en": "With a = 15 and b = 8, display true, false, true using comparison operators.",
    "instruction_es": "Con a = 15 y b = 8, muestra true, false, true usando operadores de comparación.",
    "starter_code": "const a = 15;\nconst b = 8;\nconsole.log(___);\nconsole.log(___);\nconsole.log(___);\n",
    "hint": "Preencha com: a > b, depois a === b, depois a !== b.",
    "hints": [
      "Preencha cada `___` com: `a > b`, `a === b`, `a !== b` (nessa ordem).",
      "`===` compara valor **e tipo** — é diferente de `==`. Sempre use `===` em JS.",
    ],
    "tests": [
      {
        "stdin": "",
        "expected_stdout": "true\nfalse\ntrue",
      },
    ],
    "quiz": [
      {
        "question": "Por que usar `===` em vez de `==` em JavaScript?",
        "options": [
          "São idênticos",
          "`===` compara valor e tipo, evitando conversões inesperadas",
          "`==` é mais rápido",
          "`===` só funciona com números",
        ],
        "correct": 1,
      },
      {
        "question": "Qual o resultado de `5 !== \"5\"` em JavaScript?",
        "options": [
          "false",
          "true",
          "undefined",
          "Erro",
        ],
        "correct": 1,
      },
    ],
  },
  {
    "order": 7,
    "slug": "js-if-else",
    "title": "if / else",
    "chapter": "Capítulo 2: Controle de Fluxo",
    "theory": "`if/else` executa blocos diferentes dependendo de uma condição — é a tomada de decisão do código.\n\n## Como funciona\n\n```javascript\nconst temperatura = 35;\n\nif (temperatura > 30) {\n  console.log(\"Está quente!\");\n} else {\n  console.log(\"Temperatura agradável.\");\n}\n// Está quente!\n```\n\n- A condição fica entre `()` após o `if`\n- Cada bloco fica entre `{}`\n- O `else` é opcional — executa quando a condição é `false`\n\n## No exercício\n\nComplete a condição do `if` para verificar se `idade` é maior ou igual a 18.",
    "instruction_pt": "Complete a condição do `if` para verificar se `idade >= 18`.\n\n- Se sim: exiba `Maior de idade`\n- Se não: exiba `Menor de idade`\n\nVeja um exemplo:\n\n```javascript\nconst nota = 8;\nif (nota >= 7) {\n  console.log(\"Aprovado\");\n} else {\n  console.log(\"Reprovado\");\n}\n```",
    "instruction_en": "Complete the if condition to check if age >= 18.",
    "instruction_es": "Completa la condición del if para verificar si edad >= 18.",
    "starter_code": "const idade = 20;\n// Complete a condição\nif (___) {\n  console.log(\"Maior de idade\");\n} else {\n  console.log(\"Menor de idade\");\n}\n",
    "hint": "A condição é: idade >= 18",
    "hints": [
      "A condição vai entre os parênteses: `if (idade >= 18)`.",
      "Com `idade = 20`, a condição é verdadeira — o programa deve exibir `\"Maior de idade\"`.",
    ],
    "tests": [
      {
        "stdin": "",
        "expected_stdout": "Maior de idade",
      },
    ],
    "quiz": [
      {
        "question": "O que acontece quando a condição do `if` é false e não há `else`?",
        "options": [
          "O programa encerra",
          "O bloco if é ignorado e a execução continua",
          "Ocorre um erro",
          "O bloco if executa mesmo assim",
        ],
        "correct": 1,
      },
      {
        "question": "Qual a sintaxe correta de um if em JavaScript?",
        "options": [
          "if condicao:",
          "if (condicao) {}",
          "if [condicao] {}",
          "if <condicao> {}",
        ],
        "correct": 1,
      },
    ],
  },
  {
    "order": 8,
    "slug": "js-else-if",
    "title": "else if",
    "chapter": "Capítulo 2: Controle de Fluxo",
    "theory": "`else if` testa múltiplas condições em sequência — é o equivalente ao `elif` do Python.\n\n## Como funciona\n\n```javascript\nconst hora = 14;\n\nif (hora < 12) {\n  console.log(\"Bom dia!\");\n} else if (hora < 18) {\n  console.log(\"Boa tarde!\");\n} else {\n  console.log(\"Boa noite!\");\n}\n// Boa tarde!\n```\n\n- O JS testa cada condição de cima para baixo e executa **apenas o primeiro bloco verdadeiro**\n- A ordem importa: coloque as condições mais específicas primeiro\n\n## No exercício\n\nPreencha os dois valores nos `___` para criar um sistema de avaliação escolar.",
    "instruction_pt": "Preencha os dois `___` para que:\n\n- `nota >= 7` → `Aprovado`\n- `nota >= 5` → `Recuperacao`\n- Abaixo disso → `Reprovado`\n\nCom `nota = 7.5` o resultado deve ser `Aprovado`.\n\nVeja um exemplo com outros valores:\n\n```javascript\nconst idade = 16;\nif (idade >= 18) {\n  console.log(\"Adulto\");\n} else if (idade >= 13) {\n  console.log(\"Adolescente\");\n} else {\n  console.log(\"Crianca\");\n}\n```",
    "instruction_en": "Fill the two ___ so that nota >= 7 prints Aprovado, nota >= 5 prints Recuperacao.",
    "instruction_es": "Rellena los dos ___ para que nota >= 7 muestre Aprovado, nota >= 5 Recuperacao.",
    "starter_code": "const nota = 7.5;\nif (nota >= ___) {\n  console.log(\"Aprovado\");\n} else if (nota >= ___) {\n  console.log(\"Recuperacao\");\n} else {\n  console.log(\"Reprovado\");\n}\n",
    "hint": "Troque os ___ por 7 (aprovado) e 5 (recuperação).",
    "hints": [
      "Troque o primeiro `___` por `7` e o segundo por `5`.",
      "A ordem importa: verifique `>= 7` primeiro. Se colocar `>= 5` antes, notas 7+ entrariam em Recuperacao.",
    ],
    "tests": [
      {
        "stdin": "",
        "expected_stdout": "Aprovado",
      },
    ],
    "quiz": [
      {
        "question": "Se uma condição `if` for verdadeira, o que acontece com os `else if` seguintes?",
        "options": [
          "Todos são testados",
          "São ignorados",
          "Causam erro",
          "São executados também",
        ],
        "correct": 1,
      },
      {
        "question": "Quantos `else if` você pode encadear num mesmo bloco?",
        "options": [
          "No máximo 3",
          "No máximo 10",
          "Apenas 1",
          "Quantos quiser",
        ],
        "correct": 3,
      },
    ],
  },
  {
    "order": 9,
    "slug": "js-for",
    "title": "for loop",
    "chapter": "Capítulo 2: Controle de Fluxo",
    "theory": "O `for` repete um bloco um número determinado de vezes — perfeito quando você sabe quantas iterações precisa.\n\n## Como funciona\n\n```javascript\nfor (let i = 1; i <= 5; i++) {\n  console.log(`Passo ${i}`);\n}\n// Passo 1  Passo 2  Passo 3  Passo 4  Passo 5\n```\n\nO `for` tem três partes separadas por `;`:\n- **Início**: `let i = 1` — cria e inicializa o contador\n- **Condição**: `i <= 5` — enquanto isso for true, o loop continua\n- **Incremento**: `i++` — atualiza o contador a cada volta\n\n## Acumulando valores\n\n```javascript\nlet soma = 0;\nfor (let i = 1; i <= 4; i++) {\n  soma += i;\n}\nconsole.log(soma);  // 10 (1+2+3+4)\n```\n\n## No exercício\n\nComplete os dois `___` no `for` para exibir a tabuada do 4 de 1 a 5.",
    "instruction_pt": "Complete o `for` para exibir a **tabuada do 4**, do 1 ao 5 (veja a saída esperada abaixo).\n\nVeja um exemplo com a tabuada do 2:\n\n```javascript\nfor (let i = 1; i <= 3; i++) {\n  console.log(`2 x ${i} = ${2 * i}`);\n}\n```",
    "instruction_en": "Complete the for loop to display the multiplication table of 4 from 1 to 5.",
    "instruction_es": "Completa el bucle for para mostrar la tabla del 4 del 1 al 5.",
    "starter_code": "// Exiba a tabuada do 4 de 1 a 5\nfor (let i = ___; i <= ___; i++) {\n  console.log(`4 x ${i} = ${4 * i}`);\n}\n",
    "hint": "O loop começa em 1 e vai até 5: for (let i = 1; i <= 5; i++)",
    "hints": [
      "Troque os dois `___` por `1` e `5`: `for (let i = 1; i <= 5; i++)`.",
      "O `i++` já está pronto — ele aumenta `i` de 1 em 1 a cada volta do loop.",
    ],
    "tests": [
      {
        "stdin": "",
        "expected_stdout": "4 x 1 = 4\n4 x 2 = 8\n4 x 3 = 12\n4 x 4 = 16\n4 x 5 = 20",
      },
    ],
    "quiz": [
      {
        "question": "O que `i++` faz dentro de um for loop?",
        "options": [
          "Cria uma nova variável",
          "Incrementa i em 1 a cada volta",
          "Reinicia o loop",
          "Para o loop",
        ],
        "correct": 1,
      },
      {
        "question": "Quantas vezes o loop `for (let i = 0; i < 3; i++)` executa?",
        "options": [
          "2",
          "3",
          "4",
          "Infinitas",
        ],
        "correct": 1,
      },
    ],
  },
  {
    "order": 10,
    "slug": "js-while",
    "title": "while",
    "chapter": "Capítulo 2: Controle de Fluxo",
    "theory": "O `while` repete um bloco **enquanto** uma condição for verdadeira — ideal quando você não sabe quantas iterações serão necessárias.\n\n## Como funciona\n\n```javascript\nlet contador = 1;\n\nwhile (contador <= 3) {\n  console.log(contador);\n  contador++;\n}\n// 1  2  3\n```\n\n- A condição é verificada **antes** de cada volta\n- Se já começa `false`, o bloco nunca executa\n- **Cuidado**: esquecer de atualizar o contador cria um loop infinito!\n\n## for vs while\n\n```javascript\n// Use for quando sabe o número de repetições\nfor (let i = 1; i <= 5; i++) { ... }\n\n// Use while quando a condição é dinâmica\nwhile (saldo > 0) { ... }\n```\n\n## No exercício\n\nComplete a condição do `while` para exibir os números de 1 a 5.",
    "instruction_pt": "Complete o `___` na condição do `while` para exibir:\n\n`1`, `2`, `3`, `4`, `5` (cada número numa linha)\n\nVeja um exemplo:\n\n```javascript\nlet n = 1;\nwhile (n <= 3) {\n  console.log(n);\n  n++;\n}\n// 1  2  3\n```",
    "instruction_en": "Complete the while condition to display numbers 1 through 5.",
    "instruction_es": "Completa la condición del while para mostrar los números del 1 al 5.",
    "starter_code": "let i = 1;\nwhile (i ___ 5) {\n  console.log(i);\n  i++;\n}\n",
    "hint": "A condição deve ser `i <= 5` para incluir o 5.",
    "hints": [
      "Troque `___` por `<=` para que o loop inclua o número 5.",
      "Com `i > 5` o loop nunca executa (1 não é maior que 5). Use `<=`.",
    ],
    "tests": [
      {
        "stdin": "",
        "expected_stdout": "1\n2\n3\n4\n5",
      },
    ],
    "quiz": [
      {
        "question": "O que acontece se a condição do while nunca ficar false?",
        "options": [
          "O programa encerra normalmente",
          "O loop executa apenas uma vez",
          "Loop infinito — o programa trava",
          "JS lança um erro automaticamente",
        ],
        "correct": 2,
      },
      {
        "question": "Quando é preferível usar `while` em vez de `for`?",
        "options": [
          "Quando sabe o número exato de repetições",
          "Quando a condição de parada é dinâmica ou desconhecida",
          "Nunca, for é sempre melhor",
          "Apenas para loops de 1 a 10",
        ],
        "correct": 1,
      },
    ],
  },
  {
    "order": 11,
    "slug": "js-funcoes",
    "title": "Funções",
    "chapter": "Capítulo 3: Funções e Dados",
    "theory": "Funções são blocos de código reutilizáveis — você define uma vez e chama quantas vezes quiser.\n\n## Como funciona\n\n```javascript\nfunction saudacao(nome) {\n  return `Ola, ${nome}!`;\n}\n\nconsole.log(saudacao(\"Ana\"));    // Ola, Ana!\nconsole.log(saudacao(\"Carlos\")); // Ola, Carlos!\n```\n\n- `function` declara a função\n- O nome vem depois de `function`\n- `return` devolve o resultado para quem chamou\n- Sem `return`, a função retorna `undefined`\n\n## Função sem parâmetros\n\n```javascript\nfunction boasVindas() {\n  return \"Bem-vindo ao CodeFuturo!\";\n}\nconsole.log(boasVindas());  // Bem-vindo ao CodeFuturo!\n```\n\n## No exercício\n\nComplete o `return` da função `saudacao()` para que ela retorne `Ola, [nome]!`.",
    "instruction_pt": "Complete o `return` da função para que:\n\n- `saudacao(\"Ana\")` retorne `Ola, Ana!`\n- `saudacao(\"Carlos\")` retorne `Ola, Carlos!`\n\nVeja um exemplo com outra funcao:\n\n```javascript\nfunction dobro(x) {\n  return x * 2;\n}\nconsole.log(dobro(5));   // 10\nconsole.log(dobro(10));  // 20\n```",
    "instruction_en": "Complete the return statement so saudacao(\"Ana\") returns \"Ola, Ana!\"",
    "instruction_es": "Completa el return para que saudacao(\"Ana\") retorne \"Ola, Ana!\"",
    "starter_code": "function saudacao(nome) {\n  return ___;\n}\nconsole.log(saudacao(\"Ana\"));\nconsole.log(saudacao(\"Carlos\"));\n",
    "hint": "Use template literal: return `Ola, ${nome}!`",
    "hints": [
      "Use um template literal no return: `` return `Ola, ${nome}!`; ``",
      "O parâmetro `nome` já contém o valor passado na chamada — use `${nome}` para interpolá-lo.",
    ],
    "tests": [
      {
        "stdin": "",
        "expected_stdout": "Ola, Ana!\nOla, Carlos!",
      },
    ],
    "quiz": [
      {
        "question": "O que acontece se uma função não tem `return`?",
        "options": [
          "Erro de sintaxe",
          "Retorna 0",
          "Retorna undefined",
          "Retorna null",
        ],
        "correct": 2,
      },
      {
        "question": "Como chamar a função `calcular()` e exibir seu resultado?",
        "options": [
          "print(calcular())",
          "console.log calcular()",
          "console.log(calcular())",
          "call calcular()",
        ],
        "correct": 2,
      },
    ],
  },
  {
    "order": 12,
    "slug": "js-parametros",
    "title": "Parâmetros e Retorno",
    "chapter": "Capítulo 3: Funções e Dados",
    "theory": "Funções podem receber múltiplos parâmetros e devolver qualquer tipo de valor com `return`.\n\n## Como funciona\n\n```javascript\nfunction soma(a, b) {\n  return a + b;\n}\n\nconst resultado = soma(4, 6);\nconsole.log(resultado);  // 10\n```\n\n- Parâmetros são as variáveis listadas na definição: `(a, b)`\n- Argumentos são os valores passados na chamada: `soma(4, 6)`\n- O `return` pode devolver qualquer valor: número, string, boolean\n\n## Retornando boolean\n\n```javascript\nfunction ehPar(n) {\n  return n % 2 === 0;\n}\nconsole.log(ehPar(4));   // true\nconsole.log(ehPar(7));   // false\n```\n\n## No exercício\n\nComplete as duas funções: `calcularMedia(a, b, c)` e `ehAprovado(media)`.",
    "instruction_pt": "Complete as duas funções para que:\n\n- `calcularMedia(6, 8, 7)` retorne `7`\n- `ehAprovado(7)` retorne `true` (média >= 7 é aprovado)\n\nVeja um exemplo com outras funcoes:\n\n```javascript\nfunction area(largura, altura) {\n  return largura * altura;\n}\nfunction ehGrande(area) {\n  return area > 100;\n}\nconsole.log(area(10, 5));  // 50\nconsole.log(ehGrande(50)); // false\n```",
    "instruction_en": "Complete calcularMedia(6,8,7) returning 7 and ehAprovado(7) returning true.",
    "instruction_es": "Completa calcularMedia(6,8,7) que retorne 7 y ehAprovado(7) que retorne true.",
    "starter_code": "function calcularMedia(a, b, c) {\n  return ___;\n}\nfunction ehAprovado(media) {\n  return media ___ 7;\n}\nconsole.log(calcularMedia(6, 8, 7));\nconsole.log(ehAprovado(7));\n",
    "hint": "Media: (a + b + c) / 3. Aprovado: media >= 7.",
    "hints": [
      "Para a média: `return (a + b + c) / 3;` — (6+8+7)/3 = 7.",
      "Para aprovado: `return media >= 7;` — retorna true se a média for 7 ou mais.",
    ],
    "tests": [
      {
        "stdin": "",
        "expected_stdout": "7\ntrue",
      },
    ],
    "quiz": [
      {
        "question": "Qual a diferença entre parâmetro e argumento?",
        "options": [
          "São a mesma coisa",
          "Parâmetro é na definição; argumento é na chamada",
          "Argumento é na definição; parâmetro é na chamada",
          "Parâmetro é opcional; argumento obrigatório",
        ],
        "correct": 1,
      },
      {
        "question": "O que `return n % 2 === 0` devolve quando n = 5?",
        "options": [
          "1",
          "true",
          "false",
          "0",
        ],
        "correct": 2,
      },
    ],
  },
  {
    "order": 13,
    "slug": "js-arrays",
    "title": "Arrays",
    "chapter": "Capítulo 3: Funções e Dados",
    "theory": "Arrays armazenam listas de valores. Cada item tem um índice que começa em `0`.\n\n## Como funciona\n\n```javascript\nconst frutas = [\"maçã\", \"banana\", \"uva\"];\n\nconsole.log(frutas[0]);      // maçã    — primeiro\nconsole.log(frutas[2]);      // uva     — terceiro\nconsole.log(frutas.length);  // 3       — tamanho\n```\n\n- Índices começam em `0` — o último elemento está em `array.length - 1`\n- Arrays podem misturar tipos: `[1, \"dois\", true]`\n\n## Iterando com for...of\n\n```javascript\nconst cores = [\"azul\", \"verde\", \"vermelho\"];\nfor (const cor of cores) {\n  console.log(cor);\n}\n```\n\n## No exercício\n\nAcesse os índices corretos do array `cores` e exiba seu `length`.",
    "instruction_pt": "Com o array `cores = [\"vermelho\", \"verde\", \"azul\", \"amarelo\"]`, exiba (uma por linha):\n\n- O elemento no índice `0` → `vermelho`\n- O elemento no índice `2` → `azul`\n- O tamanho do array → `4`\n\nVeja um exemplo com outro array:\n\n```javascript\nconst numeros = [10, 20, 30, 40];\nconsole.log(numeros[0]);     // 10\nconsole.log(numeros[2]);     // 30\nconsole.log(numeros.length); // 4\n```",
    "instruction_en": "Display cores[0], cores[2], and cores.length.",
    "instruction_es": "Muestra cores[0], cores[2] y cores.length.",
    "starter_code": "const cores = [\"vermelho\", \"verde\", \"azul\", \"amarelo\"];\nconsole.log(cores[___]);\nconsole.log(cores[___]);\nconsole.log(cores.length);\n",
    "hint": "Preencha com os índices 0 e 2 (índices começam em zero).",
    "hints": [
      "Preencha os dois `___` com `0` e `2` para acessar `vermelho` e `azul`.",
      "`cores.length` já está pronto — retorna `4` (o número de elementos).",
    ],
    "tests": [
      {
        "stdin": "",
        "expected_stdout": "vermelho\nazul\n4",
      },
    ],
    "quiz": [
      {
        "question": "Qual o índice do primeiro elemento de um array em JS?",
        "options": [
          "1",
          "0",
          "-1",
          "Depende do array",
        ],
        "correct": 1,
      },
      {
        "question": "Como acessar o último elemento de `arr` sem saber o tamanho?",
        "options": [
          "arr[-1]",
          "arr.last()",
          "arr[arr.length - 1]",
          "arr.end()",
        ],
        "correct": 2,
      },
    ],
  },
  {
    "order": 14,
    "slug": "js-metodos-array",
    "title": "Métodos de Array",
    "chapter": "Capítulo 3: Funções e Dados",
    "theory": "Arrays têm métodos poderosos que facilitam manipular listas sem escrever loops manualmente.\n\n## Como funciona\n\n```javascript\nconst lista = [\"Ana\", \"Carlos\"];\n\nlista.push(\"Beatriz\");       // adiciona no final\nlista.pop();                 // remove o último\nlista.includes(\"Ana\");       // true — verifica presença\nconsole.log(lista.length);   // 2\n```\n\n- `push(valor)` — adiciona ao final, aumenta `length`\n- `pop()` — remove e retorna o último elemento\n- `includes(valor)` — retorna `true` ou `false`\n\n## Mais métodos úteis\n\n```javascript\nconst nums = [3, 1, 4, 1, 5];\nconsole.log(nums.indexOf(4));    // 2 — posição do elemento\nconsole.log(nums.join(\"-\"));     // 3-1-4-1-5 — une em string\nconsole.log(nums.reverse());     // [5, 1, 4, 1, 3]\n```\n\n## No exercício\n\nUse `push()`, `length` e `includes()` numa lista de convidados.",
    "instruction_pt": "Com `convidados = [\"Ana\", \"Carlos\", \"Beatriz\"]`, faça (na ordem):\n\n1. Adicione `\"Diego\"` com `push()`\n2. Exiba o `length` → `4`\n3. Exiba se `\"Carlos\"` está na lista → `true`\n4. Exiba se `\"Pedro\"` está na lista → `false`\n\nVeja um exemplo com outro array:\n\n```javascript\nconst frutas = [\"maca\", \"banana\"];\nfrutas.push(\"uva\");\nconsole.log(frutas.length);             // 3\nconsole.log(frutas.includes(\"banana\")); // true\nconsole.log(frutas.includes(\"pera\"));   // false\n```",
    "instruction_en": "Push Diego to the array, then display length, includes Carlos, includes Pedro.",
    "instruction_es": "Agrega Diego con push, luego muestra length, includes Carlos, includes Pedro.",
    "starter_code": "const convidados = [\"Ana\", \"Carlos\", \"Beatriz\"];\nconvidados.___(\"Diego\");\nconsole.log(convidados.___);\nconsole.log(convidados.includes(___));\nconsole.log(convidados.includes(___));\n",
    "hint": "Complete com `push`, `length` e `includes(...)`.",
    "hints": [
      "Use `push(\"Diego\")` para adicionar e `length` para exibir o tamanho da lista.",
      "Complete com `includes(\"Carlos\")` e `includes(\"Pedro\")` para verificar se cada nome está na lista.",
    ],
    "tests": [
      {
        "stdin": "",
        "expected_stdout": "4\ntrue\nfalse",
      },
    ],
    "quiz": [
      {
        "question": "O que `push()` faz em um array?",
        "options": [
          "Remove o primeiro elemento",
          "Remove o último elemento",
          "Adiciona um elemento ao final",
          "Inverte o array",
        ],
        "correct": 2,
      },
      {
        "question": "O que `includes()` retorna?",
        "options": [
          "O índice do elemento",
          "true ou false",
          "O elemento encontrado",
          "O tamanho do array",
        ],
        "correct": 1,
      },
    ],
  },
  {
    "order": 15,
    "slug": "js-objetos",
    "title": "Objetos",
    "chapter": "Capítulo 3: Funções e Dados",
    "theory": "Objetos armazenam pares **chave: valor** — como uma ficha de cadastro onde cada campo tem um nome.\n\n## Como funciona\n\n```javascript\nconst aluno = {\n  nome: \"Beatriz\",\n  idade: 14,\n  cidade: \"Recife\",\n};\n\nconsole.log(aluno.nome);    // Beatriz\nconsole.log(aluno.idade);   // 14\n```\n\n- Acesse propriedades com ponto `.` (notação de ponto)\n- Ou com colchetes: `aluno[\"nome\"]` (útil com chaves dinâmicas)\n\n## Adicionando e atualizando\n\n```javascript\naluno.nota = 9.5;         // adiciona nova propriedade\naluno.cidade = \"SP\";      // atualiza valor existente\n```\n\n## No exercício\n\nAcesse as propriedades corretas do objeto `produto` para exibir nome e preço.",
    "instruction_pt": "Com o objeto `produto` já declarado, complete os `___` para exibir:\n\n- `produto.___` → `Teclado`\n- `produto.___` → `150`\n\nVeja um exemplo com outro objeto:\n\n```javascript\nconst pessoa = { nome: \"Ana\", idade: 30 };\nconsole.log(pessoa.nome);  // Ana\nconsole.log(pessoa.idade); // 30\n```",
    "instruction_en": "Access produto.nome and produto.preco to display Teclado and 150.",
    "instruction_es": "Accede a produto.nome y produto.preco para mostrar Teclado y 150.",
    "starter_code": "const produto = {\n  nome: \"Teclado\",\n  preco: 150,\n  disponivel: true,\n};\nconsole.log(produto.___);\nconsole.log(produto.___);\n",
    "hint": "Preencha com as chaves do objeto: nome e preco.",
    "hints": [
      "Preencha os `___` com `nome` e `preco` — as chaves do objeto.",
      "`produto.nome` retorna `\"Teclado\"` e `produto.preco` retorna `150`.",
    ],
    "tests": [
      {
        "stdin": "",
        "expected_stdout": "Teclado\n150",
      },
    ],
    "quiz": [
      {
        "question": "Como acessar a propriedade `nome` de um objeto `pessoa`?",
        "options": [
          "pessoa[nome]",
          "pessoa->nome",
          "pessoa.nome",
          "pessoa::nome",
        ],
        "correct": 2,
      },
      {
        "question": "Qual é o resultado de `typeof {}` em JavaScript?",
        "options": [
          "\"dict\"",
          "\"array\"",
          "\"object\"",
          "\"undefined\"",
        ],
        "correct": 2,
      },
    ],
  },
  {
    "order": 16,
    "slug": "js-arrow-functions",
    "title": "Arrow Functions",
    "chapter": "Capítulo 4: JS Moderno",
    "theory": "Arrow functions são uma sintaxe mais curta para escrever funções — use `=>` (seta) no lugar de `function`.\n\n## Como funciona\n\n```javascript\n// Função tradicional\nfunction dobrar(n) {\n  return n * 2;\n}\n\n// Arrow function equivalente\nconst dobrar = n => n * 2;\n\nconsole.log(dobrar(5));  // 10\n```\n\n- Com **um** parâmetro: não precisam de `()`\n- Com **expressão única**: não precisam de `{}` nem `return`\n\n## Diferentes formas\n\n```javascript\nconst somar = (a, b) => a + b;           // dois parâmetros\nconst oi = () => 'Olá!';                  // sem parâmetros\nconst grande = n => {                     // bloco com return\n  const msg = `Número: ${n}`;\n  return msg;\n};\n```\n\n## No exercício\n\nComplete as duas arrow functions com a expressão de retorno correta.",
    "instruction_pt": "Complete as duas arrow functions:\n\n- `quadrado` recebe `n` e retorna `n * n` → `quadrado(4)` = `16`\n- `bemVindo` recebe `nome` e retorna `` `Bem-vindo, ${nome}!` `` → `bemVindo(\"Ana\")` = `Bem-vindo, Ana!`\n\nVeja um exemplo com outras arrow functions:\n\n```javascript\nconst dobro = n => n * 2;\nconst saudacao = nome => `Oi, ${nome}!`;\nconsole.log(dobro(5));          // 10\nconsole.log(saudacao(\"Joao\"));  // Oi, Joao!\n```",
    "instruction_en": "Complete: quadrado returns n*n, bemVindo returns a welcome template literal.",
    "instruction_es": "Completa: quadrado retorna n*n, bemVindo retorna un template literal de bienvenida.",
    "starter_code": "const quadrado = n => ___;\nconst bemVindo = nome => `Bem-vindo, ${nome}!`;\nconsole.log(quadrado(4));\nconsole.log(bemVindo(\"Ana\"));\n",
    "hint": "quadrado: n => n * n",
    "hints": [
      "Para `quadrado`, complete com `n * n` — a arrow function retorna automaticamente expressões únicas.",
      "`bemVindo` já está completa — execute e observe `Bem-vindo, Ana!`.",
    ],
    "tests": [
      {
        "stdin": "",
        "expected_stdout": "16\nBem-vindo, Ana!",
      },
    ],
    "quiz": [
      {
        "question": "Qual é a arrow function equivalente a `function dobrar(n) { return n*2; }`?",
        "options": [
          "n -> n*2",
          "n => n*2",
          "(n) >> n*2",
          "fn n => n*2",
        ],
        "correct": 1,
      },
      {
        "question": "Quando uma arrow function precisa de `{}` e `return`?",
        "options": [
          "Sempre",
          "Nunca",
          "Quando tem mais de uma instrução no corpo",
          "Quando tem mais de dois parâmetros",
        ],
        "correct": 2,
      },
    ],
  },
  {
    "order": 17,
    "slug": "js-map-filter",
    "title": "Map e Filter",
    "chapter": "Capítulo 4: JS Moderno",
    "theory": "`.map()` e `.filter()` são os dois métodos mais usados para trabalhar com arrays em JS moderno — eles substituem loops manuais com código mais limpo.\n\n## Como funciona\n\n```javascript\nconst nums = [1, 2, 3, 4, 5];\n\n// map: transforma cada elemento\nconst dobrados = nums.map(n => n * 2);\n// [2, 4, 6, 8, 10]\n\n// filter: seleciona elementos que passam no teste\nconst pares = nums.filter(n => n % 2 === 0);\n// [2, 4]\n```\n\n- `map()` sempre retorna um array de **mesmo tamanho**\n- `filter()` retorna um array com **zero ou mais** elementos\n\n## Encadeando\n\n```javascript\nconst resultado = nums\n  .filter(n => n > 2)       // [3, 4, 5]\n  .map(n => n * 10);        // [30, 40, 50]\n```\n\n## No exercício\n\nUse `map()` para triplicar e `filter()` para selecionar ímpares.",
    "instruction_pt": "Com `numeros = [1, 2, 3, 4, 5, 6]`:\n\n1. Crie `triplos` com `map()` multiplicando por 3 → `3,6,9,12,15,18`\n2. Crie `impares` com `filter()` selecionando os ímpares → `1,3,5`\n3. Exiba com `.join(\",\")`\n\nVeja um exemplo com outro array:\n\n```javascript\nconst numeros = [1, 2, 3, 4];\nconst dobrados = numeros.map(n => n * 2);\nconst pares = numeros.filter(n => n % 2 === 0);\nconsole.log(dobrados.join(\",\")); // 2,4,6,8\nconsole.log(pares.join(\",\"));    // 2,4\n```",
    "instruction_en": "Use map() to triple and filter() to select odd numbers, display with join.",
    "instruction_es": "Usa map() para triplicar y filter() para seleccionar impares, muestra con join.",
    "starter_code": "const numeros = [1, 2, 3, 4, 5, 6];\nconst triplos = numeros.map(n => ___);\nconst impares = numeros.filter(n => ___);\nconsole.log(triplos.join(\",\"));\nconsole.log(impares.join(\",\"));\n",
    "hint": "triplos: n => n * 3 | impares: n => n % 2 !== 0",
    "hints": [
      "Para `triplos`: `n => n * 3` — multiplica cada elemento por 3.",
      "Para `impares`: `n => n % 2 !== 0` — seleciona números que não são divisíveis por 2.",
    ],
    "tests": [
      {
        "stdin": "",
        "expected_stdout": "3,6,9,12,15,18\n1,3,5",
      },
    ],
    "quiz": [
      {
        "question": "Qual a diferença entre map() e filter()?",
        "options": [
          "São idênticos",
          "map() transforma elementos; filter() seleciona elementos",
          "filter() transforma; map() seleciona",
          "Ambos removem elementos",
        ],
        "correct": 1,
      },
      {
        "question": "Quantos elementos `[1,2,3].map(n => n+1)` retorna?",
        "options": [
          "Depende",
          "2",
          "3",
          "6",
        ],
        "correct": 2,
      },
    ],
  },
  {
    "order": 18,
    "slug": "js-destructuring",
    "title": "Destructuring",
    "chapter": "Capítulo 4: JS Moderno",
    "theory": "Destructuring extrai valores de objetos e arrays em variáveis com uma sintaxe limpa e direta.\n\n## Como funciona — Objetos\n\n```javascript\nconst pessoa = { nome: \"Ana\", cidade: \"SP\", idade: 20 };\n\n// Sem destructuring (verboso)\nconst nome = pessoa.nome;\nconst cidade = pessoa.cidade;\n\n// Com destructuring (limpo)\nconst { nome, cidade } = pessoa;\n\nconsole.log(nome);    // Ana\nconsole.log(cidade);  // SP\n```\n\n## Destructuring de Arrays\n\n```javascript\nconst coords = [10, 20, 30];\nconst [x, y, z] = coords;\nconsole.log(x);  // 10\nconsole.log(y);  // 20\n```\n\n## No exercício\n\nUse destructuring para extrair `marca` e `ano` do objeto `carro`.",
    "instruction_pt": "Use destructuring para extrair `marca` e `ano` do objeto `carro` e exibir:\n\n- `Toyota`\n- `2023`\n\nVeja um exemplo com outro objeto:\n\n```javascript\nconst livro = { titulo: \"1984\", autor: \"Orwell\", ano: 1949 };\nconst { titulo, ano } = livro;\nconsole.log(titulo); // 1984\nconsole.log(ano);    // 1949\n```",
    "instruction_en": "Use destructuring to extract marca and ano from carro, display Toyota and 2023.",
    "instruction_es": "Usa destructuring para extraer marca y ano de carro, muestra Toyota y 2023.",
    "starter_code": "const carro = { marca: \"Toyota\", modelo: \"Corolla\", ano: 2023 };\nconst { ___, ___ } = carro;\nconsole.log(marca);\nconsole.log(ano);\n",
    "hint": "Preencha com: marca, ano (as chaves do objeto que você quer extrair).",
    "hints": [
      "Preencha os `___` com `marca` e `ano` — os nomes devem bater com as chaves do objeto.",
      "Resultado: `{ marca, ano } = carro` cria as variáveis `marca = \"Toyota\"` e `ano = 2023`.",
    ],
    "tests": [
      {
        "stdin": "",
        "expected_stdout": "Toyota\n2023",
      },
    ],
    "quiz": [
      {
        "question": "O que `const { nome } = pessoa` faz?",
        "options": [
          "Cria um novo objeto",
          "Extrai a propriedade nome de pessoa para uma variável",
          "Remove nome de pessoa",
          "Verifica se pessoa tem nome",
        ],
        "correct": 1,
      },
      {
        "question": "Como usar destructuring para extrair o segundo elemento de um array `arr`?",
        "options": [
          "const [, segundo] = arr",
          "const {1: segundo} = arr",
          "const segundo = arr.get(1)",
          "const [segundo] = arr.slice(1)",
        ],
        "correct": 0,
      },
    ],
  },
  {
    "order": 19,
    "slug": "js-projeto",
    "title": "Projeto Final",
    "chapter": "Capítulo 4: JS Moderno",
    "theory": "Hora de juntar tudo que você aprendeu: variáveis, arrays, objetos, filter, map e template literals num mini-programa real!\n\n## O que vamos construir\n\nUm sistema simples de estoque que filtra produtos caros e lista seus nomes.\n\n## Revisando os conceitos usados\n\n```javascript\n// Objetos dentro de arrays\nconst produtos = [\n  { nome: \"A\", preco: 10 },\n  { nome: \"B\", preco: 50 },\n];\n\n// filter: seleciona por condição\nconst caros = produtos.filter(p => p.preco > 30);\n// [{ nome: 'B', preco: 50 }]\n\n// forEach: itera sem transformar\ncaros.forEach(p => console.log(p.nome));\n// B\n```\n\n## No exercício\n\nComplete os dois `___` para filtrar produtos acima de R$ 50 e exibir seus nomes.",
    "instruction_pt": "Complete o programa para:\n\n1. Filtrar produtos com `preco > 50` → Mochila e Calculadora\n2. Exibir `Produtos caros: 2`\n3. Exibir o nome de cada produto caro (um por linha)\n\nVeja um exemplo com outro cenario:\n\n```javascript\nconst alunos = [\n  { nome: \"Ana\", nota: 8 },\n  { nome: \"Bruno\", nota: 5 },\n];\nconst aprovados = alunos.filter(a => a.nota >= 7);\nconsole.log(`Aprovados: ${aprovados.length}`);\naprovados.forEach(a => console.log(a.nome));\n```",
    "instruction_en": "Filter products with price > 50, display count and each name.",
    "instruction_es": "Filtra productos con precio > 50, muestra la cantidad y cada nombre.",
    "starter_code": "const produtos = [\n  { nome: \"Caderno\",     preco: 15  },\n  { nome: \"Mochila\",     preco: 120 },\n  { nome: \"Caneta\",      preco: 5   },\n  { nome: \"Calculadora\", preco: 85  },\n];\n\n// 1. Filtre produtos com preco > 50\nconst caros = produtos.filter(p => p.preco > ___);\n\n// 2. Exiba o total de produtos caros\nconsole.log(`Produtos caros: ${caros.length}`);\n\n// 3. Exiba o nome de cada produto caro\ncaros.forEach(p => console.log(p.___));\n",
    "hint": "Preencha: > 50 no filter e .nome no forEach.",
    "hints": [
      "Troque o primeiro `___` por `50` — o filtro selecionará Mochila (120) e Calculadora (85).",
      "No `forEach`, acesse `p.nome` para exibir apenas o nome de cada produto.",
    ],
    "tests": [
      {
        "stdin": "",
        "expected_stdout": "Produtos caros: 2\nMochila\nCalculadora",
      },
    ],
    "quiz": [
      {
        "question": "Qual método percorre um array executando uma função para cada elemento sem retornar um novo array?",
        "options": [
          "map()",
          "filter()",
          "forEach()",
          "reduce()",
        ],
        "correct": 2,
      },
      {
        "question": "Como acessar a propriedade `preco` de um objeto `p` dentro de um callback?",
        "options": [
          "p[preco]",
          "p->preco",
          "p.preco",
          "preco(p)",
        ],
        "correct": 2,
      },
      {
        "question": "Você terminou a trilha de JavaScript! O que vem a seguir no CodeFuturo?",
        "options": [
          "Nada, JS é o fim",
          "HTML & CSS — a base visual da web",
          "Direto para React",
          "Banco de dados",
        ],
        "correct": 1,
      },
    ],
  },
],

# ── HTML & CSS ─────────────────────────────────────────────────────────────────
"html-css": [
  {
    'order': 1,
    'slug': 'html-titulo',
    'title': 'Título com h1',
    'chapter': 'Capítulo 1: Estrutura HTML',
    'theory': "HTML usa tags para estruturar o conteúdo de uma página. Cada tag tem abertura `<tag>` e fechamento `</tag>`, com o conteúdo entre elas.\n\n## Como funciona\n\n```html\n<h1>Título Principal</h1>\n<h2>Subtítulo</h2>\n<p>Um parágrafo de texto.</p>\n```\n\n- `<h1>` a `<h6>` são títulos, do mais importante ao menos importante\n- Toda tag aberta precisa ser fechada\n\n## No exercício\n\nCrie um `<h1>` com o texto 'Olá, Web!'.",
    'instruction_pt': "HTML usa tags para estruturar conteúdo. `<h1>` cria um título principal. Tags HTML seguem o padrão `<tag>conteúdo</tag>`. Escreva a tag que exibe o título 'Olá, Web!'\n\nVeja um exemplo:\n\n```html\n<h1>Bem-vindo</h1>\n```",
    'instruction_en': "HTML uses tags to structure content. `<h1>` creates a main heading. Write the tag that displays the heading 'Olá, Web!'",
    'instruction_es': "HTML usa etiquetas para estructurar contenido. `<h1>` crea un título principal. Escribe la etiqueta que muestra el título 'Olá, Web!'",
    'starter_code': '<!DOCTYPE html>\n<html>\n  <body>\n    <!-- Adicione um título h1 com o texto: Olá, Web! -->\n    <!-- escreva aqui -->\n  </body>\n</html>\n',
    'hint': 'Estrutura: <h1>texto aqui</h1>',
    'hints': [
      'Tags HTML seguem o padrão `<tag>conteúdo</tag>` — abre e fecha.',
      'Solução: `<h1>Olá, Web!</h1>` — coloque dentro do comentário no código.',
    ],
    'tests': [
      {
        'stdin': '',
        'expected_stdout': '<h1>Olá, Web!</h1>',
      },
    ],
    'quiz': [
      {
        'question': 'Qual tag HTML cria o título principal de uma página?',
        'options': [
          '<title>',
          '<heading>',
          '<h1>',
          '<header>',
        ],
        'correct': 2,
      },
      {
        'question': 'Como é a estrutura de uma tag HTML com conteúdo?',
        'options': [
          '<tag>conteúdo</tag>',
          '{tag}conteúdo{/tag}',
          '[tag]conteúdo[/tag]',
          'tag(conteúdo)',
        ],
        'correct': 0,
      },
    ],
  },
  {
    'order': 2,
    'slug': 'html-paragrafos',
    'title': 'Parágrafos',
    'chapter': 'Capítulo 1: Estrutura HTML',
    'theory': "A tag `<p>` cria parágrafos de texto — é a tag mais usada para conteúdo textual em páginas web.\n\n## Como funciona\n\n```html\n<p>Este é um parágrafo de texto.</p>\n<p>Este é outro parágrafo.</p>\n```\n\nCada `<p>` cria um bloco de texto separado, com espaçamento automático entre eles.\n\n## No exercício\n\nAdicione um `<p>` com o texto 'Bem-vindo ao HTML!'.",
    'instruction_pt': '`<p>` cria parágrafos de texto. É a tag mais usada para conteúdo textual em páginas web. Escreva o parágrafo com o texto exato solicitado.\n\nVeja um exemplo:\n\n```html\n<p>Aprendendo HTML na prática.</p>\n```',
    'instruction_en': "`<p>` creates text paragraphs. It's the most used tag for textual content on web pages.",
    'instruction_es': '`<p>` crea párrafos de texto. Es la etiqueta más usada para contenido textual en páginas web.',
    'starter_code': '<body>\n  <h1>Meu Site</h1>\n  <!-- Adicione um parágrafo com: Bem-vindo ao HTML! -->\n  <!-- escreva aqui -->\n</body>\n',
    'hint': 'Use <p>texto aqui</p>',
    'hints': [
      '`<p>` é a tag de parágrafo — abre e fecha: `<p>texto</p>`.',
      'Solução: `<p>Bem-vindo ao HTML!</p>` — copie o texto exato.',
    ],
    'tests': [
      {
        'stdin': '',
        'expected_stdout': '<p>Bem-vindo ao HTML!</p>',
      },
    ],
    'quiz': [
      {
        'question': 'Qual tag HTML cria parágrafos de texto?',
        'options': [
          '<text>',
          '<para>',
          '<p>',
          '<txt>',
        ],
        'correct': 2,
      },
      {
        'question': 'Qual tag é mais usada para conteúdo textual em páginas?',
        'options': [
          '<span>',
          '<div>',
          '<p>',
          '<text>',
        ],
        'correct': 2,
      },
    ],
  },
  {
    'order': 3,
    'slug': 'html-links',
    'title': 'Links',
    'chapter': 'Capítulo 1: Estrutura HTML',
    'theory': 'Links conectam páginas. A tag `<a>` cria um link clicável, e o atributo `href` define para onde ele aponta.\n\n## Como funciona\n\n```html\n<a href="https://exemplo.com">Visitar site</a>\n```\n\n- `href` define o destino do link\n- O texto entre `<a>` e `</a>` é o que aparece clicável\n- Aspas simples `\'` ou duplas `"` funcionam igualmente em `href`\n\n## No exercício\n\nCrie um link para https://codefuturo.com.br com o texto \'Acessar\'.',
    'instruction_pt': '`<a href="url">texto</a>` cria links clicáveis. O atributo `href` define o destino. Escreva o link completo que aponta para https://codefuturo.com.br com o texto \'Acessar\'. Aspas simples \' ou duplas " funcionam igualmente.\n\nVeja um exemplo:\n\n```html\n<a href="https://exemplo.com">Visitar</a>\n```',
    'instruction_en': '`<a href="url">text</a>` creates clickable links. The `href` attribute defines the destination. Single \' or double " quotes both work.',
    'instruction_es': '`<a href="url">texto</a>` crea enlaces clicables. El atributo `href` define el destino. Las comillas simples \' y dobles " funcionan igual.',
    'starter_code': '<!-- Crie um link para https://codefuturo.com.br com o texto "Acessar" -->\n<!-- escreva aqui -->\n',
    'hint': 'Estrutura: <a href="https://...">texto</a> — aspas simples ou duplas são aceitas.',
    'hints': [
      '`href` define o destino do link — o texto clicável fica entre as tags `<a>` e `</a>`.',
      'Solução: `<a href="https://codefuturo.com.br">Acessar</a>` — aspas simples ou duplas funcionam.',
      "Lembre: o texto visível é 'Acessar', o endereço vai no `href`.",
    ],
    'tests': [
      {
        'stdin': '',
        'expected_stdout': '<a href="https://codefuturo.com.br">Acessar</a>',
      },
    ],
    'quiz': [
      {
        'question': 'Qual atributo HTML define o destino de um link?',
        'options': [
          'src',
          'href',
          'link',
          'url',
        ],
        'correct': 1,
      },
      {
        'question': 'Qual tag HTML cria links clicáveis?',
        'options': [
          '<link>',
          '<url>',
          '<a>',
          '<goto>',
        ],
        'correct': 2,
      },
      {
        'question': 'Como abrir um link em nova aba com HTML?',
        'options': [
          "target='_blank'",
          "href='new'",
          "open='tab'",
          "new='true'",
        ],
        'correct': 0,
      },
    ],
  },
  {
    'order': 4,
    'slug': 'html-imagem',
    'title': 'Imagem',
    'chapter': 'Capítulo 1: Estrutura HTML',
    'theory': 'A tag `<img>` insere imagens na página. Ela é auto-fechante — não precisa de `</img>`.\n\n## Como funciona\n\n```html\n<img src="foto.jpg" alt="Minha foto">\n```\n\n- `src` define o caminho (ou URL) da imagem — atributo obrigatório\n- `alt` descreve a imagem para acessibilidade e aparece se a imagem não carregar\n- A ordem dos atributos não importa\n\n## No exercício\n\nAdicione uma imagem com src="logo.png" e alt="Logo CodeFuturo".',
    'instruction_pt': '`<img>` insere imagens. Atributos obrigatórios: `src` (caminho) e `alt` (descrição para acessibilidade). É uma tag auto-fechante — não precisa de `</img>`.\n\nVeja um exemplo:\n\n```html\n<img src="foto.jpg" alt="Minha foto">\n```',
    'instruction_en': "`<img>` inserts images. Required attributes: `src` (path) and `alt` (accessibility description). It's self-closing.",
    'instruction_es': '`<img>` inserta imágenes. Atributos requeridos: `src` y `alt`. Es una etiqueta auto-cerrante.',
    'starter_code': '<!-- Adicione uma imagem com src="logo.png" e alt="Logo CodeFuturo" -->\n<!-- escreva aqui -->\n',
    'hint': 'Estrutura: <img src="logo.png" alt="Logo CodeFuturo">',
    'hints': [
      '`<img>` é auto-fechante — não precisa de `</img>`, use só a tag de abertura.',
      'Solução: `<img src="logo.png" alt="Logo CodeFuturo">` — dois atributos obrigatórios.',
      'Ordem dos atributos não importa: `alt` antes de `src` também funciona.',
    ],
    'tests': [
      {
        'stdin': '',
        'expected_stdout': '<img src="logo.png" alt="Logo CodeFuturo">',
      },
    ],
    'quiz': [
      {
        'question': 'Qual atributo HTML define o caminho da imagem em <img>?',
        'options': [
          'href',
          'link',
          'src',
          'path',
        ],
        'correct': 2,
      },
      {
        'question': 'Para que serve o atributo alt em <img>?',
        'options': [
          'Altera o tamanho',
          'Descrição alternativa para acessibilidade',
          'Alinha a imagem',
          'Define o formato',
        ],
        'correct': 1,
      },
      {
        'question': 'A tag <img> precisa de tag de fechamento?',
        'options': [
          'Sim, </img>',
          'Não, é auto-fechante',
          'Sim, <img/>',
          'Depende do navegador',
        ],
        'correct': 1,
      },
    ],
  },
  {
    'order': 5,
    'slug': 'html-listas',
    'title': 'Listas',
    'chapter': 'Capítulo 1: Estrutura HTML',
    'theory': 'Listas organizam itens. `<ul>` cria uma lista não ordenada (com bolinhas) e `<ol>` cria uma lista ordenada (numerada). Cada item usa `<li>`.\n\n## Como funciona\n\n```html\n<ul>\n  <li>Python</li>\n  <li>JavaScript</li>\n</ul>\n\n<ol>\n  <li>Primeiro passo</li>\n  <li>Segundo passo</li>\n</ol>\n```\n\n- `<ul>` = lista com bolinhas; `<ol>` = lista numerada\n- Cada item, em ambas, fica dentro de `<li>...</li>`\n\n## No exercício\n\nCrie uma lista não ordenada com 3 linguagens: Python, JavaScript, Go.',
    'instruction_pt': '`<ul>` cria lista não ordenada (com bolinhas). `<ol>` cria lista ordenada (numerada). Cada item usa `<li>`.\n\nVeja um exemplo:\n\n```html\n<ul>\n  <li>Maçã</li>\n  <li>Banana</li>\n</ul>\n```',
    'instruction_en': '`<ul>` creates unordered (bulleted) lists. `<ol>` creates ordered (numbered) lists. Each item uses `<li>`.',
    'instruction_es': '`<ul>` crea listas no ordenadas. `<ol>` crea listas ordenadas. Cada elemento usa `<li>`.',
    'starter_code': '<!-- Crie uma lista não ordenada com 3 linguagens: Python, JavaScript, Go -->\n<!-- escreva aqui -->\n',
    'hint': '<ul><li>Python</li><li>JavaScript</li><li>Go</li></ul>',
    'hints': [
      '`<ul>` é a lista não ordenada — cada item fica dentro de `<li>...</li>`.',
      'Estrutura: `<ul><li>Python</li><li>JavaScript</li><li>Go</li></ul>`',
      'O teste verifica apenas se `<li>Python</li>` existe no código.',
    ],
    'tests': [
      {
        'stdin': '',
        'expected_stdout': '<li>Python</li>',
      },
    ],
    'quiz': [
      {
        'question': 'Qual tag HTML cria uma lista não ordenada (com bolinhas)?',
        'options': [
          '<ol>',
          '<list>',
          '<ul>',
          '<dl>',
        ],
        'correct': 2,
      },
      {
        'question': 'Qual tag representa cada item de uma lista HTML?',
        'options': [
          '<item>',
          '<li>',
          '<dt>',
          '<point>',
        ],
        'correct': 1,
      },
      {
        'question': 'Qual tag HTML cria uma lista numerada?',
        'options': [
          '<nl>',
          '<ul>',
          '<il>',
          '<ol>',
        ],
        'correct': 3,
      },
    ],
  },
  {
    'order': 6,
    'slug': 'html-semantica',
    'title': 'Tags semânticas',
    'chapter': 'Capítulo 1: Estrutura HTML',
    'theory': "`<div>` e `<span>` são genéricas — agrupam conteúdo sem dizer nada sobre seu significado. Tags semânticas como `<header>`, `<nav>`, `<main>`, `<section>` e `<footer>` descrevem o papel de cada parte da página.\n\n## Como funciona\n\n```html\n<header>\n  <h1>Meu Site</h1>\n</header>\n<main>\n  <p>Conteúdo principal da página.</p>\n</main>\n<footer>\n  <p>© 2026 Meu Site</p>\n</footer>\n```\n\n- `<div>` = bloco genérico, `<span>` = trecho de texto genérico\n- `<header>`, `<main>`, `<footer>`, `<nav>`, `<section>` descrevem a estrutura — ajudam leitores de tela e SEO\n\n## No exercício\n\nCrie um `<footer>` com o texto '© 2026 CodeFuturo'.",
    'instruction_pt': "Tags semânticas como `<header>`, `<main>` e `<footer>` descrevem o papel de cada parte da página — diferente de `<div>`, que é genérica. Crie um `<footer>` com o texto '© 2026 CodeFuturo'.\n\nVeja um exemplo:\n\n```html\n<footer>\n  <p>Feito com HTML</p>\n</footer>\n```",
    'instruction_en': "Semantic tags like `<header>`, `<main>` and `<footer>` describe the role of each part of the page. Create a `<footer>` with the text '© 2026 CodeFuturo'.",
    'instruction_es': "Las etiquetas semánticas como `<header>`, `<main>` y `<footer>` describen el papel de cada parte de la página. Crea un `<footer>` con el texto '© 2026 CodeFuturo'.",
    'starter_code': '<!-- Crie um footer com o texto: © 2026 CodeFuturo -->\n<!-- escreva aqui -->\n',
    'hint': '<footer>© 2026 CodeFuturo</footer>',
    'hints': [
      '`<footer>` é uma tag semântica para o rodapé da página.',
      'Solução: `<footer>© 2026 CodeFuturo</footer>` — copie o texto exato.',
    ],
    'tests': [
      {
        'stdin': '',
        'expected_stdout': '<footer>© 2026 CodeFuturo</footer>',
      },
    ],
    'quiz': [
      {
        'question': 'Qual tag semântica representa o rodapé de uma página?',
        'options': [
          '<bottom>',
          '<end>',
          '<footer>',
          '<div>',
        ],
        'correct': 2,
      },
      {
        'question': 'Qual a diferença entre <div> e tags como <header>/<footer>?',
        'options': [
          'Não há diferença',
          '<div> é genérica, as semânticas descrevem o papel do conteúdo',
          '<div> só funciona com CSS',
          '<header> não pode ter filhos',
        ],
        'correct': 1,
      },
    ],
  },
  {
    'order': 7,
    'slug': 'html-tabela',
    'title': 'Tabela',
    'chapter': 'Capítulo 2: Conteúdo Estruturado',
    'theory': 'Tabelas organizam dados em linhas e colunas.\n\n## Como funciona\n\n```html\n<table>\n  <tr>\n    <th>Produto</th>\n    <th>Preço</th>\n  </tr>\n  <tr>\n    <td>Caderno</td>\n    <td>15</td>\n  </tr>\n</table>\n```\n\n- `<table>` → container da tabela\n- `<tr>` → linha (table row)\n- `<th>` → célula de cabeçalho (table header)\n- `<td>` → célula de dados (table data)\n\n## No exercício\n\nCrie uma tabela com cabeçalhos Nome e Idade.',
    'instruction_pt': 'Tabelas organizam dados em linhas e colunas:\n- `<table>` → container\n- `<tr>` → linha\n- `<th>` → cabeçalho\n- `<td>` → célula de dados\n\nCrie uma tabela com cabeçalhos Nome e Idade.\n\nVeja um exemplo:\n\n```html\n<table>\n  <tr>\n    <th>Produto</th>\n    <th>Preço</th>\n  </tr>\n</table>\n```',
    'instruction_en': 'Tables organize data in rows and columns: `<table>`, `<tr>`, `<th>`, `<td>`.',
    'instruction_es': 'Las tablas organizan datos en filas y columnas: `<table>`, `<tr>`, `<th>`, `<td>`.',
    'starter_code': '<!-- Crie uma tabela com cabeçalhos "Nome" e "Idade" -->\n<table>\n  <tr>\n    <!-- escreva os cabeçalhos aqui -->\n  </tr>\n</table>\n',
    'hint': '<th>Nome</th><th>Idade</th>',
    'hints': [
      '`<th>` é o cabeçalho de coluna — diferente de `<td>` que é dado normal.',
      'Dentro do `<tr>` já existente, adicione: `<th>Nome</th><th>Idade</th>`',
      'O teste verifica apenas `<th>Nome</th>` — Idade também precisa existir.',
    ],
    'tests': [
      {
        'stdin': '',
        'expected_stdout': '<th>Nome</th>',
      },
    ],
    'quiz': [
      {
        'question': 'Qual tag HTML define uma linha em uma tabela?',
        'options': [
          '<td>',
          '<row>',
          '<tr>',
          '<line>',
        ],
        'correct': 2,
      },
      {
        'question': 'Qual tag HTML cria uma célula de cabeçalho em tabela?',
        'options': [
          '<td>',
          '<th>',
          '<head>',
          '<header>',
        ],
        'correct': 1,
      },
    ],
  },
  {
    'order': 8,
    'slug': 'html-formulario',
    'title': 'Formulário',
    'chapter': 'Capítulo 2: Conteúdo Estruturado',
    'theory': 'Formulários coletam dados do usuário. `<form>` agrupa os campos, e `<input>` é o campo de entrada mais comum.\n\n## Como funciona\n\n```html\n<form>\n  <input type="email" name="email" placeholder="seu@email.com">\n  <button type="submit">Enviar</button>\n</form>\n```\n\n- `type` define o tipo do campo: `text`, `email`, `password`, `submit`...\n- `name` identifica o campo quando o formulário é enviado\n- `placeholder` mostra um texto de exemplo dentro do campo\n\n## No exercício\n\nAdicione um input do tipo "text" com name="usuario".',
    'instruction_pt': '`<form>` agrupa campos de entrada. `<input>` recebe dados do usuário. Atributos importantes: `type` (text, email, password, submit) e `name`.\n\nVeja um exemplo:\n\n```html\n<input type="email" name="email" placeholder="seu@email.com">\n```',
    'instruction_en': '`<form>` groups input fields. `<input>` receives user data. Key attributes: `type` and `name`.',
    'instruction_es': '`<form>` agrupa campos de entrada. `<input>` recibe datos del usuario.',
    'starter_code': '<form>\n  <!-- Adicione um input do tipo "text" com name="usuario" -->\n  <!-- escreva aqui -->\n  <button type="submit">Enviar</button>\n</form>\n',
    'hint': 'Estrutura: <input type="text" name="usuario">',
    'hints': [
      '`<input>` é auto-fechante — não precisa de tag de fechamento.',
      'Solução: `<input type="text" name="usuario">` — dois atributos obrigatórios.',
      'O atributo `type="text"` define o tipo de campo, `name` identifica no formulário.',
    ],
    'tests': [
      {
        'stdin': '',
        'expected_stdout': '<input type="text" name="usuario">',
      },
    ],
    'quiz': [
      {
        'question': 'Qual tag HTML agrupa campos de um formulário?',
        'options': [
          '<input>',
          '<group>',
          '<fieldset>',
          '<form>',
        ],
        'correct': 3,
      },
      {
        'question': 'Qual atributo define o tipo de campo <input>?',
        'options': [
          'kind',
          'style',
          'type',
          'mode',
        ],
        'correct': 2,
      },
      {
        'question': 'Qual type de input cria um botão de envio?',
        'options': [
          "type='button'",
          "type='submit'",
          "type='send'",
          "type='action'",
        ],
        'correct': 1,
      },
    ],
  },
  {
    'order': 9,
    'slug': 'html-select',
    'title': 'Select e Label',
    'chapter': 'Capítulo 2: Conteúdo Estruturado',
    'theory': '`<select>` cria uma lista suspensa (dropdown); cada opção é um `<option>`. `<label>` associa um texto descritivo a um campo, melhorando a acessibilidade.\n\n## Como funciona\n\n```html\n<label>Linguagem:</label>\n<select>\n  <option>Python</option>\n  <option>JavaScript</option>\n</select>\n```\n\n- Cada `<option>` é uma escolha do dropdown\n- `<label>` ajuda leitores de tela e melhora a usabilidade do formulário\n\n## No exercício\n\nCrie um `<select>` com duas opções: Python e JavaScript.',
    'instruction_pt': '`<select>` cria uma lista suspensa; cada `<option>` é uma escolha. Crie um `<select>` com duas `<option>`: Python e JavaScript.\n\nVeja um exemplo:\n\n```html\n<select>\n  <option>Cão</option>\n  <option>Gato</option>\n</select>\n```',
    'instruction_en': '`<select>` creates a dropdown list; each `<option>` is a choice. Create a `<select>` with two options: Python and JavaScript.',
    'instruction_es': '`<select>` crea una lista desplegable; cada `<option>` es una opción. Crea un `<select>` con dos opciones: Python y JavaScript.',
    'starter_code': '<!-- Crie um select com duas options: Python e JavaScript -->\n<!-- escreva aqui -->\n',
    'hint': '<select><option>Python</option><option>JavaScript</option></select>',
    'hints': [
      '`<select>` envolve as opções; cada escolha é um `<option>texto</option>`.',
      'Estrutura: `<select><option>Python</option><option>JavaScript</option></select>`',
      'O teste verifica apenas `<option>Python</option>` — adicione JavaScript também.',
    ],
    'tests': [
      {
        'stdin': '',
        'expected_stdout': '<option>Python</option>',
      },
    ],
    'quiz': [
      {
        'question': 'Qual tag cria uma lista suspensa (dropdown) em HTML?',
        'options': [
          '<dropdown>',
          '<list>',
          '<select>',
          '<menu>',
        ],
        'correct': 2,
      },
      {
        'question': 'Qual tag representa cada opção dentro de um <select>?',
        'options': [
          '<item>',
          '<option>',
          '<choice>',
          '<li>',
        ],
        'correct': 1,
      },
      {
        'question': 'Para que serve a tag <label>?',
        'options': [
          'Estiliza o texto',
          'Associa um texto descritivo a um campo',
          'Cria uma tabela',
          'Define a cor',
        ],
        'correct': 1,
      },
    ],
  },
  {
    'order': 10,
    'slug': 'css-cor',
    'title': 'Cor com CSS',
    'chapter': 'Capítulo 3: Estilo com CSS',
    'theory': 'CSS (Cascading Style Sheets) define a aparência do HTML: cores, fontes, espaçamento e layout.\n\n## Como funciona\n\n```html\n<style>\n  h1 {\n    color: blue;\n  }\n</style>\n```\n\n- Cada regra tem um **seletor** (`h1`) e **declarações** entre `{ }`\n- Cada declaração segue o formato `propriedade: valor;`\n\n## No exercício\n\nDeixe o texto do `h1` azul com `color: blue;`.',
    'instruction_pt': 'CSS estiliza o HTML. A propriedade `color` define a cor do texto. Escreva apenas a declaração CSS que deixa o texto azul.\n\nVeja um exemplo:\n\n```css\np {\n  color: green;\n}\n```',
    'instruction_en': 'CSS styles HTML. The `color` property defines text color. Write only the CSS declaration that makes text blue.',
    'instruction_es': 'CSS da estilo al HTML. La propiedad `color` define el color del texto. Escribe solo la declaración CSS que hace el texto azul.',
    'starter_code': '<style>\n  h1 {\n    /* Deixe o texto azul */\n    /* escreva aqui */\n  }\n</style>\n',
    'hint': 'Propriedade: color: blue;',
    'hints': [
      'Em CSS, cada declaração tem o formato `propriedade: valor;`',
      'Para texto azul: `color: blue;` — substitua o comentário por isso.',
    ],
    'tests': [
      {
        'stdin': '',
        'expected_stdout': 'color: blue;',
      },
    ],
    'quiz': [
      {
        'question': 'Qual propriedade CSS define a cor do texto?',
        'options': [
          'text-color',
          'font-color',
          'color',
          'foreground',
        ],
        'correct': 2,
      },
      {
        'question': 'Onde fica o CSS embutido em uma página HTML?',
        'options': [
          'Na tag <script>',
          'Na tag <style>',
          'Na tag <meta>',
          'Na tag <head>',
        ],
        'correct': 1,
      },
    ],
  },
  {
    'order': 11,
    'slug': 'css-classes',
    'title': 'Classes CSS',
    'chapter': 'Capítulo 3: Estilo com CSS',
    'theory': 'Classes CSS permitem estilizar elementos específicos. Defina com `.nome-da-classe { }` e aplique no HTML com `class="nome"`.\n\n## Como funciona\n\n```html\n<style>\n  .aviso {\n    color: red;\n  }\n</style>\n<p class="aviso">Atenção!</p>\n```\n\n- Classes começam com `.` no CSS\n- O mesmo nome pode ser aplicado a vários elementos com `class="nome"`\n\n## No exercício\n\nCrie a classe `.destaque` com `color: orange`.',
    'instruction_pt': 'Classes CSS permitem estilizar elementos específicos. Defina com `.nome-da-classe { }` e aplique no HTML com `class="nome"`.\n\nVeja um exemplo:\n\n```css\n.aviso {\n  color: red;\n}\n```',
    'instruction_en': 'CSS classes style specific elements. Define with `.class-name { }` and apply with `class="name"`.',
    'instruction_es': 'Las clases CSS permiten estilizar elementos específicos. Define con `.nombre` y aplica con `class="nombre"`.',
    'starter_code': '<style>\n  /* Crie uma classe "destaque" com color: orange */\n  /* escreva aqui */\n</style>\n<p class="destaque">Texto importante</p>\n',
    'hint': '.destaque { color: orange; }',
    'hints': [
      'Classes CSS começam com ponto: `.nome-da-classe { propriedades }`',
      'Solução: `.destaque { color: orange; }` — substitua o comentário no `<style>`.',
      'O teste verifica apenas se `.destaque` existe no código.',
    ],
    'tests': [
      {
        'stdin': '',
        'expected_stdout': '.destaque',
      },
    ],
    'quiz': [
      {
        'question': 'Como referenciar uma classe CSS no HTML?',
        'options': [
          "id='nome'",
          "class='nome'",
          "style='nome'",
          "css='nome'",
        ],
        'correct': 1,
      },
      {
        'question': "Como definir uma classe CSS chamada 'destaque'?",
        'options': [
          '#destaque { }',
          '.destaque { }',
          'destaque { }',
          '@destaque { }',
        ],
        'correct': 1,
      },
    ],
  },
  {
    'order': 12,
    'slug': 'css-id-seletor',
    'title': 'Seletor de ID',
    'chapter': 'Capítulo 3: Estilo com CSS',
    'theory': 'Além de classes, CSS pode selecionar um elemento único pelo **id**, usando `#`. Diferente da classe (reutilizável em vários elementos), o `id` deve ser único na página.\n\n## Como funciona\n\n```html\n<style>\n  #titulo-principal {\n    color: purple;\n  }\n</style>\n<h1 id="titulo-principal">Olá!</h1>\n```\n\n- `#nome { }` no CSS seleciona o elemento com `id="nome"`\n- Use `id` para um elemento único; `class` para grupos de elementos\n\n## No exercício\n\nCrie a regra `#destaque` com `background: yellow`.',
    'instruction_pt': 'Seletores de `id` usam `#` e aplicam estilo a um elemento único, identificado por `id="..."`. Crie a regra `#destaque` com `background: yellow`.\n\nVeja um exemplo:\n\n```css\n#topo {\n  background: lightgray;\n}\n```',
    'instruction_en': 'ID selectors use `#` and style a single element identified by `id="..."`. Create the rule `#destaque` with `background: yellow`.',
    'instruction_es': 'Los selectores de `id` usan `#` y aplican estilo a un elemento único, identificado por `id="..."`. Crea la regla `#destaque` con `background: yellow`.',
    'starter_code': '<style>\n  /* Crie a regra #destaque com background: yellow */\n  /* escreva aqui */\n</style>\n<p id="destaque">Texto destacado</p>\n',
    'hint': '#destaque { background: yellow; }',
    'hints': [
      'Seletores de id começam com `#`, seguido do valor do atributo `id`.',
      'Solução: `#destaque { background: yellow; }` — substitua o comentário no `<style>`.',
      'O teste verifica apenas se `#destaque` existe no código.',
    ],
    'tests': [
      {
        'stdin': '',
        'expected_stdout': '#destaque',
      },
    ],
    'quiz': [
      {
        'question': 'Como selecionar em CSS um elemento com id="topo"?',
        'options': [
          '.topo',
          '#topo',
          '*topo',
          '@topo',
        ],
        'correct': 1,
      },
      {
        'question': 'Qual a principal diferença entre id e class em CSS?',
        'options': [
          'Não há diferença',
          'id deve ser único na página, class pode repetir',
          'class é mais rápida',
          'id não aceita estilos',
        ],
        'correct': 1,
      },
    ],
  },
  {
    'order': 13,
    'slug': 'css-hover',
    'title': 'Pseudo-classe :hover',
    'chapter': 'Capítulo 3: Estilo com CSS',
    'theory': 'Pseudo-classes aplicam estilo em estados especiais de um elemento, como quando o mouse passa por cima. `:hover` é a mais usada.\n\n## Como funciona\n\n```html\n<style>\n  button {\n    background: blue;\n  }\n  button:hover {\n    background: darkblue;\n  }\n</style>\n<button>Clique aqui</button>\n```\n\n- `seletor:hover { }` muda o estilo quando o mouse está sobre o elemento\n- Outras pseudo-classes comuns: `:focus`, `:active`, `:first-child`\n\n## No exercício\n\nCrie a regra `button:hover` com `background: green`.',
    'instruction_pt': '`:hover` aplica estilo quando o mouse passa sobre o elemento. Crie a regra `button:hover` com `background: green`.\n\nVeja um exemplo:\n\n```css\na:hover {\n  color: red;\n}\n```',
    'instruction_en': '`:hover` applies a style when the mouse is over the element. Create the rule `button:hover` with `background: green`.',
    'instruction_es': '`:hover` aplica un estilo cuando el mouse pasa sobre el elemento. Crea la regla `button:hover` con `background: green`.',
    'starter_code': '<style>\n  button {\n    background: blue;\n    color: white;\n  }\n  /* Ao passar o mouse, deixe o fundo verde */\n  /* escreva aqui */\n</style>\n<button>Clique aqui</button>\n',
    'hint': 'button:hover { background: green; }',
    'hints': [
      'Pseudo-classes usam `:` depois do seletor — `seletor:hover { }`.',
      'Solução: `button:hover { background: green; }` — adicione após a regra do `button`.',
      'O teste verifica apenas se `button:hover` existe no código.',
    ],
    'tests': [
      {
        'stdin': '',
        'expected_stdout': 'button:hover',
      },
    ],
    'quiz': [
      {
        'question': 'O que a pseudo-classe :hover faz?',
        'options': [
          'Estiliza o primeiro elemento',
          'Aplica estilo quando o mouse está sobre o elemento',
          'Esconde o elemento',
          'Estiliza links visitados',
        ],
        'correct': 1,
      },
      {
        'question': 'Qual a sintaxe correta de uma pseudo-classe?',
        'options': [
          'seletor.hover',
          'seletor#hover',
          'seletor:hover',
          'seletor->hover',
        ],
        'correct': 2,
      },
    ],
  },
  {
    'order': 14,
    'slug': 'css-flexbox',
    'title': 'Flexbox',
    'chapter': 'Capítulo 4: Layout Moderno',
    'theory': 'Flexbox é o sistema de layout mais usado no CSS moderno. `display: flex` ativa o flex container, e as propriedades de alinhamento organizam os elementos dentro dele.\n\n## Como funciona\n\n```css\n.container {\n  display: flex;\n  justify-content: center;\n  align-items: center;\n}\n```\n\n- `display: flex` ativa o Flexbox no container\n- `justify-content` alinha no eixo horizontal (`center`, `space-between`...)\n- `align-items` alinha no eixo vertical\n\n## No exercício\n\nAtive o flexbox e centralize horizontalmente com `justify-content: center`.',
    'instruction_pt': 'Flexbox é o sistema de layout mais usado no CSS moderno. `display: flex` ativa o flex container. Use `justify-content` para alinhar horizontalmente e `align-items` verticalmente.\n\nVeja um exemplo:\n\n```css\n.container {\n  display: flex;\n  align-items: center;\n}\n```',
    'instruction_en': 'Flexbox is the most used layout system. `display: flex` activates the flex container.',
    'instruction_es': 'Flexbox es el sistema de layout más usado en CSS moderno.',
    'starter_code': '<style>\n  .container {\n    /* Ative flexbox e centralize horizontalmente */\n    /* escreva aqui */\n  }\n</style>\n<div class="container">\n  <p>Item 1</p><p>Item 2</p><p>Item 3</p>\n</div>\n',
    'hint': 'display: flex; justify-content: center;',
    'hints': [
      '`display: flex;` ativa o Flexbox no container — é o primeiro passo.',
      'Para centralizar: adicione `justify-content: center;` após o `display: flex;`',
      'O teste verifica `display: flex;` — mas adicione ambas as propriedades.',
    ],
    'tests': [
      {
        'stdin': '',
        'expected_stdout': 'display: flex;',
      },
    ],
    'quiz': [
      {
        'question': 'Como ativar o Flexbox em um container CSS?',
        'options': [
          'flex: true',
          'layout: flex',
          'display: flex',
          'box: flex',
        ],
        'correct': 2,
      },
      {
        'question': 'Qual propriedade alinha itens horizontalmente no Flexbox?',
        'options': [
          'align-items',
          'justify-content',
          'flex-direction',
          'align-content',
        ],
        'correct': 1,
      },
    ],
  },
  {
    'order': 15,
    'slug': 'css-box-model',
    'title': 'Box Model',
    'chapter': 'Capítulo 4: Layout Moderno',
    'theory': 'Todo elemento HTML é uma caixa com 4 camadas, de dentro para fora: content, padding, border e margin.\n\n## Como funciona\n\n```css\n.caixa {\n  width: 300px;\n  padding: 20px;\n  border: 2px solid black;\n  margin: 0 auto;\n}\n```\n\n- **content** → o conteúdo em si\n- **padding** → espaço interno, entre o conteúdo e a borda\n- **border** → a borda da caixa\n- **margin** → espaço externo, entre a caixa e os outros elementos\n- `margin: 0 auto` centraliza horizontalmente um elemento com `width` definido\n\n## No exercício\n\nCentralize um div adicionando `margin: 0 auto` (o `width: 400px` já está definido).',
    'instruction_pt': 'Todo elemento HTML é uma caixa com 4 camadas:\n- **content** → conteúdo\n- **padding** → espaço interno\n- **border** → borda\n- **margin** → espaço externo\n\nCentralize um div adicionando `margin: 0 auto` (o `width: 400px` já está definido).\n\nVeja um exemplo:\n\n```css\n.cartao {\n  width: 200px;\n  padding: 10px;\n  border: 1px solid gray;\n}\n```',
    'instruction_en': 'Every HTML element is a box with content, padding, border, and margin.',
    'instruction_es': 'Todo elemento HTML es una caja con content, padding, border y margin.',
    'starter_code': '<style>\n  .caixa {\n    width: 400px;\n    background: lightblue;\n    /* Centralize horizontalmente com margin */\n    /* escreva aqui */\n  }\n</style>\n<div class="caixa">Conteúdo centralizado</div>\n',
    'hint': 'margin: 0 auto;',
    'hints': [
      '`margin: 0 auto;` centraliza um div horizontalmente — `auto` distribui o espaço igualmente.',
      'Adicione `margin: 0 auto;` dentro das chaves do `.caixa`.',
      'O div também precisa de `width` definido para o `auto` funcionar — o starter já tem `width: 400px`.',
    ],
    'tests': [
      {
        'stdin': '',
        'expected_stdout': 'margin: 0 auto;',
      },
    ],
    'quiz': [
      {
        'question': 'Qual é a ordem do Box Model de dentro para fora?',
        'options': [
          'margin > border > padding > content',
          'content > padding > border > margin',
          'padding > content > border > margin',
          'border > content > padding > margin',
        ],
        'correct': 1,
      },
      {
        'question': 'Como centralizar um div horizontalmente com CSS?',
        'options': [
          'align: center',
          'margin: auto',
          'margin: 0 auto',
          'text-align: center',
        ],
        'correct': 2,
      },
      {
        'question': 'O que é padding?',
        'options': [
          'Espaço externo entre elementos',
          'Espaço interno entre o conteúdo e a borda',
          'A borda do elemento',
          'A largura do elemento',
        ],
        'correct': 1,
      },
    ],
  },
  {
    'order': 16,
    'slug': 'css-grid',
    'title': 'CSS Grid',
    'chapter': 'Capítulo 4: Layout Moderno',
    'theory': 'CSS Grid organiza elementos em linhas e colunas — ideal para layouts em duas dimensões.\n\n## Como funciona\n\n```html\n<style>\n  .grade {\n    display: grid;\n    grid-template-columns: 1fr 1fr 1fr;\n    gap: 10px;\n  }\n</style>\n<div class="grade">\n  <div>1</div><div>2</div><div>3</div>\n</div>\n```\n\n- `display: grid` ativa o grid container\n- `grid-template-columns` define o número e o tamanho das colunas (`1fr` = uma fração do espaço)\n- `gap` define o espaçamento entre as células\n\n## No exercício\n\nAtive o grid e crie 3 colunas iguais com `grid-template-columns: 1fr 1fr 1fr`.',
    'instruction_pt': 'CSS Grid organiza itens em linhas e colunas. Ative o grid com `display: grid` e crie 3 colunas iguais com `grid-template-columns: 1fr 1fr 1fr`.\n\nVeja um exemplo:\n\n```css\n.grade {\n  display: grid;\n  grid-template-columns: 1fr 1fr;\n}\n```',
    'instruction_en': 'CSS Grid organizes items in rows and columns. Activate grid with `display: grid` and create 3 equal columns with `grid-template-columns: 1fr 1fr 1fr`.',
    'instruction_es': 'CSS Grid organiza elementos en filas y columnas. Activa el grid con `display: grid` y crea 3 columnas iguales con `grid-template-columns: 1fr 1fr 1fr`.',
    'starter_code': '<style>\n  .grade {\n    /* Ative o grid com 3 colunas iguais */\n    /* escreva aqui */\n    gap: 10px;\n  }\n</style>\n<div class="grade">\n  <div>1</div><div>2</div><div>3</div>\n</div>\n',
    'hint': 'display: grid; grid-template-columns: 1fr 1fr 1fr;',
    'hints': [
      '`display: grid;` ativa o CSS Grid no container — é o primeiro passo.',
      'Para 3 colunas iguais: `grid-template-columns: 1fr 1fr 1fr;`',
      'O teste verifica `display: grid;` — mas adicione `grid-template-columns` também.',
    ],
    'tests': [
      {
        'stdin': '',
        'expected_stdout': 'display: grid;',
      },
    ],
    'quiz': [
      {
        'question': 'Como ativar o CSS Grid em um container?',
        'options': [
          'grid: true',
          'display: grid',
          'layout: grid',
          'position: grid',
        ],
        'correct': 1,
      },
      {
        'question': 'O que `1fr` representa em grid-template-columns?',
        'options': [
          '1 pixel',
          'Uma fração do espaço disponível',
          '1% da tela',
          '1 elemento fixo',
        ],
        'correct': 1,
      },
    ],
  },
  {
    'order': 17,
    'slug': 'css-responsivo',
    'title': 'Responsividade',
    'chapter': 'Capítulo 4: Layout Moderno',
    'theory': 'Media queries aplicam estilos diferentes dependendo do tamanho da tela — a base do design responsivo.\n\n## Como funciona\n\n```css\n.container {\n  display: flex;\n}\n\n@media (max-width: 600px) {\n  .container {\n    flex-direction: column;\n  }\n}\n```\n\n- `@media (max-width: 600px)` aplica as regras só quando a tela tem até 600px\n- Permite adaptar o layout para celulares, tablets e desktops\n\n## No exercício\n\nCrie uma media query para telas com até 600px que muda `.container` para `flex-direction: column`.',
    'instruction_pt': 'Media queries aplicam estilos só em certas larguras de tela. Crie uma `@media (max-width: 600px)` que muda `.container` para `flex-direction: column`.\n\nVeja um exemplo:\n\n```css\n@media (max-width: 800px) {\n  h1 {\n    font-size: 24px;\n  }\n}\n```',
    'instruction_en': 'Media queries apply styles only at certain screen widths. Create an `@media (max-width: 600px)` that changes `.container` to `flex-direction: column`.',
    'instruction_es': 'Las media queries aplican estilos solo en ciertos anchos de pantalla. Crea un `@media (max-width: 600px)` que cambie `.container` a `flex-direction: column`.',
    'starter_code': '<style>\n  .container {\n    display: flex;\n    flex-direction: row;\n  }\n  /* Em telas de até 600px, mude para coluna */\n  /* escreva aqui */\n</style>\n<div class="container">\n  <p>Item 1</p><p>Item 2</p>\n</div>\n',
    'hint': '@media (max-width: 600px) { .container { flex-direction: column; } }',
    'hints': [
      'Media queries começam com `@media (condição) { regras }`.',
      'Solução: `@media (max-width: 600px) { .container { flex-direction: column; } }`',
      'O teste verifica apenas se `@media (max-width: 600px)` existe no código.',
    ],
    'tests': [
      {
        'stdin': '',
        'expected_stdout': '@media (max-width: 600px)',
      },
    ],
    'quiz': [
      {
        'question': 'Para que servem media queries em CSS?',
        'options': [
          'Para animar elementos',
          'Para aplicar estilos diferentes conforme o tamanho da tela',
          'Para carregar imagens mais rápido',
          'Para criar variáveis',
        ],
        'correct': 1,
      },
      {
        'question': 'Qual a sintaxe correta de uma media query?',
        'options': [
          '@screen (max-width: 600px) { }',
          '@media (max-width: 600px) { }',
          'media: max-width(600px) { }',
          '#media(600px) { }',
        ],
        'correct': 1,
      },
    ],
  },
  {
    'order': 18,
    'slug': 'html-projeto',
    'title': 'Projeto: Cartão de Perfil',
    'chapter': 'Capítulo 4: Layout Moderno',
    'theory': 'Vamos juntar HTML e CSS num mini-projeto: um cartão de perfil com título, parágrafo e estilo.\n\n## Como funciona\n\n```html\n<div class="cartao">\n  <h2>Ana Silva</h2>\n  <p>Desenvolvedora Front-end</p>\n</div>\n\n<style>\n  .cartao {\n    border: 1px solid gray;\n    padding: 16px;\n    text-align: center;\n  }\n</style>\n```\n\nUm componente combina estrutura (HTML) com aparência (CSS) usando uma classe.\n\n## No exercício\n\nComplete o cartão: adicione um `<h2>` com o nome, um `<p>` com a profissão, e a regra `.cartao` com `text-align: center`.',
    'instruction_pt': 'Complete o cartão de perfil:\n\n1. Adicione um `<h2>` com o texto `Ana Silva`\n2. Adicione um `<p>` com o texto `Desenvolvedora Front-end`\n3. Na classe `.cartao`, adicione `text-align: center`\n\nVeja um exemplo com outro cartão:\n\n```html\n<div class="cartao">\n  <h2>Bruno Costa</h2>\n  <p>Designer UX</p>\n</div>\n\n<style>\n  .cartao {\n    border: 1px solid gray;\n    text-align: center;\n  }\n</style>\n```',
    'instruction_en': 'Complete the profile card: add an <h2> with the name, a <p> with the role, and `text-align: center` in `.cartao`.',
    'instruction_es': 'Completa la tarjeta de perfil: agrega un <h2> con el nombre, un <p> con el cargo, y `text-align: center` en `.cartao`.',
    'starter_code': '<div class="cartao">\n  <!-- 1. Adicione um h2 com: Ana Silva -->\n  <!-- escreva aqui -->\n\n  <!-- 2. Adicione um p com: Desenvolvedora Front-end -->\n  <!-- escreva aqui -->\n</div>\n\n<style>\n  .cartao {\n    border: 1px solid gray;\n    padding: 16px;\n    /* 3. Centralize o texto */\n    /* escreva aqui */\n  }\n</style>\n',
    'hint': '<h2>Ana Silva</h2>, <p>Desenvolvedora Front-end</p> e text-align: center;',
    'hints': [
      'Passo 1 e 2 são tags simples: `<h2>Ana Silva</h2>` e `<p>Desenvolvedora Front-end</p>`.',
      'Passo 3: dentro de `.cartao { }`, adicione `text-align: center;`.',
      'O teste verifica `<h2>Ana Silva</h2>` — mas complete os 3 itens.',
    ],
    'tests': [
      {
        'stdin': '',
        'expected_stdout': '<h2>Ana Silva</h2>',
      },
    ],
    'quiz': [
      {
        'question': 'Qual tag é usada para um subtítulo, como o nome em um cartão de perfil?',
        'options': [
          '<h1>',
          '<h2>',
          '<title>',
          '<name>',
        ],
        'correct': 1,
      },
      {
        'question': 'Qual propriedade CSS centraliza o texto horizontalmente dentro de um elemento?',
        'options': [
          'align: center',
          'text-align: center',
          'justify: center',
          'center: true',
        ],
        'correct': 1,
      },
    ],
  },
],

# ── SQL ──────────────────────────────────────────────────────────────────────
"sql": [
  {
    "order": 1,
    "title": "SELECT básico",
    "chapter": "Capítulo 1: Consultando Dados",
    "instruction_pt": "`SELECT` recupera dados de uma tabela. `SELECT * FROM tabela` retorna todas as colunas. Escreva a query completa que seleciona todos os dados da tabela 'usuarios'.",
    "instruction_en": "`SELECT` retrieves data from a table. `SELECT * FROM table` returns all columns.",
    "instruction_es": "`SELECT` recupera datos de una tabla. `SELECT * FROM tabla` devuelve todas las columnas.",
    "starter_code": '-- Selecione todos os dados da tabela "usuarios"\n-- escreva aqui\n',
    "hint": "SELECT * FROM nome_da_tabela;",
    "hints": [
      "`SELECT *` significa 'selecionar todas as colunas' — `FROM` indica a tabela.",
      "Solução: `SELECT * FROM usuarios;` — não esqueça o ponto-e-vírgula no final.",
    ],
    "tests": [{"stdin": "", "expected_stdout": "SELECT * FROM usuarios;"}],
    "quiz": [
      {"question": "Qual cláusula SQL recupera dados de uma tabela?", "options": ["GET", "FETCH", "SELECT", "READ"], "correct": 2},
      {"question": "O que SELECT * faz em SQL?", "options": ["Seleciona a primeira coluna", "Seleciona todas as colunas", "Multiplica os valores", "Seleciona a última linha"], "correct": 1},
    ],
  },
  {
    "order": 2,
    "title": "Filtrando com WHERE",
    "chapter": "Capítulo 1: Consultando Dados",
    "instruction_pt": "`WHERE` filtra as linhas retornadas. Escreva a query que seleciona todos os usuários cuja idade é maior que 18.",
    "instruction_en": "`WHERE` filters returned rows. Write the query that selects all users whose age is greater than 18.",
    "instruction_es": "`WHERE` filtra las filas devueltas. Escribe la consulta que selecciona todos los usuarios con edad mayor a 18.",
    "starter_code": '-- Selecione todos os usuários com idade > 18\n-- escreva aqui\n',
    "hint": "SELECT * FROM tabela WHERE coluna > valor;",
    "hints": [
      "`WHERE` vem depois do `FROM tabela` — e antes usa-se o operador de comparação.",
      "Solução: `SELECT * FROM usuarios WHERE idade > 18;`",
      "Em SQL, `>` (maior que), `<` (menor que), `=` (igual) — note que igualdade usa `=`, não `==`.",
    ],
    "tests": [{"stdin": "", "expected_stdout": "SELECT * FROM usuarios WHERE idade > 18;"}],
    "quiz": [
      {"question": "Qual cláusula SQL filtra linhas por condição?", "options": ["FILTER", "HAVING", "WHERE", "WHEN"], "correct": 2},
      {"question": "Qual operador verifica igualdade no WHERE em SQL?", "options": ["==", ":=", "=", "==="], "correct": 2},
      {"question": "Como filtrar nomes que começam com 'A' em SQL?", "options": ["WHERE nome LIKE 'A%'", "WHERE nome START 'A'", "WHERE nome BEGINS 'A'", "WHERE nome = 'A*'"], "correct": 0},
    ],
  },
  {
    "order": 3,
    "title": "Inserindo dados",
    "chapter": "Capítulo 2: Manipulando Dados",
    "instruction_pt": "`INSERT INTO` adiciona novos registros. Escreva o comando que insere um usuário com nome 'Maria' e email 'maria@email.com' na tabela 'usuarios'.",
    "instruction_en": "`INSERT INTO` adds new records. Write the command that inserts a user with name 'Maria' and email 'maria@email.com'.",
    "instruction_es": "`INSERT INTO` agrega nuevos registros. Escribe el comando que inserta un usuario con nombre 'Maria' y email 'maria@email.com'.",
    "starter_code": "-- Insira um usuário com nome 'Maria' e email 'maria@email.com'\n-- escreva aqui\n",
    "hint": "INSERT INTO tabela (coluna1, coluna2) VALUES ('valor1', 'valor2'); — aspas simples ' ou duplas \" são aceitas.",
    "hints": [
      "Estrutura: `INSERT INTO tabela (colunas) VALUES (valores);`",
      "Solução: `INSERT INTO usuarios (nome, email) VALUES ('Maria', 'maria@email.com');`",
      "Aspas simples ' são convenção SQL — aspas duplas também são aceitas neste exercício.",
    ],
    "tests": [{"stdin": "", "expected_stdout": "INSERT INTO usuarios (nome, email) VALUES ('Maria', 'maria@email.com');"}],
    "quiz": [
      {"question": "Qual comando SQL adiciona novos registros?", "options": ["ADD INTO", "INSERT INTO", "PUT INTO", "CREATE INTO"], "correct": 1},
      {"question": "Na sintaxe INSERT INTO, VALUES contém:", "options": ["As colunas da tabela", "Os nomes das tabelas", "Os valores a inserir", "Os filtros WHERE"], "correct": 2},
    ],
  },
  {
    "order": 4,
    "title": "Atualizando dados",
    "chapter": "Capítulo 2: Manipulando Dados",
    "instruction_pt": "`UPDATE ... SET ... WHERE` atualiza registros existentes. Sempre use `WHERE` para evitar alterar todos os registros. Escreva o comando que atualiza o email do usuário com id=1.",
    "instruction_en": "`UPDATE ... SET ... WHERE` updates existing records. Always use `WHERE` to avoid changing all records.",
    "instruction_es": "`UPDATE ... SET ... WHERE` actualiza registros existentes. Siempre usa `WHERE` para evitar cambiar todos los registros.",
    "starter_code": "-- Atualize o email para 'novo@email.com' do usuário com id = 1\n-- escreva aqui\n",
    "hint": "UPDATE tabela SET coluna = 'valor' WHERE id = 1; — aspas simples ' ou duplas \" são aceitas.",
    "hints": [
      "Estrutura: `UPDATE tabela SET coluna = valor WHERE condição;`",
      "Solução: `UPDATE usuarios SET email = 'novo@email.com' WHERE id = 1;`",
      "SEMPRE use WHERE no UPDATE — sem ele, TODOS os registros serão alterados!",
    ],
    "tests": [{"stdin": "", "expected_stdout": "UPDATE usuarios SET email = 'novo@email.com' WHERE id = 1;"}],
    "quiz": [
      {"question": "Qual cláusula SQL define qual linha atualizar em UPDATE?", "options": ["WHEN", "FILTER", "WHERE", "SET"], "correct": 2},
      {"question": "O que acontece se UPDATE não usar WHERE?", "options": ["Nada", "Atualiza apenas a primeira linha", "Atualiza todos os registros", "Gera erro"], "correct": 2},
    ],
  },
  {
    "order": 5,
    "title": "DELETE",
    "chapter": "Capítulo 2: Manipulando Dados",
    "instruction_pt": "`DELETE FROM` remove registros. **Sempre use `WHERE`** para evitar apagar tudo!\n\n  DELETE FROM tabela WHERE condição;\n\nEscreva o comando que remove o usuário com id = 5.",
    "instruction_en": "`DELETE FROM` removes records. Always use `WHERE` to avoid deleting everything!",
    "instruction_es": "`DELETE FROM` elimina registros. ¡Siempre usa `WHERE` para evitar borrar todo!",
    "starter_code": "-- Remova o usuário com id = 5 da tabela usuarios\n-- escreva aqui\n",
    "hint": "DELETE FROM tabela WHERE coluna = valor;",
    "hints": [
      "Estrutura: `DELETE FROM tabela WHERE condição;` — sem WHERE apaga TUDO!",
      "Solução: `DELETE FROM usuarios WHERE id = 5;`",
      "Em SQL, `id = 5` usa um `=` apenas (não `==` como em Python/JS).",
    ],
    "tests": [{"stdin": "", "expected_stdout": "DELETE FROM usuarios WHERE id = 5;"}],
    "quiz": [
      {"question": "Qual comando SQL remove registros?", "options": ["REMOVE FROM", "DROP FROM", "DELETE FROM", "ERASE FROM"], "correct": 2},
      {"question": "Por que sempre usar WHERE com DELETE?", "options": ["Por convenção", "Para evitar remover todos os registros", "Por performance", "É obrigatório"], "correct": 1},
    ],
  },
  {
    "order": 6,
    "title": "ORDER BY",
    "chapter": "Capítulo 3: Consultando com Estilo",
    "instruction_pt": "`ORDER BY` ordena os resultados. Use `ASC` (crescente, padrão) ou `DESC` (decrescente).\n\n  SELECT * FROM produtos ORDER BY preco DESC;\n\nEscreva a query que lista todos os usuários ordenados por nome em ordem crescente.",
    "instruction_en": "`ORDER BY` sorts results. Use `ASC` (ascending, default) or `DESC` (descending).",
    "instruction_es": "`ORDER BY` ordena los resultados. Usa `ASC` (ascendente) o `DESC` (descendente).",
    "starter_code": "-- Liste todos os usuários ordenados pelo nome (A-Z)\n-- escreva aqui\n",
    "hint": "SELECT * FROM usuarios ORDER BY nome ASC;",
    "hints": [
      "`ORDER BY` vem no final da query, depois do `FROM tabela`.",
      "Solução: `SELECT * FROM usuarios ORDER BY nome ASC;` — ASC = ascendente (A→Z).",
      "O padrão já é ASC — você pode omitir, mas inclua para maior clareza.",
    ],
    "tests": [{"stdin": "", "expected_stdout": "SELECT * FROM usuarios ORDER BY nome ASC;"}],
    "quiz": [
      {"question": "Qual cláusula SQL ordena os resultados?", "options": ["SORT BY", "ORDER BY", "GROUP BY", "ARRANGE BY"], "correct": 1},
      {"question": "Para ordenar em ordem decrescente usa-se:", "options": ["ASC", "DESC", "DOWN", "REVERSE"], "correct": 1},
    ],
  },
  {
    "order": 7,
    "title": "LIMIT",
    "chapter": "Capítulo 3: Consultando com Estilo",
    "instruction_pt": "`LIMIT` restringe o número de linhas retornadas. Muito útil para paginação.\n\n  SELECT * FROM tabela LIMIT 10;\n\nEscreva a query que retorna os 3 primeiros produtos da tabela `produtos`.",
    "instruction_en": "`LIMIT` restricts the number of returned rows. Very useful for pagination.",
    "instruction_es": "`LIMIT` restringe el número de filas devueltas. Muy útil para paginación.",
    "starter_code": "-- Retorne apenas os 3 primeiros produtos\n-- escreva aqui\n",
    "hint": "SELECT * FROM produtos LIMIT 3;",
    "hints": [
      "`LIMIT n` vai no final da query e restringe o número de linhas retornadas.",
      "Solução: `SELECT * FROM produtos LIMIT 3;`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "SELECT * FROM produtos LIMIT 3;"}],
    "quiz": [
      {"question": "Qual cláusula SQL limita o número de linhas retornadas?", "options": ["MAXIMUM", "TOP", "LIMIT", "ROWS"], "correct": 2},
      {"question": "LIMIT é especialmente útil para:", "options": ["Filtrar por data", "Paginação de resultados", "Ordenar dados", "Contar registros"], "correct": 1},
    ],
  },
  {
    "order": 8,
    "title": "Funções de Agregação",
    "chapter": "Capítulo 3: Consultando com Estilo",
    "instruction_pt": "Funções de agregação calculam valores sobre múltiplas linhas:\n- `COUNT(*)` → conta linhas\n- `SUM(coluna)` → soma\n- `AVG(coluna)` → média\n- `MAX/MIN` → máximo/mínimo\n\nEscreva a query que conta o total de usuários.",
    "instruction_en": "Aggregate functions calculate values over multiple rows: COUNT, SUM, AVG, MAX, MIN.",
    "instruction_es": "Las funciones de agregación calculan valores sobre múltiples filas: COUNT, SUM, AVG, MAX, MIN.",
    "starter_code": "-- Conte o número total de usuários na tabela usuarios\n-- escreva aqui\n",
    "hint": "SELECT COUNT(*) FROM usuarios;",
    "hints": [
      "`COUNT(*)` conta todas as linhas de uma tabela.",
      "Solução: `SELECT COUNT(*) FROM usuarios;`",
      "`COUNT(coluna)` ignora NULLs; `COUNT(*)` conta tudo — use `*` para total geral.",
    ],
    "tests": [{"stdin": "", "expected_stdout": "SELECT COUNT(*) FROM usuarios;"}],
    "quiz": [
      {"question": "Qual função SQL conta o total de linhas?", "options": ["SUM(*)", "COUNT(*)", "TOTAL(*)", "NUM(*)"], "correct": 1},
      {"question": "Qual função SQL calcula a média de uma coluna?", "options": ["MEAN()", "AVERAGE()", "AVG()", "MED()"], "correct": 2},
      {"question": "Qual função SQL retorna o maior valor de uma coluna?", "options": ["GREATEST()", "MAX()", "TOP()", "HIGH()"], "correct": 1},
    ],
  },
  {
    "order": 9,
    "title": "GROUP BY",
    "chapter": "Capítulo 3: Consultando com Estilo",
    "instruction_pt": "`GROUP BY` agrupa linhas com o mesmo valor. Sempre usado com funções de agregação.\n\n  SELECT cidade, COUNT(*) FROM clientes GROUP BY cidade;\n\nEscreva a query que mostra quantos usuários existem por cidade.",
    "instruction_en": "`GROUP BY` groups rows with the same value. Always used with aggregate functions.",
    "instruction_es": "`GROUP BY` agrupa filas con el mismo valor. Siempre se usa con funciones de agregación.",
    "starter_code": "-- Mostre quantos usuários existem em cada cidade\n-- escreva aqui\n",
    "hint": "SELECT cidade, COUNT(*) FROM usuarios GROUP BY cidade;",
    "hints": [
      "Selecione a coluna de agrupamento + a função de agregação: `cidade, COUNT(*)`",
      "Solução: `SELECT cidade, COUNT(*) FROM usuarios GROUP BY cidade;`",
      "A coluna no SELECT (cidade) deve ser a mesma no GROUP BY — e vice-versa.",
    ],
    "tests": [{"stdin": "", "expected_stdout": "SELECT cidade, COUNT(*) FROM usuarios GROUP BY cidade;"}],
    "quiz": [
      {"question": "GROUP BY agrupa linhas que possuem:", "options": ["Valores únicos em uma coluna", "Datas iguais", "Qualquer condição", "Linhas consecutivas"], "correct": 0},
      {"question": "GROUP BY sempre é usado junto com:", "options": ["WHERE", "LIMIT", "Funções de agregação", "ORDER BY"], "correct": 2},
    ],
  },
  {
    "order": 10,
    "title": "INNER JOIN",
    "chapter": "Capítulo 4: Relacionamentos",
    "instruction_pt": "`JOIN` combina linhas de duas tabelas com base em uma coluna relacionada.\n`INNER JOIN` retorna apenas as linhas com correspondência em ambas.\n\n  SELECT u.nome, p.produto\n  FROM usuarios u\n  INNER JOIN pedidos p ON u.id = p.usuario_id;\n\nEscreva essa query exatamente.",
    "instruction_en": "`INNER JOIN` combines rows from two tables based on a related column, returning only matching rows.",
    "instruction_es": "`INNER JOIN` combina filas de dos tablas basándose en una columna relacionada.",
    "starter_code": "-- Una usuarios com pedidos pelo id do usuário\n-- Selecione u.nome e p.produto\n-- escreva aqui\n",
    "hint": "SELECT u.nome, p.produto FROM usuarios u INNER JOIN pedidos p ON u.id = p.usuario_id;",
    "hints": [
      "`u` e `p` são aliases (apelidos) para as tabelas — facilitam a escrita.",
      "`ON u.id = p.usuario_id` define como as tabelas se relacionam.",
      "Solução completa: `SELECT u.nome, p.produto FROM usuarios u INNER JOIN pedidos p ON u.id = p.usuario_id;`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "SELECT u.nome, p.produto FROM usuarios u INNER JOIN pedidos p ON u.id = p.usuario_id;"}],
    "quiz": [
      {"question": "O que INNER JOIN retorna?", "options": ["Todos os registros da primeira tabela", "Todos os registros de ambas as tabelas", "Apenas os registros com correspondência em ambas", "Registros sem correspondência"], "correct": 2},
      {"question": "Qual cláusula define a condição de ligação no JOIN?", "options": ["WHERE", "ON", "AND", "USING"], "correct": 1},
    ],
  },
  {
    "order": 11,
    "title": "CREATE TABLE",
    "chapter": "Capítulo 4: Relacionamentos",
    "instruction_pt": "`CREATE TABLE` cria uma nova tabela. Defina as colunas com nome e tipo:\n- `INT` → inteiro\n- `VARCHAR(n)` → texto até n caracteres\n- `DECIMAL(10,2)` → número decimal\n- `PRIMARY KEY` → chave primária\n\nCrie a tabela `produtos` com id (INT), nome (VARCHAR 100) e preco (DECIMAL 10,2).",
    "instruction_en": "`CREATE TABLE` creates a new table. Define columns with name and type.",
    "instruction_es": "`CREATE TABLE` crea una nueva tabla. Define las columnas con nombre y tipo.",
    "starter_code": "-- Crie a tabela produtos com id (INT), nome (VARCHAR(100)) e preco (DECIMAL(10,2))\n-- escreva aqui\n",
    "hint": "CREATE TABLE produtos (id INT, nome VARCHAR(100), preco DECIMAL(10,2));",
    "hints": [
      "Estrutura: `CREATE TABLE nome (coluna1 TIPO, coluna2 TIPO, ...);`",
      "Solução: `CREATE TABLE produtos (id INT, nome VARCHAR(100), preco DECIMAL(10,2));`",
      "`DECIMAL(10,2)` significa: até 10 dígitos no total, 2 deles decimais — ex: 99999999.99",
    ],
    "tests": [{"stdin": "", "expected_stdout": "CREATE TABLE produtos (id INT, nome VARCHAR(100), preco DECIMAL(10,2));"}],
    "quiz": [
      {"question": "Qual comando SQL cria uma nova tabela?", "options": ["NEW TABLE", "ADD TABLE", "CREATE TABLE", "MAKE TABLE"], "correct": 2},
      {"question": "Qual tipo SQL armazena texto de tamanho variável?", "options": ["TEXT()", "CHAR", "VARCHAR(n)", "STRING"], "correct": 2},
      {"question": "O que é PRIMARY KEY em SQL?", "options": ["A primeira coluna da tabela", "Um índice único que identifica cada registro", "Uma senha da tabela", "A chave de criptografia"], "correct": 1},
    ],
  },
  {
    "order": 12,
    "title": "ALTER TABLE",
    "chapter": "Capítulo 4: Relacionamentos",
    "instruction_pt": "`ALTER TABLE` modifica uma tabela existente. Use `ADD COLUMN` para adicionar colunas, `DROP COLUMN` para remover.\n\n  ALTER TABLE clientes ADD COLUMN telefone VARCHAR(15);\n\nEscreva o comando que adiciona a coluna `telefone` (VARCHAR 15) à tabela `usuarios`.",
    "instruction_en": "`ALTER TABLE` modifies an existing table. Use `ADD COLUMN` to add columns.",
    "instruction_es": "`ALTER TABLE` modifica una tabla existente. Usa `ADD COLUMN` para agregar columnas.",
    "starter_code": "-- Adicione a coluna telefone (VARCHAR(15)) à tabela usuarios\n-- escreva aqui\n",
    "hint": "ALTER TABLE usuarios ADD COLUMN telefone VARCHAR(15);",
    "hints": [
      "Estrutura: `ALTER TABLE tabela ADD COLUMN nome_coluna TIPO;`",
      "Solução: `ALTER TABLE usuarios ADD COLUMN telefone VARCHAR(15);`",
      "`VARCHAR(15)` permite até 15 caracteres — ideal para números de telefone.",
    ],
    "tests": [{"stdin": "", "expected_stdout": "ALTER TABLE usuarios ADD COLUMN telefone VARCHAR(15);"}],
    "quiz": [
      {"question": "Qual comando SQL modifica a estrutura de uma tabela?", "options": ["MODIFY TABLE", "CHANGE TABLE", "ALTER TABLE", "UPDATE TABLE"], "correct": 2},
      {"question": "Como adicionar uma coluna com ALTER TABLE?", "options": ["ADD COLUMN", "INSERT COLUMN", "APPEND COLUMN", "NEW COLUMN"], "correct": 0},
    ],
  },
],

# ── TypeScript ───────────────────────────────────────────────────────────────
"typescript": [
  {
    "order": 1,
    "title": "Tipos básicos",
    "chapter": "Capítulo 1: Tipagem Estática",
    "instruction_pt": "TypeScript adiciona tipos ao JavaScript. `let nome: string` garante que a variável só aceita texto. Escreva a declaração de uma variável `nome` do tipo `string` sem valor inicial.",
    "instruction_en": "TypeScript adds types to JavaScript. Write the declaration of a `nome` variable of type `string` with no initial value.",
    "instruction_es": "TypeScript añade tipos a JavaScript. Escribe la declaración de una variable `nome` de tipo `string` sin valor inicial.",
    "starter_code": '// Declare a variável "nome" com tipo string (sem valor inicial)\n// escreva aqui\n',
    "hint": "Sintaxe: let nome: string;",
    "hints": [
      "Em TypeScript, o tipo fica após o nome da variável com `:` — `let nome: tipo`",
      "Solução: `let nome: string;` — não esqueça o ponto-e-vírgula.",
    ],
    "tests": [{"stdin": "", "expected_stdout": "let nome: string;"}],
    "quiz": [
      {"question": "O que TypeScript adiciona ao JavaScript?", "options": ["Mais velocidade de execução", "Tipagem estática", "CSS-in-JS", "Banco de dados embutido"], "correct": 1},
      {"question": "Como declarar uma variável string em TypeScript?", "options": ["let nome = string", "string nome;", "let nome: string;", "var nome as string;"], "correct": 2},
    ],
  },
  {
    "order": 2,
    "title": "Função tipada",
    "chapter": "Capítulo 1: Tipagem Estática",
    "instruction_pt": "Em TypeScript, funções têm tipos nos parâmetros e no retorno: `function nome(a: tipo): tipoRetorno`. Escreva a assinatura de uma função `somar` que recebe dois `number` e retorna `number`.",
    "instruction_en": "In TypeScript, functions have typed parameters and return types. Write the signature of a `somar` function that takes two `number` and returns `number`.",
    "instruction_es": "En TypeScript, las funciones tienen tipos en los parámetros y en el retorno.",
    "starter_code": '// Escreva a assinatura (apenas a primeira linha) da função somar\n// function somar(??): ?? {\n// escreva aqui\n',
    "hint": "function somar(a: number, b: number): number {",
    "hints": [
      "Tipos nos parâmetros: `(a: number, b: number)` — tipo de retorno vem após os parênteses.",
      "Solução: `function somar(a: number, b: number): number {`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "function somar(a: number, b: number): number {"}],
    "quiz": [
      {"question": "Como especificar o tipo de retorno de uma função TypeScript?", "options": ["function f() as number", "function f(): number", "function f() -> number", "function f() => number"], "correct": 1},
      {"question": "Uma vantagem de tipar funções em TypeScript é:", "options": ["Código mais lento", "Evitar erros de tipo em tempo de compilação", "Menos linhas de código", "Compatibilidade com Python"], "correct": 1},
    ],
  },
  {
    "order": 3,
    "title": "Interface",
    "chapter": "Capítulo 2: Tipos Avançados",
    "instruction_pt": "Interfaces definem a forma de objetos. Escreva a interface `Aluno` com os campos `nome` (string) e `idade` (number) em uma linha, sem quebras de linha.",
    "instruction_en": "Interfaces define the shape of objects. Write the `Aluno` interface with fields `nome` (string) and `idade` (number) on one line.",
    "instruction_es": "Las interfaces definen la forma de los objetos. Escribe la interfaz `Aluno` con los campos `nome` (string) y `idade` (number) en una línea.",
    "starter_code": '// Escreva a interface Aluno com dois campos: nome (string) e idade (number)\n// Formato: interface NomeInterface { campo: tipo; campo2: tipo; }\n// escreva aqui\n',
    "hint": "interface NomeInterface { campo: tipo; campo2: tipo; }",
    "hints": [
      "Interface define a 'forma' de um objeto — chaves e tipos de cada campo.",
      "Solução: `interface Aluno { nome: string; idade: number; }`",
      "Campos separados por `;` dentro das chaves `{}` — tudo em uma única linha.",
    ],
    "tests": [{"stdin": "", "expected_stdout": "interface Aluno { nome: string; idade: number; }"}],
    "quiz": [
      {"question": "Qual palavra-chave define uma interface em TypeScript?", "options": ["type", "interface", "struct", "schema"], "correct": 1},
      {"question": "Interfaces em TypeScript servem para:", "options": ["Executar funções", "Definir a forma esperada de objetos", "Criar loops", "Declarar variáveis globais"], "correct": 1},
      {"question": "Uma interface pode ter diferentes tipos nas propriedades?", "options": ["Não", "Sim, cada propriedade tem seu próprio tipo", "Apenas tipos primitivos", "Apenas string e number"], "correct": 1},
    ],
  },
  {
    "order": 4,
    "title": "Type Alias",
    "chapter": "Capítulo 2: Tipos Avançados",
    "instruction_pt": "`type` cria um apelido para um tipo. Útil para reutilização. Escreva o type alias `Cor` que aceita os valores literais `'vermelho'`, `'azul'` ou `'verde'`.",
    "instruction_en": "`type` creates an alias for a type. Write the type alias `Cor` that accepts the literal values `'vermelho'`, `'azul'` or `'verde'`.",
    "instruction_es": "`type` crea un alias para un tipo. Escribe el type alias `Cor` que acepta los valores literales `'vermelho'`, `'azul'` o `'verde'`.",
    "starter_code": "// Escreva o type alias Cor com três cores: vermelho, azul e verde\n// Dica: type NomeAlias = 'valor1' | 'valor2' | 'valor3';\n// escreva aqui\n",
    "hint": "type NomeAlias = 'valor1' | 'valor2' | 'valor3'; — aspas simples ' ou duplas \" são aceitas.",
    "hints": [
      "Type alias usa `type NomeAlias = ...` e union types usam `|` para separar opções.",
      "Solução: `type Cor = 'vermelho' | 'azul' | 'verde';`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "type Cor = 'vermelho' | 'azul' | 'verde';"}],
    "quiz": [
      {"question": "O que um type alias faz em TypeScript?", "options": ["Renomeia variáveis", "Cria um apelido reutilizável para um tipo", "Define uma interface", "Cria uma classe"], "correct": 1},
      {"question": "Qual símbolo separa valores em union types?", "options": ["&", "|", "+", "~"], "correct": 1},
    ],
  },
  {
    "order": 5,
    "title": "Union Types",
    "chapter": "Capítulo 2: Tipos Avançados",
    "instruction_pt": "Union types permitem que uma variável aceite mais de um tipo. Use `|` para combinar tipos. Declare a variável `id` que pode ser `number` ou `string`.",
    "instruction_en": "Union types allow a variable to accept more than one type. Use `|` to combine types. Declare the variable `id` that can be `number` or `string`.",
    "instruction_es": "Los union types permiten que una variable acepte más de un tipo. Declara la variable `id` que puede ser `number` o `string`.",
    "starter_code": "// Declare a variável id que aceita number OU string\n// escreva aqui\n",
    "hint": "let variavel: tipo1 | tipo2;",
    "hints": [
      "Union types usam `|` para combinar dois ou mais tipos — `tipo1 | tipo2`.",
      "Solução: `let id: number | string;`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "let id: number | string;"}],
    "quiz": [
      {"question": "O que let id: number | string significa?", "options": ["id pode ser number e string ao mesmo tempo", "id pode ser number ou string", "id é do tipo number_string", "Erro de sintaxe"], "correct": 1},
      {"question": "Union types usam qual operador?", "options": ["+", "&", "|", "~"], "correct": 2},
    ],
  },
  {
    "order": 6,
    "title": "Arrays Tipados",
    "chapter": "Capítulo 3: Coleções",
    "instruction_pt": "Em TypeScript, arrays têm tipos: `number[]` é um array de números. Declare a variável `numeros` como um array de `number` com os valores `[1, 2, 3]`.",
    "instruction_en": "In TypeScript, arrays have types: `number[]` is an array of numbers. Declare the variable `numeros` as an array of `number` with values `[1, 2, 3]`.",
    "instruction_es": "En TypeScript, los arrays tienen tipos. Declara la variable `numeros` como un array de `number` con los valores `[1, 2, 3]`.",
    "starter_code": "// Declare o array numeros do tipo number[] com valores [1, 2, 3]\n// escreva aqui\n",
    "hint": "let variavel: tipo[] = [valor1, valor2, valor3];",
    "hints": [
      "Arrays tipados em TypeScript: `tipo[]` — ex: `number[]` para array de números.",
      "Solução: `let numeros: number[] = [1, 2, 3];`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "let numeros: number[] = [1, 2, 3];"}],
    "quiz": [
      {"question": "Como declarar um array de strings em TypeScript?", "options": ["string array", "Array(string)", "string[]", "list<string>"], "correct": 2},
      {"question": "O que number[] representa em TypeScript?", "options": ["Um número com índice", "Um array de números", "Uma matriz 2D", "Um tipo numérico especial"], "correct": 1},
    ],
  },
  {
    "order": 7,
    "title": "Propriedade Opcional",
    "chapter": "Capítulo 2: Tipos Avançados",
    "instruction_pt": "Em interfaces, adicione `?` após o nome do campo para torná-lo opcional. Escreva a interface `Config` com a propriedade opcional `debug` do tipo `boolean`.",
    "instruction_en": "In interfaces, add `?` after the field name to make it optional. Write the `Config` interface with an optional `debug` property of type `boolean`.",
    "instruction_es": "En las interfaces, añade `?` después del nombre del campo para hacerlo opcional. Escribe la interfaz `Config` con la propiedad opcional `debug` de tipo `boolean`.",
    "starter_code": "// Escreva a interface Config com a propriedade opcional debug do tipo boolean\n// Use ? após o nome do campo para torná-lo opcional\n// escreva aqui\n",
    "hint": "interface NomeInterface { campo?: tipo; }",
    "hints": [
      "O `?` após o nome do campo torna-o opcional — sem `?` o campo é obrigatório.",
      "Solução: `interface Config { debug?: boolean; }`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "interface Config { debug?: boolean; }"}],
    "quiz": [
      {"question": "Como marcar uma propriedade como opcional em interface TypeScript?", "options": ["Colocar ! após o nome", "Colocar ? após o nome", "Usar o tipo optional", "Adicionar | undefined"], "correct": 1},
      {"question": "interface Config { debug?: boolean } significa:", "options": ["debug é obrigatório boolean", "debug pode estar ausente ou ser boolean", "debug é sempre true", "debug aceita qualquer tipo"], "correct": 1},
    ],
  },
  {
    "order": 8,
    "title": "Enum",
    "chapter": "Capítulo 4: Recursos Avançados",
    "instruction_pt": "`enum` define um conjunto nomeado de constantes. Escreva o enum `Direcao` com os membros `Norte`, `Sul`, `Leste` e `Oeste` em uma linha.",
    "instruction_en": "`enum` defines a named set of constants. Write the `Direcao` enum with members `Norte`, `Sul`, `Leste` and `Oeste` on one line.",
    "instruction_es": "`enum` define un conjunto nombrado de constantes. Escribe el enum `Direcao` con los miembros `Norte`, `Sul`, `Leste` y `Oeste` en una línea.",
    "starter_code": "// Escreva o enum Direcao com os membros: Norte, Sul, Leste, Oeste\n// Dica: enum NomeEnum { Membro1, Membro2, Membro3, Membro4 }\n// escreva aqui\n",
    "hint": "enum NomeEnum { Membro1, Membro2, Membro3, Membro4 }",
    "hints": [
      "`enum` agrupa constantes nomeadas — sem aspas nos membros, separados por vírgula.",
      "Solução: `enum Direcao { Norte, Sul, Leste, Oeste }`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "enum Direcao { Norte, Sul, Leste, Oeste }"}],
    "quiz": [
      {"question": "Para que serve enum em TypeScript?", "options": ["Criar loops", "Definir um conjunto de constantes nomeadas", "Fazer herança", "Importar módulos"], "correct": 1},
      {"question": "Qual é o valor padrão de enum Cor { Vermelho, Azul }?", "options": ["'Vermelho', 'Azul'", "null, null", "0, 1", "1, 2"], "correct": 2},
    ],
  },
  {
    "order": 9,
    "title": "Generics",
    "chapter": "Capítulo 4: Recursos Avançados",
    "instruction_pt": "Generics permitem criar funções e classes reutilizáveis para qualquer tipo. Escreva a assinatura da função genérica `identidade` que recebe um parâmetro `valor` do tipo `T` e retorna `T`.",
    "instruction_en": "Generics allow creating reusable functions for any type. Write the signature of the generic function `identidade` that receives a parameter `valor` of type `T` and returns `T`.",
    "instruction_es": "Los generics permiten crear funciones reutilizables para cualquier tipo. Escribe la firma de la función genérica `identidade`.",
    "starter_code": "// Escreva a assinatura da função genérica identidade<T>\n// que recebe um parâmetro (valor: T) e retorna T\n// escreva aqui\n",
    "hint": "function nomeFuncao<T>(param: T): T {",
    "hints": [
      "`<T>` é o parâmetro de tipo — colocado entre o nome da função e os parênteses.",
      "O parâmetro e o retorno usam o mesmo `T`: `(valor: T): T`",
      "Solução: `function identidade<T>(valor: T): T {`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "function identidade<T>(valor: T): T {"}],
    "quiz": [
      {"question": "O que <T> representa em uma função genérica TypeScript?", "options": ["O nome da função", "Um tipo que será definido na chamada", "TypeScript interno", "Um template HTML"], "correct": 1},
      {"question": "A vantagem dos generics é:", "options": ["Código mais rápido", "Reutilização tipada para qualquer tipo", "Menos memória", "Compilação mais rápida"], "correct": 1},
    ],
  },
  {
    "order": 10,
    "title": "Classe Tipada",
    "chapter": "Capítulo 4: Recursos Avançados",
    "instruction_pt": "Classes em TypeScript podem ter propriedades tipadas no construtor usando `public`. Escreva a linha `constructor` da classe `Animal` com a propriedade pública `nome: string`.",
    "instruction_en": "TypeScript classes can have typed properties in the constructor using `public`. Write the `constructor` line of the `Animal` class with the public property `nome: string`.",
    "instruction_es": "Las clases TypeScript pueden tener propiedades tipadas en el constructor con `public`. Escribe la línea `constructor` de la clase `Animal`.",
    "starter_code": "// Escreva o constructor da classe Animal\n// com a propriedade pública nome do tipo string\n// escreva aqui\n",
    "hint": "constructor(public nomeProp: tipo) {}",
    "hints": [
      "`public` dentro do constructor cria e atribui a propriedade automaticamente — sem precisar de `this.nome = nome`.",
      "Solução: `constructor(public nome: string) {}`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "constructor(public nome: string) {}"}],
    "quiz": [
      {"question": "O que 'public' faz no constructor de uma classe TypeScript?", "options": ["Deixa a classe pública", "Cria e atribui automaticamente a propriedade", "Permite herança", "Define o tipo de retorno"], "correct": 1},
      {"question": "Classes TypeScript funcionam de modo similar a:", "options": ["Python (def)", "Java/C++ (class com tipos)", "Go (struct)", "Lua (table)"], "correct": 1},
    ],
  },
],

# ── Java ─────────────────────────────────────────────────────────────────────
"java": [
  {
    "order": 1,
    "title": "Imprimir no console",
    "chapter": "Capítulo 1: Fundamentos Java",
    "instruction_pt": "Java usa `System.out.println()` para imprimir no console. Escreva apenas o comando que imprime 'Olá, Java!'.",
    "instruction_en": "Java uses `System.out.println()` to print to the console. Write only the command that prints 'Olá, Java!'.",
    "instruction_es": "Java usa `System.out.println()` para imprimir en la consola. Escribe solo el comando que imprime 'Olá, Java!'.",
    "starter_code": 'public class Main {\n    public static void main(String[] args) {\n        // Escreva o comando para imprimir "Olá, Java!"\n        // escreva aqui\n    }\n}\n',
    "hint": "System.out.println(\"Olá, Java!\"); — aspas simples ' ou duplas \" são aceitas neste exercício.",
    "hints": [
      "Em Java, `System.out.println()` imprime texto com quebra de linha automática.",
      "Solução: `System.out.println(\"Olá, Java!\");` — não esqueça o ponto-e-vírgula.",
    ],
    "tests": [{"stdin": "", "expected_stdout": 'System.out.println("Olá, Java!");'}],
    "quiz": [
      {"question": "Como imprimir texto com quebra de linha em Java?", "options": ["System.print()", "Console.log()", "System.out.println()", "print()"], "correct": 2},
      {"question": "O que System.out.print() faz diferente de println()?", "options": ["Imprime em vermelho", "Não adiciona quebra de linha no final", "Imprime em maiúsculas", "Salva em arquivo"], "correct": 1},
    ],
  },
  {
    "order": 2,
    "title": "Declarando variáveis",
    "chapter": "Capítulo 1: Fundamentos Java",
    "instruction_pt": "Java é fortemente tipado — toda variável precisa de um tipo. `int` para inteiros, `String` para texto. Escreva a declaração de um inteiro `idade` com valor 25.",
    "instruction_en": "Java is strongly typed — every variable needs a type. Write the declaration of an integer `idade` with value 25.",
    "instruction_es": "Java es fuertemente tipado. Escribe la declaración de un entero `idade` con valor 25.",
    "starter_code": '// Declare um inteiro chamado "idade" com valor 25\n// escreva aqui\n',
    "hint": "int nomeDaVariavel = valor;",
    "hints": [
      "Em Java, o tipo vem antes do nome: `int nome = valor;` — sem `var` ou `let`.",
      "Solução: `int idade = 25;` — não esqueça o ponto-e-vírgula.",
    ],
    "tests": [{"stdin": "", "expected_stdout": "int idade = 25;"}],
    "quiz": [
      {"question": "Como declarar um inteiro em Java?", "options": ["integer x = 5;", "Int x = 5;", "int x = 5;", "number x = 5;"], "correct": 2},
      {"question": "Java é uma linguagem:", "options": ["Dinamicamente tipada", "Fortemente tipada (requer declaração de tipo)", "Sem tipos", "Tipada opcionalmente"], "correct": 1},
    ],
  },
  {
    "order": 3,
    "title": "Método estático",
    "chapter": "Capítulo 2: Orientação a Objetos",
    "instruction_pt": "Métodos em Java são declarados com `public static TipoRetorno nomeMetodo(Tipo param)`. Escreva a assinatura do método `dobrar` que recebe e retorna `int`.",
    "instruction_en": "Methods in Java are declared with `public static ReturnType methodName(Type param)`. Write the signature of the `dobrar` method that receives and returns `int`.",
    "instruction_es": "Los métodos en Java se declaran con `public static TipoRetorno nombreMetodo(Tipo param)`. Escribe la firma del método `dobrar`.",
    "starter_code": '// Escreva apenas a assinatura do método dobrar (sem o corpo)\n// Recebe int n e retorna int\n// escreva aqui\n',
    "hint": "public static int dobrar(int n) {",
    "hints": [
      "Estrutura: `public static tipoRetorno nomeMetodo(Tipo param) {`",
      "Solução: `public static int dobrar(int n) {`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "public static int dobrar(int n) {"}],
    "quiz": [
      {"question": "O que 'static' significa em um método Java?", "options": ["O método não muda", "O método pertence à classe, não a uma instância", "O método é privado", "O método é final"], "correct": 1},
      {"question": "Qual é o tipo de retorno void em Java?", "options": ["Retorna zero", "Retorna string vazia", "Não retorna nada", "Retorna null sempre"], "correct": 2},
    ],
  },
  {
    "order": 4,
    "title": "Arrays",
    "chapter": "Capítulo 2: Orientação a Objetos",
    "instruction_pt": "Arrays em Java têm tamanho fixo e tipo declarado. Escreva a declaração do array `numeros` do tipo `int[]` com os valores `{1, 2, 3}` em uma linha.",
    "instruction_en": "Arrays in Java have a fixed size and a declared type. Write the declaration of the `numeros` array of type `int[]` with values `{1, 2, 3}` on one line.",
    "instruction_es": "Los arrays en Java tienen tamaño fijo y tipo declarado. Escribe la declaración del array `numeros` de tipo `int[]` con los valores `{1, 2, 3}`.",
    "starter_code": "// Declare um array de inteiros chamado numeros com os valores 1, 2 e 3\n// Dica: tipo[] nome = {val1, val2, val3};\n// escreva aqui\n",
    "hint": "int[] nomeArray = {val1, val2, val3};",
    "hints": [
      "Sintaxe de array Java: `tipo[] nome = {val1, val2, val3};` — chaves `{}` para inicializar.",
      "Solução: `int[] numeros = {1, 2, 3};`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "int[] numeros = {1, 2, 3};"}],
    "quiz": [
      {"question": "Arrays em Java têm tamanho:", "options": ["Dinâmico (cresce automaticamente)", "Fixo (definido na criação)", "Indefinido", "Limitado a 100 elementos"], "correct": 1},
      {"question": "Como acessar o terceiro elemento de int[] arr em Java?", "options": ["arr[3]", "arr.get(3)", "arr[2]", "arr.third()"], "correct": 2},
    ],
  },
  {
    "order": 5,
    "title": "Condicionais",
    "chapter": "Capítulo 3: Controle de Fluxo",
    "instruction_pt": "Java usa `if (condição) { ... } else { ... }` para tomar decisões. Escreva a estrutura `if` que verifica se a variável `x` é maior que zero e imprime `'positivo'`.",
    "instruction_en": "Java uses `if (condition) { ... } else { ... }` to make decisions. Write the `if` structure that checks if variable `x` is greater than zero and prints `'positivo'`.",
    "instruction_es": "Java usa `if (condición) { ... } else { ... }` para tomar decisiones. Escribe la estructura `if` que verifica si la variable `x` es mayor que cero.",
    "starter_code": "// Escreva o cabeçalho do if que verifica se a variável x é maior que zero\n// Dica: if (condicao) {\n// escreva aqui\n",
    "hint": "if (variavel > 0) {",
    "hints": [
      "Em Java, a condição do `if` fica entre parênteses: `if (condição) {`",
      "Solução: `if (x > 0) {`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "if (x > 0) {"}],
    "quiz": [
      {"question": "Java usa parênteses na condição do if?", "options": ["Não, é opcional", "Sim, são obrigatórios", "Só em else if", "Depende da versão"], "correct": 1},
      {"question": "Como escrever else-if em Java?", "options": ["elseif (cond)", "elif (cond)", "else if (cond)", "otherwise (cond)"], "correct": 2},
    ],
  },
  {
    "order": 6,
    "title": "Loop For",
    "chapter": "Capítulo 3: Controle de Fluxo",
    "instruction_pt": "O `for` em Java tem três partes: inicialização, condição e incremento. Escreva o cabeçalho do `for` que conta de 0 até 4 (i < 5).",
    "instruction_en": "The `for` in Java has three parts: initialization, condition, and increment. Write the header of the `for` that counts from 0 to 4 (i < 5).",
    "instruction_es": "El `for` en Java tiene tres partes: inicialización, condición e incremento. Escribe el encabezado del `for` que cuenta de 0 a 4.",
    "starter_code": "// Escreva o cabeçalho do for que conta de 0 a 4 (i menor que 5)\n// Dica: for (inicializacao; condicao; incremento) {\n// escreva aqui\n",
    "hint": "for (int i = 0; i < 5; i++) {",
    "hints": [
      "Estrutura: `for (inicialização; condição; incremento) {` — separadas por `;`.",
      "Solução: `for (int i = 0; i < 5; i++) {`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "for (int i = 0; i < 5; i++) {"}],
    "quiz": [
      {"question": "Qual é a ordem das partes do for em Java?", "options": ["condição; incremento; init", "init; condição; incremento", "incremento; init; condição", "init; incremento; condição"], "correct": 1},
      {"question": "O que i++ faz em Java?", "options": ["Multiplica por i", "Incrementa i em 1", "Decrementa i em 1", "Reinicia i"], "correct": 1},
    ],
  },
  {
    "order": 7,
    "title": "String em Java",
    "chapter": "Capítulo 3: Controle de Fluxo",
    "instruction_pt": "`String` em Java é uma classe. Use o método `.length()` para obter o número de caracteres. Escreva a linha que declara a `String` chamada `msg` com o valor `'Olá'` e em seguida chama `msg.length()`.",
    "instruction_en": "`String` in Java is a class. Use the `.length()` method to get the number of characters. Write the declaration of the `String` `msg` with value `'Olá'`.",
    "instruction_es": "`String` en Java es una clase. Escribe la declaración de la `String` llamada `msg` con el valor `'Olá'`.",
    "starter_code": "// Declare uma String chamada msg com o valor Olá\n// Dica: String nomeDaVariavel = \"valor\";\n// escreva aqui\n",
    "hint": "String nomeDaVariavel = \"valor\"; — aspas simples ' ou duplas \" são aceitas.",
    "hints": [
      "Em Java, `String` (com S maiúsculo) é uma classe — declare como: `String nome = \"valor\";`",
      "Solução: `String msg = \"Olá\";`",
    ],
    "tests": [{"stdin": "", "expected_stdout": 'String msg = "Olá";'}],
    "quiz": [
      {"question": "Em Java, String é:", "options": ["Um tipo primitivo como int", "Uma classe (objeto)", "Um array de char básico", "Um tipo numérico"], "correct": 1},
      {"question": "Como obter o número de caracteres de uma String em Java?", "options": ["str.size()", "str.count()", "str.len", "str.length()"], "correct": 3},
    ],
  },
  {
    "order": 8,
    "title": "ArrayList",
    "chapter": "Capítulo 4: Coleções",
    "instruction_pt": "`ArrayList` é uma lista dinâmica em Java. Use `ArrayList<Tipo> nome = new ArrayList<>();` para criar uma. Escreva a declaração de um ArrayList de String chamado `nomes`.",
    "instruction_en": "`ArrayList` is a dynamic list in Java. Write the declaration of an ArrayList of String named `nomes`.",
    "instruction_es": "`ArrayList` es una lista dinámica en Java. Escribe la declaración de un ArrayList de String llamado `nomes`.",
    "starter_code": "// Declare um ArrayList de String chamado nomes\n// Dica: ArrayList<Tipo> nome = new ArrayList<>();\n// escreva aqui\n",
    "hint": "ArrayList<Tipo> nomeDaLista = new ArrayList<>();",
    "hints": [
      "`ArrayList<Tipo>` usa generics para definir o tipo dos elementos.",
      "`new ArrayList<>()` — o `<>` é o 'diamond operator', o tipo é inferido.",
      "Solução: `ArrayList<String> nomes = new ArrayList<>();`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "ArrayList<String> nomes = new ArrayList<>();"}],
    "quiz": [
      {"question": "Qual é a diferença entre Array e ArrayList em Java?", "options": ["Array é mais lento", "ArrayList tem tamanho dinâmico, Array tem tamanho fixo", "ArrayList não aceita objetos", "São idênticos"], "correct": 1},
      {"question": "Qual método adiciona elemento ao ArrayList em Java?", "options": ["append()", "push()", "add()", "insert()"], "correct": 2},
    ],
  },
  {
    "order": 9,
    "title": "Classe com Construtor",
    "chapter": "Capítulo 4: Coleções",
    "instruction_pt": "Uma classe em Java agrupa dados e comportamentos. Escreva a assinatura do construtor da classe `Pessoa` que recebe o parâmetro `String nome` e atribui `this.nome = nome`.",
    "instruction_en": "A class in Java groups data and behavior. Write the constructor signature of the `Pessoa` class that receives `String nome` and assigns `this.nome = nome`.",
    "instruction_es": "Una clase en Java agrupa datos y comportamientos. Escribe la firma del constructor de la clase `Pessoa`.",
    "starter_code": "// Escreva o construtor da classe Pessoa que recebe String nome\n// Dica: NomeDaClasse(Tipo parametro) {\n// escreva aqui\n",
    "hint": "NomeDaClasse(Tipo parametro) {",
    "hints": [
      "O construtor tem o mesmo nome da classe e não tem tipo de retorno.",
      "Dentro do construtor, use `this.campo = parametro` para atribuir.",
      "Solução: `Pessoa(String nome) {`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "Pessoa(String nome) {"}],
    "quiz": [
      {"question": "O construtor de uma classe Java:", "options": ["Tem o mesmo nome da classe", "Sempre retorna void", "É chamado com 'create'", "É opcional em toda classe"], "correct": 0},
      {"question": "O que 'this' representa no construtor Java?", "options": ["A classe pai", "A instância sendo criada", "O método main", "O pacote atual"], "correct": 1},
    ],
  },
  {
    "order": 10,
    "title": "Herança",
    "chapter": "Capítulo 5: Herança",
    "instruction_pt": "Herança em Java usa a palavra-chave `extends`. A subclasse herda todos os métodos e atributos da superclasse. Escreva a declaração da classe `Aluno` que herda de `Pessoa`.",
    "instruction_en": "Inheritance in Java uses the keyword `extends`. Write the declaration of the class `Aluno` that extends `Pessoa`.",
    "instruction_es": "La herencia en Java usa la palabra clave `extends`. Escribe la declaración de la clase `Aluno` que hereda de `Pessoa`.",
    "starter_code": "// Escreva a declaração da classe Aluno que herda de Pessoa\n// Dica: public class SubClasse extends SuperClasse {\n// escreva aqui\n",
    "hint": "public class SubClasse extends SuperClasse {",
    "hints": [
      "Herança em Java usa `extends`: `public class Filha extends Mae {`",
      "Solução: `public class Aluno extends Pessoa {`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "public class Aluno extends Pessoa {"}],
    "quiz": [
      {"question": "Qual palavra-chave implementa herança em Java?", "options": ["inherits", "implements", "extends", ":"], "correct": 2},
      {"question": "Uma classe Java pode herdar de quantas classes simultaneamente?", "options": ["Quantas quiser", "Apenas uma", "Máximo de três", "Apenas de classes abstratas"], "correct": 1},
    ],
  },
],

# ── C++ ──────────────────────────────────────────────────────────────────────
"cpp": [
  {
    "order": 1,
    "title": "Saída no console",
    "chapter": "Capítulo 1: Fundamentos C++",
    "instruction_pt": "C++ usa `cout << \"texto\" << endl;` para exibir texto. `endl` quebra a linha. Escreva o comando que exibe 'Olá, C++!'.",
    "instruction_en": "C++ uses `cout << \"text\" << endl;` to display text. Write the command that displays 'Olá, C++!'.",
    "instruction_es": "C++ usa `cout << \"texto\" << endl;` para mostrar texto. Escribe el comando que muestra 'Olá, C++!'.",
    "starter_code": '#include <iostream>\nusing namespace std;\nint main() {\n    // Escreva o comando para exibir "Olá, C++!"\n    // escreva aqui\n    return 0;\n}\n',
    "hint": "cout << \"Olá, C++!\" << endl; — aspas simples ' ou duplas \" são aceitas neste exercício.",
    "hints": [
      "`cout` envia texto para o console — use `<<` para cada parte: `cout << \"texto\" << endl;`",
      "Solução: `cout << \"Olá, C++!\" << endl;`",
    ],
    "tests": [{"stdin": "", "expected_stdout": 'cout << "Olá, C++!" << endl;'}],
    "quiz": [
      {"question": "Qual objeto exibe texto no console em C++?", "options": ["System.out", "Console", "cout", "print"], "correct": 2},
      {"question": "O que 'endl' faz em C++?", "options": ["Finaliza o programa", "Quebra a linha (equivalente a \\n)", "Limpa o buffer", "Define o fim do array"], "correct": 1},
    ],
  },
  {
    "order": 2,
    "title": "Declarando variáveis",
    "chapter": "Capítulo 1: Fundamentos C++",
    "instruction_pt": "C++ exige declaração de tipo: `int`, `double`, `string`. Escreva a declaração de um inteiro `nota` com valor 10.",
    "instruction_en": "C++ requires type declaration: `int`, `double`, `string`. Write the declaration of an integer `nota` with value 10.",
    "instruction_es": "C++ requiere declaración de tipo. Escribe la declaración de un entero `nota` con valor 10.",
    "starter_code": '// Declare um inteiro chamado "nota" com valor 10\n// escreva aqui\n',
    "hint": "int nomeDaVariavel = valor;",
    "hints": [
      "C++ exige tipo explícito antes do nome: `int nome = valor;`",
      "Solução: `int nota = 10;`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "int nota = 10;"}],
    "quiz": [
      {"question": "Qual tipo C++ armazena números decimais?", "options": ["float/double", "int", "char", "bool"], "correct": 0},
      {"question": "C++ requer declaração explícita de tipo?", "options": ["Não, é opcional", "Sim, sempre", "Só para funções", "Só para arrays"], "correct": 1},
    ],
  },
  {
    "order": 3,
    "title": "Função",
    "chapter": "Capítulo 2: Funções",
    "instruction_pt": "Funções C++ têm tipo de retorno antes do nome: `int soma(int a, int b)`. Escreva a assinatura da função `soma` que recebe dois inteiros e retorna inteiro.",
    "instruction_en": "C++ functions have return type before the name: `int soma(int a, int b)`. Write the signature of the `soma` function.",
    "instruction_es": "Las funciones C++ tienen el tipo de retorno antes del nombre. Escribe la firma de la función `soma`.",
    "starter_code": '// Escreva apenas a assinatura da função soma(int a, int b) que retorna int\n// escreva aqui\n',
    "hint": "int nomeFuncao(int a, int b) {",
    "hints": [
      "Em C++, o tipo de retorno vem antes do nome: `tipoRetorno nomeFuncao(Tipo a, Tipo b) {`",
      "Solução: `int soma(int a, int b) {`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "int soma(int a, int b) {"}],
    "quiz": [
      {"question": "Em C++, onde fica o tipo de retorno na declaração de função?", "options": ["Após o nome da função", "Antes do nome da função", "Após os parâmetros", "Em uma linha separada"], "correct": 1},
      {"question": "O que void como tipo de retorno significa em C++?", "options": ["Retorna zero", "Retorna null", "Função sem retorno", "Retorna string vazia"], "correct": 2},
    ],
  },
  {
    "order": 4,
    "title": "Arrays",
    "chapter": "Capítulo 2: Funções",
    "instruction_pt": "Arrays em C++ têm tamanho fixo. Declare o array de inteiros `numeros` com os valores `{1, 2, 3}` em uma linha.",
    "instruction_en": "Arrays in C++ have a fixed size. Declare the integer array `numeros` with values `{1, 2, 3}` on one line.",
    "instruction_es": "Los arrays en C++ tienen tamaño fijo. Declara el array de enteros `numeros` con los valores `{1, 2, 3}`.",
    "starter_code": "// Declare um array de inteiros chamado numeros com os valores 1, 2 e 3\n// Dica: tipo nomeArray[] = {val1, val2, val3};\n// escreva aqui\n",
    "hint": "int nomeArray[] = {val1, val2, val3};",
    "hints": [
      "Sintaxe: `tipo nomeArray[] = {val1, val2, val3};` — colchetes após o nome.",
      "Solução: `int numeros[] = {1, 2, 3};`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "int numeros[] = {1, 2, 3};"}],
    "quiz": [
      {"question": "Arrays em C++ têm tamanho:", "options": ["Dinâmico", "Fixo definido na criação", "Ilimitado", "Até 256 elementos"], "correct": 1},
      {"question": "Como declarar um array de 5 inteiros em C++?", "options": ["int arr(5)", "int[] arr = {}", "int arr[5]", "array<int> arr[5]"], "correct": 2},
    ],
  },
  {
    "order": 5,
    "title": "Condicionais",
    "chapter": "Capítulo 3: Controle de Fluxo",
    "instruction_pt": "C++ usa `if (condição) { ... } else { ... }`. Escreva o cabeçalho do `if` que verifica se a variável `x` é maior que zero.",
    "instruction_en": "C++ uses `if (condition) { ... } else { ... }`. Write the `if` header that checks if variable `x` is greater than zero.",
    "instruction_es": "C++ usa `if (condición) { ... }`. Escribe el encabezado del `if` que verifica si la variable `x` es mayor que cero.",
    "starter_code": "// Escreva o cabeçalho do if que verifica se a variável x é maior que zero\n// Dica: if (condicao) {\n// escreva aqui\n",
    "hint": "if (variavel > 0) {",
    "hints": [
      "Em C++ (assim como Java), a condição do `if` fica entre parênteses.",
      "Solução: `if (x > 0) {`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "if (x > 0) {"}],
    "quiz": [
      {"question": "C++ usa chaves {} para delimitar blocos condicionais?", "options": ["Não, usa indentação", "Sim, definem o início e fim do bloco", "Só em funções", "Só com else"], "correct": 1},
      {"question": "Qual operador lógico significa 'E' em C++?", "options": ["and", "&&", "||", "!"], "correct": 1},
    ],
  },
  {
    "order": 6,
    "title": "Loop For",
    "chapter": "Capítulo 3: Controle de Fluxo",
    "instruction_pt": "O `for` em C++ funciona igual ao Java: inicialização, condição e incremento. Escreva o cabeçalho do `for` que conta de 0 até 4 (i < 5).",
    "instruction_en": "The `for` in C++ works the same as Java. Write the header of the `for` that counts from 0 to 4 (i < 5).",
    "instruction_es": "El `for` en C++ funciona igual que en Java. Escribe el encabezado del `for` que cuenta de 0 a 4.",
    "starter_code": "// Escreva o cabeçalho do for que conta de 0 a 4 (i menor que 5)\n// Dica: for (inicializacao; condicao; incremento) {\n// escreva aqui\n",
    "hint": "for (int i = 0; i < 5; i++) {",
    "hints": [
      "O `for` em C++ é idêntico ao Java: `for (init; condição; incremento) {`",
      "Solução: `for (int i = 0; i < 5; i++) {`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "for (int i = 0; i < 5; i++) {"}],
    "quiz": [
      {"question": "O loop for em C++ é idêntico ao de:", "options": ["Python", "Java/JavaScript", "Go", "Rust"], "correct": 1},
      {"question": "O que i++ faz em C++?", "options": ["Cria novo i", "Incrementa i em 1", "Multiplica i por 2", "Copia i"], "correct": 1},
    ],
  },
  {
    "order": 7,
    "title": "String em C++",
    "chapter": "Capítulo 3: Controle de Fluxo",
    "instruction_pt": "C++ tem o tipo `string` (da biblioteca `<string>`). Declare a variável `nome` do tipo `string` com o valor `'Carlos'`.",
    "instruction_en": "C++ has the `string` type (from the `<string>` library). Declare the variable `nome` of type `string` with the value `'Carlos'`.",
    "instruction_es": "C++ tiene el tipo `string`. Declara la variable `nome` de tipo `string` con el valor `'Carlos'`.",
    "starter_code": "// Declare uma string chamada nome com o valor Carlos\n// Dica: string nomeDaVariavel = \"valor\";\n// escreva aqui\n",
    "hint": "string nomeDaVariavel = \"valor\"; — aspas simples ' ou duplas \" são aceitas.",
    "hints": [
      "C++ tem o tipo `string` (com s minúsculo) quando se inclui `<string>`.",
      "Solução: `string nome = \"Carlos\";`",
    ],
    "tests": [{"stdin": "", "expected_stdout": 'string nome = "Carlos";'}],
    "quiz": [
      {"question": "Para usar string em C++ você precisa incluir:", "options": ["<stdio.h>", "<string>", "<text>", "<chars>"], "correct": 1},
      {"question": "Qual a diferença entre char e string em C++?", "options": ["char é um texto, string é um caractere", "char é um único caractere, string é uma sequência", "São idênticos", "char é mais rápido sempre"], "correct": 1},
    ],
  },
  {
    "order": 8,
    "title": "Vector",
    "chapter": "Capítulo 4: Coleções",
    "instruction_pt": "`vector` é a coleção dinâmica de C++ (da `<vector>`). Escreva a declaração do vector de inteiros `numeros` com os valores `{1, 2, 3}`.",
    "instruction_en": "`vector` is C++'s dynamic collection. Write the declaration of the integer vector `numeros` with values `{1, 2, 3}`.",
    "instruction_es": "`vector` es la colección dinámica de C++. Escribe la declaración del vector de enteros `numeros` con los valores `{1, 2, 3}`.",
    "starter_code": "// Declare um vector de inteiros chamado numeros com os valores 1, 2 e 3\n// Dica: vector<Tipo> nomeVector = {val1, val2, val3};\n// escreva aqui\n",
    "hint": "vector<Tipo> nomeVector = {val1, val2, val3};",
    "hints": [
      "`vector<Tipo>` usa generics igual ao Java: o tipo vai entre `<>`.",
      "Inicialização com chaves: `vector<int> v = {1, 2, 3};`",
      "Solução: `vector<int> numeros = {1, 2, 3};`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "vector<int> numeros = {1, 2, 3};"}],
    "quiz": [
      {"question": "Qual é a vantagem do vector sobre arrays em C++?", "options": ["É mais rápido sempre", "Tem tamanho dinâmico (cresce conforme necessário)", "Usa menos memória", "Não precisa de tipo"], "correct": 1},
      {"question": "Para usar vector em C++ você precisa incluir:", "options": ["<array>", "<list>", "<vector>", "<dynamic>"], "correct": 2},
    ],
  },
  {
    "order": 9,
    "title": "Struct",
    "chapter": "Capítulo 4: Coleções",
    "instruction_pt": "`struct` em C++ agrupa variáveis relacionadas. Escreva a declaração da struct `Pessoa` com os campos `string nome` e `int idade` em uma linha.",
    "instruction_en": "`struct` in C++ groups related variables. Write the declaration of the struct `Pessoa` with fields `string nome` and `int idade` on one line.",
    "instruction_es": "`struct` en C++ agrupa variables relacionadas. Escribe la declaración de la struct `Pessoa` con los campos `string nome` e `int idade`.",
    "starter_code": "// Escreva a struct Pessoa com dois campos: nome (string) e idade (int)\n// Dica: struct NomeDaStruct { tipo campo; tipo campo; };\n// escreva aqui\n",
    "hint": "struct NomeDaStruct { tipo campo1; tipo campo2; };",
    "hints": [
      "Estrutura: `struct Nome { tipo campo1; tipo campo2; };` — note o `;` no final da struct.",
      "Cada campo: `tipo nome;` separado por `;` dentro das chaves.",
      "Solução: `struct Pessoa { string nome; int idade; };`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "struct Pessoa { string nome; int idade; };"}],
    "quiz": [
      {"question": "Para que serve struct em C++?", "options": ["Criar loops", "Agrupar variáveis relacionadas", "Definir funções", "Gerenciar memória"], "correct": 1},
      {"question": "Diferença entre struct e class em C++:", "options": ["struct tem membros públicos por padrão, class tem privados", "São completamente iguais", "struct não tem métodos", "class não tem dados"], "correct": 0},
    ],
  },
  {
    "order": 10,
    "title": "Ponteiros",
    "chapter": "Capítulo 5: Ponteiros",
    "instruction_pt": "Ponteiros armazenam o endereço de memória de uma variável. `int* ptr = &x;` cria um ponteiro que aponta para `x`. Escreva essa declaração de ponteiro para a variável inteira `x`.",
    "instruction_en": "Pointers store the memory address of a variable. `int* ptr = &x;` creates a pointer pointing to `x`. Write that pointer declaration.",
    "instruction_es": "Los punteros almacenan la dirección de memoria de una variable. Escribe la declaración del puntero `ptr` que apunta a `x`.",
    "starter_code": "// Declare um ponteiro do tipo int chamado ptr que aponta para a variável x\n// Dica: tipo* nomePonteiro = &nomeVariavel;\n// escreva aqui\n",
    "hint": "tipo* nomePonteiro = &nomeVariavel;",
    "hints": [
      "`*` após o tipo declara um ponteiro — `int* ptr` é um ponteiro para inteiro.",
      "`&variavel` obtém o endereço de memória da variável.",
      "Solução: `int* ptr = &x;`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "int* ptr = &x;"}],
    "quiz": [
      {"question": "O que um ponteiro armazena em C++?", "options": ["Um valor inteiro", "O endereço de memória de uma variável", "Uma cópia da variável", "O tipo da variável"], "correct": 1},
      {"question": "O que o operador & faz com uma variável?", "options": ["Copia a variável", "Retorna o endereço de memória", "Decrementa o valor", "Cria uma referência constante"], "correct": 1},
      {"question": "O que o operador * faz com um ponteiro?", "options": ["Multiplica o endereço", "Desreferencia (acessa o valor apontado)", "Cria um novo ponteiro", "Libera memória"], "correct": 1},
    ],
  },
],

# ── Go ───────────────────────────────────────────────────────────────────────
"go": [
  {
    "order": 1,
    "title": "fmt.Println",
    "chapter": "Capítulo 1: Introdução ao Go",
    "instruction_pt": "Go usa `fmt.Println()` para exibir texto com quebra de linha. Escreva o comando que exibe 'Olá, Go!'.",
    "instruction_en": "Go uses `fmt.Println()` to display text with a newline. Write the command that displays 'Olá, Go!'.",
    "instruction_es": "Go usa `fmt.Println()` para mostrar texto con salto de línea. Escribe el comando que muestra 'Olá, Go!'.",
    "starter_code": 'package main\nimport "fmt"\nfunc main() {\n    // Exiba "Olá, Go!"\n    // escreva aqui\n}\n',
    "hint": "fmt.Println(\"Olá, Go!\") — aspas simples ' ou duplas \" são aceitas neste exercício.",
    "hints": [
      "Go usa `fmt.Println()` do pacote `fmt` — sem ponto-e-vírgula obrigatório.",
      "Solução: `fmt.Println(\"Olá, Go!\")`",
    ],
    "tests": [{"stdin": "", "expected_stdout": 'fmt.Println("Olá, Go!")'}],
    "quiz": [
      {"question": "Qual pacote Go precisa ser importado para imprimir?", "options": ["os", "io", "fmt", "log"], "correct": 2},
      {"question": "Qual função Go imprime com quebra de linha no final?", "options": ["fmt.Print()", "fmt.Println()", "fmt.Printf()", "print()"], "correct": 1},
    ],
  },
  {
    "order": 2,
    "title": "Declaração curta",
    "chapter": "Capítulo 1: Introdução ao Go",
    "instruction_pt": "Go permite declarar variáveis com `:=` — o compilador infere o tipo automaticamente. Escreva a declaração da variável `nome` com valor 'Gopher'.",
    "instruction_en": "Go allows declaring variables with `:=` — the compiler infers the type automatically. Write the declaration of variable `nome` with value 'Gopher'.",
    "instruction_es": "Go permite declarar variables con `:=` — el compilador infiere el tipo automáticamente.",
    "starter_code": '// Declare a variável "nome" com valor "Gopher" usando :=\n// escreva aqui\n',
    "hint": "nome := \"Gopher\" — aspas simples ' ou duplas \" são aceitas neste exercício.",
    "hints": [
      "`:=` é a declaração curta do Go — cria a variável e infere o tipo automaticamente.",
      "Solução: `nome := \"Gopher\"`",
    ],
    "tests": [{"stdin": "", "expected_stdout": 'nome := "Gopher"'}],
    "quiz": [
      {"question": "O que := faz em Go?", "options": ["Compara dois valores", "Declara e atribui uma variável com tipo inferido", "Incrementa uma variável", "Importa um pacote"], "correct": 1},
      {"question": "Qual é a diferença entre := e var em Go?", "options": [":= só funciona em funções e infere o tipo; var pode ser global", "São idênticos", "var é mais rápido", ":= exige tipo explícito"], "correct": 0},
    ],
  },
  {
    "order": 3,
    "title": "Função",
    "chapter": "Capítulo 2: Funções",
    "instruction_pt": "Go declara funções com `func nome(params tipo) tipoRetorno`. Escreva a assinatura da função `dobrar` que recebe `n int` e retorna `int`.",
    "instruction_en": "Go declares functions with `func name(params type) returnType`. Write the signature of `dobrar` function.",
    "instruction_es": "Go declara funciones con `func nombre(params tipo) tipoRetorno`. Escribe la firma de la función `dobrar`.",
    "starter_code": '// Escreva a assinatura da função dobrar(n int) que retorna int\n// escreva aqui\n',
    "hint": "func dobrar(n int) int {",
    "hints": [
      "Funções Go: `func nome(param tipo) tipoRetorno {` — o tipo do retorno vem após os parâmetros.",
      "Solução: `func dobrar(n int) int {`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "func dobrar(n int) int {"}],
    "quiz": [
      {"question": "Qual palavra-chave define uma função em Go?", "options": ["def", "function", "fn", "func"], "correct": 3},
      {"question": "Em Go, o tipo de retorno fica:", "options": ["Antes do nome da função", "Após os parâmetros", "Entre parênteses", "No início do arquivo"], "correct": 1},
    ],
  },
  {
    "order": 4,
    "title": "Slices",
    "chapter": "Capítulo 2: Funções",
    "instruction_pt": "Slices são arrays dinâmicos em Go. Declare o slice de inteiros `numeros` com os valores `{1, 2, 3}` usando a sintaxe literal.",
    "instruction_en": "Slices are dynamic arrays in Go. Declare the integer slice `numeros` with values `{1, 2, 3}` using literal syntax.",
    "instruction_es": "Los slices son arrays dinámicos en Go. Declara el slice de enteros `numeros` con los valores `{1, 2, 3}`.",
    "starter_code": "// Declare um slice de inteiros chamado numeros com os valores 1, 2 e 3\n// Dica: nomeSlice := []tipo{val1, val2, val3}\n// escreva aqui\n",
    "hint": "nomeSlice := []tipo{val1, val2, val3}",
    "hints": [
      "Slice literal em Go: `[]tipo{val1, val2, val3}` — colchetes vazios antes do tipo.",
      "Solução: `numeros := []int{1, 2, 3}`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "numeros := []int{1, 2, 3}"}],
    "quiz": [
      {"question": "Qual é a diferença entre slice e array em Go?", "options": ["Slice tem tipo diferente", "Slice tem tamanho dinâmico, array tem tamanho fixo", "Array é mais moderno", "São idênticos"], "correct": 1},
      {"question": "Como declarar um slice literal de ints em Go?", "options": ["int[]{1, 2, 3}", "[]int{1, 2, 3}", "(1, 2, 3)", "slice{1, 2, 3}"], "correct": 1},
    ],
  },
  {
    "order": 5,
    "title": "Maps",
    "chapter": "Capítulo 3: Coleções",
    "instruction_pt": "Maps são dicionários em Go. Escreva a declaração do map `idades` que mapeia `string` para `int`, com um par `'Ana': 20` usando sintaxe literal.",
    "instruction_en": "Maps are dictionaries in Go. Write the declaration of the `idades` map that maps `string` to `int`, with one pair `'Ana': 20` using literal syntax.",
    "instruction_es": "Los maps son diccionarios en Go. Escribe la declaración del map `idades` que mapea `string` a `int`, con el par `'Ana': 20`.",
    "starter_code": "// Declare um map chamado idades que mapeia string para int com o par Ana:20\n// Dica: nomeMap := map[tipoChave]tipoValor{\"chave\": valor}\n// escreva aqui\n",
    "hint": "nomeMap := map[tipoChave]tipoValor{\"chave\": valor} — aspas simples ' ou duplas \" são aceitas.",
    "hints": [
      "Sintaxe map: `map[tipoChave]tipoValor{\"chave\": valor}` — chave entre colchetes, valor após.",
      "`map[string]int` → chaves são strings, valores são inteiros.",
      "Solução: `idades := map[string]int{\"Ana\": 20}`",
    ],
    "tests": [{"stdin": "", "expected_stdout": 'idades := map[string]int{"Ana": 20}'}],
    "quiz": [
      {"question": "Qual é o equivalente de dicionário em Go?", "options": ["dict", "hashmap", "map", "object"], "correct": 2},
      {"question": "Como declarar um map de string para int em Go?", "options": ["map{string:int}{}", "map[string]int{}", "Map<string, int>{}", "dict[string]int{}"], "correct": 1},
    ],
  },
  {
    "order": 6,
    "title": "Condicionais",
    "chapter": "Capítulo 3: Controle de Fluxo",
    "instruction_pt": "Go usa `if` sem parênteses ao redor da condição (diferente de Java e C++). Escreva o cabeçalho do `if` que verifica se a variável `x` é maior que zero.",
    "instruction_en": "Go uses `if` without parentheses around the condition (unlike Java and C++). Write the `if` header that checks if variable `x` is greater than zero.",
    "instruction_es": "Go usa `if` sin paréntesis (a diferencia de Java y C++). Escribe el encabezado del `if` que verifica si `x` es mayor que cero.",
    "starter_code": "// Escreva o cabeçalho do if que verifica se x é maior que zero\n// Lembrete: Go nao usa parenteses no if\n// escreva aqui\n",
    "hint": "if variavel > 0 {",
    "hints": [
      "Em Go, `if` NÃO usa parênteses — diferente de Java/C++: `if condição {`",
      "Solução: `if x > 0 {`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "if x > 0 {"}],
    "quiz": [
      {"question": "Go usa parênteses na condição do if?", "options": ["Sim, obrigatórios", "Não, são proibidos/desnecessários", "Opcional", "Só com else"], "correct": 1},
      {"question": "Go tem switch? Como ele difere do C++?", "options": ["Não tem switch", "Tem switch; não precisa de break entre cases", "Tem switch igual ao C++", "Só suporta strings no switch"], "correct": 1},
    ],
  },
  {
    "order": 7,
    "title": "Loop For",
    "chapter": "Capítulo 3: Controle de Fluxo",
    "instruction_pt": "Go tem apenas `for` como estrutura de repetição (não existe `while`). Assim como no `if`, não use parênteses. Escreva o cabeçalho do `for` que conta de 0 até 4 (i < 5).",
    "instruction_en": "Go has only `for` as a loop construct (no `while`). Like `if`, no parentheses. Write the header of the `for` that counts from 0 to 4 (i < 5).",
    "instruction_es": "Go solo tiene `for` (no hay `while`). Como el `if`, sin paréntesis. Escribe el encabezado del `for` que cuenta de 0 a 4.",
    "starter_code": "// Escreva o cabeçalho do for que conta de 0 a 4 (i menor que 5)\n// Lembrete: Go nao usa parenteses no for\n// escreva aqui\n",
    "hint": "for i := 0; i < 5; i++ {",
    "hints": [
      "Go não usa parênteses no `for` e usa `:=` para inicializar a variável.",
      "Solução: `for i := 0; i < 5; i++ {`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "for i := 0; i < 5; i++ {"}],
    "quiz": [
      {"question": "Go tem loop while?", "options": ["Sim, com a palavra while", "Não; for sozinho age como while", "Sim, com a palavra loop", "Não, só for...range"], "correct": 1},
      {"question": "Como percorrer uma slice em Go?", "options": ["for item in slice", "foreach(slice)", "for i, v := range slice", "slice.forEach()"], "correct": 2},
    ],
  },
  {
    "order": 8,
    "title": "Struct",
    "chapter": "Capítulo 4: Tipos e Structs",
    "instruction_pt": "`struct` em Go agrupa campos relacionados. Use `type NomeStruct struct { ... }`. Escreva a struct `Pessoa` com os campos `Nome string` e `Idade int` em uma linha.",
    "instruction_en": "`struct` in Go groups related fields. Write the `Pessoa` struct with fields `Nome string` and `Idade int` on one line.",
    "instruction_es": "`struct` en Go agrupa campos relacionados. Escribe la struct `Pessoa` con los campos `Nome string` e `Idade int` en una línea.",
    "starter_code": "// Escreva a struct Pessoa com dois campos: Nome (string) e Idade (int)\n// Dica: type NomeDaStruct struct { Campo1 tipo1; Campo2 tipo2 }\n// escreva aqui\n",
    "hint": "type NomeDaStruct struct { Campo1 tipo1; Campo2 tipo2 }",
    "hints": [
      "Struct em Go: `type Nome struct { Campo Tipo; Campo2 Tipo2 }` — note o `type` e `struct`.",
      "Solução: `type Pessoa struct { Nome string; Idade int }`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "type Pessoa struct { Nome string; Idade int }"}],
    "quiz": [
      {"question": "Como definir uma struct em Go?", "options": ["struct Pessoa { }", "class Pessoa { }", "type Pessoa struct { }", "Pessoa struct { }"], "correct": 2},
      {"question": "Structs em Go podem ter métodos?", "options": ["Não, apenas dados", "Sim, definidos com receiver", "Só métodos estáticos", "Só com interface"], "correct": 1},
    ],
  },
  {
    "order": 9,
    "title": "Métodos em Struct",
    "chapter": "Capítulo 4: Tipos e Structs",
    "instruction_pt": "Go adiciona métodos a structs com um *receiver*. Escreva a assinatura do método `saudar` que pertence a `Pessoa` e retorna `string`.",
    "instruction_en": "Go adds methods to structs with a *receiver*. Write the signature of the `saudar` method that belongs to `Pessoa` and returns `string`.",
    "instruction_es": "Go añade métodos a structs con un *receiver*. Escribe la firma del método `saudar` que pertenece a `Pessoa` y retorna `string`.",
    "starter_code": "// Escreva a assinatura do método saudar para a struct Pessoa, que retorna string\n// Dica: func (receiver NomeStruct) nomeMetodo() tipoRetorno {\n// escreva aqui\n",
    "hint": "func (receiver NomeStruct) nomeMetodo() tipoRetorno {",
    "hints": [
      "O receiver fica entre parênteses após `func`: `func (p Pessoa) metodo() tipo {`",
      "`p` é a convenção para o receiver — normalmente a primeira letra do nome da struct.",
      "Solução: `func (p Pessoa) saudar() string {`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "func (p Pessoa) saudar() string {"}],
    "quiz": [
      {"question": "O que é um receiver em Go?", "options": ["Um canal de comunicação", "O tipo ao qual o método pertence", "Um retorno especial", "Uma importação de pacote"], "correct": 1},
      {"question": "A sintaxe de um método com receiver em Go é:", "options": ["func Pessoa.saudar() {}", "func (p Pessoa) saudar() {}", "method Pessoa.saudar() {}", "func saudar(Pessoa) {}"], "correct": 1},
    ],
  },
  {
    "order": 10,
    "title": "Interface",
    "chapter": "Capítulo 5: Interfaces",
    "instruction_pt": "Interfaces em Go definem comportamentos. Qualquer struct que implemente os métodos satisfaz a interface automaticamente. Escreva a interface `Animal` com o método `Falar() string` em uma linha.",
    "instruction_en": "Interfaces in Go define behaviors. Any struct that implements the methods satisfies the interface automatically. Write the `Animal` interface with the method `Falar() string` on one line.",
    "instruction_es": "Las interfaces en Go definen comportamientos. Escribe la interfaz `Animal` con el método `Falar() string` en una línea.",
    "starter_code": "// Escreva a interface Animal com o método Falar() que retorna string\n// Dica: type NomeInterface interface { NomeMetodo() tipoRetorno }\n// escreva aqui\n",
    "hint": "type NomeInterface interface { NomeMetodo() tipoRetorno }",
    "hints": [
      "Interface Go: `type Nome interface { Metodo() tipoRetorno }` — começa com `type`.",
      "Em Go, interfaces são implícitas — nenhuma declaração explícita de implementação necessária.",
      "Solução: `type Animal interface { Falar() string }`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "type Animal interface { Falar() string }"}],
    "quiz": [
      {"question": "Como uma struct satisfaz uma interface em Go?", "options": ["Declarando implements explicitamente", "Implementando todos os métodos da interface", "Herdando a interface", "Registrando no compilador"], "correct": 1},
      {"question": "Interfaces em Go são:", "options": ["Explícitas (declara-se implements)", "Implícitas (automático ao implementar os métodos)", "Opcionais", "Apenas para classes"], "correct": 1},
    ],
  },
],

# ── AI Prompts ───────────────────────────────────────────────────────────────
"ai-prompts": [
  {
    "order": 1,
    "title": "Comando Direto",
    "chapter": "Capítulo 1: Fundamentos de Prompting",
    "instruction_pt": "Prompts vagos geram respostas vagas. Sempre especifique quantidade, tema e idioma. Escreva um prompt pedindo exatamente **3 exemplos de Python para ciência de dados**. Seu prompt deve conter a frase: `3 exemplos de Python para ciência de dados`",
    "instruction_en": "Vague prompts produce vague answers. Always specify quantity, topic, and language. Write a prompt asking for exactly **3 Python examples for data science**. Your prompt must contain: `3 examples of Python for data science`",
    "instruction_es": "Los prompts vagos generan respuestas vagas. Escribe un prompt que contenga exactamente: `3 exemplos de Python para ciência de dados`",
    "starter_code": "// Escreva seu prompt aqui:\n// (deve conter a frase: 3 exemplos de Python para ciência de dados)\n// escreva aqui\n",
    "hint": "Exemplo completo: Dê-me 3 exemplos de Python para ciência de dados, em português.",
    "hints": [
      "O exercício verifica se seu prompt contém a frase exata: `3 exemplos de Python para ciência de dados`",
      "Exemplo: `Dê-me 3 exemplos de Python para ciência de dados, em português, com explicação.`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "3 exemplos de Python para ciência de dados"}],
    "quiz": [
      {"question": "Por que prompts vagos geram respostas ruins?", "options": ["A IA é mais lenta com prompts curtos", "Falta de contexto e especificidade leva a respostas genéricas", "Prompts curtos consomem mais tokens", "A IA prefere prompts formais"], "correct": 1},
      {"question": "O que especificar em um bom prompt?", "options": ["Apenas o tema", "Quantidade, tema, idioma e formato", "Só a pergunta principal", "O nome da IA"], "correct": 1},
    ],
  },
  {
    "order": 2,
    "title": "Atribuindo uma Persona",
    "chapter": "Capítulo 1: Fundamentos de Prompting",
    "instruction_pt": "Atribuir uma persona muda como a IA responde. 'Aja como um professor de matemática' gera respostas mais didáticas. Escreva um prompt pedindo à IA que aja como **tutor de programação** e explique variáveis. Seu prompt deve começar com `Aja como`.",
    "instruction_en": "Assigning a persona changes how the AI responds. Write a prompt asking the AI to act as a **programming tutor** and explain variables. Your prompt must start with `Aja como`.",
    "instruction_es": "Asignar una persona cambia la respuesta. Escribe un prompt que empiece con `Aja como` y pida explicar variables.",
    "starter_code": "// Escreva um prompt com persona\n// Comece com: Aja como [persona]. [Tarefa].\n// escreva aqui\n",
    "hint": "Exemplo: Aja como um tutor de programação paciente. Explique o que é uma variável de forma simples.",
    "hints": [
      "Seu prompt deve começar com `Aja como` — isso define a persona da IA.",
      "Exemplo: `Aja como um tutor de programação paciente. Explique variáveis de forma simples.`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "Aja como um tutor de programação"}],
    "quiz": [
      {"question": "Por que atribuir uma persona melhora as respostas da IA?", "options": ["A IA fica mais rápida", "Orienta o estilo, tom e nível de profundidade da resposta", "Economiza tokens", "É requisito técnico das APIs"], "correct": 1},
      {"question": "Qual frase geralmente inicia um prompt com persona?", "options": ["'Responda como se fosse'", "'Aja como [persona].'", "'Simule [persona].'", "Qualquer das anteriores funciona igualmente"], "correct": 3},
    ],
  },
  {
    "order": 3,
    "title": "Cadeia de Pensamento",
    "chapter": "Capítulo 2: Técnicas Avançadas",
    "instruction_pt": "Chain-of-thought pede que a IA raciocine passo a passo, melhorando problemas complexos. Adicione `Pense passo a passo antes de responder.` ao final de qualquer pergunta. Escreva um prompt perguntando quanto é 17 × 23 com essa instrução.",
    "instruction_en": "Chain-of-thought asks the AI to reason step by step. Add `Pense passo a passo antes de responder.` at the end. Write a prompt asking what 17 × 23 is with this instruction.",
    "instruction_es": "Chain-of-thought pide a la IA que razone paso a paso. Añade `Pense passo a passo antes de responder.` al final.",
    "starter_code": "// Escreva seu prompt sobre 17 × 23\n// Termine com: Pense passo a passo antes de responder.\n// escreva aqui\n",
    "hint": "Exemplo: Quanto é 17 × 23? Pense passo a passo antes de responder.",
    "hints": [
      "Seu prompt deve terminar com a frase: `Pense passo a passo antes de responder.`",
      "Exemplo: `Quanto é 17 × 23? Pense passo a passo antes de responder.`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "passo a passo antes de responder"}],
    "quiz": [
      {"question": "O que chain-of-thought prompting solicita da IA?", "options": ["Respostas mais curtas", "Raciocinar passo a passo antes de responder", "Usar linguagem formal", "Citar fontes"], "correct": 1},
      {"question": "Chain-of-thought é mais útil para:", "options": ["Criar imagens", "Traduzir textos", "Problemas matemáticos e raciocínio complexo", "Formatar documentos"], "correct": 2},
    ],
  },
  {
    "order": 4,
    "title": "Few-Shot Prompting",
    "chapter": "Capítulo 2: Técnicas Avançadas",
    "instruction_pt": "Few-shot prompting ensina a IA com exemplos antes de pedir a tarefa. Padrão: `Entrada: X → Saída: Y`. Escreva um prompt com dois exemplos do padrão `Produto → Slogan` e peça o slogan para `Café`. Seu prompt deve conter `Produto: Café → Slogan:`.",
    "instruction_en": "Few-shot prompting teaches the AI with examples before the task. Write a prompt with two `Product → Slogan` examples and ask for the slogan for `Coffee`. Your prompt must contain `Produto: Café → Slogan:`.",
    "instruction_es": "Few-shot usa ejemplos antes de pedir la tarea. Escribe un prompt con dos ejemplos y pide el slogan para Café. Debe contener `Produto: Café → Slogan:`.",
    "starter_code": "// Escreva dois exemplos Produto → Slogan e peça para Café\n// Deve conter: Produto: Café → Slogan:\n// escreva aqui\n",
    "hint": "Exemplo: Produto: Tênis → Slogan: Vá além dos seus limites. Produto: Livro → Slogan: Abra um mundo novo. Produto: Café → Slogan:",
    "hints": [
      "Seu prompt deve conter a parte que a IA deve completar: `Produto: Café → Slogan:`",
      "Dê dois exemplos completos antes de pedir o Café — a IA aprende o padrão.",
    ],
    "tests": [{"stdin": "", "expected_stdout": "Produto: Café → Slogan:"}],
    "quiz": [
      {"question": "O que few-shot prompting significa?", "options": ["Usar poucas palavras", "Fornecer exemplos antes de pedir a tarefa", "Limitar o tamanho da resposta", "Usar várias IAs"], "correct": 1},
      {"question": "Zero-shot prompting é quando:", "options": ["O modelo não funciona", "A tarefa é pedida sem nenhum exemplo", "São dados zero parâmetros", "A resposta tem zero erros"], "correct": 1},
    ],
  },
  {
    "order": 5,
    "title": "Formato de Saída",
    "chapter": "Capítulo 2: Técnicas Avançadas",
    "instruction_pt": "Especificar o formato de saída torna respostas mais úteis e processáveis. Escreva um prompt pedindo as 3 linguagens de programação mais populares **em formato JSON**. Seu prompt deve conter `formato JSON`.",
    "instruction_en": "Specifying output format makes responses more useful. Write a prompt asking for the 3 most popular programming languages **in JSON format**. Your prompt must contain `formato JSON`.",
    "instruction_es": "Especificar el formato hace las respuestas más útiles. Escribe un prompt pidiendo las 3 lenguajes más populares en JSON. Debe contener `formato JSON`.",
    "starter_code": "// Escreva um prompt pedindo dados em formato JSON\n// Deve conter: formato JSON\n// escreva aqui\n",
    "hint": "Exemplo: Liste as 3 linguagens de programação mais populares em formato JSON, com os campos nome e uso_principal.",
    "hints": [
      "Seu prompt deve conter a frase `formato JSON` — que instrui a IA a formatar a saída.",
      "Especifique também os campos que quer no JSON: ex. `campos: nome, popularidade`.",
      "Exemplo: `Liste as 3 linguagens mais populares em formato JSON com os campos nome e uso_principal.`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "formato JSON"}],
    "quiz": [
      {"question": "Por que especificar formato de saída no prompt?", "options": ["A IA responde mais rápido", "A resposta fica mais processável e previsível", "Economiza memória", "É obrigatório na API"], "correct": 1},
      {"question": "Qual dos seguintes especifica formato de saída?", "options": ["'Responda brevemente'", "'Responda em JSON com campos nome e idade'", "'Use linguagem simples'", "'Seja preciso'"], "correct": 1},
    ],
  },
  {
    "order": 6,
    "title": "Prompt para Código",
    "chapter": "Capítulo 3: Prompts para Desenvolvimento",
    "instruction_pt": "Prompts para código devem informar: linguagem, nome da função, parâmetros, retorno e extras (como docstring). Escreva um prompt pedindo uma **função Python chamada `calcular_media`** que receba uma lista e retorne a média. Seu prompt deve conter `calcular_media`.",
    "instruction_en": "Code prompts must specify: language, function name, parameters, return, and extras. Write a prompt asking for a **Python function named `calcular_media`** that takes a list and returns the average. Must contain `calcular_media`.",
    "instruction_es": "Los prompts de código deben especificar lenguaje, nombre, parámetros y extras. Escribe un prompt pidiendo la función `calcular_media`. Debe contener `calcular_media`.",
    "starter_code": "// Escreva um prompt de geração de código\n// Deve conter o nome: calcular_media\n// escreva aqui\n",
    "hint": "Exemplo: Escreva uma função Python chamada calcular_media que receba uma lista de números e retorne a média. Inclua docstring.",
    "hints": [
      "Seu prompt deve conter o nome exato da função: `calcular_media`.",
      "Um bom prompt de código especifica: linguagem + nome + parâmetros + o que retorna.",
      "Exemplo: `Escreva uma função Python chamada calcular_media que receba uma lista e retorne a média.`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "calcular_media"}],
    "quiz": [
      {"question": "O que incluir em um prompt para gerar código?", "options": ["Apenas o nome da função", "Linguagem, nome, parâmetros, retorno e observações", "Só a linguagem de programação", "Apenas o comportamento esperado"], "correct": 1},
      {"question": "Por que pedir docstring no prompt de código?", "options": ["Ocupa mais espaço", "Documenta o código gerado para fácil entendimento", "É obrigatório pelo Python", "Torna o código mais rápido"], "correct": 1},
    ],
  },
  {
    "order": 7,
    "title": "Restrições no Prompt",
    "chapter": "Capítulo 3: Prompts para Desenvolvimento",
    "instruction_pt": "Restrições tornam respostas mais precisas e adequadas ao contexto. Escreva um prompt explicando machine learning **em no máximo 3 frases** e **sem jargões técnicos**. Seu prompt deve conter `no máximo 3 frases`.",
    "instruction_en": "Constraints make responses more precise. Write a prompt explaining machine learning **in at most 3 sentences** and **without technical jargon**. Must contain `no máximo 3 frases`.",
    "instruction_es": "Las restricciones hacen las respuestas más precisas. Escribe un prompt explicando machine learning en no más de 3 frases. Debe contener `no máximo 3 frases`.",
    "starter_code": "// Escreva um prompt com restrições claras\n// Deve conter: no máximo 3 frases\n// escreva aqui\n",
    "hint": "Exemplo: Explique o que é machine learning em no máximo 3 frases, sem jargões técnicos, para um aluno do ensino médio.",
    "hints": [
      "Seu prompt deve conter a restrição exata: `no máximo 3 frases`.",
      "Combine restrições: quantidade de frases + audiência + proibições (`sem jargões`).",
      "Exemplo: `Explique machine learning em no máximo 3 frases, sem jargões técnicos, para um aluno do ensino médio.`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "no máximo 3 frases"}],
    "quiz": [
      {"question": "Por que adicionar restrições ao prompt?", "options": ["Para testar a IA", "Para tornar a resposta mais adequada ao contexto e audiência", "Para economizar tokens", "Por requisito técnico"], "correct": 1},
      {"question": "Qual é um exemplo de restrição de prompt?", "options": ["'Responda em português'", "'Sem jargões técnicos, máximo 3 frases, para leigos'", "'Use emojis'", "Todas acima são restrições"], "correct": 3},
    ],
  },
  {
    "order": 8,
    "title": "Projeto Final: Prompt Completo",
    "chapter": "Capítulo 4: Projeto Final",
    "instruction_pt": "Um prompt profissional combina: **persona + contexto + tarefa + formato + restrições**. Escreva um prompt pedindo à IA que aja como **coach de carreira**, analise o perfil de um desenvolvedor júnior e dê dicas em lista numerada. Seu prompt deve conter `coach de carreira`.",
    "instruction_en": "A professional prompt combines: persona + context + task + format + constraints. Write a prompt asking the AI to act as a **career coach**, analyze a junior developer's profile, and give tips in a numbered list. Must contain `coach de carreira`.",
    "instruction_es": "Un prompt profesional combina persona + contexto + tarea + formato. Escribe un prompt completo con la persona `coach de carreira`.",
    "starter_code": "// Escreva um prompt profissional completo:\n// Persona + contexto + tarefa + formato\n// Deve conter: coach de carreira\n// escreva aqui\n",
    "hint": "Exemplo: Aja como um coach de carreira experiente em tecnologia. Analise o perfil de um desenvolvedor júnior com 1 ano de experiência em Python. Dê 3 dicas práticas em formato de lista numerada.",
    "hints": [
      "Seu prompt deve conter a persona: `coach de carreira` — combine com contexto + tarefa + formato.",
      "Estrutura: `Aja como [persona]. [Contexto]. [Tarefa]. [Formato]. [Restrição].`",
      "Exemplo: `Aja como um coach de carreira. Analise um dev júnior de Python. Dê 3 dicas em lista numerada.`",
    ],
    "tests": [{"stdin": "", "expected_stdout": "coach de carreira"}],
    "quiz": [
      {"question": "Um prompt profissional completo combina:", "options": ["Apenas persona e tarefa", "Persona + contexto + tarefa + formato + restrições", "Só tarefa e formato", "Contexto e tarefa apenas"], "correct": 1},
      {"question": "Qual elemento do prompt define o estilo da resposta?", "options": ["Contexto", "Tarefa", "Persona", "Restrições"], "correct": 2},
      {"question": "Qual elemento define limitações como 'máximo 3 itens'?", "options": ["Persona", "Contexto", "Formato", "Restrições"], "correct": 3},
    ],
  },
],

} # fim LESSONS

# ---------------------------------------------------------------------------
# Engine de inserção
# ---------------------------------------------------------------------------

def _slug_base(title: str) -> str:
    # Normalize Unicode → decompose accented chars (e.g. "ã" → "a" + combining tilde)
    # then keep only ASCII, so "Condições" → "condicoes" not "condi-es"
    normalized = unicodedata.normalize("NFKD", title)
    ascii_title = normalized.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", ascii_title.lower()).strip("-")[:40]


def _build_doc(path_cfg: dict, les: dict) -> dict:
    order = les["order"]
    slug = les.get("slug") or f"{path_cfg['slug']}-{order:02d}-{_slug_base(les['title'])}"
    return {
        "id": str(uuid.uuid4()),
        "slug": slug,
        "path_slug": path_cfg["slug"],
        "order": order,
        "title": les["title"],
        "chapter": les.get("chapter", "Capítulo 1"),
        "theory": les.get("theory", ""),
        "instruction_pt": les.get("instruction_pt", ""),
        "instruction_en": les.get("instruction_en", ""),
        "instruction_es": les.get("instruction_es", ""),
        "starter_code": les.get("starter_code", ""),
        "hint": les.get("hint", ""),
        "hints": les.get("hints", []),
        "tests": les.get("tests", []),
        "quiz": les.get("quiz", []),
        "language": path_cfg["language"],
        "real_exec": path_cfg["real_exec"],
        "updated_at": datetime.utcnow().isoformat(),
    }


async def seed_path(path_cfg: dict):
    slug = path_cfg["slug"]
    lessons_data = LESSONS.get(slug, [])
    if not lessons_data:
        print(f"  aviso: nenhuma lição definida para {slug}")
        return

    # Upsert path metadata
    await db.paths.update_one(
        {"slug": slug},
        {"$set": {
            "slug": slug,
            "name": path_cfg["name"],
            "language": path_cfg["language"],
            "color": path_cfg["color"],
            "desc": path_cfg["desc"],
            "real_exec": path_cfg["real_exec"],
            "total_lessons": len(lessons_data),
            "updated_at": datetime.utcnow().isoformat(),
        }},
        upsert=True,
    )

    # Upsert each lesson
    for les in lessons_data:
        doc = _build_doc(path_cfg, les)
        await db.lessons.update_one(
            {"path_slug": slug, "order": doc["order"]},
            {"$set": doc},
            upsert=True,
        )

    print(f"  {path_cfg['name']}: {len(lessons_data)} lições inseridas")


async def main(slugs=None):
    await db.paths.create_index("slug", unique=True)
    await db.lessons.create_index([("path_slug", 1), ("order", 1)], unique=True)
    await db.lessons.create_index("slug", unique=True)

    targets = PATHS if not slugs else [p for p in PATHS if p["slug"] in slugs]
    print(f"Populando {len(targets)} trilha(s)...")
    for p in targets:
        await seed_path(p)
    print("Pronto!")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:] or None))
