# GraphOath — Installation Guide

## 1. System Requirements

| Component | Minimum |
|---|---|
| Operating System | Linux (Ubuntu 22.04+ recommended), macOS 13+, or WSL2 on Windows 11 |
| Python runtime | Python 3.12.x |
| Node.js runtime | Node.js 20.x LTS |
| Database | PostgreSQL 15+ (local via Docker, or a managed instance such as Neon) |
| DataHub | A reachable DataHub instance, version 0.14+, with GraphQL API and MCP Server enabled |
| RAM | 4 GB minimum for local development stack (Postgres + FastAPI + Next.js); 8 GB recommended |
| Disk | 2 GB free for dependencies and container images |
| Docker | Docker Engine 24+ and Docker Compose v2, if using the containerized setup |

## 2. Step-by-Step Setup

### 2.1 Clone the repository

```bash
git clone https://github.com/graphoath/graphoath.git
cd graphoath
```

### 2.2 Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and set the following required values:

```
DATAHUB_GMS_URL=http://localhost:8080
DATAHUB_TOKEN=<your-datahub-personal-access-token>
DATABASE_URL=postgresql://graphoath:graphoath@localhost:5432/graphoath
SLACK_WEBHOOK_URL=<your-slack-incoming-webhook-url>
JWT_SECRET=<generate-with-openssl-rand-hex-32>
```

### 2.3 Start dependencies via Docker Compose

```bash
docker compose up -d postgres
```

Confirm Postgres is healthy:

```bash
docker compose ps
```

### 2.4 Install backend dependencies

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2.5 Run database migrations

```bash
python -m graphoath.db.migrate
```

Expected output ends with:

```
Applied migration 0001_initial.sql
Database schema up to date.
```

### 2.6 Seed the DataHub showcase datapack (local development only)

```bash
python scripts/seed_showcase_datapack.py --datahub-url $DATAHUB_GMS_URL
```

### 2.7 Install and build the dashboard

```bash
cd src/dashboard
npm install
npm run build
cd ../..
```

### 2.8 Start the full local stack

```bash
docker compose up
```

This starts Postgres, the FastAPI runtime on `http://localhost:8000`, and the
Next.js dashboard on `http://localhost:3000`.

### 2.9 Verify the installation

```bash
curl http://localhost:8000/api/ledger/verify
```

Expected response: `{"status": "intact", "receipts_checked": 0, ...}` on a fresh
install.

Open `http://localhost:3000` in a browser and confirm the dashboard loads and
prompts for login.

## 3. Troubleshooting Matrix

| Symptom | Likely Cause | Resolution |
|---|---|---|
| `psycopg2.OperationalError: could not connect to server` on migration | Postgres container not yet healthy when migration ran | Run `docker compose ps` to confirm `postgres` shows `healthy`, then re-run `python -m graphoath.db.migrate`. If it never becomes healthy, run `docker compose logs postgres` and check for a port conflict on 5432. |
| `401 Unauthorized` from every DataHub call in the logs | `DATAHUB_TOKEN` is missing, expired, or scoped without GraphQL/metadata-write permission | Regenerate a personal access token in DataHub under **Settings → Access Tokens**, ensure it has metadata read and write scope, and update `.env`, then restart the runtime container. |
| Dashboard loads but shows "Network Error" on every page | `NEXT_PUBLIC_API_BASE_URL` in `src/dashboard/.env.local` does not match the FastAPI service address | Confirm the FastAPI service is reachable at the configured URL with `curl http://localhost:8000/api/ledger/verify`; correct the dashboard env variable and re-run `npm run build`. |
| `searchAcrossLineage` returns an empty result for a urn known to have lineage | The DataHub showcase datapack seed script did not complete, or the urn was mistyped | Re-run `python scripts/seed_showcase_datapack.py` and check its exit code is 0; confirm the exact urn with `curl` against DataHub's own `/entities?action=search` endpoint before assuming GraphOath is at fault. |
| `Hash chain broken` result from `/api/ledger/verify` on a fresh install with zero real activity | A prior partial migration or manual database edit inserted a receipt row outside the application's write path | On a development database, this is safe to resolve by dropping and recreating the `receipts` table via `python -m graphoath.db.migrate --reset` (destructive, local only). On a production database, do not run `--reset`; escalate per the incident process in `docs/security.md`, since a genuine break outside development is a security event, not a bug. |

