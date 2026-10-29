# Payment Webhook Risk Review

## 1. Missing or Invalid Signature — Critical

**Risk:** An attacker could send fake payment events if the webhook accepts requests without a valid signature.

**Fix:** The webhook now rejects missing or invalid signatures and uses `hmac.compare_digest()` to compare signatures safely.

## 2. Duplicate Webhook Events — High

**Risk:** Payment providers may retry events, which could create duplicate orders and send duplicate receipt emails.

**Fix:** The database now uses a unique event ID, and duplicate insertions are ignored. The application sends a receipt only when a new order is saved.

## 3. Database Failure Before Email — High

**Risk:** Sending a receipt before saving an order could notify a customer about an order that was not stored.

**Fix:** The application saves the order first. If saving fails, it returns an error and does not send the receipt.

## 4. Sensitive Information in Logs — Medium

**Risk:** Logging the complete webhook payload could expose customer or payment information.

**Fix:** The application logs the event type instead of the full payload.

## 5. Receipt Email Failure — Medium

**Risk:** If email delivery fails after an order is saved, the customer may not receive a receipt. A duplicate event will not automatically resend it.

**Recommendation:** Add a retry mechanism or a background email queue and monitor failed deliveries.

## Verification

Six automated tests pass, covering successful payments, refunds, invalid and missing signatures, duplicate events, and database-write failure. One dependency deprecation warning remains.
