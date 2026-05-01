"""CodeFuturo subscription/billing routes — Stripe integration.

Plans are defined here on the backend (NEVER trust price from frontend).
Lookup keys map to Stripe Price IDs at runtime (cached after first call).
"""
import os
import logging
from datetime import datetime
from typing import Optional

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase

logger = logging.getLogger(__name__)

stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
WEBHOOK_SECRET = os.environ["STRIPE_WEBHOOK_SECRET"]

# Server-side plan catalog. Lookup keys must match the ones in Stripe Dashboard.
# Frontend only sends the plan_id — never amount/price.
PLANS = {
    "pro_annual": {
        "lookup_key": "cf_pro_annual",
        "name": "CodeFuturo Pro",
        "price_brl": 347.00,
        "interval": "year",
        "mode": "subscription",
        "tier": "pro",
        "trial_days": 7,
    },
    "pro_pioneer": {
        "lookup_key": "cf_pro_pioneer",
        "name": "CodeFuturo Pioneiros",
        "price_brl": 197.00,
        "interval": "year",
        "mode": "subscription",
        "tier": "pro",
        "trial_days": 7,
    },
    "lifetime": {
        "lookup_key": "cf_lifetime",
        "name": "CodeFuturo Lifetime",
        "price_brl": 997.00,
        "interval": "one_time",
        "mode": "payment",
        "tier": "lifetime",
        "trial_days": 0,
    },
}

# Cache: lookup_key -> price_id (resolved on first use)
_price_cache: dict[str, str] = {}


def _resolve_price_id(lookup_key: str) -> str:
    if lookup_key in _price_cache:
        return _price_cache[lookup_key]
    prices = stripe.Price.list(lookup_keys=[lookup_key], expand=["data.product"], limit=1)
    if not prices.data:
        raise HTTPException(500, f"Stripe price not found for lookup_key={lookup_key}. Check lookup keys in Stripe Dashboard.")
    pid = prices.data[0].id
    _price_cache[lookup_key] = pid
    return pid


# --- Models ---
class CheckoutIn(BaseModel):
    plan_id: str  # one of PLANS keys
    origin_url: str  # frontend origin (window.location.origin)


def build_router(db: AsyncIOMotorDatabase, current_user_dep) -> APIRouter:
    """Factory: receives the shared db handle + auth dependency from server.py."""
    router = APIRouter(prefix="/api/subscription", tags=["subscription"])

    @router.get("/plans")
    async def list_plans():
        return {"plans": [{"id": k, **{x: v for x, v in p.items() if x != "lookup_key"}} for k, p in PLANS.items()]}

    @router.get("/me")
    async def my_subscription(user=Depends(current_user_dep)):
        u = await db.users.find_one({"id": user["id"]}, {"_id": 0, "password_hash": 0})
        return {
            "is_pro": bool(u.get("is_pro")),
            "plan": u.get("plan"),
            "tier": u.get("tier"),
            "subscription_ends_at": u.get("subscription_ends_at"),
            "stripe_customer_id": u.get("stripe_customer_id"),
        }

    @router.post("/checkout")
    async def create_checkout(data: CheckoutIn, user=Depends(current_user_dep)):
        if data.plan_id not in PLANS:
            raise HTTPException(400, "Invalid plan")
        plan = PLANS[data.plan_id]
        price_id = _resolve_price_id(plan["lookup_key"])

        origin = data.origin_url.rstrip("/")
        success_url = f"{origin}/pagamento/sucesso?session_id={{CHECKOUT_SESSION_ID}}"
        cancel_url = f"{origin}/planos?canceled=1"

        # Reuse Stripe customer if user has one
        customer_id = user.get("stripe_customer_id")
        if not customer_id:
            customer = stripe.Customer.create(
                email=user["email"],
                name=user.get("name"),
                metadata={"user_id": user["id"]},
            )
            customer_id = customer.id
            await db.users.update_one({"id": user["id"]}, {"$set": {"stripe_customer_id": customer_id}})

        session_kwargs = {
            "customer": customer_id,
            "mode": plan["mode"],
            "line_items": [{"price": price_id, "quantity": 1}],
            "success_url": success_url,
            "cancel_url": cancel_url,
            "client_reference_id": user["id"],
            "metadata": {
                "user_id": user["id"],
                "plan_id": data.plan_id,
                "tier": plan["tier"],
            },
            "allow_promotion_codes": True,
        }
        if plan["mode"] == "subscription" and plan["trial_days"] > 0:
            session_kwargs["subscription_data"] = {
                "trial_period_days": plan["trial_days"],
                "metadata": {"user_id": user["id"], "plan_id": data.plan_id},
            }

        try:
            session = stripe.checkout.Session.create(**session_kwargs)
        except stripe.error.StripeError as e:
            logger.error("stripe_checkout_create_failed: %s", e)
            raise HTTPException(502, f"Stripe error: {e.user_message or str(e)}")

        # Audit transaction (mandatory per playbook)
        await db.payment_transactions.insert_one({
            "session_id": session.id,
            "user_id": user["id"],
            "plan_id": data.plan_id,
            "mode": plan["mode"],
            "amount_brl": plan["price_brl"],
            "status": "initiated",
            "created_at": datetime.utcnow().isoformat(),
        })

        return {"url": session.url, "session_id": session.id}

    @router.get("/status/{session_id}")
    async def checkout_status(session_id: str, user=Depends(current_user_dep)):
        try:
            session = stripe.checkout.Session.retrieve(session_id)
        except stripe.error.StripeError as e:
            raise HTTPException(404, f"Session not found: {e}")

        # Best-effort: if paid, ensure user is upgraded (idempotent — webhook may have done it already)
        if session.payment_status == "paid" and session.client_reference_id == user["id"]:
            await _activate_user(db, session)

        await db.payment_transactions.update_one(
            {"session_id": session_id},
            {"$set": {
                "status": session.status,
                "payment_status": session.payment_status,
                "updated_at": datetime.utcnow().isoformat(),
            }},
        )

        return {
            "status": session.status,
            "payment_status": session.payment_status,
            "amount_total": session.amount_total,
            "currency": session.currency,
        }

    @router.post("/portal")
    async def customer_portal(req: Request, user=Depends(current_user_dep)):
        if not user.get("stripe_customer_id"):
            raise HTTPException(400, "No subscription to manage")
        body = await req.json() if req.headers.get("content-type", "").startswith("application/json") else {}
        origin = (body or {}).get("origin_url") or "https://codefuturo.com"
        portal = stripe.billing_portal.Session.create(
            customer=user["stripe_customer_id"],
            return_url=origin.rstrip("/") + "/perfil",
        )
        return {"url": portal.url}

    return router


