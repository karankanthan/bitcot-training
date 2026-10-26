"""Send a signed sample event to a running server.

Usage: python scripts/send_event.py [payment_id]
"""
import json
import sys
import urllib.request

from app.main import sign

payment_id = sys.argv[1] if len(sys.argv) > 1 else "pay_100"
payload = {
    "id": f"evt_{payment_id}",
    "type": "payment.succeeded",
    "data": {"payment_id": payment_id, "customer_email": "asha@example.com", "amount": 49.99},
}
req = urllib.request.Request(
    "http://127.0.0.1:8000/webhooks/payments",
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json", "X-Signature": sign(payload)},
)
print(urllib.request.urlopen(req).read().decode())
