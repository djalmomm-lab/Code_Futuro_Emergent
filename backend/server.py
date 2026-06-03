"""CodeFuturo backend - FastAPI + MongoDB.

Single-file for MVP - easy to split later.
"""
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import Optional, Literal
import os
import uuid
import logging

from fastapi import FastAPI, APIRouter, HTTPException, Depends, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
from jose import jwt, JWTError
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

# --- Config ---
MONGO_URL = os.environ["MONGO_URL"]
DB_NAME = os.environ.get("DB_NAME", "codefuturo")
JWT_SECRET = os.environ.get("JWT_SECRET", "cf-dev-secret-change-me")
JWT_ALGO = "HS256"
JWT_EXPIRE_DAYS = 7
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)

app = FastAPI(title="CodeFuturo API")
api = APIRouter(prefix="/api")

_cors_origins = [
    FRONTEND_URL,
    "https://codefuturo.com",
    "https://www.codefuturo.com",
    "http://localhost:3000",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=_cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Models ---
class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    name: str = Field(min_length=2, max_length=80)


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class OnboardIn(BaseModel):
    birth_date: str  # YYYY-MM-DD
    parent_name: Optional[str] = None
    parent_email: Optional[EmailStr] = None
    consent_data: Optional[bool] = None
    consent_comm: Optional[bool] = None
    interest: str
    diagnostic_score: int = 0
    recommendation: dict


class CompleteLessonIn(BaseModel):
    lesson_slug: str
    path_slug: str = "python-zero"


# --- Helpers ---
def new_id() -> str:
    return str(uuid.uuid4())


def hash_password(pw: str) -> str:
    return pwd_ctx.hash(pw)


def verify_password(pw: str, hashed: str) -> bool:
    return pwd_ctx.verify(pw, hashed)


def make_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(days=JWT_EXPIRE_DAYS),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)


async def current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing token")
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGO])
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")
    user = await db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found")
    return user


