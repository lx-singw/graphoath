# 📊 GraphOath Sample Output Artifacts Showcase

> **For Hackathon Judges**: This directory contains pre-generated, production-grade output artifacts produced by GraphOath during real-world AI agent tool interception, pipeline triage, ledger verification, and OpenTelemetry trace collection. You can inspect these files directly without installing or running any code.

---

## 📂 Sample Outputs Inventory

| Sample Output File | Category | Description | Key Highlights |
| :--- | :--- | :--- | :--- |
| 📄 [`1_pipeline_triage_incident_report.md`](./1_pipeline_triage_incident_report.md) | **Automated Incident Triage** | Full root-cause analysis report for a Snowflake $\rightarrow$ dbt $\rightarrow$ Looker schema break | Blast radius calculation ($142.5k revenue at risk), dbt quarantine playbooks, DataHub incident URNs |
| 🛡️ [`2_cryptographic_receipt_audit_ledger.json`](./2_cryptographic_receipt_audit_ledger.json) | **Audit & Security** | JSON ledger export of SHA-256 cryptographic verification receipts | Merkle hash chain ($H_{n-1} \rightarrow H_n$), Citation Gate SLA timing (1.4ms evaluation), TrustTag payload |
| 📡 [`3_opentelemetry_trace_export.json`](./3_opentelemetry_trace_export.json) | **Observability** | Standard W3C OpenTelemetry JSON trace span hierarchy | Nested OTel spans, OTLP exporter payloads, OLS latency tracking |
| 💰 [`4_financial_roi_hallucination_savings.md`](./4_financial_roi_hallucination_savings.md) | **Financial ROI Model** | Cost-of-Hallucination ROI analysis | Annual savings calculations ($480,000+ saved per 1,000 agent queries/day) |

---

## ⚡ Quick Links to Original Demo Scripts

If you wish to execute the code live, run any of the following standard Python scripts:
```powershell
# Run 30-Second Fast-Track Verification Suite
$env:PYTHONPATH="src"; python scripts/fast_track_evaluation.py

# Run Schema Break & Pipeline Triage Demo
$env:PYTHONPATH="src"; python examples/realworld_pipeline_triage_demo.py

# Run OpenTelemetry Spans & Governance Metrics Demo
$env:PYTHONPATH="src"; python examples/otel_tracing_demo.py

# Run Financial ROI Model Calculator Demo
$env:PYTHONPATH="src"; python examples/cost_calculator_demo.py
```
