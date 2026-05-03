# I54 / P5 — CI integration (`playwright_a11y_smoke` profile)

**Date:** 2026-05-03
**Phase:** P5 (CI integration)

## Deliverables

### 1. New `playwright_a11y_smoke` profile in `config/verification-profiles.json`

```jsonc
"playwright_a11y_smoke": {
  "description": "Initiative 54 P5: Playwright + axe-core a11y smoke audit on madeira_control + dossier HTML surfaces. Pre-commit: warn-only when axe-playwright-python is not installed (SKIP gracefully per R-54-1). Release-gate: Critical-only fail (D-IH-54-A). Run with: py scripts/browser-smoke.py --playwright --axe.",
  "steps": [
    {
      "id": "playwright_dom_a11y_unit_tests",
      "description": "Run tests/playwright/ DOM-source contract + wiring tests …",
      "argv": ["__pytest__", "tests/playwright/", "-v"]
    },
    {
      "id": "browser_smoke_axe_audit",
      "description": "scripts/browser-smoke.py --playwright --axe …",
      "argv": ["scripts/browser-smoke.py", "--playwright", "--axe"]
    }
  ]
}
```

Profile count: 15 → **16** total. Verified by `tests/test_verification_profiles.py` (5 tests pass, including the argv-shape lint that caught a `-m pytest` argv that was rejected → fixed to use the canonical `__pytest__` token; documented as part of this phase).

### 2. USER_GUIDE.md row in §16.3 browser-smoke flag table

Added `--axe` row + a paragraph cross-link to `docs/wip/planning/54-surface-test-hardening/`. Operators see the install path + the D-IH-54-A / D-IH-54-B contract from one screen.

### 3. Pre-commit vs release-gate split (D-IH-54-B)

Per **D-IH-54-B**, the profile is opt-in:

| Surface | Behavior when axe-playwright-python missing | Behavior on Critical findings | Behavior on Serious findings |
|:--|:--|:--|:--|
| `pre_commit` | SKIP gracefully (warn-only) | warn-only first cycle, escalates after one clean cycle (D-IH-54-A) | warn-only first cycle |
| `release_gate` | SKIP gracefully (warn-only) — gates do not block on missing dev tooling | **Critical = release block** | warn-only first cycle |

The two-step bar (D-IH-54-A) means the first clean operator-run cycle of OPS-54-1 — once `axe-playwright-python` is installed and the live audit returns 0 Critical / N Serious — the next cycle promotes Serious to a release-gate fail tier. A POLICY row could codify this; per **D-IH-54-A**, that POLICY row is conditional and lands on the first clean cycle (not authored speculatively).

## Verification

```text
py -m pytest tests/test_verification_profiles.py -q
=> 5 passed in 0.12s
```

```text
py -m pytest tests/playwright/ -q
=> 25 passed, 2 skipped in 0.25s
```

```text
py -c "import json; data = json.load(open('config/verification-profiles.json')); \
       print('profiles:', len(data['profiles'])); \
       print('has playwright_a11y_smoke:', 'playwright_a11y_smoke' in data['profiles'])"
=> profiles: 16
=> has playwright_a11y_smoke: True
```

## Forward look

- **P6** closure UAT: pytest sweep, dossier `--filter madeira` Section 8 Surface UX subsection re-emit with `madeira_a11y` flavor (when the operator has run the live audit), CHANGELOG, README row Closed, WIP_DASHBOARD; flips I49 follow-up `OPS-49-craft-followups` complete.
