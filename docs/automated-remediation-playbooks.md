# GraphOath — Citation-Gated Automated Remediation Playbooks

This document specifies **GraphOath's Automated Remediation Playbook Generator**, implemented in [`graphoath/playbooks.py`](graphoath/playbooks.py), which dynamically attaches verified, actionable remediation playbooks to native DataHub Incidents (`raiseIncident`) when pipeline schema breaks occur.

---

## 1. Overview & Remediation Safety

When an upstream schema break occurs (e.g. dropping a column or modifying a data type), traditional alerting only notifies engineers that something broke. GraphOath goes further: it walks the DataHub lineage graph via MCP, computes downstream blast radius, and **generates a citation-gated remediation playbook**.

```
 ┌─────────────────────────────────────────────────────────────┐
 │                Schema Break Detected on Dataset             │
 └──────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │               DataHub Lineage Traversal (MCP)                │
 └──────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │         Citation-Gated Playbook Generator Engine            │
 │  - Dataset Quarantine Tagging (`addTag`)                    │
 │  - dbt Model Pause Recommendation                           │
 │  - Hierarchical Owner Escalation                             │
 └──────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │         DataHub Incident Raised + Playbook Attached         │
 └──────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │         Interactive Slack Card Rendered ([Approve])         │
 └─────────────────────────────────────────────────────────────┘
```

---

## 2. Playbook Catalog & Python Module Architecture

GraphOath ships 3 standard playbooks in `graphoath/playbooks.py`:

1. **Dataset Quarantine Playbook (`RemediationPlaybooks.dataset_quarantine_playbook`)**:
   Applies a native `Quarantined` tag to downstream datasets in DataHub (`addTag`), preventing business analysts from querying unverified/corrupted data models.
2. **dbt Model Pause Playbook (`RemediationPlaybooks.dbt_model_pause_playbook`)**:
   Generates a dbt model deferral payload (`--defer --state ./prod_artifacts`) to pause downstream model execution during CI runs.
3. **Owner Escalation Playbook (`RemediationPlaybooks.owner_escalation_playbook`)**:
   Escalates unassigned or unacknowledged incidents to domain leads if unresolved after 15 minutes.

---

## 3. Human Approval Gate Integration

Playbook steps classified as `LOW_NON_DESTRUCTIVE` can be executed automatically by platform automation, while steps classified as `MEDIUM_REQUIRES_APPROVAL` are routed through GraphOath's Human-in-the-Loop Slack approval gate (`graphoath/slack_notifier.py`) before execution (see [`docs/human-in-the-loop-approval.md`](docs/human-in-the-loop-approval.md)).
