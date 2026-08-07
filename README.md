# GraphOath

**The citation-gated control plane for AI agents acting on DataHub.**

GraphOath sits between autonomous agents and your DataHub metadata graph. Before
any agent-initiated claim becomes an action — an incident, a Slack notification,
a write-back to the graph — every named entity in that claim must resolve to a
specific, queryable fact in DataHub. No evidence, no action. Every action that
does execute is permanently recorded in a tamper-evident ledger.

This submission implements **Deposition**, GraphOath's first module: on a
schema-breaking change, it walks DataHub's lineage graph, assembles a cited
evidence package, and raises a **native DataHub Incident** — composing with
DataHub's existing Incident entity and Actions framework rather than
duplicating them — with the full evidence trail attached as a linked receipt.

## Hackathon track

Submitted under **Agents That Do Real Work**.

## The problem

Enterprise data teams lose a large share of engineering capacity to pipeline
firefighting and schema-drift maintenance, and AI-authored changes are trusted
and merged at roughly a third the rate of human-authored ones — not because the
agents are unhelpful, but because nothing forces an agent's claim to be
checkable before it's acted on. See `docs/vision.md` for the full problem
statement and supporting research.

## How it uses DataHub

- **Lineage, ownership, usage, and glossary queries** via the DataHub GraphQL
  API / Agent Context Kit, to build the evidence array behind every claim.
- **Native `raiseIncident` / `updateIncident` mutations** — Deposition does not
  build a parallel incident system; it extends DataHub's own Incident entity.
- **`emitMetadataChangeProposal`** to attach the receipt as a custom
  `graphoathReceipt` aspect, linked to the incident by urn, so the evidence
  trail is part of the graph itself and queryable by any future agent.
- **DataHub Actions framework** as the event source triggering Deposition on a
  schema or deprecation change.

Full architecture, data flow, and an ASCII infrastructure diagram: `docs/architecture.md`.

## Quick start

Full setup instructions, environment variables, and a troubleshooting matrix
live in `docs/installation.md`. Short version:

```bash
cp .env.example .env               # fill in DataHub + Slack + DB credentials
docker compose up -d postgres
python -m graphoath.db.migrate
python scripts/seed_showcase_datapack.py
docker compose up
```

Dashboard: `http://localhost:3000` · API: `http://localhost:8000/api`

## What's in this repo

| Path | Contents |
|---|---|
| `docs/` | Vision, PRD, architecture, API reference, security, and contributing docs |
| `src/graphoath/` | Python runtime — DataHub client, the Deposition pipeline, Custody ledger, API |
| `src/dashboard/` | Next.js operator dashboard |
| `examples/` | Real, generated receipts and screenshots from this submission |
| `tests/` | Unit and integration tests |

Full annotated tree: `docs/directory-structure.md`.

## Demo

[Link to the ≤3-minute demo video]

## Roadmap beyond this submission

Deposition is the first of six planned modules — Undertow (ML drift detection),
Prune (cost governance), Rosetta (knowledge capture), ReguLineage (ML
compliance provenance), and Redline (regulatory exposure tracking) — all
writing through the same Custody ledger. Full roadmap: `docs/project-scope.md`.

## License

Apache License 2.0 — see `LICENSE`.
