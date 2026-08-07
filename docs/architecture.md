# GraphOath — System Architecture

## 1. Architectural Style

GraphOath is an **event-driven, single-service backend with a modular pipeline
core**, not a microservices mesh. This is a deliberate choice, not a shortcut:
the citation-gate mechanic depends on a tight, debuggable causal chain from event
to evidence to gate to action, and splitting that chain across service boundaries
would trade demo and operational reliability for an architectural purity the
system does not yet need at MVP scale. Each module (Deposition today; Undertow,
Prune, Rosetta, ReguLineage, and Redline in the roadmap) is an isolated Python
package under `src/graphoath/modules/`, sharing the same DataHub client and the
same Custody ledger writer, but independently deployable behind a feature flag
once module count and load justify splitting them into separate worker
processes.

## 2. Components

### 2.1 Frontend — Operator Dashboard (Next.js)

A read-mostly interface for two audiences: platform engineers inspecting a
specific receipt's evidence chain, and governance staff reviewing or exporting
the ledger. It communicates with the backend exclusively through the REST API
defined in `docs/api-reference.md`; it holds no DataHub credentials and cannot
trigger DataHub write actions directly. Approval actions (US-06) are the one
write path exposed to the dashboard, and they are scoped to the `operator` role.

### 2.2 Gateway / Reverse Proxy

An Nginx (or equivalent) reverse proxy terminates TLS, enforces the CORS policy
defined in `docs/security.md`, and routes `/api/*` to the FastAPI service and all
other paths to the Next.js server. Rate limiting (per-IP and per-token) is
enforced at this layer before requests reach application code.

### 2.3 Auth Service

Authentication is handled within the FastAPI application rather than as a
separate service at MVP scale, using OAuth 2.0 authorization-code flow for
dashboard users and short-lived JWTs for session state. Role assignment
(`operator` vs. `governance_admin`) is stored in Postgres and checked as FastAPI
dependency injection on every protected route. See `docs/security.md` for the
full token lifecycle.

### 2.4 Module Pipeline (Deposition, and future modules)

Each module implements the same four-stage interface:

1. **Trigger** — subscribes to a DataHub event source (Actions framework
   webhook, or a polling fallback) and normalizes it into an internal event
   object.
2. **Evidence** — queries DataHub (via the `datahub/` client, itself backed by
   the MCP Server / Agent Context Kit / direct GraphQL as appropriate per call)
   to build an evidence array of urns, relationships, and supporting facts.
3. **Gate** — a pure function with no network calls: given a draft claim string
   and an evidence array, returns either an approved claim (every named entity
   resolves to an evidence entry) or a rejection with the specific unsupported
   entities named, so the evidence stage can be re-run or the claim trimmed.
4. **Action** — executes the DataHub write (e.g., `raiseIncident`) and, in the
   same transaction, writes the resulting receipt to Custody.

### 2.5 DataHub Integration Layer

A single Python package (`src/graphoath/datahub/`) wrapping all outbound calls
to DataHub: `lineage.py` for `searchAcrossLineage`, `ownership.py` and
`usage.py` for their respective queries, and `incidents.py` for the native
`raiseIncident` / `updateIncident` mutations. Every module calls DataHub only
through this layer — never directly — so that authentication, retry policy, and
MCP Server vs. direct GraphQL routing are configured in exactly one place.

### 2.6 Custody (Ledger)

The persistence layer for every receipt, independent of which module produced
it. A receipt is written to two places in the same logical transaction: as a
`graphoathReceipt` custom aspect on the relevant DataHub entity (via
`emitMetadataChangeProposal`), so the evidence is part of the graph itself and
queryable by any future agent; and as a row in the Postgres `receipts` table,
hash-chained to the prior row, which is the tamper-evidence mechanism described
in `docs/security.md`.

### 2.7 Database / Graph Engine

