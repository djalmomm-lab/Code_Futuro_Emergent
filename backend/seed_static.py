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
    "title": "Olá, Mundo!",
    "chapter": "Capítulo 1: Primeiros Passos",
    "instruction_pt": "Seu primeiro programa! Use `print()` para exibir texto na tela. Tudo o que estiver entre as aspas dentro de `print()` será mostrado ao usuário.",
    "instruction_en": "Your first program! Use `print()` to display text on screen. Everything inside the quotes will be shown to the user.",
    "instruction_es": "¡Tu primer programa! Usa `print()` para mostrar texto en pantalla. Todo lo que esté entre comillas se mostrará al usuario.",
    "starter_code": '# Use print() para exibir sua primeira mensagem\n# escreva aqui\n',
    "hint": "Digite: print(\"Olá, Mundo!\") — o texto entre aspas aparece exatamente como está escrito.",
    "tests": [{"stdin": "", "expected_stdout": "Olá, Mundo!"}],
  },
  {
    "order": 2,
    "title": "Variáveis",
    "chapter": "Capítulo 1: Primeiros Passos",
    "instruction_pt": "Variáveis guardam dados. Use `nome = valor` para criar uma variável. F-strings (f\"...\") permitem inserir variáveis dentro de texto usando `{variavel}`.",
    "instruction_en": "Variables store data. Use `name = value` to create a variable. F-strings allow inserting variables inside text using `{variable}`.",
    "instruction_es": "Las variables guardan datos. Usa `nombre = valor` para crear una variable. Las f-strings permiten insertar variables dentro del texto usando `{variable}`.",
    "starter_code": '# As variáveis abaixo estão fixas — não precisa alterar\nnome = "Ana"\nidade = 16\n# Imprima exatamente: Olá! Meu nome é Ana e tenho 16 anos.\nprint(f"Olá! Meu nome é {nome} e tenho {idade} anos.")\n',
    "hint": "Use f\"...\" com chaves ao redor das variáveis: f\"Olá! Meu nome é {nome}...\"",
    "tests": [{"stdin": "", "expected_stdout": "Olá! Meu nome é Ana e tenho 16 anos."}],
  },
  {
    "order": 3,
    "title": "Entrada do Usuário",
    "chapter": "Capítulo 1: Primeiros Passos",
    "instruction_pt": "`input()` lê o que o usuário digita e retorna uma string. Combine com `print()` para criar programas interativos. O teste passa 'Carlos' como entrada — seu programa deve responder com 'Bem-vindo, Carlos!'",
    "instruction_en": "`input()` reads what the user types and returns a string. The test passes 'Carlos' as input — your program should respond with 'Bem-vindo, Carlos!'",
    "instruction_es": "`input()` lee lo que el usuario escribe y devuelve un string. La prueba pasa 'Carlos' como entrada — tu programa debe responder con 'Bem-vindo, Carlos!'",
    "starter_code": '# Leia o nome do usuário e cumprimente-o\nnome = input()\n# Imprima: Bem-vindo, <nome>!\n# escreva aqui\n',
    "hint": "Use print(f\"Bem-vindo, {nome}!\") após ler o nome com input().",
    "tests": [{"stdin": "Carlos", "expected_stdout": "Bem-vindo, Carlos!"}],
  },
  {
    "order": 4,
    "title": "Condicionais",
    "chapter": "Capítulo 2: Lógica e Controle",
    "instruction_pt": "`if`, `elif` e `else` permitem que o programa tome decisões. O bloco indentado (4 espaços) após o `if` executa somente quando a condição é verdadeira.",
    "instruction_en": "`if`, `elif` and `else` allow the program to make decisions. The indented block after `if` runs only when the condition is true.",
    "instruction_es": "`if`, `elif` y `else` permiten que el programa tome decisiones. El bloque indentado después del `if` se ejecuta solo cuando la condición es verdadera.",
    "starter_code": 'numero = int(input())\n# Se > 0 imprima "positivo"\n# Se < 0 imprima "negativo"\n# Se == 0 imprima "zero"\n# escreva aqui\n',
    "hint": "Estrutura: if numero > 0: / print(\"positivo\") / elif numero < 0: / ... / else: / ...",
    "tests": [
      {"stdin": "7",  "expected_stdout": "positivo"},
      {"stdin": "-3", "expected_stdout": "negativo"},
      {"stdin": "0",  "expected_stdout": "zero"},
    ],
  },
  {
    "order": 5,
    "title": "Loops com for",
    "chapter": "Capítulo 2: Lógica e Controle",
    "instruction_pt": "`for` repete um bloco de código. `range(1, 6)` gera os números 1, 2, 3, 4, 5. Use `for i in range(...)` para iterar sobre sequências.",
    "instruction_en": "`for` repeats a block of code. `range(1, 6)` generates numbers 1, 2, 3, 4, 5. Use `for i in range(...)` to iterate over sequences.",
    "instruction_es": "`for` repite un bloque de código. `range(1, 6)` genera los números 1, 2, 3, 4, 5. Usa `for i in range(...)` para iterar sobre secuencias.",
    "starter_code": '# Imprima os números de 1 a 5, um por linha\n# escreva aqui\n',
    "hint": "Use: for i in range(1, 6): / print(i)",
    "tests": [{"stdin": "", "expected_stdout": "1\n2\n3\n4\n5"}],
  },
  {
    "order": 6,
    "title": "Funções",
    "chapter": "Capítulo 3: Funções e Estruturas",
    "instruction_pt": "Funções agrupam código reutilizável. `def nome(parametros):` define uma função e `return` devolve um resultado. Chame a função pelo nome para executá-la.",
    "instruction_en": "Functions group reusable code. `def name(parameters):` defines a function and `return` returns a result. Call the function by name to run it.",
    "instruction_es": "Las funciones agrupan código reutilizable. `def nombre(parámetros):` define una función y `return` devuelve un resultado.",
    "starter_code": '# Crie uma função que recebe dois números e retorna a soma\ndef somar(a, b):\n    # escreva aqui\n\nprint(somar(3, 7))\n',
    "hint": "Dentro da função, use: return a + b",
    "tests": [{"stdin": "", "expected_stdout": "10"}],
  },
],

