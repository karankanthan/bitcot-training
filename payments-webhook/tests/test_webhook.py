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

@patch("app.main.send_receipt")
def test_duplicate_event_does_not_create_duplicate_order(mock_send):
    event = make_event()

    first = client.post(
        "/webhooks/payments",
        json=event,
        headers={"X-Signature": sign(event)},
    )
    second = client.post(
        "/webhooks/payments",
        json=event,
        headers={"X-Signature": sign(event)},
    )

    assert first.status_code == 200
    assert second.status_code == 200

    orders = client.get("/orders").json()
    assert len(orders) == 1
    mock_send.assert_called_once()


def test_missing_signature_rejected():
    event = make_event()

    response = client.post("/webhooks/payments", json=event)

    assert response.status_code == 401


@patch("app.main.send_receipt")
@patch("app.main.save_order", side_effect=Exception("database unavailable"))
def test_database_failure_does_not_send_receipt(mock_save, mock_send):
    event = make_event()

    response = client.post(
        "/webhooks/payments",
        json=event,
        headers={"X-Signature": sign(event)},
    )

    assert response.status_code == 500
    mock_send.assert_not_called()

