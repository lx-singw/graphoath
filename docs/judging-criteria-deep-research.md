# GraphOath — Brutally Honest Judging Criteria Deep Audit

> **Research Date**: 2026-08-08
> **Deadline**: August 10, 2026 (2 days remaining)
> **Track**: Agents That Do Real Work ($20,500 prize pool across 4 tracks)

---

## Executive Summary

> [!CAUTION]
> **GraphOath has world-class documentation and design thinking, but a critical execution gap.**
> The codebase audit reveals that **zero lines of code actually call DataHub's real APIs successfully.** Every DataHub interaction is mocked, hardcoded, or falls back to simulated data. The judging criteria explicitly asks *"Does the code do what the submission claims?"* — and right now, **the answer is no.**

### Honest Composite Score: 5.5/10 for 1st Place

| Judging Criterion | Weight | Current Score | Ceiling If Fixed | Critical Gap |
| :--- | :---: | :---: | :---: | :--- |
| **Use of DataHub** | High | **4/10** | 9/10 | No real DataHub SDK usage; no `datahub-agent-context` or `acryl-datahub` in dependencies; all calls mock/fallback |
| **Technical Execution** | High | **4/10** | 8/10 | Code exists but doesn't work end-to-end against a real DataHub instance; mock-heavy runtime |
| **Originality** | Medium | **8/10** | 9/10 | Genuinely novel — citation-gating, tamper-evident ledger, naive-vs-verified diff, TOCTOU prevention |
| **Real-World Usefulness** | Medium | **7/10** | 9/10 | Addresses a real practitioner pain point; undermined by lack of working demo |

---

## Criterion 1: Use of DataHub (Current: 4/10)

### What the Judges Are Looking For
*"How meaningfully does the project use DataHub — its context graph, MCP Server, Agent Context Kit, DataHub Skills, or Analytics Agent? Strong submissions go beyond reading metadata and contribute back to the graph where appropriate."*

### What We Claim
- MCP Server integration (`search_across_lineage`, `get_dataset_ownership`, `get_dataset_assertions`)
- Agent Context Kit (`datahub-agent-context` Python SDK)
- Native GraphQL `raiseIncident` mutation
- Custom `graphoathReceipt` aspect via `emitMetadataChangeProposal`
- DataHub Actions Framework listener (`MetadataChangeLog_v1`)
- DataHub Skill (`skills/graphoath-citation-verification/SKILL.md`)
- Native `addTag` trust tagging

### What Actually Exists (Audit Findings)

> [!WARNING]
> **ZERO real DataHub SDK packages exist in `pyproject.toml` or `requirements.txt`.**
> No `datahub-agent-context`, no `acryl-datahub`, no `datahub` package.

| Claimed Integration | Actual Code Reality |
| :--- | :--- |
| `search_across_lineage` via MCP | `lineage.py` calls `execute_graphql` but **falls back to hardcoded mock URNs** when no server responds |
| `get_dataset_ownership` | `ownership.py` calls `execute_graphql` but **ignores the response** and returns hardcoded `"team-growth-analytics"` |
| `raiseIncident` GraphQL mutation | `incidents.py` **does NOT call** `execute_graphql` at all — generates local UUIDs and returns mock dictionaries |
| `emitMetadataChangeProposal` | Referenced in docs, **no code exists** that calls this endpoint |
| `addTag` trust tag | Referenced in docs, **code in `tags.py` exists** but untested against real DataHub |
| `datahub-agent-context` SDK | **Not installed**, not imported, not in requirements |
| DataHub Actions webhook listener | Architecture documented, **no running webhook endpoint** |
| DataHub Skill `SKILL.md` | ✅ **EXISTS** and is well-structured |
| Avro aspect schema | ✅ **EXISTS** (`schemas/graphoathReceipt.avsc`) |

