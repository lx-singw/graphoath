from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
from graphoath.api.schemas import (
    ReceiptsListResponse, ReceiptSummary, ReceiptDetailResponse,
    LedgerVerifyResponse, ExportRequest, ExportResponse
)
from graphoath.datahub.client import DataHubClient
from graphoath.custody.drift import verify_evidence_drift

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

@router.get("/receipts", response_model=ReceiptsListResponse)
async def list_receipts(
    urn: Optional[str] = None,
    module: Optional[str] = None,
    limit: int = Query(default=25, le=200)
):
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

@router.get("/receipts/{receipt_id}", response_model=ReceiptDetailResponse)
async def get_receipt(receipt_id: str):
    if receipt_id == MOCK_RECEIPT_DETAIL.receipt_id or receipt_id.startswith("rcpt_"):
        return MOCK_RECEIPT_DETAIL
    raise HTTPException(status_code=404, detail=f"Receipt '{receipt_id}' not found")

@router.get("/ledger/verify", response_model=LedgerVerifyResponse)
async def verify_ledger(from_receipt_id: Optional[str] = None, to_receipt_id: Optional[str] = None):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return LedgerVerifyResponse(
        status="intact",
        receipts_checked=1,
        checked_at=now
    )

@router.post("/receipts/verify-drift")
async def verify_drift(receipt_id: str):
    client = DataHubClient()
    detail = MOCK_RECEIPT_DETAIL.dict()
    detail["receipt_id"] = receipt_id
    res = await verify_evidence_drift(client, detail)
    return res

@router.post("/exports", response_model=ExportResponse, status_code=201)
async def create_export(body: ExportRequest):
    return ExportResponse(
        export_id="exp_4b8d2f1a",
        status="processing",
        requested_by="usr_3f7a9c",
        estimated_completion_seconds=12
    )

