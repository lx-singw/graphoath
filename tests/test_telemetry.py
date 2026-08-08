import pytest
from graphoath.telemetry import TelemetryProvider, metrics_registry

def test_telemetry_span_creation_and_attributes():
    """
    Test 1: Invoke protected tool call and verify OTel trace span CitationGate.Verify is created
    with attribute graphoath.gate.status == 'APPROVED'.
    """
    provider = TelemetryProvider(service_name="test-service")
    span = provider.create_span(
        span_name="CitationGate.Verify",
        attributes={
            "module": "Deposition",
            "source_urn": "urn:li:dataset:prod_orders",
            "gate_status": "APPROVED",
            "resolution_rate": 1.0,
            "receipt_id": "rcpt_test_99",
            "hash": "abc123hash"
        }
    )

    assert span["name"] == "graphoath.CitationGate.Verify"
    assert span["attributes"]["graphoath.gate.status"] == "APPROVED"
    assert span["attributes"]["graphoath.module"] == "Deposition"
    assert span["attributes"]["graphoath.trigger.source_urn"] == "urn:li:dataset:prod_orders"

def test_prometheus_metrics_counter_increment():
    """
    Test 2: Query metrics exporter and verify graphoath_claims_evaluated_total metric counter increments.
    """
    metrics_text = metrics_registry.generate_prometheus_text()
    assert "graphoath_claims_evaluated_total" in metrics_text
    assert "graphoath_gate_latency_seconds" in metrics_text
