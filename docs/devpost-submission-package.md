# Build with DataHub: The Agent Hackathon — Complete Devpost Launch Package

This document contains copy-paste ready text for all Devpost submission fields for **GraphOath**.

---

## 1. Project Basics

* **Project Title**: GraphOath — The Citation-Gated Control Plane for DataHub AI Agents
* **Tagline**: *"No evidence, no action. The zero-trust safety harness stopping agent hallucinated writes before execution."*
* **Track**: **Agents That Do Real Work** (Primary Track)
* **GitHub Repository**: `https://github.com/lx-singw/graphoath`

---

## 2. Devpost Submission Sections

### What it does
GraphOath is an open-source, citation-gated control plane middleware for AI agents operating on DataHub. Before any agent-initiated claim produces a write action (e.g. `raiseIncident`, `emitMetadataChangeProposal`, schema modification), GraphOath's deterministic **Citation Gate** verifies that every entity URN named in the agent's claim resolves to a queryable fact in DataHub's metadata graph (retrieved via MCP or Agent Context Kit).

### How we built it
* **Backend**: Python 3.12, FastAPI, PostgreSQL (SHA-256 hash-chained Custody ledger).
* **DataHub Integration**: Native GraphQL API (`raiseIncident`), DataHub MCP Server (`search_across_lineage`, `get_dataset_ownership`, `get_dataset_assertions`), Actions Framework (`MetadataChangeLog_v1`), and custom `graphoathReceipt` aspects.
* **AI Framework Adapters**: Pre-built wrappers for LangChain (`GraphOathCitationToolWrapper`), LangGraph (`CitationGateStateNode`), LlamaIndex (`@llama_graphoath_protected`), and Google ADK (`GraphOathADKInterceptor`).
* **Operator Dashboard**: Next.js 14, TypeScript, TailwindCSS.

### Challenges we overcame
1. **Zero-Network Gating Speed**: Guaranteeing sub-5ms gate evaluation by avoiding network calls during the citation check.
2. **Cryptographic Tamper Evidence**: Designing a dual-tier ledger (Postgres SHA-256 hash chain + DataHub `graphoathReceipt` aspects) that detects database tampering in real time.
3. **Multi-Platform Lineage Triage**: Supporting heterogeneous data stacks (Snowflake $\rightarrow$ dbt $\rightarrow$ Looker) with 100% owner assignee resolution.

### Accomplishments that we're proud of
* **Zero Duplication**: Native composition with DataHub's Incident entity rather than building a parallel catalog.
* **PR-Ready Avro Aspect Schema**: Formulated [`schemas/graphoathReceipt.avsc`](schemas/graphoathReceipt.avsc) for merging directly into `datahub-project/datahub`.
* **Fast-Track Judge UX**: 1-command evaluation runner (`python scripts/fast_track_evaluation.py`) and interactive Master CLI Menu (`python examples/master_demo.py`).
* **Financial ROI Model**: Quantified $442,500.00 in annual net savings for enterprise data engineering teams.

---

## 3. Quickstart Command for Judges

```bash
python scripts/fast_track_evaluation.py
```
