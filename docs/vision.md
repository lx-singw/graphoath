# GraphOath — Vision

## Project Context

GraphOath is a control-plane platform that sits between autonomous AI agents and an
organization's DataHub metadata graph. It requires every agent-initiated claim and
write-back action to be validated against citable lineage, ownership, and usage
evidence before it is allowed to execute. The runtime is built on Python 3.12 and
FastAPI, backed by Postgres for a tamper-evident receipt ledger, with a Next.js/
TypeScript operator dashboard. GraphOath composes with DataHub's native Incident
entity, GraphQL API, MCP Server, and Agent Context Kit rather than duplicating
catalog functionality. Its first module, Deposition, walks DataHub's lineage graph
on schema-change events and raises a native DataHub Incident only once every claim
in its evidence package is backed by a specific, queryable fact. The target
audience is data platform teams and DataHub administrators at mid-to-large
enterprises running many interdependent pipelines, who need AI agents to act on
their metadata without hallucinating impact or acting without an audit trail.

## Executive Summary

Every enterprise adopting AI agents for data operations faces the same unresolved
question: what happens the first time an agent is wrong, and nobody can reconstruct
why it did what it did? Catalog vendors have spent the last eighteen months
racing to give agents *read* access to metadata — native MCP servers, GraphQL
endpoints, agent-context SDKs. Almost none of them have addressed the *write* side:
what an agent is allowed to assert, what evidence that assertion has to rest on,
and what permanent record exists once the agent has acted.

GraphOath is that missing layer. It does not compete with DataHub, Atlan, or
Collibra as a catalog. It sits downstream of them, as the control plane every
agent — first-party or third-party — has to pass through before a claim it makes
about the data estate is allowed to become an action. Every claim is checked
against live evidence before execution; every action that does execute is written,
permanently and verifiably, to a ledger that the next agent or human inherits.

## Problem Statement

Three converging failures define the current state of agentic data operations:

1. **Agents claim things they cannot support.** An LLM asked "what breaks if we
   drop this column" will answer fluently whether or not it queried anything.
   Nothing in the current agent-tooling stack forces a claim to be backed by a
   specific, checkable fact before it is acted on.
2. **Nobody trusts agent-authored changes, and the data backs that instinct up.**
   AI-authored pull requests are accepted at roughly a third the rate of
   human-authored ones, and a meaningful share of AI-generated changes that pass
   automated review still require manual debugging once they reach production.
   The bottleneck is not generation speed — it is verification cost.
3. **When an agent does act, the reasoning behind that action evaporates.** A
   Slack message gets sent, an incident gets filed, a PR gets opened — and the
   evidence trail that justified it lives, if anywhere, in a chat log nobody will
   find during the next audit or the next postmortem.

Enterprises running hundreds of interdependent pipelines already lose a large
share of engineering capacity to firefighting and schema-drift maintenance before
any agent is introduced. Layering ungoverned autonomous agents on top of that
environment does not reduce the fire; it adds an actor that can start new ones
faster than a human ever could.

## Value Proposition

GraphOath's differentiation is structural, not cosmetic:

- **Claims require citations, mechanically, not by convention.** Every assertion
  a GraphOath-governed agent makes is checked against DataHub lineage, ownership,
  usage, and glossary data at the moment of action. A claim with no matching
  evidence is rejected or routed back for more evidence — it is never allowed to
  reach a human or another system unverified.
- **We extend DataHub's own model instead of rebuilding it.** Incidents raised by
  GraphOath are native DataHub Incident entities, not a parallel bookkeeping
  system. GraphOath adds the evidence and citation layer DataHub does not have;
  it does not reinvent the incident, ownership, or lineage primitives DataHub
  already ships.
- **Every action is permanently and verifiably recorded.** The Custody ledger is
  hash-chained and append-only. A receipt is not a log line that can quietly
  disappear; it is evidence that the action was taken for a specific, checkable
  reason, retrievable by any future agent or auditor.
- **The moat compounds with usage, not just with code.** Every incident, every
  blocked claim, every resolved receipt becomes part of an organization's history
  of how its agents actually behaved — a dataset a competitor cannot buy or
  replicate by shipping a similar feature next quarter.

## Long-Term Vision (3–5 Years)

**Year 1 — Prove the primitive.** Ship Deposition as the flagship module:
lineage-triggered, citation-gated incident response, composed directly with
DataHub's native Incident entity. Establish Custody as the ledger every other
module writes through.

**Year 2 — Expand the module family, one evidentiary domain at a time.**
- *Undertow* — continuous ML lineage monitoring that catches training-serving
  skew before it becomes a business-metric incident.
- *Prune* — cost-governance agent that identifies orphaned pipelines with zero
  downstream consumers and drafts their deprecation.
- *Rosetta* — knowledge-capture agent that mines Slack threads and postmortems
  for undocumented tribal knowledge and proposes glossary updates.
- *ReguLineage* — regulatory-exposure tracing for ML features, flagging PII or
  restricted data that entered a training set without proper classification.
- *Redline* — schema and lineage change monitoring for new regulatory exposure
  under frameworks such as GDPR and the EU AI Act.

**Year 3 — Become the default write-path for third-party agents, not just our
own.** Publish the Custody protocol as an open specification so agents built by
other teams — internal or vendor — can submit claims through the same
citation-gate and land in the same ledger. GraphOath's value shifts from "the
agents we built" to "the layer every agent, regardless of origin, is expected to
clear."

**Year 4–5 — The ledger becomes a portable trust asset.** With multiple years of
incident, compliance, and data-quality history accumulated per customer, package
that history as a cryptographically verifiable trust record — usable in B2B data
marketplace transactions, M&A technical due diligence, and cyber-insurance
underwriting. This is the point at which GraphOath stops being a tool that
governs agents and becomes the record of trust those agents' actions have
earned — a dataset with no substitute, because there is no shortcut to having
actually generated the history.
