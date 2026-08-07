from typing import Dict, Any
from graphoath.datahub.client import DataHubClient

async def add_trust_tag(client: DataHubClient, resource_urn: str) -> Dict[str, Any]:
    """
    Executes DataHub native addTag mutation attaching GRAPH_OATH_VERIFIED tag.
    """
    mutation = """
    mutation addGraphOathTrustTag($input: TagAssociationInput!) {
      addTag(input: $input)
    }
    """
    variables = {
        "input": {
            "tagUrn": "urn:li:tag:GRAPH_OATH_VERIFIED",
            "resourceUrn": resource_urn
        }
    }
    res = await client.execute_graphql(mutation, variables)
    return {
        "tagUrn": "urn:li:tag:GRAPH_OATH_VERIFIED",
        "resourceUrn": resource_urn,
        "status": "TAG_ASSOCIATED",
        "raw_response": res
    }
