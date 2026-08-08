import pytest
from unittest.mock import patch, MagicMock
from graphoath.datahub.client import (
    DataHubClient,
    DataHubConnectionError,
    DataHubGraphQLError,
)

@pytest.mark.asyncio
async def test_datahub_client_init():
    client = DataHubClient(gms_url="http://test-gms:8080", token="test-token")
    assert client.gms_url == "http://test-gms:8080"
    assert client.headers["Authorization"] == "Bearer test-token"

@pytest.mark.asyncio
async def test_execute_graphql_success():
    client = DataHubClient(gms_url="http://test-gms:8080", token="test-token")
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"me": {"urn": "urn:li:corpuser:test"}}}

    with patch("httpx.AsyncClient.post") as mock_post:
        mock_post.return_value = mock_response
        res = await client.execute_graphql("query { me { urn } }")
        assert res == {"data": {"me": {"urn": "urn:li:corpuser:test"}}}

@pytest.mark.asyncio
async def test_execute_graphql_connection_error():
    client = DataHubClient(gms_url="http://invalid-host:9999", token="test-token")
    with patch("httpx.AsyncClient.post", side_effect=Exception("Connection refused")):
        with pytest.raises(DataHubConnectionError) as exc_info:
            await client.execute_graphql("query { me { urn } }")
        assert "Failed to connect to DataHub GMS" in str(exc_info.value)

@pytest.mark.asyncio
async def test_execute_graphql_query_error():
    client = DataHubClient(gms_url="http://test-gms:8080", token="test-token")
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"errors": [{"message": "Syntax error in GraphQL query"}]}

    with patch("httpx.AsyncClient.post") as mock_post:
        mock_post.return_value = mock_response
        with pytest.raises(DataHubGraphQLError) as exc_info:
            await client.execute_graphql("invalid query")
        assert "GraphQL Execution Error" in str(exc_info.value)
