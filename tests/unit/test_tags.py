import pytest
from graphoath.datahub.client import DataHubClient
from graphoath.datahub.tags import add_trust_tag

@pytest.mark.asyncio
async def test_add_trust_tag():
    client = DataHubClient()
    resource_urn = "urn:li:dataset:(snowflake,prod.stg_orders,PROD)"
    result = await add_trust_tag(client, resource_urn)
    assert result["tagUrn"] == "urn:li:tag:GRAPH_OATH_VERIFIED"
    assert result["status"] == "TAG_ASSOCIATED"
