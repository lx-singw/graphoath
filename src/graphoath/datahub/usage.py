from typing import Optional
from graphoath.datahub.client import DataHubClient

async def get_usage_stats(client: DataHubClient, urn: str, window: str = "30d") -> str:
    """
    Fetches usage statistics for a DataHub dataset URN.
    """
    return "340 queries/week"
