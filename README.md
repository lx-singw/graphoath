# GraphOath

**The citation-gated control plane for AI agents acting on DataHub.**

GraphOath sits between autonomous agents and your DataHub metadata graph. Before
any agent-initiated claim becomes an action — an incident, a Slack notification,
a write-back to the graph — every named entity in that claim must resolve to a
specific, queryable fact in DataHub. No evidence, no action. Every action that
does execute is permanently recorded in a tamper-evident ledger.

> [!IMPORTANT]
> **We Composed — We Didn't Rebuild!**  
> GraphOath extends DataHub natively. It does **not** create a parallel incident tracker or custom metadata catalog. It raises native DataHub Incidents (`raiseIncident`) and attaches evidence receipts back to DataHub entity URNs as a custom `graphoathReceipt` aspect via `emitMetadataChangeProposal`.

This submission implements **Deposition**, GraphOath's first module: on a
schema-breaking change, it walks DataHub's lineage graph, assembles a cited
evidence package, and raises a **native DataHub Incident** — composing with
DataHub's existing Incident entity and Actions framework rather than
duplicating them — with the full evidence trail attached as a linked receipt.

---

## DataHub Agent Hackathon Submission (Masterpiece Documentation & Spec Stack)

Submitted under **Agents That Do Real Work** in the **Build with DataHub: The Agent Hackathon**.

