import inspect
from typing import Any, Dict, List, Optional, Callable
from graphoath.adapters.decorator import graphoath_protected, CitationGateValidationError
from graphoath.datahub.client import DataHubClientWrapper
from graphoath.datahub.incidents import raise_datahub_incident_sync
from graphoath.custody.receipt import CustodyReceipt
from graphoath.custody.ledger import Ledger

class BaseToolFallback:
    """Fallback BaseTool if langchain_core is not installed."""
    name: str = "graphoath_incident_tool"
    description: str = "Raises a citation-gated incident on DataHub"

    def run(self, tool_input: Any) -> Any:
        return self._run(tool_input)

    def _run(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    async def _arun(self, *args, **kwargs) -> Any:
        raise NotImplementedError

try:
    from langchain_core.tools import BaseTool
except ImportError:
    BaseTool = BaseToolFallback  # type: ignore

class GraphOathIncidentTool(BaseTool):
    name: str = "graphoath_raise_incident"
    description: str = "Raises a citation-gated DataHub incident with evidence provenance verification."

    def _run(self, claim_text: str, evidence_urns: List[str], source_urn: str) -> Dict[str, Any]:
        @graphoath_protected()
        def _execute_raise(target_urn: str, claims: List[str]):
            client = DataHubClientWrapper()
            return raise_datahub_incident_sync(
                client=client,
                target_urn=target_urn,
                title=f"Incident: {claim_text[:60]}",
                description=claim_text
            )
        return _execute_raise(source_urn, evidence_urns)

    async def _arun(self, claim_text: str, evidence_urns: List[str], source_urn: str) -> Dict[str, Any]:
        @graphoath_protected()
        async def _execute_raise_async(target_urn: str, claims: List[str]):
            client = DataHubClientWrapper()
            return raise_datahub_incident_sync(
                client=client,
                target_urn=target_urn,
                title=f"Incident: {claim_text[:60]}",
                description=claim_text
            )
        return await _execute_raise_async(source_urn, evidence_urns)

class GraphOathCitationToolWrapper:
    """Wraps an existing LangChain tool to enforce GraphOath citation gating transparently."""
    def __init__(self, tool: Any, module: str = "LangChain"):
        self.tool = tool
        self.module = module

    def run(self, *args, **kwargs) -> Any:
        protected_fn = graphoath_protected(module=self.module)(getattr(self.tool, "run", self.tool))
        return protected_fn(*args, **kwargs)

    async def arun(self, *args, **kwargs) -> Any:
        protected_fn = graphoath_protected(module=self.module)(getattr(self.tool, "arun", self.tool))
        return await protected_fn(*args, **kwargs)
