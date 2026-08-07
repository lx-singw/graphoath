# DataHub Agent Hackathon — GraphOath Alignment & Evaluation Blueprint

This document explicitly maps **GraphOath** to the **Build with DataHub: The Agent Hackathon** tracks, challenge categories, technical requirements, and judging criteria. It is designed to provide judges with a clear evaluation blueprint showing how GraphOath directly fulfills the hackathon's mission: **grounding autonomous AI agents in enterprise data context**.

---

## 1. Executive Alignment Summary

| Hackathon Requirement | GraphOath Implementation | Location in Repo |
|---|---|---|
| **Core Mission** | Solves the AI agent hallucination / unverified write-action problem by enforcing that no agent action executes without a citation-backed proof chain in DataHub. | [`docs/vision.md`](docs/vision.md) |
| **Track Submitted** | **Agents That Do Real Work** | [`README.md`](README.md) |
| **DataHub Tech Stack** | Integrates with DataHub's **MCP Server**, **Agent Context Kit**, **GraphQL API** (`searchAcrossLineage`, `getDataset`), **Actions Framework**, and **Native Incidents** (`raiseIncident`). | [`docs/mcp-context-kit-guide.md`](docs/mcp-context-kit-guide.md) |
| **AI Framework Support** | Provides first-class integration tools and patterns for **LangChain**, **LangGraph**, **LlamaIndex**, and **Google ADK**. | [`docs/framework-integrations.md`](docs/framework-integrations.md) |
| **Proof of Context** | Custom aspect `graphoathReceipt` emitted via `emitMetadataChangeProposal` linking tamper-evident evidence directly into DataHub's metadata graph. | [`docs/architecture.md`](docs/architecture.md) |
| **Runnable Code** | Full end-to-end runnable Python agent scripts demonstrating MCP querying and citation gating. | [`examples/langchain_agent_example.py`](examples/langchain_agent_example.py) |

---

## 2. Challenge Category Alignment Matrix

GraphOath is submitted under **Agents That Do Real Work**, but its modular architecture directly satisfies all 4 challenge focus areas of the hackathon:

```
                  ┌──────────────────────────────────────────────┐
                  │          GraphOath Control Plane             │
                  └──────────────────────┬───────────────────────┘
                                         │
       ┌──────────────────┬──────────────┴───────┬──────────────────┐
       ▼                  ▼                      ▼                  ▼
┌──────────────┐   ┌──────────────┐       ┌──────────────┐   ┌──────────────┐
│  Track 1:    │   │  Track 2:    │       │  Track 3:    │   │  Track 4:    │
│ Real Work &  │   │  Autonomous  │       │  Context     │   │ Frameworks & │
│ Firefighting │   │ Data Handling│       │ Governance   │   │ MCP Tooling  │
└──────────────┘   └──────────────┘       └──────────────┘   └──────────────┘
```

### Track 1: Agents That Do Real Work (Primary Track)
* **Goal**: Build agents that solve real operational data problems rather than toy tasks.
* **GraphOath Solution**: **Deposition** (GraphOath's flagship module) automates schema-break triage. When a breaking schema change occurs, Deposition walks the downstream lineage graph, calculates blast radius, identifies dataset owners, and raises a native DataHub Incident with owner routing in under 60 seconds.

### Track 2: Autonomous Data Handling & Remediation
* **Goal**: Build agents that independently navigate, inspect, and safely interact with data pipelines.
* **GraphOath Solution**: GraphOath acts as the safety harness for autonomous data handling. It allows agents to autonomously suggest pipeline fixes, dataset deprecations, or incidents, but intercepts every claim before execution. If an entity named by the agent cannot be verified against DataHub's live graph, the action is blocked.

### Track 3: Context-Grounded Operations & Hallucination Prevention
* **Goal**: Ensure agents are grounded in metadata (schemas, lineage, ownership, quality) rather than LLM assumptions.
* **GraphOath Solution**: GraphOath's **Citation Gate** (`gate.py`) is a pure verification function that cross-references every claims array with DataHub's metadata graph (retrieved via MCP / Agent Context Kit). Uncited claims are rejected, preventing hallucinated asset URNs from reaching production systems.

### Track 4: Tooling & AI Framework Integration
* **Goal**: Seamlessly combine DataHub context tools with standard agent frameworks (LangChain, LangGraph, ADK).
* **GraphOath Solution**: GraphOath provides custom wrappers (`GraphOathCitationTool`, `CitationGateNode`) that plug directly into LangChain tools and LangGraph stateful DAGs, showing how any enterprise agent framework can incorporate citation gating.

---

## 3. Judging Criteria Evaluation Rubric

| Judging Criterion | Weight | How GraphOath Scores Maximum Points | Reference |
|---|---|---|---|
| **Impact & Value** | 25% | Solves pipeline downtime and unverified AI actions—a top pain point for data platform teams. Automates triage while guaranteeing compliance. | [`docs/vision.md`](docs/vision.md) |
| **Depth of DataHub Integration** | 25% | Composes natively with DataHub: uses GraphQL, Actions framework, MCP Server, Agent Context Kit, `raiseIncident` mutation, and custom `graphoathReceipt` aspects. | [`docs/architecture.md`](docs/architecture.md) |
| **Technical Rigor & Security** | 25% | Implements a hash-chained tamper-evident Custody ledger in Postgres (SHA-256 chain) backed by cryptographic receipts and human approval workflows for destructive actions. | [`docs/security.md`](docs/security.md) |
| **User Experience & Completeness** | 25% | Ships with an operator dashboard (Next.js), comprehensive documentation, OpenAPI REST specifications, and runnable end-to-end Python demo scripts. | [`examples/README.md`](examples/README.md) |

---

## 4. Key Architectural Differentiators for Judges

1. **Native Composition, Zero Duplication**: GraphOath does *not* build a secondary incident tracker or a separate metadata catalog. It raises native DataHub Incidents (`raiseIncident`) and attaches receipts back to DataHub entity URNs (`graphoathReceipt` aspect).
2. **Cryptographic Tamper-Evidence**: Receipts are stored in a dual format—queryable in DataHub's graph and immutable in GraphOath's Postgres hash ledger (`receipts` table with `hash_chain`).
3. **Citation Gating Architecture**: The citation gate is deterministic and zero-network during evaluation, ensuring low-latency enforcement.

---

## 5. Verification & Demo Walkthrough

Judges can verify GraphOath in two ways:
1. **Interactive Demo Scripts**: Run `python examples/mock_mcp_citation_demo.py` or `python examples/langchain_agent_example.py`.
2. **Full Stack Docker Deployment**: Follow [`docs/installation.md`](docs/installation.md) to launch the API and Next.js operator dashboard.
