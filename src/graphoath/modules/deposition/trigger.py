import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from graphoath.agents.egal_loop import run_egal_loop, AgentState
from graphoath.datahub.incidents import raise_datahub_incident_sync
from graphoath.datahub.client import DataHubClientWrapper

class AssertionRunEvent(BaseModel):
    event_type: str = "AssertionRunEvent_v1"
    assertion_urn: str
    dataset_urn: str
    status: str  # FAILURE, SUCCESS
    failure_type: str = "ROW_COUNT_ZERO"
    timestamp: float = 0.0

    def model_post_init(self, __context: Any) -> None:
        if not self.timestamp:
            self.timestamp = time.time()

class AssertionTriggerListener:
    """
    Assertion-Triggered Incident Listener:
    Ingests DataHub assertion failure events (dbt, Great Expectations, Soda) and triggers
    Citation-Gated EGAL Deposition loop and native DataHub incident creation.
    """
    def __init__(self, datahub_client: Optional[DataHubClientWrapper] = None):
        self.client = datahub_client or DataHubClientWrapper()

    def process_assertion_event(self, event_payload: Dict[str, Any]) -> Dict[str, Any]:
        event = AssertionRunEvent(**event_payload)
        
        if event.status.upper() != "FAILURE":
            return {"status": "IGNORED", "reason": f"Event status is {event.status}"}

        # 1. Run EGAL deposition loop
        claimed_urns = [event.dataset_urn]
        draft_claim = f"Data Quality Assertion Failure: {event.failure_type} on {event.assertion_urn}"
        
        egal_payload = {
            "source_urn": event.dataset_urn,
            "event_type": event.event_type,
            "failure_type": event.failure_type,
            "assertion_urn": event.assertion_urn
        }

        egal_state: AgentState = run_egal_loop(
            event_payload=egal_payload,
            claimed_urns=claimed_urns,
            draft_claim=draft_claim
        )

        # 2. Raise DataHub Incident with DATA_QUALITY type
        title = f"DATA_QUALITY Failure: {event.failure_type} on {event.dataset_urn}"
        description = (
            f"GraphOath Assertion Monitor triggered for assertion '{event.assertion_urn}'. "
            f"Failure Type: {event.failure_type}. Downstream lineage verified: {len(egal_state.get('evidence_urns', []))} URNs."
        )

        inc_res = raise_datahub_incident_sync(
            client=self.client,
            target_urn=event.dataset_urn,
            title=title,
            description=description,
            priority="HIGH"
        )

        return {
            "status": "INCIDENT_RAISED",
            "dataset_urn": event.dataset_urn,
            "assertion_urn": event.assertion_urn,
            "incident_urn": inc_res.get("incident_urn"),
            "egal_action_status": egal_state.get("action_status"),
            "evidence_count": len(egal_state.get("evidence_urns", []))
        }
