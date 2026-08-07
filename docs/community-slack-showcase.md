# DataHub Community Slack Announcement Template (`#agent-hackathon`)

Copy-paste ready post template for sharing GraphOath in the DataHub Community Slack:

```text
🚀 Hey DataHub Community! We're excited to submit **GraphOath** for Build with DataHub: The Agent Hackathon!

🤖 **The Unresolved Crisis**: Catalog vendors spent 18 months giving AI agents READ access to metadata. But what stops an agent from hallucinating asset URNs or making un-auditable WRITE mutations to production?

🛡️ **Our Solution**: GraphOath — The Citation-Gated Control Plane for DataHub AI Agents.
Before any agent write call executes (`raiseIncident`, `emitMetadataChangeProposal`):
1️⃣ **Evidence Gathering**: Queries DataHub MCP Server (lineage, ownership, quality assertions).
2️⃣ **Zero-Trust Citation Gate**: Verifies that every claim URN is backed by queryable DataHub context in < 5ms (`Ref(Claims) ⊆ Ref(Evidence)`).
3️⃣ **Native Graph Action**: Raises native DataHub Incidents (`raiseIncident`) and attaches tamper-evident `graphoathReceipt` aspects to the metadata graph.

⚡ **1-Command Fast-Track Judge Evaluation**:
```bash
git clone https://github.com/lx-singw/graphoath.git
cd graphoath
python scripts/fast_track_evaluation.py
```

📦 **Open-Source Artifacts**:
- 📜 **PR-Ready Avro Aspect Schema**: `schemas/graphoathReceipt.avsc`
- 🎮 **Interactive Master CLI Menu**: `python examples/master_demo.py`
- 📖 **120-Sec Judge Guide**: `docs/judge-walkthrough.md`
- 📝 **DataHub Community RFC**: `docs/datahub-rfc-citation-gate.md`

We'd love your feedback! 🙌
```
