# GraphOath — 3-Minute Demo Video Script & Storyboard

This document provides the complete narration script, timestamp breakdown, visual storyboard, and demonstration cues for the **≤3-minute hackathon demo video** submission for **Build with DataHub: The Agent Hackathon**.

---

## Video Specifications
- **Target Duration**: 2 minutes 45 seconds (max 3:00)
- **Track**: Agents That Do Real Work
- **Target Audience**: DataHub Community & Hackathon Judges

---

## Timed Narration Script & Visual Storyboard

| Time | On-Screen Visual | Audio Narration / Voiceover |
|---|---|---|
| **0:00 - 0:25** | Title Card: *GraphOath — Citation-Gated Control Plane for DataHub*. Cut to DataHub UI showing a complex lineage graph. | *"Enterprise data teams are adopting AI agents to automate pipeline firefighting. But here's the problem: when autonomous agents take actions—like raising incidents or deprecating datasets—they often hallucinate entities or act without verifiable proof. In production, unverified AI actions cause chaos."* |
| **0:25 - 0:50** | Slide/Diagram showing GraphOath sitting between AI Agent Frameworks (LangChain/LangGraph) and DataHub API. | *"Meet GraphOath: the citation-gated control plane for AI agents acting on DataHub. GraphOath enforces a simple rule: No evidence, no action. Every claim made by an agent must resolve to a queryable fact in DataHub's metadata graph before any action executes."* |
| **0:50 - 1:30** | Screen capture of Terminal executing `python examples/langchain_agent_example.py`. Highlight the `[X] REJECTED!` scenario. | *"Let's see it in action. Here, an agent detects a breaking schema change on an upstream orders table. In Scenario A, the agent drafts a claim referencing a hallucinated dataset URN. GraphOath's Citation Gate evaluates the claim against DataHub's live graph retrieved via MCP, detects the unverified URN, and instantly blocks the action from hitting DataHub."* |
| **1:30 - 2:10** | Highlight Scenario B (`[OK] PASSED!`). Switch screen to DataHub UI showing the native DataHub Incident raised. | *"In Scenario B, the agent revises its claim using verified downstream URNs. The Citation Gate passes the claim, raises a native DataHub Incident routed to the asset owner, and emits a custom graphoathReceipt aspect directly onto DataHub's graph."* |
| **2:10 - 2:35** | Show GraphOath Next.js Operator Dashboard (`http://localhost:3000`) displaying the hash-chained Custody receipt. | *"Every GraphOath action is written to a tamper-evident Custody ledger in PostgreSQL using SHA-256 hash chains. Governance teams can view the exact evidence trail behind every incident, or export compliance reports in seconds."* |
| **2:35 - 2:45** | Terminal showing `python examples/mock_mcp_citation_demo.py`. Callout to repo docs. | *"GraphOath supports DataHub's MCP Server, Agent Context Kit, LangChain, and LangGraph. You can test our standalone demo scripts right now in the repository. Thank you!"* |

---

## Recording Checklist for Presenters
- [ ] Record terminal at 1080p, font size 16pt for clear readability.
- [ ] Use clear microphone audio with noise suppression.
- [ ] Ensure DataHub UI demo instance is pre-loaded with `showcase-ecommerce` datapack.
- [ ] Verify both `langchain_agent_example.py` and `mock_mcp_citation_demo.py` execute cleanly before recording.
