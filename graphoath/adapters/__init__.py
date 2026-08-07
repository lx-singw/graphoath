"""
GraphOath Multi-Framework Agent Adapters Package.

Provides pre-built citation gating adapters and tool wrappers for:
- LangChain (GraphOathCitationToolWrapper)
- LangGraph (CitationGateStateNode)
- LlamaIndex (@llama_graphoath_protected)
- Google ADK (GraphOathADKInterceptor)
"""

from .langchain_adapter import GraphOathCitationToolWrapper
from .langgraph_adapter import CitationGateStateNode
from .llamaindex_adapter import llama_graphoath_protected
from .adk_adapter import GraphOathADKInterceptor

__all__ = [
    "GraphOathCitationToolWrapper",
    "CitationGateStateNode",
    "llama_graphoath_protected",
    "GraphOathADKInterceptor",
]
