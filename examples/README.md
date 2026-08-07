# Examples

This folder holds real, generated output from GraphOath — not hand-written
samples — per the hackathon's recommendation to include sample outputs judges
can review without running the project themselves.

Once Deposition is running end-to-end against the DataHub showcase-ecommerce
datapack, replace this file by adding:

- `receipt-schema-break.json` — a full receipt generated from a real schema-break
  run, matching the shape documented in `docs/api-reference.md` under
  `GET /receipts/{receipt_id}`.
- A second receipt from a different scenario, to show the citation gate
  handling more than one case.
- `screenshots/datahub-incident.png` — the resulting native DataHub Incident.
- `screenshots/slack-notification.png` — the Slack message produced by the run.

Do not hand-write these — generate them from an actual run and drop the real
output here, so what a judge sees here matches what the demo video shows.
