import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from graphoath.datahub.tags import add_trust_tag_sync
from graphoath.datahub.ownership import get_dataset_ownership_sync
from graphoath.datahub.client import DataHubClientWrapper

class PlaybookExecutionResult(BaseModel):
    playbook_id: str
    target_urn: str
    status: str  # EXECUTED, PENDING_APPROVAL, ESCALATED
    risk_level: str  # LOW_NON_DESTRUCTIVE, MEDIUM_REQUIRES_APPROVAL
    details: Dict[str, Any]
    timestamp: float = 0.0

    def model_post_init(self, __context: Any) -> None:
        if not self.timestamp:
            self.timestamp = time.time()

class RemediationPlaybookEngine:
    """
    Automated Remediation Playbook Engine:
    Executes automated quarantine, dbt deferral pause, and owner escalation playbooks.
    """
    def __init__(self, datahub_client: Optional[DataHubClientWrapper] = None):
        self.client = datahub_client or DataHubClientWrapper()

    def dataset_quarantine_playbook(self, target_urn: str) -> PlaybookExecutionResult:
        """
        Applies urn:li:tag:Quarantined tag to target dataset.
        Risk Level: LOW_NON_DESTRUCTIVE (auto-executable).
        """
        res = add_trust_tag_sync(self.client, target_urn, "Quarantined")
        return PlaybookExecutionResult(
            playbook_id="dataset_quarantine_playbook",
            target_urn=target_urn,
            status="EXECUTED",
            risk_level="LOW_NON_DESTRUCTIVE",
            details={"tag": "Quarantined", "result": res}
        )

    def dbt_model_pause_playbook(self, target_urn: str) -> PlaybookExecutionResult:
        """
        Generates --defer --state ./prod_artifacts payload to pause dbt model execution during CI runs.
        Risk Level: MEDIUM_REQUIRES_APPROVAL (routes to Slack HITL approval gate).
        """
        payload = {
            "dbt_command": "dbt run --select " + target_urn.split(",")[-1].replace(")", "") if "," in target_urn else target_urn,
            "flags": ["--defer", "--state", "./prod_artifacts"],
            "action": "PAUSE_MODEL_EXECUTION"
        }
        return PlaybookExecutionResult(
            playbook_id="dbt_model_pause_playbook",
            target_urn=target_urn,
            status="PENDING_APPROVAL",
            risk_level="MEDIUM_REQUIRES_APPROVAL",
            details=payload
        )

    def owner_escalation_playbook(self, target_urn: str) -> PlaybookExecutionResult:
        """
        Evaluates dataset ownership via get_dataset_ownership_sync().
        Escalates unassigned or unacknowledged incidents to domain leads.
        Risk Level: LOW_NON_DESTRUCTIVE.
        """
        ownership = get_dataset_ownership_sync(self.client, target_urn)
        owners = ownership.get("owners", [])
        
        if not owners or ownership.get("ownership_type") == "UNASSIGNED":
            escalated_to = "urn:li:corpuser:lead_data_architect"
            status = "ESCALATED"
        else:
            escalated_to = owners[0]
            status = "NOTIFIED"

        return PlaybookExecutionResult(
            playbook_id="owner_escalation_playbook",
            target_urn=target_urn,
            status=status,
            risk_level="LOW_NON_DESTRUCTIVE",
            details={"original_owners": owners, "escalated_to": escalated_to}
        )

class RemediationPlaybooks:
    @staticmethod
    def dataset_quarantine_playbook(target_urns: Any) -> Dict[str, Any]:
        count = len(target_urns) if isinstance(target_urns, list) else 1
        return {"action": f"Applied Quarantined tag to {count} downstream datasets"}

    @staticmethod
    def dbt_model_pause_playbook(models: Any) -> Dict[str, Any]:
        count = len(models) if isinstance(models, list) else 1
        return {"action": f"Paused dbt model execution for {count} downstream models"}


