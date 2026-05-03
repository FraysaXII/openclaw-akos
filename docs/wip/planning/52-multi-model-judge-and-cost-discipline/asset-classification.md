---
language: en
status: active
initiative: 52-multi-model-judge-and-cost-discipline
report_kind: asset-classification
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 52 — Asset classification

Per [`docs/references/hlk/compliance/PRECEDENCE.md`](../../../docs/references/hlk/compliance/PRECEDENCE.md):

## Canonical (edit here first)

| Asset | Path | Notes |
|:------|:-----|:------|
| `judge.py` | [`akos/eval_harness/judge.py`](../../../akos/eval_harness/judge.py) | `JudgeRoster` class; `score_response_live` calls dispatcher; cassette captures all member `model_id`s (P2) |
| `cost_obs.py` | [`akos/eval_harness/cost_obs.py`](../../../akos/eval_harness/cost_obs.py) | `CostRecord.unit ∈ {"token", "gpu_hour"}`; aggregator forbids unit-mixing (P5) |
| `POLICY_REGISTER.csv` | [`docs/references/hlk/compliance/dimensions/POLICY_REGISTER.csv`](../../../docs/references/hlk/compliance/dimensions/POLICY_REGISTER.csv) | New `POL-EVAL-COST-CEILING-ENDPOINT-{RUNPOD,KALAVAI,...}-V1` rows (P5; reuses `cost_ceiling` policy_class from I50). `POL-EVAL-JUDGE-THRESHOLD-*-V1` edits only if P3 calibration surfaces drift |
| `JUDGE_ROSTER_V1.md` | `prompts/judge/JUDGE_ROSTER_V1.md` | Operator-pinned roster (P1) |
| `JUDGE_PROMPT_V1.md` | `prompts/judge/JUDGE_PROMPT_V1.md` | Operator-pinned judge prompt (P1) |
| `endpoint-prices.json` | `config/eval/endpoint-prices.json` | Per-endpoint USD/hour table (P5; FinOps-owned) |
| Section 03/04/08 | [`akos/dossier/sections.py`](../../../akos/dossier/sections.py) | Per-axis fail count + worst-axis trend; new Section 8 endpoint cost subsection (P6) |

## Mirrored / derived

| Asset | Path | Notes |
|:------|:-----|:------|
| `compliance.policy_register_mirror` | Supabase | Reseeded after POLICY edits (D-IH-51-D cadence applies) |
| `compliance.eval_run` | Supabase | Live writes via I47/P13 item 4; gains multi-judge `model_id`s in `judge_scores` JSONB (no DDL change) |
| `dossier_run.cost_breakdown` | Supabase | Distinguishes `judge_usd_per_token` vs `endpoint_usd_per_hour` (P6) |

## Reference-only

| Asset | Path | Notes |
|:------|:-----|:------|
| `tests/evals/cassettes/` | Repository | Multi-judge cassettes added under `<skill_id>/multi_judge/` keyed by roster fingerprint (P3) |
| `.github/workflows/eval-tier-b.yml` | Repository | `MAX_JUDGE_USD_PER_RUN` envelope wiring (P7) |
| `scripts/endpoint_cost_probe.py` | Repository | New script — queries RunPod / Kalavai APIs; SKIPs gracefully when env not set |
| `scripts/endpoint_envelope_alarm.py` | Repository | New script — alarm + auto-pause hook (D-IH-52-E opt-in) |
| `tests/test_eval_judge_multi.py` | Repository | New test suite for `JudgeRoster` consensus + tie-break + fallback |
| `tests/test_endpoint_cost_unit.py` | Repository | New test suite for `CostRecord.unit` discriminator |
| `tests/test_endpoint_envelope.py` | Repository | New test suite for envelope breach + alarm |

## Scope-out

| Asset | Why excluded |
|:------|:-------------|
| Public benchmark adoption (HELM / MASEval full suite) | D-DEFER-47-γ stays deferred; out-of-scope for I52 |
| Building a custom LLM judge model | We use vendor models + roster discipline (D-IH-52-A) |
| Replacing the offline rubric | Offline stays as cassette-replay default (`AKOS_RECORD_LIVE` unset path) |
| Auto-purchasing GPU capacity | Alarm-only by default (D-IH-52-E); operator decides on scale |
| FinOps replacement (full vendor lifecycle) | This is judge + endpoint cost discipline only; FINOPS register remains the SSOT for vendor counterparties |
