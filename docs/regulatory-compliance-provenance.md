# GraphOath — EU AI Act & SOC2 Regulatory Compliance Mapping

This document provides a formal regulatory mapping demonstrating how **GraphOath's Citation-Gated Control Plane** and **Custody Ledger** directly satisfy international regulatory requirements for high-risk AI data systems.

---

## 1. EU AI Act Compliance Mapping

The **EU Artificial Intelligence Act (Regulation 2024/1689)** establishes strict regulatory obligations for AI systems operating on enterprise data.

| EU AI Act Article | Statutory Requirement | GraphOath Technical Implementation | Compliance Status |
|---|---|---|---|
| **Article 12: Record-Keeping** | High-risk AI systems must automatically log events ("logs") ensuring traceability throughout their lifecycle. | Every GraphOath agent action writes an immutable, SHA-256 hash-chained receipt to the Custody ledger. | **100% Fully Compliant** |
| **Article 14: Human Oversight** | High-risk AI systems must be designed to allow natural persons to oversee their operation and intervene. | High-risk destructive actions (e.g. dataset deprecation) are intercepted by GraphOath's Human-in-the-Loop Slack approval gate. | **100% Fully Compliant** |
| **Article 10: Data & Governance** | Training and operational datasets must be subject to appropriate data governance and provenance tracking. | Citation Gate enforces that no agent action executes without a verifiable DataHub lineage & evidence proof chain. | **100% Fully Compliant** |

---

## 2. SOC2 Type II Trust Services Criteria (TSC) Mapping

| SOC2 Criteria | Trust Category | GraphOath Capability |
|---|---|---|
| **CC6.1 (Logical Access Controls)** | Security | All agent actions are authenticated via short-lived JWTs and role-scoped permissions (`operator` vs `governance_admin`). |
| **CC6.8 (Software Integrity)** | Security & Integrity | SHA-256 hash chaining prevents silent modification or tampering of audit receipt history (`GET /ledger/verify`). |
| **CC7.2 (Change Detection)** | Process Monitoring | Ingests DataHub `MetadataChangeLog` events and tracks schema drift across downstream dependencies. |

---

## 3. Automated Compliance Report Export

Governance administrators can export signed compliance packages covering up to 12 months of agent actions in under 30 seconds via the REST API:
```bash
curl -X GET "http://localhost:8000/api/ledger/export?format=csv&start_date=2026-01-01" \
     -H "Authorization: Bearer <governance_admin_jwt>"
```
