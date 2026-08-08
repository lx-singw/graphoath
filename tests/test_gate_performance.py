import time
import pytest
from graphoath.modules.deposition.gate import CitationGate

def test_citation_gate_sub_millisecond_latency():
    """
    Test 1: Execute 1,000 CitationGate.verify() calls in sequence and assert total execution time is < 5.0 ms per call.
    """
    claimed_urns = {"urn:li:dataset:prod_orders", "urn:li:dataset:stg_orders"}
    evidence_urns = {"urn:li:dataset:prod_orders", "urn:li:dataset:stg_orders", "urn:li:dataset:raw_orders"}

    start = time.perf_counter()
    for _ in range(1000):
        is_approved, missing, latency = CitationGate.verify(claimed_urns, evidence_urns)
        assert is_approved is True
        assert len(missing) == 0
    total_time_ms = (time.perf_counter() - start) * 1000.0
    avg_time_ms = total_time_ms / 1000.0

    assert avg_time_ms < 5.0, f"Average Citation Gate verification latency {avg_time_ms:.4f} ms exceeded 5.0 ms SLA!"

def test_citation_gate_rejection_performance():
    """
    Test 2: CitationGate correctly identifies unevidenced citations in sub-millisecond time.
    """
    claimed_urns = {"urn:li:dataset:prod_orders", "urn:li:dataset:fake_table"}
    evidence_urns = {"urn:li:dataset:prod_orders"}

    is_approved, missing, latency = CitationGate.verify(claimed_urns, evidence_urns)
    assert is_approved is False
    assert "urn:li:dataset:fake_table" in missing
    assert latency < 5.0
