# GraphOath — Strategic Vision & Industry Paradigm Shift

## 1. Executive Summary & Industry Paradigm Shift

Every enterprise adopting AI agents for data operations faces the same unresolved crisis: **what happens the first time an agent is wrong, and nobody can reconstruct why it did what it did?**

Catalog vendors have spent eighteen months racing to give AI agents **READ** access to metadata — native MCP servers, GraphQL endpoints, and agent-context SDKs. Virtually none of them have addressed the **WRITE** side: what an agent is allowed to assert, what evidence that assertion has to rest on, and what permanent record exists once the agent has acted.

GraphOath is that missing layer. It introduces the **Zero-Trust Metadata Control Plane Architecture (ZMCPA)**. GraphOath does not compete with DataHub as a catalog; it sits downstream as the safety harness every agent must pass through before a claim about the data estate becomes an action.

```
   BEFORE GRAPHOATH (Read-Only Catalog Context)     WITH GRAPHOATH (Zero-Trust Write Control Plane)
   
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

---

## 2. Multi-Agent Consensus Gating Topology

As enterprise data architectures evolve from single agents to multi-agent swarms, GraphOath enforces **Multi-Agent Consensus Gating**. High-impact write operations (e.g. schema deprecation, production model retraining) require multi-agent quorum:

```
  ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
  │ Triage Agent    │       │ Security Agent  │       │ Cost Agent      │
  └────────┬────────┘       └────────┬────────┘       └────────┬────────┘
           │ Evidence               │ Security Tag            │ Usage & ROI
           ▼                        ▼                         ▼
  ┌─────────────────────────────────────────────────────────────────────┐
  │                GraphOath Multi-Agent Consensus Gate                 │
  │     Requires 100% Quorum Consensus Across All Evidence URNs         │
  └──────────────────────────────────┬──────────────────────────────────┘
                                     │ Quorum Verified
                                     ▼
                      ┌─────────────────────────────┐
                      │ DataHub Native Write Action │
                      └─────────────────────────────┘
```

See [`docs/multi-agent-consensus-gate.md`](docs/multi-agent-consensus-gate.md) for complete quorum specs.

---

## 3. EU AI Act Article 14 & Regulatory Non-Repudiation

Under global regulations such as **EU AI Act Article 14 (Human Oversight)** and **SOC 2 Type II Audits**, enterprises operating autonomous AI agents must guarantee human oversight and tamper-evident audit trails.

GraphOath satisfies regulatory compliance by design:
1. **Human Oversight Routing**: Medium-confidence agent actions are routed to Slack/Teams human approval workflows ([`docs/human-in-the-loop-approval.md`](docs/human-in-the-loop-approval.md)).
2. **Legal Non-Repudiation**: Receipts are written to an append-only, SHA-256 hash-chained Postgres ledger and mirrored to DataHub custom aspects ([`docs/regulatory-compliance-provenance.md`](docs/regulatory-compliance-provenance.md)).

---

## 4. Enterprise Memory Flywheel & Functional Memory Recall

Every receipt written back to DataHub enriches the graph itself. When future agents query DataHub via MCP tools, they read past `graphoathReceipt` aspects to perform **Functional Memory Recall**:

$$\text{Enterprise Trust Moat} = \sum_{t=1}^{T} \text{Receipts}_t \times \text{VerifiedEvidence}$$

Future agents automatically learn from historical schema breaks and incident resolutions, creating a self-reinforcing enterprise memory flywheel. See [`docs/functional-memory-recall.md`](docs/functional-memory-recall.md).

---

## 5. Open Custody Protocol & DataHub Community RFC

GraphOath open-sources the **Custody Protocol** as a DataHub Community RFC ([`docs/datahub-rfc-citation-gate.md`](docs/datahub-rfc-citation-gate.md)). Any third-party agent framework (LangChain, LangGraph, LlamaIndex, Google ADK, AutoGen) can submit proof chains to DataHub through a standardized custom aspect specification (`graphoathReceipt`).

---

## 6. Financial Cost of Hallucination ROI Model

GraphOath quantifies the economic value of hallucination prevention:

$$\text{Financial Risk Saved} = N_{\text{actions}} \times P_{\text{hallucination}} \times \left( \text{MTTR}_{\text{manual}} \times \text{HourlyRate} + \text{SLA\_Penalties} \right)$$

For a typical mid-sized enterprise running 5,000 agent actions annually with a 15% hallucination risk, GraphOath delivers **$442,500.00 in annual net savings** (demonstrated in [`examples/cost_calculator_demo.py`](examples/cost_calculator_demo.py) and [`docs/cost-of-hallucination-calculator.md`](docs/cost-of-hallucination-calculator.md)).

---

## 7. 5-Module Product Expansion Roadmap

GraphOath is a scalable platform with a multi-stage product expansion roadmap:

1. **Deposition** (Flagship MVP): Schema-break triage & lineage incident gate.
2. **Undertow**: Continuous ML feature lineage drift & training-serving skew guard.
3. **Prune**: Automated cost-governance & orphaned dataset deprecation agent.
4. **Rosetta**: Tribal knowledge capture & automated glossary term generator.
5. **ReguLineage**: Regulatory exposure tracing (PII / GDPR / EU AI Act).

See [`docs/roadmap-future-modules.md`](docs/roadmap-future-modules.md).
