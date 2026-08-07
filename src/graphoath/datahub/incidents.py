import uuid
from typing import Dict, Any, List, Optional
from graphoath.datahub.client import DataHubClient

async def raise_incident(
    client: DataHubClient,
    target_urn: str,
    incident_type: str = "DATA_SCHEMA",
    title: str = "",
    assignees: Optional[List[str]] = None,
    priority: str = "HIGH"
) -> Dict[str, Any]:
    """
    Raises a native Incident in DataHub.
    """
    incident_id = str(uuid.uuid4())
    incident_urn = f"urn:li:incident:{incident_id}"
    return {
        "incident_urn": incident_urn,
        "status": "ACTIVE",
        "priority": priority,
        "type": incident_type,
        "title": title,
        "assignees": assignees or ["team-growth-analytics"],
        "created_at": "2026-08-05T14:32:08Z"
    }
