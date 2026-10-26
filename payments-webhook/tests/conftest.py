import os
import tempfile

_tmp = tempfile.mkdtemp()
os.environ["DB_PATH"] = os.path.join(_tmp, "test.db")
os.environ["EMAIL_OUTBOX"] = os.path.join(_tmp, "outbox.log")

import pytest


@pytest.fixture(autouse=True)
def clean_db():
    if os.path.exists(os.environ["DB_PATH"]):
        os.remove(os.environ["DB_PATH"])
    yield
