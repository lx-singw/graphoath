# DataHub MCP Server & Agent Context Kit Integration Guide

This guide details how **GraphOath** leverages **DataHub's Model Context Protocol (MCP) Server**, **Agent Context Kit**, **DataHub Skills**, and **Actions Framework** to query lineage, usage, ownership, quality assertions, and governance metadata to ground AI agents in data context.

---

## 1. Context Architecture & Coverage Matrix

DataHub provides an open-source Context Platform for AI agents through multiple complementary interfaces. GraphOath sits as a **citation-gated control plane middleware** between AI agents and the DataHub Context Platform:

```
  ┌─────────────────────────────────────────────────────────────┐
  │                    AI Agent Engine                          │
  └──────────────────────────────┬──────────────────────────────┘
                                 │ Standard MCP Tool Calls
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                  DataHub MCP Server                         │
  │  - search_across_lineage                                    │
  │  - get_dataset_ownership                                    │
  │  - get_dataset_usage / get_dataset_assertions                │
  └──────────────────────────────┬──────────────────────────────┘
                                 │ Metadata Graph Response
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                   GraphOath Evidence Array                  │
  │   [urn:li:dataset:..., urn:li:corpuser:..., usage_stats]    │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                   GraphOath Citation Gate                   │
  │  Matches every claim against evidence URNs before writing   │
  └─────────────────────────────────────────────────────────────┘
```

### DataHub Context Coverage Matrix

| DataHub Platform Primitive | GraphOath Integration Point | Read / Write | Value Delivered |
| :--- | :--- | :---: | :--- |
| **MCP Server** | `search_across_lineage`, `get_dataset_ownership`, `get_dataset_usage`, `get_dataset_assertions` | **Read** | Fetches live lineage graph, ownership, & blast radius |
| **Agent Context Kit** | Python SDK wrappers for GraphQL (`dataset`, `searchAcrossLineage`) | **Read** | Low-latency context resolution |
| **DataHub Actions** | Real-time `MetadataChangeLog` (MCL) event listener plugin | **Read** | Event-driven automated triage |
| **Incidents API** | `raiseIncident` GraphQL mutation with assignees | **Write** | Native incident creation |
| **Custom Aspects** | `graphoathReceipt` aspect attached to DataHub entities | **Write** | Tamper-evident graph provenance |
| **DataHub Skills** | `skills/graphoath-citation-verification/SKILL.md` package | **Tool** | Pluggable skill for any AI agent framework |

---

## 2. DataHub Agent Skill Integration

GraphOath is packaged as an official DataHub Agent Skill located at [`skills/graphoath-citation-verification/SKILL.md`](file:///z:/home/lx_singw/projects/graphoath/skills/graphoath-citation-verification/SKILL.md).

Any DataHub Analytics Agent, Gemini agent, or Claude model can load GraphOath directly as a native skill to perform zero-trust verification of proposed actions before executing mutations.

---

## 3. Key DataHub MCP Tools & Expanded Context Depth

GraphOath's evidence engine queries multiple DataHub context primitives:

### 3.1 Lineage Inspection (`search_across_lineage`)
- **Purpose**: Traces downstream dependencies from a changed dataset.
- **MCP Call Parameters**:
  ```json
  {
    "urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)",
    "direction": "DOWNSTREAM",
    "max_hops": 3
  }
  ```
- **GraphOath Usage**: Builds the list of impacted downstream datasets and dashboards that form the core evidence array.

### 3.2 Ownership Identification (`get_dataset_ownership`)
- **Purpose**: Identifies responsible engineers and teams for downstream assets.
- **GraphOath Usage**: Populates the `assignees` parameter on native DataHub Incidents (`raiseIncident`).

### 3.3 Usage & Blast Radius (`get_dataset_usage`)
- **Purpose**: Retrieves query volume and active user count for affected datasets.
- **GraphOath Usage**: Computes impact severity to ensure triage incidents are prioritized correctly.

### 3.4 Data Quality Assertions (`get_dataset_assertions`)
- **Purpose**: Checks passing/failing status of data quality tests.
- **GraphOath Usage**: Prevents agents from executing downstream pipeline jobs if upstream assertions are failing.

### 3.5 Glossary Terms & Governance Tags (`get_dataset_tags`)
- **Purpose**: Inspects PII classification and tiering.
- **GraphOath Usage**: Blocks destructive agent actions targeted at `PII` or `Tier-1-Core` datasets without human approval.

---

## 4. Emitting Receipts & Lineage Graph Visibility

Once GraphOath verifies a claim, it writes the evidence trail back into DataHub using DataHub's metadata change proposal API (`emitMetadataChangeProposal`).

### 4.1 Custom Aspect: `graphoathReceipt`
GraphOath defines a custom aspect attached to DataHub entities:

```json
{
  "entityUrn": "urn:li:incident:graphoath-dep-20260807-001",
  "entityType": "incident",
  "aspectName": "graphoathReceipt",
  "aspect": {
    "contentType": "application/json",
    "value": {
      "receipt_id": "rcpt_98f4a12b",
      "timestamp": "2026-08-07T09:36:33Z",
      "module": "Deposition",
      "source_event_urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)",
      "evidence_count": 4,
      "ledger_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    }
  }
}
```

### 4.2 Web UI Lineage Graph Visibility
In addition to writing the receipt aspect, GraphOath emits bi-directional lineage edges between the `urn:li:incident:...` and the source `urn:li:dataset:...`. This ensures that anyone inspecting the dataset inside **DataHub's Web UI** sees the GraphOath Incident and Evidence Receipt right inside the interactive graph.

---

## 5. Configuration & Troubleshooting

To enable DataHub MCP integration in GraphOath:

1. Ensure DataHub v0.14+ is running with GMS GraphQL enabled.
2. Set environment variables in `.env`:
   ```bash
   DATAHUB_GMS_URL=http://localhost:8080
   DATAHUB_TOKEN=your_datahub_pat_token
   DATAHUB_MCP_ENABLED=true
   ```
3. Run the connection verification check:
   ```bash
   python -m graphoath.datahub.verify_mcp
   ```
