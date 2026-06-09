"""Substitui a secao javascript no seed_static.py pelas 19 licoes novas."""

# ---------------------------------------------------------------------------
# Converte Python dicts em texto de codigo Python (para injetar no seed)
# ---------------------------------------------------------------------------

def _py(val, ind=4):
    if isinstance(val, str):
        escaped = (val.replace("\\", "\\\\")
                      .replace('"', '\\"')
                      .replace("\n", "\\n"))
        return f'"{escaped}"'
    if isinstance(val, bool):
        return "True" if val else "False"
    if isinstance(val, (int, float)):
        return str(val)
    if isinstance(val, list):
        if not val:
            return "[]"
        items = [" " * (ind + 2) + _py(v, ind + 2) for v in val]
        inner = ",\n".join(items)
        return f"[\n{inner},\n{' ' * ind}]"
    if isinstance(val, dict):
        lines = [f'{" " * (ind + 2)}"{k}": {_py(v, ind + 2)}' for k, v in val.items()]
        inner = ",\n".join(lines)
        return f"{{\n{inner},\n{' ' * ind}}}"
    return repr(val)


def fmt_lesson(les, ind=2):
    lines = [f'{" " * (ind + 2)}"{k}": {_py(v, ind + 2)}' for k, v in les.items()]
    inner = ",\n".join(lines)
    return f"{' ' * ind}{{\n{inner},\n{' ' * ind}}}"


# ---------------------------------------------------------------------------
# 19 licoes da trilha JavaScript
# ---------------------------------------------------------------------------

