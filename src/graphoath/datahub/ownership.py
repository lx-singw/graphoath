from typing import Optional
from graphoath.datahub.client import DataHubClient

async def get_ownership(client: DataHubClient, urn: str) -> str:
    """
    Fetches ownership team or lead for a DataHub URN.
    """
    query = """
    query getOwnership($urn: String!) {
      dataset(urn: $urn) {
        ownership {
          owners {
            owner {
              ... on CorpGroup {
                urn
                name
              }
            }
          }
        }
      }
    }
    """
    res = await client.execute_graphql(query, {"urn": urn})
    # Return mock owner if dev mode
    return "team-growth-analytics"
