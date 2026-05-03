---
language: en
status: active
initiative: 54-surface-test-hardening
report_kind: asset-classification
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 54 — Asset classification

Per [`PRECEDENCE.md`](../../references/hlk/compliance/PRECEDENCE.md).

## Canonical (edit here first)

- *(none in I54; the initiative is purely test-tooling + CI wiring + optional HTML fixes if Critical findings surface)*

## Mirrored / derived

- *(none)*

## Reference-only (do not edit)

- [`docs/wip/planning/49-madeira-management-rollup/reports/impeccable-critique-madeira-control-2026-05-03.md`](../49-madeira-management-rollup/reports/impeccable-critique-madeira-control-2026-05-03.md) — impeccable craft critique; I54 closes the line-53 follow-up.

## Code

- [`scripts/browser-smoke.py`](../../../scripts/browser-smoke.py) — modified at P1 to add `--axe` flag.
- [`static/madeira_control.html`](../../../static/madeira_control.html) — modified ONLY if Critical/Serious axe findings surface at P3 (G-54-1 governance gate).

## Tests

- [`tests/test_madeira_control_a11y.py`](../../../tests/test_madeira_control_a11y.py) — HTML-source baseline; **stays untouched** at I54 (we add DOM tests on top, not replace).
- [`tests/test_madeira_control_i18n.py`](../../../tests/test_madeira_control_i18n.py) — i18n locale-dictionary parity; stays untouched.
- New: `tests/playwright/test_madeira_control_a11y_dom.py` — DOM-level + axe-core for madeira_control.
- New: `tests/playwright/test_dossier_html_a11y.py` — DOM-level + axe-core for dossier HTML output.

## Config

- [`config/verification-profiles.json`](../../../config/verification-profiles.json) — modified at P5 to add `playwright_a11y_smoke` step.

## Dependencies

- New: [`requirements-dev.txt`](../../../requirements-dev.txt) — DEV-scope dependencies; pin `axe-playwright-python` minor version. Future cleanup may also relocate `playwright>=1.40` from `requirements.txt` here.

## Reports

- New: `reports/p<N>-*-2026-05-03.md` per phase.
- New: `reports/a11y-audit-<surface>-2026-05-03.md` per in-scope surface (P3 output).
- New: `reports/uat-i54-surface-test-hardening-2026-05-03.md` (P6 closure).
