# I54 / P4 — Fix Critical/Serious findings (G-54-1 NO-FIRE)

**Date:** 2026-05-03
**Phase:** P4 (Fix Critical/Serious findings)
**Outcome:** **G-54-1 NO-FIRE** (no live Critical/Serious findings to react to; dispatcher-validation mode).

## Why NO-FIRE

P3 reported zero findings in dispatcher-validation mode (no
`axe-playwright-python` installed). Per the gate contract:

> **G-54-1** (P4) — Any breaking HTML structural change to fix Critical
> findings on shipped surfaces (e.g., aria-pressed toggle restructure
> that touches operator workflow).

…there are no Critical findings to fix this cycle, so G-54-1 has no
input. The decision-log row notes this and re-arms G-54-1 for the
OPS-54-1 cycle.

## Edits to HTML this phase

**None.** The redesign baseline is preserved as-shipped at I49 P15.

The HTML-source assertions in `tests/test_madeira_control_a11y.py`
(I49 P15) + DOM-source contract assertions in
`tests/playwright/test_madeira_control_a11y_dom.py` (I54 P2) collectively
confirm the structural floor — but as noted in P3, this is not a
substitute for the live axe-core run.

## Deferred backlog (D-IH-54-D)

Empty this cycle (no findings → no deferrals).

```text
| Finding | WCAG ID | Severity | Surface | Remediation hint | Status |
|:--------|:--------|:---------|:--------|:-----------------|:-------|
| (none yet) | | | | | |
```

(Mirrored in [`risk-register.md`](../risk-register.md) deferred backlog
table; identical until OPS-54-1 fires.)

## Forward look

- **P5** wires `playwright_a11y_smoke` profile in `config/verification-profiles.json`; registers the dossier HTML URL in `AXE_IN_SCOPE_SURFACES`.
- **P6** closure UAT.
