# GraphOath — API Reference

Base URL (local development): `http://localhost:8000/api`
Base URL (production): `https://api.graphoath.example.com/api`

All endpoints except `/auth/login` require a bearer token issued by
`/auth/login`, sent as `Authorization: Bearer <token>`. All request and response
bodies are JSON, `Content-Type: application/json`.

---

## POST /auth/login

Authenticates a dashboard user and issues an access token and refresh token.

**Request:**

```json
{
  "email": "priya.ramaswamy@example-fintech.com",
  "password": "correct-horse-battery-staple-9x"
}
```

**Response — 200 OK:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c3JfM2Y3YTljIiwicm9sZSI6Im9wZXJhdG9yIiwiZXhwIjoxNzM4ODAwMDAwfQ.9pQe1z-3sVh6yqjK2Y8kQxN0lX0pQyR4kT8v5wZ1BdU",
  "refresh_token": "rtok_8f3e9c2a1b4d6e7f9a0c1b2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f",
  "token_type": "bearer",
  "expires_in": 43200,
  "user": {
    "id": "usr_3f7a9c",
    "email": "priya.ramaswamy@example-fintech.com",
    "role": "operator",
    "organization_id": "org_8b2e1f"
  }
}
```

**Status codes:**

- `200 OK` — credentials valid, tokens issued.
- `401 Unauthorized` — email/password combination does not match a record.
- `422 Unprocessable Entity` — request body missing `email` or `password`, or
  `email` is not a valid email format.
- `500 Internal Server Error` — the auth database is unreachable.

---

## POST /auth/refresh

Exchanges a valid, unexpired refresh token for a new access token.

**Request:**

```json
{
  "refresh_token": "rtok_8f3e9c2a1b4d6e7f9a0c1b2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f"
}
```

**Response — 200 OK:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c3JfM2Y3YTljIiwicm9sZSI6Im9wZXJhdG9yIiwiZXhwIjoxNzM4ODQzMjAwfQ.qX8z2Nb0V4a6Y1jK7wR3sT9pQoL5mE2cA1fD6gH8iJk",
  "token_type": "bearer",
  "expires_in": 43200
}
```

**Status codes:**

- `200 OK` — new access token issued.
- `401 Unauthorized` — refresh token is expired, revoked, or unrecognized.
- `422 Unprocessable Entity` — `refresh_token` field missing from body.

---

## GET /receipts

Lists receipts, most recent first, with optional filtering.

**Query parameters:** `urn` (filter by DataHub entity urn), `module` (e.g.
`deposition`), `from`, `to` (ISO-8601 date range), `limit` (default 25, max
200), `cursor` (pagination cursor).

**Response — 200 OK:**

```json
{
  "receipts": [
    {
      "receipt_id": "rcpt_2026-08-05T14:32:07Z-0091",
      "module": "deposition",
      "created_at": "2026-08-05T14:32:07Z",
      "trigger": {
        "event": "field_removed",
        "urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,ecommerce.fct_orders,PROD)",
        "field": "customer_region"
      },
      "claim": "Removing customer_region will affect churn-overview and churn_model_v3",
      "incident_urn": "urn:li:incident:5f2a9c3e-7b1d-4a6f-9e0c-1d2b3a4c5d6e",
      "hash": "9f2a1e7c3b5d8f0a2c4e6b8d0f1a3c5e7b9d1f3a5c7e9b1d3f5a7c9e1b3d5f7a",
      "prev_hash": "7c11de88f4a2b6c8e0d2f4a6c8e0b2d4f6a8c0e2b4d6f8a0c2e4b6d8f0a2c4e6"
    }
  ],
  "next_cursor": "eyJvZmZzZXQiOjI1fQ==",
  "total_count": 342
}
```

**Status codes:**

- `200 OK` — list returned, possibly empty (`"receipts": []`).
- `400 Bad Request` — `from` is later than `to`, or `limit` exceeds 200.
- `401 Unauthorized` — missing or invalid bearer token.

---

## GET /receipts/{receipt_id}

Retrieves a single receipt with its full evidence array.

**Response — 200 OK:**

```json
{
  "receipt_id": "rcpt_2026-08-05T14:32:07Z-0091",
  "module": "deposition",
  "created_at": "2026-08-05T14:32:07Z",
  "trigger": {
    "event": "field_removed",
    "urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,ecommerce.fct_orders,PROD)",
    "field": "customer_region"
  },
  "claim": "Removing customer_region will affect churn-overview and churn_model_v3",
  "evidence": [
    {
      "type": "lineage",
      "call": "searchAcrossLineage(urn, direction=DOWNSTREAM, degree=2)",
      "result_urn": "urn:li:dashboard:(looker,churn-overview)",
      "hops": 2
    },
    {
      "type": "lineage",
      "call": "searchAcrossLineage(urn, direction=DOWNSTREAM, degree=1)",
      "result_urn": "urn:li:mlFeatureTable:(churn_model_v3,region_bucket)",
      "hops": 1
    },
    {
      "type": "ownership",
      "call": "getOwnership(urn=churn-overview)",
      "result": "team-growth-analytics"
    },
    {
      "type": "usage",
      "call": "getUsageStats(urn=churn-overview, window=30d)",
      "result": "340 queries/week"
    }
  ],
  "confidence": "high",
  "action_taken": {
    "type": "raise_incident",
    "incident_urn": "urn:li:incident:5f2a9c3e-7b1d-4a6f-9e0c-1d2b3a4c5d6e",
    "target_channel": "#team-growth-analytics",
    "reversible": true,
    "requires_approval": false
  },
  "hash": "9f2a1e7c3b5d8f0a2c4e6b8d0f1a3c5e7b9d1f3a5c7e9b1d3f5a7c9e1b3d5f7a",
  "prev_hash": "7c11de88f4a2b6c8e0d2f4a6c8e0b2d4f6a8c0e2b4d6f8a0c2e4b6d8f0a2c4e6",
  "prior_receipts": ["rcpt_2026-07-12T09:14:22Z-0044"],
  "memory_note": "2nd occurrence in 30 days, same root cause"
}
```