### What Past Winners Did (April 2026 DataHub × Nebius Hackathon)
- **DataHub Agent On Call** (Winner): Four-agent loop that **actually queries DataHub context** via Agent Context Kit, retrieves live lineage/ownership, takes real actions, and **writes findings back to the graph**.
- **Key differentiator**: Winners used `pip install datahub-agent-context` and made **real API calls** to a live or Quickstart DataHub instance.

### Gap Analysis
The documentation is impressive, but judges will immediately notice:
1. No `datahub-agent-context` or `acryl-datahub` in `requirements.txt`
2. Running `python examples/langchain_agent_example.py` produces output from **hardcoded mock data**, not from querying DataHub
3. The GitHub Codespaces environment doesn't spin up a DataHub instance, so judges **cannot verify** any DataHub integration

---

## Criterion 2: Technical Execution (Current: 4/10)

### What the Judges Are Looking For
*"Quality of implementation, robustness, and whether the project actually works end-to-end. Does the code do what the submission claims?"*

### What Actually Works (Verified)
| Component | Status | Evidence |
| :--- | :---: | :--- |
| Citation Gate logic (`gate.py`) | ✅ Works | Set-intersection check runs correctly on in-memory data |
| SHA-256 hash-chain ledger (`ledger.py`) | ✅ Works | Hash chaining logic is correct and tested |
| Tamper detection (`ledger_verify.py`) | ✅ Works | Catches modified records in simulated ledger |
| `fast_track_evaluation.py` runner | ✅ Works | Runs 8/8 steps, all pass (on mock data) |
| Framework adapters (LangChain, ADK) | ⚠️ Structural | Classes exist with correct interfaces but wrap mock internals |
| Deposition pipeline | ⚠️ Mock-only | Evidence→Gate→Action pipeline runs but on hardcoded data |
| DataHub GraphQL calls | ❌ Mock fallback | `client.py` catches connection errors → returns `{"data": {}, "mock": True}` |
| FastAPI backend server | ⚠️ Untested | Routes exist but require Postgres + DataHub to actually serve |
| Next.js dashboard | ⚠️ Not built | `src/dashboard/` referenced but no build/deployment verified |

### The Critical "Does It Work End-to-End?" Test
If a judge runs:
```bash
git clone https://github.com/lx-singw/graphoath
cd graphoath
python scripts/fast_track_evaluation.py
```
They will see **8/8 PASS** — but every single PASS is against **mock/simulated data**. There is no point where real DataHub metadata flows through the system.

> [!CAUTION]
> The judging criteria explicitly says *"whether the project actually works end-to-end"* and *"Does the code do what the submission claims?"*. Right now, the code claims to query DataHub lineage, ownership, and assertions via MCP — but it doesn't. This is the single biggest risk to the submission.

### Codebase Structure Issue
The codebase is split across two directories (`src/graphoath/` and root `graphoath/`) without a shared `__init__.py` at root. This is confusing for judges reviewing the code.

---

## Criterion 3: Originality (Current: 8/10)

### What the Judges Are Looking For
*"How creative and novel is the approach? Submissions should clearly go beyond features DataHub already provides out of the box."*

### Where GraphOath Genuinely Excels
This is our **strongest criterion**. The following concepts are genuinely novel and not provided by DataHub:

1. **Citation-Gating Pattern**: No agent tool in DataHub's ecosystem enforces "verify before write." This is a new architectural pattern.
2. **Tamper-Evident Custody Ledger**: SHA-256 hash-chained receipts with TOCTOU prevention — DataHub has nothing like this.
3. **Naive vs. Verified Diff**: Showing what an ungated agent *would have* hallucinated is a brilliant demo mechanic.
4. **Confidence-Tiered Routing**: Evidence-quality-based routing to HITL vs auto-execute is novel.
5. **Evidence-Drift Re-Verification**: Separating "record integrity" from "claim freshness" is sophisticated.
6. **Formal Mathematical Gate Contract**: `Approved(C) = {c ∈ C | Entities(c) ⊆ E}` — deterministic, not probabilistic.

