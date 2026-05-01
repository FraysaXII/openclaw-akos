---
language: en
status: active
initiative: 45-live-eval-harness
report_kind: evidence-matrix
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-01
---

# Initiative 45 — Evidence Matrix

Evidence rows justify each phase's work with observed-state observations. Codebase evidence is collected from a 2026-04-30 read-only sweep (cursor plan §"Codebase truth"); field evidence cites the 2026 sources from §"Field grounding".

| ID | Observation | Source | Impact | Resolved by |
|:---|:------------|:-------|:-------|:------------|
| **E1** | Three eval entry points live in three different files with three different result formats: [`scripts/run-evals.py`](../../../../scripts/run-evals.py), [`scripts/eval_per_skill.py`](../../../../scripts/eval_per_skill.py), and `%TEMP%/madeira_uat_inproc.py` (built ad-hoc for D-IH-32-Q9). | Read-only sweep 2026-04-30 | Operator drift: every new canary deepens divergence; CI runs all three but no consolidated view | P1 unify into `scripts/eval.py` |
| **E2** | `SKILL_REGISTRY.csv` (5 rows, I32 P2) carries `axes_consumed`, `tools_required`, `agents_supported`, `langfuse_trace_pattern` — all routing-relevant — but [`akos/intent.py`](../../../../akos/intent.py) reads `config/intent-exemplars.json` instead. The Registry-Router gap. | Read-only sweep + grep `intent.py` for `SKILL_REGISTRY` (zero hits) | Half a control plane built; new skills land in CSV but never reach the router | P3 refactor intent.py |
| **E3** | Drift between `SKILL_REGISTRY.tools_required` (Cursor-style names like `Shell;Read;Write`) and `agent-capabilities.json` (gateway tool ids like `shell_exec`, `write_file`). Documented in [`reports/p2-skill-registry-2026-04-30.md`](../32-holistik-ops-maturation/reports/p2-skill-registry-2026-04-30.md) but unaddressed. | I32 P2 report | A new skill author can't tell which name is canonical → silent capability mismatch | P3 reconciliation + migration validator |
| **E4** | `config/eval/alerts.json` defines `madeira_internal_tool_leak`, `madeira_pseudo_hlk_path_leak`, `madeira_suspect_uuid_hallucination` — three alerts with no exercising probes. We'd find a regression at customer-report time, not CI time. | Read of `config/eval/alerts.json` | False sense of coverage; alerts that never fire because nothing pokes them | P5 adversarial cassettes |
| **E5** | Langfuse traces have `tokens_in`, `tokens_out`, `latency_ms` per span; nothing aggregates them by `skill_id`. We cannot answer "which skill costs the most" or "is SKILL-X getting slower" today. | Read of `scripts/langfuse_list_traces_by_tag.py` (lists, doesn't aggregate) | No cost-aware testing; no skill-level latency tracking | P4 scorecard cost+latency |
| **E6** | Skill promotion (e.g., `tenant_scope='shared'` → tenant-specific) is honour-based. No script blocks the CSV edit. | Inspection of validator graph (`scripts/validate_skill_registry.py` only checks schema, not promotion eligibility) | In multi-tenant land (I34), an undertested skill landing on a tenant could leak governance metadata across tenant boundaries | P7 promotion gate |
| **E7** | Tier B (live LLM) is "opt-in per worker" per `tests/evals/README.md` — no scheduled run, no model-tier matrix, no cost ceiling kill switch. | Read of `tests/evals/README.md` Tier A/B section | Tier B has been built but is effectively dormant; we have no live regression detection | P6 Tier B weekly schedule |
| **E8** | Per-skill scorecards live in 5 separate JSON files in `config/eval-baselines/`. Aggregation requires reading all 5 + correlating with SKILL_REGISTRY rows. | Read of `config/eval-baselines/` | Operator can't scan-at-a-glance; future tenants will need per-tenant scorecards (impractical with 5 files × N tenants) | P4 unified scorecard format + new `compliance.eval_run` mirror |
| **E9** | Replay-based eval is field-standard (AgentEval, MASEval, DeepEval recorded mode) but not adopted at AKOS. Every test run requires recomputing trajectories from scratch. | Cursor plan §"Field grounding" + 2026 web searches | We pay LLM cost on every CI run; deterministic replay would cut cost by ~90% per the AgentEval whitepaper | P2 cassette record-and-replay |
| **E10** | `routing_condition` is in the Abstract Algorithms 4-field minimum registry contract but missing from `SKILL_REGISTRY.csv`. We can't express "this skill is only eligible for low-risk intents" today. | Cursor plan §"Field grounding" + read of SKILL_REGISTRY.csv header | When more than one skill matches the intent, we have no policy filter to choose | P3 add `routing_condition` column |
| **E11** | The "intent classifier hybrid embed+regex" path (`akos/intent.py`) does not log which path won (embed vs regex vs escalation override). We can't measure routing-classifier accuracy or detect drift. | Read of `intent.py` `classify_request()` | Routing decisions are not traceable to a specific resolver; debugging routing regressions requires re-execution with print-statements | P3 + P4 add `routing_resolver` to trace metadata |
| **E12** | I32 P9 introduced 5 canaries (bootstrap drift, eval regression >2pp, Langfuse trace shape >3 skills, validator FK reject, UAT smoke fallback) — only canary 2 has a runner script (`eval_per_skill.py`); 1 + 3 + 4 + 5 are documented but not exercised in CI. | I32 P9 report | 4/5 canaries are aspirational; the eval surface advertises coverage that doesn't exist | P1 unify will surface them; P2 + P5 will exercise them |
| **E13** | Madeira UAT D-IH-32-Q9 (post-I32 SKILL_REGISTRY landing, 2026-05-01) confirmed runtime unchanged (8/8 in-process probes, classify_request 5/5 with `orchestrator-fallback=0/5`). The script lives in `%TEMP%`, not promoted. | [`reports/madeira-runtime-uat-2026-05-01.md`](../32-holistik-ops-maturation/reports/madeira-runtime-uat-2026-05-01.md) | Good evidence-pattern lost to `%TEMP%` cleanup; should be promoted as a `--mode smoke` runner | P1 promotes it as the smoke-mode template |

## Cross-references to other initiatives

- **Initiative 10** — built the original `akos/eval_harness` + Tier A/B split. We extend, not replace.
- **Initiative 32 P1** — built the validator graph dispatcher + `compliance.validation_runs` mirror. P4 here adds the symmetric `compliance.eval_run` mirror.
- **Initiative 32 P2** — built `SKILL_REGISTRY.csv` (E2 + E3 source).
- **Initiative 32 P9** — built per-skill scorecard for canary 2 (E12 source).
- **Initiative 26** — quarterly `service_role` rotation runbook → POLICY_REGISTER pattern reused for cost_ceiling rows in P4.
- **Initiative 46 P3** — GraphRAG PoC will use this harness for A/B comparison.
- **Initiative 34 (future)** — multi-tenancy will consume the promotion gate built in P7.
