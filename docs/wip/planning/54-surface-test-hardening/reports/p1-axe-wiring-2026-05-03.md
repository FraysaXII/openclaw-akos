# I54 / P1 — Wire axe-core into Playwright (`--axe` flag)

**Date:** 2026-05-03
**Phase:** P1 (axe-core wiring)

## Deliverables

### 1. New `requirements-dev.txt`

Pins `axe-playwright-python>=0.1.4,<0.2` (MIT license; minor-version pin avoids surprise rule-set drift between cycles). Documents the DEV vs runtime scope split and forward-look on relocating `playwright>=1.40` from `requirements.txt`.

```
# AKOS dev-only dependencies (Initiative 54 P1).
axe-playwright-python>=0.1.4,<0.2
```

### 2. `scripts/browser-smoke.py` — `--axe` flag + helpers

- New top-level import block guards `axe-playwright-python` import behind try/except (`AXE_AVAILABLE` flag), mirroring the existing `PLAYWRIGHT_AVAILABLE` pattern. No hard import requirement at runtime.
- New `--axe` CLI flag.
- New `AXE_IN_SCOPE_SURFACES` constant (today: `[("axe_madeira_control", "/madeira/control")]`).
- New `_summarise_axe_violations(violations)` helper — counts violations by `impact` ∈ {critical, serious, moderate, minor, unknown}.
- New `_check_axe_for_url(page, scenario_id, url_path, axe_runner)` helper — runs axe-core, applies D-IH-54-A severity logic:
  - Critical > 0 → **FAIL** (release-gate-blocking).
  - Critical = 0 + Serious > 0 → **PASS** with detail noting Serious as warn-only first cycle (per D-IH-54-A two-step ramp).
  - Critical = 0 + Serious = 0 → **PASS** (clean).
- New `run_axe_audits(headed, engine)` orchestrator — owns its own browser launch; gracefully SKIPs when Playwright or axe-playwright-python is missing (R-54-1 / R-54-4 mitigation).
- `main()` extended: when `--axe` is requested, append axe results after the Playwright scenario block. Three branches:
  1. `--axe --playwright` AND Playwright workers usable → run real axe audit.
  2. `--axe --playwright` AND Playwright workers **un**usable → SKIP axe scenarios with a clear "Playwright worker unusable" message (does not double-fail; this is the typical Windows worker-crash path).
  3. `--axe` without `--playwright` → SKIP axe scenarios with `"--axe requires --playwright"` message.

### 3. Smoke-test results (this cycle)

#### `py scripts/browser-smoke.py --axe` (no --playwright)

```
[SKIP] axe_madeira_control            --axe requires --playwright (Initiative 54 P1)
```

The new `axe_madeira_control` scenario appears in `JSON_RESULTS` as expected. Exit code is 1 (existing connection-refused FAILs from gateway-down environment; not introduced by I54 P1).

#### `py scripts/browser-smoke.py --playwright --axe`

Playwright workers crashed on this Windows host (pre-existing issue: STATUS_ACCESS_VIOLATION 0xC0000005; documented at `browser-smoke.py` line 859 as the "If scenarios failed but browsers work, run: ..." path). The axe block correctly fell through to the `playwright_worker_unusable` SKIP path (no spurious double-fail). The flag wiring is structurally correct; live-mode validation will happen on a Windows host where Playwright workers boot cleanly OR on Linux/macOS CI.

## Verification

- `py scripts/check-drift.py` — PASS (no drift detected).
- `py scripts/browser-smoke.py --axe` — `axe_madeira_control` scenario present in output (SKIP with clear message).
- ReadLints on `scripts/browser-smoke.py` — no linter errors.
- Imports degrade gracefully when `axe-playwright-python` is not installed (the cursor session's case): module import succeeds, `AXE_AVAILABLE=False`, `run_axe_audits()` returns SKIP for every in-scope surface with a clear install-runbook message.

## Forward look

- P2 authors DOM-level scenarios in `tests/playwright/` for three-light status surfacing, language switcher, aria-pressed toggles, focus-visible, role=status announcements.
- P3 runs the actual a11y audit; in this cursor session, P3 ships in stub-mode (mirroring I52 P3 / I53 P3), forwarding **OPS-54-1** for the next operator-side `pip install -r requirements-dev.txt` + run cycle.
