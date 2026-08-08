import pytest
from fastapi.testclient import TestClient
from graphoath.main import app

client = TestClient(app)

def test_api_health_endpoint():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

def test_auth_login_endpoint():
    res = client.post("/api/v1/auth/login", json={"username": "operator", "password": "password123"})
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_auth_refresh_endpoint():
    res = client.post("/api/v1/auth/refresh", json={"refresh_token": "mock_refresh_token"})
    assert res.status_code == 200
    assert "access_token" in res.json()

def test_receipts_list_endpoint():
    res = client.get("/api/v1/receipts")
    assert res.status_code == 200
    assert "receipts" in res.json()

def test_receipt_detail_endpoint():
    res = client.get("/api/v1/receipts/rcpt_test_001")
    assert res.status_code == 200
    assert res.json()["receipt_id"] == "rcpt_test_001"

def test_receipt_verify_drift_endpoint():
    res = client.post("/api/v1/receipts/verify-drift", json={"receipt_id": "rcpt_test_001"})
    assert res.status_code == 200
    data = res.json()
    assert "evidence_drift_status" in data or "drift_detected" in data

def test_incidents_detail_endpoint():
    res = client.get("/api/v1/incidents/urn:li:incident:inc_100")
    assert res.status_code == 200
    assert "incident_urn" in res.json()

def test_approvals_approve_endpoint():
    res = client.post("/api/v1/approvals/act_pause_001/approve", json={"operator_urn": "urn:li:corpuser:alice_operator"})
    assert res.status_code == 200
    assert res.json()["status"].upper() == "APPROVED"

def test_approvals_deny_endpoint():
    res = client.post("/api/v1/approvals/act_pause_001/deny", json={"operator_urn": "urn:li:corpuser:alice_operator"})
    assert res.status_code == 200
    assert res.json()["status"].upper() == "DENIED"

def test_ledger_verify_endpoint():
    res = client.get("/api/v1/ledger/verify")
    assert res.status_code == 200
    assert "status" in res.json()

def test_gate_evaluate_endpoint():
    payload = {
        "agent_id": "deposition_agent_v1",
        "action_type": "raiseIncident",
        "claimed_urns": ["urn:li:dataset:(snowflake,prod.orders)"],
        "evidence_urns": ["urn:li:dataset:(snowflake,prod.orders)"]
    }
    res = client.post("/api/v1/gate/evaluate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "APPROVED"
    assert data["citation_resolution_rate"] == 1.0

def test_exports_endpoint():
    res = client.post("/api/v1/exports", json={"export_type": "SOC2_AUDIT", "format": "JSON"})
    assert res.status_code in [200, 201, 202]
    assert "export_id" in res.json()

def test_webhooks_datahub_endpoint():
    payload = {
        "event_type": "MetadataChangeLog_v1",
        "entity_urn": "urn:li:dataset:(snowflake,prod.orders)",
        "change_type": "UPSERT",
        "timestamp": 1786200000
    }
    res = client.post("/api/v1/webhooks/datahub", json=payload)
    assert res.status_code == 200
    assert res.json()["status"] in ["PROCESSED", "ACCEPTED"]

def test_prometheus_metrics_endpoint():
    res = client.get("/metrics")
    assert res.status_code == 200
    assert "graphoath_claims_evaluated_total" in res.text
