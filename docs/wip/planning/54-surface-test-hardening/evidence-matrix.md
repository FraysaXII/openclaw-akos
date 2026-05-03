---
language: en
status: active
initiative: 54-surface-test-hardening
report_kind: evidence-matrix
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 54 — Evidence matrix

| ID | Observation | Source | Impact |
|:---|:------------|:-------|:-------|
| E1 | I49 P14/P15 redesigned `static/madeira_control.html` shipped with HTML-source-level a11y assertions in `tests/test_madeira_control_a11y.py` (12 tests) covering: doctype/lang, main landmark, color-scheme meta, role=status + aria-live, role=alert error path, focus-visible outline, prefers-reduced-motion respect, no external CDN, aria-pressed on mode/locale buttons, no blocking alert(), brand-voice lint clean | [`tests/test_madeira_control_a11y.py`](../../../tests/test_madeira_control_a11y.py) | I54 layers DOM-level + axe-core on top of this HTML-source baseline (HTML-source baseline stays) |
| E2 | I49 impeccable critique declared "ship" with explicit follow-up: *"Operator may wire a real Playwright + axe-core suite as part of `tests/test_madeira_control_a11y.py` once Initiative 49 closes"* | [`49-madeira-management-rollup/reports/impeccable-critique-madeira-control-2026-05-03.md`](../49-madeira-management-rollup/reports/impeccable-critique-madeira-control-2026-05-03.md) line 53 | I54 P6 closes this follow-up (`OPS-49-craft-followups` flips to complete) |
| E3 | `scripts/browser-smoke.py` already supports `--playwright` for DOM-based tests (Phase 1 + 2 + 3 scenarios; Windows multi-engine fallback chromium/msedge/firefox); axe-core wiring is the missing piece | [`scripts/browser-smoke.py`](../../../scripts/browser-smoke.py) lines 669-686, 731-738, 751-866 | I54 P1 adds `--axe` flag; reuses the existing Playwright path |
| E4 | No `requirements-dev.txt` exists today; `requirements.txt` mixes runtime + optional deps (e.g., `playwright>=1.40` is listed for browser-smoke) | `requirements.txt` lines 16-17 | I54 P1 introduces `requirements-dev.txt` for DEV-scope tooling (`axe-playwright-python`); future cleanup moves Playwright there |
| E5 | `tests/playwright/` directory does not exist today | repo state 2026-05-03 | I54 P2 creates it; tests live there to keep Playwright-dependent tests cleanly separated from the unit-level baseline |
| E6 | I49 P15 redesign + impeccable critique already exhibit zero documented Critical/Serious axe-core violations on the HTML-source baseline (no contrast <4.5:1, no missing labels, no keyboard trap, no aria-* misuse called out by the critique) | I49 P15 + impeccable critique | I54 P3 expected outcome on a clean redesign baseline: zero or near-zero findings; the gate primarily protects against future regressions |
| E7 | `axe-playwright-python` is the de-facto Python wrapper for axe-core in Playwright contexts; license MIT; pinned minor version available | upstream PyPI | I54 P1 picks this dependency |
| E8 | I52 P5/P6 introduced the dossier `Section08OperationalHealth` Surface UX subsection (`madeira_endpoint_cost`); the same section is the right home for the a11y signal under a new `madeira_a11y` subsection at I54 P6 | [`akos/dossier/sections.py`](../../../akos/dossier/sections.py) | I54 P6 wires the dossier surface (consistent with I52's "operator one-liner" pattern) |
| E9 | The "stub-mode" pattern is well-established: I52 P3 calibration burn (100% / 100% / 100% in offline-fallback), I52 P5 endpoint cost probe (`--stub` fixture), I53 P3 NO-FIRE governance event. I54 P3 follows the same pattern when `axe-playwright-python` is not installed in this cursor session (no PyPI access for cursor agent installs) | I52 P3 / P5 reports + I53 P3 report | I54 P3 ships in stub-mode with OPS-54-1 forwarded to next operator-side install |
