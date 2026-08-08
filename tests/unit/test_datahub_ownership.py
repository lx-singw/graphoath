import pytest
from unittest.mock import AsyncMock
from graphoath.datahub.client import DataHubClient
from graphoath.datahub.ownership import get_ownership, get_dataset_ownership

@pytest.mark.asyncio
async def test_get_ownership_parsing():
    mock_client = AsyncMock(spec=DataHubClient)
    mock_client.execute_graphql.return_value = {
        "data": {
            "dataset": {
                "ownership": {
                    "owners": [
                        {"owner": {"urn": "urn:li:corpuser:priya_ramaswamy", "username": "priya_ramaswamy"}},
                        {"owner": {"urn": "urn:li:corpGroup:data_platform_team", "name": "data_platform_team"}}
                    ]
                }
            }
        }
    }

    owners = await get_ownership(mock_client, "urn:li:dataset:test")
    assert len(owners) == 2
    assert "urn:li:corpuser:priya_ramaswamy" in owners
    assert "urn:li:corpGroup:data_platform_team" in owners

@pytest.mark.asyncio
async def test_get_dataset_ownership_alias():
    mock_client = AsyncMock(spec=DataHubClient)
    mock_client.execute_graphql.return_value = {
        "data": {
            "dataset": {
                "ownership": {
                    "owners": [
                        {"owner": {"urn": "urn:li:corpuser:marcus_webb"}}
                    ]
                }
            }
        }
    }

    owners = await get_dataset_ownership(mock_client, "urn:li:dataset:test")
    assert owners == ["urn:li:corpuser:marcus_webb"]
