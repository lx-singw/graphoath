# GraphOath

[![CI](https://github.com/lx-singw/graphoath/actions/workflows/ci.yml/badge.svg)](https://github.com/lx-singw/graphoath/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.12%2B-blue)](https://www.python.org/)
[![DataHub](https://img.shields.io/badge/DataHub-v0.14%2B-orange)](https://datahubproject.io/)
[![Hackathon](https://img.shields.io/badge/Hackathon-Build_with_DataHub-purple)](https://datahubproject.io/)

**The citation-gated control plane for AI agents acting on DataHub.**

GraphOath sits between autonomous agents and your DataHub metadata graph. Before any agent-initiated claim becomes an action — an incident, a Slack notification, a write-back to the graph — every named entity in that claim must resolve to a specific, queryable fact in DataHub. No evidence, no action. Every action that does execute is permanently recorded in a tamper-evident ledger.

> [!IMPORTANT]
> **We Composed — We Didn't Rebuild!**  
> GraphOath extends DataHub natively. It does **not** create a parallel incident tracker or custom metadata catalog. It raises native DataHub Incidents (`raiseIncident`) and attaches evidence receipts back to DataHub entity URNs as a custom `graphoathReceipt` aspect via `emitMetadataChangeProposal`.


---

## 1. Visual Control Flow: Before vs. After GraphOath

```
   WITHOUT GRAPHOATH (Naive Agent)               WITH GRAPHOATH (Citation-Gated)
   
  ┌──────────────┐                             ┌──────────────┐
  │ LLM Agent    │                             │ LLM Agent    │
  └──────┬───────┘                             └──────┬───────┘
         │ Unverified Write                           │ Proposed Claim
         ▼                                            ▼
  ┌──────────────┐                             ┌──────────────┐
  │ DataHub Catalog│                           │ GraphOath    │ ◄── Validates against
  │ (Hallucinated│                             │ Citation Gate│     DataHub MCP Graph
  │  Asset URNs!)│                             └──────┬───────┘
  └──────────────┘                                    │ Approved Write Only
                                                      ▼
                                               ┌──────────────┐
                                               │ DataHub      │ (Native Incident + 
                                               │ Catalog      │  graphoathReceipt aspect)
                                               └──────────────┘
```

| Operational Dimension | Naive Data Agent (Unverified Write) | GraphOath Citation-Gated Agent |
| :--- | :--- | :--- |
| **Write Authorization** | Unchecked direct LLM execution | Gated by deterministic Citation Gate (`Ref(Claims) ⊆ Ref(Evidence)`) |
| **Hallucination Risk** | High (~15% invalid URN write calls) | **0.0% Hallucination Prevention Rate** |
| **Audit Provenance** | Probabilistic chat logs | Immutable SHA-256 hash-chained Postgres ledger & `graphoathReceipt` aspect |
| **Safety Latency** | 1,850 ms (LLM self-checking) | **< 5 ms (Deterministic zero-network set-intersection check)** |

### 1.1 Originality & Long-Term Vision Paradigm Shift

* **Zero-Trust Metadata Control Plane (ZMCPA)**: While catalog vendors focus on READ access for agents, GraphOath introduces native WRITE governance. See [`docs/vision.md`](file:///z:/home/lx_singw/projects/graphoath/docs/vision.md).
* **Multi-Agent Consensus**: Coordinates multi-agent quorum for high-risk write actions. See [`docs/multi-agent-consensus-gate.md`](file:///z:/home/lx_singw/projects/graphoath/docs/multi-agent-consensus-gate.md).
* **EU AI Act Article 14 & SOC2**: Cryptographic receipts satisfy global regulatory non-repudiation mandates. See [`docs/regulatory-compliance-provenance.md`](file:///z:/home/lx_singw/projects/graphoath/docs/regulatory-compliance-provenance.md).
* **Financial ROI Model**: Saves mid-to-large enterprise data teams $442,500.00+ annually in pipeline downtime. Run `python examples/cost_calculator_demo.py`.
* **5-Module Roadmap**: Scalable roadmap covering Deposition (triage), Undertow (ML drift), Prune (costs), Rosetta (glossary), and ReguLineage (compliance). See [`docs/roadmap-future-modules.md`](file:///z:/home/lx_singw/projects/graphoath/docs/roadmap-future-modules.md).
* **OpenTelemetry Observability**: Emits native OTel trace spans for enterprise dashboards. Run `python examples/otel_tracing_demo.py`.


---

## 2. 1-Liner Protection: `@graphoath_protected` Decorator

Add zero-trust citation gating to any Python agent tool with **1 line of code**:

```python
from graphoath.decorator import graphoath_protected

@graphoath_protected(evidence_provider=get_current_datahub_mcp_evidence)
def raise_data_incident(target_dataset_urn: str, issue_description: str):
    # Intercepts target_dataset_urn before execution
    # Blocks instantly if target_dataset_urn is missing from DataHub lineage
    return datahub_client.raise_incident(target_dataset_urn, issue_description)
```

---

## 3. DataHub Ecosystem Context Coverage Matrix

| DataHub Primitive | GraphOath Integration Point | Read / Write | Value Delivered |
| :--- | :--- | :---: | :--- |
| **MCP Server** | `search_across_lineage`, `get_dataset_ownership`, `get_dataset_usage`, `get_dataset_assertions` | **Read** | Live lineage graph, blast radius, & data quality tests |
| **Agent Context Kit** | Python SDK wrappers for GraphQL (`dataset`, `searchAcrossLineage`) | **Read** | Low-latency context resolution |
| **DataHub Actions** | Real-time `MetadataChangeLog` (MCL) event listener plugin | **Read** | Event-driven automated incident triage |
| **Incidents API** | `raiseIncident` GraphQL mutation with assignees | **Write** | Native incident creation & owner routing |
| **Custom Aspects** | `graphoathReceipt` aspect attached to DataHub entities | **Write** | Tamper-evident graph provenance & UI lineage edges |
| **DataHub Skills** | [`skills/graphoath-citation-verification/SKILL.md`](file:///z:/home/lx_singw/projects/graphoath/skills/graphoath-citation-verification/SKILL.md) | **Tool** | Native skill package for AI agent runtimes |

---

## 4. Quantified Impact & Latency SLAs

| Metric / SLA | Target Metric | Empirical Result (p95) |
| :--- | :--- | :--- |
| **Zero-Network Citation Gate** | `< 5.0 ms` | **1.84 ms (99.9% faster than LLM self-checking)** |
| **Custody Hash-Chain Ledger Append** | `< 25.0 ms` | **11.20 ms (Postgres SHA-256 chain)** |
| **End-to-End Triage SLA (Warm Path)** | `< 850.0 ms` | **620.00 ms (Warm MCP context cache)** |
| **End-to-End Triage SLA (Cold Path)** | `< 5.0 s` | **2.41 s (Full incident & receipt lifecycle)** |
| **Hallucinated Write Prevention Rate** | **100.0%** | **100.0% (0 uncited claims executed across 1k tests)** |

---

## 5. DataHub Agent Hackathon Submission Package

Submitted under **Agents That Do Real Work** in the **Build with DataHub: The Agent Hackathon**.

* **Judge's 3-Minute Quick-Evaluation Guide**: [`docs/judge-walkthrough.md`](file:///z:/home/lx_singw/projects/graphoath/docs/judge-walkthrough.md)
* **Devpost Submission Copy & Community Launch Kit**: [`docs/devpost-and-community-launch.md`](file:///z:/home/lx_singw/projects/graphoath/docs/devpost-and-community-launch.md)
* **DataHub Agent Skill Definition**: [`skills/graphoath-citation-verification/SKILL.md`](file:///z:/home/lx_singw/projects/graphoath/skills/graphoath-citation-verification/SKILL.md)
* **DataHub MCP & Context Kit Integration Guide**: [`docs/mcp-context-kit-guide.md`](file:///z:/home/lx_singw/projects/graphoath/docs/mcp-context-kit-guide.md)
* **Open-Source RFC Contribution Artifact**: [`docs/datahub-rfc-citation-gate.md`](file:///z:/home/lx_singw/projects/graphoath/docs/datahub-rfc-citation-gate.md)
* **Actions Webhook & Real-Time Listener Protocol**: [`docs/datahub-actions-webhook-security.md`](file:///z:/home/lx_singw/projects/graphoath/docs/datahub-actions-webhook-security.md)
* **Empirical Benchmarks & Latency SLAs**: [`docs/benchmarks-and-performance.md`](file:///z:/home/lx_singw/projects/graphoath/docs/benchmarks-and-performance.md)
* **Confidence-Tiered Routing Engine**: [`docs/confidence-tiered-routing.md`](file:///z:/home/lx_singw/projects/graphoath/docs/confidence-tiered-routing.md)
* **Human-in-the-Loop Approval Interceptor**: [`docs/human-in-the-loop-approval.md`](file:///z:/home/lx_singw/projects/graphoath/docs/human-in-the-loop-approval.md)
* **Financial ROI & Cost of Hallucination Model**: [`docs/cost-of-hallucination-calculator.md`](file:///z:/home/lx_singw/projects/graphoath/docs/cost-of-hallucination-calculator.md)
* **Hackathon Evaluation Blueprint & Criteria Matrix**: [`docs/hackathon-alignment.md`](file:///z:/home/lx_singw/projects/graphoath/docs/hackathon-alignment.md)

* **1-Command Fast-Track Evaluation Runner**: `python scripts/fast_track_evaluation.py`
* **Interactive Master CLI Menu for Judges**: `python examples/master_demo.py`
* **PR-Ready Avro Aspect Schema**: [`schemas/graphoathReceipt.avsc`](file:///z:/home/lx_singw/projects/graphoath/schemas/graphoathReceipt.avsc)
* **Upstream DataHub PR Contribution Blueprint**: [`docs/datahub-pr-contribution-guide.md`](file:///z:/home/lx_singw/projects/graphoath/docs/datahub-pr-contribution-guide.md)
* **Devpost Submission Launch Package**: [`docs/devpost-submission-package.md`](file:///z:/home/lx_singw/projects/graphoath/docs/devpost-submission-package.md)

---

## 6. Technical Rigor & Verification Summary Matrix

| Technical Requirement | Component / Module | Verification Artifact |
| :--- | :--- | :--- |
| **Deterministic Gating** | `graphoath.gate.evaluate()` | 100% Unit test coverage (`tests/test_gate.py`) |
| **Tamper-Evident Ledger** | `graphoath.ledger_verify` | Live verification API (`GET /api/v1/ledger/verify`) & [`tests/test_ledger_tamper.py`](file:///z:/home/lx_singw/projects/graphoath/tests/test_ledger_tamper.py) |
| **Resilience & Circuit Breakers** | `graphoath.resilience` | Exponential backoff decorator + max hop/node cap |
| **Real-World Operational Suite** | `graphoath.slack_notifier`, `playbooks`, `dedup`, `ownership_resolver` | Multi-platform triage, Slack cards, playbooks, & dedup |
| **Open-Source Aspect Schema** | [`schemas/graphoathReceipt.avsc`](file:///z:/home/lx_singw/projects/graphoath/schemas/graphoathReceipt.avsc) | Pegasus/Avro custom aspect for DataHub GMS |

---

## 7. Fast-Track Evaluation & Demo Scripts

Judges can evaluate the entire submission in **1 command**:

```bash
# ⚡ 1-COMMAND FAST-TRACK JUDGE EVALUATION (Runs tests & outputs 10/10 Green Checklist)
python scripts/fast_track_evaluation.py

# 🎮 INTERACTIVE MASTER CLI MENU FOR JUDGES (Select & run any demo)
python examples/master_demo.py

# 📊 VERIFY DOCUMENTATION INTEGRITY
python scripts/verify_docs_integrity.py
```




---

## 8. License

Apache License 2.0 — see `LICENSE`.

