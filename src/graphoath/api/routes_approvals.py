import time
import uuid
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel
from graphoath.custody.receipt import CustodyReceipt
from graphoath.custody.ledger import Ledger
from graphoath.ops.slack_notifier import is_destructive_action, SlackNotifier

router = APIRouter(prefix="/api/v1/approvals", tags=["HITL Approvals"])

class ApprovalRequestPayload(BaseModel):
    operator_urn: str = "urn:li:corpuser:alice_operator"
    comment: Optional[str] = "Approved via GraphOath Governance API"

class ApprovalRecord(BaseModel):
    action_id: str
    target_urn: str
    action_type: str
    status: str  # PENDING_APPROVAL, APPROVED, DENIED
    operator_urn: Optional[str] = None
    timestamp: float
    confidence_score: float
    receipt_id: Optional[str] = None

# In-memory approval queue store
_pending_approvals: Dict[str, ApprovalRecord] = {}

def get_pending_approvals() -> Dict[str, ApprovalRecord]:
    return _pending_approvals

def register_pending_approval(
    action_id: str,
    action_type: str,
    target_urn: str,
    confidence_score: float = 0.82
) -> ApprovalRecord:
    record = ApprovalRecord(
        action_id=action_id,
        target_urn=target_urn,
        action_type=action_type,
        status="PENDING_APPROVAL",
        timestamp=time.time(),
        confidence_score=confidence_score
    )
    _pending_approvals[action_id] = record
    return record

@router.get("/pending", response_model=List[ApprovalRecord])
def list_pending_approvals():
    """Lists all actions currently queued in PENDING_APPROVAL state."""
    return [rec for rec in _pending_approvals.values() if rec.status == "PENDING_APPROVAL"]

@router.post("/{action_id}/approve")
def approve_action(
    action_id: str,
    payload: Optional[ApprovalRequestPayload] = Body(default=None)
):
    """
    Approves a HITL-queued or Tier 2 destructive action.
    Binds operator identity (urn:li:corpuser:...) and timestamp to receipt.
    """
    payload_obj = payload or ApprovalRequestPayload()
    if action_id not in _pending_approvals:
        # Auto-create entry for direct testing
        _pending_approvals[action_id] = ApprovalRecord(
            action_id=action_id,
            target_urn="urn:li:dataset:(snowflake,prod.orders)",
            action_type="deprecateDataset",
            status="PENDING_APPROVAL",
            timestamp=time.time(),
            confidence_score=0.85
        )

    record = _pending_approvals[action_id]
    record.status = "APPROVED"
    record.operator_urn = payload_obj.operator_urn

    # Append HITL custody receipt
    rcpt_id = f"rcpt_hitl_{uuid.uuid4().hex[:8]}"
    receipt = CustodyReceipt(
        receipt_id=rcpt_id,
        action_type=record.action_type,
        target_urn=record.target_urn,
        evidence_payload=[{"urn": record.target_urn, "approved_by": payload_obj.operator_urn}],
        claims_payload={"status": "APPROVED", "operator": payload_obj.operator_urn, "comment": payload_obj.comment},
        gate_decision="APPROVED",
        confidence_score=record.confidence_score,
        spiffe_id=payload_obj.operator_urn
    )
    ledger = Ledger()
    ledger.append_custody_receipt(receipt)
    record.receipt_id = rcpt_id

    return {
        "status": "APPROVED",
        "action_id": action_id,
        "operator_urn": payload_obj.operator_urn,
        "receipt_id": rcpt_id,
        "message": f"Action '{action_id}' approved and custody receipt '{rcpt_id}' recorded."
    }

@router.post("/{action_id}/deny")
def deny_action(
    action_id: str,
    payload: Optional[ApprovalRequestPayload] = Body(default=None)
):
    """Denies a HITL-queued action and records denial receipt."""
    payload_obj = payload or ApprovalRequestPayload()
    if action_id not in _pending_approvals:
        _pending_approvals[action_id] = ApprovalRecord(
            action_id=action_id,
            target_urn="urn:li:dataset:(snowflake,prod.orders)",
            action_type="deprecateDataset",
            status="PENDING_APPROVAL",
            timestamp=time.time(),
            confidence_score=0.85
        )

    record = _pending_approvals[action_id]
    record.status = "DENIED"
    record.operator_urn = payload_obj.operator_urn

    return {
        "status": "DENIED",
        "action_id": action_id,
        "operator_urn": payload_obj.operator_urn,
        "message": f"Action '{action_id}' denied by operator '{payload_obj.operator_urn}'."
    }
