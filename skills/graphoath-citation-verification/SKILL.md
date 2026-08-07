---
name: graphoath-citation-verification
description: Zero-trust citation gate skill for DataHub AI agents. Intercepts proposed write calls, cross-references target asset URNs against DataHub's metadata graph, blocks uncited/hallucinated entities, and writes tamper-evident graphoathReceipt aspects to DataHub.
---

# GraphOath Citation Verification Skill

This skill provides a deterministic **Citation Gate** for AI agents operating on the DataHub platform. It prevents AI agents from executing write operations (e.g. `raiseIncident`, `emitMetadataChangeProposal`, schema modifications) if the entities referenced by the agent cannot be verified against DataHub's metadata context graph.

---

## 1. Skill Input & Output Schemas

### Input Schema (Claim & Evidence Payload)
```json
{
  "agent_id": "string",
  "proposed_action": "raiseIncident | updateMetadata | deprecateDataset",
  "claims": [
    {
      "claim_id": "string",
      "target_urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)",
      "assertion": "Schema breaking change detected on column order_id"
    }
  ],
  "evidence_urns": [
    "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)",
    "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders_downstream,PROD)",
    "urn:li:corpuser:data_owner_alice"
  ]
}
```

### Output Schema (Verification Gate Result)
```json
{
  "status": "APPROVED | REJECTED | REQUIRE_HUMAN_APPROVAL",
  "citation_resolution_rate": 1.0,
  "verified_urns": [
    "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)"
  ],
  "unverified_urns": [],
  "ledger_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "receipt_urn": "urn:li:aspect:graphoathReceipt:rcpt_98f4a12b"
}
```

---

## 2. When to Use This Skill

Use this skill whenever an agent is about to execute a write action on DataHub or a downstream enterprise database.

* **Before `raiseIncident`**: Verify that the dataset URN and downstream lineage nodes exist in DataHub.
* **Before schema modification**: Ensure target tables and column URNs match live metadata schemas.
* **Before automated remediation**: Gate destructive actions behind citation resolution and human-in-the-loop confidence thresholds.

---

## 3. Integration Procedure

1. Query DataHub context via DataHub MCP Server (`search_across_lineage`, `get_dataset_ownership`).
2. Populate the `evidence_urns` array with retrieved entities.
3. Pass the agent's proposed write claims to `graphoath-citation-verification`.
4. Execute the write action **only if** `status == "APPROVED"`.
5. Attach the returned `ledger_hash` and `receipt_urn` to the DataHub entity.
