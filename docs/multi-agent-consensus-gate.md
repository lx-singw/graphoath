# GraphOath — Multi-Agent Consensus & Conflict Resolution Gate

This document specifies **GraphOath's Multi-Agent Consensus Engine**, which resolves tool call collisions when multiple autonomous AI agents attempt conflicting operations on the same DataHub dataset URN.

---

## 1. The Multi-Agent Collision Problem

In modern enterprise data platforms, multiple specialized AI agents operate concurrently:
- **Agent A (FinOps Cost Optimizer)**: Wants to deprecate an unqueried dataset URN to save storage costs.
- **Agent B (ML Feature Pipeline)**: Wants to query the same dataset URN for monthly feature engineering.

If agents execute write actions independently, Agent A might deprecate a dataset that Agent B depends on, causing pipeline failure.

---

## 2. Multi-Agent Consensus Resolution Flow

GraphOath acts as a **centralized consensus gate** that evaluates proposed actions across all active agent sessions:

```
  ┌──────────────────┐               ┌──────────────────┐
  │  FinOps Agent A  │               │    ML Agent B    │
  │ (Deprecate URN)  │               │   (Query URN)    │
  └────────┬─────────┘               └────────┬─────────┘
           │                                  │
           │ Proposed Action A                │ Proposed Action B
           └────────────────┬─────────────────┘
                            │
                            ▼
          ┌───────────────────────────────────┐
          │  GraphOath Consensus Gate Engine  │
          │  1. Check DataHub Lineage Graph   │
          │  2. Evaluate Dataset Tier Policy  │
          │  3. Resolve Conflict Matrix       │
          └─────────────────┬─────────────────┘
                            │
             ┌──────────────┴──────────────┐
             ▼                             ▼
  ┌────────────────────┐        ┌────────────────────┐
  │  Approved Action B │        │ Rejected Action A  │
  │  (Preserve Table)  │        │ (Deprecation Block)│
  └────────────────────┘        └────────────────────┘
```

---

## 3. Conflict Resolution Priority Matrix

When conflicting tool actions target the same DataHub dataset URN, GraphOath applies deterministic priority rules:

| Priority Rank | Action Category | Precedence | Reasoning |
|---|---|---|---|
| **1 (Highest)** | **Security / Regulatory Containment** | Overrides all | PII leakage or compliance breaches must be contained immediately. |
| **2** | **Incident Triage & Alerting** (`raiseIncident`) | Overrides Deprecation | Operational incidents take precedence over cost optimization. |
| **3** | **Active Pipeline Dependencies** (`readQuery`) | Overrides Deprecation | Datasets with active downstream lineage cannot be deprecated. |
| **4 (Lowest)** | **Cost Optimization & Pruning** (`deprecate`) | Lowest precedence | Destructive pruning requires zero active lineage dependencies. |
