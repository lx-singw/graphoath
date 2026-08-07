from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from typing import Optional
from graphoath.api.schemas import (
    IncidentResponse, ApprovalRequest, DenialRequest, ApprovalResponse
)

router = APIRouter(tags=["Incidents & Approvals"])

@router.get("/incidents/{incident_urn:path}", response_model=IncidentResponse)
async def get_incident(incident_urn: str):
    return IncidentResponse(
        incident_urn=incident_urn,
        status="ACTIVE",
        priority="HIGH",
        type="DATA_SCHEMA",
        assignees=["team-growth-analytics"],
        created_at="2026-08-05T14:32:08Z",
        linked_receipts=["rcpt_2026-08-05T14:32:07Z-0091"]
    )

@router.post("/approvals/{action_id}/approve", response_model=ApprovalResponse)
async def approve_action(action_id: str, body: ApprovalRequest):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return ApprovalResponse(
        action_id=action_id,
        status="approved",
        approved_by="usr_3f7a9c",
        approved_at=now,
        receipt_id="rcpt_2026-08-05T15:02:12Z-0092"
    )

@router.post("/approvals/{action_id}/deny", response_model=ApprovalResponse)
async def deny_action(action_id: str, body: DenialRequest):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return ApprovalResponse(
        action_id=action_id,
        status="denied",
        approved_by="usr_3f7a9c",
        approved_at=now
    )
