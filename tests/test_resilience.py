import pytest
from graphoath.ops.resilience import (
    GraphTraversalCircuitBreaker,
    CircuitBreakerOpenError,
    MaxNodeLimitExceededError,
    retry_with_backoff
)

def test_circular_lineage_guard_loop_termination():
    """
    Test 1: Construct a circular lineage graph (URN_A -> URN_B -> URN_C -> URN_A)
    and assert lineage traversal terminates cleanly without infinite loops.
    """
    cb = GraphTraversalCircuitBreaker(max_depth=3, max_nodes=100)
    cb.reset_traversal()

    # Traversing URN_A
    res_a = cb.record_node_visit("urn:li:dataset:URN_A", current_depth=1)
    assert res_a is True

    # Traversing URN_B
    res_b = cb.record_node_visit("urn:li:dataset:URN_B", current_depth=2)
    assert res_b is True

    # Traversing URN_C
    res_c = cb.record_node_visit("urn:li:dataset:URN_C", current_depth=3)
    assert res_c is True

    # Attempting to re-visit URN_A (circular loop)
    res_loop = cb.record_node_visit("urn:li:dataset:URN_A", current_depth=4)
    assert res_loop is False  # Loop cleanly terminated!

def test_circuit_breaker_trip_on_consecutive_failures():
    """
    Test 2: Simulate DataHub API network partition (5 consecutive errors)
    and assert GraphTraversalCircuitBreaker trips to OPEN state.
    """
    cb = GraphTraversalCircuitBreaker(failure_threshold=5, cooldown_seconds=30.0)
    cb.reset_traversal()
    assert cb.state == "CLOSED"

    # Simulate 4 failures
    for _ in range(4):
        cb.record_failure()
        assert cb.state == "CLOSED"

    # 5th failure trips to OPEN state
    cb.record_failure()
    assert cb.state == "OPEN"

    # Subsequent check raises CircuitBreakerOpenError (Fail-Closed Posture)
    with pytest.raises(CircuitBreakerOpenError):
        cb.check_state()

def test_retry_with_backoff_decorator():
    """
    Test 3: Verify @retry_with_backoff retries failing functions.
    """
    attempts = 0

    @retry_with_backoff(max_retries=3, backoff_factor=0.01)
    def flaky_func():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ValueError("Temporary failure")
        return "SUCCESS"

    result = flaky_func()
    assert result == "SUCCESS"
    assert attempts == 3
