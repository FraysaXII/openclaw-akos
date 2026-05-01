---
language: en
status: active
intellectual_kind: phase_report
role_owner: System Owner
area: Tech / Holistik Ops
entity: Holistika Research
authority: Founder + System Owner
last_review: 2026-05-01
artifact_role: governed_evidence
topic_ids:
  - topic_skill_registry
parent_topic: topic_skill_registry
---

# I45 P4 — Cost + latency observability per skill

**Phase:** P4 (per-skill cost+latency in scorecard; POLICY_REGISTER cost_ceiling rows; --enforce-cost mode)
**Closes:** I45 P4 + evidence-matrix E5 (no per-skill cost aggregation) + R-45-3 mitigation foundation.
**Date:** 2026-05-01

## Actions

1. **`config/eval/model-prices.json`** — operator-edited price table. USD per 1k tokens, per model_id. Ships with 5 entries:
   - `deterministic:akos.intent.classify_request` → 0/0
   - `ollama:nomic-embed-text` → 0/0
   - `anthropic:claude-3-5-sonnet-20241022` → $0.003/$0.015
   - `openai:gpt-4o-mini` → $0.00015/$0.0006
   - `openai:gpt-4o` → $0.0025/$0.01
   - Owner: FinOps. Last reviewed: 2026-05-01. Next price review per Anthropic/OpenAI quarterly cycles.

2. **`akos/eval_harness/cost_obs.py`** (~205 lines):
   - `compute_cost_usd(tokens_in, tokens_out, model_id) → float` — uses model-prices table; 0 for unknowns
   - `load_cost_ceilings()` — parses POLICY_REGISTER rows where `policy_class=cost_ceiling`; extracts `max_usd_per_run=<float>` from policy_text
   - `aggregate_skill_cost(skill_id) → CostMetrics` — walks cassettes for the skill; aggregates avg/p95 cost + p50/p95 latency + token totals
   - `evaluate_cost_ceiling(skill_id, metrics, ceiling) → {status, failures, delta_pct, reason}` — applies D-IH-45-D thresholds (PASS <10%, WARN 10-20%, FAIL >20% over ceiling)
   - Soft-fail discipline (R-45-11): every load_* function returns `{}` on missing/malformed input; no fake numbers

3. **POLICY_REGISTER extensions**:
   - `akos/hlk_policy_register_csv.py`: extended `VALID_POLICY_CLASSES` from 4 → 8 with: `cost_ceiling` (P4), `adversarial_floor` (P5), `promotion_gate` (P7), `graph_rag_eligibility` (I46 P5)
   - `POLICY_REGISTER.csv`: 5 NEW `cost_ceiling` rows (one per skill):
     - POL-EVAL-COST-CEILING-MADEIRA-LOOKUP → 0.005/run
     - POL-EVAL-COST-CEILING-ARCHITECT-PLAN → 0.05/run
     - POL-EVAL-COST-CEILING-EXECUTOR-RUN → 0.10/run
     - POL-EVAL-COST-CEILING-VERIFIER-CHECK → 0.02/run
     - POL-EVAL-COST-CEILING-SHARED-LOCALE-DETECT → 0.0/run (rule-based; non-zero = regression)
   - All 5 owned by `Business Controller` (the canonical baseline_organisation role for FinOps responsibilities)

4. **`akos/eval_harness/v2.py:run_canary` extended** with `enforce_cost: bool = False` parameter:
   - When True: per-skill metrics aggregated from cassettes; `evaluate_cost_ceiling` consulted; `cost_ceiling_breach` failures added to row failures; cost_status=FAIL flips overall row status to FAIL
   - When False: cost is still populated in ScoreRow (for visibility) but does not affect row status — only canary-2 accuracy regression does
   - Soft-fail: if `cost_obs` import fails or POLICY_REGISTER missing, falls back to no-cost mode

5. **`scripts/eval.py --enforce-cost` flag** — operator opt-in. Default off so existing CI doesn't break on cost ceiling changes; intentionally opt-in until the rolling baseline mechanism (P6) lands.

6. **`supabase/migrations/20260501050000_i45_eval_run_mirror.sql`** — `compliance.eval_run` mirror:
   - Symmetric to `compliance.validation_runs` (I32 P1) — append-only event log
   - Per-row Scorecard archive: skill_id, mode, status, baseline_pct, current_pct, delta_pp, canary_2_tripped, **cost_usd, latency_ms_p50, latency_ms_p95**, failures[], notes
   - Standard governance posture: deny anon + authenticated; service_role only with INSERT + SELECT (no UPDATE/DELETE)
   - 5 indexes for the most likely query patterns (by time, by skill, by status, by mode, by skill+time+cost)

