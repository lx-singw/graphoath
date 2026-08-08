from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from graphoath.datahub.client import DataHubClient

@dataclass
class EvidencePackage:
    source_urn: str
    direction: str
    max_hops: int
    entities: List[Dict[str, Any]] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)

async def search_across_lineage(
    client: DataHubClient,
    urn: str,
    direction: str = "DOWNSTREAM",
    degree: int = 3
) -> List[Dict[str, Any]]:
    """
    Queries DataHub GraphQL for lineage relations down to degree N.
    Returns list of dicts with result_urn, entity_type, and hops count.
    
    Zero Mock Policy: Does NOT return hardcoded fallbacks if no lineage exists.
    """
    query = """
    query searchAcrossLineage($urn: String!, $direction: LineageDirection!, $degree: Int!) {
      searchAcrossLineage(input: {urn: $urn, direction: $direction, maxHops: $degree}) {
        searchResults {
          entity {
            urn
            type
          }
          degree
        }
      }
    }
    """
    res = await client.execute_graphql(query, {"urn": urn, "direction": direction, "degree": degree})
    results = []

    if "data" in res and res["data"] and "searchAcrossLineage" in res["data"]:
        search_results = res["data"]["searchAcrossLineage"] or {}
        for item in search_results.get("searchResults", []):
            entity = item.get("entity", {})
            entity_urn = entity.get("urn")
            entity_type = entity.get("type", "DATASET")
            hops = item.get("degree", 1)
            if entity_urn:
                results.append({
                    "result_urn": entity_urn,
                    "entity_type": entity_type,
                    "hops": hops
                })

    return results

async def get_evidence_package(
    client: DataHubClient,
    urn: str,
    direction: str = "DOWNSTREAM",
    degree: int = 3
) -> EvidencePackage:
    """Fetches an EvidencePackage containing live DataHub lineage evidence."""
    raw = await client.execute_graphql(
        """
        query searchAcrossLineage($urn: String!, $direction: LineageDirection!, $degree: Int!) {
          searchAcrossLineage(input: {urn: $urn, direction: $direction, maxHops: $degree}) {
            searchResults {
              entity {
                urn
                type
              }
              degree
            }
          }
        }
        """,
        {"urn": urn, "direction": direction, "degree": degree}
    )
    
    entities = []
    if "data" in raw and raw["data"] and "searchAcrossLineage" in raw["data"]:
        search_results = raw["data"]["searchAcrossLineage"] or {}
        for item in search_results.get("searchResults", []):
            entity = item.get("entity", {})
            if entity.get("urn"):
                entities.append({
                    "urn": entity.get("urn"),
                    "type": entity.get("type", "DATASET"),
                    "hops": item.get("degree", 1)
                })

    return EvidencePackage(
        source_urn=urn,
        direction=direction,
        max_hops=degree,
        entities=entities,
        raw_response=raw
    )

