---
language: en
status: active
initiative: 47-user-centric-uat
report_kind: asset-classification
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-02
---

# Initiative 47 — Asset Classification

Per [`PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md): every artifact below is classified as **canonical** (authored, SSOT in git), **mirrored / derived** (rebuildable from canonical), or **reference-only** (not governed).

## New canonical (planning artifacts)

| Path | Class | Owner | Validator |
|:-----|:------|:------|:----------|
| `docs/wip/planning/47-user-centric-uat/master-roadmap.md` | canonical | Founder + System Owner | `validate_planning_traceability` |
| `docs/wip/planning/47-user-centric-uat/decision-log.md` | canonical | Founder + System Owner | `validate_planning_traceability` |
| `docs/wip/planning/47-user-centric-uat/evidence-matrix.md` | canonical | Founder + System Owner | none (prose) |
| `docs/wip/planning/47-user-centric-uat/asset-classification.md` (this file) | canonical | Founder + System Owner | `validate_planning_traceability` |
| `docs/wip/planning/47-user-centric-uat/risk-register.md` | canonical | Founder + System Owner | `validate_planning_traceability` |
| `docs/wip/planning/47-user-centric-uat/scenario-taxonomy.md` (NEW per I47) | canonical | System Owner | none (prose) |

## New canonical (registry surface)

| Path | Class | Owner | Validator |
|:-----|:------|:------|:----------|
| `docs/references/hlk/compliance/dimensions/PERSONA_SCENARIO_REGISTRY.csv` (P1) | canonical | System Owner | `scripts/validate_persona_scenario_registry.py` (NEW) |
| `tenant_id` column (NULL default per D-IH-47-K) | canonical | System Owner | same validator (NULL accepted; non-NULL string) |
| New POLICY_REGISTER rows: `POL-EVAL-JUDGE-THRESHOLD-{BRAND_VOICE,CITATION,PERSONA_FIT}` (P12 per D-IH-47-J) | canonical | System Owner + Brand Manager | `scripts/validate_policy_register.py` (existing) |

## New canonical (vault overlays)

| Path | Class | Owner | Phase |
|:-----|:------|:------|:------|
| `prompts/overlays/PERSONA_OVERLAY.md` (P11 per D-IH-47-I) | canonical (template) | System Owner | P11 |
| `prompts/personas/<persona_id>/MADEIRA_HINTS.md` per Tier-1 persona (≥4 at P11 close) | canonical (per-persona override) | System Owner + Brand Manager | P11 |

## New mirrored / derived (Supabase mirrors)

| Path | Class | Source of truth | Mirror table |
|:-----|:------|:----------------|:-------------|
| `supabase/migrations/<ts>_i47_persona_scenario_registry_mirror.sql` (P1) | canonical migration | the migration | `compliance.persona_scenario_registry_mirror` |
| `compliance.persona_scenario_registry_mirror` table | mirrored | `PERSONA_SCENARIO_REGISTRY.csv` | RLS deny anon/auth; service_role only; `(persona_id, tenant_id)` composite index |
| `supabase/migrations/<ts>_i47_eval_run_persona_columns.sql` (P10) | canonical migration | the migration | extends `compliance.eval_run` with `persona_id` + `difficulty_class` columns |
| `supabase/migrations/<ts>_i47_eval_run_judge_scores.sql` (P12) | canonical migration | the migration | extends `compliance.eval_run` with `judge_scores JSONB` column |

## New mirrored / derived (cassettes)

| Path | Class | Recording authority | Replay reproducibility |
|:-----|:------|:--------------------|:-----------------------|
| `tests/evals/cassettes/persona/<persona_id>/<scenario_id>.jsonl` (~225 across all 16 personas; P2-P5) | mirrored / derived | `py scripts/eval.py record --persona <id> --scenario <id>` | Deterministic; replay does not require live LLM unless `probe_kind=live_llm` |
| `tests/evals/cassettes/cross_axis/<scenario_id>.jsonl` (~25; P6) | mirrored / derived | Same as above with `--scenario-class cross_axis` | Same |
| `tests/evals/cassettes/adversarial_persona/<persona_id>/<scenario_id>.jsonl` (~30; P7) | mirrored / derived | Same with `--scenario-class adversarial` | Same |
| `tests/evals/cassettes/benchmark/<adapter>/<scenario_id>.jsonl` (~30; P8) | mirrored / derived | Same with `--scenario-class benchmark` | Same |
| `tests/evals/cassettes/recovery/<scenario_id>.jsonl` (~15 + 1 real-chaos; P9) | mirrored / derived | Same with `--scenario-class recovery` | Synthetic mocks deterministic; real-chaos requires `AKOS_REAL_CHAOS_OK=1` |

## New scripts + modules

| Path | Class | Purpose | Phase |
|:-----|:------|:--------|:------|
| `akos/hlk_persona_scenario_csv.py` (NEW) | canonical (akos contract) | Field contract + valid enums for PERSONA_SCENARIO_REGISTRY.csv | P1 |
| `akos/eval_harness/persona.py` (NEW) | canonical | Per-persona aggregator + filtering helpers | P10 |
| `akos/eval_harness/judge.py` (NEW per D-IH-47-J) | canonical | LLM-as-judge 3-axis scoring | P12 |
| `scripts/validate_persona_scenario_registry.py` (NEW) | canonical | Schema + FK enforcement | P1 |
| `scripts/calibrate_scenarios.py` (NEW) | canonical | P0 + P10 difficulty meta-eval; auto-classifies scenarios into difficulty buckets | P0 + P10 |
| `scripts/agent_memory_trigger_watcher.py` (NEW per D-IH-47-G item 3) | canonical | Cron-ready trigger watcher per I46 P4 ADR | P13 |
| `scripts/eval.py` extensions | canonical (existing) | New flags: `--persona <id>`, `--calibrate`, `--difficulty <class>`, `--judge-cost-cap <usd>`, `--real-chaos` (env-gated) | P10/P11/P12/P9 |
| `scripts/assemble-prompts.py` extension | canonical (existing) | New flag: `--persona <id>` (lazy-loads persona overlay fragments) | P11 |

## Modified canonical

| Path | Change | Phase |
|:-----|:-------|:------|
| `akos/eval_harness/v2.py` | `ScoreRow` extended with `persona_id`, `difficulty_class`, `scenario_class`, `judge_scores: dict` fields; `Scorecard.to_markdown()` extended with per-persona section | P10 |
| `akos/hlk_graph_model.py` | No changes (model already defines all 10 dimensions; sync_hlk_neo4j uses them in P13 item 1) | — |
| `scripts/sync_hlk_neo4j.py` | `sync_csv_graph()` extended to write all 10 dimensions (was 4) | P13 item 1 |
| `scripts/sync_compliance_mirrors_from_csv.py` | Boolean column emit fix (`true`/`false` not `''`) | P13 item 2 |
| `scripts/validate_hlk.py` | Dispatcher gains `validate_persona_scenario_registry.py` step | P1 |
| `prompts/base/MADEIRA_BASE.md` | No changes (overlay system in P11 keeps base unchanged) | — |
| `docs/wip/planning/README.md` | New row for I47 | P0 |
| `docs/wip/planning/WIP_DASHBOARD.md` | Re-rendered | P0 + P15 |
| `CHANGELOG.md` | Closure entry | P15 |
| `.github/workflows/eval-tier-b.yml` | Matrix extended to 4-D (model_tier × persona × scenario_class × judge_axis) | P14 |

## New CI

| Profile | Trigger | Phase |
|:--------|:--------|:------|
| `persona_scenario_smoke` (NEW; Tier A only) | `pre_commit` | P10 |
| `eval-tier-b.yml` 4-D matrix extension | weekly cron + workflow_dispatch (per D-IH-47-H) | P14 |

## Reference-only / external (cited but not authored)

| Source | Citation use |
|:-------|:-------------|
| LongMemEval (github.com/xiaowu0162/LongMemEval) | P8 LongMemEval-LIGHT pattern adapter |
| MASEval (parameterlab.github.io/MASEval) | P8 MASEval-LIGHT whole-MAS pattern |
| Promptfoo (github.com/promptfoo/promptfoo) | P8 curated 10-vector subset for our threat surface |
| HELM benchmark distribution | P0 calibration framework (40/40/10/10 difficulty distribution pattern) |
| AgentMarketCap 2026 multi-tenant patterns | E9 evidence + D-IH-47-K rationale |

These are **not** copied into the repo. They are cited inline in evidence-matrix and decision-log.

## What is explicitly NOT changed

- `PERSONA_REGISTRY.csv` (I31 P2 stays as authored)
- `SKILL_REGISTRY.csv` (I32 P2 + I45 P3 + I46 P5; PERSONA_SCENARIO_REGISTRY references it via FK only)
- Langfuse setup (I45 telemetry surface untouched)
- Pytest as the unit test runner
- The 5 agents in OpenClaw Control SPA (governance unchanged)
- KiRBe / hlk-erp / boilerplate external repo contracts (I32 P7)
