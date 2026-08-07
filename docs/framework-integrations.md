# GraphOath — AI Framework Integration Guide (LangChain, LangGraph, LlamaIndex, ADK)

This guide explains how autonomous AI agents built with modern orchestration frameworks—such as **LangChain**, **LangGraph**, **LlamaIndex**, or **Google ADK**—integrate with **GraphOath** and **DataHub's Context Platform**.

---

## 1. Overview & Integration Pattern

Autonomous agents use frameworks like LangChain or LangGraph to reason over data tools. However, when an agent decides to take an action (e.g., raising an incident, deprecating a dataset, sending a notification), letting the agent directly call write APIs risks **unverified claims and hallucinated metadata**.

GraphOath introduces the **Citation-Gated Tool Pattern**:

```
 ┌────────────────┐     1. Request Context      ┌─────────────────────┐
 │  LangChain /   ├────────────────────────────►│  DataHub MCP Server │
 │ LangGraph Agent│◄────────────────────────────┤ / Context Kit API   │
 └───────┬────────┘     2. Metadata Graph       └─────────────────────┘
         │
         │ 3. Proposed Action & Claim Text
         ▼
 ┌──────────────────────────────────────────────┐
 │          GraphOath Citation Gate             │
 │  (Verifies every URN against evidence array) │
 └───────┬──────────────────────────────┬───────┘
         │ Passed                       │ Rejected
         ▼                              ▼
 ┌──────────────────────┐      ┌─────────────────────┐
 │ Native DataHub Action│      │ Return Citation Error│
 │ + Hash Receipt       │      │ to Agent for Retry  │
 └──────────────────────┘      └─────────────────────┘
```

---

## 2. LangChain Integration

### 2.1 LangChain Custom Tool Wrapper

In LangChain, write actions are exposed as `BaseTool` instances. By wrapping native DataHub write tools inside GraphOath's citation gate, we guarantee that the agent cannot execute an incident or deprecation action without valid DataHub citations.

```python
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from graphoath.gate import CitationGate
from graphoath.datahub.incidents import raise_datahub_incident

class GraphOathIncidentInput(BaseModel):
    claim_text: str = Field(description="Summary of the incident with referenced dataset URNs")
    evidence_urns: List[str] = Field(description="List of DataHub URNs fetched during metadata inspection")
    source_urn: str = Field(description="The primary dataset URN where the schema break originated")

class GraphOathIncidentTool(BaseTool):
    name: str = "raise_citation_gated_incident"
    description: str = (
        "Safely raises a native DataHub Incident. Every dataset URN named in claim_text "
        "must exist in evidence_urns, or the action will be blocked by GraphOath."
    )
    args_schema = GraphOathIncidentInput

    def _run(self, claim_text: str, evidence_urns: List[str], source_urn: str) -> str:
        # Step 1: Run GraphOath Citation Gate
        gate = CitationGate()
        gate_result = gate.verify(claim_text=claim_text, evidence_urns=evidence_urns)
        
        if not gate_result.passed:
            return (
                f"ACTION REJECTED BY GRAPHOATH: The claim referenced unverified entity URNs: "
                f"{gate_result.missing_citations}. Please query DataHub MCP for these URNs first."
            )
        
        # Step 2: Execute Native DataHub Action & Record Custody Receipt
        incident_urn, receipt_id = raise_datahub_incident(
            source_urn=source_urn,
            description=claim_text,
            evidence=gate_result.evidence_array
        )
        
        return f"SUCCESS: Incident raised: {incident_urn} (Receipt ID: {receipt_id})"
```

---

## 3. LangGraph Integration

### 3.1 Stateful Verification Node

In **LangGraph**, agents operate as state machines. GraphOath provides a dedicated node for the agent graph that inspects state transitions before any write operation.

```python
from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    event_payload: Dict[str, Any]
    evidence_graph: List[Dict[str, Any]]
    draft_claim: str
    citation_passed: bool
    rejection_reason: str
    incident_urn: str

def verify_citation_gate_node(state: AgentState) -> AgentState:
    """LangGraph node that acts as a gatekeeper prior to incident creation."""
    evidence_urns = [item["urn"] for item in state["evidence_graph"]]
    claim = state["draft_claim"]
    
    # Check claim against evidence URNs
    unmatched = [urn for urn in extract_urns(claim) if urn not in evidence_urns]
    
    if unmatched:
        state["citation_passed"] = False
        state["rejection_reason"] = f"Uncited URNs found in claim: {unmatched}"
    else:
        state["citation_passed"] = True
    
    return state

# Building the LangGraph
workflow = StateGraph(AgentState)
workflow.add_node("gather_evidence", gather_datahub_evidence_node)
workflow.add_node("draft_claim", draft_incident_claim_node)
workflow.add_node("citation_gate", verify_citation_gate_node)
workflow.add_node("raise_incident", raise_incident_action_node)

# Conditional Branching based on Citation Gate
workflow.add_conditional_edges(
    "citation_gate",
    lambda state: "raise_incident" if state["citation_passed"] else "gather_evidence",
    {
        "raise_incident": "raise_incident",
        "gather_evidence": "gather_evidence" # Re-query context if uncited
    }
)
```

---

## 4. LlamaIndex & Google Agent Development Kit (ADK)

GraphOath provides clean abstractions for all major frameworks:

- **LlamaIndex**: GraphOath can be implemented as a `QueryEngineTool` post-processor or `FunctionTool` wrapper that intercepts query engine outputs before returning structured actions.
- **Google ADK**: GraphOath integrates into ADK agent pipelines via custom **Tool Call Interceptors**, ensuring all outbound tool calls comply with the citation-gated protocol.

---

## 5. Runnable Examples

To see these framework patterns in action, explore the scripts in the [`examples/`](examples/) directory:
- [`examples/langchain_agent_example.py`](examples/langchain_agent_example.py): Full runnable LangChain agent integration script.
- [`examples/mock_mcp_citation_demo.py`](examples/mock_mcp_citation_demo.py): Standalone script demonstrating citation gate mechanics.
