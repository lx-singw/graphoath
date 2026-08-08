import pytest
from graphoath.ops.playbooks import RemediationPlaybookEngine

def test_dataset_quarantine_playbook():
    engine = RemediationPlaybookEngine()
    target_urn = "urn:li:dataset:(snowflake,prod.orders)"
    res = engine.dataset_quarantine_playbook(target_urn)
    assert res.playbook_id == "dataset_quarantine_playbook"
    assert res.status == "EXECUTED"
    assert res.risk_level == "LOW_NON_DESTRUCTIVE"
    assert res.details["tag"] == "Quarantined"

def test_dbt_model_pause_playbook():
    engine = RemediationPlaybookEngine()
    target_urn = "urn:li:dataset:(snowflake,prod.orders)"
    res = engine.dbt_model_pause_playbook(target_urn)
    assert res.playbook_id == "dbt_model_pause_playbook"
    assert res.status == "PENDING_APPROVAL"
    assert res.risk_level == "MEDIUM_REQUIRES_APPROVAL"
    assert "--defer" in res.details["flags"]

def test_owner_escalation_playbook_unassigned():
    engine = RemediationPlaybookEngine()
    target_urn = "urn:li:dataset:unassigned_table"
    res = engine.owner_escalation_playbook(target_urn)
    assert res.playbook_id == "owner_escalation_playbook"
    assert res.status in ("ESCALATED", "NOTIFIED")
    assert "escalated_to" in res.details
