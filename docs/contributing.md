# GraphOath — Contributing

## 1. Code Quality Standards

### 1.1 Python (backend, `src/graphoath/`)

- **Linting:** `ruff` with the configuration in `pyproject.toml`, running the
  `E`, `F`, `I`, `UP`, and `B` rule sets (pyflakes errors, import sorting,
  pyupgrade, and bugbear). No `# noqa` suppression without an inline comment
  explaining why.
- **Formatting:** `ruff format` (Black-compatible), enforced pre-commit and in
  CI; unformatted code fails the `ci.yml` workflow.
- **Type checking:** `mypy --strict` on `src/graphoath/`. New code must be
  fully typed; `# type: ignore` requires an inline justification comment and
  is tracked as technical debt in the module's docstring.
- **Docstrings:** Every public function in `datahub/`, `custody/`, and
  `modules/*/` requires a docstring stating what DataHub calls it makes (if
  any) and what it returns, since these are the functions most load-bearing
  for the citation-gate guarantee described in `docs/architecture.md`.

### 1.2 TypeScript (dashboard, `src/dashboard/`)

- **Linting:** ESLint with `next/core-web-vitals` and `@typescript-eslint/recommended-requiring-type-checking`.
- **Formatting:** Prettier, run via `npm run format`, enforced in CI.
- **Type checking:** `strict: true` in `tsconfig.json`; no `any` without an
  inline comment explaining why a precise type was not feasible.

### 1.3 Testing Strategy

| Level | Scope | Tooling | Requirement to merge |
|---|---|---|---|
| Unit | Pure functions with no network calls — the citation gate, the hash-chain computation, evidence-array parsing | `pytest` (Python), `vitest` (TypeScript) | 100% of new logic branches covered; overall repository line coverage may not drop below the value on `main` at the time of the PR. |
| Integration | Full module pipeline (trigger → evidence → gate → action → Custody write) against a local DataHub instance seeded from `tests/fixtures/` | `pytest` with `docker compose -f docker-compose.test.yml` | Required for any change touching `modules/*/`, `datahub/`, or `custody/`. |
| End-to-end | Dashboard flows against the full local stack | Playwright | Required for any change touching `src/dashboard/app/` routes or `src/graphoath/api/`. |

All three levels run in `ci.yml` on every pull request. A PR cannot merge with
a red CI run regardless of reviewer approval.

## 2. Branching Strategy

GraphOath uses **trunk-based development** with short-lived feature branches,
not Gitflow — the module-isolated architecture in `docs/architecture.md` means
long-lived parallel branches per module create more merge risk than they
prevent.

- **`main`** is always deployable. Direct pushes to `main` are disabled at the
  repository level; every change lands via pull request.
- **Feature branches** are named `feature/<short-description>` or
  `fix/<short-description>` and branch from `main`. Branches older than 5 days
  should be rebased onto `main` before further work, to keep integration
  friction low.
- **Pull request template** (`.github/PULL_REQUEST_TEMPLATE.md`) requires:
  a one-paragraph description of the change, which of the three test levels
  above were added or updated, and — for any change touching `custody/` or
  `modules/*/gate.py` specifically — an explicit statement of whether the
  citation-gate behavior changed and why.
- **Review requirement:** one approving review minimum; two required for any
  change to `custody/ledger.py` or `security.md`-referenced auth code, given
  the outsized blast radius of a defect in either.
- **Semantic versioning:** releases are tagged `vMAJOR.MINOR.PATCH` on `main`.
  `MAJOR` increments only for a breaking change to the receipt schema or the
  public API described in `docs/api-reference.md`; `MINOR` for new modules or
  new endpoints; `PATCH` for fixes with no interface change. The receipt schema
  version is additionally embedded in every receipt payload as
  `schema_version`, independent of the repository's release tag, so that
  historical receipts remain interpretable even after the schema evolves.
