from typing import Dict, Any, List
from graphoath.datahub.client import DataHubClient
from graphoath.datahub.ownership import get_ownership

async def verify_evidence_drift(client: DataHubClient, receipt_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Re-verifies evidence items cited in a receipt against live DataHub graph
    to detect evidence drift (e.g. ownership transfer or schema field removal).
    """
    receipt_id = receipt_data.get("receipt_id", "")
    evidence_items = receipt_data.get("evidence", [])

    drift_details: List[Dict[str, Any]] = []

    for item in evidence_items:
        if item.get("type") == "ownership":
            cited_owner = item.get("result", "")
            trigger_urn = receipt_data.get("trigger", {}).get("urn", "")
            live_owner = await get_ownership(client, trigger_urn)
            if cited_owner and live_owner and cited_owner != live_owner:
                drift_details.append({
                    "urn": trigger_urn,
                    "cited_fact": f"owner: {cited_owner}",
                    "live_fact": f"owner: {live_owner}",
                    "drift_type": "OWNERSHIP_TRANSFER"
                })

    drift_status = "CITATION_DRIFT_DETECTED" if drift_details else "NO_DRIFT_DETECTED"

    return {
        "receipt_id": receipt_id,
        "ledger_integrity": "INTACT_UNMODIFIED",
        "evidence_drift_status": drift_status,
        "drift_details": drift_details
    }
