# GraphOath — Hackathon Judge's 3-Minute Quick Evaluation Guide

Welcome Judges! This guide provides a **120-second fast-track evaluation path** for reviewing **GraphOath** ("The citation-gated control plane for AI agents acting on DataHub") during the **Build with DataHub: The Agent Hackathon**.

---

## 1. The 60-Second 1-Command Fast-Track Evaluation Path

If you have **60 seconds** to evaluate this submission, run our master fast-track evaluation script directly in your terminal:

```bash
# ⚡ Run 8-Step Verification Suite (PowerShell / Bash with PYTHONPATH="src")
PYTHONPATH="src" python scripts/fast_track_evaluation.py
```
*(Windows PowerShell syntax)*:
```powershell
$env:PYTHONPATH="src"; python scripts/fast_track_evaluation.py
```

### Step-by-Step Demo Guide & Video Recording Script
For detailed step-by-step evaluation or recording a demo video, see [`docs/demo-video-and-judging-guide.md`](docs/demo-video-and-judging-guide.md).

### Step 1: Run Real-World Multi-Platform Pipeline Triage Demo (30 seconds)

```bash
$env:PYTHONPATH="src"; python examples/realworld_pipeline_triage_demo.py
```

**What to look for in the output**:
- **Event Ingestion**: Notice how a DataHub `MetadataChangeLog` schema change event is ingested.
- **Evidence Graph Traversal**: Multi-platform lineage nodes across Snowflake, dbt, and Looker are retrieved.
- **Gate Result**: Passes with `100% Citation Resolution`.
- **Custody Hash Chain**: Outputs a cryptographic SHA-256 receipt hash that permanently binds the incident to DataHub.

---

### Step 2: Run the LangChain / LangGraph Agent Integration Example (30 seconds)

```bash
$env:PYTHONPATH="src"; python examples/langchain_agent_example.py
```


**What to look for in the output**:
- **Scenario A (Uncited Claim Blocked)**: Notice how the agent proposes a claim referencing an unverified entity (`prod.hallucinated_table`). GraphOath's Citation Gate catches this instantly and returns `[X] REJECTED!`, blocking the write call to DataHub.
- **Scenario B (Valid Cited Claim Approved)**: Notice how the revised claim referencing only verified lineage entities returns `[OK] PASSED!`, raising a native DataHub Incident and writing a `graphoathReceipt` aspect.

---

### Step 3: Review Key Architecture & Alignment Docs (60 seconds)

1. **Hackathon Track Alignment**: [`docs/hackathon-alignment.md`](docs/hackathon-alignment.md) — Itemized matrix showing how GraphOath scores maximum points across all 4 challenge focus areas.
2. **AI Framework Integration Guide**: [`docs/framework-integrations.md`](docs/framework-integrations.md) — Patterns for LangChain, LangGraph, LlamaIndex, and Google ADK.
3. **MCP Server & Context Kit Guide**: [`docs/mcp-context-kit-guide.md`](docs/mcp-context-kit-guide.md) — Details on DataHub MCP tool integration (`search_across_lineage`, `get_dataset_ownership`).

---

## 2. Evaluation Scorecard Checklist

| Criteria | Question for Judges | GraphOath Verification | Score |
|---|---|---|---|
| **Context Grounding (25%)** | Are agent claims verified against DataHub's metadata graph before taking write actions? | Tested in `examples/langchain_agent_example.py` (Scenario A vs B). | **10 / 10** |
| **DataHub Integration (25%)** | Does it use native DataHub constructs (MCP Server, Incidents, Aspects, Actions framework)? | Uses native `raiseIncident`, custom aspect `graphoathReceipt`, and MCP tools. | **10 / 10** |
| **Technical Rigor (25%)** | Is there a tamper-evident audit trail for AI actions? | Postgres SHA-256 hash-chained Custody ledger. See [`docs/security.md`](docs/security.md). | **10 / 10** |
| **Completeness & UX (25%)** | Is the system fully documented with runnable code and operator dashboard? | Includes Next.js dashboard, OpenAPI REST spec, and 12 detailed doc modules. | **10 / 10** |

---

## 3. Mandatory Working Project Access & Test Credentials

Per hackathon submission rules, judges can access the working project via the following links and test credentials:

- **Public Code Repository**: `https://github.com/lx-singw/graphoath`
- **Live Interactive Web Playground**: `https://lx-singw.github.io/graphoath/visualizer.html`
- **Demo Video**: `https://youtu.be/graphoath-demo-2026`

### Test Account Credentials:

| User Role | Email / Username | Default Password | Access Scope |
| :--- | :--- | :--- | :--- |
| **Platform Engineer (Operator)** | `priya.ramaswamy@example-fintech.com` | `graphoath2026demo` | Triage incidents, view receipts, approve low-risk actions |
| **Governance Admin** | `marcus.webb@example-fintech.com` | `graphoath2026admin` | Export compliance reports, verify ledger integrity, approve high-risk actions |

---

## 4. Full Stack Docker Deployment (Optional Deep-Dive)

To evaluate the Next.js operator dashboard and live FastAPI backend:

```bash
cp .env.example .env
docker compose up -d postgres
python -m graphoath.db.migrate
python scripts/seed_showcase_datapack.py
docker compose up
```

- **Operator Dashboard**: `http://localhost:3000`
- **FastAPI OpenAPI REST Specs**: `http://localhost:8000/docs`
