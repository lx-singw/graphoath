## What does this change?

<!-- One paragraph: what changed and why. -->

## Test coverage

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] End-to-end tests added/updated (only required for `src/dashboard/app/` or `src/graphoath/api/` changes)

## Citation-gate impact

<!--
Required only if this PR touches src/graphoath/custody/ or
src/graphoath/modules/*/gate.py.

Does this change alter what counts as sufficient evidence for a claim to pass
the validation gate? If yes, explain exactly what changed and why.
-->

## Checklist

- [ ] `ruff check` / `ruff format` and `mypy --strict` pass locally (Python changes)
- [ ] `npm run lint` and `tsc --noEmit` pass locally (dashboard changes)
- [ ] Docs under `docs/` updated if this changes architecture, API, or scope
