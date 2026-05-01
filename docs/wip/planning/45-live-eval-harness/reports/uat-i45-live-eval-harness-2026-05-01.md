---
language: en
status: active
intellectual_kind: uat_report
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

# UAT — Initiative 45 (Live Eval Harness Modernisation) closure

**UAT id:** UAT-I45-2026-05-01
**Closes:** Initiative 45 (all 9 phases, P0-P8).
**Date:** 2026-05-01

## Phase verification matrix

| # | Phase | Deliverable | Verification | Status |
|:--:|:------|:-----------|:-------------|:------:|
| P0 | Bootstrap + audit | 5 planning artifacts + audit memo | `validate_planning_traceability`; `audit-current-eval-surface-2026-05-01.md` shipped | PASS |
| P1 | Unify into v2 | `akos/eval_harness/__init__.py` (package) + `v2.py` + `scripts/eval.py` + back-compat shims | `pytest tests/test_eval_harness*.py` 22+5+9 = 36/36; CLI `--mode all` returns 14 rows green | PASS |
| P2 | Cassette record/replay | `cassette.py` + 6 seed cassettes + `record`/`replay` CLI | `pytest tests/test_eval_cassette.py` 16/16; `--mode replay` 6/6 PASS | PASS |
| P3 | Registry-Router gap | `routing_condition` + `tools_required_waived` columns; `akos.skill_router`; `intent.py` enriched | `pytest tests/test_skill_router.py` 24/24; `validate_skill_registry` PASS; `validate_hlk` 152 files PASS | PASS |
| P4 | Cost + latency | `cost_obs.py` + 5 cost_ceiling rows + `--enforce-cost` + `compliance.eval_run` DDL | `pytest tests/test_eval_cost_obs.py` 20/20; `--enforce-cost` returns cost+latency for all 5 skills | PASS |
| P5 | Adversarial cassettes | 12 cassettes (3 vectors × 5 skills) + PII linter + adversarial_floor policy | `pytest tests/test_eval_adversarial.py` 23/23; `--mode adversarial` 12/12 PASS; PII linter 0 findings | PASS |
| P6 | Tier B weekly | `--tier {A,B}` + `--max-spend` + `eval-tier-b.yml` + `eval_harness_smoke` profile | `pytest tests/test_eval_tier_b.py` 11/11; preflight blocks without `AKOS_RECORD_LIVE`; banner with it | PASS |
| P7 | Promotion gate | `promotion.py` + `promote --skill --override --reason` + POL-EVAL-PROMOTION-GATE | `pytest tests/test_eval_promotion.py` 17/17; MADEIRA promote PASS; SHARED-LOCALE FAILs on empty routing_condition | PASS |
| P8 | Tests + UAT + closure | This report + CHANGELOG entry + WIP_DASHBOARD re-render | `pytest tests/`: **1057 passed, 5 skipped, 2 pre-existing failures unrelated to I45** | PASS |

## Test count delta

| Suite | Tests | Status |
|:------|:-----:|:------:|
| tests/test_eval_harness.py (I10) | 5 | unchanged |
| tests/test_madeira_eval_per_skill.py (I32 P9) | 9 | unchanged |
| tests/test_skill_registry.py (I32 P2) | 14 | unchanged |
| tests/test_policy_register.py (I32 P4) | 15 | 1 updated for I45 enum superset |
| **tests/test_eval_harness_v2.py** | **23** | **NEW (P1)** |
| **tests/test_eval_cassette.py** | **16** | **NEW (P2)** |
| **tests/test_skill_router.py** | **24** | **NEW (P3)** |
| **tests/test_eval_cost_obs.py** | **20** | **NEW (P4)** |
| **tests/test_eval_adversarial.py** | **23** | **NEW (P5)** |
| **tests/test_eval_tier_b.py** | **11** | **NEW (P6)** |
| **tests/test_eval_promotion.py** | **17** | **NEW (P7)** |
| **I45-only TOTAL** | **134** | **all PASS** |

Full pytest sweep: **1057 passed, 5 skipped, 2 pre-existing failures** (`tests/validate_configs.py::TestOpenclawConfig::test_validates_via_pydantic` and `test_agents_defaults_sandbox_strict`; both are an `openclaw.json.example` sandbox.mode='all' vs Pydantic literal_error mismatch from before I45 started — not in scope).

## Architectural impact

The 3-system drift is collapsed:
- `scripts/run-evals.py` → shim → `scripts/eval.py --mode rubric`
- `scripts/eval_per_skill.py` → shim → `scripts/eval.py --mode canary`
- `madeira_uat_inproc.py` (TEMP-only) → promoted into `--mode smoke`

The Registry-Router-Evaluator triangle is closed:
- Registry: `SKILL_REGISTRY.csv` extended with `routing_condition` + `tools_required_waived` (the 4-field minimum from the Abstract Algorithms 2026 piece)
- Router: `akos.skill_router` middle-component built; `akos.intent.classify_request` enriched with `candidate_skills` field
- Evaluator: unified `--mode all` runs smoke + canary + rubric in one pass; `--mode replay` adds AgentEval-style cost-controlled regression; `--mode adversarial` adds 3 safety vectors; `promote` enforces the graduation gate

## What is NOT yet shipped (operator-pending or deferred)

- **Live LLM cassettes** — P6 ships infra; first `live_llm` recording happens when operator sets `AKOS_RECORD_LIVE=1` + API keys + records via `scripts/eval.py record --kind live_llm`
- **`compliance.eval_run` mirror DDL** — operator runs `npx supabase db push` to land the migration
- **Tier B GitHub Action** — operator sets `AKOS_TIER_B_ENABLED=true` repo variable + `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` secrets
- **Rolling-baseline cost regression** — waits for `compliance.eval_run` to accumulate 4 weeks of data
- **Inspect AI / Promptfoo / DeepEval adoption** — D-IH-45-A/E alternatives; defer to I47 if needed

## Operator-applied checklist

1. `npx supabase db push` (lands `compliance.eval_run` mirror + `routing_condition` columns)
2. `py scripts/sync_compliance_mirrors_from_csv.py --policy-only` (reseeds the 7 new POLICY_REGISTER rows: 5 cost_ceiling + 1 adversarial_floor + 1 promotion_gate)
3. `gh variable set AKOS_TIER_B_ENABLED -b true` (opt in to weekly Tier B)
4. `gh secret set OPENAI_API_KEY ANTHROPIC_API_KEY LANGFUSE_PUBLIC_KEY LANGFUSE_SECRET_KEY LANGFUSE_HOST` (Tier B model + telemetry credentials)
5. `gh workflow run eval-tier-b -f max_spend_usd=2.50 -f skill_filter=SKILL-MADEIRA-LOOKUP-V1` (verify on-demand budget-capped run before relying on weekly schedule)
6. Optional: extend `pre_commit` profile in `verification-profiles.json` with `eval_harness_smoke` for per-commit Tier A enforcement

## Closure assertion

Initiative 45 is **closed**. All 9 phases shipped. 134 new tests added; 1057 total pass; 0 new failures introduced. The drift documented in P0 audit is operationally collapsed; the Registry-Router gap is closed; cost+latency observability is wired; adversarial and promotion gates are enforced.

Hand-off to I46: I46 P5 (conditional GraphRAG ship) and I46 P6 (cassette wiring for graph_rag) depend on I45 P3 + P2 respectively. Both are now ready to consume.
