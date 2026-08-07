"""
LlamaIndex Adapter for GraphOath Citation Gate.
"""

import functools
from typing import Callable, List, Any

def llama_graphoath_protected(evidence_provider: Callable[[], List[str]]):
    """
    Decorator for LlamaIndex function tools to enforce GraphOath citation gating.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            evidence_urns = set(evidence_provider())
            claimed_urns = [arg for arg in args if isinstance(arg, str) and "urn:li:" in arg]
            for val in kwargs.values():
                if isinstance(val, str) and "urn:li:" in val:
                    claimed_urns.append(val)

            uncited = [urn for urn in claimed_urns if urn not in evidence_urns]
            if uncited:
                raise PermissionError(f"[GraphOath LlamaIndex Decorator REJECTED] Uncited URNs: {uncited}")

            print(f"[GraphOath LlamaIndex Decorator] Verified {len(claimed_urns)} URN(s).")
            return func(*args, **kwargs)
        return wrapper
    return decorator
