# GraphOath — Zero-Knowledge Judge Setup & Execution Guide

Welcome Judges! This guide is written with **zero assumptions**. Whether you are running on Windows, macOS, or Linux, follow these step-by-step instructions to set up, install, and run GraphOath in **under 3 minutes**.

---

## 📋 Prerequisites Checklist

Before you begin, ensure you have:
1. **Python 3.10, 3.11, 3.12, or 3.13** installed (`python --version` or `python3 --version`).
2. **Git** installed (`git --version`).

> [!NOTE]
> No local DataHub cluster, PostgreSQL, or Docker setup is required to run the standalone evaluation suite. Everything runs out of the box using built-in Python evaluation runners.

---

## 🚀 Step 1: Clone the Repository

Open your terminal (PowerShell, Bash, or Zsh) and clone the repository:

```bash
git clone https://github.com/lx-singw/graphoath.git
cd graphoath
```

---

## 🐍 Step 2: Create & Activate Virtual Environment

### On Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(If PowerShell blocks script activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first)*.

### On macOS / Linux (Bash or Zsh):
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 📦 Step 3: Install Dependencies

Install the project dependencies in your active virtual environment:

```bash
pip install -r requirements.txt
```

*(Alternatively, install in editable development mode)*:
```bash
pip install -e .
```

---

## ⚡ Step 4: Run the 1-Command Fast-Track Evaluation Suite

Execute our master evaluation script to verify all 8 technical components of GraphOath in 30 seconds:

### On Windows (PowerShell):
```powershell
$env:PYTHONPATH="src"; python scripts/fast_track_evaluation.py
```

### On macOS / Linux (Bash / Zsh):
```bash
PYTHONPATH="src" python scripts/fast_track_evaluation.py
```

### Expected Output:
```
========================================================================
  GraphOath — Standalone Verification & Evaluation Runner
========================================================================

[EXECUTING VERIFICATION STEP] Custody Ledger Tamper Pytest Suite...
  --> [PASS] Custody Ledger Tamper Pytest Suite

[EXECUTING VERIFICATION STEP] Agent Key Signature Verification...
  --> [PASS] Agent Key Signature Verification

[EXECUTING VERIFICATION STEP] Continuous Audit Daemon Verification...
  --> [PASS] Continuous Audit Daemon Verification

[EXECUTING VERIFICATION STEP] Circuit Breaker & Resilience Verification...
  --> [PASS] Circuit Breaker & Resilience Verification

[EXECUTING VERIFICATION STEP] Financial Impact Model Estimator...
  --> [PASS] Financial Impact Model Estimator

[EXECUTING VERIFICATION STEP] OpenTelemetry Semantic Telemetry Trace Emitter...
  --> [PASS] OpenTelemetry Semantic Telemetry Trace Emitter

[EXECUTING VERIFICATION STEP] Real-World Multi-Platform Pipeline Triage Simulation...
  --> [PASS] Real-World Multi-Platform Pipeline Triage Simulation

[EXECUTING VERIFICATION STEP] Documentation Link Integrity Verifier...
  --> [PASS] Documentation Link Integrity Verifier

========================================================================
  VERIFICATION SUMMARY: 8/8 Steps Completed Successfully
========================================================================
```

---

## 🎮 Step 5: Run Interactive Demos (Optional Deep-Dive)

Judges can launch an interactive terminal menu to test individual components:

```powershell
$env:PYTHONPATH="src"; python examples/master_demo.py
```

### Individual Script Commands:

| Demonstration Target | Description | Command |
| :--- | :--- | :--- |
| **Real-World Triage** | Snowflake -> dbt -> Looker schema-break triage | `$env:PYTHONPATH="src"; python examples/realworld_pipeline_triage_demo.py` |
| **Agent Gating** | Uncited claim vs cited claim interception | `$env:PYTHONPATH="src"; python examples/langchain_agent_example.py` |
| **Financial ROI Model** | Cost of hallucination ROI savings calculator | `$env:PYTHONPATH="src"; python examples/cost_calculator_demo.py` |
| **OpenTelemetry Spans** | Native OTel trace span emitter | `$env:PYTHONPATH="src"; python examples/otel_tracing_demo.py` |
| **Ledger Security** | SHA-256 hash chain tamper verification | `$env:PYTHONPATH="src"; python -m pytest tests/test_ledger_tamper.py` |

---

## 🐳 Step 6: Full-Stack Docker Deployment (Optional UI & API Evaluation)

If you wish to evaluate the Next.js Operator Dashboard and live FastAPI REST server:

```bash
docker compose -f deployments/docker-compose.prod.yml up -d
```

- **Operator Dashboard**: Open [http://localhost:3000](http://localhost:3000)
- **FastAPI OpenAPI REST Specs**: Open [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ❓ Troubleshooting & FAQs

### Q: `ModuleNotFoundError: No module named 'graphoath'`
**Solution**: Make sure `PYTHONPATH` is set to `"src"`.
- Windows PowerShell: `$env:PYTHONPATH="src"` before calling `python`.
- Linux/macOS: `PYTHONPATH="src" python ...` or `export PYTHONPATH="src"`.

### Q: PowerShell script execution error when activating `venv`
**Solution**: Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in PowerShell, then retry `.\venv\Scripts\Activate.ps1`.
