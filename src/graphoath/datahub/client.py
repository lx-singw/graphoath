import httpx
from typing import Dict, Any, Optional
from graphoath.config import settings

class DataHubClient:
    def __init__(self, gms_url: Optional[str] = None, token: Optional[str] = None):
        self.gms_url = (gms_url or settings.datahub_gms_url).rstrip('/')
        self.token = token or settings.datahub_token
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

    async def execute_graphql(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.gms_url}/api/graphql"
        payload = {"query": query, "variables": variables or {}}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(url, json=payload, headers=self.headers)
                if response.status_code == 200:
                    return response.json()
                return {"errors": [{"message": f"HTTP {response.status_code}: {response.text}"}]}
        except Exception as e:
            # Fallback mock response for offline/dev environments
            return {"data": {}, "mock": True, "error": str(e)}
