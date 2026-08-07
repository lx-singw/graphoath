# GraphOath — Security

## 1. Threat Modeling

### Threat 1 — A compromised or malicious upstream agent submits a claim designed to pass the citation gate with misleading evidence

**Attack surface:** The evidence-gathering step (`evidence.py`) queries DataHub
in good faith; an attacker who can influence DataHub metadata itself (e.g., by
compromising an ingestion source or forging ownership records) could cause the
gate to validate a claim that is technically "cited" but substantively false.

**Mitigation:** GraphOath does not treat citation as equivalent to truth — it
treats citation as the minimum bar for a claim to be actionable at all. Every
evidence entry stores the exact query and result at the time it was gathered,
so a later human or automated audit can re-run the same query against DataHub
and detect drift between what was cited and what is true now. High-impact
action types (destructive or irreversible changes) are additionally routed
through the human approval gate (US-06) regardless of how clean the citation
looks, so a single falsified metadata record cannot alone trigger an
irreversible action.

### Threat 2 — Ledger tampering to hide or alter a past action

**Attack surface:** Direct database access (e.g., a compromised credential with
write access to the `receipts` Postgres table) could be used to alter a past
receipt's content to obscure what an agent actually did.

**Mitigation:** The hash-chain design means altering any receipt changes its
hash, which breaks the chain for every subsequent receipt. `GET
/api/ledger/verify` detects this by recomputing the chain from genesis and
comparing computed hashes against stored ones; the nightly CI job
(`ledger-integrity-check.yml`) runs this automatically and pages
`governance_admin`-role users on failure. Database credentials with write
access to the `receipts` table are restricted to the application's own service
account; no human operator credential has direct write access to that table in
production, enforced via Postgres role grants documented in
`deployments/terraform/main.tf`.

### Threat 3 — Credential exfiltration of the DataHub service-account token

**Attack surface:** The `DATAHUB_TOKEN` environment variable grants read and
metadata-write access to the customer's DataHub instance; if exfiltrated, an
attacker could read the full lineage graph or forge metadata directly, bypassing
GraphOath entirely.

**Mitigation:** The token is never logged, never included in receipt payloads,
and is stored only as an encrypted secret (see Section 2.3). It is scoped to
the minimum permission set GraphOath's own calls require — metadata read,
lineage read, and write access limited to the Incident entity type and
GraphOath's own custom aspect namespace (`graphoathReceipt`) — rather than a
broad admin token, so that even a fully exfiltrated token cannot be used to
modify arbitrary DataHub entities.

## 2. Auth Mechanisms

### 2.1 Dashboard user authentication

OAuth 2.0 authorization-code flow against the organization's configured
identity provider (or GraphOath's built-in email/password store for
organizations without SSO). On successful authentication, the API issues:

- An **access token** — a JWT signed with `HS256` using `JWT_SECRET`,
  containing `sub` (user ID), `role`, and `exp` claims, valid for 12 hours.
- A **refresh token** — a 256-bit random value, stored server-side hashed with
  SHA-256, valid for 30 days from last use, single-use (rotated on every
  refresh).

### 2.2 Token lifecycle

1. Login issues both tokens (see `POST /auth/login` in `docs/api-reference.md`).
2. The dashboard stores the access token in memory only (not `localStorage`),
   and the refresh token in an `HttpOnly`, `Secure`, `SameSite=Strict` cookie.
3. On access-token expiry, the dashboard calls `POST /auth/refresh`; the old
   refresh token is invalidated and a new one issued (rotation prevents replay
   of a stolen refresh token beyond its single use).
4. Logout invalidates the refresh token server-side immediately; the access
   token remains technically valid until its natural expiry (max 12-hour
   exposure window), which is an accepted tradeoff documented here rather than
   left implicit.

### 2.3 Encryption at rest for tokens and secrets

- `DATAHUB_TOKEN`, `SLACK_WEBHOOK_URL`, and `JWT_SECRET` are stored in the
  deployment's secret manager (e.g., AWS Secrets Manager or HashiCorp Vault in
  production; Docker secrets in local development), never in plaintext
  environment files committed to version control.
- Refresh token hashes and user password hashes (Argon2id, minimum 19 MiB
  memory cost, 2 iterations, per current OWASP recommendation) are stored in
  Postgres with the `pgcrypto` extension enabled for column-level encryption of
  any field containing credential material.
- Postgres itself is deployed with encryption at rest enabled at the volume
  level (AES-256) regardless of column-level encryption, as defense in depth.

### 2.4 CORS and CSP configuration

```
Access-Control-Allow-Origin: https://dashboard.graphoath.example.com
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Authorization, Content-Type
Access-Control-Allow-Credentials: true

Content-Security-Policy: default-src 'self'; connect-src 'self' https://api.graphoath.example.com; script-src 'self'; style-src 'self' 'unsafe-inline'; frame-ancestors 'none';
```

No wildcard origins are permitted in any environment above local development;
`docker-compose.yml` sets a permissive local-only CORS policy explicitly marked
as unsafe for production use.

## 3. Compliance & Production Hardening Checklist

- [ ] TLS 1.3 minimum enforced at the reverse proxy; TLS 1.2 accepted only as a
      fallback for legacy clients if the organization requires it, disabled by
      default.
- [ ] `DATAHUB_TOKEN` scoped to least privilege as described in Threat 3 above,
      rotated on a maximum 90-day schedule.
- [ ] Postgres accessible only from the application's private network segment;
      no public internet exposure of the database port under any circumstance.
- [ ] Nightly `ledger-integrity-check.yml` alerting routed to an on-call channel
      distinct from general engineering alerts, since a ledger break is a
      governance incident, not an operational one.
- [ ] Rate limiting enforced at the reverse proxy: 100 requests/minute per
      token for read endpoints, 20 requests/minute per token for write and
      approval endpoints.
- [ ] Audit logging of every `governance_admin`-role action (exports, approval
      overrides, role changes) retained separately from the Custody ledger
      itself, per the retention policy in `docs/prd.md`.
- [ ] Dependency vulnerability scanning (`pip-audit` and `npm audit`) run in CI
      on every pull request, blocking merge on any `high` or `critical`
      finding without an explicit, reviewed suppression.
