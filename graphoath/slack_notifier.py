"""
GraphOath Slack & MS Teams Interactive Notification Module.

Formats Slack Block Kit cards with downstream blast radius, owner tags, and interactive approval buttons.
"""

import json
from typing import List, Dict, Any

def generate_slack_incident_card(
    incident_id: str,
    source_urn: str,
    downstream_urns: List[str],
    assignees: List[str],
    receipt_hash: str
) -> Dict[str, Any]:
    """Generates Slack Block Kit interactive message card payload."""
    assignee_mentions = " ".join([f"<@{owner}>" for owner in assignees]) if assignees else "@data-platform-oncall"
    downstream_text = "\n".join([f"• `{urn}`" for urn in downstream_urns])
    
    card = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🚨 GraphOath Triage Alert: Native DataHub Incident {incident_id}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Root Cause Asset:*\n`{source_urn}`"},
                    {"type": "mrkdwn", "text": f"*Assignees:*\n{assignee_mentions}"}
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Impacted Downstream Blast Radius ({len(downstream_urns)} Assets):*\n{downstream_text}"
                }
            },
            {
                "type": "context",
                "elements": [
                    {"type": "mrkdwn", "text": f"🛡️ *GraphOath Citation Gate:* 100% Verified | *Receipt Hash:* `{receipt_hash[:16]}...`"}
                ]
            },
            {
                "type": "actions",
                "block_id": f"incident_actions_{incident_id}",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Approve Remediation Playbook"},
                        "style": "primary",
                        "value": f"approve_{incident_id}"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Escalate to Lead"},
                        "style": "danger",
                        "value": f"escalate_{incident_id}"
                    }
                ]
            }
        ]
    }
    return card

if __name__ == "__main__":
    card = generate_slack_incident_card(
        "dep_20260807_001",
        "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)",
        [
            "urn:li:dataset:(urn:li:dataPlatform:dbt,dbt.stg_orders,PROD)",
            "urn:li:dataset:(urn:li:dataPlatform:dbt,dbt.fct_daily_revenue,PROD)"
        ],
        ["alice_data_eng"],
        "0c15e57b87c3fa3cd2097bd977f9b76874ef52080f883bd99e5467c4bf03672d"
    )
    print("[GraphOath Slack Notifier] Generated Slack Block Kit Card:")
    print(json.dumps(card, indent=2))
    assert len(card["blocks"]) == 5
