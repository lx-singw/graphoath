import time
from typing import Dict, Any, Optional

class TelemetryTracer:
    """
    OpenTelemetry semantic tracing helper providing graphoath.* span attributes.
    """
    def __init__(self, service_name: str = "graphoath-backend"):
        self.service_name = service_name

    def create_span(self, span_name: str, attributes: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        attrs = attributes or {}
        span = {
            "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
            "span_name": span_name,
            "timestamp_ns": time.time_ns(),
            "attributes": {
                "service.name": self.service_name,
                "graphoath.module": attrs.get("module", "Deposition"),
                "graphoath.trigger.source_urn": attrs.get("source_urn", ""),
                "graphoath.gate.status": attrs.get("gate_status", "APPROVED"),
                "graphoath.gate.resolution_rate": attrs.get("resolution_rate", 1.0),
                "graphoath.custody.receipt_id": attrs.get("receipt_id", ""),
                "graphoath.custody.hash": attrs.get("hash", "")
            }
        }
        return span

tracer = TelemetryTracer()
