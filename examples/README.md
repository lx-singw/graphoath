# GraphOath — Examples, Demonstrations & Benchmark Scripts

This folder contains real generated output and runnable demonstration scripts for **GraphOath**, provided for judges and evaluators to test and review the citation gate mechanics, MCP proxy middleware, and independent cryptographic verifiers.

---

## 1. Runnable Agent Demonstration & Benchmark Scripts

### `verify_receipt_chain.py` — *Judge-Runnable Independent Receipt Verifier*
A standalone, zero-dependency script that independently re-computes SHA-256 hash chains across exported Custody receipts without needing Docker or DataHub.
```bash
python examples/verify_receipt_chain.py
```

### `naive_vs_verified_diff_demo.py` — *Naive vs. Verified Claim Side-by-Side Diff Demo*
Contrasts what an unconstrained LLM agent would claim from a schema change event vs. what GraphOath's Deposition module actually asserts.
```bash
python examples/naive_vs_verified_diff_demo.py
```

### `generate_synthetic_graph.py` — *10,000-Node Synthetic Lineage Benchmark Harness*
Generates a 10,000-node synthetic DataHub lineage graph and benchmarks GraphOath's Citation Gate under 1,000 concurrent agent claims.
```bash
python examples/generate_synthetic_graph.py
```

### `mcp_server_proxy_demo.py` — *MCP Server Proxy Middleware Demo*
Demonstrates how GraphOath acts as a transparent proxy around DataHub MCP Server tool calls, verifying citations in real time.
```bash
python examples/mcp_server_proxy_demo.py
```

### `langchain_agent_example.py` — *LangChain / LangGraph Agent Integration Demo*
Demonstrates a LangChain agent attempting an uncited claim (blocked by GraphOath) vs. a valid cited claim (passed & emitted as a native DataHub Incident).
```bash
python examples/langchain_agent_example.py
```

### `mock_mcp_citation_demo.py` — *End-to-End Citation Gate & Live Tamper Detection Demo*
Demonstrates event ingestion, lineage traversal, citation verification, functional memory recall, and a live "tamper the ledger, watch it get caught" integrity check.
```bash
python examples/mock_mcp_citation_demo.py
```

---

## 2. Sample Output Files (Generated Receipts)

- `receipt-schema-break.json` — A full generated receipt payload matching the `GET /receipts/{receipt_id}` REST API specification.
- `receipt-repeat-incident.json` — Generated receipt demonstrating Functional Memory Recall (`"repeat_incident_detected": true`).
- `screenshots/datahub-incident.png` — Screenshot of the native DataHub Incident raised by GraphOath (`raiseIncident`).
- `screenshots/slack-notification.png` — Screenshot of the human approval workflow notification posted to Slack.
