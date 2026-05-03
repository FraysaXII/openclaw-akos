# a11y audit — dossier HTML output (`render_dossier_html`)

**Date:** 2026-05-03
**Surface:** dossier HTML rendered by `akos.dossier.html_render.render_dossier_html` (operator runs `py scripts/render_uat_dossier.py --format html` to produce a concrete file)
**Audit tool:** axe-core (planned)
**Audit mode:** **DISPATCHER VALIDATION ONLY** (stub-mode; mirrors I52 P3 / I53 P3 pattern)
**Operator opt-in for live mode:** see this report's "Forward look" section

## Mode

Same dispatcher-validation posture as
[`a11y-audit-madeira-control-2026-05-03.md`](./a11y-audit-madeira-control-2026-05-03.md):
the audit wiring is verified end-to-end at the template + helper level
without `axe-playwright-python` installed.

## Findings (stub mode)

| Severity (D-IH-54-A) | Count | Notes |
|:--------------------|------:|:-----|
| Critical | **0** | dispatcher-validation; live audit pending OPS-54-1 |
| Serious | **0** | dispatcher-validation; live audit pending OPS-54-1 |
| Moderate | **0** | dispatcher-validation; live audit pending OPS-54-1 |
| Minor | **0** | dispatcher-validation; live audit pending OPS-54-1 |

## Dispatcher-validation evidence

The dossier HTML template carries an axe-friendly structural floor that
makes Critical-tier findings unlikely on a clean stub render:

| Evidence | Source |
|:---------|:-------|
| `<!doctype html>` + `<html lang="en">` declared | `tests/playwright/test_dossier_html_a11y.py::test_dossier_template_declares_doctype` + `test_dossier_template_declares_html_lang_attribute` |
| `<meta charset="utf-8">` + `<meta name="viewport">` | `test_dossier_template_declares_meta_charset` + `test_dossier_template_declares_meta_viewport` |
| `<main>` landmark (axe `landmark-one-main`) | `test_dossier_template_has_main_landmark` + `test_rendered_dossier_html_has_main_landmark_when_callable` |
| `<header>` + `<footer>` landmarks (axe `region` rule) | `test_dossier_template_has_header_and_footer_landmarks` |
| Content-Security-Policy header (CSP-compliant; axe-friendly offline) | `test_dossier_template_has_csp_header` |
| No inline JS event handlers (`onclick=`, `onload=`, etc.) | `test_dossier_template_has_no_inline_javascript_event_handlers` |
| `<dl>/<dt>/<dd>` semantic structure for meta key-value pairs | `test_dossier_template_uses_definition_list_for_meta_pairs` |
| No external CDN refs (`fonts.googleapis.com`, `cdn.jsdelivr.net`, `unpkg.com`) | `test_dossier_template_no_external_font_or_script_src` |

Per **R-54-3** mitigation, all of these are **template-time** assertions
— accumulated KM data cannot regress the template-level a11y contract.

## Forward look (live mode contract)

Once OPS-54-1 fires:

```bash
pip install -r requirements-dev.txt
py -m playwright install chromium
py scripts/render_uat_dossier.py --filter madeira --mode snapshot --format html --out-dir artifacts/dossier-i54-p3-live
# Then point Playwright at the generated HTML file (file:// or
# served via local server) and run axe-core. Today's
# AXE_IN_SCOPE_SURFACES does not yet include a stable URL for the
# dossier HTML output; that registration lands at I54 P5 (CI
# integration), which adds the dossier surface to the in-scope list
# under a stable test fixture path.
```

Per **D-IH-54-A** + **D-IH-54-D** the same severity-tier policy applies
as for `madeira_control.html`.
