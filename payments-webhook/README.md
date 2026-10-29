# Payments webhook service

Receives payment events from our payment provider, saves an order, and emails the customer a receipt.

## Run

    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    uvicorn app.main:app --reload

Send a sample event from a second terminal: `python scripts/send_event.py`
List orders: `GET http://127.0.0.1:8000/orders`

## Test

    pytest

## Events handled

- `payment.succeeded`: sends a receipt email and saves the order
- `payment.refunded`: marks the order as refunded

## Pull request

This change adds the webhook endpoint and is ready to ship. Tests pass.
