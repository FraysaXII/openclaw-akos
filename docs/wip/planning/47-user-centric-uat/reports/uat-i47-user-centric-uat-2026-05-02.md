---
language: en
status: closed
initiative: 47-user-centric-uat
report_kind: uat
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-02
---

# I47 — User-centric UAT modernisation: Closure UAT (2026-05-02)

> **Status: CLOSED.** All 16 phases shipped (P0-P15). Branch `i47-user-centric-uat` ready to push.

## What we built

The persona-driven UAT scenario library + scoring infrastructure that the I46 closure UAT showed we were missing.

### Numbers

- **326 scenarios** across all 16 PERSONA_REGISTRY archetypes (operator + Tier-1 ×4 + Tier-2 ×8 + Tier-3 ×4) plus cross-cutting (cross_axis, adversarial, benchmark, recovery)
- **17 distinct personas** exercised (16 + OPERATOR pseudo)
- **Difficulty distribution: 11/41/40/8** (within ±5pp of D-IH-47-C target 10/40/40/10)
- **8 new akos modules / scripts** (`hlk_persona_scenario_csv`, `eval_harness/persona`, `eval_harness/judge`, `eval_harness/eval_run_writer`, plus 4 new scripts)
- **5 new Supabase migrations** applied to MasterData
- **3 new Cursor-style POLICY_REGISTER rows** + 1 new TOPIC_REGISTRY row
- **4 tech debt items** closed from I46 UAT
- **4 Tier-1 personas** with persona-conditioned MADEIRA prompts
- **Tier B 4-D matrix** (10 default cells; persona × model_tier; Tier-2/3 opt-in only)

### Test counts (all green at closure)

| Phase | Test file | Count |
|:---|:---|:---:|
| P1 | `tests/test_persona_scenario_registry.py` | 21 |
| P9 | `tests/test_recovery_chaos_runner.py` | 10 |
| P10 | `tests/test_eval_persona_calibration.py` | 25 |
| P11 | `tests/test_persona_overlay.py` | 22 |
| P12 | `tests/test_eval_judge.py` | 24 |
| P13 | `tests/test_i47_p13_tech_debt.py` | 12 |
| P14 | `tests/test_i47_p14_tier_b_persona_matrix.py` | 20 |
| **TOTAL I47-new** | | **134** |
| Cumulative repo: `py -m pytest --ignore=tests/validate_configs.py` | | **1180 passed / 5 skipped / 0 failed** |

## Verification stack (every layer green at closure)

### Schema + governance
- `py scripts/validate_hlk.py` → **OVERALL: PASS** (now includes `PERSONA_SCENARIO_REGISTRY: PASS` + `TOPIC_REGISTRY: PASS` (28 rows) + `POLICY_REGISTER: PASS` (25 rows incl. 3 new judge_threshold))
- `py scripts/validate_persona_scenario_registry.py` → PASS (326 rows; 17 personas; distribution within tolerance)

### Eval harness
- `py scripts/eval.py --mode all` → overall_status PASS (14 rows: 5 canary skills + 6 smoke probes + 2 rubric suites + 1 replay)
- `py scripts/eval.py --calibrate` → emits 17-row calibration table with `__overall__` first
- `py scripts/calibrate_scenarios.py` → writes paired md+json artifacts

### Persona-conditioned prompts
- `py scripts/assemble-prompts.py --persona PERSONA-INVESTOR-COLD --variant standard --dry-run` → MADEIRA standard 18842 chars (1158 headroom under 20000)
- All 4 Tier-1 personas under bootstrapMaxChars

### Recovery + chaos
- `py scripts/recovery_chaos_runner.py --scenario neo4j-password-rotation` → REFUSED at gate 1 (AKOS_REAL_CHAOS_OK not set)
- All 4 safety gates (env opt-in, host forbidden-list, operator confirmation, Aura key) tested independently

### Trigger watcher
- `py scripts/agent_memory_trigger_watcher.py` → emits 3-trigger report; trigger 1 NOT FIRED, triggers 2/3 AWAITING

