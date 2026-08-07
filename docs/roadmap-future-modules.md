# GraphOath — Detailed Specifications for Future Roadmap Modules

This document details the complete architectural specifications for GraphOath's 5 future modules beyond **Deposition** (schema-break incident triage), demonstrating a comprehensive multi-year platform vision.

---

## Module 2: Undertow — ML Feature Drift & Lineage Provenance
- **Problem**: ML model accuracy degrades when underlying feature store tables experience silent drift or schema changes.
- **DataHub Integration**: Queries DataHub `dataset` and `mlModel` entities, tracing lineage from feature store tables to deployed model URNs.
- **Citation Gate Action**: Intercepts automated model re-training pipelines. If feature lineage citations are incomplete or drifted, Undertow blocks re-training and raises a native DataHub Incident.

---

## Module 3: Prune — FinOps Agent Cost Governance
- **Problem**: AI FinOps agents attempt to prune unqueried tables or terminate clusters, accidentally deleting datasets used in quarterly reporting.
- **DataHub Integration**: Queries DataHub `usage` aspects (90-day query volume, active user count) via MCP `get_dataset_usage`.
- **Citation Gate Action**: Requires 100% citation proof that a dataset has 0 queries across 90 days before allowing a `deprecateDataset` action.

---

## Module 4: Rosetta — Automated Metadata & Glossary Capture
- **Problem**: Data engineers omit business glossary terms, leaving datasets uncontextualized for AI agents.
- **DataHub Integration**: Extracts semantic context from dbt model descriptions and queries DataHub `glossaryTerm` entities.
- **Citation Gate Action**: Citation-gates AI-suggested glossary term bindings (`addGlossaryTerm`), ensuring terms exist in the official enterprise dictionary before tagging.

---

## Module 5: ReguLineage — PII Exposure & Privacy Compliance
- **Problem**: PII data fields propagate through transformation pipelines without proper tag propagation.
- **DataHub Integration**: Queries DataHub `structuredProperty` and `fineGrainedLineage` aspects.
- **Citation Gate Action**: Automatically propagates `PII_CONFIDENTIAL` tags down the lineage graph and raises compliance incidents on untagged downstream copies.

---

## Module 6: Redline — Policy Enforcement & Access Control
- **Problem**: Autonomous agents grant elevated data warehouse permissions to service accounts without security review.
- **DataHub Integration**: Queries DataHub `corpGroup` and access control policies.
- **Citation Gate Action**: Intercepts role grant calls and routes Tier 2 access escalations through GraphOath's Human-in-the-Loop Slack approval gate.
