# GraphOath — Brand Clearance, IP Strategy & Community Engagement

This document details the **IP clearance strategy**, **trademark assessment**, **domain availability check**, and **DataHub Community Engagement Plan** for **GraphOath**.

---

## 1. Brand & Trademark Clearance Assessment

To ensure GraphOath maintains a clear commercial identity and zero trademark conflicts:

### 1.1 Mark Clearance: `GraphOath`
- **USPTO TESS / TSDR Search**: Performed clearance search for standard character mark `"GraphOath"`.
  - Class 042 (Software as a Service / Computer Software Development).
  - **Result**: Zero conflicting active live registrations or pending applications found under Class 042 for `"GraphOath"`.
- **Phonetic & Conceptual Uniqueness**: Combines *"Graph"* (DataHub Metadata Graph) + *"Oath"* (Verification / Unbreakable Contract). High inherent distinctiveness (Suggestive / Fanciful mark).

### 1.2 Domain Clearance Strategy
- Primary Target Domain: `graphoath.io` / `graphoath.dev`
- GitHub Organization Namespace: `github.com/lx-singw/graphoath`

---

## 2. DataHub Community Engagement Strategy

Winning a community-driven hackathon requires proactive visibility with the core open-source maintainers and community:

### 2.1 Slack Community Engagement Plan (`#agent-hackathon`)
1. **Public Proposal Sharing**: Post an announcement introducing GraphOath and linking to our open-source RFC ([`docs/datahub-rfc-citation-gate.md`](docs/datahub-rfc-citation-gate.md)).
2. **Key Message**: *"We built GraphOath to solve the agent hallucination risk by enforcing citation gating natively on DataHub. Check out our open-source RFC and runnable examples!"*
3. **Feedback Gathering**: Engage Acryl Data engineers in technical discussion around custom aspects (`graphoathReceipt`) and DataHub MCP Server tool performance.

---

## 3. Official Hackathon Feedback Survey Submission

As part of our commitment to the DataHub ecosystem, we submit structured feedback on the DataHub Agent Context Kit & MCP Server integration experience:

### Constructive Feedback Points Submitted:
1. **MCP Tool Error Output Structure**: Suggest standardizing error payloads in `search_across_lineage` when max hop depth is reached, to simplify agent retry loops.
2. **GraphQL Aspect Emission Latency**: Recommend adding batching support for `emitMetadataChangeProposal` when emitting custom aspects on multiple downstream nodes simultaneously.
3. **Documentation Praise**: Highlight the excellence of the DataHub Agent Context Kit documentation and GMS GraphQL schema ergonomics.
