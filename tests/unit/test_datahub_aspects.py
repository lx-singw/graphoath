import pytest
from unittest.mock import AsyncMock
from graphoath.datahub.client import DataHubClient
from graphoath.datahub.aspects import (
    load_aspect_schema,
    format_receipt_aspect_payload,
    emit_receipt_aspect,
)

def test_load_aspect_schema():
    schema = load_aspect_schema()
    assert schema.get("name") == "graphoathReceipt"
    assert "fields" in schema

def test_format_receipt_aspect_payload():
    payload = format_receipt_aspect_payload(
        receipt_id="rcpt_12345",
        source_entity_urn="urn:li:dataset:source",
        claim_text="Verified claim statement",
        evidence_urns=["urn:li:dataset:e1", "urn:li:dataset:e2"],
        ledger_hash="sha256_mock_hash"
    )
    assert payload["receiptId"] == "rcpt_12345"
    assert payload["sourceEntityUrn"] == "urn:li:dataset:source"
    assert payload["citationResolutionRate"] == 1.0
    assert len(payload["evidenceUrns"]) == 2

@pytest.mark.asyncio
async def test_emit_receipt_aspect():
    mock_client = AsyncMock(spec=DataHubClient)
    mock_client.execute_graphql.return_value = {"data": {"emitMetadataChangeProposal": True}}

    payload = format_receipt_aspect_payload(
        receipt_id="rcpt_999",
        source_entity_urn="urn:li:dataset:source",
        claim_text="Claim",
        evidence_urns=[]
    )
    res = await emit_receipt_aspect(mock_client, "urn:li:dataset:source", payload)
    assert res["status"] == "SUCCESS"
