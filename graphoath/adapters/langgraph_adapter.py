"""
LangGraph Adapter for GraphOath Citation Gate.
"""

from typing import Dict, Any, List

class CitationGateStateNode:
    """
    LangGraph state DAG node that evaluates proposed state mutations against DataHub evidence.
    """
    def __init__(self, evidence_key: str = "evidence_urns", claims_key: str = "proposed_claims"):
        self.evidence_key = evidence_key
        self.claims_key = claims_key

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        evidence = set(state.get(self.evidence_key, []))
        claims = state.get(self.claims_key, [])
        
        verified = []
        rejected = []
        
        for claim in claims:
            target_urn = claim.get("target_urn", "")
            if target_urn in evidence or not target_urn:
                verified.append(claim)
            else:
                rejected.append(claim)
                
        state["gate_status"] = "PASSED" if not rejected else "REJECTED"
        state["verified_claims"] = verified
        state["rejected_claims"] = rejected
        
        print(f"[GraphOath LangGraph Node] Evaluated {len(claims)} claim(s). Status: {state['gate_status']}")
        return state