# ── JavaScript ───────────────────────────────────────────────────────────────
"javascript": [
  {
    "order": 1,
    "title": "console.log",
    "chapter": "Capítulo 1: Fundamentos",
    "instruction_pt": "`console.log()` exibe valores no terminal. É a forma mais básica de depurar e comunicar resultados em JavaScript.",
    "instruction_en": "`console.log()` displays values in the terminal. It's the most basic way to debug and communicate results in JavaScript.",
    "instruction_es": "`console.log()` muestra valores en el terminal. Es la forma más básica de depurar y comunicar resultados en JavaScript.",
    "starter_code": '// Exiba "Olá, JavaScript!" no console\n// escreva aqui\n',
    "hint": "Use: console.log(\"Olá, JavaScript!\")",
    "tests": [{"stdin": "", "expected_stdout": "Olá, JavaScript!"}],
  },
  {
    "order": 2,
    "title": "let e const",
    "chapter": "Capítulo 1: Fundamentos",
    "instruction_pt": "Use `const` para valores que não mudam e `let` para variáveis que podem ser reatribuídas. Template literals (crase) permitem interpolar variáveis com `${variavel}`.",
    "instruction_en": "Use `const` for values that don't change and `let` for variables that can be reassigned. Template literals (backtick) allow interpolating variables with `${variable}`.",
    "instruction_es": "Usa `const` para valores que no cambian y `let` para variables que pueden ser reasignadas.",
    "starter_code": 'const linguagem = "JavaScript";\nlet versao = 2024;\n// Exiba: Aprendendo JavaScript versão 2024\nconsole.log(`Aprendendo ${linguagem} versão ${versao}`);\n',
    "hint": "O código já está quase pronto — o console.log usa template literal corretamente.",
    "tests": [{"stdin": "", "expected_stdout": "Aprendendo JavaScript versão 2024"}],
  },
  {
    "order": 3,
    "title": "Funções",
    "chapter": "Capítulo 1: Fundamentos",
    "instruction_pt": "Funções em JS são declaradas com `function nome(params) { ... }`. Use `return` para devolver valores. Chame a função pelo nome seguido de parênteses.",
    "instruction_en": "Functions in JS are declared with `function name(params) { ... }`. Use `return` to return values. Call the function by name followed by parentheses.",
    "instruction_es": "Las funciones en JS se declaran con `function nombre(params) { ... }`. Usa `return` para devolver valores.",
    "starter_code": '// Complete a função que recebe um nome e retorna uma saudação\nfunction saudar(nome) {\n    // escreva aqui (return "Olá, " + nome + "!")\n}\nconsole.log(saudar("Mundo"));\n',
    "hint": "Dentro da função: return \"Olá, \" + nome + \"!\"",
    "tests": [{"stdin": "", "expected_stdout": "Olá, Mundo!"}],
  },
  {
    "order": 4,
    "title": "Arrays",
    "chapter": "Capítulo 2: Estruturas de Dados",
    "instruction_pt": "Arrays armazenam listas de valores. Use `array[indice]` para acessar elementos (começa no índice 0). `.length` retorna o tamanho do array.",
    "instruction_en": "Arrays store lists of values. Use `array[index]` to access elements (starts at index 0). `.length` returns the array size.",
    "instruction_es": "Los arrays almacenan listas de valores. Usa `array[indice]` para acceder a elementos (comienza en el índice 0).",
    "starter_code": 'const frutas = ["maçã", "banana", "laranja"];\n// Exiba o segundo elemento do array\n// escreva aqui\n',
    "hint": "Índices começam em 0: frutas[0] é \"maçã\", frutas[1] é \"banana\"",
    "tests": [{"stdin": "", "expected_stdout": "banana"}],
  },
],

