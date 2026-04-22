"""AI-powered lesson generator for CodeFuturo.

Generates a complete learning path for a programming language using GPT,
with chapters, lessons, starter code, hints and test cases.

Usage:
    python -m backend.seed_lessons           # generate all languages
    python -m backend.seed_lessons python    # generate just one

Idempotent: uses upsert by (path_slug, order).
"""
import asyncio
import json
import os
import re
import sys
import uuid
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from emergentintegrations.llm.chat import LlmChat, UserMessage

ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")

MONGO_URL = os.environ["MONGO_URL"]
DB_NAME = os.environ.get("DB_NAME", "test_database")
EMERGENT_KEY = os.environ["EMERGENT_LLM_KEY"]

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]


PATHS = [
    # id, name, lang-code, total_lessons, level progression, has_pyodide, icon_color
    {"slug": "python-zero", "name": "Python",          "language": "python",     "count": 12, "color": "#3776AB", "real_exec": True,  "desc": "A linguagem mais popular para iniciantes. Base sólida para IA, web, dados e automação."},
    {"slug": "javascript",   "name": "JavaScript",      "language": "javascript", "count": 10, "color": "#F7DF1E", "real_exec": True,  "desc": "A linguagem da web. Interatividade, frameworks modernos e Node.js."},
    {"slug": "html-css",     "name": "HTML & CSS",      "language": "html",       "count": 10, "color": "#E34F26", "real_exec": False, "desc": "A base da web. Aprenda a estruturar páginas e criar layouts modernos."},
    {"slug": "sql",          "name": "SQL",             "language": "sql",        "count": 8,  "color": "#CC2927", "real_exec": False, "desc": "Linguagem para consultar e manipular bancos de dados relacionais."},
    {"slug": "typescript",   "name": "TypeScript",      "language": "typescript", "count": 8,  "color": "#3178C6", "real_exec": False, "desc": "JavaScript com tipos. Essencial para projetos profissionais em escala."},
    {"slug": "java",         "name": "Java",            "language": "java",       "count": 8,  "color": "#EA2D2E", "real_exec": False, "desc": "Orientação a objetos robusta. Usada em Android, empresas e backend."},
    {"slug": "cpp",          "name": "C++",             "language": "cpp",        "count": 8,  "color": "#00599C", "real_exec": False, "desc": "Performance e controle total. Base de jogos, sistemas e engenharia."},
    {"slug": "go",           "name": "Go",              "language": "go",         "count": 6,  "color": "#00ADD8", "real_exec": False, "desc": "Linguagem simples e poderosa do Google. Ideal para backend e DevOps."},
    {"slug": "ai-prompts",   "name": "AI Prompts",      "language": "prompts",    "count": 6,  "color": "#A3E635", "real_exec": False, "desc": "Aprenda a conversar com IA. Engenharia de prompts para GPT, Claude e Gemini."},
]


SYSTEM_PROMPT = """Você é um designer pedagógico sênior que cria trilhas de programação gamificadas ao estilo Coddy.tech / Duolingo.

Gere JSON estrito (array) com lições curtas, interativas e progressivas.

Cada lição é um objeto com exatamente estes campos:
{
  "title": "Título curto em português",
  "chapter": "Capítulo N: Nome do Capítulo",
  "order": número_sequencial_começando_em_1,
  "instruction_pt": "Instrução clara em português com o que fazer (2-5 frases, use crases em trechos de código)",
  "instruction_en": "Same instruction in English",
  "instruction_es": "Misma instrucción en español",
  "starter_code": "código inicial com comentários e lacunas para o aluno completar",
  "hint": "Dica útil em português sem dar a resposta pronta",
  "tests": [
    {"stdin": "", "expected_stdout": "saída exata esperada"}
  ]
}

REGRAS CRÍTICAS:
- Para linguagens que NÃO executamos (HTML, CSS, SQL, TypeScript, Java, C++, Go, prompts): o campo `tests[0].expected_stdout` deve conter o conteúdo EXATO que o aluno deve escrever/imprimir/retornar (não saída real de execução, é validação textual).
- Para Python e JavaScript (execução real): `expected_stdout` é a saída real após executar o código correto, exatamente como apareceria no terminal.
- Progrida do básico (Olá Mundo, variáveis) ao intermediário (funções, arrays/listas, loops) ao avançado/projeto.
- Capítulos: 3-4 capítulos por trilha, distribuídos equilibradamente.
- NUNCA use markdown fora do JSON. Retorne APENAS o array JSON.
- Starter code deve ser curto (3-15 linhas), com comentários PT e `# escreva aqui` ou `// escreva aqui` indicando o que completar.
- Test cases: 1 a 3 por lição, validação por igualdade de strings (trim).
- Exatidão > criatividade: expected_stdout deve ser deterministicamente alcançável com o starter + solução óbvia.
"""


