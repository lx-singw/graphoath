# GraphOath — OpenTelemetry (OTel) Semantic Tracing Specification

This document specifies **GraphOath's OpenTelemetry (OTel) Observability Integration**, which maps AI agent tool calls, DataHub lineage queries, Citation Gate decisions, and Custody receipts into standard OpenTelemetry trace spans.

---

## 1. OTel Semantic Conventions for AI Agent Context

GraphOath exports OTel trace spans using standardized attributes under the `graphoath.*` namespace:

```
  [Span 1: Deposition.IngestEvent]  (trace_id: 4bf92f3577b34da6a3ce929d0e0e4736)
      │
      ├── [Span 2: DataHub.MCPQuery]  (search_across_lineage)
      │
      ├── [Span 3: CitationGate.Verify]  (latency_ms: 1.84ms, status: APPROVED)
      │
      └── [Span 4: Custody.WriteReceipt]  (receipt_hash: e3b0c442...)
```

---

## 2. Span Attribute Specification Table

| Attribute Name | Type | Example Value | Description |
|---|---|---|---|
| `graphoath.module` | `string` | `"Deposition"` | Active GraphOath module name. |
| `graphoath.trigger.source_urn` | `string` | `"urn:li:dataset:(snowflake,prod.orders)"` | Inbound DataHub entity URN. |
| `graphoath.gate.status` | `string` | `"APPROVED"` or `"REJECTED"` | Citation Gate decision outcome. |
| `graphoath.gate.resolution_rate` | `float` | `1.0` | Citation resolution ratio (1.0 = 100%). |
| `graphoath.custody.receipt_id` | `string` | `"rcpt_98f4a12b"` | Custody receipt identifier. |
| `graphoath.custody.hash` | `string` | `"e3b0c442..."` | SHA-256 hash-chain receipt hash. |

---

## 3. Integration with Datadog & Grafana Tempo

GraphOath's OTel exporter outputs traces via standard OTLP/gRPC or OTLP/HTTP to any collector (Grafana Tempo, Datadog, Dynatrace, New Relic), enabling enterprise SRE teams to trace AI agent actions alongside standard application microservices.
