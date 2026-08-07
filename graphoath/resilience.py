"""
GraphOath Resilience & Circuit Breaker Safeguards.

Provides jittered exponential backoff retries and graph traversal memory/node caps.
"""

import functools
import time
import random
from typing import Callable, Any, List, Set

class CircuitBreakerError(RuntimeError):
    """Raised when graph lineage traversal exceeds max hop or node bounds."""
    pass

def retry_with_backoff(
    max_retries: int = 3,
    initial_delay_sec: float = 0.1,
    backoff_factor: float = 2.0,
    jitter: bool = True,
    exceptions: tuple = (Exception,)
):
    """
    Decorator executing exponential backoff retries for network/GraphQL calls.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            delay = initial_delay_sec
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries:
                        print(f"[GraphOath Resilience] Max retries ({max_retries}) reached for {func.__name__}. Error: {e}")
                        raise e
                    sleep_time = delay * (1.0 + random.uniform(-0.1, 0.1) if jitter else 1.0)
                    print(f"[GraphOath Resilience] Attempt {attempt} failed ({e}). Retrying in {sleep_time:.3f}s...")
                    time.sleep(sleep_time)
                    delay *= backoff_factor
        return wrapper
    return decorator

class GraphTraversalCircuitBreaker:
    """
    Safeguards lineage graph traversal against graph explosion.
    Enforces maximum hop depth cap (default 3) and maximum node count cap (default 1,000).
    """
    def __init__(self, max_hops: int = 3, max_nodes: int = 1000):
        self.max_hops = max_hops
        self.max_nodes = max_nodes
        self.visited_nodes: Set[str] = set()

    def record_node(self, node_urn: str, current_hop: int):
        if current_hop > self.max_hops:
            raise CircuitBreakerError(
                f"[GraphOath Circuit Breaker EXCEEDED] Max hop depth of {self.max_hops} exceeded at hop {current_hop} for URN '{node_urn}'."
            )
        self.visited_nodes.add(node_urn)
        if len(self.visited_nodes) > self.max_nodes:
            raise CircuitBreakerError(
                f"[GraphOath Circuit Breaker EXCEEDED] Max node limit of {self.max_nodes} exceeded! Total visited: {len(self.visited_nodes)}."
            )
            
    def reset(self):
        self.visited_nodes.clear()

if __name__ == "__main__":
    cb = GraphTraversalCircuitBreaker(max_hops=3, max_nodes=5)
    for i in range(5):
        cb.record_node(f"urn:li:dataset:node_{i}", current_hop=1)
    print(f"[Self-Test] Circuit breaker recorded {len(cb.visited_nodes)} nodes successfully.")
    try:
        cb.record_node("urn:li:dataset:overflow_node", current_hop=1)
    except CircuitBreakerError as e:
        print(f"[Self-Test] Caught expected circuit breaker error: {e}")
