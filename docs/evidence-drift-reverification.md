# GraphOath — Evidence-Drift Re-Verification Architecture

This document specifies **GraphOath's Evidence-Drift Engine**, which provides periodic re-verification of cited evidence facts against live DataHub metadata to detect when a citation has gone stale.

---

## 1. Protecting the Record vs. Protecting the Claim

GraphOath provides two distinct, cleanly separated trust guarantees:

1. **Custody Ledger Integrity** (Protects the *Record*): SHA-256 hash chains guarantee that historical receipt payloads have not been tampered with or modified in PostgreSQL.
2. **Evidence-Drift Re-Verification** (Protects the *Claim*): Periodically re-queries live DataHub metadata to check if facts cited in an old receipt (e.g. dataset ownership or schema field presence) have since changed in the live graph.

```
 ┌─────────────────────────────────────────────────────────────┐
 │                Custody Receipt (rcpt_98f4a12b)               │
 │ Cited Fact: Owner = urn:li:corpuser:priya_ramaswamy         │
 └──────────────────────────────┬──────────────────────────────┘
                                │
                                ▼  Periodic Re-Verification Check
 ┌─────────────────────────────────────────────────────────────┐
 │            DataHub Live Metadata Query (MCP)                │
 │ Live Fact : Owner = urn:li:corpuser:marcus_webb             │
 └──────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │              Evidence Drift Detected & Flagged              │
 │ Flag: Receipt Citation Stale (Owner transferred 14 days ago)│
 └─────────────────────────────────────────────────────────────┘
```

---

## 2. Evidence Drift REST Endpoint

Governance administrators can execute background evidence-drift verification via REST:

```bash
curl -X POST "http://localhost:8000/api/receipts/verify-drift?receipt_id=rcpt_98f4a12b" \
     -H "Authorization: Bearer <governance_jwt>"
```

### JSON Response Body:
```json
{
  "receipt_id": "rcpt_98f4a12b",
  "ledger_integrity": "INTACT_UNMODIFIED",
  "evidence_drift_status": "CITATION_DRIFT_DETECTED",
  "drift_details": [
    {
      "urn": "urn:li:dataset:(snowflake,prod.stg_orders)",
      "cited_fact": "owner: priya_ramaswamy",
      "live_fact": "owner: marcus_webb",
      "drift_type": "OWNERSHIP_TRANSFER"
    }
  ]
}
```
