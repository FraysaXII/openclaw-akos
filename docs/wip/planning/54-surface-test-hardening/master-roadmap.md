---
language: en
status: closed
initiative: 54-surface-test-hardening
initiative_id: INIT-OPENCLAW_AKOS-54
report_kind: master-roadmap
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-04
closed_at: 2026-05-04
closure_decision_id: D-IH-54-CLOSURE
---
# Initiative 54 — Surface test hardening (Playwright + axe-core)

**Folder:** `docs/wip/planning/54-surface-test-hardening/`

**Status:** **Closed (2026-05-03 dispatcher-validation; OPS-54-1 closed 2026-05-04 live audit).** P0-P5 all executed; P6 closure UAT PASS (release-gate 8/8). **OPS-54-1 live audit** ran 2026-05-04 on Python 3.14.2 + Playwright 1.58.0 + axe-playwright-python 0.1.7 + msedge against `/madeira/control` — **0 Critical / 2 Serious / 0 Moderate / 0 Minor**; PASS per D-IH-54-A (Serious warn-only first cycle). Two findings recorded as residual fixes (`OPS-54-1.a` color-contrast, `OPS-54-1.b` keyboard scrollable region). See [reports/uat-i54-live-a11y-audit-20260504.md](reports/uat-i54-live-a11y-audit-20260504.md).

**Authoritative Cursor plan:** `~/.cursor/plans/i50–i56_madeira_kb_completion_87cc767e.plan.md` §"Initiative 54".

**Origin:** I49 P14/P15 redesign of [`static/madeira_control.html`](../../../static/madeira_control.html) shipped a11y + i18n; the [Impeccable craft critique](../49-madeira-management-rollup/reports/impeccable-critique-madeira-control-2026-05-03.md) declared "ship" with documented follow-up: *"Operator may wire a real Playwright + axe-core suite as part of `tests/test_madeira_control_a11y.py` once Initiative 49 closes; current tests exercise the HTML-only assertions and locale-dictionary parity."* (line 53). I54 closes that follow-up.

**Depends:** I50 closure ✓; can parallelize with I51-I53 once branch discipline holds (no shared file edits) — I53 closed cleanly 2026-05-03.

## Goal

Promote MADEIRA control plane, AKOS dashboards, and dossier HTML surfaces from HTTP-smoke + ad-hoc to **DOM-tested + axe-core a11y-audited**; wire into existing `browser-smoke.py --playwright` path; capture WCAG-mapped findings; close out I49 impeccable follow-ups; bidirectional contract: dossier `Section08OperationalHealth` Surface UX subsection consumes a11y signal.

## Asset classification

| Class | Paths | Rule |
|:------|:------|:-----|
| **Modified script** | [`scripts/browser-smoke.py`](../../../scripts/browser-smoke.py) | Add axe-core wiring to Playwright Phase 2/3; opt-in via `--axe` flag |
| **Modified HTML (a11y fixes only if Critical/Serious found)** | [`static/madeira_control.html`](../../../static/madeira_control.html) + dossier HTML template if surfaced | Fix Critical/Serious findings only |
| **New dependency** | new [`requirements-dev.txt`](../../../requirements-dev.txt) — pin `axe-playwright-python` minor version | DEV scope only; not required for runtime |
| **New tests** | `tests/playwright/test_madeira_control_a11y_dom.py`, `tests/playwright/test_dossier_html_a11y.py` | Extends existing `tests/test_madeira_control_a11y.py` (HTML-source heuristic) with real DOM/axe |
| **Modified profile** | [`config/verification-profiles.json`](../../../config/verification-profiles.json) | New `playwright_a11y_smoke` step (when Playwright + axe installed; warn-only on Critical for pre-commit; gate at `release_gate` for Critical-only) |
| **New reports** | `reports/a11y-audit-<surface>-YYYY-MM-DD.md` per surface, classified Critical/Serious/Moderate/Minor with WCAG IDs | |

## Phase plan (~3-5 op-days)