DataHub itself is the graph engine of record for lineage, ownership, usage, and
glossary data — GraphOath does not maintain a competing graph. Postgres is used
exclusively for GraphOath's own operational state: the hash-chained receipts
table, user/role records, and approval-workflow state.

## 3. Data Flow — Schema Change to Recorded Incident

1. A schema field is removed or deprecated on a DataHub dataset, either through
   normal pipeline operation or (in the hackathon build) a manually triggered
   `emitMetadataChangeProposal` call.
2. DataHub's Actions framework (or the polling fallback) delivers the resulting
   `MetadataChangeLog` event to Deposition's `trigger.py`.
3. `evidence.py` calls `searchAcrossLineage` from the changed urn, direction
   `DOWNSTREAM`, to the configured hop depth (default 3), then calls
   `getOwnership` and `getUsageStats` for each returned urn.
4. A draft claim string is generated referencing the affected downstream assets,
   alongside the full evidence array backing each reference.
5. `gate.py` checks every named entity in the claim string against the evidence
   array. Any entity without a matching evidence record is either dropped from
   the claim or triggers a re-query of `evidence.py` for that specific urn
   (configurable retry limit, default 1).
6. Once the gate passes, `action.py` calls `raiseIncident` against DataHub's
   native Incident entity, with `assignees` populated from the ownership record
   of the most-affected downstream asset and `priority` derived from usage
   volume.
7. In the same logical transaction, Custody writes the `graphoathReceipt` aspect
   (linked to the new incident's urn) and appends a row to the Postgres
   `receipts` table, computing `hash = SHA256(prev_hash + canonical_json(receipt))`.
8. If the action is classified `requires_approval: true` (not applicable to a
   basic incident raise, but applicable to destructive actions in later
   modules), execution pauses at this step pending a Slack approval event before
   the receipt is finalized.
9. The dashboard's `/receipts/{receiptId}` view becomes queryable immediately
   after the ledger write is confirmed via read-back.

## 4. ASCII Infrastructure Diagram

```
                         ┌─────────────────────────┐
                         │   DataHub Instance       │
                         │  (Actions / MCP Server /  │
                         │   Agent Context Kit /    │
                         │   GraphQL API)           │
                         └───────────┬──────────────┘
                                     │ schema change event
                                     ▼
        ┌────────────────────────────────────────────────┐
        │                FastAPI Runtime                  │
        │  ┌──────────────────────────────────────────┐  │
        │  │           Deposition Module               │  │
        │  │  trigger.py → evidence.py → gate.py        │  │
        │  │                     │                       │  │
        │  │                     ▼                       │  │
        │  │                 action.py ──────────────┐   │  │
        │  └─────────────────────┼──────────────────┼───┘  │
        │                        │                  │       │
        │              raiseIncident (native)   write receipt│
        │                        │                  │       │
        │                        ▼                  ▼       │
        │              ┌──────────────┐   ┌───────────────┐ │
        │              │ DataHub       │   │  Custody       │ │
        │              │ Incident      │   │  (Postgres +   │ │
        │              │ entity        │   │  graphoath     │ │
        │              │               │   │  Receipt       │ │
        │              │               │   │  aspect)       │ │
        │              └──────────────┘   └───────┬───────┘ │
        │                                          │         │
        │                        ┌─────────────────┘         │
        │                        ▼                            │
        │              ┌──────────────────┐                  │
        │              │  REST API layer   │                  │
        │              │  /api/receipts    │                  │
        │              │  /api/incidents   │                  │
        │              └────────┬──────────┘                  │
        └───────────────────────┼─────────────────────────────┘
                                 │
                                 ▼
                    ┌──────────────────────┐
                    │  Nginx Reverse Proxy  │
                    │  (TLS, CORS, rate      │
                    │   limiting)            │
                    └──────────┬────────────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │  Next.js Dashboard    │
                    │  /receipts/[id]        │
                    │  /ledger               │
                    └──────────────────────┘

External notification path:
        action.py ── Slack webhook (incident notification,
                       and Approve/Deny for gated actions)
```