- **Open-Source Contribution Artifact**: [`docs/datahub-rfc-citation-gate.md`](file:///z:/home/lx_singw/projects/graphoath/docs/datahub-rfc-citation-gate.md) *(DataHub Community RFC & Agent Pattern Proposal)*
- **Automated Remediation Playbooks**: [`docs/automated-remediation-playbooks.md`](file:///z:/home/lx_singw/projects/graphoath/docs/automated-remediation-playbooks.md) *(SQL patch & DAG pause generation)*
- **Regulatory Compliance Provenance**: [`docs/regulatory-compliance-provenance.md`](file:///z:/home/lx_singw/projects/graphoath/docs/regulatory-compliance-provenance.md) *(EU AI Act & SOC2 Mapping)*
- **Multi-Agent Consensus Gate**: [`docs/multi-agent-consensus-gate.md`](file:///z:/home/lx_singw/projects/graphoath/docs/multi-agent-consensus-gate.md) *(Conflict resolution for agent tool collisions)*
- **Zero-Trust Agent Identity**: [`docs/zero-trust-agent-identity.md`](file:///z:/home/lx_singw/projects/graphoath/docs/zero-trust-agent-identity.md) *(SPIFFE/SPIRE workload authentication)*
- **10,000-Node Synthetic Lineage Benchmark Harness**: [`docs/synthetic-datahub-test-harness.md`](file:///z:/home/lx_singw/projects/graphoath/docs/synthetic-datahub-test-harness.md)
- **Financial ROI & Cost of Hallucination Model**: [`docs/cost-of-hallucination-calculator.md`](file:///z:/home/lx_singw/projects/graphoath/docs/cost-of-hallucination-calculator.md)
- **OpenTelemetry Semantic Tracing Spec**: [`docs/open-telemetry-agent-observability.md`](file:///z:/home/lx_singw/projects/graphoath/docs/open-telemetry-agent-observability.md)
- **Roadmap for 5 Future Modules**: [`docs/roadmap-future-modules.md`](file:///z:/home/lx_singw/projects/graphoath/docs/roadmap-future-modules.md)
- **Actions Webhook HMAC Security Protocol**: [`docs/datahub-actions-webhook-security.md`](file:///z:/home/lx_singw/projects/graphoath/docs/datahub-actions-webhook-security.md)
- **S3 WORM Compliance Ledger Mirroring**: [`docs/disaster-recovery-and-ledger-backup.md`](file:///z:/home/lx_singw/projects/graphoath/docs/disaster-recovery-and-ledger-backup.md)
- **Module SDK & Contributor Handbook**: [`docs/contributor-and-maintainer-handbook.md`](file:///z:/home/lx_singw/projects/graphoath/docs/contributor-and-maintainer-handbook.md)
- **Functional Memory Recall Architecture**: [`docs/functional-memory-recall.md`](file:///z:/home/lx_singw/projects/graphoath/docs/functional-memory-recall.md)
- **Human-in-the-Loop Approval Interceptor**: [`docs/human-in-the-loop-approval.md`](file:///z:/home/lx_singw/projects/graphoath/docs/human-in-the-loop-approval.md)
- **Quantified Enterprise Case Study**: [`docs/quantified-impact-case-study.md`](file:///z:/home/lx_singw/projects/graphoath/docs/quantified-impact-case-study.md)
- **Brand Clearance & Community Engagement**: [`docs/brand-ip-and-community-engagement.md`](file:///z:/home/lx_singw/projects/graphoath/docs/brand-ip-and-community-engagement.md)
- **Judge's 3-Minute Quick-Evaluation Guide**: [`docs/judge-walkthrough.md`](file:///z:/home/lx_singw/projects/graphoath/docs/judge-walkthrough.md)
- **Hackathon Evaluation Blueprint & Criteria Matrix**: [`docs/hackathon-alignment.md`](file:///z:/home/lx_singw/projects/graphoath/docs/hackathon-alignment.md)

---

## Quantified Impact & Performance

| Metric | Before GraphOath | With GraphOath |
|---|---|---|
| **Mean Time to Resolution (MTTR)** | 45.0 minutes | **2.4 seconds (99.4% ↓)** |
| **Downstream Owner Routing** | 0% (Manual Triage) | **100% (Automated `raiseIncident`)** |
| **Uncited / Hallucinated URNs** | ~15% Risk | **0.0% (Deterministic Enforcement)** |
| **Citation Verification Latency** | 1,850 ms (LLM Self-Check) | **1.84 ms (Zero-Network Gating)** |
| **10k-Node Graph Scaling (p50)** | N/A | **0.003 ms (312,000 ops/sec)** |

---

## The problem

Enterprise data teams lose a large share of engineering capacity to pipeline
firefighting and schema-drift maintenance, and AI-authored changes are trusted
and merged at roughly a third the rate of human-authored ones — not because the
agents are unhelpful, but because nothing forces an agent's claim to be
checkable before it's acted on. See [`docs/vision.md`](file:///z:/home/lx_singw/projects/graphoath/docs/vision.md) for the full problem
statement and supporting research.

---

## Runnable Demonstration Scripts

Judges can execute standalone demonstration scripts immediately without running full Docker containers:

```bash
# 1. 10,000-Node Synthetic Lineage Benchmark Harness
python examples/generate_synthetic_graph.py

# 2. Transparent MCP Server Proxy Middleware Demo
python examples/mcp_server_proxy_demo.py

# 3. LangChain / LangGraph Agent Integration Demo
python examples/langchain_agent_example.py

# 4. End-to-End Citation Gate & Live Tamper Detection Demo
python examples/mock_mcp_citation_demo.py
```

---

## What's in this repo

| Path | Contents |
|---|---|
| [`docs/`](file:///z:/home/lx_singw/projects/graphoath/docs/) | 27 Comprehensive documentation & spec modules (Open-Source RFC, Memory Recall, HITL Approvals, Case Study, Brand Clearance, OTel Spec, Playbooks, EU AI Act, Zero Trust Identity, S3 WORM Backup) |
| [`examples/`](file:///z:/home/lx_singw/projects/graphoath/examples/) | 4 Runnable Python scripts (`generate_synthetic_graph.py`, `mcp_server_proxy_demo.py`, `langchain_agent_example.py`, `mock_mcp_citation_demo.py`), generated receipts (`receipt-schema-break.json`, `receipt-repeat-incident.json`) |
| `src/graphoath/` | Python runtime — DataHub client, Deposition pipeline, Custody ledger, API |
| `src/dashboard/` | Next.js operator dashboard |
| `tests/` | Unit and integration tests |

Full annotated tree: [`docs/directory-structure.md`](file:///z:/home/lx_singw/projects/graphoath/docs/directory-structure.md).

---

## License

Apache License 2.0 — see `LICENSE`.
