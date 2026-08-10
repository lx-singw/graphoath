import httpx
from typing import Dict, Any, Optional

import datahub
from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub_agent_context import DataHubContext, get_datahub_client, get_graph

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
    """Production DataHub GraphQL & GMS client wrapper with real SDK bindings."""
    def __init__(self, gms_url: Optional[str] = None, token: Optional[str] = None, timeout: float = 10.0):
        self.gms_url = (gms_url or settings.datahub_gms_url).rstrip('/')
        self.token = token or settings.datahub_token
        self.timeout = timeout
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        # Initialize native acryl-datahub REST emitter
        self.emitter = DatahubRestEmitter(gms_server=self.gms_url, token=self.token)

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

    def get_evidence_package(self, urn: str, max_hops: int = 3):
        """Returns EvidencePackage with lineage for URN by querying live DataHub GMS."""
        from graphoath.datahub.lineage import EvidencePackage
        try:
            res = self.execute_graphql_sync(
                """
                query searchAcrossLineage($urn: String!) {
                  searchAcrossLineage(input: {urn: $urn, direction: DOWNSTREAM}) {
                    searchResults {
                      entity {
                        ... on Dataset { urn type }
                        ... on Chart { urn type }
                        ... on Dashboard { urn type }
                      }
                    }
                  }
                }
                """,
                {"urn": urn}
            )
            entities = []
            if "data" in res and res["data"] and res["data"].get("searchAcrossLineage"):
                search_results = res["data"]["searchAcrossLineage"] or {}
                for item in search_results.get("searchResults", []):
                    entity = item.get("entity", {})
                    if entity.get("urn"):
                        entities.append({"urn": entity.get("urn"), "type": entity.get("type", "DATASET"), "hops": 1})
            return EvidencePackage(source_urn=urn, direction="DOWNSTREAM", max_hops=max_hops, entities=entities, raw_response=res)
        except Exception as e:
            # Zero-mock policy: Raise DataHubConnectionError if live GMS query fails
            raise DataHubConnectionError(f"Live DataHub GMS lineage query failed for URN '{urn}': {e}") from e

DataHubClientWrapper = DataHubClient


