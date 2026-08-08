import pytest
from unittest.mock import AsyncMock
from graphoath.datahub.client import DataHubClient
from graphoath.datahub.tags import add_trust_tag, add_tag

@pytest.mark.asyncio
async def test_add_trust_tag():
    mock_client = AsyncMock(spec=DataHubClient)
    mock_client.execute_graphql.return_value = {"data": {"addTag": True}}

    res = await add_trust_tag(mock_client, "urn:li:dataset:prod_orders")
    assert res["status"] == "TAG_ASSOCIATED"
    assert res["tagUrn"] == "urn:li:tag:GRAPH_OATH_VERIFIED"
    assert res["resourceUrn"] == "urn:li:dataset:prod_orders"

@pytest.mark.asyncio
async def test_add_tag_custom():
    mock_client = AsyncMock(spec=DataHubClient)
    mock_client.execute_graphql.return_value = {"data": {"addTag": True}}

    res = await add_tag(mock_client, "urn:li:dataset:prod_orders", tag_urn="urn:li:tag:CustomTag")
    assert res["tagUrn"] == "urn:li:tag:CustomTag"
