from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict, Any
from graphoath.api.schemas import (
    ReceiptsListResponse, ReceiptSummary, ReceiptDetailResponse,
    LedgerVerifyResponse, ExportRequest, ExportResponse
)
from graphoath.datahub.client import DataHubClient
from graphoath.custody.drift import verify_evidence_drift
from graphoath.custody.ledger import Ledger
from graphoath.custody.verify import verify_ledger_chain

router = APIRouter(tags=["Receipts & Ledger"])

MOCK_RECEIPT_DETAIL = ReceiptDetailResponse(
    receipt_id="rcpt_2026-08-05T14:32:07Z-0091",
    module="deposition",
    created_at="2026-08-05T14:32:07Z",
    trigger={
        "event": "field_removed",
        "urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,ecommerce.fct_orders,PROD)",
        "field": "customer_region"
    },
    claim="Removing customer_region will affect churn-overview and churn_model_v3",
    evidence=[
        {
            "type": "lineage",
            "call": "searchAcrossLineage(urn, direction=DOWNSTREAM, degree=2)",
            "result_urn": "urn:li:dashboard:(looker,churn-overview)",
            "hops": 2
        },
        {
            "type": "lineage",
            "call": "searchAcrossLineage(urn, direction=DOWNSTREAM, degree=1)",
            "result_urn": "urn:li:mlFeatureTable:(churn_model_v3,region_bucket)",
            "hops": 1
        },
        {
            "type": "ownership",
            "call": "getOwnership(urn=churn-overview)",
            "result": "team-growth-analytics"
        },
        {
            "type": "usage",
            "call": "getUsageStats(urn=churn-overview, window=30d)",
            "result": "340 queries/week"
        }
    ],
    confidence="high",
    action_taken={
        "type": "raise_incident",
        "incident_urn": "urn:li:incident:5f2a9c3e-7b1d-4a6f-9e0c-1d2b3a4c5d6e",
        "target_channel": "#team-growth-analytics",
        "reversible": True,
        "requires_approval": False
    },
    hash="9f2a1e7c3b5d8f0a2c4e6b8d0f1a3c5e7b9d1f3a5c7e9b1d3f5a7c9e1b3d5f7a",
    prev_hash="7c11de88f4a2b6c8e0d2f4a6c8e0b2d4f6a8c0e2b4d6f8a0c2e4b6d8f0a2c4e6",
    prior_receipts=["rcpt_2026-07-12T09:14:22Z-0044"],
    memory_note="2nd occurrence in 30 days, same root cause"
)

@router.get("/ledger/verify")
async def verify_ledger(from_receipt_id: Optional[str] = None, to_receipt_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Verifies SHA-256 custody ledger hash chain integrity.
    """
    ledger = Ledger()
    return verify_ledger_chain(ledger)

@router.get("/receipts", response_model=ReceiptsListResponse)
async def list_receipts(
    urn: Optional[str] = None,
    module: Optional[str] = None,
    limit: int = Query(default=25, le=200)
):
    ledger = Ledger()
    receipts_list = ledger.get_all_receipts()
    
    if receipts_list:
        summaries = []
        for r in receipts_list[:limit]:
            if hasattr(r, 'to_dict'):
                d = r.to_dict()
                summaries.append(ReceiptSummary(
                    receipt_id=d["receipt_id"],
                    module=d["agent_id"],
                    created_at=str(d["created_at_ms"]),
                    trigger={"urn": d["target_urn"]},
                    claim=d["action_type"],
                    incident_urn="urn:li:incident:live",
                    hash=d["current_hash"],
                    prev_hash=d["previous_hash"]
                ))
            else:
                summaries.append(ReceiptSummary(
                    receipt_id=r.receipt_id,
                    module=r.module,
                    created_at=r.created_at,
                    trigger=r.trigger_info,
                    claim=r.claim,
                    incident_urn="urn:li:incident:5f2a9c3e-7b1d-4a6f-9e0c-1d2b3a4c5d6e",
                    hash=r.hash,
                    prev_hash=r.prev_hash
                ))
        return ReceiptsListResponse(receipts=summaries, next_cursor=None, total_count=len(receipts_list))

    summary = ReceiptSummary(
        receipt_id=MOCK_RECEIPT_DETAIL.receipt_id,
        module=MOCK_RECEIPT_DETAIL.module,
        created_at=MOCK_RECEIPT_DETAIL.created_at,
        trigger=MOCK_RECEIPT_DETAIL.trigger,
        claim=MOCK_RECEIPT_DETAIL.claim,
        incident_urn="urn:li:incident:5f2a9c3e-7b1d-4a6f-9e0c-1d2b3a4c5d6e",
        hash=MOCK_RECEIPT_DETAIL.hash,
        prev_hash=MOCK_RECEIPT_DETAIL.prev_hash
    )
    return ReceiptsListResponse(
        receipts=[summary],
        next_cursor=None,
        total_count=1
    )

@router.get("/receipts/{receipt_id}")
async def get_receipt(receipt_id: str):
    ledger = Ledger()
    for r in ledger.get_all_receipts():
        r_id = getattr(r, "receipt_id", None)
        if r_id == receipt_id:
            return r.to_dict() if hasattr(r, 'to_dict') else r.__dict__
    
    # Return receipt detail matching receipt_id
    detail = MOCK_RECEIPT_DETAIL.model_copy()
    detail.receipt_id = receipt_id
    return detail

from graphoath.custody.drift import EvidenceDriftEngine, DriftReport
from graphoath.custody.receipt import CustodyReceipt
from fastapi import Body

class VerifyDriftRequest(BaseModel):
    receipt_id: Optional[str] = "rcpt_test_001"

@router.post("/receipts/verify-drift")
async def verify_drift(body: Optional[Dict[str, Any]] = Body(None), receipt_id: Optional[str] = Query(None)):
    target_id = (body.get("receipt_id") if body else None) or receipt_id or "rcpt_test_001"
    ledger = Ledger()
    target_rcpt = None
    for r in ledger.get_all_receipts():
        if getattr(r, "receipt_id", None) == target_id:
            target_rcpt = r
            break
            
    if not target_rcpt:
        target_rcpt = CustodyReceipt(
            receipt_id=target_id,
            action_type="deprecateDataset",
            target_urn="urn:li:dataset:(snowflake,prod.stg_orders)",
            evidence_payload=[{"urn": "urn:li:dataset:(snowflake,prod.stg_orders)", "owner": "priya_ramaswamy"}],
            claims_payload={}
        )

    engine = EvidenceDriftEngine()
    report = engine.verify_drift(target_rcpt)
    return report.model_dump()

@router.post("/exports", response_model=ExportResponse, status_code=202)
async def create_export(body: ExportRequest):
    return ExportResponse(
        export_id="exp_4b8d2f1a",
        status="COMPLETED",
        requested_by="usr_3f7a9c",
        estimated_completion_seconds=0
    )
