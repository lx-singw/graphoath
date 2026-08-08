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


