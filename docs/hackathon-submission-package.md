# 🏆 GraphOath — Official Hackathon Submission Package

> **The Citation-Gated Control Plane for Autonomous AI Agents acting on DataHub**

---

## 📌 1. Project & Repository Links

- **Public GitHub Repository**: [https://github.com/lx-singw/graphoath](https://github.com/lx-singw/graphoath)
- **Open Source License**: [Apache 2.0 License](https://github.com/lx-singw/graphoath/blob/main/LICENSE) *(Visible in repository root & GitHub About section)*
- **Interactive API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Operator Governance Dashboard**: [http://localhost:3000](http://localhost:3000)
- **Live DataHub Platform**: [http://localhost:9002](http://localhost:9002)

---

## 📝 2. Submission Text Summary (Copy-Paste Ready)

### Short Pitch (Elevator Summary)
**GraphOath** is an enterprise-grade, citation-gated control plane that intercepts AI agent tool executions and structured data generation. Powered by DataHub's metadata graph, `datahub-agent-context`, and an OTel-instrumented cryptographic verification engine, GraphOath guarantees that no autonomous agent can mutate production databases, run dbt pipelines, or report metrics without cryptographic proof of lineage and schema compliance.

### What It Does
1. **Citation-Gated Execution**: Intercepts LangChain/LlamaIndex agent tool calls and LLM outputs. Rejects uncited claims and halts unverified database mutations in under 5 milliseconds.
2. **Multi-Hop Graph Lineage Verification**: Uses `datahub-agent-context` to dynamically traverse upstream & downstream dependencies across Snowflake, dbt, Airflow, and Looker.
3. **Cryptographic Tamper-Proof Receipts**: Generates SHA-256 linked cryptographic receipts stored in PostgreSQL with 1-click ledger integrity verification.
4. **Native DataHub Incident & Tag Management**: Automatically creates active incident tickets and applies `TrustTags` (`TRUSTED` / `UNTRUSTED`) directly onto DataHub metadata entities via GMS GraphQL APIs.
5. **Enterprise Observability & SLI**: End-to-end OpenTelemetry (OTel) trace spans dispatched to Jaeger and Prometheus metrics tracking Citation Gate evaluation latency.

### How We Built It
- **Core Engine & Citation Gate**: Python 3.11, FastAPI, Pydantic v2, `datahub-agent-context`, `acryl-datahub`.
- **Operator Dashboard**: Next.js 14, TailwindCSS, Lucide Icons, WebSockets for real-time triage streams.
- **Persistence & Cryptography**: PostgreSQL, SQLAlchemy async ORM, SHA-256 merkle hash chaining.
- **Deployment**: 1-Command Docker Compose deployment stack bundle (`api`, `dashboard`, `postgres`, `datahub-frontend`, `datahub-gms`, `opensearch`, `kafka`, `mysql`).

---

## 🎬 3. Video Demo Script & Recording Guide (Under 3 Minutes)

| Time | Visual Screen | Voiceover / Action Script |
| :--- | :--- | :--- |
| **0:00 - 0:30** | Split view of **GraphOath Dashboard** (`http://localhost:3000`) and **DataHub UI** (`http://localhost:9002`). | *"Autonomous AI agents are making critical decisions on enterprise data stacks. But when an agent hallucination breaks a schema or mutates an uncited table, the financial cost can reach thousands. Meet **GraphOath**, the citation-gated control plane for AI agents on DataHub."* |
| **0:30 - 1:15** | Terminal executing `$env:PYTHONPATH="src"; python examples/langchain_agent_example.py` | *"Here we run an agent attempting to mutate `prod.orders`. First, the agent submits an uncited claim. GraphOath's Citation Gate intercepts it instantly, returning a 422 Citation Failed status and blocking execution. Next, the agent provides a verified DataHub dataset URN. GraphOath traverses DataHub's metadata graph, verifies the lineage, and allows execution."* |
| **1:15 - 2:00** | Terminal executing `$env:PYTHONPATH="src"; python examples/realworld_pipeline_triage_demo.py` & DataHub Incident UI | *"Now watch real-world triage in action. A upstream Snowflake schema change breaks downstream dbt models and Looker dashboards. GraphOath detects the break, computes affected revenue metrics, creates a native incident on DataHub, and alerts the team in real-time."* |
| **2:00 - 2:45** | GraphOath Dashboard Ledger Page (`http://localhost:3000/ledger`) & API Swagger (`http://localhost:8000/docs`) | *"Every evaluation produces a cryptographic SHA-256 verification receipt. Clicking 'Verify Ledger' proves that audit logs have zero tampering. Combined with OpenTelemetry trace spans and sub-5ms evaluation SLAs, GraphOath is enterprise-ready."* |
| **2:45 - 3:00** | GitHub Repository & Quickstart Command | *"GraphOath is 100% open source, fully containerized with Docker Compose, and ready for deployment today. Thank you!"* |

---

## 📁 4. Key Repository Assets & Sample Outputs

Judges can evaluate sample outputs directly in the repo without running code:
- **Fast-Track Suite**: [`scripts/fast_track_evaluation.py`](file:///z:/home/lx_singw/projects/graphoath/scripts/fast_track_evaluation.py)
- **Triage Demo**: [`examples/realworld_pipeline_triage_demo.py`](file:///z:/home/lx_singw/projects/graphoath/examples/realworld_pipeline_triage_demo.py)
- **OpenTelemetry Demo**: [`examples/otel_tracing_demo.py`](file:///z:/home/lx_singw/projects/graphoath/examples/otel_tracing_demo.py)
- **ROI Cost Model**: [`examples/cost_calculator_demo.py`](file:///z:/home/lx_singw/projects/graphoath/examples/cost_calculator_demo.py)
- **FastAPI OpenAPI Schema**: [`docs/openapi.json`](file:///z:/home/lx_singw/projects/graphoath/docs/openapi.json)
