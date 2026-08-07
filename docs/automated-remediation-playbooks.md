# GraphOath — Citation-Gated Automated Remediation Playbooks

This document specifies **GraphOath's Automated Remediation Playbook Generator**, which dynamically attaches verified, actionable remediation playbooks to native DataHub Incidents (`raiseIncident`) when pipeline schema breaks occur.

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
 │  - Identifies affected dbt models & Airflow DAGs            │
 │  - Generates SQL alias patches & DAG pause commands         │
 │  - Verifies all target URN citations against graph          │
 └──────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │         DataHub Incident Raised + Playbook Attached         │
 └─────────────────────────────────────────────────────────────┘
```

---

## 2. Playbook Structure & JSON Aspect Format

Remediation playbooks are attached to DataHub Incidents as structured metadata:

```json
{
  "playbook_id": "ply_schema_break_orders_001",
  "source_urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)",
  "incident_urn": "urn:li:incident:graphoath-dep-20260807-001",
  "remediation_actions": [
    {
      "step": 1,
      "type": "SQL_COLUMN_ALIAS_PATCH",
      "target_urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.stg_orders,PROD)",
      "recommended_sql": "SELECT COALESCE(customer_id, legacy_customer_id) AS customer_id FROM prod.orders",
      "risk_level": "LOW_NON_DESTRUCTIVE"
    },
    {
      "step": 2,
      "type": "PAUSE_AIRFLOW_DAG",
      "target_dag_id": "dag_daily_revenue_aggregation",
      "command": "airflow dags pause dag_daily_revenue_aggregation",
      "risk_level": "MEDIUM_REQUIRES_APPROVAL"
    }
  ]
}
```

---

## 3. Human Approval Gate Integration

Playbook steps classified as `LOW_NON_DESTRUCTIVE` can be executed automatically by platform automation, while steps classified as `MEDIUM_REQUIRES_APPROVAL` are routed through GraphOath's Human-in-the-Loop Slack approval gate before execution (see [`docs/human-in-the-loop-approval.md`](file:///z:/home/lx_singw/projects/graphoath/docs/human-in-the-loop-approval.md)).
