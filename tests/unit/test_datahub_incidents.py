import pytest
from unittest.mock import AsyncMock
from graphoath.datahub.client import DataHubClient
from graphoath.datahub.incidents import raise_incident, raise_datahub_incident

@pytest.mark.asyncio
async def test_raise_incident_mutation():
    mock_client = AsyncMock(spec=DataHubClient)
    mock_client.execute_graphql.return_value = {
        "data": {
            "raiseIncident": "urn:li:incident:1001-2002-3003"
        }
    }

    res = await raise_incident(
        mock_client,
        target_urn="urn:li:dataset:target",
        incident_type="OPERATIONAL",
        title="Schema Break Alert",
        priority="HIGH"
    )

    assert res["incident_urn"] == "urn:li:incident:1001-2002-3003"
    assert res["status"] == "ACTIVE"
    assert res["priority"] == "HIGH"
    mock_client.execute_graphql.assert_called_once()

@pytest.mark.asyncio
async def test_raise_datahub_incident_helper():
    mock_client = AsyncMock(spec=DataHubClient)
    mock_client.execute_graphql.return_value = {
        "data": {
            "raiseIncident": "urn:li:incident:9999-8888"
        }
    }

    urn = await raise_datahub_incident(mock_client, target_urn="urn:li:dataset:target")
    assert urn == "urn:li:incident:9999-8888"
