'''
import os

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "dev-secret")
DB_PATH = os.getenv("DB_PATH", "orders.db")
EMAIL_OUTBOX = os.getenv("EMAIL_OUTBOX", "outbox.log")
'''


import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "dev-secret")
DB_PATH = os.getenv("DB_PATH", "orders.db")
EMAIL_OUTBOX = os.getenv("EMAIL_OUTBOX", "outbox.log")