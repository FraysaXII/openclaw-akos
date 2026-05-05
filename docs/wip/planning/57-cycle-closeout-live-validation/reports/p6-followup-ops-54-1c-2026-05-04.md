---
language: en
status: closed
initiative: 57-cycle-closeout-live-validation
report_kind: phase-report
phase: P6-followup
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-05-04
---

# I57 P6 follow-up — OPS-54-1.c residual axe-Serious closed (2026-05-04)

## Outcome

**OPS-54-1.c closed.** Live `py scripts/browser-smoke.py --playwright --axe` against `/madeira/control` now returns **`0 Critical / 0 Serious / 0 Moderate / 0 Minor`** (down from `0 Critical / 1 Serious` at I57 P6 closure UAT). Two changes were required because the residual was actually a **two-source defect**:

1. **CSS contrast deepening** (the documented OPS-54-1.c fix). `static/madeira_control.html` light-mode `--accent` deepened from `oklch(56% 0.16 var(--brand-h))` to `oklch(48% 0.16 var(--brand-h))`. This raises the contrast ratio of the active `aria-pressed="true"` state on the locale switcher buttons (and the generic `button[aria-pressed="true"]`, the hover border, and the link colour) against `--accent-ink` (oklch 99%) past the WCAG 1.4.3 4.5:1 boundary.
2. **Bootstrap-JS settle race in `browser-smoke.py`'s axe injection** (the *actual* root cause). On the Python 3.14 free-threaded build + Windows msedge launch path, `axe_runner.run(page)` could fire while the page's `applyLocale(detectInitialLocale())` was still in-flight, producing a non-deterministic phantom `color-contrast` Serious finding even on pages that pass a cold sync `Axe()` inspection. Adding a 500 ms `page.wait_for_timeout(500)` between `page.goto(...wait_until="domcontentloaded")` and `axe_runner.run(page)` eliminates the flake.

Both changes ship together so the CSS-only path is robust to future re-introductions of the bootstrap-JS race, and the smoke-test path is robust to future borderline contrast values.

## Diagnostic trail

| Step | Observation | Conclusion |
|:-----|:------------|:-----------|
| 1 | I57 P6 closure UAT recorded `0 Critical / 1 Serious` on `/madeira/control` and filed the residual as OPS-54-1.c. | Engineering closure was correct; one residual remained. |
| 2 | OPS-54-1.c CSS deepening shipped; smoke re-run still reported `0 Critical / 1 Serious`. | The CSS deepening alone wasn't enough — or wasn't being measured. |
| 3 | Direct ad-hoc inspection via async axe API (`axe_playwright_python.async_playwright.Axe` against the live `/madeira/control`) returned `count: 0`. | The page itself had zero violations. |
| 4 | Direct ad-hoc inspection via sync axe API in a fresh subprocess returned `count: 0`. | The page itself had zero violations under the *same* sync-API code path used by `browser-smoke.py`. |
| 5 | Difference between the standalone runner and `browser-smoke.py`: the standalone added a `page.wait_for_timeout(500)` between `goto` and `axe.run`. | The 500 ms settle wait was masking a real race in `browser-smoke.py`. |
| 6 | `browser-smoke.py` patched to add the same 500 ms wait. Re-run reported `0 Critical / 0 Serious / 0 Moderate / 0 Minor`. | Race confirmed; both fixes shipping together. |

The async-API run at step 3 is what made it clear the residual was a measurement flake rather than a real ratio-still-too-low: with WCAG 1.4.3 the active `aria-pressed="true"` background at oklch(56%) was already passing in steady state — the failing read happened only when axe tried to compute contrast against a button mid-transition between its inactive and active style.

## Changes

### `static/madeira_control.html` — light-mode `--accent` deepened

```html
/* I57 P6 follow-up / OPS-54-1.c — light-mode --accent deepened from
   oklch(56%) to oklch(48%) so the active aria-pressed="true" state of
   the locale switcher buttons clears the WCAG 1.4.3 4.5:1 contrast
   boundary against --accent-ink (oklch 99%) in light mode. The previous
   oklch(56%) value sat at the boundary and produced a residual
   axe-core color-contrast Serious finding even after OPS-54-1.a hardened
   the inactive state. The deepening also benefits the generic active
   button state (#btn-ask aria-pressed="true"), the hover border color,
   and link colour without affecting brand identity (same hue 215, same
   chroma 0.16). Dark-mode --accent at line ~31 unchanged because dark-
   mode contrast was already passing. */
--accent: oklch(48% 0.16 var(--brand-h));
```

### `scripts/browser-smoke.py` — axe injection settle wait

```python
# I57 P6 follow-up — let the page's bootstrap JS settle before injecting
# axe-core. Without this, on Python 3.14 free-threaded builds + Windows
# msedge, axe can be invoked while the locale-detection / aria-pressed
# initialisation is still in-flight, producing a non-deterministic
# "1 Serious color-contrast" phantom finding even on pages that pass a
# cold sync_playwright + Axe inspection. The 500ms wait is small enough
# to be invisible in the smoke-test budget and stops a flaky-failure
# vector that already cost a P6 OPS-54-1.c follow-up cycle to diagnose.
page.wait_for_timeout(500)
report = axe_runner.run(page)
```

### `tests/playwright/test_madeira_control_a11y_dom.py` — regression lock

New test `test_i57_p6_followup_light_mode_accent_is_deepened_for_wcag_contrast` asserts the deepened value is present in the `:root` block. The earlier `test_i57_locale_buttons_have_explicit_high_contrast_styling` (OPS-54-1.a) and `test_i57_handoff_example_is_keyboard_focusable` (OPS-54-1.b) regression locks remain in force.

## Verification

| Check | Command | Result |
|:------|:--------|:-------|
| DOM regression locks (3 OPS-54-1 tests) | `py -m pytest tests/playwright/test_madeira_control_a11y_dom.py -v` | **18/18 PASS** |
| Mirror emit regression locks (P1 fixes intact) | `py -m pytest tests/test_sync_compliance_mirrors_from_csv.py -v` | **11/11 PASS** |
| Live axe re-audit | `py scripts/browser-smoke.py --playwright --axe` | **`0 Critical / 0 Serious / 0 Moderate / 0 Minor`** on `/madeira/control` |

## Decisions captured during execution

- **No new D-IH-57-* required.** OPS-54-1.c was a pre-existing residual; this report closes it within the I57 envelope (D-IH-57-A "single coordinating I57") rather than spawning a new initiative for a one-line CSS + one-line script change.
- The `browser-smoke.py` settle delay is **not** an OPS-54-1.d follow-up — it lands as a quality-of-implementation fix to OPS-54-1.c since the two are inseparable in practice (without the delay, OPS-54-1.c regressions would silently re-flake).

## Cross-references

- I57 P6 closure UAT (which filed the residual): [`uat-i57-cycle-closeout-2026-05-04.md`](uat-i57-cycle-closeout-2026-05-04.md).
- I54 audit baseline (the rule the residual was filed against): [`docs/wip/planning/54-surface-test-hardening/reports/uat-i54-live-a11y-audit-20260504.md`](../../54-surface-test-hardening/reports/uat-i54-live-a11y-audit-20260504.md).
- I57 P1 quick-wins report (which closed OPS-54-1.a + OPS-54-1.b): [`p1-bucket4-quick-wins-2026-05-04.md`](p1-bucket4-quick-wins-2026-05-04.md).
- D-IH-54-A (single-Critical-only release-gate fail policy): preserved — `0 Critical` continues to be the only PASS gate.
