# DataHub RFC / Skill Proposal: Citation-Gated Agent Control Plane Pattern

**Proposal Type**: DataHub Community RFC & Agent Context Pattern Standard  
**Authors**: GraphOath Team  
**Status**: Proposal / Hackathon Open-Source Artifact  
**Target Entities**: `incident`, `aspect:graphoathReceipt`, `MCP Server`  

---

## 1. Abstract

As AI agents increasingly automate enterprise data operations (schema-drift maintenance, dbt model generation, pipeline incident triage), allowing agents to execute unverified write operations directly against metadata catalogs leads to **hallucinated entity references, unassigned incidents, and unauditable state changes**.

This RFC proposes the **Citation-Gated Control Plane Pattern** as a standard DataHub open-source extension. Before any agent-initiated claim produces a DataHub write action (e.g. `raiseIncident`, `emitMetadataChangeProposal`), every entity URN named in the agent's claim must resolve to a queryable fact in DataHub's metadata graph (retrieved via MCP or Agent Context Kit).

---

## 2. Proposed DataHub Custom Aspect Specification

We propose standardizing a `citationReceipt` (or `graphoathReceipt`) aspect attached to native DataHub entities (`incident`, `dataset`, `chart`).

### Aspect JSON Schema: `graphoathReceipt.json`

```json
{
  "name": "graphoathReceipt",
  "type": "record",
  "doc": "Tamper-evident evidence receipt for agent-initiated DataHub actions.",
  "fields": [
    { "name": "receiptId", "type": "string" },
    { "name": "timestampMillis", "type": "long" },
    { "name": "agentModule", "type": "string" },
    { "name": "sourceEntityUrn", "type": "string" },
    { "name": "claimText", "type": "string" },
    { "name": "evidenceUrns", "type": { "type": "array", "items": "string" } },
    { "name": "citationResolutionRate", "type": "float" },
    { "name": "ledgerHash", "type": "string" }
  ]
}
```

---

## 3. The 4-Stage Protocol Workflow

```
┌──────────────┐     1. Ingest Change     ┌──────────────────┐
│ DataHub      ├─────────────────────────►│ Trigger Stage    │
│ Actions      │                          │ (MCL Normalized) │
└──────────────┘                          └────────┬─────────┘
                                                   │
                                                   ▼
┌──────────────┐     2. Query Graph       ┌──────────────────┐
│ DataHub MCP  │◄─────────────────────────┤ Evidence Stage   │
│ Server       ├─────────────────────────►│ (Lineage/Owner)  │
└──────────────┘                          └────────┬─────────┘
                                                   │
                                                   ▼
                                          ┌──────────────────┐
                                          │ Citation Gate    │
                                          │ (Zero-Network)   │
                                          └────────┬─────────┘
                                                   │ Approved
                                                   ▼
┌──────────────┐     3. Native Action     ┌──────────────────┐
│ DataHub      │◄─────────────────────────┤ Action Stage     │
│ GraphQL API  │  (raiseIncident + Aspect)│ (Receipt Written)│
└──────────────┘                          └──────────────────┘
```

1. **Trigger**: Subscribes to `MetadataChangeLog_v1` change events.
2. **Evidence**: Queries DataHub lineage, ownership, and usage via MCP tools (`search_across_lineage`, `get_dataset_ownership`).
3. **Citation Gate**: Verifies that `Ref(ClaimURNs) ⊆ Ref(EvidenceURNs)`. Rejects uncited claims instantly without network overhead.
4. **Action & Receipt**: Mutates DataHub natively via `raiseIncident` and emits the `graphoathReceipt` aspect.

---

## 4. Community Value & Standardization

By standardizing this pattern within DataHub:
- Any agent framework (LangChain, LangGraph, LlamaIndex, Google ADK) can use a uniform tool wrapper to interact with DataHub safely.
- Data governance teams gain immediate, tamper-evident auditability across all AI agent interactions.
- Prevents parallel incident tracking systems by composing natively with DataHub's core entities.
