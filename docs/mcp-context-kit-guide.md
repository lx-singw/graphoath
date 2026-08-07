# DataHub MCP Server & Agent Context Kit Integration Guide

This guide details how **GraphOath** leverages **DataHub's Model Context Protocol (MCP) Server** and **Agent Context Kit** to query lineage, usage, ownership, and governance metadata to ground AI agents in data context.

---

## 1. Context Architecture Overview

DataHub provides an open-source Context Platform for AI agents through two main interfaces:
1. **DataHub MCP Server**: Enables agents to query DataHub tools via standard JSON-RPC protocol over stdio or HTTP.
2. **DataHub Agent Context Kit**: Python/TypeScript SDK wrappers around DataHub's GraphQL API optimized for agent context retrieval.

GraphOath sits as a **citation-gated control plane middleware** between AI agents and the DataHub Context Platform:

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
  │  - get_dataset_usage                                        │
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

---

## 2. Key DataHub MCP Tools Consumed by GraphOath

GraphOath's evidence engine relies on several core MCP tools provided by DataHub:

### 2.1 Lineage Inspection (`search_across_lineage`)
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

### 2.2 Ownership Identification (`get_dataset_ownership`)
- **Purpose**: Identifies responsible engineers and teams for downstream assets.
- **MCP Call Parameters**:
  ```json
  {
    "urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.finance_monthly,PROD)"
  }
  ```
- **GraphOath Usage**: Populates the `assignees` parameter on native DataHub Incidents (`raiseIncident`).

### 2.3 Usage & Blast Radius (`get_dataset_usage`)
- **Purpose**: Retrieves query volume and active user count for affected datasets.
- **MCP Call Parameters**:
  ```json
  {
    "urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.finance_monthly,PROD)"
  }
  ```
- **GraphOath Usage**: Computes impact severity to ensure triage incidents are prioritized correctly.

---

## 3. Emitting Receipts back to DataHub Graph

Once GraphOath verifies a claim, it writes the evidence trail back into DataHub using DataHub's metadata change proposal API (`emitMetadataChangeProposal`).

### 3.1 Custom Aspect: `graphoathReceipt`
GraphOath defines a custom aspect on DataHub entities:

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

This attaches the evidence payload directly to the DataHub entity, allowing future agents querying DataHub via MCP to inspect the receipt history.

---

## 4. Configuration & Troubleshooting

To enable DataHub MCP integration in GraphOath:

1. Ensure DataHub v0.14+ is running with GMS GraphQL enabled.
2. Set the following environment variables in `.env`:
   ```bash
   DATAHUB_GMS_URL=http://localhost:8080
   DATAHUB_TOKEN=your_datahub_pat_token
   DATAHUB_MCP_ENABLED=true
   ```
3. Run the connection verification check:
   ```bash
   python -m graphoath.datahub.verify_mcp
   ```
