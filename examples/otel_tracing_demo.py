"""
GraphOath OpenTelemetry (OTel) Telemetry Trace Emitter Demo.

Generates OpenTelemetry spans for citation gate evaluations and evidence array counts.
"""

import json
import time

def emit_graphoath_otel_span(trace_id: str, agent_id: str, action: str, evidence_count: int, gate_result: str) -> dict:
    """Emits mock OpenTelemetry span matching GraphOath semantic conventions."""
    timestamp_ns = int(time.time() * 1e9)
    span = {
        "name": "graphoath.citation_gate.evaluate",
        "context": {
            "trace_id": trace_id,
            "span_id": "span_gate_eval_001"
        },
        "kind": "SPAN_KIND_INTERNAL",
        "start_time_unix_nano": timestamp_ns - 1840000, # 1.84 ms
        "end_time_unix_nano": timestamp_ns,
        "attributes": {
            "graphoath.agent.id": agent_id,
            "graphoath.action.type": action,
            "graphoath.evidence.count": evidence_count,
            "graphoath.gate.result": gate_result,
            "graphoath.gate.latency_ms": 1.84,
            "graphoath.ledger.hash_chained": True
        },
        "events": [
            {
                "name": "evidence_array_assembled",
                "time_unix_nano": timestamp_ns - 1000000,
                "attributes": {"evidence_urn_count": evidence_count}
            },
            {
                "name": "citation_gate_passed",
                "time_unix_nano": timestamp_ns,
                "attributes": {"status": gate_result}
            }
        ]
    }
    return span

if __name__ == "__main__":
    print("=======================================================================")
    print("GraphOath — OpenTelemetry (OTel) Semantic Telemetry Trace Emitter Demo")
    print("=======================================================================")
    
    mock_span = emit_graphoath_otel_span("4bf92f3577b34da6a3ce929d0e0e4736", "deposition_agent_v1", "raiseIncident", 3, "APPROVED")
    print(json.dumps(mock_span, indent=2))
    print("=======================================================================")
    print("[OK] OpenTelemetry Trace Span Emitted Successfully.")
