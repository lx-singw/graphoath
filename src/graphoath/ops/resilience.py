import time
import functools
import asyncio
from typing import Set, List, Dict, Any, Callable, Optional, Union

class GraphOathResilienceError(Exception):
    """Base exception for resilience safeguards."""
    pass

class CircuitBreakerOpenError(GraphOathResilienceError):
    """Raised when circuit breaker is in OPEN state (Fail-Closed Posture)."""
    pass

class MaxNodeLimitExceededError(GraphOathResilienceError):
    """Raised when traversal exceeds max allowed graph nodes."""
    pass

class GraphTraversalCircuitBreaker:
    """
    Graph Traversal Circuit Breaker & Circular Lineage Guard.
    
    Protects against infinite lineage loops (URN_A -> URN_B -> URN_A), graph explosion
    (max_depth=3, max_nodes=1000), and DataHub API network partitions.
    """
    def __init__(self, max_depth: int = 3, max_nodes: int = 1000, failure_threshold: int = 5, cooldown_seconds: float = 30.0):
        self.max_depth = min(max_depth, 5)
        self.max_nodes = max_nodes
        self.failure_threshold = failure_threshold
        self.cooldown_seconds = cooldown_seconds
        
        self.visited_urns: Set[str] = set()
        self.state: str = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.consecutive_failures: int = 0
        self.last_failure_time: float = 0.0

    def reset_traversal(self) -> None:
        """Resets active visited URN set for a new traversal session."""
        self.visited_urns.clear()

    def record_node_visit(self, urn: str, current_depth: int) -> bool:
        """
        Records node visit.
        Returns False if circular loop detected or hop depth exceeded.
        Raises MaxNodeLimitExceededError if node count exceeds limit.
        """
        if current_depth > self.max_depth:
            return False
        
        if urn in self.visited_urns:
            # Circular loop detected! Terminate branch.
            return False

        if len(self.visited_urns) >= self.max_nodes:
            raise MaxNodeLimitExceededError(f"[GraphOath Circuit Breaker EXCEEDED] Max node limit of {self.max_nodes} exceeded! Total visited: {len(self.visited_urns) + 1}.")

        self.visited_urns.add(urn)
        return True

    def check_state(self) -> None:
        """
        Checks circuit breaker state.
        If OPEN and cooldown elapsed, transition to HALF_OPEN.
        If OPEN and cooldown active, raise CircuitBreakerOpenError (Fail-Closed Posture).
        """
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.cooldown_seconds:
                self.state = "HALF_OPEN"
            else:
                raise CircuitBreakerOpenError("[GraphOath Circuit Breaker OPEN] DataHub API network failure threshold exceeded! Fail-Closed posture active.")

    def record_success(self) -> None:
        self.consecutive_failures = 0
        self.state = "CLOSED"

    def record_failure(self) -> None:
        self.consecutive_failures += 1
        self.last_failure_time = time.time()
        if self.consecutive_failures >= self.failure_threshold:
            self.state = "OPEN"

def retry_with_backoff(max_retries: int = 3, backoff_factor: float = 1.5):
    """
    Decorator for retrying functions on failure with exponential backoff.
    Works for both synchronous and asynchronous functions.
    """
    def decorator(func: Callable):
        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                last_exc = None
                for attempt in range(1, max_retries + 1):
                    try:
                        return await func(*args, **kwargs)
                    except Exception as exc:
                        last_exc = exc
                        if attempt == max_retries:
                            raise exc
                        await asyncio.sleep(backoff_factor ** (attempt - 1))
                raise last_exc
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                last_exc = None
                for attempt in range(1, max_retries + 1):
                    try:
                        return func(*args, **kwargs)
                    except Exception as exc:
                        last_exc = exc
                        if attempt == max_retries:
                            raise exc
                        time.sleep(backoff_factor ** (attempt - 1))
                raise last_exc
            return sync_wrapper
    return decorator

_global_circuit_breaker = GraphTraversalCircuitBreaker()
