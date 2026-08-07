# GraphOath — DataHub Native Assertion-Triggered Incident Path

This document specifies how **GraphOath** integrates with **DataHub Native Assertions** (Data Quality test failures), expanding GraphOath's trigger sources beyond schema-drift changes.

---

## 1. Overview & DataHub Surface Area Expansion

Most data incidents in enterprise pipelines are caught by failing data quality tests (e.g. `dbt test`, Great Expectations, or DataHub Native Assertions) rather than column schema changes.

GraphOath subscribes directly to DataHub `AssertionRunEvent` changes:

```
 ┌─────────────────────────────────────────────────────────────┐
 │                DataHub AssertionRunEvent                    │
 │ (e.g., Row Count Assertion FAIL on prod.orders)            │
 └──────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │                Deposition Assertion Module                  │
 │  1. Extract Assertion URN & Dataset URN                     │
 │  2. Query Lineage Graph via MCP                             │
 │  3. Evaluate Citation Gate                                  │
 │  4. Raise Native Incident (IncidentType.DATA_QUALITY)       │
 └─────────────────────────────────────────────────────────────┘
```

---

## 2. Assertion Change Event Schema

When an assertion fails in DataHub, the event is normalized:

```json
{
  "event_type": "AssertionRunEvent_v1",
  "assertion_urn": "urn:li:assertion:4f8e910a-2b3c-4d5e-6f7a-8b9c0d1e2f3a",
  "dataset_urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)",
  "status": "FAILURE",
  "failure_type": "ROW_COUNT_ZERO",
  "timestamp": 1770452900
}
```

---

## 3. DataHub Native incident Creation (`IncidentType.DATA_QUALITY`)

Upon citation verification, Deposition calls native GraphQL `raiseIncident`:
- `type`: `DATA_QUALITY`
- `sourceProvider`: `GRAPHOATH_ASSERTION_MONITOR`
- `assignees`: Populated from downstream dataset owners (`getDatasetOwnership`).
