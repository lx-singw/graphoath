import hmac
import hashlib
import time
import pytest
from fastapi.testclient import TestClient
from graphoath.main import app
from graphoath.config import settings
from graphoath.api.routes_webhooks import verify_datahub_hmac_signature

client = TestClient(app)

def test_verify_datahub_hmac_signature_valid():
    secret = "test-secret-key"
    ts = str(int(time.time()))
    body = b'{"entityType": "DATASET", "entityUrn": "urn:li:dataset:test"}'
    
    msg = f"{ts}.".encode("utf-8") + body
    sig = hmac.new(secret.encode("utf-8"), msg, hashlib.sha256).hexdigest()
    
    assert verify_datahub_hmac_signature(body, ts, sig, secret) is True

def test_verify_datahub_hmac_signature_invalid():
    secret = "test-secret-key"
    ts = str(int(time.time()))
    body = b'{"entityType": "DATASET"}'
    
    assert verify_datahub_hmac_signature(body, ts, "invalid_sig", secret) is False

def test_verify_datahub_hmac_signature_expired():
    secret = "test-secret-key"
    old_ts = str(int(time.time()) - 3600)  # 1 hour ago
    body = b'{"entityType": "DATASET"}'
    
    msg = f"{old_ts}.".encode("utf-8") + body
    sig = hmac.new(secret.encode("utf-8"), msg, hashlib.sha256).hexdigest()
    
    assert verify_datahub_hmac_signature(body, old_ts, sig, secret) is False

def test_webhook_endpoint_unprotected_dev_mode():
    payload = {
        "entityType": "DATASET",
        "entityUrn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)",
        "changeType": "UPSERT"
    }
    response = client.post("/api/v1/webhooks/datahub", json=payload)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["status"] == "ACCEPTED"
    assert res_data["entity_type"] == "DATASET"
