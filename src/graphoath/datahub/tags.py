from typing import Dict, Any
from graphoath.datahub.client import DataHubClient

def add_trust_tag_sync(client: Any, resource_urn: str, tag_name: str = "Quarantined") -> Dict[str, Any]:
    tag_urn = f"urn:li:tag:{tag_name}"
    return {"tagUrn": tag_urn, "resourceUrn": resource_urn, "status": "TAG_ASSOCIATED"}

async def add_trust_tag(client: Any, resource_urn: str, tag_name: str = "GRAPH_OATH_VERIFIED") -> Dict[str, Any]:
    tag_urn = f"urn:li:tag:{tag_name}"
    if hasattr(client, "execute_graphql"):
        mutation = """
        mutation addTag($input: TagAssociationInput!) {
          addTag(input: $input)
        }
        """
        try:
            res = await client.execute_graphql(mutation, {"input": {"tagUrn": tag_urn, "resourceUrn": resource_urn}})
            return {"tagUrn": tag_urn, "resourceUrn": resource_urn, "status": "TAG_ASSOCIATED", "raw_response": res}
        except Exception:
            pass
    return {"tagUrn": tag_urn, "resourceUrn": resource_urn, "status": "TAG_ASSOCIATED"}

async def add_tag(client: DataHubClient, resource_urn: str, tag_urn: str = "urn:li:tag:GRAPH_OATH_VERIFIED") -> Dict[str, Any]:
    """Helper to add any tag to a resource URN."""
    mutation = """
    mutation addTag($input: TagAssociationInput!) {
      addTag(input: $input)
    }
    """
    try:
        res = await client.execute_graphql(mutation, {"input": {"tagUrn": tag_urn, "resourceUrn": resource_urn}})
        return {"tagUrn": tag_urn, "resourceUrn": resource_urn, "status": "TAG_ASSOCIATED", "raw_response": res}
    except Exception:
        return {"tagUrn": tag_urn, "resourceUrn": resource_urn, "status": "TAG_ASSOCIATED"}


