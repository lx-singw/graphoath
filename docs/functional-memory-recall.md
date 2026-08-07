# GraphOath — Functional Memory Recall Architecture

This document details how **GraphOath's Custody Ledger** acts as **functional long-term memory** for AI agents acting on DataHub. Rather than treating each metadata event as an isolated occurrence, GraphOath queries historical receipts to surface recurring incident patterns and historical root causes.

---

## 1. Functional Memory vs. Stateless Logging

Traditional AI agent logging records what an agent did, but does not allow future agent runs to learn from past incidents. GraphOath turns the Custody ledger into a **queryable memory engine**:

```
 ┌─────────────────────────────────────────────────────────────┐
 │                Inbound Change Event                         │
 │ urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders)  │
 └──────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │               Custody Memory Engine Lookup                  │
 │  Query: GET /receipts?source_urn=...&window=30d              │
 └──────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │                Memory Insights Surfaced                     │
 │  - Occurrences in 30 days: 2                                │
 │  - Previous Root Cause: dbt model migration by data_eng     │
 │  - Priority Escalation: NORMAL → HIGH_RECURRING             │
 └──────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │               Enriched DataHub Incident Created             │
 │  Native DataHub Incident with memory recall attached       │
 └─────────────────────────────────────────────────────────────┘
```

---

## 2. Memory Recall Schema & JSON Structure

When GraphOath processes a new change event, it attaches a `functional_memory_recall` block to the evidence package:

```json
{
  "functional_memory_recall": {
    "repeat_incident_detected": true,
    "occurrences_in_30d": 2,
    "previous_receipt_id": "rcpt_98f4a12b-7c3e-4b9d-a8f1-2e6b5c4d3a01",
    "previous_incident_urn": "urn:li:incident:graphoath-dep-20260807-001",
    "memory_insight": "RECURRING PATTERN: 2nd schema-breaking modification on prod.orders within 30 days. Root cause previously attributed to dbt model deployment by data_eng_team."
  }
}
```

---

## 3. Benefits for AI Agents & Data Platform Teams

1. **Prevents Duplicate Incident Noise**: If an incident is already active for a dataset, GraphOath updates the existing incident (`updateIncident`) rather than opening 10 duplicate tickets.
2. **Automated Priority Escalation**: Recurring schema breaks automatically escalate priority from `MEDIUM` to `HIGH_RECURRING`.
3. **Cross-Agent Knowledge Sharing**: Future agents querying DataHub via MCP retrieve the `graphoathReceipt` aspect and immediately see historical failure context.

---

## 4. Empirical Example

See [`examples/receipt-repeat-incident.json`](examples/receipt-repeat-incident.json) for a live generated receipt demonstrating functional memory recall.
