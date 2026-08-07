import pytest
from graphoath.datahub.client import DataHubClient
from graphoath.modules.deposition.evidence import gather_evidence

@pytest.mark.asyncio
async def test_gather_evidence():
    client = DataHubClient()
    trigger_info = {
        "event": "field_removed",
        "urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,ecommerce.fct_orders,PROD)",
        "field": "customer_region"
    }
    evidence = await gather_evidence(client, trigger_info)
    assert len(evidence) >= 3
    types = [item["type"] for item in evidence]
    assert "lineage" in types
    assert "ownership" in types
    assert "usage" in types
