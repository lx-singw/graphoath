import time
from typing import Dict, Any, Optional, List

class PrometheusMetricsRegistry:
    """
    Prometheus metrics collector and text-format exporter.
    """
    def __init__(self):
        self._counters: Dict[str, float] = {
            "graphoath_claims_evaluated_total{status=\"APPROVED\",module=\"Deposition\"}": 0.0,
            "graphoath_claims_evaluated_total{status=\"REJECTED\",module=\"Deposition\"}": 0.0,
            "graphoath_ledger_appends_total": 0.0,
        }
        self._histogram_sum = 0.0
        self._histogram_count = 0

    def inc_claims_evaluated(self, status: str = "APPROVED", module: str = "Deposition"):
        key = f'graphoath_claims_evaluated_total{{status="{status}",module="{module}"}}'
        self._counters[key] = self._counters.get(key, 0.0) + 1.0

    def inc_ledger_appends(self):
        self._counters["graphoath_ledger_appends_total"] += 1.0

    def observe_gate_latency(self, latency_seconds: float):
        self._histogram_sum += latency_seconds
        self._histogram_count += 1

    def generate_prometheus_text(self) -> str:
        lines = [
            "# HELP graphoath_claims_evaluated_total Total number of agent claims evaluated by Citation Gate.",
            "# TYPE graphoath_claims_evaluated_total counter",
        ]
        for k, v in self._counters.items():
            lines.append(f"{k} {v}")
        
        lines.extend([
            "# HELP graphoath_gate_latency_seconds Citation Gate verification latency in seconds.",
            "# TYPE graphoath_gate_latency_seconds histogram",
            f"graphoath_gate_latency_seconds_sum {self._histogram_sum:.6f}",
            f"graphoath_gate_latency_seconds_count {self._histogram_count}"
        ])
        return "\n".join(lines) + "\n"

metrics_registry = PrometheusMetricsRegistry()

class TelemetryTracer:
    """
    OpenTelemetry semantic tracing helper providing graphoath.* span attributes.
    """
    def __init__(self, service_name: str = "graphoath-backend"):
        self.service_name = service_name
        self.spans: List[Dict[str, Any]] = []

    def create_span(self, span_name: str, attributes: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        attrs = attributes or {}
        status = attrs.get("gate_status") or attrs.get("status") or "APPROVED"
        module = attrs.get("module", "Deposition")
        latency_ms = attrs.get("latency_ms", 1.84)
        
        # Record metrics
        metrics_registry.inc_claims_evaluated(status, module)
        metrics_registry.observe_gate_latency(latency_ms / 1000.0)

        span = {
            "name": f"graphoath.{span_name}",
            "context": {
                "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
                "span_id": f"span_{int(time.time()*1000)}"
            },
            "kind": "SPAN_KIND_INTERNAL",
            "timestamp_ns": time.time_ns(),
            "attributes": {
                "service.name": self.service_name,
                "graphoath.module": module,
                "graphoath.trigger.source_urn": attrs.get("source_urn", ""),
                "graphoath.gate.status": status,
                "graphoath.gate.resolution_rate": attrs.get("resolution_rate", 1.0),
                "graphoath.custody.receipt_id": attrs.get("receipt_id", ""),
                "graphoath.custody.hash": attrs.get("hash", "")
            }
        }
        self.spans.append(span)
        return span

tracer = TelemetryTracer()
TelemetryProvider = TelemetryTracer