| Phase | Focus |
|:-:|:----|
| **P0** | Bootstrap I54 folder + 6 artefacts; README row; cross-link I49 impeccable critique. |
| **P1** | **Wire axe-core into Playwright:** Pin `axe-playwright-python` in `requirements-dev.txt`; document in `scripts/browser-smoke.py` Phase 2/3; smoke test on `static/madeira_control.html`. |
| **P2** | **Author DOM-level scenarios:** Three-light status surfacing, language switcher (en/es/fr), `aria-pressed` toggles, focus-visible outlines, `role=status` announcements; assert from DOM, not HTML source. |
| **P3** | **Run a11y audit:** Execute axe-core on each in-scope surface; emit `reports/a11y-audit-<surface>-YYYY-MM-DD.md` per surface; classify violations Critical/Serious/Moderate/Minor with WCAG 2.1/2.2 IDs. **Stub-mode** when axe-playwright-python not installed: emit zero-finding "dispatcher-validation" report mirroring I52 P3 / I53 P3 stub-mode pattern. |
| **P4** | **Fix Critical/Serious findings (G-54-1):** Edit HTML; defer Moderate/Minor with backlog row in `risk-register.md`; re-run audit; verify clean. |
| **P5** | **CI integration:** Add `playwright_a11y_smoke` step to `pre_commit` (warn-only when not installed; warn on any Critical when installed); `release_gate` gates on Critical=0 only; document operator install path in `USER_GUIDE` + `SOP`. |
| **P6** | **Closure:** pytest sweep, dossier `--filter madeira` Section 8 Surface UX subsection re-emit, CHANGELOG, README row, WIP_DASHBOARD; flip I49 follow-up `OPS-49-craft-followups` complete. |

## Verification matrix

| Check | Cadence |
|:------|:--------|
| `py scripts/browser-smoke.py --playwright --axe` (new flag) | New `playwright_a11y_smoke` profile |
| `py -m pytest tests/playwright/ -v` | Every commit when Playwright installed |
| `py -m pytest tests/test_madeira_control_a11y.py tests/test_madeira_control_i18n.py -v` | Every commit (HTML-source baseline stays) |
| `release_gate` enforces Critical=0 | Per release |
| Dossier Surface UX signal reflects a11y audit (Section 8 madeira flavor) | P6 + ongoing |

## Operator approval gates

- **G-54-1** (P4) — Any breaking HTML structural change to fix Critical findings on shipped surfaces (e.g., aria-pressed toggle restructure that touches operator workflow). NO-FIRE expected this cycle on a clean redesign baseline.

## Decisions seeded

- **D-IH-54-A** — axe-core severity bar for CI fail: **Critical only** (default); Serious is warn-only at first run, escalates after one cycle of clean operation.
- **D-IH-54-B** — Test runner location: `playwright_a11y_smoke` step in `pre_commit` (warn-only) + `release_gate` (Critical-only gate).
- **D-IH-54-C** — HTML surfaces in scope: `static/madeira_control.html` + dossier HTML output; **NOT** the deck assets (those have their own brand-jargon-audit lint at I49 P12).
- **D-IH-54-D** — Defer-policy for Moderate/Minor findings: backlog row in `risk-register.md` with WCAG ID; revisit at WCAG 2.2 industry adoption signal.

## Risks

- **R-54-1** — Playwright + axe not available on operator's machine; CI false-flagging. Mitigation: warn-only at pre-commit when not installed; install runbook in `USER_GUIDE`.
- **R-54-2** — A11y fix breaks existing operator workflow (e.g., aria-pressed restructure). Mitigation: G-54-1 gate; impeccable critique re-run after each Critical fix.
- **R-54-3** — Dossier HTML template auto-renders new violations as KM data lands. Mitigation: dossier HTML template is canonical (small surface); template-time test (not data-time).
- **R-54-4** — `axe-playwright-python` not available at install time in this cursor session (no PyPI access). Mitigation: P3 ships in **stub mode** (zero-finding dispatcher-validation report) mirroring I52 P3 / I53 P3 pattern; OPS-54-1 forwarded to next operator-side install + run.

## Success metrics

- 0 Critical / 0 Serious axe-core findings on `static/madeira_control.html` + dossier HTML (or stub-mode dispatcher-validation report demonstrating wiring).
- Playwright DOM tests cover three-light surfacing + language switch + aria-pressed at minimum.
- `playwright_a11y_smoke` runs in <90s on operator machine (target).
- Dossier Section 8 (madeira flavor) Surface UX signal reflects post-audit clean state.

## What this is NOT

- A wholesale UI refresh; the I49 impeccable redesign stays.
- Replacement for the I49 Impeccable design audit (that human craft critique stays the source of truth for aesthetic choices).
- Coverage of off-repo product surfaces (boilerplate / KiRBe / hlk-erp; per [external repo contract](../../../EXTERNAL_REPO_CONTRACT.md)).
- A switch to a different a11y framework (axe-core is the de facto WCAG mapper).