async def optional_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Like current_user but returns None instead of raising for unauthenticated."""
    if not credentials:
        return None
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGO])
        user_id = payload.get("sub")
    except JWTError:
        return None
    return await db.users.find_one({"id": user_id})


# Paywall config: Capítulo 1 de cada trilha é gratuito
# Uma lição é gratuita se seu campo "chapter" começa com "Capítulo 1"
FREE_LESSONS_PER_PATH = 3  # fallback para trilhas sem chapter definido

def is_free_lesson(lesson: dict) -> bool:
    """Retorna True se a lição é gratuita (Capítulo 1 ou order <= FREE_LESSONS_PER_PATH)."""
    chapter = lesson.get("chapter", "")
    if chapter:
        return chapter.strip().startswith("Capítulo 1") or chapter.strip().startswith("Chapter 1")
    return lesson.get("order", 0) <= FREE_LESSONS_PER_PATH


def calc_age(birth_date: str) -> int:
    bd = datetime.strptime(birth_date, "%Y-%m-%d").date()
    today = date.today()
    age = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
    return age


def public_user(u: dict) -> dict:
    return {
        "id": u["id"],
        "email": u["email"],
        "name": u["name"],
        "is_pro": bool(u.get("is_pro", False)),
        "tier": u.get("tier"),
        "plan": u.get("plan"),
        "subscription_ends_at": u.get("subscription_ends_at"),
    }


async def ensure_progress(user_id: str) -> dict:
    prog = await db.progress.find_one({"user_id": user_id})
    if not prog:
        prog = {
            "id": new_id(),
            "user_id": user_id,
            "xp_total": 0,
            "xp_today": 0,
            "daily_goal": 200,
            "level": 1,
            "streak": 0,
            "last_streak_date": None,
            "energy": 5,
            "max_energy": 5,
            "last_energy_reset": datetime.utcnow().isoformat(),
            "tokens": 10,
            "updated_at": datetime.utcnow().isoformat(),
        }
        await db.progress.insert_one(prog)
        return prog

    # ── Sincronizar max_energy com status Pro (Pro = 10, free = 5) ──────────
    changed = {}
    user_doc = await db.users.find_one({"id": user_id}, {"is_pro": 1, "_id": 0})
    is_pro = bool(user_doc and user_doc.get("is_pro"))
    correct_max = 10 if is_pro else 5
    if prog.get("max_energy", 5) != correct_max:
        prog["max_energy"] = correct_max
        # Se energia atual excede o novo max, ajusta
        if prog.get("energy", 5) > correct_max:
            prog["energy"] = correct_max
        changed["max_energy"] = correct_max
        changed["energy"] = prog.get("energy", correct_max)

    # ── Recarga gradual de energia: +1 por hora completa desde o último uso ──
    max_e = prog.get("max_energy", correct_max)
    cur_e = prog.get("energy", max_e)
    try:
        last_reset = datetime.fromisoformat(prog.get("last_energy_reset") or "")
    except Exception:
        last_reset = datetime.utcnow() - timedelta(hours=max_e)

    if cur_e < max_e:
        elapsed_hours = int((datetime.utcnow() - last_reset).total_seconds() / 3600)
        if elapsed_hours > 0:
            refill = min(elapsed_hours, max_e - cur_e)
            prog["energy"] = min(max_e, cur_e + refill)
            prog["last_energy_reset"] = (last_reset + timedelta(hours=refill)).isoformat()
            changed["energy"] = prog["energy"]
            changed["last_energy_reset"] = prog["last_energy_reset"]

    # ── Zera xp_today se mudou o dia ────────────────────────────────────────
    today = date.today().isoformat()
    if prog.get("last_streak_date") and prog.get("last_streak_date") != today and prog.get("xp_today", 0) > 0:
        prog["xp_today"] = 0
        changed["xp_today"] = 0

    if changed:
        await db.progress.update_one({"user_id": user_id}, {"$set": changed})

    return prog


def serialize(doc: dict) -> dict:
    if not doc:
        return doc
    d = dict(doc)
    d.pop("_id", None)
    d.pop("password_hash", None)
    return d


# --- Routes ---
@api.get("/")
async def root():
    return {"name": "CodeFuturo API", "status": "ok"}


@api.post("/auth/register")
async def register(data: RegisterIn):
    existing = await db.users.find_one({"email": data.email.lower()})
    if existing:
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")
    user = {
        "id": new_id(),
        "email": data.email.lower(),
        "password_hash": hash_password(data.password),
        "name": data.name,
        "created_at": datetime.utcnow().isoformat(),
    }
    await db.users.insert_one(user)
    await ensure_progress(user["id"])
    token = make_token(user["id"])
    return {"token": token, "user": public_user(user)}


@api.post("/auth/login")
async def login(data: LoginIn):
    user = await db.users.find_one({"email": data.email.lower()})
    if not user or not user.get("password_hash"):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    if not verify_password(data.password, user["password_hash"]):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    token = make_token(user["id"])
    return {"token": token, "user": public_user(user)}


class GoogleLoginIn(BaseModel):
    credential: str


@api.post("/auth/google")
async def google_login(data: GoogleLoginIn):
    import requests as _req
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")

    resp = _req.get(
        "https://oauth2.googleapis.com/tokeninfo",
        params={"id_token": data.credential},
        timeout=5,
    )
    if resp.status_code != 200:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token Google inválido")

    info = resp.json()
    if GOOGLE_CLIENT_ID and info.get("aud") != GOOGLE_CLIENT_ID:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token não pertence a este app")

    email = info.get("email", "").lower()
    name = info.get("name") or info.get("given_name") or "Usuário Google"
    google_id = info.get("sub", "")

    if not email:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Google não forneceu e-mail")

    user = await db.users.find_one({"email": email})
    if not user:
        user = {
            "id": new_id(),
            "email": email,
            "password_hash": None,
            "name": name,
            "google_id": google_id,
            "created_at": datetime.utcnow().isoformat(),
        }
        await db.users.insert_one(user)
        await ensure_progress(user["id"])
    elif not user.get("google_id"):
        await db.users.update_one({"id": user["id"]}, {"$set": {"google_id": google_id}})

    token = make_token(user["id"])
    return {"token": token, "user": public_user(user)}


@api.get("/auth/me")
async def me(user=Depends(current_user)):
    profile = await db.profiles.find_one({"user_id": user["id"]})
    progress = await ensure_progress(user["id"])
    return {
        "user": public_user(user),
        "profile": serialize(profile),
        "progress": serialize(progress),
    }


@api.post("/onboard")
async def onboard(data: OnboardIn, request: Request, user=Depends(current_user)):
    age = calc_age(data.birth_date)
    needs_parent = age < 13
    if needs_parent:
        if not data.parent_name or not data.parent_email or not data.consent_data:
            raise HTTPException(422, "Parent consent required for users under 13")

    profile_doc = {
        "id": new_id(),
        "user_id": user["id"],
        "birth_date": data.birth_date,
        "age": age,
        "parent_name": data.parent_name,
        "parent_email": data.parent_email,
        "consent_data": data.consent_data,
        "consent_comm": data.consent_comm,
        "consent_ip": request.client.host if request.client else None,
        "consent_at": datetime.utcnow().isoformat() if needs_parent else None,
        "interest": data.interest,
        "diagnostic_score": data.diagnostic_score,
        "recommendation": data.recommendation,
        "onboarded_at": datetime.utcnow().isoformat(),
    }
    await db.profiles.update_one(
        {"user_id": user["id"]}, {"$set": profile_doc}, upsert=True
    )
    await ensure_progress(user["id"])
    return {"ok": True, "profile": serialize(profile_doc)}


@api.get("/progress")
async def get_progress(user=Depends(current_user)):
    prog = await ensure_progress(user["id"])
    return serialize(prog)


@api.post("/progress/complete")
async def complete_lesson(data: CompleteLessonIn, user=Depends(current_user)):
    # Paywall enforcement: block server-side even if client bypasses UI
    les = await db.lessons.find_one({"slug": data.lesson_slug}, {"_id": 0, "order": 1, "chapter": 1})
    if les and not is_free_lesson(les) and not user.get("is_pro"):
        raise HTTPException(
            status.HTTP_402_PAYMENT_REQUIRED,
            "Esta lição requer assinatura Pro",
        )

    # idempotent: if already completed, return current progress unchanged
    existing = await db.lesson_completions.find_one(
        {"user_id": user["id"], "lesson_slug": data.lesson_slug}
    )
    prog = await ensure_progress(user["id"])
    if existing:
        return {"already_completed": True, "progress": serialize(prog), "xp_earned": 0}

    xp = 50
    today = date.today().isoformat()
    new_streak = prog["streak"]
    if prog.get("last_streak_date") != today:
        if prog.get("last_streak_date") == (date.today() - timedelta(days=1)).isoformat():
            new_streak += 1
        else:
            new_streak = 1

    update = {
        "xp_total": prog["xp_total"] + xp,
        "xp_today": prog["xp_today"] + xp if prog.get("last_streak_date") == today else xp,
        "streak": new_streak,
        "last_streak_date": today,
        "level": 1 + (prog["xp_total"] + xp) // 500,
        "updated_at": datetime.utcnow().isoformat(),
    }
    await db.progress.update_one({"user_id": user["id"]}, {"$set": update})

    await db.lesson_completions.insert_one({
        "id": new_id(),
        "user_id": user["id"],
        "lesson_slug": data.lesson_slug,
        "path_slug": data.path_slug,
        "xp_earned": xp,
        "completed_at": datetime.utcnow().isoformat(),
    })

    # If this completion finishes the path AND user is Pro, upsert the certificate
    # record so it can be publicly verified at /verificar/<cert_id> even before download.
    if user.get("is_pro"):
        await _ensure_certificate_record(user, data.path_slug)

    prog.update(update)
    return {"already_completed": False, "progress": serialize(prog), "xp_earned": xp}


@api.post("/energy/consume")
async def consume_energy(user=Depends(current_user)):
    prog = await ensure_progress(user["id"])

    # Recarga gradual: +1 energia por hora completa desde o último uso
    try:
        last_reset = datetime.fromisoformat(prog.get("last_energy_reset"))
    except Exception:
        last_reset = datetime.utcnow() - timedelta(hours=prog["max_energy"])

    elapsed_hours = int((datetime.utcnow() - last_reset).total_seconds() / 3600)
    if elapsed_hours > 0 and prog["energy"] < prog["max_energy"]:
        refill = min(elapsed_hours, prog["max_energy"] - prog["energy"])
        prog["energy"] = min(prog["max_energy"], prog["energy"] + refill)
        # Avança o timestamp pelo número exato de horas recarregadas
        prog["last_energy_reset"] = (
            last_reset + timedelta(hours=refill)
        ).isoformat()

    if prog["energy"] <= 0:
        raise HTTPException(429, "No energy left. Upgrade to Pro or wait for reset.")

    prog["energy"] -= 1
    prog["updated_at"] = datetime.utcnow().isoformat()
    await db.progress.update_one({"user_id": user["id"]}, {"$set": prog}, upsert=True)
    return {"energy": prog["energy"], "max_energy": prog["max_energy"]}


@api.get("/leaderboard")
async def leaderboard(period: str = "week", limit: int = 20):
    cursor = db.progress.find().sort("xp_total", -1).limit(limit)
    rows = []
    async for p in cursor:
        user = await db.users.find_one({"id": p["user_id"]})
        if not user:
            continue
        rows.append({
            "user_id": p["user_id"],
            "name": user["name"],
            "xp": p["xp_total"],
            "streak": p["streak"],
            "level": p["level"],
        })
    return {"period": period, "rows": rows}


ADMIN_SECRET = os.environ.get("ADMIN_SECRET", "")


def _check_admin(request: Request):
    secret = request.headers.get("x-admin-secret", "")
    if not ADMIN_SECRET or secret != ADMIN_SECRET:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Acesso negado")


class AdminSetProIn(BaseModel):
    email: EmailStr
    is_pro: bool = True


@api.post("/admin/set-pro")
async def admin_set_pro(data: AdminSetProIn, request: Request):
    """Promove (ou rebaixa) um usuário para Pro/free. Requer x-admin-secret."""
    _check_admin(request)
    user = await db.users.find_one({"email": data.email.lower()})
    if not user:
        raise HTTPException(404, f"Usuário não encontrado: {data.email}")

    update = {
        "is_pro": data.is_pro,
        "tier": "pro" if data.is_pro else "free",
        "plan": "admin" if data.is_pro else None,
        "subscription_ends_at": None,  # sem vencimento para conta admin
    }
    await db.users.update_one({"email": data.email.lower()}, {"$set": update})
    return {
        "ok": True,
        "email": data.email.lower(),
        "is_pro": data.is_pro,
        "message": f"Usuário {'promovido a Pro' if data.is_pro else 'revertido para free'} com sucesso.",
    }


class AdminResetEnergyIn(BaseModel):
    email: EmailStr
    energy: int = Field(default=5, ge=0, le=10)


@api.post("/admin/reset-energy")
async def admin_reset_energy(data: AdminResetEnergyIn, request: Request):
    """Redefine a energia de um usuário. Requer x-admin-secret."""
    _check_admin(request)
    user = await db.users.find_one({"email": data.email.lower()})
    if not user:
        raise HTTPException(404, f"Usuário não encontrado: {data.email}")
    prog = await db.progress.find_one({"user_id": user["id"]})
    if not prog:
        raise HTTPException(404, "Progresso não encontrado")
    await db.progress.update_one(
        {"user_id": user["id"]},
        {"$set": {
            "energy": data.energy,
            "last_energy_reset": datetime.utcnow().isoformat(),
        }},
    )
    return {"ok": True, "email": data.email.lower(), "energy": data.energy}


@api.get("/admin/users")
async def admin_list_users(request: Request, limit: int = 50):
    """Lista usuários (email, nome, is_pro). Requer x-admin-secret."""
    _check_admin(request)
    cursor = db.users.find({}, {"_id": 0, "id": 1, "email": 1, "name": 1, "is_pro": 1, "plan": 1, "created_at": 1})
    users = await cursor.sort("created_at", -1).to_list(limit)
    return {"users": users, "total": len(users)}


@api.post("/admin/reseed")
async def admin_reseed(request: Request):
    """Re-executa o seed estático para atualizar lições e trilhas no MongoDB."""
    _check_admin(request)
    try:
        import sys, importlib
        sys.path.insert(0, str(ROOT_DIR))
        if "seed_static" in sys.modules:
            del sys.modules["seed_static"]
        import seed_static as _seed
        await _seed.main()
        return {"ok": True, "message": "Seed executado com sucesso"}
    except Exception as e:
        raise HTTPException(500, f"Erro no seed: {e}")


@api.post("/admin/update-lesson")
async def admin_update_lesson(request: Request):
    """Atualiza campos de uma lição diretamente no MongoDB via JSON."""
    _check_admin(request)
    body = await request.json()
    slug = body.get("slug")
    if not slug:
        raise HTTPException(400, "slug obrigatório")
    update_fields = {k: v for k, v in body.items() if k != "slug"}
    if not update_fields:
        raise HTTPException(400, "Nenhum campo para atualizar")
    result = await db.lessons.update_one({"slug": slug}, {"$set": update_fields})
    if result.matched_count == 0:
        raise HTTPException(404, f"Lição '{slug}' não encontrada")
    return {"ok": True, "slug": slug, "updated": list(update_fields.keys())}


@api.get("/tracks")
async def tracks():
    """List learning paths from DB (seeded by seed_lessons.py)."""
    cursor = db.paths.find({}, {"_id": 0})
    rows = await cursor.to_list(100)
    # Sort: highlight common beginners first
    order = ["python-zero", "javascript", "html-css", "sql", "typescript", "java", "cpp", "go", "ai-prompts"]
    rows.sort(key=lambda r: order.index(r["slug"]) if r["slug"] in order else 99)
    return {"paths": rows}


@api.get("/paths/{slug}")
async def path_detail(slug: str, user=Depends(optional_user)):
    path = await db.paths.find_one({"slug": slug}, {"_id": 0})
    if not path:
        raise HTTPException(404, "Path not found")
    lessons = await db.lessons.find({"path_slug": slug}, {"_id": 0}).sort("order", 1).to_list(200)
    is_pro = bool(user and user.get("is_pro"))

    # Build a set of completed lesson slugs for this user (empty for anonymous)
    completed_slugs: set = set()
    if user:
        completions = await db.lesson_completions.find(
            {"user_id": user["id"], "path_slug": slug},
            {"_id": 0, "lesson_slug": 1},
        ).to_list(500)
        completed_slugs = {c["lesson_slug"] for c in completions}

    # Mark paywall and completion status per lesson
    for le in lessons:
        le["requires_pro"] = not is_free_lesson(le) and not is_pro
        le["is_completed"] = le["slug"] in completed_slugs

    return {"path": path, "lessons": lessons, "free_limit": FREE_LESSONS_PER_PATH, "is_pro": is_pro}


@api.get("/lessons/{lesson_slug}")
async def lesson_detail(lesson_slug: str, user=Depends(optional_user)):
    les = await db.lessons.find_one({"slug": lesson_slug}, {"_id": 0})
    if not les:
        raise HTTPException(404, "Lesson not found")
    # Also return next and previous lessons for chaining
    nxt = await db.lessons.find_one(
        {"path_slug": les["path_slug"], "order": les["order"] + 1},
        {"_id": 0, "slug": 1, "title": 1},
    )
    les["next"] = nxt
    prev = await db.lessons.find_one(
        {"path_slug": les["path_slug"], "order": les["order"] - 1},
        {"_id": 0, "slug": 1, "title": 1},
    )
    les["previous"] = prev

    # Paywall: Capítulo 1 é gratuito; demais capítulos requerem Pro
    is_pro = bool(user and user.get("is_pro"))
    if not is_free_lesson(les) and not is_pro:
        # Return minimal metadata so UI can render the paywall with context
        return {
            "slug": les["slug"],
            "path_slug": les["path_slug"],
            "order": les["order"],
            "title": les["title"],
            "chapter": les.get("chapter"),
            "language": les.get("language"),
            "next": les.get("next"),
            "previous": les.get("previous"),
            "requires_pro": True,
            "free_limit": FREE_LESSONS_PER_PATH,
        }

    les["requires_pro"] = False
    return les


# --- LGPD: user data export & deletion ---
@api.get("/privacy/export")
async def export_data(user=Depends(current_user)):
    profile = await db.profiles.find_one({"user_id": user["id"]})
    progress = await db.progress.find_one({"user_id": user["id"]})
    completions = await db.lesson_completions.find({"user_id": user["id"]}).to_list(1000)
    return {
        "user": public_user(user),
        "profile": serialize(profile),
        "progress": serialize(progress),
        "completions": [serialize(c) for c in completions],
    }


@api.delete("/privacy/delete")
async def delete_account(user=Depends(current_user)):
    user_id = user["id"]
    await db.users.delete_one({"id": user_id})
    await db.profiles.delete_many({"user_id": user_id})
    await db.progress.delete_many({"user_id": user_id})
    await db.lesson_completions.delete_many({"user_id": user_id})
    return {"ok": True, "deleted_user_id": user_id}


# --- Certificates (Pro feature) ---
import asyncio  # noqa: E402
from fastapi.responses import Response  # noqa: E402
from certificates import render_certificate, cert_filename  # noqa: E402
import hashlib  # noqa: E402


async def _track_completion_status(user_id: str, path_slug: str) -> dict:
    """Return completion stats for a path/user pair."""
    path = await db.paths.find_one({"slug": path_slug}, {"_id": 0})
    if not path:
        raise HTTPException(404, "Path not found")
    lessons = await db.lessons.find({"path_slug": path_slug}, {"_id": 0, "slug": 1}).to_list(500)
    total = len(lessons)
    if total == 0:
        return {"path": path, "total": 0, "completed": 0, "is_complete": False}
    slugs = [le["slug"] for le in lessons]
    done = await db.lesson_completions.count_documents({
        "user_id": user_id,
        "lesson_slug": {"$in": slugs},
    })
    return {
        "path": path,
        "total": total,
        "completed": done,
        "is_complete": done >= total,
    }


def _compute_cert_id(user_id: str, path_slug: str) -> str:
    return "CF-" + hashlib.sha1(f"{user_id}:{path_slug}".encode()).hexdigest()[:12].upper()


async def _ensure_certificate_record(user: dict, path_slug: str) -> Optional[str]:
    """Upsert the certificate record if (and only if) the user has fully completed
    the path. Returns the cert_id when the record exists, else None."""
    st = await _track_completion_status(user["id"], path_slug)
    if not st["is_complete"]:
        return None
    cert_id = _compute_cert_id(user["id"], path_slug)
    progress = await db.progress.find_one({"user_id": user["id"]}) or {}
    await db.certificates.update_one(
        {"cert_id": cert_id},
        {"$setOnInsert": {
            "cert_id": cert_id,
            "user_id": user["id"],
            "path_slug": path_slug,
            "track_name": st["path"]["name"],
            "student_name": user.get("name") or user.get("email", "Aluno"),
            "total_lessons": st["total"],
            "xp_earned": int(progress.get("xp_total", 0)),
            "issued_at": datetime.utcnow().isoformat(),
        }},
        upsert=True,
    )
    return cert_id


@api.get("/certificates")
async def list_certificates(user=Depends(current_user)):
    """Return per-track completion status for the current user."""
    paths = await db.paths.find({}, {"_id": 0}).to_list(100)
    items = []
    for p in paths:
        st = await _track_completion_status(user["id"], p["slug"])
        cert_id = None
        if st["is_complete"]:
            # Make sure cert is issued (Pro users will have a record);
            # for non-Pro users we still compute the deterministic id but don't expose it.
            existing_id = _compute_cert_id(user["id"], p["slug"])
            rec = await db.certificates.find_one({"cert_id": existing_id}, {"_id": 0, "cert_id": 1})
            cert_id = rec["cert_id"] if rec else None
        items.append({
            "path_slug": p["slug"],
            "path_name": p["name"],
            "color": p.get("color"),
            "total": st["total"],
            "completed": st["completed"],
            "is_complete": st["is_complete"],
            "cert_id": cert_id,
        })
    return {"items": items, "is_pro": bool(user.get("is_pro"))}


@api.get("/certificates/{path_slug}")
async def download_certificate(path_slug: str, user=Depends(current_user)):
    """Generate and return a PDF certificate for the user's completion of a path.

    Requirements:
      - User must be Pro.
      - User must have completed every lesson in the path.
    """
    if not user.get("is_pro"):
        raise HTTPException(status.HTTP_402_PAYMENT_REQUIRED, "Certificados são exclusivos para usuários Pro")

    st = await _track_completion_status(user["id"], path_slug)
    if not st["is_complete"]:
        raise HTTPException(403, f"Trilha incompleta: {st['completed']}/{st['total']} lições concluídas")

    # Persist (idempotent) so it can be publicly verified.
    cert_id = await _ensure_certificate_record(user, path_slug)
    rec = await db.certificates.find_one({"cert_id": cert_id}, {"_id": 0})

    # render PDF off the event loop to avoid blocking under load
    pdf_bytes = await asyncio.to_thread(
        render_certificate,
        student_name=rec["student_name"],
        track_name=rec["track_name"],
        completed_at=datetime.fromisoformat(rec["issued_at"]),
        cert_id=cert_id,
        total_lessons=rec["total_lessons"],
        xp_earned=rec.get("xp_earned", 0),
    )
    filename = cert_filename(path_slug, rec["student_name"])
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@api.get("/verify/{cert_id}")
async def verify_certificate(cert_id: str):
    """Public certificate verification endpoint (no auth).

    Returns only the fields the UI renders — never leak internal fields
    such as _id or user_id. Uses an explicit allow-list projection.
    """
    rec = await db.certificates.find_one(
        {"cert_id": cert_id},
        {
            "_id": 0,
            "cert_id": 1,
            "student_name": 1,
            "track_name": 1,
            "path_slug": 1,
            "total_lessons": 1,
            "xp_earned": 1,
            "issued_at": 1,
        },
    )
    if not rec:
        raise HTTPException(404, "Certificado não encontrado ou inválido")
    return {"valid": True, **rec}


app.include_router(api)

# Stripe subscription routes (depend on db + auth dep already defined above)
from subscription_routes import build_router as _sub_router, build_webhook_router as _sub_webhook  # noqa: E402
app.include_router(_sub_router(db, current_user))
app.include_router(_sub_webhook(db))

# CodeFuturo Escolas (B2B classes)
from classes_routes import build_router as _classes_router  # noqa: E402
app.include_router(_classes_router(db, current_user))

# Push Notifications (graceful — não derruba o servidor se pywebpush não instalado)
_push_available = False
try:
    from push_routes import build_router as _push_router, build_scheduler as _build_scheduler  # noqa: E402
    app.include_router(_push_router(db, current_user))
    _push_available = True
except Exception as _push_err:  # noqa: BLE001
    logging.warning("push_routes indisponível: %s", _push_err)

logging.basicConfig(level=logging.INFO)

@app.on_event("startup")
async def _start_scheduler():
    if not _push_available:
        return
    try:
        scheduler = _build_scheduler(db)
        scheduler.start()
    except Exception as e:  # noqa: BLE001
        logging.warning("scheduler não iniciou: %s", e)


@app.on_event("startup")
async def startup():
    await db.users.create_index("email", unique=True)
    await db.progress.create_index("user_id", unique=True)
    await db.profiles.create_index("user_id")
    await db.lesson_completions.create_index([("user_id", 1), ("lesson_slug", 1)], unique=True)
    await db.certificates.create_index("cert_id", unique=True)
    await db.classes.create_index("invite_code", unique=True)
    await db.class_memberships.create_index([("class_id", 1), ("user_id", 1)], unique=True)
    await db.class_memberships.create_index("user_id")


@app.on_event("shutdown")
async def shutdown():
    client.close()
