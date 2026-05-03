---
language: en
status: complete
initiative: 51-persona-calibration-cleanup
report_kind: phase-report
phase: P5
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# I51 / P5 — D-IH-51-C CI tightening: `--hard-fail-on-drift` in `eval_tier_b_weekly`

**Date:** 2026-05-03
**Phase scope:** D-IH-51-C — wire calibration drift hard-fail into the
weekly Tier-B GitHub Actions workflow; preserve pre-commit as warn-only.
**Plan reference:** §"Initiative 51" P5 of the master roadmap.

## TL;DR

- Added a new `calibration-drift-gate` job to
  [`.github/workflows/eval-tier-b.yml`](../../../../.github/workflows/eval-tier-b.yml)
  (single-invocation, runs `needs: tier-b`).
- Job invokes `py scripts/calibrate_scenarios.py --hard-fail-on-drift`
  against the per-persona `target_difficulty_band` values landed in
  I51/P3, exits non-zero on any persona outside ±5pp of its own band.
- Job uploads the resulting
  `artifacts/calibration/calibration-baseline-*.{md,json}` as a
  90-day-retention artifact (`calibration-baseline`).
- Pre-commit stays warn-only by design: there is no
  `.pre-commit-config.yaml` calibration hook in the repo, and
  D-IH-51-C **deliberately bounds the hard-fail surface** to the
  weekly Tier-B profile so operators can iterate freely on
  `target_difficulty_band` without per-keystroke gating.
- Local dry-run: `py scripts/calibrate_scenarios.py --hard-fail-on-drift --quiet` →
  exit 0 (0 / 17 personas outside tolerance; matches P3 closure state).

## What changed

### `.github/workflows/eval-tier-b.yml`

A new job under the same workflow:

```yaml
calibration-drift-gate:
  if: ${{ vars.AKOS_TIER_B_ENABLED == 'true' }}
  runs-on: ubuntu-latest
  needs: tier-b
  timeout-minutes: 5
  permissions:
    contents: read
  steps:
    - uses: actions/checkout@v4
    - name: Setup Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.13'
    - name: Install deps (calibration only; no LLM toolchain)
      run: |
        python -m pip install --upgrade pip
        pip install -e .
    - name: Calibration baseline + hard-fail-on-drift gate (D-IH-51-C)
      run: |
        python scripts/calibrate_scenarios.py --hard-fail-on-drift
    - name: Upload calibration artifacts
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: calibration-baseline
        path: |
          artifacts/calibration/calibration-baseline-*.md
          artifacts/calibration/calibration-baseline-*.json
        retention-days: 90
```

Design notes:

- **Why a separate job, not a step in the matrix?** The matrix `tier-b`
  job has up to 10 cells (2 model_tiers × 5 personas); embedding
  `--hard-fail-on-drift` inside it would invoke calibration up to 10
  times per workflow run with identical output. A separate
  `needs: tier-b` job runs once.
- **Why `needs: tier-b`?** Calibration drift gating is only meaningful
  if the Tier-B regression sweep itself ran (or was deliberately
  skipped via missing `AKOS_RECORD_LIVE`). Putting it after the matrix
  means a flake-only failure surface in `tier-b` doesn't mask
  calibration drift, and a calibration-only failure surface here
  doesn't mask a regression in `tier-b`.
- **Why no LLM toolchain in install?** Calibration is a pure CSV →
  in-memory aggregation; no API keys needed.
- **Why `--quiet` is *not* set in CI?** GHA captures stdout into the
  job log; the full markdown report is useful for forensics. Local
  invocations may use `--quiet`.

### Pre-commit invariant

There is no `.pre-commit-config.yaml` in the repo as of 2026-05-03
(`Glob {.pre-commit*}` → 0 files). D-IH-51-C scope is therefore
preserved without explicit action: the only `--hard-fail-on-drift`
caller in the repo is now the new GHA job.

If a future initiative adds `.pre-commit-config.yaml`, the
calibration script **must not** be added as a pre-commit hook — that
would violate D-IH-51-C and be flagged at release-gate.

## Verification

| Gate | Result |
|:-----|:-------|
| `py scripts/calibrate_scenarios.py --hard-fail-on-drift --quiet` | exit 0 |
| `py scripts/check-drift.py` | PASS (no schema drift introduced) |
| YAML well-formedness (workflow YAML) | OK; new job indents under `jobs:` symmetrically with `tier-b` |
| Pre-commit invariant | preserved — no `.pre-commit-config.yaml` in repo |

```text
$ py scripts/calibrate_scenarios.py --hard-fail-on-drift --quiet
Calibration report written: artifacts/calibration/calibration-baseline-20260503T175543Z.md
Calibration JSON written:   artifacts/calibration/calibration-baseline-20260503T175543Z.json
$ echo $?
0
```

## What this is NOT

- A new pre-commit hook (deliberately excluded — D-IH-51-C scope).
- A change to the calibration tolerance (still ±5pp per D-IH-47-C).
- A change to the per-persona `target_difficulty_band` values
  (those landed in I51/P3 and are unchanged here).
- A change to the matrix dimensions of `tier-b` (still
  model_tier × persona; calibration is orthogonal).

## Carriers

- None new. P5 closes the third-party seam from R-47-2 — calibration
  drift is now a CI-gated property of the repository.

## Cross-references

- Decision: D-IH-51-C in [`decision-log.md`](../decision-log.md).
- Evidence: E6, E6a in [`evidence-matrix.md`](../evidence-matrix.md).
- Predecessor phase: [`p4-flake-threshold-2026-05-03.md`](p4-flake-threshold-2026-05-03.md).
- Predecessor calibration baseline: [`p3-rebalance-2026-05-03.md`](p3-rebalance-2026-05-03.md).
- Workflow: [`.github/workflows/eval-tier-b.yml`](../../../../.github/workflows/eval-tier-b.yml).
- Script: [`scripts/calibrate_scenarios.py`](../../../../scripts/calibrate_scenarios.py).
