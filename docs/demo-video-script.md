# GraphOath — 180-Second Presentation Video Script & Storyboard

**Total Length**: 3 Minutes (180 Seconds)  
**Target Audience**: DataHub Hackathon Judges & Data Platform Engineers

---

## Storyboard & Line-by-Line Script

### [0:00 - 0:30] Phase 1: The Unresolved Enterprise Problem
* **Visual**: Terminal screen showing a naive AI agent hallucinating a fake dataset URN (`prod.hallucinated_table`) and filing a broken incident directly into production.
* **Voiceover**:
  > *"Every enterprise adopting AI agents for data operations faces the same crisis: catalog vendors spent eighteen months racing to give agents READ access to metadata via MCP servers and GraphQL. But nobody built governance for the WRITE side. When an agent hallucinated an asset name, it broke production."*

---

### [0:30 - 1:15] Phase 2: Introducing GraphOath & Zero-Trust Citation Gating
* **Visual**: Cut to architecture diagram in [`docs/visualizer.html`](file:///z:/home/lx_singw/projects/graphoath/docs/visualizer.html). Switch to terminal and run `python examples/langchain_agent_example.py`.
* **Voiceover**:
  > *"Meet GraphOath — the citation-gated control plane for AI agents acting on DataHub. GraphOath sits between agents and your catalog. In Scenario A, our LangChain agent tries to raise an incident on an unverified table. GraphOath's Citation Gate catches it in under 5 milliseconds and returns REJECTED, blocking the write. In Scenario B, the agent provides valid DataHub lineage citations — GraphOath verifies the proof chain and raises a native DataHub Incident."*

---

### [1:15 - 2:00] Phase 3: Real-World Multi-Platform Pipeline Triage & Slack Approval
* **Visual**: Terminal executing `python examples/realworld_pipeline_triage_demo.py`. Highlight the rendered Slack Block Kit card JSON and executed Quarantine remediation playbook.
* **Voiceover**:
  > *"Watch Deposition, GraphOath's flagship module, handle a real-world Snowflake schema break. It traces 3 hops across Snowflake, dbt, and Looker, resolves hierarchical owners, renders an interactive Slack approval card, and executes automated dataset quarantine playbooks — reducing manual MTTR from 45 minutes down to 2.4 seconds."*

---

### [2:00 - 2:30] Phase 4: Cryptographic Ledger & Live Tamper Detection
* **Visual**: Terminal running `python examples/mock_mcp_citation_demo.py`. Show the live database tampering simulation and instant detection alert.
* **Voiceover**:
  > *"Every verified action is permanently bound to DataHub via custom `graphoathReceipt` aspects and written to an append-only SHA-256 Postgres hash ledger. If a malicious actor alters a record in the database, GraphOath detects the hash mismatch instantly and freezes automated write permissions."*

---

### [2:30 - 3:00] Phase 5: Fast-Track Judge Evaluation & Open-Source Vision
* **Visual**: Run `python scripts/fast_track_evaluation.py`. Show the 10/10 Verification Green Checklist.
* **Voiceover**:
  > *"GraphOath features an official PR-ready Avro aspect schema, a $442,500 annual ROI model, and 1-command fast-track evaluation for judges. Try it today in 1 line: python scripts/fast_track_evaluation.py. No evidence, no action. Thank you!"*