LESSONS = [
    # ── L01 ─────────────────────────────────────────────────────────────────
    {
        "order": 1,
        "slug": "js-console-log",
        "title": "console.log",
        "chapter": "Capítulo 1: Fundamentos",
        "theory": (
            "`console.log()` é o `print()` do JavaScript — exibe qualquer valor no terminal.\n\n"
            "## Como funciona\n\n"
            "```javascript\n"
            'console.log("Olá, JavaScript!");  // Olá, JavaScript!\n'
            "console.log(42);                  // 42\n"
            "console.log(true);                // true\n"
            "```\n\n"
            "- Passe qualquer valor entre os parênteses\n"
            "- Textos ficam entre aspas duplas `\"` ou simples `'`\n"
            "- Você pode exibir números e booleanos sem aspas\n\n"
            "## Múltiplos valores\n\n"
            "```javascript\n"
            'console.log("Versão:", 2024);     // Versão: 2024\n'
            "```\n\n"
            "## No exercício\n\n"
            'Exiba exatamente `Olá, JavaScript!` no console usando `console.log()`.'
        ),
        "instruction_pt": 'Use `console.log()` para exibir `Olá, JavaScript!` no terminal.',
        "instruction_en": 'Use `console.log()` to display `Hello, JavaScript!` in the terminal.',
        "instruction_es": 'Usa `console.log()` para mostrar `¡Hola, JavaScript!` en la terminal.',
        "starter_code": '// Exiba "Olá, JavaScript!" no console\n// escreva aqui\n',
        "hint": 'Use: console.log("Olá, JavaScript!")',
        "hints": [
            '`console.log()` em JS é como `print()` em Python — exibe no terminal.',
            'Solução: `console.log("Olá, JavaScript!")` — não esqueça a exclamação!',
        ],
        "tests": [{"stdin": "", "expected_stdout": "Olá, JavaScript!"}],
        "quiz": [
            {
                "question": "Como exibir texto no console em JavaScript?",
                "options": ["print('texto')", "echo('texto')", "console.log('texto')", "log('texto')"],
                "correct": 2,
            },
            {
                "question": "console.log() é útil principalmente para:",
                "options": ["Criar interfaces gráficas", "Depurar código e exibir resultados", "Enviar e-mails", "Salvar arquivos"],
                "correct": 1,
            },
        ],
    },

    # ── L02 ─────────────────────────────────────────────────────────────────
    {
        "order": 2,
        "slug": "js-variaveis",
        "title": "let e const",
        "chapter": "Capítulo 1: Fundamentos",
        "theory": (
            "Em JavaScript, variáveis são criadas com `let` (pode mudar) ou `const` (valor fixo).\n\n"
            "## Como funciona\n\n"
            "```javascript\n"
            'const linguagem = "JavaScript";  // não pode mudar\n'
            "let versao = 2024;               // pode mudar\n\n"
            "versao = 2025;                   // ok!\n"
            '// linguagem = "Python";         // ERRO — const não aceita reatribuição\n'
            "```\n\n"
            "- Use `const` como padrão — só troque por `let` quando precisar reatribuir\n"
            "- Textos ficam entre aspas `\"texto\"`, números sem aspas `42`\n\n"
            "## Concatenando com +\n\n"
            "```javascript\n"
            'const nome = "Ana";\n'
            "const idade = 16;\n"
            'console.log(nome + " tem " + idade + " anos");  // Ana tem 16 anos\n'
            "```\n\n"
            "## No exercício\n\n"
            "Use as variáveis `cidade` e `populacao` já declaradas e concatene-as para exibir a frase pedida."
        ),
        "instruction_pt": (
            "As variáveis `cidade` e `populacao` já estão declaradas.\n\n"
            "Complete o `console.log()` usando concatenação (`+`) para exibir:\n"
            "`São Paulo tem 12000000 habitantes`"
        ),
        "instruction_en": "Complete the console.log() to display: `São Paulo has 12000000 inhabitants`",
        "instruction_es": "Completa el console.log() para mostrar: `São Paulo tiene 12000000 habitantes`",
        "starter_code": (
            'const cidade = "São Paulo";\n'
            "let populacao = 12000000;\n"
            "// Exiba: São Paulo tem 12000000 habitantes\n"
            "console.log(___);\n"
        ),
        "hint": 'Use: console.log(cidade + " tem " + populacao + " habitantes");',
        "hints": [
            'Concatene com `+`: `cidade + " tem " + populacao + " habitantes"`.',
            'Resultado esperado: `São Paulo tem 12000000 habitantes` — sem vírgulas extras.',
        ],
        "tests": [{"stdin": "", "expected_stdout": "São Paulo tem 12000000 habitantes"}],
        "quiz": [
            {
                "question": "Qual palavra-chave usar para uma variável que nunca muda em JS?",
                "options": ["let", "var", "const", "static"],
                "correct": 2,
            },
            {
                "question": "O que acontece se você tentar reatribuir uma const?",
                "options": ["Ela muda normalmente", "O programa ignora a linha", "Ocorre um erro TypeError", "Ela vira let automaticamente"],
                "correct": 2,
            },
        ],
    },

    # ── L03 ─────────────────────────────────────────────────────────────────
    {
        "order": 3,
        "slug": "js-tipos-de-dados",
        "title": "Tipos de Dados",
        "chapter": "Capítulo 1: Fundamentos",
        "theory": (
            "JavaScript tem tipos primitivos que definem como os dados são armazenados e operados. "
            "`typeof` revela o tipo de qualquer valor.\n\n"
            "## Como funciona\n\n"
            "```javascript\n"
            'console.log(typeof 42);          // number\n'
            'console.log(typeof "JavaScript");// string\n'
            'console.log(typeof true);        // boolean\n'
            'console.log(typeof undefined);   // undefined\n'
            "```\n\n"
            "- **number** — inteiros e decimais: `42`, `3.14`, `-7`\n"
            "- **string** — textos entre aspas: `\"Olá\"`, `'mundo'`\n"
            "- **boolean** — verdadeiro ou falso: `true`, `false`\n"
            "- **undefined** — variável declarada sem valor\n\n"
            "## Comparando tipos\n\n"
            "```javascript\n"
            'console.log(typeof 3.14);   // number — decimais também são number\n'
            'console.log(typeof \"42\");   // string — número entre aspas é texto!\n'
            "```\n\n"
            "## No exercício\n\n"
            "Use `typeof` para revelar o tipo de três valores diferentes."
        ),
        "instruction_pt": (
            "Use `console.log(typeof ...)` para exibir o tipo de cada valor:\n\n"
            "- `100` → `number`\n"
            "- `\"JavaScript\"` → `string`\n"
            "- `false` → `boolean`"
        ),
        "instruction_en": "Use `console.log(typeof ...)` to show the type of 100, \"JavaScript\", and false.",
        "instruction_es": "Usa `console.log(typeof ...)` para mostrar el tipo de 100, \"JavaScript\" y false.",
        "starter_code": (
            "console.log(typeof ___);\n"
            "console.log(typeof ___);\n"
            "console.log(typeof ___);\n"
        ),
        "hint": "Preencha os ___ com: 100, \"JavaScript\" e false (nessa ordem).",
        "hints": [
            "Preencha os três `___` com os valores: `100`, `\"JavaScript\"` e `false`.",
            'Resultado esperado (uma por linha): `number`, `string`, `boolean`.',
        ],
        "tests": [{"stdin": "", "expected_stdout": "number\nstring\nboolean"}],
        "quiz": [
            {
                "question": "Qual é o tipo de `3.14` em JavaScript?",
                "options": ["float", "double", "number", "decimal"],
                "correct": 2,
            },
            {
                "question": "O que `typeof \"42\"` retorna?",
                "options": ["number", "string", "integer", "char"],
                "correct": 1,
            },
            {
                "question": "Qual operador revela o tipo de um valor em JS?",
                "options": ["typecheck", "type()", "typeof", "getType"],
                "correct": 2,
            },
        ],
    },

    # ── L04 ─────────────────────────────────────────────────────────────────
    {
        "order": 4,
        "slug": "js-operadores",
        "title": "Operadores",
        "chapter": "Capítulo 1: Fundamentos",
        "theory": (
            "Operadores aritméticos em JavaScript funcionam como na matemática — com um bônus: "
            "`%` para resto e `**` para potência.\n\n"
            "## Como funciona\n\n"
            "```javascript\n"
            "console.log(10 + 3);   // 13  — soma\n"
            "console.log(10 - 3);   //  7  — subtração\n"
            "console.log(10 * 3);   // 30  — multiplicação\n"
            "console.log(10 / 4);   //  2.5 — divisão\n"
            "console.log(10 % 3);   //  1  — resto da divisão\n"
            "console.log(2 ** 8);   // 256 — potência\n"
            "```\n\n"
            "- O operador `%` retorna o **resto** da divisão inteira: `17 % 5` = 2 (porque 17 = 3×5 + **2**)\n"
            "- `**` é o operador de potência: `2 ** 10` = 1024\n\n"
            "## No exercício\n\n"
            "Calcule três operações e exiba cada resultado com `console.log()`."
        ),
        "instruction_pt": (
            "Exiba o resultado de três operações (uma por linha):\n\n"
            "- `20 + 8` → `28`\n"
            "- `7 * 6` → `42`\n"
            "- `17 % 5` → `2`"
        ),
        "instruction_en": "Display the result of: 20 + 8, 7 * 6, and 17 % 5.",
        "instruction_es": "Muestra el resultado de: 20 + 8, 7 * 6 y 17 % 5.",
        "starter_code": (
            "console.log(___);\n"
            "console.log(___);\n"
            "console.log(___);\n"
        ),
        "hint": "Preencha com: 20 + 8, depois 7 * 6, depois 17 % 5.",
        "hints": [
            "Preencha cada `___` com a operação: `20 + 8`, `7 * 6` e `17 % 5`.",
            "`17 % 5` = 2 porque 17 = 3×5 + 2 — o `%` retorna o resto da divisão.",
        ],
        "tests": [{"stdin": "", "expected_stdout": "28\n42\n2"}],
        "quiz": [
            {
                "question": "O que o operador `%` calcula em JavaScript?",
                "options": ["Porcentagem", "Resto da divisão", "Potência", "Divisão decimal"],
                "correct": 1,
            },
            {
                "question": "Qual o resultado de `2 ** 3` em JavaScript?",
                "options": ["6", "5", "8", "9"],
                "correct": 2,
            },
        ],
    },

    # ── L05 ─────────────────────────────────────────────────────────────────
    {
        "order": 5,
        "slug": "js-template-literals",
        "title": "Template Literals",
        "chapter": "Capítulo 1: Fundamentos",
        "theory": (
            "Template literals usam **crase** (`) e permitem inserir variáveis com `${}` — "
            "muito mais limpo do que concatenar com `+`.\n\n"
            "## Como funciona\n\n"
            "```javascript\n"
            'const nome = "Ana";\n'
            "const idade = 16;\n\n"
            "// Com concatenação (verboso)\n"
            'console.log(nome + " tem " + idade + " anos");\n\n'
            "// Com template literal (limpo)\n"
            "console.log(`${nome} tem ${idade} anos`);\n"
            "// Ana tem 16 anos\n"
            "```\n\n"
            "- Use crase `` ` `` (não aspas) para abrir e fechar o template\n"
            "- Coloque qualquer expressão dentro de `${  }`\n\n"
            "## Expressões dentro de ${}\n\n"
            "```javascript\n"
            "const preco = 50;\n"
            "const qtd = 3;\n"
            "console.log(`Total: R$ ${preco * qtd}`);  // Total: R$ 150\n"
            "```\n\n"
            "## No exercício\n\n"
            "Use um template literal para exibir a frase com as variáveis `nome` e `nota`."
        ),
        "instruction_pt": (
            "Use um template literal (crase + `${}`) para exibir:\n\n"
            "`Carlos tirou 9.5 na prova`"
        ),
        "instruction_en": "Use a template literal to display: `Carlos got 9.5 on the test`",
        "instruction_es": "Usa un template literal para mostrar: `Carlos sacó 9.5 en el examen`",
        "starter_code": (
            'const nome = "Carlos";\n'
            "const nota = 9.5;\n"
            "// Exiba: Carlos tirou 9.5 na prova\n"
            "// Use template literal com crase e ${}\n"
            "console.log(___)\n"
        ),
        "hint": "Use crase: console.log(`${nome} tirou ${nota} na prova`)",
        "hints": [
            "Abra com crase `` ` ``, insira as variáveis com `${}`: `` `${nome} tirou ${nota} na prova` ``",
            "Solução: `console.log(\\`${nome} tirou ${nota} na prova\\`)`",
        ],
        "tests": [{"stdin": "", "expected_stdout": "Carlos tirou 9.5 na prova"}],
        "quiz": [
            {
                "question": "Qual caractere delimita um template literal em JS?",
                "options": ["Aspas duplas \"", "Aspas simples '", "Crase `", "Colchetes []"],
                "correct": 2,
            },
            {
                "question": "Como inserir uma variável dentro de um template literal?",
                "options": ["%(variavel)", "${variavel}", "#{variavel}", "{{variavel}}"],
                "correct": 1,
            },
            {
                "question": "O que `console.log(`Resultado: ${2 + 3}`)` exibe?",
                "options": ["Resultado: 2 + 3", "Resultado: ${2 + 3}", "Resultado: 5", "Erro de sintaxe"],
                "correct": 2,
            },
        ],
    },

    # ── L06 ─────────────────────────────────────────────────────────────────
    {
        "order": 6,
        "slug": "js-comparadores",
        "title": "Comparadores",
        "chapter": "Capítulo 1: Fundamentos",
        "theory": (
            "Comparadores retornam `true` ou `false`. Em JS, use sempre `===` (igualdade estrita) "
            "em vez de `==` — ela compara valor **e** tipo.\n\n"
            "## Como funciona\n\n"
            "```javascript\n"
            "const a = 10;\n"
            "const b = 5;\n\n"
            "console.log(a > b);    // true  — maior que\n"
            "console.log(a < b);    // false — menor que\n"
            "console.log(a === b);  // false — igual (valor e tipo)\n"
            "console.log(a !== b);  // true  — diferente\n"
            "```\n\n"
            "- `>` e `<` comparam grandeza\n"
            "- `>=` e `<=` incluem a igualdade\n"
            "- `===` e `!==` são os comparadores de igualdade recomendados em JS\n\n"
            "## Operadores lógicos\n\n"
            "```javascript\n"
            "console.log(10 > 5 && 3 > 1);  // true  — E (ambos verdadeiros)\n"
            "console.log(10 > 5 || 1 > 9);  // true  — OU (um basta)\n"
            "console.log(!(10 > 5));         // false — NÃO (inverte)\n"
            "```\n\n"
            "## No exercício\n\n"
            "Compare `a = 15` e `b = 8` e exiba três resultados booleanos."
        ),
        "instruction_pt": (
            "Com `a = 15` e `b = 8`, exiba (uma por linha):\n\n"
            "- `a > b` → `true`\n"
            "- `a === b` → `false`\n"
            "- `a !== b` → `true`"
        ),
        "instruction_en": "With a = 15 and b = 8, display true, false, true using comparison operators.",
        "instruction_es": "Con a = 15 y b = 8, muestra true, false, true usando operadores de comparación.",
        "starter_code": (
            "const a = 15;\n"
            "const b = 8;\n"
            "console.log(___);\n"
            "console.log(___);\n"
            "console.log(___);\n"
        ),
        "hint": "Preencha com: a > b, depois a === b, depois a !== b.",
        "hints": [
            "Preencha cada `___` com: `a > b`, `a === b`, `a !== b` (nessa ordem).",
            "`===` compara valor **e tipo** — é diferente de `==`. Sempre use `===` em JS.",
        ],
        "tests": [{"stdin": "", "expected_stdout": "true\nfalse\ntrue"}],
        "quiz": [
            {
                "question": "Por que usar `===` em vez de `==` em JavaScript?",
                "options": ["São idênticos", "`===` compara valor e tipo, evitando conversões inesperadas", "`==` é mais rápido", "`===` só funciona com números"],
                "correct": 1,
            },
            {
                "question": "Qual o resultado de `5 !== \"5\"` em JavaScript?",
                "options": ["false", "true", "undefined", "Erro"],
                "correct": 1,
            },
        ],
    },

    # ── L07 ─────────────────────────────────────────────────────────────────
    {
        "order": 7,
        "slug": "js-if-else",
        "title": "if / else",
        "chapter": "Capítulo 2: Controle de Fluxo",
        "theory": (
            "`if/else` executa blocos diferentes dependendo de uma condição — é a tomada de decisão do código.\n\n"
            "## Como funciona\n\n"
            "```javascript\n"
            "const temperatura = 35;\n\n"
            "if (temperatura > 30) {\n"
            '  console.log("Está quente!");\n'
            "} else {\n"
            '  console.log("Temperatura agradável.");\n'
            "}\n"
            "// Está quente!\n"
            "```\n\n"
            "- A condição fica entre `()` após o `if`\n"
            "- Cada bloco fica entre `{}`\n"
            "- O `else` é opcional — executa quando a condição é `false`\n\n"
            "## No exercício\n\n"
            "Complete a condição do `if` para verificar se `idade` é maior ou igual a 18."
        ),
        "instruction_pt": (
            "Complete a condição do `if` para verificar se `idade >= 18`.\n\n"
            "- Se sim: exiba `Maior de idade`\n"
            "- Se não: exiba `Menor de idade`"
        ),
        "instruction_en": "Complete the if condition to check if age >= 18.",
        "instruction_es": "Completa la condición del if para verificar si edad >= 18.",
        "starter_code": (
            "const idade = 20;\n"
            "// Complete a condição\n"
            "if (___) {\n"
            '  console.log("Maior de idade");\n'
            "} else {\n"
            '  console.log("Menor de idade");\n'
            "}\n"
        ),
        "hint": "A condição é: idade >= 18",
        "hints": [
            "A condição vai entre os parênteses: `if (idade >= 18)`.",
            'Com `idade = 20`, a condição é verdadeira — o programa deve exibir `"Maior de idade"`.',
        ],
        "tests": [{"stdin": "", "expected_stdout": "Maior de idade"}],
        "quiz": [
            {
                "question": "O que acontece quando a condição do `if` é false e não há `else`?",
                "options": ["O programa encerra", "O bloco if é ignorado e a execução continua", "Ocorre um erro", "O bloco if executa mesmo assim"],
                "correct": 1,
            },
            {
                "question": "Qual a sintaxe correta de um if em JavaScript?",
                "options": ["if condicao:", "if (condicao) {}", "if [condicao] {}", "if <condicao> {}"],
                "correct": 1,
            },
        ],
    },

    # ── L08 ─────────────────────────────────────────────────────────────────
    {
        "order": 8,
        "slug": "js-else-if",
        "title": "else if",
        "chapter": "Capítulo 2: Controle de Fluxo",
        "theory": (
            "`else if` testa múltiplas condições em sequência — é o equivalente ao `elif` do Python.\n\n"
            "## Como funciona\n\n"
            "```javascript\n"
            "const hora = 14;\n\n"
            "if (hora < 12) {\n"
            '  console.log("Bom dia!");\n'
            "} else if (hora < 18) {\n"
            '  console.log("Boa tarde!");\n'
            "} else {\n"
            '  console.log("Boa noite!");\n'
            "}\n"
            "// Boa tarde!\n"
            "```\n\n"
            "- O JS testa cada condição de cima para baixo e executa **apenas o primeiro bloco verdadeiro**\n"
            "- A ordem importa: coloque as condições mais específicas primeiro\n\n"
            "## No exercício\n\n"
            "Preencha os dois valores nos `___` para criar um sistema de avaliação escolar."
        ),
        "instruction_pt": (
            "Preencha os dois `___` para que:\n\n"
            "- `nota >= 7` → `Aprovado`\n"
            "- `nota >= 5` → `Recuperacao`\n"
            "- Abaixo disso → `Reprovado`\n\n"
            "Com `nota = 7.5` o resultado deve ser `Aprovado`."
        ),
        "instruction_en": "Fill the two ___ so that nota >= 7 prints Aprovado, nota >= 5 prints Recuperacao.",
        "instruction_es": "Rellena los dos ___ para que nota >= 7 muestre Aprovado, nota >= 5 Recuperacao.",
        "starter_code": (
            "const nota = 7.5;\n"
            "if (nota >= ___) {\n"
            '  console.log("Aprovado");\n'
            "} else if (nota >= ___) {\n"
            '  console.log("Recuperacao");\n'
            "} else {\n"
            '  console.log("Reprovado");\n'
            "}\n"
        ),
        "hint": "Troque os ___ por 7 (aprovado) e 5 (recuperação).",
        "hints": [
            "Troque o primeiro `___` por `7` e o segundo por `5`.",
            "A ordem importa: verifique `>= 7` primeiro. Se colocar `>= 5` antes, notas 7+ entrariam em Recuperacao.",
        ],
        "tests": [{"stdin": "", "expected_stdout": "Aprovado"}],
        "quiz": [
            {
                "question": "Se uma condição `if` for verdadeira, o que acontece com os `else if` seguintes?",
                "options": ["Todos são testados", "São ignorados", "Causam erro", "São executados também"],
                "correct": 1,
            },
            {
                "question": "Quantos `else if` você pode encadear num mesmo bloco?",
                "options": ["No máximo 3", "No máximo 10", "Apenas 1", "Quantos quiser"],
                "correct": 3,
            },
        ],
    },

    # ── L09 ─────────────────────────────────────────────────────────────────
    {
        "order": 9,
        "slug": "js-for",
        "title": "for loop",
        "chapter": "Capítulo 2: Controle de Fluxo",
        "theory": (
            "O `for` repete um bloco um número determinado de vezes — "
            "perfeito quando você sabe quantas iterações precisa.\n\n"
            "## Como funciona\n\n"
            "```javascript\n"
            "for (let i = 1; i <= 5; i++) {\n"
            "  console.log(`Passo ${i}`);\n"
            "}\n"
            "// Passo 1  Passo 2  Passo 3  Passo 4  Passo 5\n"
            "```\n\n"
            "O `for` tem três partes separadas por `;`:\n"
            "- **Início**: `let i = 1` — cria e inicializa o contador\n"
            "- **Condição**: `i <= 5` — enquanto isso for true, o loop continua\n"
            "- **Incremento**: `i++` — atualiza o contador a cada volta\n\n"
            "## Acumulando valores\n\n"
            "```javascript\n"
            "let soma = 0;\n"
            "for (let i = 1; i <= 4; i++) {\n"
            "  soma += i;\n"
            "}\n"
            "console.log(soma);  // 10 (1+2+3+4)\n"
            "```\n\n"
            "## No exercício\n\n"
            "Complete os dois `___` no `for` para exibir a tabuada do 4 de 1 a 5."
        ),
        "instruction_pt": (
            "Complete o `for` para exibir a tabuada do 4 de 1 a 5:\n\n"
            "```\n"
            "4 x 1 = 4\n"
            "4 x 2 = 8\n"
            "...\n"
            "4 x 5 = 20\n"
            "```"
        ),
        "instruction_en": "Complete the for loop to display the multiplication table of 4 from 1 to 5.",
        "instruction_es": "Completa el bucle for para mostrar la tabla del 4 del 1 al 5.",
        "starter_code": (
            "// Exiba a tabuada do 4 de 1 a 5\n"
            "for (let i = ___; i <= ___; i++) {\n"
            "  console.log(`4 x ${i} = ${4 * i}`);\n"
            "}\n"
        ),
        "hint": "O loop começa em 1 e vai até 5: for (let i = 1; i <= 5; i++)",
        "hints": [
            "Troque os dois `___` por `1` e `5`: `for (let i = 1; i <= 5; i++)`.",
            "O `i++` já está pronto — ele aumenta `i` de 1 em 1 a cada volta do loop.",
        ],
        "tests": [{"stdin": "", "expected_stdout": "4 x 1 = 4\n4 x 2 = 8\n4 x 3 = 12\n4 x 4 = 16\n4 x 5 = 20"}],
        "quiz": [
            {
                "question": "O que `i++` faz dentro de um for loop?",
                "options": ["Cria uma nova variável", "Incrementa i em 1 a cada volta", "Reinicia o loop", "Para o loop"],
                "correct": 1,
            },
            {
                "question": "Quantas vezes o loop `for (let i = 0; i < 3; i++)` executa?",
                "options": ["2", "3", "4", "Infinitas"],
                "correct": 1,
            },
        ],
    },

    # ── L10 ─────────────────────────────────────────────────────────────────
    {
        "order": 10,
        "slug": "js-while",
        "title": "while",
        "chapter": "Capítulo 2: Controle de Fluxo",
        "theory": (
            "O `while` repete um bloco **enquanto** uma condição for verdadeira — "
            "ideal quando você não sabe quantas iterações serão necessárias.\n\n"
            "## Como funciona\n\n"
            "```javascript\n"
            "let contador = 1;\n\n"
            "while (contador <= 3) {\n"
            "  console.log(contador);\n"
            "  contador++;\n"
            "}\n"
            "// 1  2  3\n"
            "```\n\n"
            "- A condição é verificada **antes** de cada volta\n"
            "- Se já começa `false`, o bloco nunca executa\n"
            "- **Cuidado**: esquecer de atualizar o contador cria um loop infinito!\n\n"
            "## for vs while\n\n"
            "```javascript\n"
            "// Use for quando sabe o número de repetições\n"
            "for (let i = 1; i <= 5; i++) { ... }\n\n"
            "// Use while quando a condição é dinâmica\n"
            "while (saldo > 0) { ... }\n"
            "```\n\n"
            "## No exercício\n\n"
            "Complete a condição do `while` para exibir os números de 1 a 5."
        ),
        "instruction_pt": (
            "Complete o `___` na condição do `while` para exibir:\n\n"
            "`1`, `2`, `3`, `4`, `5` (cada número numa linha)"
        ),
        "instruction_en": "Complete the while condition to display numbers 1 through 5.",
        "instruction_es": "Completa la condición del while para mostrar los números del 1 al 5.",
        "starter_code": (
            "let i = 1;\n"
            "while (i ___ 5) {\n"
            "  console.log(i);\n"
            "  i++;\n"
            "}\n"
        ),
        "hint": "A condição deve ser `i <= 5` para incluir o 5.",
        "hints": [
            "Troque `___` por `<=` para que o loop inclua o número 5.",
            "Com `i > 5` o loop nunca executa (1 não é maior que 5). Use `<=`.",
        ],
        "tests": [{"stdin": "", "expected_stdout": "1\n2\n3\n4\n5"}],
        "quiz": [
            {
                "question": "O que acontece se a condição do while nunca ficar false?",
                "options": ["O programa encerra normalmente", "O loop executa apenas uma vez", "Loop infinito — o programa trava", "JS lança um erro automaticamente"],
                "correct": 2,
            },
            {
                "question": "Quando é preferível usar `while` em vez de `for`?",
                "options": ["Quando sabe o número exato de repetições", "Quando a condição de parada é dinâmica ou desconhecida", "Nunca, for é sempre melhor", "Apenas para loops de 1 a 10"],
                "correct": 1,
            },
        ],
    },

    # ── L11 ─────────────────────────────────────────────────────────────────
    {
        "order": 11,
        "slug": "js-funcoes",
        "title": "Funções",
        "chapter": "Capítulo 3: Funções e Dados",
        "theory": (
            "Funções são blocos de código reutilizáveis — você define uma vez e chama quantas vezes quiser.\n\n"
            "## Como funciona\n\n"
            "```javascript\n"
            "function saudacao(nome) {\n"
            "  return `Ola, ${nome}!`;\n"
            "}\n\n"
            'console.log(saudacao("Ana"));    // Ola, Ana!\n'
            'console.log(saudacao("Carlos")); // Ola, Carlos!\n'
            "```\n\n"
            "- `function` declara a função\n"
            "- O nome vem depois de `function`\n"
            "- `return` devolve o resultado para quem chamou\n"
            "- Sem `return`, a função retorna `undefined`\n\n"
            "## Função sem parâmetros\n\n"
            "```javascript\n"
            "function boasVindas() {\n"
            '  return "Bem-vindo ao CodeFuturo!";\n'
            "}\n"
            "console.log(boasVindas());  // Bem-vindo ao CodeFuturo!\n"
            "```\n\n"
            "## No exercício\n\n"
            "Complete o `return` da função `saudacao()` para que ela retorne `Ola, [nome]!`."
        ),
        "instruction_pt": (
            "Complete o `return` da função para que:\n\n"
            "- `saudacao(\"Ana\")` retorne `Ola, Ana!`\n"
            "- `saudacao(\"Carlos\")` retorne `Ola, Carlos!`"
        ),
        "instruction_en": "Complete the return statement so saudacao(\"Ana\") returns \"Ola, Ana!\"",
        "instruction_es": "Completa el return para que saudacao(\"Ana\") retorne \"Ola, Ana!\"",
        "starter_code": (
            "function saudacao(nome) {\n"
            "  return ___;\n"
            "}\n"
            'console.log(saudacao("Ana"));\n'
            'console.log(saudacao("Carlos"));\n'
        ),
        "hint": "Use template literal: return `Ola, ${nome}!`",
        "hints": [
            "Use um template literal no return: `` return `Ola, ${nome}!`; ``",
            "O parâmetro `nome` já contém o valor passado na chamada — use `${nome}` para interpolá-lo.",
        ],
        "tests": [{"stdin": "", "expected_stdout": "Ola, Ana!\nOla, Carlos!"}],
        "quiz": [
            {
                "question": "O que acontece se uma função não tem `return`?",
                "options": ["Erro de sintaxe", "Retorna 0", "Retorna undefined", "Retorna null"],
                "correct": 2,
            },
            {
                "question": "Como chamar a função `calcular()` e exibir seu resultado?",
                "options": ["print(calcular())", "console.log calcular()", "console.log(calcular())", "call calcular()"],
                "correct": 2,
            },
        ],
    },

    # ── L12 ─────────────────────────────────────────────────────────────────
    {
        "order": 12,
        "slug": "js-parametros",
        "title": "Parâmetros e Retorno",
        "chapter": "Capítulo 3: Funções e Dados",
        "theory": (
            "Funções podem receber múltiplos parâmetros e devolver qualquer tipo de valor com `return`.\n\n"
            "## Como funciona\n\n"
            "```javascript\n"
            "function soma(a, b) {\n"
            "  return a + b;\n"
            "}\n\n"
            "const resultado = soma(4, 6);\n"
            "console.log(resultado);  // 10\n"
            "```\n\n"
            "- Parâmetros são as variáveis listadas na definição: `(a, b)`\n"
            "- Argumentos são os valores passados na chamada: `soma(4, 6)`\n"
            "- O `return` pode devolver qualquer valor: número, string, boolean\n\n"
            "## Retornando boolean\n\n"
            "```javascript\n"
            "function ehPar(n) {\n"
            "  return n % 2 === 0;\n"
            "}\n"
            "console.log(ehPar(4));   // true\n"
            "console.log(ehPar(7));   // false\n"
            "```\n\n"
            "## No exercício\n\n"
            "Complete as duas funções: `calcularMedia(a, b, c)` e `ehAprovado(media)`."
        ),
        "instruction_pt": (
            "Complete as duas funções para que:\n\n"
            "- `calcularMedia(6, 8, 7)` retorne `7`\n"
            "- `ehAprovado(7)` retorne `true` (média >= 7 é aprovado)"
        ),
        "instruction_en": "Complete calcularMedia(6,8,7) returning 7 and ehAprovado(7) returning true.",
        "instruction_es": "Completa calcularMedia(6,8,7) que retorne 7 y ehAprovado(7) que retorne true.",
        "starter_code": (
            "function calcularMedia(a, b, c) {\n"
            "  return ___;\n"
            "}\n"
            "function ehAprovado(media) {\n"
            "  return media ___ 7;\n"
            "}\n"
            "console.log(calcularMedia(6, 8, 7));\n"
            "console.log(ehAprovado(7));\n"
        ),
        "hint": "Media: (a + b + c) / 3. Aprovado: media >= 7.",
        "hints": [
            "Para a média: `return (a + b + c) / 3;` — (6+8+7)/3 = 7.",
            "Para aprovado: `return media >= 7;` — retorna true se a média for 7 ou mais.",
        ],
        "tests": [{"stdin": "", "expected_stdout": "7\ntrue"}],
        "quiz": [
            {
                "question": "Qual a diferença entre parâmetro e argumento?",
                "options": ["São a mesma coisa", "Parâmetro é na definição; argumento é na chamada", "Argumento é na definição; parâmetro é na chamada", "Parâmetro é opcional; argumento obrigatório"],
                "correct": 1,
            },
            {
                "question": "O que `return n % 2 === 0` devolve quando n = 5?",
                "options": ["1", "true", "false", "0"],
                "correct": 2,
            },
        ],
    },

    # ── L13 ─────────────────────────────────────────────────────────────────
    {
        "order": 13,
        "slug": "js-arrays",
        "title": "Arrays",
        "chapter": "Capítulo 3: Funções e Dados",
        "theory": (
            "Arrays armazenam listas de valores. Cada item tem um índice que começa em `0`.\n\n"
            "## Como funciona\n\n"
            "```javascript\n"
            'const frutas = ["maçã", "banana", "uva"];\n\n'
            'console.log(frutas[0]);      // maçã    — primeiro\n'
            'console.log(frutas[2]);      // uva     — terceiro\n'
            "console.log(frutas.length);  // 3       — tamanho\n"
            "```\n\n"
            "- Índices começam em `0` — o último elemento está em `array.length - 1`\n"
            "- Arrays podem misturar tipos: `[1, \"dois\", true]`\n\n"
            "## Iterando com for...of\n\n"
            "```javascript\n"
            'const cores = ["azul", "verde", "vermelho"];\n'
            "for (const cor of cores) {\n"
            "  console.log(cor);\n"
            "}\n"
            "```\n\n"
            "## No exercício\n\n"
            "Acesse os índices corretos do array `cores` e exiba seu `length`."
        ),
        "instruction_pt": (
            "Com o array `cores = [\"vermelho\", \"verde\", \"azul\", \"amarelo\"]`, exiba (uma por linha):\n\n"
            "- O elemento no índice `0` → `vermelho`\n"
            "- O elemento no índice `2` → `azul`\n"
            "- O tamanho do array → `4`"
        ),
        "instruction_en": "Display cores[0], cores[2], and cores.length.",
        "instruction_es": "Muestra cores[0], cores[2] y cores.length.",
        "starter_code": (
            'const cores = ["vermelho", "verde", "azul", "amarelo"];\n'
            "console.log(cores[___]);\n"
            "console.log(cores[___]);\n"
            "console.log(cores.length);\n"
        ),
        "hint": "Preencha com os índices 0 e 2 (índices começam em zero).",
        "hints": [
            "Preencha os dois `___` com `0` e `2` para acessar `vermelho` e `azul`.",
            "`cores.length` já está pronto — retorna `4` (o número de elementos).",
        ],
        "tests": [{"stdin": "", "expected_stdout": "vermelho\nazul\n4"}],
        "quiz": [
            {
                "question": "Qual o índice do primeiro elemento de um array em JS?",
                "options": ["1", "0", "-1", "Depende do array"],
                "correct": 1,
            },
            {
                "question": "Como acessar o último elemento de `arr` sem saber o tamanho?",
                "options": ["arr[-1]", "arr.last()", "arr[arr.length - 1]", "arr.end()"],
                "correct": 2,
            },
        ],
    },

    # ── L14 ─────────────────────────────────────────────────────────────────
    {
        "order": 14,
        "slug": "js-metodos-array",
        "title": "Métodos de Array",
        "chapter": "Capítulo 3: Funções e Dados",
        "theory": (
            "Arrays têm métodos poderosos que facilitam manipular listas sem escrever loops manualmente.\n\n"
            "## Como funciona\n\n"
            "```javascript\n"
            'const lista = ["Ana", "Carlos"];\n\n'
            'lista.push("Beatriz");       // adiciona no final\n'
            "lista.pop();                 // remove o último\n"
            'lista.includes("Ana");       // true — verifica presença\n'
            "console.log(lista.length);   // 2\n"
            "```\n\n"
            "- `push(valor)` — adiciona ao final, aumenta `length`\n"
            "- `pop()` — remove e retorna o último elemento\n"
            "- `includes(valor)` — retorna `true` ou `false`\n\n"
            "## Mais métodos úteis\n\n"
            "```javascript\n"
            'const nums = [3, 1, 4, 1, 5];\n'
            "console.log(nums.indexOf(4));    // 2 — posição do elemento\n"
            'console.log(nums.join("-"));     // 3-1-4-1-5 — une em string\n'
            "console.log(nums.reverse());     // [5, 1, 4, 1, 3]\n"
            "```\n\n"
            "## No exercício\n\n"
            "Use `push()`, `length` e `includes()` numa lista de convidados."
        ),
        "instruction_pt": (
            "Com `convidados = [\"Ana\", \"Carlos\", \"Beatriz\"]`, faça (na ordem):\n\n"
            "1. Adicione `\"Diego\"` com `push()`\n"
            "2. Exiba o `length` → `4`\n"
            "3. Exiba se `\"Carlos\"` está na lista → `true`\n"
            "4. Exiba se `\"Pedro\"` está na lista → `false`"
        ),
        "instruction_en": "Push Diego to the array, then display length, includes Carlos, includes Pedro.",
        "instruction_es": "Agrega Diego con push, luego muestra length, includes Carlos, includes Pedro.",
        "starter_code": (
            'const convidados = ["Ana", "Carlos", "Beatriz"];\n'
            'convidados.push("Diego");\n'
            "console.log(convidados.length);\n"
            'console.log(convidados.includes("Carlos"));\n'
            'console.log(convidados.includes("Pedro"));\n'
        ),
        "hint": "O código já está quase completo — execute e observe o resultado.",
        "hints": [
            "O código já está correto — execute e observe: `push` adiciona Diego, `length` vira 4.",
            '`includes("Carlos")` retorna `true`; `includes("Pedro")` retorna `false` — Pedro não está na lista.',
        ],
        "tests": [{"stdin": "", "expected_stdout": "4\ntrue\nfalse"}],
        "quiz": [
            {
                "question": "O que `push()` faz em um array?",
                "options": ["Remove o primeiro elemento", "Remove o último elemento", "Adiciona um elemento ao final", "Inverte o array"],
                "correct": 2,
            },
            {
                "question": "O que `includes()` retorna?",
                "options": ["O índice do elemento", "true ou false", "O elemento encontrado", "O tamanho do array"],
                "correct": 1,
            },
        ],
    },

    # ── L15 ─────────────────────────────────────────────────────────────────
    {
        "order": 15,
        "slug": "js-objetos",
        "title": "Objetos",
        "chapter": "Capítulo 3: Funções e Dados",
        "theory": (
            "Objetos armazenam pares **chave: valor** — como uma ficha de cadastro onde cada campo tem um nome.\n\n"
            "## Como funciona\n\n"
            "```javascript\n"
            "const aluno = {\n"
            '  nome: "Beatriz",\n'
            "  idade: 14,\n"
            '  cidade: "Recife",\n'
            "};\n\n"
            'console.log(aluno.nome);    // Beatriz\n'
            "console.log(aluno.idade);   // 14\n"
            "```\n\n"
            "- Acesse propriedades com ponto `.` (notação de ponto)\n"
            "- Ou com colchetes: `aluno[\"nome\"]` (útil com chaves dinâmicas)\n\n"
            "## Adicionando e atualizando\n\n"
            "```javascript\n"
            'aluno.nota = 9.5;         // adiciona nova propriedade\n'
            'aluno.cidade = "SP";      // atualiza valor existente\n'
            "```\n\n"
            "## No exercício\n\n"
            "Acesse as propriedades corretas do objeto `produto` para exibir nome e preço."
        ),
        "instruction_pt": (
            "Com o objeto `produto` já declarado, complete os `___` para exibir:\n\n"
            "- `produto.___` → `Teclado`\n"
            "- `produto.___` → `150`"
        ),
        "instruction_en": "Access produto.nome and produto.preco to display Teclado and 150.",
        "instruction_es": "Accede a produto.nome y produto.preco para mostrar Teclado y 150.",
        "starter_code": (
            "const produto = {\n"
            '  nome: "Teclado",\n'
            "  preco: 150,\n"
            "  disponivel: true,\n"
            "};\n"
            "console.log(produto.___);\n"
            "console.log(produto.___);\n"
        ),
        "hint": "Preencha com as chaves do objeto: nome e preco.",
        "hints": [
            'Preencha os `___` com `nome` e `preco` — as chaves do objeto.',
            '`produto.nome` retorna `"Teclado"` e `produto.preco` retorna `150`.',
        ],
        "tests": [{"stdin": "", "expected_stdout": "Teclado\n150"}],
        "quiz": [
            {
                "question": "Como acessar a propriedade `nome` de um objeto `pessoa`?",
                "options": ["pessoa[nome]", "pessoa->nome", "pessoa.nome", "pessoa::nome"],
                "correct": 2,
            },
            {
                "question": "Qual é o resultado de `typeof {}` em JavaScript?",
                "options": ["\"dict\"", "\"array\"", "\"object\"", "\"undefined\""],
                "correct": 2,
            },
        ],
    },

    # ── L16 ─────────────────────────────────────────────────────────────────
    {
        "order": 16,
        "slug": "js-arrow-functions",
        "title": "Arrow Functions",
        "chapter": "Capítulo 4: JS Moderno",
        "theory": (
            "Arrow functions são uma sintaxe mais curta para escrever funções — "
            "use `=>` (seta) no lugar de `function`.\n\n"
            "## Como funciona\n\n"
            "```javascript\n"
            "// Função tradicional\n"
            "function dobrar(n) {\n"
            "  return n * 2;\n"
            "}\n\n"
            "// Arrow function equivalente\n"
            "const dobrar = n => n * 2;\n\n"
            "console.log(dobrar(5));  // 10\n"
            "```\n\n"
            "- Com **um** parâmetro: não precisam de `()`\n"
            "- Com **expressão única**: não precisam de `{}` nem `return`\n\n"
            "## Diferentes formas\n\n"
            "```javascript\n"
            "const somar = (a, b) => a + b;           // dois parâmetros\n"
            "const oi = () => 'Olá!';                  // sem parâmetros\n"
            "const grande = n => {                     // bloco com return\n"
            "  const msg = `Número: ${n}`;\n"
            "  return msg;\n"
            "};\n"
            "```\n\n"
            "## No exercício\n\n"
            "Complete as duas arrow functions com a expressão de retorno correta."
        ),
        "instruction_pt": (
            "Complete as duas arrow functions:\n\n"
            "- `quadrado` recebe `n` e retorna `n * n` → `quadrado(4)` = `16`\n"
            "- `bemVindo` recebe `nome` e retorna `` `Bem-vindo, ${nome}!` `` → `bemVindo(\"Ana\")` = `Bem-vindo, Ana!`"
        ),
        "instruction_en": "Complete: quadrado returns n*n, bemVindo returns a welcome template literal.",
        "instruction_es": "Completa: quadrado retorna n*n, bemVindo retorna un template literal de bienvenida.",
        "starter_code": (
            "const quadrado = n => ___;\n"
            "const bemVindo = nome => `Bem-vindo, ${nome}!`;\n"
            "console.log(quadrado(4));\n"
            'console.log(bemVindo("Ana"));\n'
        ),
        "hint": "quadrado: n => n * n",
        "hints": [
            "Para `quadrado`, complete com `n * n` — a arrow function retorna automaticamente expressões únicas.",
            '`bemVindo` já está completa — execute e observe `Bem-vindo, Ana!`.',
        ],
        "tests": [{"stdin": "", "expected_stdout": "16\nBem-vindo, Ana!"}],
        "quiz": [
            {
                "question": "Qual é a arrow function equivalente a `function dobrar(n) { return n*2; }`?",
                "options": ["n -> n*2", "n => n*2", "(n) >> n*2", "fn n => n*2"],
                "correct": 1,
            },
            {
                "question": "Quando uma arrow function precisa de `{}` e `return`?",
                "options": ["Sempre", "Nunca", "Quando tem mais de uma instrução no corpo", "Quando tem mais de dois parâmetros"],
                "correct": 2,
            },
        ],
    },

    # ── L17 ─────────────────────────────────────────────────────────────────
    {
        "order": 17,
        "slug": "js-map-filter",
        "title": "Map e Filter",
        "chapter": "Capítulo 4: JS Moderno",
        "theory": (
            "`.map()` e `.filter()` são os dois métodos mais usados para trabalhar com arrays em JS moderno "
            "— eles substituem loops manuais com código mais limpo.\n\n"
            "## Como funciona\n\n"
            "```javascript\n"
            "const nums = [1, 2, 3, 4, 5];\n\n"
            "// map: transforma cada elemento\n"
            "const dobrados = nums.map(n => n * 2);\n"
            "// [2, 4, 6, 8, 10]\n\n"
            "// filter: seleciona elementos que passam no teste\n"
            "const pares = nums.filter(n => n % 2 === 0);\n"
            "// [2, 4]\n"
            "```\n\n"
            "- `map()` sempre retorna um array de **mesmo tamanho**\n"
            "- `filter()` retorna um array com **zero ou mais** elementos\n\n"
            "## Encadeando\n\n"
            "```javascript\n"
            "const resultado = nums\n"
            "  .filter(n => n > 2)       // [3, 4, 5]\n"
            "  .map(n => n * 10);        // [30, 40, 50]\n"
            "```\n\n"
            "## No exercício\n\n"
            "Use `map()` para triplicar e `filter()` para selecionar ímpares."
        ),
        "instruction_pt": (
            "Com `numeros = [1, 2, 3, 4, 5, 6]`:\n\n"
            "1. Crie `triplos` com `map()` multiplicando por 3 → `3,6,9,12,15,18`\n"
            "2. Crie `impares` com `filter()` selecionando os ímpares → `1,3,5`\n"
            "3. Exiba com `.join(\",\")`"
        ),
        "instruction_en": "Use map() to triple and filter() to select odd numbers, display with join.",
        "instruction_es": "Usa map() para triplicar y filter() para seleccionar impares, muestra con join.",
        "starter_code": (
            "const numeros = [1, 2, 3, 4, 5, 6];\n"
            "const triplos = numeros.map(n => ___);\n"
            "const impares = numeros.filter(n => ___);\n"
            'console.log(triplos.join(","));\n'
            'console.log(impares.join(","));\n'
        ),
        "hint": "triplos: n => n * 3 | impares: n => n % 2 !== 0",
        "hints": [
            "Para `triplos`: `n => n * 3` — multiplica cada elemento por 3.",
            "Para `impares`: `n => n % 2 !== 0` — seleciona números que não são divisíveis por 2.",
        ],
        "tests": [{"stdin": "", "expected_stdout": "3,6,9,12,15,18\n1,3,5"}],
        "quiz": [
            {
                "question": "Qual a diferença entre map() e filter()?",
                "options": ["São idênticos", "map() transforma elementos; filter() seleciona elementos", "filter() transforma; map() seleciona", "Ambos removem elementos"],
                "correct": 1,
            },
            {
                "question": "Quantos elementos `[1,2,3].map(n => n+1)` retorna?",
                "options": ["Depende", "2", "3", "6"],
                "correct": 2,
            },
        ],
    },

    # ── L18 ─────────────────────────────────────────────────────────────────
    {
        "order": 18,
        "slug": "js-destructuring",
        "title": "Destructuring",
        "chapter": "Capítulo 4: JS Moderno",
        "theory": (
            "Destructuring extrai valores de objetos e arrays em variáveis com uma sintaxe limpa e direta.\n\n"
            "## Como funciona — Objetos\n\n"
            "```javascript\n"
            'const pessoa = { nome: "Ana", cidade: "SP", idade: 20 };\n\n'
            "// Sem destructuring (verboso)\n"
            "const nome = pessoa.nome;\n"
            "const cidade = pessoa.cidade;\n\n"
            "// Com destructuring (limpo)\n"
            "const { nome, cidade } = pessoa;\n\n"
            'console.log(nome);    // Ana\n'
            'console.log(cidade);  // SP\n'
            "```\n\n"
            "## Destructuring de Arrays\n\n"
            "```javascript\n"
            "const coords = [10, 20, 30];\n"
            "const [x, y, z] = coords;\n"
            "console.log(x);  // 10\n"
            "console.log(y);  // 20\n"
            "```\n\n"
            "## No exercício\n\n"
            "Use destructuring para extrair `marca` e `ano` do objeto `carro`."
        ),
        "instruction_pt": (
            "Use destructuring para extrair `marca` e `ano` do objeto `carro` e exibir:\n\n"
            "- `Toyota`\n"
            "- `2023`"
        ),
        "instruction_en": "Use destructuring to extract marca and ano from carro, display Toyota and 2023.",
        "instruction_es": "Usa destructuring para extraer marca y ano de carro, muestra Toyota y 2023.",
        "starter_code": (
            'const carro = { marca: "Toyota", modelo: "Corolla", ano: 2023 };\n'
            "const { ___, ___ } = carro;\n"
            "console.log(marca);\n"
            "console.log(ano);\n"
        ),
        "hint": "Preencha com: marca, ano (as chaves do objeto que você quer extrair).",
        "hints": [
            "Preencha os `___` com `marca` e `ano` — os nomes devem bater com as chaves do objeto.",
            'Resultado: `{ marca, ano } = carro` cria as variáveis `marca = "Toyota"` e `ano = 2023`.',
        ],
        "tests": [{"stdin": "", "expected_stdout": "Toyota\n2023"}],
        "quiz": [
            {
                "question": "O que `const { nome } = pessoa` faz?",
                "options": ["Cria um novo objeto", "Extrai a propriedade nome de pessoa para uma variável", "Remove nome de pessoa", "Verifica se pessoa tem nome"],
                "correct": 1,
            },
            {
                "question": "Como usar destructuring para extrair o segundo elemento de um array `arr`?",
                "options": ["const [, segundo] = arr", "const {1: segundo} = arr", "const segundo = arr.get(1)", "const [segundo] = arr.slice(1)"],
                "correct": 0,
            },
        ],
    },

    # ── L19 ─────────────────────────────────────────────────────────────────
    {
        "order": 19,
        "slug": "js-projeto",
        "title": "Projeto Final",
        "chapter": "Capítulo 4: JS Moderno",
        "theory": (
            "Hora de juntar tudo que você aprendeu: variáveis, arrays, objetos, filter, map e template literals "
            "num mini-programa real!\n\n"
            "## O que vamos construir\n\n"
            "Um sistema simples de estoque que filtra produtos caros e lista seus nomes.\n\n"
            "## Revisando os conceitos usados\n\n"
            "```javascript\n"
            "// Objetos dentro de arrays\n"
            "const produtos = [\n"
            '  { nome: "A", preco: 10 },\n'
            '  { nome: "B", preco: 50 },\n'
            "];\n\n"
            "// filter: seleciona por condição\n"
            "const caros = produtos.filter(p => p.preco > 30);\n"
            "// [{ nome: 'B', preco: 50 }]\n\n"
            "// forEach: itera sem transformar\n"
            "caros.forEach(p => console.log(p.nome));\n"
            "// B\n"
            "```\n\n"
            "## No exercício\n\n"
            "Complete os dois `___` para filtrar produtos acima de R$ 50 e exibir seus nomes."
        ),
        "instruction_pt": (
            "Complete o programa para:\n\n"
            "1. Filtrar produtos com `preco > 50` → Mochila e Calculadora\n"
            "2. Exibir `Produtos caros: 2`\n"
            "3. Exibir o nome de cada produto caro (um por linha)"
        ),
        "instruction_en": "Filter products with price > 50, display count and each name.",
        "instruction_es": "Filtra productos con precio > 50, muestra la cantidad y cada nombre.",
        "starter_code": (
            "const produtos = [\n"
            '  { nome: "Caderno",     preco: 15  },\n'
            '  { nome: "Mochila",     preco: 120 },\n'
            '  { nome: "Caneta",      preco: 5   },\n'
            '  { nome: "Calculadora", preco: 85  },\n'
            "];\n\n"
            "// 1. Filtre produtos com preco > 50\n"
            "const caros = produtos.filter(p => p.preco > ___);\n\n"
            "// 2. Exiba o total de produtos caros\n"
            "console.log(`Produtos caros: ${caros.length}`);\n\n"
            "// 3. Exiba o nome de cada produto caro\n"
            "caros.forEach(p => console.log(p.___));\n"
        ),
        "hint": "Preencha: > 50 no filter e .nome no forEach.",
        "hints": [
            "Troque o primeiro `___` por `50` — o filtro selecionará Mochila (120) e Calculadora (85).",
            "No `forEach`, acesse `p.nome` para exibir apenas o nome de cada produto.",
        ],
        "tests": [{"stdin": "", "expected_stdout": "Produtos caros: 2\nMochila\nCalculadora"}],
        "quiz": [
            {
                "question": "Qual método percorre um array executando uma função para cada elemento sem retornar um novo array?",
                "options": ["map()", "filter()", "forEach()", "reduce()"],
                "correct": 2,
            },
            {
                "question": "Como acessar a propriedade `preco` de um objeto `p` dentro de um callback?",
                "options": ["p[preco]", "p->preco", "p.preco", "preco(p)"],
                "correct": 2,
            },
            {
                "question": "Você terminou a trilha de JavaScript! O que vem a seguir no CodeFuturo?",
                "options": ["Nada, JS é o fim", "HTML & CSS — a base visual da web", "Direto para React", "Banco de dados"],
                "correct": 1,
            },
        ],
    },
]

# ---------------------------------------------------------------------------
# Substituir a secao no seed
# ---------------------------------------------------------------------------

lessons_str = ""
for les in LESSONS:
    lessons_str += fmt_lesson(les) + ",\n"

HEADER = "# ── JavaScript " + "─" * 60 + "\n"
new_block = HEADER + '"javascript": [\n' + lessons_str + '],\n'

with open("seed_static.py", encoding="utf-8") as f:
    src = f.read()

js_start = src.index("# ── JavaScript")
html_start = src.index("# ── HTML")

new_src = src[:js_start] + new_block + "\n" + src[html_start:]

with open("seed_static.py", "w", encoding="utf-8") as f:
    f.write(new_src)

print(f"Done! {len(LESSONS)} licoes escritas.")
print(f"Arquivo: {len(new_src)} chars (era {len(src)})")
