"""
Push Notification routes + daily reminder scheduler.
Requires env vars: VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY, VAPID_CLAIMS_EMAIL
"""
import os, json, logging
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from pywebpush import webpush, WebPushException
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger("push")

VAPID_PUBLIC_KEY  = os.environ.get("VAPID_PUBLIC_KEY", "")
VAPID_PRIVATE_KEY = os.environ.get("VAPID_PRIVATE_KEY", "")
VAPID_EMAIL       = os.environ.get("VAPID_CLAIMS_EMAIL", "mailto:contato@codefuturo.com")


# ── models ────────────────────────────────────────────────────────────────────

class PushSubscription(BaseModel):
    endpoint: str
    keys: dict  # {"p256dh": "...", "auth": "..."}


# ── helpers ───────────────────────────────────────────────────────────────────

def _send_push(subscription_info: dict, payload: dict) -> bool:
    """Send a single push message. Returns True on success."""
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
        # 410 Gone = subscription expired, 404 = endpoint not found
        if e.response and e.response.status_code in (404, 410):
            return False  # caller should delete this subscription
        logger.warning("push_send_failed: %s", e)
        return False
    except Exception as e:
        logger.warning("push_error: %s", e)
        return False


# ── router builder ────────────────────────────────────────────────────────────

def build_router(db, current_user):
    router = APIRouter(prefix="/api/push", tags=["push"])

    @router.get("/vapid-public-key")
    async def get_vapid_key():
        return {"publicKey": VAPID_PUBLIC_KEY}

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

    @router.delete("/subscribe")
    async def unsubscribe(sub: PushSubscription, user=Depends(current_user)):
        await db.push_subscriptions.delete_one(
            {"user_id": user["id"], "endpoint": sub.endpoint}
        )
        return {"ok": True}

    return router


# ── daily reminder scheduler ──────────────────────────────────────────────────

def build_scheduler(db) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="America/Sao_Paulo")

    async def send_daily_reminders():
        """Send push to users inactive for 20-47 h (missed yesterday's session)."""
        now = datetime.now(timezone.utc)
        cutoff_min = now - timedelta(hours=47)
        cutoff_max = now - timedelta(hours=20)

        # Find users whose last activity is in the "missed" window
        inactive_users = await db.users.find({
            "last_activity": {
                "$gte": cutoff_min.isoformat(),
                "$lte": cutoff_max.isoformat(),
            }
        }).to_list(length=500)

        for user in inactive_users:
            subs = await db.push_subscriptions.find(
                {"user_id": user["id"]}
            ).to_list(length=10)

            name = (user.get("name") or "").split()[0] or "Dev"
            payload = {
                "title": f"Ei, {name}! 🚀",
                "body": "Não deixe sua sequência quebrar! Pratique hoje no CodeFuturo.",
                "icon": "/icons/icon-192.png",
                "badge": "/icons/icon-192.png",
                "url": "/dashboard",
            }

            dead_endpoints = []
            for sub in subs:
                ok = _send_push(
                    {"endpoint": sub["endpoint"], "keys": sub["keys"]},
                    payload,
                )
                if not ok:
                    dead_endpoints.append(sub["endpoint"])

            if dead_endpoints:
                await db.push_subscriptions.delete_many(
                    {"user_id": user["id"], "endpoint": {"$in": dead_endpoints}}
                )

        logger.info("daily_reminders_sent: %d users", len(inactive_users))

    # Run every day at 19:00 (horário de Brasília)
    scheduler.add_job(send_daily_reminders, "cron", hour=19, minute=0)
    return scheduler
