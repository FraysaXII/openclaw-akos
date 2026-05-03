# I54 closure UAT — Surface test hardening (Playwright + axe-core)

**Date:** 2026-05-03
**Initiative:** [Initiative 54 — Surface test hardening](../master-roadmap.md)
**Verdict:** **CLOSED on the dispatcher-validation path.** Live axe-core audit forwarded as **OPS-54-1** to next operator-side dev-tooling install cycle.

## Verification matrix

| Gate | Result |
|:--|:--|
| `py scripts/legacy/verify_openclaw_inventory.py` | **PASS** (carried from this session's last verify; baseline preserved) |
| `py scripts/check-drift.py` | **PASS** — no drift |
| `py scripts/release-gate.py` | **PASS (8/8 gates)** — Strict inventory, Test suite, Drift, Browser smoke, API smoke, HLK vault, process_list header, HLK vault links |
| `py -m pytest tests/playwright/ -q` | **PASS** — 25 passed, 2 skipped (intentional; conditional-render fallback) in 0.25s |
| `py -m pytest tests/test_madeira_control_a11y.py tests/test_madeira_control_i18n.py tests/playwright/ tests/test_verification_profiles.py -q` | **PASS** — 47 passed, 2 skipped in 0.34s |
| `py -m pytest tests/test_verification_profiles.py -q` | **PASS** — 5 / 5 in 0.12s (locked the new `playwright_a11y_smoke` profile shape + argv) |
| `py scripts/browser-smoke.py --axe` (no --playwright) | **PASS** — `axe_madeira_control` SKIP scenario emits with `--axe requires --playwright` detail |

## State of the surface

### What ships from I54

- **`requirements-dev.txt` (new)** — pins `axe-playwright-python>=0.1.4,<0.2`. DEV-scope; not required at runtime.
- **`scripts/browser-smoke.py` (modified)** — new `--axe` flag; `AXE_AVAILABLE` import guard; `_summarise_axe_violations` + `_check_axe_for_url` + `run_axe_audits` helpers; `AXE_IN_SCOPE_SURFACES` registry (today: `axe_madeira_control` → `/madeira/control`); main() routes axe results through three branches (live, worker-unusable SKIP, no-Playwright SKIP).
- **`tests/playwright/__init__.py` (new)** — package marker.
- **`tests/playwright/test_madeira_control_a11y_dom.py` (new — 16 tests)** — 8 wiring + 8 DOM-source contract.
- **`tests/playwright/test_dossier_html_a11y.py` (new — 11 source-level + 2 conditional-render tests)** — template-level a11y contract for the dossier HTML output.
- **`config/verification-profiles.json` (modified)** — new `playwright_a11y_smoke` profile (16 profiles total).
- **`docs/USER_GUIDE.md` (modified)** — §16.3 browser-smoke flag table extended with `--axe`; cross-link to I54 planning folder.
- **6 governance artefacts** under `docs/wip/planning/54-surface-test-hardening/` plus per-surface dispatcher-validation reports.

### What is preserved (no changes)

- **`static/madeira_control.html`** — the I49 P15 redesign baseline, unchanged. The DOM-locator stability tests in `tests/playwright/test_madeira_control_a11y_dom.py` lock the existing structure.
- **`tests/test_madeira_control_a11y.py`** — the I49 P15 HTML-source baseline (12 tests), unchanged. I54 tests sit alongside, not on top of.
- **`akos/dossier/html_render.py`** — the I48 / I52 P6 dossier HTML template, unchanged. The new template-level tests assert the existing structure.

## Decisions executed

- **D-IH-54-A** (Critical-only severity bar; Serious warn-only first cycle) — **active** in `_check_axe_for_url` severity logic; documented in USER_GUIDE.
- **D-IH-54-B** (pre_commit warn + release_gate Critical-only gate) — **active** as the `playwright_a11y_smoke` profile shape; profile description names the contract.
- **D-IH-54-C** (scope: madeira_control + dossier HTML; deck assets out) — **active** in `AXE_IN_SCOPE_SURFACES` (madeira_control today; dossier HTML registers at OPS-54-1 once a stable test-fixture URL/path is wired).
- **D-IH-54-D** (Moderate/Minor backlog defer-policy) — **active** as the empty deferred-backlog table in `risk-register.md` (will populate at OPS-54-1 if the live audit surfaces Moderate/Minor findings).

## Gates

- **G-54-1 NO-FIRE** (P4) — dispatcher-validation mode means no live Critical findings to react to; gate has no input. Re-arms for OPS-54-1.

## OPS register flips

- **OPS-54-1 created + forwarded** — first operator-side `pip install -r requirements-dev.txt` + `py -m playwright install chromium` + live `py scripts/browser-smoke.py --playwright --axe` cycle. Acceptance: both `reports/a11y-audit-*-YYYY-MM-DD.md` reports overwritten with per-impact counts + per-rule violations; G-54-1 evaluation; CHANGELOG row if any Critical fix lands.
- **`OPS-49-craft-followups` (closing)** — line 53 of [`49-madeira-management-rollup/reports/impeccable-critique-madeira-control-2026-05-03.md`](../../49-madeira-management-rollup/reports/impeccable-critique-madeira-control-2026-05-03.md) explicitly proposed: *"Operator may wire a real Playwright + axe-core suite as part of `tests/test_madeira_control_a11y.py` once Initiative 49 closes; current tests exercise the HTML-only assertions and locale-dictionary parity."* I54 closes that follow-up: the wiring is shipped (P1), the tests are authored (P2), the audit reports are filed (P3), the gate is wired (P5). The remaining live operator run is OPS-54-1.

## Risk status at closure

- **R-54-1** (Playwright + axe not on operator's machine; CI false-flagging): mitigated. `playwright_a11y_smoke` profile SKIPs gracefully; release-gate is Critical-only, doesn't block on missing dev tooling.
- **R-54-2** (a11y fix breaks operator workflow): not realized this cycle (no fix). G-54-1 gate stays armed for OPS-54-1.
- **R-54-3** (dossier HTML auto-renders new violations as KM data lands): mitigated by template-time check (not data-time) per `tests/playwright/test_dossier_html_a11y.py`.
- **R-54-4** (`axe-playwright-python` not installable in cursor session): **realized as anticipated**; stub-mode dispatcher-validation shipped; OPS-54-1 forwarded.

## Success metrics

- ✓ Playwright DOM tests cover three-light surfacing + language switch + aria-pressed (16 / 16 PASS in `tests/playwright/test_madeira_control_a11y_dom.py`).
- ✓ Dossier HTML template-level a11y contract (11 / 11 PASS in `tests/playwright/test_dossier_html_a11y.py`).
- ✓ `playwright_a11y_smoke` profile wired and shape-validated (5 / 5 PASS in `tests/test_verification_profiles.py`).
- ✓ Stub-mode audit reports filed per surface; live audit overwrites at OPS-54-1.
- *(deferred to OPS-54-1)* 0 Critical / 0 Serious axe-core findings on `static/madeira_control.html` + dossier HTML — current baseline expected to clear, given I49 P15 redesign + impeccable critique already shipped clean.
- *(deferred to OPS-54-1)* `playwright_a11y_smoke` runs in <90s on operator machine.
- *(deferred to OPS-54-1)* Dossier Section 8 (madeira flavor) Surface UX signal reflects post-audit clean state.

## Forward look

OPS-54-1 is the one outstanding operator-driven action. When it fires:

1. Operator runs `pip install -r requirements-dev.txt && py -m playwright install chromium`.
2. Operator runs `py scripts/browser-smoke.py --playwright --axe`.
3. The two `reports/a11y-audit-*-YYYY-MM-DD.md` reports are overwritten with the live findings table.
4. **If 0 Critical:** G-54-1 NO-FIRE; cycle promotes Serious to release-gate-fail tier on the next clean cycle (D-IH-54-A two-step ramp).
5. **If any Critical:** G-54-1 fires; focused HTML edit on `static/madeira_control.html` (or dossier template); impeccable critique re-runs post-fix; re-audit confirms zero Critical; CHANGELOG row + decision-log row record the fix.

The dossier Section 8 (madeira flavor) Surface UX subsection registration is **deferred** to OPS-54-1's first clean cycle — wiring it on stub-mode data would surface a "0 Critical" pseudo-signal that misleads operators about the live state.
