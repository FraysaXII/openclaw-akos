---
language: en
status: active
initiative: 45-live-eval-harness
report_kind: asset-classification
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-01
---

# Initiative 45 — Asset Classification

Per [`PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md), every artifact below is classified as **canonical** (authored, SSOT in git), **mirrored / derived** (rebuildable from canonical), or **reference-only** (not governed).

## New canonical (planning artifacts)

| Path | Class | Owner | Validator |
|:-----|:------|:------|:----------|
| `docs/wip/planning/45-live-eval-harness/master-roadmap.md` | canonical | Founder + System Owner | `validate_planning_traceability` |
| `docs/wip/planning/45-live-eval-harness/decision-log.md` | canonical | Founder + System Owner | `validate_planning_traceability` |
| `docs/wip/planning/45-live-eval-harness/evidence-matrix.md` | canonical | Founder + System Owner | none (prose) |
| `docs/wip/planning/45-live-eval-harness/asset-classification.md` (this file) | canonical | Founder + System Owner | `validate_planning_traceability` |
| `docs/wip/planning/45-live-eval-harness/risk-register.md` | canonical | Founder + System Owner | `validate_planning_traceability` |

## New canonical (registry surface)

| Path | Class | Owner | Validator |
|:-----|:------|:------|:----------|
| `routing_condition` column added to `docs/references/hlk/compliance/dimensions/SKILL_REGISTRY.csv` (P3) | canonical | System Owner | `scripts/validate_skill_registry.py` (extended) |
| `retrieval_mode` column reserved for I46 P5 use | canonical (placeholder) | System Owner | extended in I46 |
| New POLICY_REGISTER rows: `pol_eval_cost_ceiling_<skill_id>` per skill (P4) | canonical | FinOps + System Owner | `scripts/validate_policy_register.py` |
| New POLICY_REGISTER row: `pol_eval_promotion_gate` (P7) | canonical | System Owner | `scripts/validate_policy_register.py` |
| New POLICY_REGISTER row: `pol_eval_adversarial_floor` (P5) | canonical | System Owner + Brand Manager | `scripts/validate_policy_register.py` |
| New `policy_class` enum value: `cost_ceiling` (extends I32 P4 set: rls / service_role_rotation / redaction / pii_scope) | canonical | System Owner | `scripts/validate_policy_register.py` (extended enum check) |

## New mirrored / derived (Supabase mirrors)

| Path | Class | Source of truth | Mirror table |
|:-----|:------|:----------------|:-------------|
| `supabase/migrations/<ts>_i45_eval_run_mirror.sql` (P4) | canonical migration | the migration itself | `compliance.eval_run` |
| `compliance.eval_run` table | mirrored | (operational; no canonical CSV — runs are events) | RLS deny anon/auth; service_role insert + select |

## New mirrored / derived (cassettes)

| Path | Class | Recording authority | Replay reproducibility |
|:-----|:------|:--------------------|:-----------------------|
| `tests/evals/cassettes/<skill_id>/*.jsonl` (P2) | mirrored / derived | `AKOS_RECORD_LIVE=1 py scripts/eval.py record --skill <id>` | Deterministic; replay does not require live LLM |
| `tests/evals/cassettes/adversarial/<skill_id>/*.jsonl` (P5) | mirrored / derived | Same as above + `--adversarial` flag | Same |
| Per-cassette frontmatter: `last_recorded`, `recorded_by`, `model_id`, `model_tier`, `skill_id`, `golden_assertion` | required schema | `scripts/eval.py record` writes; `scripts/eval.py replay` reads | Staleness alarm: 90 days |

## New scripts

| Path | Class | Purpose |
|:-----|:------|:--------|
| `scripts/eval.py` (P1) | canonical | Unified CLI: `--mode {rubric, replay, canary, smoke}`, plus `record` / `replay` / `promote` subcommands |
| `scripts/eval_record.py` (P2) | canonical | Cassette recorder; alias for `scripts/eval.py record` |
| `scripts/eval_promote.py` (P7) | canonical | Skill promotion gate; alias for `scripts/eval.py promote` |
| `scripts/run-evals.py` (existing, I10) | canonical (back-compat shim, P1) | Calls `scripts/eval.py --mode rubric` after deprecation warning; stays for 1 release cycle |
| `scripts/eval_per_skill.py` (existing, I32) | canonical (back-compat shim, P1) | Calls `scripts/eval.py --mode canary` after deprecation warning; stays for 1 release cycle |

## Modified canonical

| Path | Change | Phase |
|:-----|:-------|:------|
| `akos/intent.py` | `classify_request()` consults `SKILL_REGISTRY.csv` first; falls back to embeddings/regex | P3 |
| `config/intent-exemplars.json` | Stays as fallback; cross-referenced by SKILL_REGISTRY rows where exemplar coverage is intentional | P3 |
| `config/agent-capabilities.json` | Tool name reconciliation; per-tool waiver column for documented `tools_required` mismatches | P3 |
| `tests/evals/README.md` | Updated with v2 CLI; Tier B promoted from "opt-in" to "weekly + on-demand" | P6 |
| `docs/wip/planning/README.md` | New row for I45 | P0 |
| `docs/wip/planning/WIP_DASHBOARD.md` | Re-rendered | P0 + P8 |
| `CHANGELOG.md` | Closure entry | P8 |

## New CI

| Path | Class | Trigger |
|:-----|:------|:--------|
| `.github/workflows/eval-tier-b.yml` (P6) | canonical | `cron: '0 6 * * 1'` (weekly Monday 06:00 UTC) + `workflow_dispatch` |
| `.github/workflows/eval-tier-b.yml` matrix: `[ollama-nomic, <flagship>]` | canonical | operator-set flagship in repo secrets |

## Reference-only / external (cited but not authored)

| Source | Citation use |
|:-------|:-------------|
| **AgentEval** (github.com/AgentEvalHQ/AgentEval) | Cassette pattern inspiration (Trace Record & Replay) |
| **MASEval** (parameterlab.github.io/MASEval) | Whole-MAS framing for Tier B model matrix |
| **Abstract Algorithms** "Skill Registries, Routing Policies, Evaluation" (Mar 2026) | 4-field registry minimum contract → `routing_condition` column rationale |
| **Inference.net** "LLM Evaluation Tools 2026" | D-IH-45-A alternative analysis (Inspect AI vs DeepEval vs native) |
| **Braintrust** "7 best LLM tracing tools 2026" | Multi-agent trace correlation requirement |
| **Promptfoo** docs | Adversarial vector taxonomy reference (D-IH-45-E) |

These are **not** copied into the repo. They are cited inline in evidence-matrix and decision-log.

## What is explicitly NOT changed

- Langfuse stays the live trace surface.
- Pytest stays the unit test runner.
- `akos/eval_harness` interior is extended, not rewritten.
- I32-era `compliance.validation_runs` mirror is untouched (parallel to new `compliance.eval_run`).
- All existing `prompts/`, `config/workspace-scaffold/`, `config/agent-capabilities.json` consumers keep working through P3's reconciliation (waiver column for documented mismatches).