# ── HTML & CSS ───────────────────────────────────────────────────────────────
"html-css": [
  {
    "order": 1,
    "title": "Título com h1",
    "chapter": "Capítulo 1: Estrutura HTML",
    "instruction_pt": "HTML usa tags para estruturar conteúdo. `<h1>` cria um título principal. Tags HTML seguem o padrão `<tag>conteúdo</tag>`. Escreva a tag que exibe o título 'Olá, Web!'",
    "instruction_en": "HTML uses tags to structure content. `<h1>` creates a main heading. Write the tag that displays the heading 'Olá, Web!'",
    "instruction_es": "HTML usa etiquetas para estructurar contenido. `<h1>` crea un título principal. Escribe la etiqueta que muestra el título 'Olá, Web!'",
    "starter_code": '<!DOCTYPE html>\n<html>\n  <body>\n    <!-- Adicione um título h1 com o texto: Olá, Web! -->\n    <!-- escreva aqui -->\n  </body>\n</html>\n',
    "hint": "Estrutura: <h1>texto aqui</h1>",
    "tests": [{"stdin": "", "expected_stdout": "<h1>Olá, Web!</h1>"}],
  },
  {
    "order": 2,
    "title": "Parágrafos",
    "chapter": "Capítulo 1: Estrutura HTML",
    "instruction_pt": "`<p>` cria parágrafos de texto. É a tag mais usada para conteúdo textual em páginas web. Escreva o parágrafo com o texto exato solicitado.",
    "instruction_en": "`<p>` creates text paragraphs. It's the most used tag for textual content on web pages.",
    "instruction_es": "`<p>` crea párrafos de texto. Es la etiqueta más usada para contenido textual en páginas web.",
    "starter_code": '<body>\n  <h1>Meu Site</h1>\n  <!-- Adicione um parágrafo com: Bem-vindo ao HTML! -->\n  <!-- escreva aqui -->\n</body>\n',
    "hint": "Use <p>texto aqui</p>",
    "tests": [{"stdin": "", "expected_stdout": "<p>Bem-vindo ao HTML!</p>"}],
  },
  {
    "order": 3,
    "title": "Links",
    "chapter": "Capítulo 1: Estrutura HTML",
    "instruction_pt": "`<a href=\"url\">texto</a>` cria links clicáveis. O atributo `href` define o destino. Escreva o link completo que aponta para https://codefuturo.com.br com o texto 'Acessar'.",
    "instruction_en": "`<a href=\"url\">text</a>` creates clickable links. The `href` attribute defines the destination.",
    "instruction_es": "`<a href=\"url\">texto</a>` crea enlaces clicables. El atributo `href` define el destino.",
    "starter_code": '<!-- Crie um link para https://codefuturo.com.br com o texto "Acessar" -->\n<!-- escreva aqui -->\n',
    "hint": "Estrutura: <a href=\"https://...\">texto</a>",
    "tests": [{"stdin": "", "expected_stdout": '<a href="https://codefuturo.com.br">Acessar</a>'}],
  },
  {
    "order": 4,
    "title": "Cor com CSS",
    "chapter": "Capítulo 2: Estilo com CSS",
    "instruction_pt": "CSS estiliza o HTML. A propriedade `color` define a cor do texto. Escreva apenas a declaração CSS que deixa o texto azul.",
    "instruction_en": "CSS styles HTML. The `color` property defines text color. Write only the CSS declaration that makes text blue.",
    "instruction_es": "CSS da estilo al HTML. La propiedad `color` define el color del texto. Escribe solo la declaración CSS que hace el texto azul.",
    "starter_code": '<style>\n  h1 {\n    /* Deixe o texto azul */\n    /* escreva aqui */\n  }\n</style>\n',
    "hint": "Propriedade: color: blue;",
    "tests": [{"stdin": "", "expected_stdout": "color: blue;"}],
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
    "tests": [{"stdin": "", "expected_stdout": "SELECT * FROM usuarios;"}],
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
    "tests": [{"stdin": "", "expected_stdout": "SELECT * FROM usuarios WHERE idade > 18;"}],
  },
  {
    "order": 3,
    "title": "Inserindo dados",
    "chapter": "Capítulo 2: Manipulando Dados",
    "instruction_pt": "`INSERT INTO` adiciona novos registros. Escreva o comando que insere um usuário com nome 'Maria' e email 'maria@email.com' na tabela 'usuarios'.",
    "instruction_en": "`INSERT INTO` adds new records. Write the command that inserts a user with name 'Maria' and email 'maria@email.com'.",
    "instruction_es": "`INSERT INTO` agrega nuevos registros. Escribe el comando que inserta un usuario con nombre 'Maria' y email 'maria@email.com'.",
    "starter_code": "-- Insira um usuário com nome 'Maria' e email 'maria@email.com'\n-- escreva aqui\n",
    "hint": "INSERT INTO tabela (coluna1, coluna2) VALUES ('valor1', 'valor2');",
    "tests": [{"stdin": "", "expected_stdout": "INSERT INTO usuarios (nome, email) VALUES ('Maria', 'maria@email.com');"}],
  },
  {
    "order": 4,
    "title": "Atualizando dados",
    "chapter": "Capítulo 2: Manipulando Dados",
    "instruction_pt": "`UPDATE ... SET ... WHERE` atualiza registros existentes. Sempre use `WHERE` para evitar alterar todos os registros. Escreva o comando que atualiza o email do usuário com id=1.",
    "instruction_en": "`UPDATE ... SET ... WHERE` updates existing records. Always use `WHERE` to avoid changing all records.",
    "instruction_es": "`UPDATE ... SET ... WHERE` actualiza registros existentes. Siempre usa `WHERE` para evitar cambiar todos los registros.",
    "starter_code": "-- Atualize o email para 'novo@email.com' do usuário com id = 1\n-- escreva aqui\n",
    "hint": "UPDATE tabela SET coluna = 'valor' WHERE id = 1;",
    "tests": [{"stdin": "", "expected_stdout": "UPDATE usuarios SET email = 'novo@email.com' WHERE id = 1;"}],
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
    "tests": [{"stdin": "", "expected_stdout": "let nome: string;"}],
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
    "tests": [{"stdin": "", "expected_stdout": "function somar(a: number, b: number): number {"}],
  },
  {
    "order": 3,
    "title": "Interface",
    "chapter": "Capítulo 2: Tipos Avançados",
    "instruction_pt": "Interfaces definem a forma de objetos. Escreva a interface `Aluno` com os campos `nome` (string) e `idade` (number) em uma linha, sem quebras de linha.",
    "instruction_en": "Interfaces define the shape of objects. Write the `Aluno` interface with fields `nome` (string) and `idade` (number) on one line.",
    "instruction_es": "Las interfaces definen la forma de los objetos. Escribe la interfaz `Aluno` con los campos `nome` (string) y `idade` (number) en una línea.",
    "starter_code": '// Escreva a interface Aluno com nome: string e idade: number\n// Formato: interface Aluno { nome: string; idade: number; }\n// escreva aqui\n',
    "hint": "interface NomeInterface { campo: tipo; campo2: tipo; }",
    "tests": [{"stdin": "", "expected_stdout": "interface Aluno { nome: string; idade: number; }"}],
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
    "hint": "System.out.println(\"Olá, Java!\");",
    "tests": [{"stdin": "", "expected_stdout": 'System.out.println("Olá, Java!");'}],
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
    "tests": [{"stdin": "", "expected_stdout": "int idade = 25;"}],
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
    "tests": [{"stdin": "", "expected_stdout": "public static int dobrar(int n) {"}],
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
    "hint": 'cout << "Olá, C++!" << endl;',
    "tests": [{"stdin": "", "expected_stdout": 'cout << "Olá, C++!" << endl;'}],
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
    "tests": [{"stdin": "", "expected_stdout": "int nota = 10;"}],
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
    "tests": [{"stdin": "", "expected_stdout": "int soma(int a, int b) {"}],
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
    "hint": 'fmt.Println("Olá, Go!")',
    "tests": [{"stdin": "", "expected_stdout": 'fmt.Println("Olá, Go!")'}],
  },
  {
    "order": 2,
    "title": "Declaração curta",
    "chapter": "Capítulo 1: Introdução ao Go",
    "instruction_pt": "Go permite declarar variáveis com `:=` — o compilador infere o tipo automaticamente. Escreva a declaração da variável `nome` com valor 'Gopher'.",
    "instruction_en": "Go allows declaring variables with `:=` — the compiler infers the type automatically. Write the declaration of variable `nome` with value 'Gopher'.",
    "instruction_es": "Go permite declarar variables con `:=` — el compilador infiere el tipo automáticamente.",
    "starter_code": '// Declare a variável "nome" com valor "Gopher" usando :=\n// escreva aqui\n',
    "hint": 'nome := "Gopher"',
    "tests": [{"stdin": "", "expected_stdout": 'nome := "Gopher"'}],
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
    "tests": [{"stdin": "", "expected_stdout": "func dobrar(n int) int {"}],
  },
],