**Status codes:**

- `200 OK` — receipt found and returned.
- `404 Not Found` — no receipt exists with the given `receipt_id`.
- `401 Unauthorized` — missing or invalid bearer token.

---

## GET /incidents/{incident_urn}

Retrieves the native DataHub Incident and any GraphOath receipts linked to it.
`incident_urn` must be URL-encoded.

**Response — 200 OK:**

```json
{
  "incident_urn": "urn:li:incident:5f2a9c3e-7b1d-4a6f-9e0c-1d2b3a4c5d6e",
  "status": "ACTIVE",
  "priority": "HIGH",
  "type": "DATA_SCHEMA",
  "assignees": ["team-growth-analytics"],
  "created_at": "2026-08-05T14:32:08Z",
  "linked_receipts": ["rcpt_2026-08-05T14:32:07Z-0091"]
}
```

**Status codes:**

- `200 OK` — incident found.
- `404 Not Found` — no incident exists with the given urn, or it is not visible
  to the authenticated organization.
- `502 Bad Gateway` — DataHub instance unreachable when resolving live incident
  status.

---

## POST /approvals/{action_id}/approve

Approves a pending `requires_approval: true` action, allowing it to execute.

**Request:**

```json
{
  "approver_note": "Confirmed with data-eng lead, safe to deprecate."
}
```

**Response — 200 OK:**

```json
{
  "action_id": "act_7d3e1f9c",
  "status": "approved",
  "approved_by": "usr_3f7a9c",
  "approved_at": "2026-08-05T15:02:11Z",
  "receipt_id": "rcpt_2026-08-05T15:02:12Z-0092"
}
```

**Status codes:**

- `200 OK` — approval recorded and the pending action executed.
- `403 Forbidden` — authenticated user's role is `operator` but the action
  requires `governance_admin` (configurable per action type).
- `404 Not Found` — no pending action exists with the given `action_id`.
- `409 Conflict` — the action was already approved or denied.

---

## POST /approvals/{action_id}/deny

**Request:**

```json
{
  "reason": "Table is referenced in an active migration, hold for now."
}
```

**Response — 200 OK:**

```json
{
  "action_id": "act_7d3e1f9c",
  "status": "denied",
  "denied_by": "usr_3f7a9c",
  "denied_at": "2026-08-05T15:03:44Z"
}
```

**Status codes:** same pattern as `/approve` above.

---

## GET /ledger/verify

Runs the hash-chain integrity check across the full ledger, or a bounded range.

**Query parameters:** `from_receipt_id`, `to_receipt_id` (optional; full ledger
checked if omitted).

**Response — 200 OK (chain intact):**

```json
{
  "status": "intact",
  "receipts_checked": 342,
  "checked_at": "2026-08-05T16:00:00Z"
}
```

**Response — 200 OK (break detected):**

```json
{
  "status": "broken",
  "receipts_checked": 342,
  "break_at_receipt_id": "rcpt_2026-07-30T11:04:55Z-0071",
  "expected_hash": "3a5c7e9b1d3f5a7c9e1b3d5f7a9c1e3b5d7f9a1c3e5b7d9f1a3c5e7b9d1f3a5c",
  "actual_hash": "0000000000000000000000000000000000000000000000000000000000000",
  "checked_at": "2026-08-05T16:00:00Z"
}
```

**Status codes:**

- `200 OK` — check completed (result may still indicate `"status": "broken"`).
- `403 Forbidden` — authenticated user is not `governance_admin`.
- `500 Internal Server Error` — ledger database unreachable mid-check.

---

## POST /exports

Requests a compliance export (US-05 in `docs/prd.md`).

**Request:**

```json
{
  "from": "2026-01-01",
  "to": "2026-06-30",
  "format": "pdf"
}
```

**Response — 201 Created:**

```json
{
  "export_id": "exp_4b8d2f1a",
  "status": "processing",
  "requested_by": "usr_3f7a9c",
  "estimated_completion_seconds": 12
}
```

**Status codes:**

- `201 Created` — export job accepted and queued.
- `400 Bad Request` — date range exceeds 12 months, or `format` is not `pdf` or
  `csv`.
- `403 Forbidden` — authenticated user's role is not `governance_admin`.
- `422 Unprocessable Entity` — `from` or `to` is not a valid ISO-8601 date.
