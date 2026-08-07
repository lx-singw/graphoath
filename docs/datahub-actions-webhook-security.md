# GraphOath — DataHub Actions Webhook HMAC Security Protocol

This document specifies **GraphOath's Inbound Webhook Security Architecture**, detailing how GraphOath validates DataHub Actions framework change events (`MetadataChangeLog_v1`) to prevent spoofing and replay attacks.

---

## 1. Webhook Signature Verification Algorithm

All inbound webhooks sent from DataHub Actions to GraphOath must include the `X-DataHub-Signature` and `X-DataHub-Timestamp` headers.

```
  Signature = HMAC-SHA256(SecretKey, Timestamp + "." + RawRequestBody)
```

```python
import hmac
import hashlib
import time

def verify_datahub_webhook(raw_body: bytes, timestamp: str, signature: str, secret: str) -> bool:
    # 1. Reject expired timestamps (prevent replay attacks > 300s old)
    current_time = int(time.time())
    if abs(current_time - int(timestamp)) > 300:
        return False
    
    # 2. Recompute expected HMAC-SHA256 signature
    payload_to_sign = f"{timestamp}.".encode('utf-8') + raw_body
    expected_sig = hmac.new(secret.encode('utf-8'), payload_to_sign, hashlib.sha256).hexdigest()
    
    # 3. Constant-time string comparison to prevent timing attacks
    return hmac.compare_digest(expected_sig, signature)
```

---

## 2. Replay Prevention & Nonce Tracking

GraphOath maintains an in-memory sliding window of processed event nonces (`event_id` or `MCL_uuid`). Duplicate event UUIDs received within a 15-minute window are safely ignored, ensuring **idempotent processing**.
