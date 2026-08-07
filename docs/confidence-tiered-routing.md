# GraphOath — Confidence-Tiered Routing Architecture

This document specifies **GraphOath's Confidence-Tiered Routing Engine**, which routes proposed agent actions based on **evidence quality & lineage hop distance** rather than static action allowlists.

---

## 1. Evidence Strength vs Routing Decision

Instead of relying on fixed rules for human approval, GraphOath evaluates the **Confidence Score** of the supporting evidence package:

```
  Evidence Confidence Score = (Direct Hop Weight) × (Ownership Resolution Rate) × (Usage Recency)
```

```
 ┌─────────────────────────────────────────────────────────────┐
 │                Agent Proposed Action                        │
 └──────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │           Evidence Confidence Engine Evaluation             │
 └──────────────────────────────┬──────────────────────────────┘
                                │
          ┌─────────────────────┴─────────────────────┐
          ▼                                           ▼
  Confidence ≥ 0.90                           Confidence < 0.90
  (Direct 1-Hop Lineage)                      (Multi-Hop / Inferred)
          │                                           │
          ▼                                           ▼
 ┌───────────────────────────┐               ┌───────────────────────────┐
 │   Automated Execution     │               │ Route to Slack HITL Gate  │
 │ (Native DataHub Action)   │               │ (Human Approval Required) │
 └───────────────────────────┘               └───────────────────────────┘
```

---

## 2. Confidence Tier Matrix

| Tier | Lineage Hop Distance | Ownership Verified? | Confidence Score | Action Routing |
|---|---|---|---|---|
| **Tier A (High Confidence)** | Direct 1-Hop Downstream | Yes | `0.95 - 1.00` | **Automated Execution** |
| **Tier B (Medium Confidence)** | 2-Hop Downstream | Yes | `0.75 - 0.94` | **Slack HITL Approval Gate** |
| **Tier C (Low / Inferred)** | 3+ Hop Downstream | No (Fallback owner) | `< 0.75` | **Slack HITL Approval + Warn** |
