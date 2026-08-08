---
name: graphoath-citation-verification
description: Zero-trust citation gate skill for DataHub AI agents. Intercepts proposed write calls, cross-references target asset URNs against DataHub's metadata graph, blocks uncited/hallucinated entities, and writes tamper-evident graphoathReceipt aspects to DataHub.
---

# GraphOath Citation Verification Skill

This skill provides a deterministic **Citation Gate** for AI agents operating on the DataHub platform. It prevents AI agents from executing write operations (e.g. `raiseIncident`, `emitMetadataChangeProposal`, schema modifications) if the entities referenced by the agent cannot be verified against DataHub's metadata context graph.

---

## 1. Installation

Install via standard agent skill package managers:

```bash
npx skills add graphoath-citation-verification
```

---

## 2. Skill Input & Output Schemas

### Input Schema (Claim & Evidence Payload)
```json
{
  "agent_id": "deposition_agent_v1",
  "proposed_action": "raiseIncident",
  "claims": [
    {
      "claim_id": "claim_001",
      "target_urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)",
      "assertion": "Schema breaking change detected on column order_id"
    }
  ],
  "evidence_urns": [
    "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)",
    "urn:li:dataset:(urn:li:dataPlatform:dbt,dbt.stg_orders,PROD)",
    "urn:li:corpuser:alice_data_owner"
  ]
}
```

### Output Schema (Verification Gate Result)
```json
{
  "status": "APPROVED",
  "citation_resolution_rate": 1.0,
  "verified_urns": [
    "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)"
  ],
  "unverified_urns": [],
  "ledger_hash": "a188d82fb6071b25a7a25dd5072d0fed8a89e0dab834a12d916e4e37c77b238e",
  "receipt_urn": "urn:li:aspect:graphoathReceipt:rcpt_98f4a12b",
  "latency_ms": 0.0016
}
```

---

## 3. Integration Procedure

1. **Context Resolution**: Query DataHub context via DataHub MCP Server (`search_across_lineage`, `get_dataset_ownership`).
2. **Evidence Collection**: Populate the `evidence_urns` array with all verified entities retrieved from DataHub.
3. **Citation Gate Execution**: Pass the agent's proposed write claims to `graphoath-citation-verification`.
4. **Conditional Execution**: Execute the write action **only if** `status == "APPROVED"`.
5. **Ledger Receipt**: Attach the returned `ledger_hash` and `receipt_urn` to the DataHub entity aspect store.
