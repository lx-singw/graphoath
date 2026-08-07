# GraphOath — Examples & Demonstration Scripts

This folder contains real generated output and runnable demonstration scripts for **GraphOath**, provided for judges and evaluators to test and review the citation gate mechanics and DataHub integrations.

---

## 1. Runnable Agent Demonstration Scripts

### `langchain_agent_example.py`
A runnable Python script demonstrating how an AI agent built with **LangChain / LangGraph**:
1. Fetches metadata context (lineage graph & URNs) from DataHub.
2. Attempts an **uncited/hallucinated claim** (which is caught and blocked by GraphOath's Citation Gate).
3. Produces a **valid cited claim**, which passes the gate and generates a native DataHub Incident payload and hash-chained Custody receipt.

**To Run**:
```bash
python examples/langchain_agent_example.py
```

---

### `mock_mcp_citation_demo.py`
A standalone, zero-dependency Python script demonstrating the end-to-end event flow:
- Ingesting a DataHub `MetadataChangeLog` schema change event.
- Lineage traversal and evidence array assembly.
- Deterministic zero-network citation verification.
- Tamper-evident SHA-256 hash-chain receipt emission.

**To Run**:
```bash
python examples/mock_mcp_citation_demo.py
```

---

## 2. Sample Output Files (Generated Receipts)

When Deposition runs against a live DataHub instance (e.g. `showcase-ecommerce` datapack), full generated receipts are produced under:
- `receipt-schema-break.json` — A full receipt payload matching the `GET /receipts/{receipt_id}` REST API specification.
- `screenshots/datahub-incident.png` — Screenshot of the native DataHub Incident raised by GraphOath (`raiseIncident`).
- `screenshots/slack-notification.png` — Screenshot of the human approval workflow notification posted to Slack.
