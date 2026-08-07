# GraphOath — Repository Directory Structure

## Visual Repository Tree

```
graphoath/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── deploy-staging.yml
│       └── ledger-integrity-check.yml
├── config/
│   ├── default.yaml
│   ├── production.yaml
│   └── modules/
│       └── deposition.yaml
├── deployments/
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   └── terraform/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── docs/
│   ├── vision.md
│   ├── prd.md
│   ├── project-scope.md
│   ├── directory-structure.md
│   ├── architecture.md
│   ├── api-reference.md
│   ├── installation.md
│   ├── security.md
│   ├── contributing.md
│   ├── hackathon-alignment.md
│   ├── framework-integrations.md
│   ├── mcp-context-kit-guide.md
│   ├── judge-walkthrough.md
│   ├── benchmarks-and-performance.md
│   ├── edge-cases-and-resilience.md
│   └── demo-video-script.md
├── examples/
│   ├── langchain_agent_example.py
│   ├── mock_mcp_citation_demo.py
│   ├── receipt-schema-break.json
│   ├── receipt-cost-audit.json
│   └── screenshots/
│       ├── datahub-incident.png
│       └── slack-notification.png
├── scripts/
│   ├── seed_showcase_datapack.py
│   ├── verify_ledger_integrity.py
│   └── generate_receipt_export.py
├── src/
│   ├── graphoath/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── datahub/
│   │   │   ├── __init__.py
│   │   │   ├── client.py
│   │   │   ├── lineage.py
│   │   │   ├── ownership.py
│   │   │   ├── usage.py
│   │   │   └── incidents.py
│   │   ├── modules/
│   │   │   ├── __init__.py
│   │   │   └── deposition/
│   │   │       ├── __init__.py
│   │   │       ├── trigger.py
│   │   │       ├── evidence.py
│   │   │       ├── gate.py
│   │   │       └── action.py
│   │   ├── custody/
│   │   │   ├── __init__.py
│   │   │   ├── receipt.py
│   │   │   ├── ledger.py
│   │   │   └── models.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes_receipts.py
│   │   │   ├── routes_incidents.py
│   │   │   ├── routes_auth.py
│   │   │   └── schemas.py
│   │   └── db/
│   │       ├── __init__.py
│   │       ├── session.py
│   │       └── migrations/
│   │           └── 0001_initial.sql
│   └── dashboard/
│       ├── package.json
│       ├── tsconfig.json
│       ├── next.config.js
│       ├── app/
│       │   ├── layout.tsx
│       │   ├── page.tsx
│       │   ├── receipts/
│       │   │   └── [receiptId]/
│       │   │       └── page.tsx
│       │   └── ledger/
│       │       └── page.tsx
│       └── components/
│           ├── ReceiptCard.tsx
│           ├── EvidenceList.tsx
│           └── LedgerTable.tsx
├── tests/
│   ├── unit/
│   │   ├── test_gate.py
│   │   ├── test_ledger.py
│   │   └── test_evidence.py
│   ├── integration/
│   │   └── test_deposition_end_to_end.py
│   └── fixtures/
│       └── showcase_datapack_sample.json
├── .env.example
├── .gitignore
├── docker-compose.yml
├── pyproject.toml
├── requirements.txt
├── README.md
└── LICENSE
```

## Path Explanations

- **`.github/workflows/`** — CI/CD pipeline definitions. `ci.yml` runs lint,
  unit, and integration tests on every pull request. `ledger-integrity-check.yml`
  runs the hash-chain verification script nightly against the production ledger
  and alerts on failure (see US-07 in `docs/prd.md`).
- **`config/`** — Environment-layered configuration. `default.yaml` holds values
  safe to commit (hop depth, timeouts); `production.yaml` is loaded on top of it
  and references environment-variable placeholders for secrets, never literal
  values. `config/modules/deposition.yaml` holds module-specific tuning
  (e.g., max lineage hop depth, evidence-gather timeout).
- **`deployments/`** — Infrastructure-as-code and container orchestration.
  `docker-compose.yml` is the self-hosted MVP deployment path; the `terraform/`
  subdirectory defines the managed-cloud option referenced in
  `docs/project-scope.md`.
- **`docs/`** — This documentation suite. Kept in-repo and versioned alongside
  code so architectural decisions and the code implementing them never drift
  apart.
- **`examples/`** — Real, generated (not hand-written) sample output, required
  for the hackathon submission's recommended `examples/` folder and useful
  afterward as fixtures for onboarding and support.
- **`scripts/`** — Standalone operational scripts invoked directly, not through
  the API. `seed_showcase_datapack.py` loads the DataHub showcase-ecommerce
  datapack for local development; `verify_ledger_integrity.py` is the script
  the CI workflow and the nightly check both call.
- **`src/graphoath/`** — The Python runtime package.
  - `datahub/` — All DataHub integration code, isolated behind a single
    `client.py` so that MCP Server, Agent Context Kit, or direct GraphQL calls
    can be swapped without touching module logic.
  - `modules/deposition/` — Deposition's four-stage pipeline as four files:
    `trigger.py` (event ingestion), `evidence.py` (lineage/ownership/usage
    gathering), `gate.py` (the citation-check validation gate), `action.py`
    (raising the native DataHub Incident).
  - `custody/` — The receipt schema, the hash-chain ledger writer, and the
    Postgres models backing it. Deliberately independent of `modules/` so that
    every future module (Undertow, Prune, and so on) writes through the same
    ledger code path.
  - `api/` — FastAPI route definitions and Pydantic request/response schemas,
    documented fully in `docs/api-reference.md`.
  - `db/` — SQLAlchemy session management and raw SQL migrations. Migrations
    are plain numbered `.sql` files rather than an ORM migration framework, to
    keep the hash-chain table's schema auditable at a glance.
- **`src/dashboard/`** — The Next.js operator dashboard (App Router,
  TypeScript). `app/receipts/[receiptId]/` renders a single receipt's evidence
  chain; `app/ledger/` renders the flat ledger table used in the demo and in
  day-to-day operator review.
- **`tests/`** — `unit/` tests pure logic (the gate function, the hash-chain
  math) with no network calls. `integration/` runs the full Deposition pipeline
  against a local DataHub instance seeded from `fixtures/`.
- **`.env.example`** — Documents every environment variable the runtime expects
  (DataHub connection details, Postgres URL, Slack webhook) without real
  values. Copied to `.env` during local setup per `docs/installation.md`.
- **`docker-compose.yml`** (root) — The single command referenced in the
  hackathon "definition of done": brings up Postgres, the FastAPI runtime, and
  the Next.js dashboard together for local development.
- **`pyproject.toml`** — Python project metadata, dependency declarations, and
  tool configuration (ruff, mypy, pytest) in one file, per the standards in
  `docs/contributing.md`.