async def _activate_user(db, session):
    """Mark user as Pro/Lifetime based on a paid Stripe Checkout session. Idempotent."""
    user_id = (session.metadata or {}).get("user_id") or session.client_reference_id
    plan_id = (session.metadata or {}).get("plan_id")
    tier = (session.metadata or {}).get("tier", "pro")
    if not user_id:
        return

    update = {
        "is_pro": True,
        "plan": plan_id,
        "tier": tier,
        "stripe_customer_id": session.customer,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if session.mode == "subscription" and session.subscription:
        try:
            sub = stripe.Subscription.retrieve(session.subscription)
            update["stripe_subscription_id"] = sub.id
            ends = sub.current_period_end
            update["subscription_ends_at"] = datetime.utcfromtimestamp(ends).isoformat() if ends else None
            update["subscription_status"] = sub.status  # active | trialing | etc
        except stripe.error.StripeError:
            pass
    elif session.mode == "payment":
        # Lifetime: no expiration
        update["subscription_ends_at"] = None
        update["subscription_status"] = "lifetime"

    await db.users.update_one({"id": user_id}, {"$set": update})


def build_webhook_router(db: AsyncIOMotorDatabase) -> APIRouter:
    """Public webhook router. NOT authenticated (Stripe signs the payload)."""
    router = APIRouter(prefix="/api/webhook", tags=["stripe-webhook"])

    @router.post("/stripe")
    async def stripe_webhook(request: Request):
        payload = await request.body()
        sig = request.headers.get("stripe-signature")
        try:
            event = stripe.Webhook.construct_event(payload, sig, WEBHOOK_SECRET)
        except (ValueError, stripe.error.SignatureVerificationError) as e:
            logger.warning("invalid_webhook_signature: %s", e)
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid signature")

        etype = event["type"]
        obj = event["data"]["object"]
        logger.info("stripe_event: %s", etype)

        if etype == "checkout.session.completed":
            await _activate_user(db, obj)
            await db.payment_transactions.update_one(
                {"session_id": obj["id"]},
                {"$set": {"status": "completed", "payment_status": obj.get("payment_status"), "updated_at": datetime.utcnow().isoformat()}},
            )

        elif etype in ("customer.subscription.updated", "customer.subscription.deleted"):
            sub = obj
            customer_id = sub.get("customer")
            user = await db.users.find_one({"stripe_customer_id": customer_id})
            if user:
                ends_ts = sub.get("current_period_end")
                update = {
                    "subscription_status": sub.get("status"),
                    "subscription_ends_at": datetime.utcfromtimestamp(ends_ts).isoformat() if ends_ts else None,
                    "updated_at": datetime.utcnow().isoformat(),
                }
                # If canceled or expired, downgrade
                if sub.get("status") in ("canceled", "incomplete_expired", "unpaid") or etype == "customer.subscription.deleted":
                    update["is_pro"] = False
                else:
                    update["is_pro"] = True
                await db.users.update_one({"id": user["id"]}, {"$set": update})

        elif etype == "invoice.paid":
            inv = obj
            customer_id = inv.get("customer")
            user = await db.users.find_one({"stripe_customer_id": customer_id})
            if user and inv.get("subscription"):
                try:
                    sub = stripe.Subscription.retrieve(inv["subscription"])
                    await db.users.update_one(
                        {"id": user["id"]},
                        {"$set": {
                            "is_pro": True,
                            "subscription_status": sub.status,
                            "subscription_ends_at": datetime.utcfromtimestamp(sub.current_period_end).isoformat() if sub.current_period_end else None,
                        }},
                    )
                except stripe.error.StripeError:
                    pass

        elif etype == "invoice.payment_failed":
            customer_id = obj.get("customer")
            user = await db.users.find_one({"stripe_customer_id": customer_id})
            if user:
                await db.users.update_one(
                    {"id": user["id"]},
                    {"$set": {"subscription_status": "past_due", "updated_at": datetime.utcnow().isoformat()}},
                )

        return {"received": True}

    return router
