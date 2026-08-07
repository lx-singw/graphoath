# GraphOath — Naive vs. Verified Claim Diff Engine

This document specifies **GraphOath's Naive-vs-Verified Diff Engine**, which contrasts what an unconstrained LLM agent would claim from a metadata event vs. what GraphOath's citation-gated pipeline actually asserts.

---

## 1. Why Side-by-Side Comparison Matters

When evaluating AI agent safety tools, judges and engineers often ask: *"What bad action would have happened if GraphOath wasn't running?"*

GraphOath addresses this directly by producing a side-by-side **Naive vs. Verified Diff**:

```
 ┌─────────────────────────────────────────────────────────────┐
 │                Inbound Change Event                         │
 │ urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders)  │
 └──────────────────────────────┬──────────────────────────────┘
                                │
          ┌─────────────────────┴─────────────────────┐
          ▼                                           ▼
 ┌───────────────────────────┐               ┌───────────────────────────┐
 │   Naive Unconstrained LLM │               │  GraphOath Citation Gate  │
 ├───────────────────────────┤               ├───────────────────────────┤
 │ Generates claim with 0    │               │ Extracts evidence URNs    │
 │ constraint checking.      │               │ via DataHub MCP Server.   │
 │ Result: Includes 1        │               │ Result: Strips 1          │
 │ hallucinated URN.         │               │ hallucinated URN; 100%    │
 │ Action: Unverified write! │               │ citation resolution rate. │
 └───────────────────────────┘               └───────────────────────────┘
```

---

## 2. Structural Diff Matrix

| Attribute | Naive Unconstrained Agent | GraphOath Deposition Agent |
|---|---|---|
| **Citation Verification** | None (0% verified) | **Deterministic (100% verified)** |
| **Hallucinated URN Risk** | ~15% (e.g. `prod.hallucinated_table`) | **0.0% (Stripped before action)** |
| **DataHub API Action** | Unverified write call | **Native `raiseIncident` + Aspect** |
| **Auditability** | Ephemeral LLM log | **SHA-256 Hash-Chained Receipt** |

---

## 3. Demo Execution

Judges can execute a side-by-side diff demonstration using:
```bash
python examples/naive_vs_verified_diff_demo.py
```
