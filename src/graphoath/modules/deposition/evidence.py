from typing import List, Dict, Any
from graphoath.datahub.client import DataHubClient
from graphoath.datahub.lineage import search_across_lineage
from graphoath.datahub.ownership import get_ownership
from graphoath.datahub.usage import get_usage_stats

async def gather_evidence(client: DataHubClient, trigger_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    urn = trigger_info.get("urn", "")
    lineage_items = await search_across_lineage(client, urn, direction="DOWNSTREAM", degree=2)

    evidence = []
    for item in lineage_items:
        res_urn = item.get("result_urn")
        hops = item.get("hops", 1)
        evidence.append({
            "type": "lineage",
            "call": f"searchAcrossLineage(urn, direction=DOWNSTREAM, degree={hops})",
            "result_urn": res_urn,
            "hops": hops
        })

    owner = await get_ownership(client, urn)
    evidence.append({
        "type": "ownership",
        "call": f"getOwnership(urn={urn})",
        "result": owner
    })

    usage = await get_usage_stats(client, urn, window="30d")
    evidence.append({
        "type": "usage",
        "call": f"getUsageStats(urn={urn}, window=30d)",
        "result": usage
    })

    return evidence
