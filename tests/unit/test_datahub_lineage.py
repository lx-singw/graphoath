import pytest
from unittest.mock import AsyncMock
from graphoath.datahub.client import DataHubClient
from graphoath.datahub.lineage import search_across_lineage, get_evidence_package

@pytest.mark.asyncio
async def test_search_across_lineage_parsing():
    mock_client = AsyncMock(spec=DataHubClient)
    mock_client.execute_graphql.return_value = {
        "data": {
            "searchAcrossLineage": {
                "searchResults": [
                    {
                        "entity": {"urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)", "type": "DATASET"},
                        "degree": 1
                    },
                    {
                        "entity": {"urn": "urn:li:dashboard:(looker,revenue)", "type": "DASHBOARD"},
                        "degree": 2
                    }
                ]
            }
        }
    }

    results = await search_across_lineage(mock_client, "urn:li:dataset:upstream", direction="DOWNSTREAM", degree=3)
    assert len(results) == 2
    assert results[0]["result_urn"] == "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)"
    assert results[0]["hops"] == 1
    assert results[1]["entity_type"] == "DASHBOARD"
    assert results[1]["hops"] == 2

@pytest.mark.asyncio
async def test_get_evidence_package():
    mock_client = AsyncMock(spec=DataHubClient)
    mock_client.execute_graphql.return_value = {
        "data": {
            "searchAcrossLineage": {
                "searchResults": [
                    {
                        "entity": {"urn": "urn:li:dataset:downstream1", "type": "DATASET"},
                        "degree": 1
                    }
                ]
            }
        }
    }

    pkg = await get_evidence_package(mock_client, "urn:li:dataset:root", degree=3)
    assert pkg.source_urn == "urn:li:dataset:root"
    assert pkg.max_hops == 3
    assert len(pkg.entities) == 1
    assert pkg.entities[0]["urn"] == "urn:li:dataset:downstream1"
