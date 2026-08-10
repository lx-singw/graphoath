import time
from typing import Dict, Any, List, Set
from pydantic import BaseModel, Field
from fastapi import APIRouter, status
from graphoath.modules.deposition.gate import CitationGate
from graphoath.telemetry import TelemetryProvider

router = APIRouter(prefix="/gate", tags=["Citation Gate"])

class GateEvaluationRequest(BaseModel):
    agent_id: str = Field(..., example="deposition_agent_v1")
    action_type: str = Field(..., example="raiseIncident")
    claimed_urns: List[str] = Field(..., example=["urn:li:dataset:(snowflake,prod.orders)"])
    evidence_urns: List[str] = Field(..., example=["urn:li:dataset:(snowflake,prod.orders)"])

class GateEvaluationResponse(BaseModel):
    status: str  # APPROVED, REJECTED
    citation_resolution_rate: float
    verified_urns: List[str]
    missing_citations: List[str]
    latency_ms: float
    hash: str

@router.post("/evaluate", response_model=GateEvaluationResponse, status_code=status.HTTP_200_OK)
async def evaluate_citation_gate_endpoint(req: GateEvaluationRequest) -> Dict[str, Any]:
    """
    POST /api/v1/gate/evaluate
    
    Standalone zero-network Citation Gate evaluation API endpoint.
    Verifies that claimed URNs exist in evidence URN array in < 5.0 ms.
    """
    claimed_set = set(req.claimed_urns)
    evidence_set = set(req.evidence_urns)

    is_approved, missing, latency_ms = CitationGate.verify(claimed_set, evidence_set)
    resolution_rate = 1.0 if not claimed_set else (len(claimed_set - missing) / len(claimed_set))

    status_str = "APPROVED" if is_approved else "REJECTED"
    verified_urns = list(claimed_set - missing)

    # Emit telemetry trace span
    TelemetryProvider().create_span("CitationGate.Evaluate", {
        "module": "Deposition",
        "source_urn": req.claimed_urns[0] if req.claimed_urns else "",
        "gate_status": status_str,
        "resolution_rate": resolution_rate,
        "latency_ms": latency_ms
    })

    return {
        "status": status_str,
        "citation_resolution_rate": resolution_rate,
        "verified_urns": verified_urns,
        "missing_citations": list(missing),
        "latency_ms": round(latency_ms, 4),
        "hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    }
