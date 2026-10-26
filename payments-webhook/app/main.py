'''import hashlib
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
    '''

import hashlib
import hmac
import json
import logging

from fastapi import FastAPI, Header, HTTPException, Request

from .config import WEBHOOK_SECRET
from .db import event_exists, list_orders, mark_refunded, save_order
from .emailer import send_receipt

logger = logging.getLogger("payments")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Payments webhook service")


def sign(payload: dict) -> str:
    return hmac.new(
        WEBHOOK_SECRET.encode(),
        json.dumps(payload).encode(),
        hashlib.sha256,
    ).hexdigest()


@app.post("/webhooks/payments")
async def payments_webhook(
    request: Request,
    x_signature: str = Header(default=None),
):
    payload = await request.json()

    expected_signature = sign(payload)
    if not x_signature or not hmac.compare_digest(
        x_signature, expected_signature
    ):
        raise HTTPException(status_code=401, detail="bad signature")

    event_type = payload.get("type")
    data = payload.get("data", {})

    if event_type == "payment.succeeded":
        event_id = payload.get("id")
        if not event_id:
            raise HTTPException(status_code=400, detail="missing event ID")

        try:
            saved = save_order(
                event_id,
                data["payment_id"],
                data["customer_email"],
                data["amount"],
            )
        except Exception:
            logger.exception("Failed to save payment order")
            raise HTTPException(
                status_code=500, detail="failed to save payment"
            )

        if saved:
            try:
                send_receipt(data["customer_email"], data["amount"])
            except Exception:
                logger.exception("Failed to send payment receipt")

    elif event_type == "payment.refunded":
        try:
            mark_refunded(data["payment_id"])
        except Exception:
            logger.exception("Failed to mark payment refunded")
            raise HTTPException(
                status_code=500, detail="failed to mark refund"
            )

    logger.info("Processed payment webhook event type: %s", event_type)
    return {"ok": True}


@app.get("/orders")
def orders():
    return list_orders()


@app.get("/health")
def health():
    return {"status": "ok"}
