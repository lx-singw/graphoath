from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from graphoath.datahub.client import DataHubClient
from graphoath.datahub.incidents import raise_incident
from graphoath.custody.receipt import Receipt
from graphoath.custody.ledger import Ledger

async def execute_deposition(
    client: DataHubClient,
    ledger: Ledger,
    trigger_info: Dict[str, Any],
    claim: str,
    evidence: List[Dict[str, Any]],
    prior_receipts: Optional[List[str]] = None,
    memory_note: Optional[str] = None
) -> Receipt:
    target_urn = trigger_info.get("urn", "")
    incident_res = await raise_incident(
        client=client,
        target_urn=target_urn,
        incident_type="DATA_SCHEMA",
        title=claim
    )

    action_taken = {
        "type": "raise_incident",
        "incident_urn": incident_res["incident_urn"],
        "target_channel": "#team-growth-analytics",
        "reversible": True,
        "requires_approval": False
    }

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    receipt_id = f"rcpt_{timestamp}-0091"

    receipt = Receipt(
        receipt_id=receipt_id,
        module="deposition",
        created_at=timestamp,
        trigger_info=trigger_info,
        claim=claim,
        evidence=evidence,
        action_taken=action_taken,
        prev_hash="",
        confidence="high",
        prior_receipts=prior_receipts or [],
        memory_note=memory_note
    )

    recorded_receipt = ledger.append_receipt(receipt)
    return recorded_receipt
