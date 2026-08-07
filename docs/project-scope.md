# GraphOath — Project Scope

## 1. Hackathon Scope (48-Hour Execution Plan)

The hackathon build is a single vertical slice — Deposition end-to-end — cut down
to the smallest scope that still proves the citation-gate mechanic honestly on
real DataHub data. Everything else in this document is explicitly out of scope
for the hackathon build.

**In scope:**

- A manually-triggered "break this column" action that mutates a seeded dataset's
  schema via `emitMetadataChangeProposal` against the DataHub showcase-ecommerce
  datapack, producing a real change event rather than a simulated one.
- A single-file evidence-gathering routine: `searchAcrossLineage` to 2 hops,
  `getOwnership`, `getUsageStats` for each downstream urn.
- The citation-check gate as a plain Python function: every named entity in the
  generated claim string must resolve to an evidence-array entry, or it is
  dropped before the claim is finalized.
- Raising a native DataHub Incident via `raiseIncident`, with `assignees` set
  from the resolved ownership record.
- A Custody receipt written as a `graphoathReceipt` custom aspect attached to the
  raised incident, plus a single Postgres table storing
  `receipt_id, hash, prev_hash, payload`.
- A one-page Next.js view rendering a single receipt and a flat list of the
  ledger, for screenshots and the demo recording.
- An `examples/` folder containing at least two real, generated receipt JSON
  files and a screenshot of the resulting DataHub Incident and Slack message.

**Explicitly out of scope for the hackathon build:**

- Undertow, Prune, Rosetta, Redline, ReguLineage — referenced only in the
  written submission as roadmap, not built.
- The approval-gate workflow (US-06) — noted in the roadmap slide, not
  implemented, unless time remains after the above is demoed end-to-end.
- Multi-tenant auth, i18n, and the compliance-export feature (US-05).
- Any hosted deployment; the demo runs locally and is captured on video.

**Definition of done:** a single command starts the stack, a button click
produces a real schema-change event, and within the same run a DataHub Incident
exists with an attached receipt whose evidence array can be inspected in the
dashboard — recorded end-to-end in the submission video.

## 2. MVP Scope (Baseline Commercial Release)

The MVP is the first release a design partner could run against their own
DataHub instance, not a sandboxed demo dataset.

- **Core:** Deposition module fully productionized — DataHub Actions-based
  event subscription (not manual triggering), configurable hop depth, retry and
  backoff on lineage-walk failures, structured logging.
- **Security baseline:** OAuth-based dashboard authentication, encrypted secret
  storage for DataHub service-account credentials, role-based access
  (`operator`, `governance_admin`) as referenced in US-05.
- **Onboarding:** A guided setup flow that connects to a customer's DataHub
  instance, validates MCP Server / Agent Context Kit connectivity, and runs a
  dry-run evidence gather against a sample urn before enabling live event
  processing.
- **Stability:** Ledger integrity check (US-07) runs nightly and on demand;
  alerting if a hash-chain break is detected.
- **Approval gate:** Full implementation of US-06, including the Slack
  Approve/Deny workflow and approval events recorded in the receipt.
- **Deployment:** Documented, repeatable deployment via Docker Compose for
  self-hosted customers and a managed option on a single cloud provider.

## 3. Post-MVP Scope (Roadmap)

Ordered by the sequencing described in `docs/vision.md`:

- **Undertow (ML lineage monitoring):** Continuous comparison of live production
  feature data against training-time lineage snapshots to catch training-serving
  skew before it reaches a business metric.
- **Prune (cost governance):** Identification of pipelines and tables with zero
  downstream consumers over a rolling window, with draft deprecation PRs.
- **Rosetta (knowledge capture):** Mining of Slack threads, PR discussions, and
  postmortems for undocumented context, proposed back as DataHub glossary term
  PRs for human approval.
- **ReguLineage (ML provenance and compliance):** Tracing of ML feature lineage
  back to source columns to flag PII or restricted data entering a training set
  without proper classification.
- **Redline (regulatory exposure tracking):** Monitoring schema and lineage
  changes for newly created exposure under frameworks such as GDPR and the EU AI
  Act, with draft governance-tag updates.
- **Cross-agent memory:** Before re-diagnosing an incident, Deposition (and later
  modules) query Custody for prior receipts against the same urn, surfacing
  "this table broke twice in 30 days, same root cause" rather than starting from
  zero each time.
- **Third-party agent onboarding:** Publication of the Custody submission
  protocol so agents built outside GraphOath can submit claims through the same
  citation gate and land in the same ledger.
- **Monetization vectors:** Per-seat dashboard access for governance and platform
  teams; usage-based pricing on evidence-gather volume for the runtime; a
  compliance-export add-on tier for organizations with recurring audit
  obligations; and, in the long-term-vision timeframe, a portable trust-record
  product built on accumulated ledger history for use in data-marketplace and
  M&A due-diligence contexts.
