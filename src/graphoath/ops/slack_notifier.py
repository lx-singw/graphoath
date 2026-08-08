import json
import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

TIER1_NON_DESTRUCTIVE_ACTIONS = {
    "raiseIncident", "updateIncident", "emitAspect", "addTag", "quarantineDataset"
}

TIER2_DESTRUCTIVE_ACTIONS = {
    "deprecateDataset", "dropColumn", "deleteTag", "grantAccessRole", "revokeAccess"
}

def is_destructive_action(action_name: str) -> bool:
    return action_name in TIER2_DESTRUCTIVE_ACTIONS

class SlackCardPayload(BaseModel):
    action_id: str
    target_urn: str
    action_type: str
    agent_id: str
    confidence_score: float
    claim_text: str
    block_kit_payload: Dict[str, Any]

class SlackNotifier:
    """
    Generates Slack Block Kit interactive message cards for Human-in-the-Loop (HITL) approvals.
    """
    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url

    def build_approval_card(
        self,
        action_id: str,
        action_type: str,
        target_urn: str,
        agent_id: str = "agent_deposition_v1",
        confidence_score: float = 0.82,
        claim_text: str = "Proposed action requires human oversight."
    ) -> SlackCardPayload:
        risk_level = "HIGH (DESTRUCTIVE)" if is_destructive_action(action_type) else "MEDIUM (HITL QUEUED)"
        
        block_kit = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"🛡️ GraphOath Governance Approval Request [{action_type}]",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Action ID:*\n`{action_id}`"},
                        {"type": "mrkdwn", "text": f"*Risk Level:*\n`{risk_level}`"},
                        {"type": "mrkdwn", "text": f"*Target URN:*\n`{target_urn}`"},
                        {"type": "mrkdwn", "text": f"*Agent Identity:*\n`{agent_id}`"},
                        {"type": "mrkdwn", "text": f"*Confidence Score:*\n`{confidence_score:.2f}`"}
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Proposed Claim / Impact:*\n>{claim_text}"
                    }
                },
                {"type": "divider"},
                {
                    "type": "actions",
                    "block_id": f"approval_actions_{action_id}",
                    "elements": [
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Approve Action", "emoji": True},
                            "style": "primary",
                            "value": f"approve:{action_id}",
                            "action_id": "approve_button"
                        },
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Deny Action", "emoji": True},
                            "style": "danger",
                            "value": f"deny:{action_id}",
                            "action_id": "deny_button"
                        }
                    ]
                }
            ]
        }

        return SlackCardPayload(
            action_id=action_id,
            target_urn=target_urn,
            action_type=action_type,
            agent_id=agent_id,
            confidence_score=confidence_score,
            claim_text=claim_text,
            block_kit_payload=block_kit
        )
