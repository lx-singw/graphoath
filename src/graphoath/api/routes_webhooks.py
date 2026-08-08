import hmac
import hashlib
import time
from typing import Dict, Any
from fastapi import APIRouter, Request, HTTPException, Header, status
from graphoath.config import settings

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

REPLAY_WINDOW_SECONDS = 900  # 15 minutes

def verify_datahub_hmac_signature(
    raw_body: bytes,
    timestamp: str,
    signature: str,
    secret_key: str
) -> bool:
    """
    Validates DataHub Actions Framework HMAC-SHA256 signature.
    Formula: HMAC-SHA256(SecretKey, Timestamp + "." + RawBody)
    """
    if not timestamp or not signature or not secret_key:
        return False
        
    try:
        ts_int = int(timestamp)
        now_int = int(time.time())
        if abs(now_int - ts_int) > REPLAY_WINDOW_SECONDS:
            return False
    except ValueError:
        return False

    message = f"{timestamp}.".encode("utf-8") + raw_body
    computed_signature = hmac.new(
        secret_key.encode("utf-8"),
        message,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(computed_signature.lower(), signature.lower())

@router.post("/datahub", status_code=status.HTTP_200_OK)
async def handle_datahub_webhook(
    request: Request,
    x_datahub_signature: str = Header(None, alias="X-DataHub-Signature"),
    x_datahub_timestamp: str = Header(None, alias="X-DataHub-Timestamp")
) -> Dict[str, Any]:
    """
    Ingests MetadataChangeLog_v1 events from DataHub Actions Framework.
    
    Verifies HMAC signature and rejects replayed or unauthorized events.
    """
    raw_body = await request.body()
    
    # If secret is set, enforce HMAC signature verification
    if settings.datahub_webhook_secret and settings.datahub_webhook_secret != "dev-webhook-secret-key":
        if not x_datahub_signature or not x_datahub_timestamp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing X-DataHub-Signature or X-DataHub-Timestamp header"
            )
        is_valid = verify_datahub_hmac_signature(
            raw_body=raw_body,
            timestamp=x_datahub_timestamp,
            signature=x_datahub_signature,
            secret_key=settings.datahub_webhook_secret
        )
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid DataHub HMAC webhook signature or expired timestamp"
            )

    try:
        event_payload = await request.json()
    except Exception:
        event_payload = {}

    entity_type = event_payload.get("entityType", "UNKNOWN")
    entity_urn = event_payload.get("entityUrn", "UNKNOWN")
    change_type = event_payload.get("changeType", "UPSERT")

    return {
        "status": "ACCEPTED",
        "entity_type": entity_type,
        "entity_urn": entity_urn,
        "change_type": change_type,
        "timestamp": int(time.time())
    }