def extract_json(text: str):
    # Strip markdown fences if present
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if fence:
        text = fence.group(1)
    # Find first [ and last ]
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("No JSON array found in response")
    return json.loads(text[start:end + 1])


async def generate_path(path_cfg: dict):
    print(f"→ Generating {path_cfg['name']} ({path_cfg['count']} lessons)...")
    user_prompt = f"""Crie uma trilha completa de {path_cfg['count']} lições para a linguagem **{path_cfg['name']}** ({path_cfg['language']}).

Nível: do zero absoluto até intermediário, organizadas em capítulos lógicos.
Público-alvo: pessoas de qualquer idade (adolescentes até adultos profissionais) que querem aprender {path_cfg['name']} do zero.

Contexto da linguagem: {path_cfg['desc']}

Retorne exatamente {path_cfg['count']} lições no formato JSON array descrito no sistema. Numere order de 1 a {path_cfg['count']}.
"""
    chat = LlmChat(
        api_key=EMERGENT_KEY,
        session_id=f"seed-{path_cfg['slug']}-{datetime.utcnow().timestamp()}",
        system_message=SYSTEM_PROMPT,
    ).with_model("openai", "gpt-5.1")

    response = await chat.send_message(UserMessage(text=user_prompt))
    lessons = extract_json(response)
    if not isinstance(lessons, list) or not lessons:
        raise ValueError(f"Invalid lessons response for {path_cfg['slug']}")

    # Upsert path metadata
    await db.paths.update_one(
        {"slug": path_cfg["slug"]},
        {"$set": {
            "slug": path_cfg["slug"],
            "name": path_cfg["name"],
            "language": path_cfg["language"],
            "color": path_cfg["color"],
            "desc": path_cfg["desc"],
            "real_exec": path_cfg["real_exec"],
            "total_lessons": len(lessons),
            "updated_at": datetime.utcnow().isoformat(),
        }},
        upsert=True,
    )

    # Upsert lessons
    for i, les in enumerate(lessons):
        order = int(les.get("order") or (i + 1))
        slug_base = re.sub(r"[^a-z0-9]+", "-", les["title"].lower()).strip("-")[:40]
        lesson_slug = f"{path_cfg['slug']}-{order:02d}-{slug_base}"
        doc = {
            "id": str(uuid.uuid4()),
            "slug": lesson_slug,
            "path_slug": path_cfg["slug"],
            "order": order,
            "title": les["title"],
            "chapter": les.get("chapter", "Capítulo 1"),
            "instruction_pt": les.get("instruction_pt") or les.get("instruction", ""),
            "instruction_en": les.get("instruction_en", ""),
            "instruction_es": les.get("instruction_es", ""),
            "starter_code": les.get("starter_code", ""),
            "hint": les.get("hint", ""),
            "tests": les.get("tests", []),
            "language": path_cfg["language"],
            "real_exec": path_cfg["real_exec"],
            "updated_at": datetime.utcnow().isoformat(),
        }
        await db.lessons.update_one(
            {"path_slug": path_cfg["slug"], "order": order},
            {"$set": doc},
            upsert=True,
        )
    print(f"✓ {path_cfg['name']}: {len(lessons)} lessons saved")


async def main(slugs=None):
    await db.paths.create_index("slug", unique=True)
    await db.lessons.create_index([("path_slug", 1), ("order", 1)], unique=True)
    await db.lessons.create_index("slug", unique=True)

    targets = PATHS if not slugs else [p for p in PATHS if p["slug"] in slugs]
    for p in targets:
        try:
            await generate_path(p)
        except Exception as e:
            print(f"✗ {p['slug']}: {e}")
    print("Done.")


if __name__ == "__main__":
    args = sys.argv[1:]
    asyncio.run(main(args or None))
