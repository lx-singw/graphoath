# GraphOath — Complete Setup & Execution Guide for Judges

Welcome Judges! GraphOath supports **two complete execution paths**:

- 🐳 **Method 1: Docker Compose Setup (1-Command Full-Stack Containerized Setup)** — Runs PostgreSQL, FastAPI REST API Server, Database Migrations, and Next.js Operator Dashboard inside Docker containers.
- ⚡ **Method 2: Standalone Python Fast-Track Runner (No Docker Required)** — Runs all 8 verification steps and demo simulations directly in Python in 30 seconds.

---

## 🐳 Method 1: Docker Compose Setup (Recommended Full-Stack)

If you have **Docker & Docker Compose** installed (`docker --version`), you can launch the entire GraphOath stack with **1 command**:

### Step 1: Clone the Repository & Copy Environment File
```bash
git clone https://github.com/lx-singw/graphoath.git
cd graphoath
cp .env.example .env
```

### Step 2: Launch Full Stack via Docker Compose
```bash
docker compose -f deployments/docker-compose.yml up --build -d
```
*(Or if using legacy docker-compose)*:
```bash
docker-compose -f deployments/docker-compose.yml up --build -d
```

### Step 3: Access Live Services
Once the containers start up:
- 📊 **FastAPI REST API Specs & OpenAPI Docs**: Open [http://localhost:8000/docs](http://localhost:8000/docs)
- 🛡️ **Audit Ledger Verification Endpoint**: Open [http://localhost:8000/api/v1/ledger/verify](http://localhost:8000/api/v1/ledger/verify)
- 🖥️ **Operator Dashboard**: Open [http://localhost:3000](http://localhost:3000)

### Step 4: Run Evaluation Suite Inside Docker Container
```bash
docker compose -f deployments/docker-compose.yml exec api python scripts/fast_track_evaluation.py
```

---

## ⚡ Method 2: Standalone Python Setup (No Docker Required)

If you prefer evaluating GraphOath without running Docker daemons:

### Prerequisites:
- **Python 3.10+** (`python --version`)
- **Git** (`git --version`)

### Step 1: Clone & Setup Virtual Environment
```bash
git clone https://github.com/lx-singw/graphoath.git
cd graphoath
```

**On Windows (PowerShell)**:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On macOS / Linux (Bash/Zsh)**:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Fast-Track Evaluation Suite (30 Seconds)

**On Windows (PowerShell)**:
```powershell
$env:PYTHONPATH="src"; python scripts/fast_track_evaluation.py
```

**On macOS / Linux (Bash/Zsh)**:
```bash
PYTHONPATH="src" python scripts/fast_track_evaluation.py
```

---

## 🎮 Interactive Demo Menu

Judges can interactively select and execute individual demos from an intuitive CLI menu:

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

## ❓ Troubleshooting & FAQs

### Q: `docker compose` returns permission denied or connection error
**Solution**: Ensure Docker Desktop or the Docker daemon is running on your host system (`docker ps`).

### Q: `ModuleNotFoundError: No module named 'graphoath'` in Standalone Mode
**Solution**: Ensure `PYTHONPATH` is set to `"src"`. On Windows PowerShell, use `$env:PYTHONPATH="src"` before running the python command.
