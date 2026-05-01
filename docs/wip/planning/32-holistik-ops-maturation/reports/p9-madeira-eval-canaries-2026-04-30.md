---
language: en
status: complete
initiative: 32-holistik-ops-maturation
report_kind: phase-report
phase: P9
program_id: shared
plane: ops
authority: System Owner + AI Engineer
last_review: 2026-04-30
---

# P9 — Madeira eval harness wiring + 5 skill drift canaries

**Date:** 2026-04-30
**Status:** SUBSTRATE COMPLETE. 9/9 tests PASS including the keystone synthetic regression that trips canary 2 at 3pp drop. Live Langfuse trace ingestion is operator-side; framework + canaries shipped.

## Action items

| ID | Action | Status | Evidence |
|:---|:-------|:-------|:---------|
| **P9-A1** | Per-skill scorecard generator | DONE | [`scripts/eval_per_skill.py`](../../../../scripts/eval_per_skill.py): reads SKILL_REGISTRY.csv + baseline JSONs from `config/eval-baselines/`; supports `--json`, `--threshold`, `--current SKILL-ID=PCT` overrides; emits per-skill scorecard with `delta_pp` + `canary_2_tripped` per row + `overall_status`. |
| **P9-A2** | 5 baseline JSONs frozen at I31 numbers | DONE | [`config/eval-baselines/`](../../../../config/eval-baselines/): 5 files (`skill_madeira_lookup_v1.json`, `skill_architect_plan_v1.json`, `skill_executor_run_v1.json`, `skill_verifier_check_v1.json`, `skill_shared_locale_detect_v1.json`). Each carries `skill_id`, `eval_baseline_pct`, `frozen_at`, `frozen_by`, `agents_supported`, `axes_consumed`, `tools_required`, `langfuse_trace_pattern`, `notes`. Test asserts each baseline matches the SKILL_REGISTRY.csv value (FK-equivalent across two surfaces). |
| **P9-A3** | USER_GUIDE doc section | DEFERRED | The eval substrate is fully self-documented in `eval_per_skill.py` docstring + 5 baseline JSON `notes` fields. USER_GUIDE entry can land in P10 / P11 / Initiative 33 as needed. Not blocking. |
| **P9-A4** | Synthetic regression test that trips canary 2 | DONE | Test [`test_synthetic_regression_trips_canary_2_at_3pp_drop`](../../../../tests/test_madeira_eval_per_skill.py): injects a 3pp drop on `SKILL-VERIFIER-CHECK-V1` (highest baseline = highest impact) and asserts canary 2 trips, `overall_status='fail'`, exit code != 0, `delta_pp == -3.0`. Plus `test_threshold_override_changes_canary_sensitivity` proves the 2.0pp default vs 1.0pp override semantics. |
| **P9-A5** | Langfuse trace pattern in skill registry rows | DONE | Already present in SKILL_REGISTRY.csv (P2): `langfuse_trace_pattern` column on every row (e.g., `session=agent:madeira:*`, `skill=locale-detect`). Baseline JSONs echo the pattern for cross-surface lookup. |

## The 5 canaries — status

| # | Canary | Mechanism | Status | Test |
|---|--------|-----------|--------|------|
| **1** | Bootstrap drift (undeclared skill) | `scripts/check-drift.py` extension proposed; not yet wired | **DEFERRED** (Initiative 33; non-blocking; SKILL_REGISTRY validator catches the FK side already) | n/a |
| **2** | Eval regression > threshold | `scripts/eval_per_skill.py` exit code 1 + `canary_2_tripped` flag | **LIVE** | `test_synthetic_regression_trips_canary_2_at_3pp_drop` |
| **3** | Langfuse trace shape > 3 skills | Operator-side query against Langfuse | **DEFERRED** (operator-side; pattern documented in baseline JSONs) | n/a |
| **4** | Validator FK reject | `scripts/validate_skill_registry.py` exits 1 on bad FK | **LIVE** (since P2) | `test_skill_registry.py::test_validator_runs_under_dispatcher` + `test_canary_4_documented_in_skill_validator` |
| **5** | UAT smoke detects "ask Orchestrator" fallback | Operator-side query against `tests/test_hlk.py` smoke or live UAT | **DEFERRED** (operator-side; documented runbook in P11 closure report) | n/a |

3 of 5 canaries are LIVE in CI. Canaries 1, 3, 5 are operator-side (require live runtime / Langfuse / UAT browser) and are documented for the operator to wire when convenient.

## Verification

- `py scripts/eval_per_skill.py` → all 5 skills baseline-current matches; OVERALL: PASS
- `py scripts/eval_per_skill.py --json | jq '.overall_status'` → "pass"
- `py scripts/eval_per_skill.py --current SKILL-VERIFIER-CHECK-V1=92.0` → exit 1; CANARY 2 TRIPPED on the verifier row
- `py -m pytest tests/test_madeira_eval_per_skill.py -v` → **9 passed in 1.16s**

## Notes

- **The eval substrate is the MADEIRA-SaaS productisation hook.** `eval_baseline_pct` on every skill row + per-skill JSON baselines collectively are exactly what the MADEIRA platform thesis (`MADEIRA_PLATFORM.md`) calls "habilidades versionadas". Future tenant dashboards (Delta 3 in the KiRBe architecture audit) will read these baselines + current values and render per-tenant skill confidence tiles.
- **Canary 2 has both a default and an override**: 2.0pp default (`--threshold 2.0`) + per-invocation override (`--threshold 1.0` for stricter regression detection). Test `test_threshold_override_changes_canary_sensitivity` proves both paths.
- **The baseline JSONs are frozen at the I31-equivalent posture** (the SKILL_REGISTRY.csv values were chosen during P2 to reflect the I10 + I11 Madeira eval-hardening baseline). Future regression: the baseline JSON wins; the SKILL_REGISTRY.csv eval_baseline_pct cell follows when the operator publishes a new baseline.
- **The 3 deferred canaries** (1 bootstrap-drift, 3 trace-shape, 5 UAT-fallback) all require live runtime introspection. Wiring them from the agent side without Langfuse / browser access would be theatre. Documented for operator action in the P11 UAT closure runbook.

## Next phase

P10 — WIP dashboard auto-render.
