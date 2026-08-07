import pytest
from graphoath.datahub.client import DataHubClient
from graphoath.custody.ledger import Ledger
from graphoath.modules.deposition.trigger import DepositionTrigger
from graphoath.modules.deposition.evidence import gather_evidence
from graphoath.modules.deposition.gate import validate_citation_gate
from graphoath.modules.deposition.action import execute_deposition

@pytest.mark.asyncio
async def test_deposition_pipeline_end_to_end():
    client = DataHubClient()
    ledger = Ledger()
    trigger = DepositionTrigger()

    raw_event = {
        "event": "field_removed",
        "urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,ecommerce.fct_orders,PROD)",
        "field": "customer_region"
    }

    # 1. Trigger
    trigger_info = trigger.normalize_event(raw_event)
    assert trigger_info["field"] == "customer_region"

    # 2. Evidence
    evidence = await gather_evidence(client, trigger_info)
    assert len(evidence) > 0

    # 3. Gate
    claim = "Removing customer_region will affect churn-overview and churn_model_v3"
    is_approved, finalized_claim, unsupported = validate_citation_gate(claim, evidence)
    assert is_approved is True

    # 4. Action & Custody
    receipt = await execute_deposition(
        client=client,
        ledger=ledger,
        trigger_info=trigger_info,
        claim=finalized_claim,
        evidence=evidence
    )

    assert receipt.receipt_id.startswith("rcpt_")
    assert receipt.hash != ""
    assert ledger.verify_chain()[0] is True