# ── AI Prompts ───────────────────────────────────────────────────────────────
"ai-prompts": [
  {
    "order": 1,
    "title": "Comando Direto",
    "chapter": "Capítulo 1: Fundamentos de Prompting",
    "instruction_pt": "Um bom prompt é específico e contextualizado. Em vez de 'Me fale sobre Python', escreva um prompt que peça exatamente 3 exemplos de uso de Python para ciência de dados, em português.",
    "instruction_en": "A good prompt is specific and contextual. Instead of 'Tell me about Python', write a prompt that asks for exactly 3 Python use cases for data science.",
    "instruction_es": "Un buen prompt es específico y contextualizado. Escribe un prompt que pida exactamente 3 casos de uso de Python para ciencia de datos.",
    "starter_code": '// Escreva um prompt direto e específico:\n// Peça 3 exemplos de uso de Python para ciência de dados em português\n// escreva aqui\n',
    "hint": "Seja específico: quantidade, tema, formato, idioma.",
    "tests": [{"stdin": "", "expected_stdout": "Dê-me 3 exemplos de uso de Python para ciência de dados, em português."}],
  },
  {
    "order": 2,
    "title": "Atribuindo uma Persona",
    "chapter": "Capítulo 1: Fundamentos de Prompting",
    "instruction_pt": "Atribuir uma persona à IA muda a forma como ela responde. 'Aja como um professor de matemática do ensino médio' gera respostas pedagógicas. Escreva o prompt que pede à IA que atue como um tutor de programação paciente e explique o que é uma variável.",
    "instruction_en": "Assigning a persona changes how the AI responds. Write the prompt that asks the AI to act as a patient programming tutor and explain what a variable is.",
    "instruction_es": "Asignar una persona cambia cómo responde la IA. Escribe el prompt que le pide a la IA que actúe como un tutor de programación paciente.",
    "starter_code": '// Escreva um prompt com persona:\n// Peça à IA que aja como tutor de programação e explique variáveis\n// escreva aqui\n',
    "hint": "Estrutura: Aja como [persona]. [Tarefa].",
    "tests": [{"stdin": "", "expected_stdout": "Aja como um tutor de programação paciente. Explique o que é uma variável de forma simples."}],
  },
  {
    "order": 3,
    "title": "Cadeia de Pensamento",
    "chapter": "Capítulo 2: Técnicas Avançadas",
    "instruction_pt": "Chain-of-thought (cadeia de pensamento) melhora respostas pedindo que a IA raciocine passo a passo antes de responder. Escreva o prompt que pede à IA para resolver 'Quanto é 17 × 23?' pensando passo a passo.",
    "instruction_en": "Chain-of-thought improves responses by asking the AI to reason step by step. Write the prompt that asks the AI to solve '17 × 23' thinking step by step.",
    "instruction_es": "La cadena de pensamiento mejora las respuestas pidiendo a la IA que razone paso a paso.",
    "starter_code": '// Escreva um prompt chain-of-thought:\n// Peça à IA para resolver 17 × 23 pensando passo a passo\n// escreva aqui\n',
    "hint": "Adicione 'Pense passo a passo antes de responder.' ao final do prompt.",
    "tests": [{"stdin": "", "expected_stdout": "Quanto é 17 × 23? Pense passo a passo antes de responder."}],
  },
],

} # fim LESSONS

# ---------------------------------------------------------------------------
# Engine de inserção
# ---------------------------------------------------------------------------

def _slug_base(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:40]


def _build_doc(path_cfg: dict, les: dict) -> dict:
    order = les["order"]
    return {
        "id": str(uuid.uuid4()),
        "slug": f"{path_cfg['slug']}-{order:02d}-{_slug_base(les['title'])}",
        "path_slug": path_cfg["slug"],
        "order": order,
        "title": les["title"],
        "chapter": les.get("chapter", "Capítulo 1"),
        "instruction_pt": les.get("instruction_pt", ""),
        "instruction_en": les.get("instruction_en", ""),
        "instruction_es": les.get("instruction_es", ""),
        "starter_code": les.get("starter_code", ""),
        "hint": les.get("hint", ""),
        "tests": les.get("tests", []),
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
