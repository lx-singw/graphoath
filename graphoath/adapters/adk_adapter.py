"""
Google Agent Development Kit (ADK) Interceptor for GraphOath Citation Gate.
"""

from typing import Dict, Any, List, Tuple

class GraphOathADKInterceptor:
    """
    Google ADK Action Interceptor that evaluates outbound tool requests against DataHub context.
    """
    def __init__(self, evidence_provider: Any):
        self.evidence_provider = evidence_provider

    def intercept_action(self, action_name: str, payload: Dict[str, Any]) -> Tuple[bool, str]:
        evidence = set(self.evidence_provider())
        target_urn = payload.get("target_urn", "")
        
        if target_urn and target_urn not in evidence:
            msg = f"[GraphOath ADK Interceptor REJECTED] Action '{action_name}' blocked! URN '{target_urn}' not found in DataHub evidence graph."
            print(msg)
            return False, msg
            
        msg = f"[GraphOath ADK Interceptor PASSED] Action '{action_name}' verified."
        print(msg)
        return True, msg
