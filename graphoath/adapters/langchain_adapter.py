"""
LangChain Adapter for GraphOath Citation Gate.
"""

from typing import Callable, List, Any, Dict

class GraphOathCitationToolWrapper:
    """
    Wraps standard LangChain agent tools with GraphOath citation verification.
    """
    def __init__(
        self,
        tool_func: Callable,
        evidence_provider: Callable[[], List[str]],
        name: str = "graphoath_protected_tool"
    ):
        self.tool_func = tool_func
        self.evidence_provider = evidence_provider
        self.name = name

    def run(self, *args, **kwargs) -> Any:
        evidence_urns = self.evidence_provider()
        claimed_urns = [arg for arg in args if isinstance(arg, str) and "urn:li:" in arg]
        for val in kwargs.values():
            if isinstance(val, str) and "urn:li:" in val:
                claimed_urns.append(val)

        uncited = [urn for urn in claimed_urns if urn not in evidence_urns]
        if uncited:
            raise ValueError(f"[GraphOath Citation Gate REJECTED] Uncited URNs: {uncited}")

        print(f"[GraphOath LangChain Adapter] Action approved for {len(claimed_urns)} URN(s).")
        return self.tool_func(*args, **kwargs)
