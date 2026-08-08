import functools
import inspect
from typing import Callable, Any, Dict, List, Optional
from graphoath.adapters.decorator import graphoath_protected, CitationGateValidationError

def llama_graphoath_protected(module: str = "LlamaIndex") -> Callable:
    """
    LlamaIndex query engine and tool post-processor decorator.
    Intercepts LlamaIndex output parsers & tools to enforce GraphOath citation gating.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            protected_fn = graphoath_protected(module=module)(func)
            return await protected_fn(*args, **kwargs)

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            protected_fn = graphoath_protected(module=module)(func)
            return protected_fn(*args, **kwargs)

        if inspect.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator

class LlamaIndexGraphOathPostProcessor:
    """Post-processor interceptor for LlamaIndex query engine pipelines."""
    
    def post_process_response(self, response: Any, extra_info: Optional[Dict[str, Any]] = None) -> Any:
        @graphoath_protected(module="LlamaIndex")
        def _verify(resp_text: str):
            return resp_text

        text = str(getattr(response, "response", response))
        return _verify(text)
