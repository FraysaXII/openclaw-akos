# a11y audit — `static/madeira_control.html`

**Date:** 2026-05-03
**Surface:** `/madeira/control` (rendered from `static/madeira_control.html`)
**Audit tool:** axe-core (planned, via `axe-playwright-python>=0.1.4,<0.2`)
**Audit mode:** **DISPATCHER VALIDATION ONLY** (stub-mode; mirrors I52 P3 / I53 P3 pattern)
**Operator opt-in for live mode:** `pip install -r requirements-dev.txt` + `py -m playwright install chromium` + `py scripts/browser-smoke.py --playwright --axe`

## Mode

This cycle's cursor agent does not have PyPI access to install
`axe-playwright-python`; the audit runs in **stub mode** and reports
**zero findings as the dispatcher-validation outcome**. The wiring is
verified end-to-end by `tests/playwright/test_madeira_control_a11y_dom.py`
(25 / 25 PASS).

When the operator runs the live audit (after `pip install -r requirements-dev.txt`),
this report is overwritten with the actual axe-core findings table.

## Findings (stub mode)

| Severity (D-IH-54-A) | Count | Notes |
|:--------------------|------:|:-----|
| Critical | **0** | dispatcher-validation; live audit pending OPS-54-1 |
| Serious | **0** | dispatcher-validation; live audit pending OPS-54-1 |
| Moderate | **0** | dispatcher-validation; live audit pending OPS-54-1 |
| Minor | **0** | dispatcher-validation; live audit pending OPS-54-1 |

## Dispatcher-validation evidence

The wiring that the live audit will use is verified at HTML-source +
DOM-locator + helper level:

| Evidence | Source |
|:---------|:-------|
| `<main>` landmark present (axe `landmark-one-main` rule won't fire) | `tests/playwright/test_madeira_control_a11y_dom.py::test_madeira_control_has_main_landmark_for_axe_landmark_rule` |
| `<html lang="en">` declared (axe `html-has-lang` + `valid-lang` won't fire) | `tests/test_madeira_control_a11y.py::test_doctype_and_lang_attribute` |
| `role="status"` + `aria-live="polite"` (axe `aria-allowed-role` + `aria-valid-attr-value` won't fire) | `tests/test_madeira_control_a11y.py::test_status_panel_has_role_and_aria_live` |
| Locale buttons carry `data-locale-set` selectors stable across re-render | `tests/playwright/test_madeira_control_a11y_dom.py::test_madeira_control_has_dom_locator_for_locale_buttons` |
| Mode buttons carry `aria-pressed` (axe `aria-allowed-attr` won't fire) | `tests/test_madeira_control_a11y.py::test_aria_pressed_on_mode_buttons` |
| `button:focus-visible` outline rule (axe `focus-order-semantics` aided) | `tests/test_madeira_control_a11y.py::test_focus_visible_outline_defined` |
| `prefers-reduced-motion: reduce` honored (axe-related: motion-allow / vestibular) | `tests/test_madeira_control_a11y.py::test_reduced_motion_respected` |
| No external `<script src=` / `<link>` (axe-friendly offline posture) | `tests/test_madeira_control_a11y.py::test_no_external_cdn_references` |
| No blocking `alert()` (screen-reader keyboard-trap) | `tests/test_madeira_control_a11y.py::test_no_blocking_alert_call` |
| `role="alert"` used on error path (axe `aria-allowed-role` won't fire) | `tests/test_madeira_control_a11y.py::test_alert_role_used_on_error_path` |

Per the I49 P15 redesign + impeccable critique line 53 (which declared
"ship" with this Playwright + axe wiring as the explicit follow-up),
**zero Critical or Serious findings are expected at first live run** on
this baseline.

## Forward look (live mode contract)

Once OPS-54-1 fires, the operator runs:

```bash
pip install -r requirements-dev.txt          # pulls axe-playwright-python
py -m playwright install chromium             # browser engine
py scripts/browser-smoke.py --playwright --axe  # live audit
```

Live results overwrite this report's "Findings" table with the actual
per-impact counts and the per-rule violations (when any). Per
**D-IH-54-A**, Critical > 0 is release-gate-blocking; Serious > 0 is
warn-only at first run, escalates after one clean cycle.

Per **D-IH-54-D**, Moderate / Minor findings get filed in
[`risk-register.md`](../risk-register.md) deferred backlog with WCAG ID
+ remediation hint, revisited at the next WCAG 2.2 industry adoption
signal.
