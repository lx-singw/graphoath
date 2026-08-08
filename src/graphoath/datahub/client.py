import httpx
from typing import Dict, Any, Optional
from graphoath.config import settings

class DataHubError(Exception):
    """Base exception for all DataHub integration errors."""
    pass

class DataHubConnectionError(DataHubError):
    """Raised when network connection to DataHub GMS fails."""
    pass

class DataHubGraphQLError(DataHubError):
    """Raised when DataHub GraphQL endpoint returns query errors."""
    def __init__(self, message: str, errors: Optional[list[Any]] = None):
        super().__init__(message)
        self.errors = errors or []

class DataHubClient:
    """Production DataHub GraphQL & GMS client wrapper with zero mock fallbacks."""
    def __init__(self, gms_url: Optional[str] = None, token: Optional[str] = None, timeout: float = 10.0):
        self.gms_url = (gms_url or settings.datahub_gms_url).rstrip('/')
        self.token = token or settings.datahub_token
        self.timeout = timeout
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

    async def execute_graphql(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Executes a GraphQL query against DataHub GMS asynchronously.
        
        Raises:
            DataHubConnectionError: If network connection to GMS fails.
            DataHubGraphQLError: If GMS returns HTTP non-200 or GraphQL errors array.
        """
        url = f"{self.gms_url}/api/graphql"
        payload = {"query": query, "variables": variables or {}}
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload, headers=self.headers)
        except Exception as e:
            raise DataHubConnectionError(f"Failed to connect to DataHub GMS at {url}: {str(e)}") from e

        if response.status_code != 200:
            raise DataHubGraphQLError(f"DataHub GMS returned HTTP {response.status_code}: {response.text}")

        res_json = response.json()
        if "errors" in res_json and res_json["errors"]:
            raise DataHubGraphQLError(f"GraphQL Execution Error: {res_json['errors']}", errors=res_json["errors"])

        return res_json

    def execute_graphql_sync(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Executes a GraphQL query against DataHub GMS synchronously."""
        url = f"{self.gms_url}/api/graphql"
        payload = {"query": query, "variables": variables or {}}
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, json=payload, headers=self.headers)
        except Exception as e:
            raise DataHubConnectionError(f"Failed to connect to DataHub GMS at {url}: {str(e)}") from e

        if response.status_code != 200:
            raise DataHubGraphQLError(f"DataHub GMS returned HTTP {response.status_code}: {response.text}")

        res_json = response.json()
        if "errors" in res_json and res_json["errors"]:
            raise DataHubGraphQLError(f"GraphQL Execution Error: {res_json['errors']}", errors=res_json["errors"])

        return res_json

DataHubClientWrapper = DataHubClient