### Risk
Judges may see the extensive documentation and worry it's "over-documented and under-built." The originality score is only valuable if paired with working execution.

---

## Criterion 4: Real-World Usefulness (Current: 7/10)

### What the Judges Are Looking For
*"Would a real data, ML, or AI platform team see clear value in this?"*

### Strengths
- **Problem is real and cited**: Agent hallucination is a genuine enterprise concern.
- **45-min MTTR → 2.4s**: Compelling metric (but from simulated data, not measured against real DataHub).
- **$442,500 ROI model**: Quantified financial impact is persuasive.
- **Multi-platform lineage** (Snowflake → dbt → Looker): Realistic enterprise stack.

### Weaknesses
- **No proof it works on real data**: The ROI and MTTR numbers come from hardcoded simulations.
- **No DataHub Quickstart integration**: Judges can't test against DataHub's `datahub docker quickstart` to verify claims.

---

## Competitive Landscape (What You're Up Against)

Based on the April 2026 winners and current hackathon focus:

| Competitor Pattern | Why It Wins | GraphOath Risk |
| :--- | :--- | :--- |
| **Agent that queries real DataHub + writes back** | Proves end-to-end DataHub integration | GraphOath doesn't do this |
| **Simple but working demo** | "Does it work?" = instant credibility | GraphOath has complex docs but mock runtime |
| **DataHub Quickstart integration** | Judges can spin up DataHub locally and test | GraphOath has no Quickstart integration |
| **Governed Proposal Steward pattern** | Human-in-the-loop + real write-back to graph | GraphOath docs describe this but don't implement it |

---

## Priority Action Plan (48 Hours Remaining)

> [!IMPORTANT]
> The single highest-leverage action is: **Make 1 real DataHub API call work end-to-end.**
> A working demo with 1 real GraphQL call beats 33 documentation modules with 0 real calls.

### P0 — Must Do (Today)

1. **Install `datahub-agent-context`** and add it to `requirements.txt` / `pyproject.toml`:
   ```bash
   pip install "datahub-agent-context[langchain]"
   ```

2. **Stand up DataHub Quickstart** and write a single demo script that:
   ```python
   from datahub.sdk.main_client import DataHubClient
   client = DataHubClient.from_env()
   # Real lineage query
   lineage = client.get_lineage("urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)")
   # Real raiseIncident call
   ```

3. **Record a 3-minute demo video** showing the real DataHub UI + real terminal output. This is likely your highest-weighted artifact for async judging.

4. **Deploy `docs/visualizer.html` to GitHub Pages** so the live demo URL actually works. Right now `https://lx-singw.github.io/graphoath/visualizer.html` may not be deployed.

### P1 — Should Do (Tomorrow)

5. **Fix the mock fallbacks** in `client.py`, `lineage.py`, `ownership.py`, `incidents.py` so they fail loudly instead of silently returning mock data. Judges who read the code will notice.

6. **Consolidate codebase structure**: Either everything in `src/graphoath/` or everything in `graphoath/`, not both.

7. **Add `datahub docker quickstart` instructions** to README so judges can spin up a local DataHub and test against it.

### P2 — Nice to Have

8. Deploy FastAPI backend to a free tier (Render, Railway) so judges have a live API.
9. Submit to multiple tracks (Agents That Do Real Work + Best DataHub Skill + Agentic Governance).

---

## Bottom Line

| Dimension | Status |
| :--- | :--- |
| **Documentation & Design** | 🟢 World-class. 33 modules, formal math, RFC, Avro schema, SKILL.md. |
| **Working Code** | 🔴 Mock-only. Zero real DataHub API calls succeed. |
| **Judge Experience** | 🟡 `fast_track_evaluation.py` runs clean, but against simulated data. |
| **Competitive Position** | 🟡 Strong concept, but winners typically ship working integrations. |

**The gap is not ideas — it's execution against a real DataHub instance.** Close that gap and this submission jumps from 5.5/10 to 8+/10.
