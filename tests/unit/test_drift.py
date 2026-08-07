import pytest
from graphoath.datahub.client import DataHubClient
from graphoath.custody.drift import verify_evidence_drift

@pytest.mark.asyncio
async def test_verify_evidence_drift():
    client = DataHubClient()
    receipt_data = {
        "receipt_id": "rcpt_001",
        "trigger": {"urn": "urn:li:dataset:(snowflake,prod.orders,PROD)"},
        "evidence": [
            {"type": "ownership", "result": "team-growth-analytics"}
        ]
    }
    result = await verify_evidence_drift(client, receipt_data)
    assert result["receipt_id"] == "rcpt_001"
    assert result["ledger_integrity"] == "INTACT_UNMODIFIED"
    assert "evidence_drift_status" in result
