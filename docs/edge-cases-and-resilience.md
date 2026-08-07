# GraphOath — Edge Cases & System Resilience Matrix

This document outlines how **GraphOath** handles complex real-world data stack edge cases, transient network failures, circular dependencies, and governance exceptions.

---

## 1. Edge Case Handling Matrix

| Real-World Edge Case | Potential Risk | GraphOath Mitigation & Strategy |
|---|---|---|
| **Circular Lineage Graphs** | Infinite loop during downstream lineage traversal (`searchAcrossLineage`). | GraphOath maintains a visited set of URNs during traversal. If a URN is encountered a second time, the node is flagged and traversal along that path stops immediately. |
| **Unassigned Asset Ownership** | Incident cannot be assigned to an engineer via native `raiseIncident`. | Deposition falls back to the dataset's domain owner or the global DataHub platform default user (`urn:li:corpuser:data_platform_admin`). |
| **Orphaned / Unconnected Assets** | Lineage query returns 0 downstream assets for a breaking schema change. | GraphOath generates an informational receipt acknowledging 0 downstream impact and suppresses alert noise to Slack/Incident channels. |
| **Deep Blast Radius (>1,000 Nodes)** | Lineage traversal memory overhead or giant incident payload. | Hop depth cap (default 3) and node limit (1,000 max nodes). If exceeded, GraphOath summarizes top-level staging datasets and attaches a link to full DataHub lineage graph UI. |
| **Transient DataHub API Outage** | Actions webhook fails to reach Deposition or GraphQL mutation fails. | Inbound change events are buffered in PostgreSQL. Outbound mutations implement exponential backoff with jitter (3 retries). |

---

## 2. Ledger Integrity & Tamper Recovery

If PostgreSQL experience silent row modification or malicious tampering:

```
                      Nightly Ledger Integrity Check
                                    │
                                    ▼
                Recompute SHA-256 Hash Chain from Genesis
                                    │
                         ┌──────────┴──────────┐
                         ▼                     ▼
                     Hash Match            Hash Mismatch
                         │                     │
                     [OK] Pass             [ALERT] Flag Index X
                                           Notify Governance Admin via Slack
                                           Freeze Automated Writes
```

1. **Detection**: `python -m graphoath.db.verify_ledger` recomputes hash chains.
2. **Alerting**: Immediate notification to `governance_admin` role.
3. **Recovery**: GraphOath can verify original receipts by cross-referencing `graphoathReceipt` aspects stored in DataHub's metadata graph.

---

## 3. Rate Limiting & Circuit Breakers

To prevent incident flooding during massive pipeline re-runs (e.g. 50 dbt models failing simultaneously):

- **De-duplication Window**: Deposition checks if an open DataHub Incident already exists for a dataset URN within a 15-minute window. If found, it appends evidence to the existing incident via `updateIncident` instead of creating 50 duplicate incidents.
- **Circuit Breaker**: If outbound DataHub mutations fail 5 consecutive times, the action layer trips and queues receipts locally until health checks pass.
