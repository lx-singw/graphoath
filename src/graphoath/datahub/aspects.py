import json
import time
from pathlib import Path
from typing import Dict, Any, Optional
from graphoath.datahub.client import DataHubClient

SCHEMA_PATH = Path(__file__).resolve().parents[3] / "schemas" / "graphoathReceipt.avsc"

def load_aspect_schema() -> Dict[str, Any]:
    """Loads the Pegasus Avro schema for graphoathReceipt aspect."""
    if SCHEMA_PATH.exists():
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "name": "graphoathReceipt",
        "namespace": "com.linkedin.pegasus2avro.dataset",
        "fields": []
    }

def format_receipt_aspect_payload(
    receipt_id: str,
    source_entity_urn: str,
    claim_text: str,
    evidence_urns: list[str],
    agent_module: str = "Deposition",
    citation_resolution_rate: float = 1.0,
    ledger_hash: str = "",
    timestamp_millis: Optional[int] = None
) -> Dict[str, Any]:
    """Formats payload adhering to graphoathReceipt.avsc schema."""
    return {
        "receiptId": receipt_id,
        "timestampMillis": timestamp_millis or int(time.time() * 1000),
        "agentModule": agent_module,
        "sourceEntityUrn": source_entity_urn,
        "claimText": claim_text,
        "evidenceUrns": evidence_urns,
        "citationResolutionRate": citation_resolution_rate,
        "ledgerHash": ledger_hash
    }

async def emit_receipt_aspect(
    client: Optional[DataHubClient] = None,
    entity_urn: Optional[str] = None,
    receipt_payload: Optional[Dict[str, Any]] = None,
    receipt: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Emits custom aspect graphoathReceipt to DataHub GMS for target entity URN.
    """
    aspect_name = "graphoathReceipt"
    target_urn = entity_urn or getattr(receipt, "target_urn", "urn:li:dataset:target")
    payload = receipt_payload or format_receipt_aspect_payload(
        receipt_id=getattr(receipt, "receipt_id", "rcpt_001"),
        source_entity_urn=target_urn,
        claim_text=str(getattr(receipt, "claims_payload", {})),
        evidence_urns=[e.get("urn", "") for e in getattr(receipt, "evidence_payload", []) if isinstance(e, dict)],
        ledger_hash=getattr(receipt, "current_hash", "")
    )
    
    if client is not None and hasattr(client, "execute_graphql"):
        proposal = {
            "entityType": "dataset" if "dataset" in target_urn else "incident",
            "entityUrn": target_urn,
            "aspectName": aspect_name,
            "aspect": {
                "contentType": "application/json",
                "value": json.dumps(payload)
            },
            "changeType": "UPSERT"
        }
        mutation = """
        mutation emitMetadataChangeProposal($input: MetadataChangeProposalInput!) {
          emitMetadataChangeProposal(input: $input)
        }
        """
        try:
            res = await client.execute_graphql(mutation, {"input": proposal})
            if res and isinstance(res, dict):
                return {"status": "SUCCESS", "entity_urn": target_urn, "aspect_name": aspect_name, "response": res}
            return {"status": "SUCCESS", "entity_urn": target_urn, "aspect_name": aspect_name}
        except Exception as e:
            return {"status": "EMITTED_LOCAL", "entity_urn": target_urn, "aspect_name": aspect_name, "payload": payload, "notice": str(e)}

    return {"status": "EMITTED_LOCAL", "entity_urn": target_urn, "aspect_name": aspect_name, "payload": payload}

def emit_custody_receipt_aspect(receipt: Any) -> Dict[str, Any]:
    """Helper to emit aspect from CustodyReceipt object."""
    target_urn = getattr(receipt, "target_urn", "urn:li:dataset:target")
    payload = format_receipt_aspect_payload(
        receipt_id=getattr(receipt, "receipt_id", "rcpt_001"),
        source_entity_urn=target_urn,
        claim_text=str(getattr(receipt, "claims_payload", {})),
        evidence_urns=[e.get("urn", "") for e in getattr(receipt, "evidence_payload", []) if isinstance(e, dict)],
        ledger_hash=getattr(receipt, "current_hash", "")
    )
    return {"status": "EMITTED_LOCAL", "entity_urn": target_urn, "aspect_name": "graphoathReceipt", "payload": payload}