7. **20 new tests** in `tests/test_eval_cost_obs.py` covering:
   - Model price loading (3 tests: real / missing / malformed)
   - `compute_cost_usd` (3 tests: known model, unknown model, deterministic)
   - `load_cost_ceilings` (2 tests: 5 ceilings parsed; missing file returns empty)
   - `evaluate_cost_ceiling` (6 tests: PASS / WARN at 15%, FAIL at 25%, zero-cost breach, zero-cost OK, no-ceiling SKIP)
   - `aggregate_skill_cost` (2 tests: live Madeira aggregation; unknown skill returns None)
   - End-to-end `run_canary(enforce_cost=True)` (2 tests: passes in clean state; without enforce, cost doesn't flip status)
   - Drift detectors (2 tests: 5 cost_ceiling rows in POLICY_REGISTER; new policy_class enums present)

## Verification

- `py scripts/validate_policy_register.py`: PASS (after fixing owner_role to "Business Controller").
- `py scripts/eval.py --mode canary --enforce-cost --json`: all 5 skills PASS with cost=0.0, p50 latency 425-630ms (deterministic cassette path).
- `py -m pytest tests/test_eval_*.py tests/test_skill_*.py tests/test_policy_register.py tests/test_madeira_eval_per_skill.py`: **126/126 PASS** in 14.1s.

## Sample scorecard with --enforce-cost

```text
| canary | SKILL-MADEIRA-LOOKUP-V1       | PASS | 92.0 | 92.0 | +0.0 |
  cost=0.000000  p50=630.0ms  p95=630.0ms  ceiling-eval: within ceiling (delta -100.0%)
| canary | SKILL-ARCHITECT-PLAN-V1       | PASS | 88.0 | 88.0 | +0.0 |
  cost=0.000000  p50=425.0ms  p95=425.0ms  ceiling-eval: within ceiling (delta -100.0%)
| canary | SKILL-EXECUTOR-RUN-V1         | PASS | 90.0 | 90.0 | +0.0 |
  cost=0.000000  p50=418.0ms  p95=418.0ms  ceiling-eval: within ceiling (delta -100.0%)
| canary | SKILL-VERIFIER-CHECK-V1       | PASS | 95.0 | 95.0 | +0.0 |
  cost=0.000000  p50=428.0ms  p95=428.0ms  ceiling-eval: within ceiling (delta -100.0%)
| canary | SKILL-SHARED-LOCALE-DETECT-V1 | PASS | 98.0 | 98.0 | +0.0 |
  cost=0.000000  p50=439.0ms  p95=439.0ms  ceiling-eval: within zero-cost ceiling
```

## Risks resolved or deferred

- **R-45-3 (Tier B costs balloon on bad models)**: foundation in place. Per-skill ceiling enforcement works; the Tier B kill-switch wires up in P6.
- **R-45-11 (Langfuse rate limit)**: not yet realized — P4 reads cost from cassette summaries (deterministic); Langfuse scrape only triggers when live cassettes exist (P6+).

## What this does NOT do (deferred)

- **No actual Langfuse scrape yet** — cost is computed from cassette summary `tokens_in/tokens_out`, which are 0 for all P2 deterministic cassettes. P6 will populate real numbers when live LLM cassettes exist.
- **Rolling baseline not implemented** — D-IH-45-D specifies "vs 4-week trailing baseline"; P4 enforces vs the static POLICY_REGISTER ceiling. Rolling baseline lands in P6 once `compliance.eval_run` has historical data.
- **No CI workflow yet** (P6 ships `.github/workflows/eval-tier-b.yml`).
- **`compliance.eval_run` mirror DDL not yet applied** — operator runs `npx supabase db push` post-merge.

## Operator-applied steps

1. **Apply the migration**: `npx supabase db push` lands the `compliance.eval_run` mirror.
2. **Apply the I45 P3 column migration** if not already applied (from P3 commit).
3. **Reseed POLICY_REGISTER mirror**: `py scripts/sync_compliance_mirrors_from_csv.py --policy-only` (or run the existing reseed pipeline; the 5 new cost_ceiling rows will be upserted alongside the I32 baseline).
4. **Optional**: review `config/eval/model-prices.json` quarterly per Anthropic/OpenAI billing cycles.

## Next phase

P5 — Adversarial / safety canaries. New cassette type `tests/evals/cassettes/adversarial/<skill_id>/`. 3 vectors per D-IH-45-E: prompt injection + brand jargon + PII. Wire to existing `madeira_internal_tool_leak`, `madeira_pseudo_hlk_path_leak`, `madeira_suspect_uuid_hallucination` alerts in `config/eval/alerts.json`. New policy `pol_eval_adversarial_floor`.
