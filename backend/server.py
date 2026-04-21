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

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)

app = FastAPI(title="CodeFuturo API")
api = APIRouter(prefix="/api")


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


def calc_age(birth_date: str) -> int:
    bd = datetime.strptime(birth_date, "%Y-%m-%d").date()
    today = date.today()
    age = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
    return age


def public_user(u: dict) -> dict:
    return {"id": u["id"], "email": u["email"], "name": u["name"]}


async def ensure_progress(user_id: str) -> dict:
    prog = await db.progress.find_one({"user_id": user_id})
    if prog:
        return prog
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
    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
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

    prog.update(update)
    return {"already_completed": False, "progress": serialize(prog), "xp_earned": xp}


@api.post("/energy/consume")
async def consume_energy(user=Depends(current_user)):
    prog = await ensure_progress(user["id"])
    # Reset if >24h
    try:
        last_reset = datetime.fromisoformat(prog.get("last_energy_reset"))
    except Exception:
        last_reset = datetime.utcnow() - timedelta(hours=25)
    if datetime.utcnow() - last_reset > timedelta(hours=24):
        prog["energy"] = prog["max_energy"]
        prog["last_energy_reset"] = datetime.utcnow().isoformat()

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


@api.get("/tracks")
async def tracks():
    # Static seed for now
    modules = [
        {"id": "m1", "name": "Explorador Digital", "age": "6-8", "color": "#34D399", "lessons": 42, "level": "Iniciante"},
        {"id": "m2", "name": "Criador de Blocos", "age": "9-11", "color": "#3B82F6", "lessons": 48, "level": "Iniciante"},
        {"id": "m3", "name": "Programador Iniciante", "age": "12-14", "color": "#7C3AED", "lessons": 60, "level": "Intermediário"},
        {"id": "m4", "name": "Desenvolvedor", "age": "15-17", "color": "#F97316", "lessons": 72, "level": "Avançado"},
    ]
    specialized = [
        {"id": "webfs", "name": "Web Full Stack", "level": "Intermediário", "lessons": 86, "color": "#A3E635"},
        {"id": "datasci", "name": "Ciência de Dados", "level": "Intermediário", "lessons": 72, "color": "#3B82F6"},
        {"id": "ml", "name": "Machine Learning", "level": "Avançado", "lessons": 64, "color": "#7C3AED"},
        {"id": "mobile", "name": "Mobile Dev", "level": "Intermediário", "lessons": 58, "color": "#F97316"},
        {"id": "gamedev", "name": "Game Dev", "level": "Intermediário", "lessons": 70, "color": "#EC4899"},
        {"id": "cyber", "name": "Cybersecurity", "level": "Avançado", "lessons": 54, "color": "#EF4444"},
        {"id": "devops", "name": "DevOps & Cloud", "level": "Avançado", "lessons": 62, "color": "#06B6D4"},
        {"id": "dba", "name": "Banco de Dados", "level": "Intermediário", "lessons": 48, "color": "#84CC16"},
    ]
    return {"modules": modules, "specialized": specialized}


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


app.include_router(api)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)


@app.on_event("startup")
async def startup():
    await db.users.create_index("email", unique=True)
    await db.progress.create_index("user_id", unique=True)
    await db.profiles.create_index("user_id")
    await db.lesson_completions.create_index([("user_id", 1), ("lesson_slug", 1)], unique=True)


@app.on_event("shutdown")
async def shutdown():
    client.close()
