# DataHub Agent Hackathon — Devpost & Community Launch Kit

This document provides copy-paste ready promotional copy, taglines, and Slack announcement posts for submitting **GraphOath** to **Build with DataHub: The Agent Hackathon**.

---

## 1. Devpost Submission Details

* **Project Name**: GraphOath
* **Tagline**: *"The Citation-Gated Control Plane for Autonomous AI Agents Acting on DataHub."*
* **Track**: **Agents That Do Real Work** (Primary Track)
* **GitHub Repository**: `https://github.com/lx-singw/graphoath`

### Elevator Pitch (Summary Section)
> As AI agents automate enterprise data operations—such as schema-drift maintenance, pipeline triage, and automated remediation—allowing agents to execute unverified write operations directly against production metadata catalogs leads to hallucinated entity references, unassigned incidents, and un-auditable state changes.
>
> **GraphOath** is an open-source, citation-gated control plane middleware for AI agents operating on DataHub. Before any agent-initiated claim produces a write action (e.g. `raiseIncident`, `emitMetadataChangeProposal`), GraphOath's deterministic Citation Gate verifies that every entity URN named in the agent's claim resolves to a queryable fact in DataHub's metadata graph (retrieved via MCP or Agent Context Kit).

---

## 2. DataHub Community Slack Announcement Draft

**Target Channel**: `#agent-hackathon` / `#showcase`

```text
🚀 Hey DataHub Community! We're excited to introduce GraphOath for Build with DataHub: The Agent Hackathon!

🤖 The Problem: When AI agents automate pipeline triage or schema fixes, how do you prevent them from hallucinating entity URNs or making un-auditable changes to your catalog?

🛡️ Our Solution: GraphOath ("The Citation-Gated Control Plane for DataHub Agents").
GraphOath sits between AI agents and DataHub. Before any agent write call executes:
1️⃣ Evidence Gathering: Queries DataHub MCP Server (lineage, ownership, quality assertions).
2️⃣ Zero-Trust Citation Gate: Verifies that every claim URN is backed by queryable DataHub context (in < 5ms).
3️⃣ Native Graph Action: Raises native DataHub Incidents (`raiseIncident`) and attaches tamper-evident `graphoathReceipt` aspects to the graph.

⚡ Fast-Track 60-Second Terminal Demo:
```bash
git clone https://github.com/lx-singw/graphoath.git
cd graphoath
python examples/mock_mcp_citation_demo.py
```

📖 Check out our full submission and docs:
- 120-Sec Judge Guide: https://github.com/lx-singw/graphoath/blob/main/docs/judge-walkthrough.md
- DataHub RFC Proposal: https://github.com/lx-singw/graphoath/blob/main/docs/datahub-rfc-citation-gate.md

We'd love your feedback! 🙌
```
