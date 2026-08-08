import pytest
from graphoath.agents.egal_loop import run_egal_loop

def test_egal_loop_executed_on_valid_evidence():
    event_payload = {
        "source_urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)",
        "event_type": "DBT_TEST_FAILURE"
    }
    claimed_urns = ["urn:li:dataset:(urn:li:dataPlatform:dbt,dbt.stg_orders,PROD)"]
    
    state = run_egal_loop(event_payload=event_payload, claimed_urns=claimed_urns, draft_claim="Schema break")
    
    assert state["action_status"] == "EXECUTED"
    assert state["citation_passed"] is True
    assert state["incident_urn"] is not None
    assert state["receipt_id"] is not None

def test_egal_loop_rejected_on_unevidenced_claim():
    event_payload = {
        "source_urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)",
        "event_type": "DBT_TEST_FAILURE"
    }
    claimed_urns = ["urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.fake_table_888,PROD)"]
    
    state = run_egal_loop(event_payload=event_payload, claimed_urns=claimed_urns, draft_claim="Schema break")
    
    assert state["action_status"] == "REJECTED"
    assert state["citation_passed"] is False
    assert len(state["missing_citations"]) == 1
    assert "prod.fake_table_888" in state["missing_citations"][0]
