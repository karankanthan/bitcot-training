from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app, sign

client = TestClient(app)


def make_event(event_id="evt_1", payment_id="pay_1", type_="payment.succeeded"):
    return {
        "id": event_id,
        "type": type_,
        "data": {"payment_id": payment_id, "customer_email": "asha@example.com", "amount": 49.99},
    }


@patch("app.main.send_receipt")
def test_payment_succeeded_creates_order(mock_send):
    event = make_event()
    r = client.post("/webhooks/payments", json=event, headers={"X-Signature": sign(event)})
    assert r.status_code == 200
    orders = client.get("/orders").json()
    assert len(orders) == 1
    assert orders[0]["status"] == "paid"
    mock_send.assert_called_once()


@patch("app.main.send_receipt")
def test_refund_marks_order_refunded(mock_send):
    paid = make_event()
    client.post("/webhooks/payments", json=paid, headers={"X-Signature": sign(paid)})
    refund = make_event("evt_2", "pay_1", "payment.refunded")
    r = client.post("/webhooks/payments", json=refund, headers={"X-Signature": sign(refund)})
    assert r.status_code == 200
    assert client.get("/orders").json()[0]["status"] == "refunded"


def test_wrong_signature_rejected():
    event = make_event()
    r = client.post("/webhooks/payments", json=event, headers={"X-Signature": "wrong"})
    assert r.status_code == 401
