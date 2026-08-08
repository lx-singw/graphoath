import pytest
from fastapi.testclient import TestClient
from graphoath.main import app
from graphoath.ops.slack_notifier import SlackNotifier, is_destructive_action
from graphoath.custody.ledger import Ledger

client = TestClient(app)

def test_destructive_action_pauses_in_pending():
    assert is_destructive_action("deprecateDataset") is True
    assert is_destructive_action("raiseIncident") is False

def test_approve_action_via_api():
    Ledger.clear_memory()
    action_id = "act_test_99"
    
    # 1. Post approval request
    res = client.post(
        f"/api/v1/approvals/{action_id}/approve",
        json={"operator_urn": "urn:li:corpuser:alice_operator", "comment": "Approved for migration"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "APPROVED"
    assert data["operator_urn"] == "urn:li:corpuser:alice_operator"
    assert "receipt_id" in data

    # 2. Verify receipt created in custody ledger
    ledger = Ledger()
    all_rcpts = ledger.get_all_receipts()
    assert len(all_rcpts) >= 1
    latest = all_rcpts[-1]
    assert latest.spiffe_id == "urn:li:corpuser:alice_operator"
