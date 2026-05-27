"""
Push Notification routes + daily reminder scheduler com horário por usuário.
Env vars: VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY, VAPID_CLAIMS_EMAIL
"""
import os, json, logging
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from pywebpush import webpush, WebPushException
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger("push")

VAPID_PUBLIC_KEY  = os.environ.get("VAPID_PUBLIC_KEY", "")
VAPID_PRIVATE_KEY = os.environ.get("VAPID_PRIVATE_KEY", "")
VAPID_EMAIL       = os.environ.get("VAPID_CLAIMS_EMAIL", "mailto:contato@codefuturo.com")

BRT = ZoneInfo("America/Sao_Paulo")


# ── models ────────────────────────────────────────────────────────────────────

class PushSubscription(BaseModel):
    endpoint: str
    keys: dict  # {"p256dh": "...", "auth": "..."}


class PushPreference(BaseModel):
    notification_hour: int = Field(..., ge=0, le=23)


# ── helpers ───────────────────────────────────────────────────────────────────

def _send_push(subscription_info: dict, payload: dict) -> bool:
    """Envia push. Retorna True no sucesso, False em falha permanente."""
    if not VAPID_PRIVATE_KEY:
        return False
    try:
        webpush(
            subscription_info=subscription_info,
            data=json.dumps(payload),
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims={"sub": VAPID_EMAIL},
        )
        return True
    except WebPushException as e:
        if e.response and e.response.status_code in (404, 410):
            return False  # endpoint expirado → remover
        logger.warning("push_send_failed: %s", e)
        return False
    except Exception as e:
        logger.warning("push_error: %s", e)
        return False


# ── router ────────────────────────────────────────────────────────────────────

def build_router(db, current_user):
    router = APIRouter(prefix="/api/push", tags=["push"])

    # ── VAPID public key (sem auth) ──────────────────────────────────────────
    @router.get("/vapid-public-key")
    async def get_vapid_key():
        return {"publicKey": VAPID_PUBLIC_KEY}

    # ── Inscrever ────────────────────────────────────────────────────────────
    @router.post("/subscribe")
    async def subscribe(sub: PushSubscription, user=Depends(current_user)):
        await db.push_subscriptions.update_one(
            {"user_id": user["id"], "endpoint": sub.endpoint},
            {"$set": {
                "user_id": user["id"],
                "endpoint": sub.endpoint,
                "keys": sub.keys,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }},
            upsert=True,
        )
        return {"ok": True}

    # ── Cancelar inscrição ───────────────────────────────────────────────────
    @router.delete("/subscribe")
    async def unsubscribe(sub: PushSubscription, user=Depends(current_user)):
        await db.push_subscriptions.delete_one(
            {"user_id": user["id"], "endpoint": sub.endpoint}
        )
        return {"ok": True}

    # ── Preferências de horário ──────────────────────────────────────────────
    @router.get("/preferences")
    async def get_preferences(user=Depends(current_user)):
        pref = await db.push_preferences.find_one(
            {"user_id": user["id"]}, {"_id": 0}
        )
        return {"notification_hour": pref["notification_hour"] if pref else 19}

    @router.put("/preferences")
    async def set_preferences(body: PushPreference, user=Depends(current_user)):
        await db.push_preferences.update_one(
            {"user_id": user["id"]},
            {"$set": {
                "user_id": user["id"],
                "notification_hour": body.notification_hour,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }},
            upsert=True,
        )
        return {"ok": True, "notification_hour": body.notification_hour}

    # ── Teste manual ─────────────────────────────────────────────────────────
    @router.post("/test")
    async def test_push(user=Depends(current_user)):
        """Envia push de teste imediato para o usuário autenticado."""
        subs = await db.push_subscriptions.find(
            {"user_id": user["id"]}
        ).to_list(length=10)

        if not subs:
            return {"ok": False, "reason": "Nenhuma inscrição encontrada para este usuário"}

        name = (user.get("name") or "").split()[0] or "Dev"
        payload = {
            "title": "🧪 Teste — CodeFuturo",
            "body": f"Ei, {name}! Suas notificações estão funcionando perfeitamente 🚀",
            "icon": "/icons/icon-192.png",
            "badge": "/icons/icon-192.png",
            "url": "/dashboard",
        }

        sent, dead = 0, []
        for sub in subs:
            ok = _send_push({"endpoint": sub["endpoint"], "keys": sub["keys"]}, payload)
            if ok:
                sent += 1
            else:
                dead.append(sub["endpoint"])

        if dead:
            await db.push_subscriptions.delete_many(
                {"user_id": user["id"], "endpoint": {"$in": dead}}
            )

        return {"ok": sent > 0, "sent": sent, "removed_dead": len(dead)}

    return router


# ── scheduler horário por usuário ─────────────────────────────────────────────

def build_scheduler(db) -> AsyncIOScheduler:
    """
    Roda todo início de hora (BRT).
    Para cada usuário inscrito, verifica se o horário preferido (padrão 19h)
    bate com a hora atual e, se estiver inativo nas últimas 20-47h, envia push.
    """
    scheduler = AsyncIOScheduler(timezone="America/Sao_Paulo")

    async def send_hourly_reminders():
        now_utc  = datetime.now(timezone.utc)
        now_brt  = datetime.now(BRT)
        current_hour = now_brt.hour

        # Janela de inatividade: não praticou ontem mas ainda está "em risco"
        cutoff_min = now_utc - timedelta(hours=47)
        cutoff_max = now_utc - timedelta(hours=20)

        # Usuários inativos
        inactive_users = await db.users.find({
            "last_activity": {
                "$gte": cutoff_min.isoformat(),
                "$lte": cutoff_max.isoformat(),
            }
        }).to_list(length=500)

        if not inactive_users:
            logger.info("push_hourly[%sh]: nenhum usuário inativo", current_hour)
            return

        inactive_map = {u["id"]: u for u in inactive_users}

        # IDs de usuários com pelo menos uma inscrição ativa
        subscribed_ids = await db.push_subscriptions.distinct("user_id")

        sent_total = 0
        for user_id in subscribed_ids:
            # Só notifica usuários inativos
            user_doc = inactive_map.get(user_id)
            if not user_doc:
                continue

            # Horário preferido (default 19)
            pref = await db.push_preferences.find_one({"user_id": user_id})
            preferred_hour = pref["notification_hour"] if pref else 19
            if preferred_hour != current_hour:
                continue

            subs = await db.push_subscriptions.find(
                {"user_id": user_id}
            ).to_list(length=10)

            name = (user_doc.get("name") or "").split()[0] or "Dev"
            payload = {
                "title": f"Ei, {name}! 🚀",
                "body": "Não deixe sua sequência quebrar! Pratique hoje no CodeFuturo.",
                "icon": "/icons/icon-192.png",
                "badge": "/icons/icon-192.png",
                "url": "/dashboard",
            }

            dead = []
            for sub in subs:
                ok = _send_push(
                    {"endpoint": sub["endpoint"], "keys": sub["keys"]}, payload
                )
                if ok:
                    sent_total += 1
                else:
                    dead.append(sub["endpoint"])

            if dead:
                await db.push_subscriptions.delete_many(
                    {"user_id": user_id, "endpoint": {"$in": dead}}
                )

        logger.info("push_hourly[%sh]: %d push(es) enviado(s)", current_hour, sent_total)

    # Roda todo início de hora
    scheduler.add_job(send_hourly_reminders, "cron", minute=0)
    return scheduler
