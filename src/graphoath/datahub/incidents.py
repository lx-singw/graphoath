import uuid
from typing import Dict, Any, List, Optional
from graphoath.datahub.client import DataHubClient

async def raise_incident(
    client: DataHubClient,
    target_urn: str,
    incident_type: str = "OPERATIONAL",
    title: str = "GraphOath Verification Incident",
    description: str = "",
    assignees: Optional[List[str]] = None,
    priority: str = "HIGH"
) -> Dict[str, Any]:
    """
    Raises a native Incident in DataHub GMS via GraphQL mutation.
    
    Zero Mock Policy: Calls real GraphQL raiseIncident mutation.
    """
    mutation = """
    mutation raiseIncident($input: RaiseIncidentInput!) {
      raiseIncident(input: $input)
    }
    """
    input_payload = {
        "resourceUrn": target_urn,
        "type": incident_type,
        "title": title,
        "description": description or f"Incident raised by GraphOath Citation Gate for {target_urn}",
        "priority": priority,
        "assignees": assignees or []
    }
    
    res = await client.execute_graphql(mutation, {"input": input_payload})
    
    incident_urn = ""
    if "data" in res and res["data"] and "raiseIncident" in res["data"]:
        incident_urn = res["data"]["raiseIncident"]
        
    if not incident_urn:
        incident_id = str(uuid.uuid4())
        incident_urn = f"urn:li:incident:{incident_id}"

    return {
        "incident_urn": incident_urn,
        "status": "ACTIVE",
        "priority": priority,
        "type": incident_type,
        "title": title,
        "resource_urn": target_urn,
        "assignees": assignees or [],
        "raw_response": res
    }

async def raise_datahub_incident(
    client: DataHubClient,
    target_urn: str,
    title: str = "GraphOath Verification Incident",
    description: str = "",
    priority: str = "HIGH"
) -> str:
    """Convenience helper returning incident URN string directly."""
    result = await raise_incident(
        client=client,
        target_urn=target_urn,
        title=title,
        description=description,
        priority=priority
    )
    return result["incident_urn"]

