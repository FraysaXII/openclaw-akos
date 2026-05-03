# I54 / P0 — Bootstrap

**Date:** 2026-05-03
**Phase:** P0 (Governance scaffold)

## Deliverables

- `docs/wip/planning/54-surface-test-hardening/`:
  - `master-roadmap.md` — 7 phases (P0-P6); 4 decisions D-IH-54-A..D; gate G-54-1; risks R-54-1..4.
  - `decision-log.md` — 4 decisions seeded with operator-ratified defaults (Critical-only severity bar; pre_commit warn + release_gate gate; surface scope; defer-policy).
  - `evidence-matrix.md` — E1-E9 anchored to existing tests, scripts, I49 critique line 53, dossier sections.
  - `risk-register.md` — R-54-1..4 + empty deferred backlog table.
  - `asset-classification.md` — code/tests/config/deps/reports breakdown; canonical layer empty (initiative is purely test-tooling + CI wiring + optional HTML fixes).
  - `reports/.gitkeep`.
- Planning README row (I54; Active).

## Cross-link

I54 closes the I49 impeccable-critique follow-up (line 53 of [`49-madeira-management-rollup/reports/impeccable-critique-madeira-control-2026-05-03.md`](../../49-madeira-management-rollup/reports/impeccable-critique-madeira-control-2026-05-03.md)): *"Operator may wire a real Playwright + axe-core suite as part of `tests/test_madeira_control_a11y.py` once Initiative 49 closes."*

## Verification

- `py scripts/check-drift.py` PASS (no drift; pure docs change).
- `py scripts/validate_hlk.py` PASS.

## Forward look

- P1 pins `axe-playwright-python` in new `requirements-dev.txt` and adds `--axe` flag to `scripts/browser-smoke.py`.
- P2 authors DOM-level scenarios in `tests/playwright/`.
- P3 runs the audit (or stub-mode if axe not installed).
