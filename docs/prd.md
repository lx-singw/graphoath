# GraphOath — Product Requirements Document

## 1. User Personas

### Persona A — Priya Ramaswamy, Data Platform Engineer

- **Role:** Owns the DataHub deployment and the CI/CD pipelines for ~340 dbt
  models and 60 Airflow DAGs at a mid-sized fintech.
- **Goals:** Reduce the hours she personally spends tracing "what broke" after a
  schema change; stop being the only person who understands the full lineage
  graph; get incidents routed to the correct owning team without manual triage.
- **Pain today:** She is paged for schema-drift incidents regardless of whether
  her team owns the downstream asset, because nothing else in the stack computes
  blast radius fast enough to route correctly.
- **Success looks like:** A schema change automatically produces a DataHub
  Incident with the right owner already assigned and a receipt she can open in
  under ten seconds to see exactly why the agent concluded what it concluded.

### Persona B — Marcus Webb, Head of Data Governance

- **Role:** Accountable to the CISO and to external auditors for demonstrating
  that changes to regulated data are tracked, explainable, and reversible.
- **Goals:** Produce an audit trail for any agent-initiated action within
  minutes of a request, not days of log spelunking; demonstrate to auditors that
  no autonomous system silently modified production data without a recorded,
  evidence-backed justification.
- **Pain today:** Existing AI tooling in his organization has no consistent
  record of *why* an action was taken — only that it was taken, if that.
- **Success looks like:** Every GraphOath-mediated action is retrievable from the
  Custody ledger with its full evidence chain, exportable as a compliance report
  without engineering involvement.

## 2. User Stories & Acceptance Criteria

| ID | User Story | Acceptance Criteria (Given/When/Then) |
|----|------------|-----------------------------------------|
| US-01 | As Priya, I want a schema-breaking change to automatically produce a routed incident, so that I am not the default responder for teams I don't support. | **Given** a `schemaMetadata` change is emitted for a dataset with active downstream lineage, **when** the Deposition agent processes the change event, **then** a DataHub Incident is raised via `raiseIncident` with `assignees` populated from the DataHub ownership aspect of the most-affected downstream asset, within 60 seconds of the triggering event. |
| US-02 | As Priya, I want to see the exact evidence behind an incident's claim, so that I can trust it without re-deriving the lineage myself. | **Given** an incident was raised by Deposition, **when** I open its linked receipt in the dashboard, **then** I see the full evidence array (lineage hops, ownership records, usage stats) each linked to the live DataHub urn it was drawn from. |
| US-03 | As Priya, I want the agent to refuse to name a downstream asset it cannot support with evidence, so that I never have to fact-check its output. | **Given** the evidence-gathering step returns a lineage hop with no resolvable ownership or usage data, **when** the receipt is assembled, **then** that asset is either re-queried through an alternate evidence path or dropped from the claim text entirely — it is never included in the human-facing summary without a corresponding evidence entry. |
| US-04 | As Marcus, I want every GraphOath action logged immutably, so that I can produce an audit trail on demand. | **Given** any action is executed by any GraphOath module, **when** the action completes, **then** a receipt is written to the Custody ledger with a SHA-256 hash chained to the prior entry, and the write is rejected if the prior-hash reference does not match the ledger's current head. |
| US-05 | As Marcus, I want to export a compliance report for a date range without engineering help, so that audit requests do not become engineering tickets. | **Given** I am authenticated as a user with the `governance_admin` role, **when** I request an export for a date range via the dashboard, **then** I receive a signed PDF or CSV containing every receipt in that range, its linked incident, and its full evidence chain, generated in under 30 seconds for ranges up to 12 months. |
| US-06 | As Priya, I want destructive actions to require my approval, so that an agent cannot deprecate or delete an asset without a human in the loop. | **Given** an action is classified `requires_approval: true` (e.g., dataset deprecation), **when** the validation gate passes, **then** the action is posted to the designated Slack channel with an Approve/Deny control and does not execute until an approval event is recorded in the receipt. |
| US-07 | As Marcus, I want to know immediately if the ledger has been tampered with, so that I can trust its evidentiary value. | **Given** the Custody ledger contains N receipts, **when** an integrity check is run (on-demand or on a nightly schedule), **then** the system recomputes the hash chain from the genesis receipt and flags any index where the stored hash does not match the recomputed hash. |

## 3. Functional Requirements

- **FR-1:** The system shall subscribe to DataHub schema and deprecation change
  events via the DataHub Actions framework or equivalent polling fallback.
- **FR-2:** The system shall compute downstream lineage impact using
  `searchAcrossLineage` (or the MCP Server / Agent Context Kit equivalent) to a
  configurable maximum hop depth, default 3.
- **FR-3:** The system shall reject any claim containing a named entity with no
  corresponding evidence record before that claim reaches an execution step.
- **FR-4:** The system shall raise and update incidents using DataHub's native
  Incident GraphQL mutations rather than a custom incident entity.
- **FR-5:** The system shall write one Custody receipt per executed action,
  hash-chained to the immediately preceding receipt.
- **FR-6:** The system shall support a configurable allow-list of action types
  that require human approval before execution.
- **FR-7:** The system shall expose a dashboard view for any receipt, showing
  the claim, evidence array, and resulting action in human-readable form.

## 4. Non-Functional Requirements

| Category | Requirement |
|---|---|
| Latency | Incident raised within 60 seconds (p95) of the triggering DataHub change event, measured from event ingestion to `raiseIncident` mutation acknowledgment. |
| Scalability | Support lineage graphs of up to 50,000 dataset nodes and 250,000 edges without lineage-walk latency exceeding 5 seconds (p95) at 3-hop depth. |
| Availability | 99.5% uptime for the receipt-write path (evidence gathering and ledger writes), measured monthly. Read-only dashboard access target 99.9%. |
| Durability | Zero tolerance for silent receipt loss. Every write to the Custody ledger is confirmed via a read-back verification before the triggering action is marked complete. |
| Localization | Dashboard UI strings externalized via i18n resource files at MVP; English shipped at launch, structure supports adding locales without code changes. |
| Auditability | Every receipt retrievable by urn, incident ID, or date range within 2 seconds (p95) for ledgers up to 5 million receipts. |
| Security | All evidence and receipt data encrypted at rest (AES-256) and in transit (TLS 1.3 minimum). See `docs/security.md`. |

## 5. Data Retention & Deletion Policies

- **Receipts (Custody ledger):** Retained indefinitely by default, since the
  ledger's evidentiary value depends on completeness. Organizations subject to a
  defined data-minimization policy may configure a retention window (minimum 400
  days) after which receipt *bodies* are archived to cold storage while their
  hashes remain in the live chain — preserving chain integrity without retaining
  full evidence payloads indefinitely.
- **Evidence payload contents:** Evidence entries store DataHub urns and
  snapshot metadata, not raw customer data. No end-user PII is expected in a
  receipt; if a lineage evidence entry would surface PII (e.g., a column-level
  sample), the system redacts sample values and stores only the schema-level
  reference.
- **Session tokens and API credentials:** Access tokens issued to the dashboard
  expire after 12 hours; refresh tokens expire after 30 days of inactivity. DataHub
  service-account credentials used by the runtime are stored only as encrypted
  secrets (see `docs/security.md`) and are never written into receipt payloads.
- **Deletion requests:** An organization offboarding from GraphOath may request
  full ledger export followed by deletion. Deletion is a two-step process — a
  30-day soft-delete hold followed by irreversible purge — to prevent accidental
  loss of audit-relevant history during an active compliance review.
