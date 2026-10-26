import os

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "dev-secret")
DB_PATH = os.getenv("DB_PATH", "orders.db")
EMAIL_OUTBOX = os.getenv("EMAIL_OUTBOX", "outbox.log")
