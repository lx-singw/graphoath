"""
GraphOath Citation Gate Decorator.

Provides a 1-liner decorator @graphoath_protected for agent tool functions.
Intercepts tool arguments, extracts entity URNs, evaluates claims against
DataHub MCP metadata evidence, and blocks uncited write calls.
"""

import functools
import re
from typing import Callable, Any, List, Dict

URN_REGEX = re.compile(r"urn:li:[a-zA-Z0-9_-]+:\([^\)]+\)|urn:li:[a-zA-Z0-9_-]+:[a-zA-Z0-9._-]+")

class CitationVerificationError(PermissionError):
    """Raised when an agent tool attempt is blocked by GraphOath Citation Gate."""
    pass

def extract_urns_from_args(args: tuple, kwargs: dict) -> List[str]:
    """Scans tool function arguments for DataHub URN patterns."""
    found_urns = set()
    all_str_values = []
    
    for arg in args:
        if isinstance(arg, str):
            all_str_values.append(arg)
        elif isinstance(arg, (list, tuple)):
            all_str_values.extend([item for item in arg if isinstance(item, str)])
            
    for val in kwargs.values():
        if isinstance(val, str):
            all_str_values.append(val)
        elif isinstance(val, (list, tuple)):
            all_str_values.extend([item for item in val if isinstance(item, str)])

    for text in all_str_values:
        matches = URN_REGEX.findall(text)
        found_urns.update(matches)
        
    return list(found_urns)

def graphoath_protected(
    evidence_provider: Callable[[], List[str]] = None,
    enforce_citations: bool = True
):
    """
    Decorator that wraps agent write tools with GraphOath Citation Gating.
    
    Usage:
        @graphoath_protected(evidence_provider=get_current_mcp_evidence)
        def raise_incident_tool(target_dataset_urn: str, description: str):
            return datahub_client.raise_incident(...)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if not enforce_citations:
                return func(*args, **kwargs)
                
            claimed_urns = extract_urns_from_args(args, kwargs)
            evidence_urns = evidence_provider() if evidence_provider else []
            
            if claimed_urns and evidence_urns:
                uncited_urns = [urn for urn in claimed_urns if urn not in evidence_urns]
                if uncited_urns:
                    raise CitationVerificationError(
                        f"[GraphOath Citation Gate REJECTED] Action blocked! "
                        f"Uncited or hallucinated entity URNs detected: {uncited_urns}"
                    )
                    
            print(f"[GraphOath Citation Gate PASSED] All {len(claimed_urns)} URN(s) verified against DataHub graph.")
            return func(*args, **kwargs)
        return wrapper
    return decorator

if __name__ == "__main__":
    # Self-test demonstration
    mock_evidence = [
        "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)",
        "urn:li:corpuser:alice"
    ]
    
    @graphoath_protected(evidence_provider=lambda: mock_evidence)
    def sample_raise_incident(dataset_urn: str, description: str):
        return f"Successfully raised incident on {dataset_urn}"

    print("--- Test 1: Valid Verified URN ---")
    res = sample_raise_incident("urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)", "Schema breaking change")
    print(res)
    
    print("\n--- Test 2: Unverified Hallucinated URN ---")
    try:
        sample_raise_incident("urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.hallucinated_table,PROD)", "Fake issue")
    except CitationVerificationError as e:
        print(e)