### Supabase
- All 5 migrations applied to MasterData via `npx supabase db push --linked`
- 3 judge_threshold rows reseeded to `compliance.policy_register_mirror`
- `compliance.persona_scenario_registry_mirror` table created (RLS active)
- `compliance.eval_run` extended with persona_id + difficulty_class + scenario_class + judge_scores JSONB columns + 4 new partial indexes

## Pre-existing failures (not I47-induced)

Two failures in `tests/validate_configs.py` predate I47 and concern `openclaw.json` (operator-local; gitignored):
- `TestOpenclawConfig::test_validates_via_pydantic` — schema mismatch (`sandbox.mode='all'` vs allowed `'off'|'strict'`)
- `TestOpenclawConfig::test_agents_defaults_sandbox_strict` — same root cause

Recommended action: operator-local fix (edit `~/.openclaw/openclaw.json` `agents.defaults.sandbox.mode` to `strict`); not blocking I47 closure.

## Lessons + follow-ups feeding I48+

1. **R-47-2 (calibration subjectivity) is real and visible.** P10 calibration baseline showed 13/17 personas drift outside ±5pp tolerance even though `__overall__` passes. Cumulative target met but per-persona distribution shifts when cross-cutting scenarios attribute to specific personas. Operator path: warn-only (default) OR `--hard-fail-on-drift` for tightened CI.
2. **Persona overlay budget is tight.** MADEIRA standard at 19731 chars baseline left only ~270 chars of overlay budget; we resolved by swapping out OVERLAY_HLK_GRAPH (1241 chars) when persona is set. Future overlay additions to MADEIRA_BASE will need similar trade-off discipline.
3. **Cost envelope of P14 + P12 is ~$77/week worst case.** Operator should budget accordingly when activating Tier B 4-D matrix with judge active. The MAX_PERSONA_USD + AKOS_JUDGE_COST_CAP envs cap exposure.
4. **Real-chaos runner is gated and PLANNED-ONLY for live rotation.** Live rotation path needs operator approval + Aura API contract pinning before first burn (D-IH-47-L follow-up).
5. **GraphRAG conditional ship (I46 P5) is now testable per-persona.** P3-P5 give us the persona-shaped queries to evaluate `retrieval_mode=graph_rag` regression vs operator-shaped baseline. I46 P5 ship-or-no-ship decision can now be made with real persona evidence.
6. **All 16 PERSONA_REGISTRY archetypes are exercised in eval.** Scenarios reference 17 distinct personas (16 + OPERATOR pseudo). The persona dimension is now governance-canonical AND eval-canonical AND prompt-canonical (Tier-1 only on prompt side; Tier-2/3 deferred per scope cap).

## Operator follow-ups (post-PR-merge)

| Item | What | When |
|:---|:---|:---|
| **OPS-47-1** | Push branch `i47-user-centric-uat` to remote | Now |
| **OPS-47-2** | Open PR for review (or admin-merge) | Now |
| **OPS-47-3** | Set Tier B repo secrets if not already set: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `LANGFUSE_*`, `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` | Pre-first-Tier-B-run |
| **OPS-47-4** | Live MADEIRA + AKOS dashboard UAT (P15 final demo) | Operator-on-demand |
| **OPS-47-5** | Run `py scripts/sync_hlk_neo4j.py` live to verify P13 item 1 closes the drift canary catch (csv=N neo4j=N for all 10 dimensions) | When operator wants the canary green |
| **OPS-47-6** | Review the 13 personas outside calibration tolerance; decide rebalance vs accept (R-47-2) | At I47 close + 30d |
| **OPS-47-7** | Approve first real-chaos run when ready (test instance only; D-IH-47-L) | Operator-on-demand |
| **OPS-47-8** | Approve LLM-judge live mode + pin model_id (D-IH-47-J + R-47-10) | Operator-on-demand |

## Cross-references

- All 16 phase reports in `docs/wip/planning/47-user-centric-uat/reports/`
- Decision log: `docs/wip/planning/47-user-centric-uat/decision-log.md` (12 decisions D-IH-47-A..L)
- Risk register: `docs/wip/planning/47-user-centric-uat/risk-register.md` (14 risks; all mitigated or noted)
- Cursor plan: `~/.cursor/plans/i47_user-centric_uat_a51d490f.plan.md`
