---
language: en
status: active
initiative: 47-user-centric-uat
report_kind: phase-report
phase: P10
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-05-02
---

# I47 P10 — Per-persona scorecard wiring + difficulty meta-eval

## What shipped

### `ScoreRow` extension (D-IH-47-F)

Extended `akos/eval_harness/v2.py:ScoreRow` with 4 new fields, all back-compatible (default to None / empty dict):

| Field | Type | Purpose |
|:---|:---|:---|
| `persona_id` | `str \| None` | FK PERSONA_REGISTRY (or `OPERATOR` pseudo); None for non-persona rows |
| `difficulty_class` | `str \| None` | trivial / moderate / hard / impossible |
| `scenario_class` | `str \| None` | lookup / multihop / adversarial / recovery / benchmark / cross_axis / cannot_answer |
| `judge_scores` | `dict[str, int]` | P12 LLM-judge 3-axis: `{brand_voice, citation, persona_fit}` |

### `Scorecard.to_markdown()` extension

Two new sections, emitted only when relevant:
1. **Per-persona breakdown** — emitted when ANY row has `persona_id`. Aggregates total / PASS / FAIL / SKIP / per-difficulty counts per persona.
2. **LLM-judge 3-axis** — emitted when ANY row has `judge_scores`. Aggregates mean / min / max / FAIL count (`<4`) per axis.

### `akos/eval_harness/persona.py` (NEW)

Per-persona aggregator + filtering helpers. Public API:
- `load_persona_scenarios(path) -> list[dict]`
- `filter_scenarios(scenarios, *, persona_id=None, difficulty_class=None, scenario_class=None, skill_id=None, tier=None, lifecycle="active")`
- `aggregate_by_persona(rows: list[ScoreRow]) -> dict[str, dict[str, int]]`
- `calibration_distribution(scenarios=None, target=None, tolerance_pp=5.0) -> dict[str, CalibrationResult]`
- `render_calibration_markdown(results) -> str`

`CALIBRATION_TARGET = {trivial: 10, moderate: 40, hard: 40, impossible: 10}` and `CALIBRATION_TOLERANCE_PP = 5.0` per D-IH-47-C.

### `scripts/calibrate_scenarios.py` (NEW)

Operator CLI for the difficulty meta-eval. Emits paired markdown + JSON report to `artifacts/calibration/calibration-baseline-<UTC>.{md,json}`.

```
py scripts/calibrate_scenarios.py                  # default; warn-only
py scripts/calibrate_scenarios.py --persona OPERATOR
py scripts/calibrate_scenarios.py --hard-fail-on-drift  # CI-friendly
```

### `scripts/eval.py` extensions

3 new flags wired:
- `--persona <id>` — filter scorecard rows to one persona_id post-run
- `--difficulty <class>` — filter to one difficulty class post-run
- `--calibrate` — emit calibration distribution and exit (no eval run)
- `--judge-cost-cap <usd>` — P12 cost cap (default $0.01/scenario)
- `--no-judge` — P12 skip judge axis evaluation

### Supabase migration (D-IH-47-F + D-IH-47-J)

`supabase/migrations/20260502033500_i47_eval_run_persona_columns.sql`:
- Adds `persona_id TEXT`, `difficulty_class TEXT`, `scenario_class TEXT`, `judge_scores JSONB` to `compliance.eval_run`
- 4 new indexes (single-column partial + composite `(persona_id, difficulty_class)`)
- Idempotent CREATE TABLE IF NOT EXISTS for environments without I45 P4 base
- RLS posture re-asserted (deny anon + authenticated; service_role-only)
- Applied to MasterData via `npx supabase db push`

## Calibration baseline (P10 first run)

`artifacts/calibration/calibration-baseline-20260502T023346Z.{md,json}`:

| Persona group | Total | trivial% | moderate% | hard% | impossible% | Within tol? |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **__overall__** (326) | 326 | 11.0 | 40.8 | 40.2 | 8.0 | **YES** |
| OPERATOR (55 with cross-cutting) | 55 | 16.4 | 38.2 | 36.4 | 9.1 | NO (trivial +6.4pp) |
| PERSONA-INVESTOR-COLD (35 with cross-cutting) | 35 | 17.1 | 40.0 | 34.3 | 8.6 | NO (trivial +7.1pp) |
| ... 11 more personas outside ±5pp | | | | | | |

**Operator decision:** R-47-2 ("calibration is subjective") in action. The cumulative library hits target, but per-persona drift surfaces because cross-cutting scenarios (P6/P7/P8/P9) attribute scenarios to specific personas. Three options per the risk register:

1. **Rebalance scenarios per-persona** (move some cross-cutting hard scenarios to other personas)
2. **Adjust target per-persona** (some personas have inherently hard distributions)
3. **Accept and note in decision-log** (cumulative target met; per-persona is informational)

The default warn-only mode preserves operator agency. CI-mode `--hard-fail-on-drift` is available for tightened discipline.

## Verification

- 25 new tests in `tests/test_eval_persona_calibration.py` PASS
- `py scripts/eval.py --mode all` PASS (existing canary + smoke + rubric still green)
- `py scripts/eval.py --calibrate` PASS (emits per-persona table)
- `py scripts/calibrate_scenarios.py` PASS (writes paired md + json artifact)
- `py scripts/validate_hlk.py` OVERALL PASS
- Supabase migration applied to MasterData

## Cross-references

- D-IH-47-F (ScoreRow extension)
- D-IH-47-C (40/40/10/10 calibration target)
- D-IH-47-J (judge_scores JSONB column for P12)
- I45 P4 (compliance.eval_run base table)
- R-47-2 (calibration subjectivity — surfaced in this report)
