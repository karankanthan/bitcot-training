from .config import EMAIL_OUTBOX


def send_receipt(to, amount):
    """Stand-in for a real email provider: appends the receipt to a local file."""
    with open(EMAIL_OUTBOX, "a") as f:
        f.write(f"To: {to} | Receipt for ${amount}\n")
