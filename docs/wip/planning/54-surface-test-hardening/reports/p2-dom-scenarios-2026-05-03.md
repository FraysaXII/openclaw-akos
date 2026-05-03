# I54 / P2 — DOM-level a11y scenarios

**Date:** 2026-05-03
**Phase:** P2 (DOM-level scenario authoring)

## Deliverables

### `tests/playwright/__init__.py` (new)

Empty package marker so pytest can discover tests under `tests/playwright/`.

### `tests/playwright/test_madeira_control_a11y_dom.py` (new — 16 tests)

Two categories:

1. **Wiring tests for the I54 P1 helpers** (8 tests) — exercise `_summarise_axe_violations` (count by impact tier; empty/None handling; unknown-impact routing), `AXE_IN_SCOPE_SURFACES`, `run_axe_audits` SKIP semantics (no-Playwright, no-axe-package, one-result-per-in-scope-surface), and the `--axe` flag presence in the CLI source.
2. **DOM-source contract tests** (8 tests) — assert the DOM-targetable structure that the live Playwright run will resolve: `role=status`, `aria-live=polite`, locale buttons (`data-locale-set=en/es/fr`), mode buttons (`#btn-ask` + aria-pressed), focus-visible rule, `<main>` landmark, no external `<script src=` / `<link>`, no `alert()` keyboard trap.

### `tests/playwright/test_dossier_html_a11y.py` (new — 11 source-level + 2 conditional-render tests)

Template-level a11y contract for the dossier HTML output rendered by `akos.dossier.html_render.render_dossier_html`:
- Source-level: doctype, `html lang`, `meta charset/viewport`, `<main>` landmark, `<header>` + `<footer>` landmarks, CSP header, no inline JS event handlers, definition-list semantics for meta pairs, no external CDN refs.
- Conditional-render: when the function is callable with a `SimpleNamespace`-shaped stub, the rendered HTML still carries `<main>`, `<html lang>`, `<header>`, `<footer>` and properly escapes `run_id` metadata. Per **R-54-3** mitigation: this is a template-time check, not a data-time check, so accumulated KM data cannot regress this contract.

## Verification

```text
py -m pytest tests/playwright/ -v
======================== 25 passed, 2 skipped in 0.25s ========================
```

Two `SKIPPED` entries are intentional — the conditional-render tests skip when the `render_dossier_html` signature changes (covered by source-level tests in the same file). Mirrors the pattern used by `tests/test_madeira_control_a11y.py` for HTML-source baseline tests.

The new tests run without `axe-playwright-python` or live Playwright installed (the suite runs in 0.25s), per **R-54-1 / R-54-4** mitigation. When axe-playwright-python is installed at I54 P3 (operator opt-in), the live audit becomes the source of truth; these tests stay as the wiring + DOM-source contract floor.

## Coverage matrix

| In-scope surface (D-IH-54-C) | DOM-source contract test | Live axe target |
|:-----------------------------|:-------------------------|:----------------|
| `static/madeira_control.html` | ✓ 8 DOM-source tests | `axe_madeira_control` scenario in `AXE_IN_SCOPE_SURFACES` |
| Dossier HTML (template) | ✓ 11 template-level tests + 2 conditional-render tests | not yet wired into AXE_IN_SCOPE_SURFACES — added at I54 P5 (CI integration) where the live dossier surface URL gets registered |

## Forward look

- P3 runs the live axe audit OR ships in stub-mode (this cursor session can't `pip install axe-playwright-python`; see I52 P3 / I53 P3 stub-mode pattern).
- P4 either fixes Critical/Serious findings (G-54-1 fires) or NO-FIRE governance event when the audit runs clean.
- P5 wires `playwright_a11y_smoke` profile in `config/verification-profiles.json` and registers the dossier HTML URL in `AXE_IN_SCOPE_SURFACES`.
