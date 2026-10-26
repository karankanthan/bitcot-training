import hashlib
import hmac
import json
import logging

from fastapi import FastAPI, Header, HTTPException, Request

from .config import WEBHOOK_SECRET
from .db import list_orders, mark_refunded, save_order
from .emailer import send_receipt

logger = logging.getLogger("payments")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Payments webhook service")


def sign(payload: dict) -> str:
    return hmac.new(WEBHOOK_SECRET.encode(), json.dumps(payload).encode(), hashlib.sha256).hexdigest()


@app.post("/webhooks/payments")
async def payments_webhook(request: Request, x_signature: str = Header(default=None)):
    payload = await request.json()

    if x_signature and x_signature != sign(payload):
        raise HTTPException(status_code=401, detail="bad signature")

    logger.info("received event %s", payload)

    event_type = payload.get("type")
    data = payload.get("data", {})

    if event_type == "payment.succeeded":
        try:
            send_receipt(data["customer_email"], data["amount"])
        except Exception:
            pass
        save_order(payload["id"], data["payment_id"], data["customer_email"], data["amount"])
    elif event_type == "payment.refunded":
        mark_refunded(data["payment_id"])

    return {"ok": True}


@app.get("/orders")
def orders():
    return list_orders()


@app.get("/health")
def health():
    return {"status": "ok"}
