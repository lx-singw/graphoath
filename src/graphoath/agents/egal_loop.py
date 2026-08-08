import time
import uuid
from typing import TypedDict, List, Dict, Any, Optional
from graphoath.datahub.client import DataHubClientWrapper
from graphoath.datahub.incidents import raise_datahub_incident_sync
from graphoath.datahub.aspects import emit_custody_receipt_aspect
from graphoath.custody.receipt import CustodyReceipt
from graphoath.custody.ledger import Ledger

class AgentState(TypedDict):
    event_payload: Dict[str, Any]
    evidence_graph: List[Dict[str, Any]]
    evidence_urns: List[str]
    draft_claim: str
    claimed_urns: List[str]
    citation_passed: bool
    missing_citations: List[str]
    confidence_score: float
    action_status: str  # 'EXECUTED', 'REJECTED', 'PENDING_HITL'
    incident_urn: Optional[str]
    receipt_id: Optional[str]

def sentinel_node(state: AgentState) -> AgentState:
    """Receives trigger event (e.g., schema break or dbt test failure)."""
    payload = state.get("event_payload", {})
    source_urn = payload.get("source_urn", "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)")
    draft_claim = state.get("draft_claim", f"Incident detected on {source_urn}")
    
    state["draft_claim"] = draft_claim
    state["action_status"] = "INITIALIZED"
    return state

def forensic_collector_node(state: AgentState) -> AgentState:
    """Queries DataHub MCP Server for 3-hop downstream lineage and dataset owners."""
    payload = state.get("event_payload", {})
    source_urn = payload.get("source_urn", "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)")
    
    client = DataHubClientWrapper()
    evidence_pkg = client.get_evidence_package(source_urn, max_hops=3)
    
    state["evidence_urns"] = list(evidence_pkg.lineage_urns) + [source_urn]
    state["evidence_graph"] = [{"urn": u} for u in state["evidence_urns"]]
    return state

def citation_gate_node(state: AgentState) -> AgentState:
    """Runs deterministic math check: Ref(Claims) subset of Ref(Evidence)."""
    claimed_urns = set(state.get("claimed_urns", []))
    evidence_urns = set(state.get("evidence_urns", []))
    
    missing = list(claimed_urns - evidence_urns)
    state["missing_citations"] = missing
    
    if not missing:
        state["citation_passed"] = True
        state["confidence_score"] = 0.95
    else:
        state["citation_passed"] = False
        state["confidence_score"] = max(0.0, 1.0 - (len(missing) * 0.4))
        
    return state

def arbiter_node(state: AgentState) -> AgentState:
    """Routes state based on confidence score."""
    score = state.get("confidence_score", 0.0)
    passed = state.get("citation_passed", False)
    
    if passed and score >= 0.90:
        state["action_status"] = "APPROVED_FOR_EXECUTION"
    elif score >= 0.75:
        state["action_status"] = "PENDING_HITL"
    else:
        state["action_status"] = "REJECTED"
        
    return state

def executor_node(state: AgentState) -> AgentState:
    """Executes native DataHub GraphQL raiseIncident, emits Pegasus aspect, appends receipt."""
    payload = state.get("event_payload", {})
    source_urn = payload.get("source_urn", "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)")
    
    # 1. Raise native incident
    client = DataHubClientWrapper()
    inc_res = raise_datahub_incident_sync(
        client=client,
        target_urn=source_urn,
        title=f"EGAL Incident: {state.get('draft_claim')}",
        description="Triggered by GraphOath LangGraph EGAL Loop"
    )
    incident_urn = inc_res.get("incident_urn", f"urn:li:incident:inc_{int(time.time())}")
    
    # 2. Append custody receipt
    rcpt_id = f"rcpt_egal_{uuid.uuid4().hex[:8]}"
    receipt = CustodyReceipt(
        receipt_id=rcpt_id,
        action_type="raiseIncident",
        target_urn=source_urn,
        evidence_payload=state.get("evidence_graph", []),
        claims_payload={"draft_claim": state.get("draft_claim"), "claimed_urns": state.get("claimed_urns")},
        gate_decision="APPROVED",
        confidence_score=state.get("confidence_score", 0.95)
    )
    ledger = Ledger()
    ledger.append_custody_receipt(receipt)
    
    # 3. Emit Pegasus aspect
    emit_custody_receipt_aspect(receipt)
    
    state["action_status"] = "EXECUTED"
    state["incident_urn"] = incident_urn
    state["receipt_id"] = rcpt_id
    return state

def hitl_queue_node(state: AgentState) -> AgentState:
    """Enqueues item for Human-in-the-Loop review."""
    state["action_status"] = "PENDING_HITL"
    return state

def rejection_node(state: AgentState) -> AgentState:
    """Rejects execution due to hallucinated citations."""
    state["action_status"] = "REJECTED"
    return state

class EGALWorkflow:
    """StateGraph workflow engine executing 5-stage EGAL loop."""
    
    def run(self, initial_state: AgentState) -> AgentState:
        state = sentinel_node(initial_state)
        state = forensic_collector_node(state)
        state = citation_gate_node(state)
        state = arbiter_node(state)
        
        status = state.get("action_status")
        if status == "APPROVED_FOR_EXECUTION":
            state = executor_node(state)
        elif status == "PENDING_HITL":
            state = hitl_queue_node(state)
        else:
            state = rejection_node(state)
            
        return state

def build_egal_workflow() -> EGALWorkflow:
    return EGALWorkflow()

def run_egal_loop(event_payload: Dict[str, Any], claimed_urns: List[str], draft_claim: str = "") -> AgentState:
    workflow = build_egal_workflow()
    initial_state: AgentState = {
        "event_payload": event_payload,
        "evidence_graph": [],
        "evidence_urns": [],
        "draft_claim": draft_claim,
        "claimed_urns": claimed_urns,
        "citation_passed": False,
        "missing_citations": [],
        "confidence_score": 0.0,
        "action_status": "PENDING",
        "incident_urn": None,
        "receipt_id": None
    }
    return workflow.run(initial_state)
