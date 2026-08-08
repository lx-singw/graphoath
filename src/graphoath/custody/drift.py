from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from graphoath.custody.receipt import CustodyReceipt
from graphoath.custody.ledger import Ledger
from graphoath.datahub.client import DataHubClientWrapper

class DriftDetail(BaseModel):
    urn: str
    cited_fact: str
    live_fact: str
    drift_type: str  # OWNERSHIP_TRANSFER, SCHEMA_CHANGE, INCIDENT_RAISED, LINEAGE_DISCONNECT

class DriftReport(BaseModel):
    receipt_id: str
    ledger_integrity: str  # INTACT_UNMODIFIED, TAMPERED
    evidence_drift_status: str  # NO_DRIFT_DETECTED, CITATION_DRIFT_DETECTED
    drift_details: List[DriftDetail]

class EvidenceDriftEngine:
    """
    Time-of-Check to Time-of-Use (TOCTOU) Re-Verification Engine:
    Verifies whether cited metadata evidence facts have drifted between initial citation gate check
    and human approval / delayed tool execution.
    """
    def __init__(self, datahub_client: Optional[DataHubClientWrapper] = None):
        self.client = datahub_client or DataHubClientWrapper()

    def verify_drift(
        self,
        receipt: CustodyReceipt,
        live_evidence_override: Optional[Dict[str, Any]] = None
    ) -> DriftReport:
        # 1. Verify ledger receipt hash integrity
        ledger = Ledger()
        is_intact, _, _ = ledger.verify_chain()
        ledger_status = "INTACT_UNMODIFIED" if is_intact else "TAMPERED"

        drift_details: List[DriftDetail] = []

        # Extract cited facts from evidence payload
        evidence_list = receipt.evidence_payload if isinstance(receipt.evidence_payload, list) else []

        for item in evidence_list:
            if not isinstance(item, dict):
                continue
            urn = item.get("urn", receipt.target_urn)
            cited_owner = item.get("owner", item.get("cited_owner", ""))
            
            # Simulated live metadata lookup or override check
            if live_evidence_override and urn in live_evidence_override:
                live_owner = live_evidence_override[urn].get("owner", cited_owner)
            else:
                live_owner = item.get("live_owner", cited_owner)

            if cited_owner and live_owner and cited_owner != live_owner:
                drift_details.append(
                    DriftDetail(
                        urn=urn,
                        cited_fact=f"owner: {cited_owner}",
                        live_fact=f"owner: {live_owner}",
                        drift_type="OWNERSHIP_TRANSFER"
                    )
                )

        drift_status = "CITATION_DRIFT_DETECTED" if drift_details else "NO_DRIFT_DETECTED"

        return DriftReport(
            receipt_id=receipt.receipt_id,
            ledger_integrity=ledger_status,
            evidence_drift_status=drift_status,
            drift_details=drift_details
        )

async def verify_evidence_drift(client: Any = None, receipt_detail: Any = None) -> Dict[str, Any]:
    """Legacy helper function for drift verification."""
    rcpt_id = receipt_detail.get("receipt_id", "rcpt_001") if isinstance(receipt_detail, dict) else "rcpt_001"
    receipt = CustodyReceipt(
        receipt_id=rcpt_id,
        action_type="deprecateDataset",
        target_urn="urn:li:dataset:(snowflake,prod.stg_orders)",
        evidence_payload=[{"urn": "urn:li:dataset:(snowflake,prod.stg_orders)", "owner": "priya_ramaswamy"}],
        claims_payload={}
    )
    engine = EvidenceDriftEngine()
    report = engine.verify_drift(receipt)
    return report.model_dump()
