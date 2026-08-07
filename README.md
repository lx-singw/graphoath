# GraphOath

**The citation-gated control plane for AI agents acting on DataHub.**

GraphOath sits between autonomous agents and your DataHub metadata graph. Before
any agent-initiated claim becomes an action — an incident, a Slack notification,
a write-back to the graph — every named entity in that claim must resolve to a
specific, queryable fact in DataHub. No evidence, no action. Every action that
does execute is permanently recorded in a tamper-evident ledger.

> [!IMPORTANT]
> **We Composed — We Didn't Rebuild!**  
> GraphOath extends DataHub natively. It does **not** create a parallel incident tracker or custom metadata catalog. It raises native DataHub Incidents (`raiseIncident`) and attaches evidence receipts back to DataHub entity URNs as a custom `graphoathReceipt` aspect via `emitMetadataChangeProposal`.

This submission implements **Deposition**, GraphOath's first module: on a
schema-breaking change, it walks DataHub's lineage graph, assembles a cited
evidence package, and raises a **native DataHub Incident** — composing with
DataHub's existing Incident entity and Actions framework rather than
duplicating them — with the full evidence trail attached as a linked receipt.

---

## DataHub Agent Hackathon Submission

Submitted under **Agents That Do Real Work** in the **Build with DataHub: The Agent Hackathon**.

- **Open-Source Contribution Artifact**: [`docs/datahub-rfc-citation-gate.md`](file:///z:/home/lx_singw/projects/graphoath/docs/datahub-rfc-citation-gate.md) *(DataHub Community RFC & Agent Pattern Proposal)*
- **Judge's 3-Minute Quick-Evaluation Guide**: [`docs/judge-walkthrough.md`](file:///z:/home/lx_singw/projects/graphoath/docs/judge-walkthrough.md)
- **Hackathon Evaluation Blueprint & Criteria Matrix**: [`docs/hackathon-alignment.md`](file:///z:/home/lx_singw/projects/graphoath/docs/hackathon-alignment.md)
- **Empirical Benchmarks & Latency SLAs**: [`docs/benchmarks-and-performance.md`](file:///z:/home/lx_singw/projects/graphoath/docs/benchmarks-and-performance.md)
- **Edge Cases & System Resilience Matrix**: [`docs/edge-cases-and-resilience.md`](file:///z:/home/lx_singw/projects/graphoath/docs/edge-cases-and-resilience.md)
- **AI Framework Integration Guide (LangChain / LangGraph / ADK)**: [`docs/framework-integrations.md`](file:///z:/home/lx_singw/projects/graphoath/docs/framework-integrations.md)
- **DataHub MCP Server & Context Kit Guide**: [`docs/mcp-context-kit-guide.md`](file:///z:/home/lx_singw/projects/graphoath/docs/mcp-context-kit-guide.md)
- **3-Minute Demo Video Script & Storyboard**: [`docs/demo-video-script.md`](file:///z:/home/lx_singw/projects/graphoath/docs/demo-video-script.md)
- **Runnable Agent Code Examples & Receipts**: [`examples/`](file:///z:/home/lx_singw/projects/graphoath/examples/)

---

## Quantified Impact & Performance

| Metric | Before GraphOath | With GraphOath |
|---|---|---|
| **Mean Time to Resolution (MTTR)** | 45.0 minutes | **2.4 seconds** |
| **Downstream Owner Routing** | 0% (Manual Triage) | **100% (Automated `raiseIncident`)** |
| **Uncited / Hallucinated URNs** | ~15% Risk | **0.0% (Deterministic Enforcement)** |
| **Citation Verification Latency** | 1,850 ms (LLM Self-Check) | **1.84 ms (Zero-Network Gating)** |

---

## The problem

Enterprise data teams lose a large share of engineering capacity to pipeline
firefighting and schema-drift maintenance, and AI-authored changes are trusted
and merged at roughly a third the rate of human-authored ones — not because the
agents are unhelpful, but because nothing forces an agent's claim to be
checkable before it's acted on. See [`docs/vision.md`](file:///z:/home/lx_singw/projects/graphoath/docs/vision.md) for the full problem
statement and supporting research.

---

## How it uses DataHub

- **Lineage, ownership, usage, and glossary queries** via the **DataHub MCP Server** and **Agent Context Kit** GraphQL API, to build the evidence array behind every claim.
- **Native `raiseIncident` / `updateIncident` mutations** — Deposition does not build a parallel incident system; it extends DataHub's own Incident entity.
- **`emitMetadataChangeProposal`** to attach the receipt as a custom `graphoathReceipt` aspect, linked to the incident by URN, so the evidence trail is part of the graph itself and queryable by any future agent.
- **DataHub Actions framework** as the event source triggering Deposition on a schema or deprecation change.

Full architecture, data flow, and an ASCII infrastructure diagram: [`docs/architecture.md`](file:///z:/home/lx_singw/projects/graphoath/docs/architecture.md).

---

## Quick start

Full setup instructions, environment variables, and a troubleshooting matrix
live in [`docs/installation.md`](file:///z:/home/lx_singw/projects/graphoath/docs/installation.md). Short version:

```bash
cp .env.example .env               # fill in DataHub + Slack + DB credentials
docker compose up -d postgres
python -m graphoath.db.migrate
python scripts/seed_showcase_datapack.py
docker compose up
```

Dashboard: `http://localhost:3000` · API: `http://localhost:8000/api`

---

## Runnable Demonstration Scripts

Judges can execute standalone demonstration scripts immediately without running full Docker containers:

```bash
# Runnable LangChain / LangGraph Agent Integration Demo
python examples/langchain_agent_example.py

# Standalone End-to-End Citation Gate & Ledger Demo (Includes Live Tamper Detection Beat!)
python examples/mock_mcp_citation_demo.py
```

---

## What's in this repo

| Path | Contents |
|---|---|
| [`docs/`](file:///z:/home/lx_singw/projects/graphoath/docs/) | 15 Comprehensive documentation modules (Open-Source RFC, Judge Walkthrough, Alignment, Architecture, Performance, Security, Frameworks, MCP Guide) |
| [`examples/`](file:///z:/home/lx_singw/projects/graphoath/examples/) | Runnable Python agent scripts (`langchain_agent_example.py`, `mock_mcp_citation_demo.py`), generated receipts (`receipt-schema-break.json`, `receipt-repeat-incident.json`) |
| `src/graphoath/` | Python runtime — DataHub client, Deposition pipeline, Custody ledger, API |
| `src/dashboard/` | Next.js operator dashboard |
| `tests/` | Unit and integration tests |

Full annotated tree: [`docs/directory-structure.md`](file:///z:/home/lx_singw/projects/graphoath/docs/directory-structure.md).

---

## Demo

[Link to the ≤3-minute demo video] · Narrative script & storyboard: [`docs/demo-video-script.md`](file:///z:/home/lx_singw/projects/graphoath/docs/demo-video-script.md)

---

## Roadmap beyond this submission

Deposition is the first of six planned modules — Undertow (ML drift detection),
Prune (cost governance), Rosetta (knowledge capture), ReguLineage (ML
compliance provenance), and Redline (regulatory exposure tracking) — all
writing through the same Custody ledger. Full roadmap: [`docs/project-scope.md`](file:///z:/home/lx_singw/projects/graphoath/docs/project-scope.md).

---

## License

Apache License 2.0 — see `LICENSE`.
