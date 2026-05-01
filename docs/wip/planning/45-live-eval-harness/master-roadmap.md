---
language: en
status: active
initiative: 45-live-eval-harness
report_kind: master-roadmap
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-01
---

# Initiative 45 — Live Eval Harness Modernisation: 9-phase unification + cost + adversarial pass

**Folder:** `docs/wip/planning/45-live-eval-harness/`
**Status:** Open (started 2026-05-01)
**Authoritative Cursor plan:** `~/.cursor/plans/i45-i46_eval_and_neo4j_6a72e6d7.plan.md`
**Predecessor:** [Initiative 10 — Madeira Eval Hardening](../10-madeira-eval-hardening/master-roadmap.md) (closed 2026-04-15) and [Initiative 32 P9 — Madeira eval canaries](../32-holistik-ops-maturation/reports/p9-madeira-eval-canaries-2026-04-30.md).
**Sister initiative:** [Initiative 46 — Neo4j Strategic Posture](../46-neo4j-strategic-posture/master-roadmap.md) (parallel, converges at I45 P6).

## Outcome

Collapse the three drifting eval surfaces — [`akos/eval_harness`](../../../../akos/eval_harness) (I10 manifest+rubric), [`scripts/eval_per_skill.py`](../../../../scripts/eval_per_skill.py) (I32 P9 canaries), and the inproc UAT pattern (`%TEMP%/madeira_uat_inproc.py` for D-IH-32-Q9) — into one governed harness, then add what 2026 production agent systems take for granted: trace record-and-replay, registry-driven routing, per-skill cost+latency observability, adversarial canaries, and a tooling-enforced skill promotion gate.

The phrase that triggered this initiative: *"our way of testing is dull compared to what we expect to do now"* (operator, 2026-04-30 mid-I32).

## Why now

- **3 eval systems with no shared schema** — every new canary introduced in I32 deepens the drift.
- **Registry exists, router doesn't consult it** — `SKILL_REGISTRY.csv` (I32 P2) carries `axes_consumed`, `tools_required`, `agents_supported`, `langfuse_trace_pattern` but [`akos/intent.py`](../../../../akos/intent.py) reads `config/intent-exemplars.json` instead. Half a control plane built; nobody flipping the switch.
- **No cost visibility per skill** — Langfuse traces have token counts; nothing aggregates them by `skill_id`. We can't answer "which skill costs the most" today.
- **No adversarial floor** — `config/eval/alerts.json` has 3 Madeira-specific alert rules but no exercising probes; we'd find a prompt-injection regression at customer-report time, not CI time.
- **Skill promotion is honour-based** — nothing prevents a `tenant_scope='shared'` skill from graduating without a green eval; in the multi-tenant world (I34) that becomes an outage vector.
- **Field has converged on patterns we haven't adopted** — AgentEval's record-replay (cost-controlled CI), MASEval's whole-system framing, Abstract Algorithms' three-plane registry+router+evaluator. Cited inline in the cursor plan §"Field grounding".

## Scope decisions

| In scope | Out of scope |
|:---|:---|
| Unified [`scripts/eval.py`](../../../../scripts/eval.py) CLI with 4 modes (rubric / replay / canary / smoke) | Replacing pytest as the unit-test runner |
| Trace record-and-replay cassettes under `tests/evals/cassettes/<skill_id>/` | Replacing Langfuse as the trace SoT |
| `routing_condition` column on `SKILL_REGISTRY.csv` + intent.py refactor | Building a UI for eval results (CLI + markdown is enough) |
| Reconcile `tools_required` (Cursor names) vs `agent-capabilities.json` (gateway names) drift | Multi-tenant skill scoping — that's [Initiative 34](#) |
| New POLICY_REGISTER rows: `policy_class=cost_ceiling` per skill | Vision / audio eval (out of agent scope) |
| Adversarial cassettes: prompt injection + brand jargon + PII (the 3 vectors that map to existing alerts.json rules) | Promptfoo's full 500-vector suite (D-IH-45-E alternative; revisit at I47) |
| Tier B GitHub Action: weekly + on-demand, model-tier matrix (1 cheap + 1 flagship) | Live continuous eval (cost-prohibitive at our scale) |
| `scripts/eval.py promote --skill <id>` enforces graduation criteria | Auto-promotion based on metrics (operator approval gates promotion) |
| New `compliance.eval_run` Supabase mirror (parallel to `compliance.validation_runs` from I32 P1) | Public eval leaderboard (governance-internal only) |
| Closes the loop: eval scorecard feeds back into Registry's `lifecycle_status` | Initiative 46 GraphRAG eval surface (lives in I46 P6 + uses this harness) |

## Asset classification (per [`PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md))

| Class | Paths | Rule |
|:------|:------|:-----|
| **New canonical (planning)** | `docs/wip/planning/45-live-eval-harness/{master-roadmap,decision-log,asset-classification,evidence-matrix,risk-register}.md` + `reports/` | Standard six-artifact contract |
| **New canonical (registry column)** | `routing_condition` on `SKILL_REGISTRY.csv` (P3) | Required by the Abstract Algorithms 4-field minimum registry contract |
| **New canonical (registry rows)** | POLICY_REGISTER rows: `pol_eval_cost_ceiling_<skill>`, `pol_eval_promotion_gate`, `pol_eval_adversarial_floor` (P4, P5, P7) | Cost + safety policies have policy_id traceability |
| **New canonical (mirror)** | `compliance.eval_run` mirror (Supabase migration in P4) | Operational mirror, RLS deny anon/auth, server-only service_role |
| **New mirrored / derived** | `tests/evals/cassettes/<skill_id>/*.jsonl` (P2), `tests/evals/cassettes/adversarial/<skill_id>/*.jsonl` (P5) | Recorded, not authored. Recording requires `AKOS_RECORD_LIVE=1` |
| **New scripts** | `scripts/eval.py` (P1), record/replay/promote subcommands (P2, P7) | Unified CLI; backward-compat shims for old entry points |
| **Modified canonical** | `akos/intent.py`, `config/intent-exemplars.json` (P3) | Router refactor — registry-first, exemplar-fallback |
| **New CI** | `.github/workflows/eval-tier-b.yml` (P6) | Weekly Tier B; cost ceiling kill switch |

## Phase plan (9 phases, ~3 weeks elapsed time at 1 phase/2 days)

| # | Phase | Output | Dependency |
|:--:|:------|:-------|:-----------|
| P0 | Bootstrap + audit | This initiative folder + 5 artifacts + `audit-current-eval-surface.md` evidence | — |
| P1 | Unify into `akos/eval_harness/v2` | `scripts/eval.py` with 4 modes + back-compat shims | P0 |
| P2 | Trace record-and-replay | `tests/evals/cassettes/<skill_id>/` + `record` / `replay` subcommands | P1 |
| P3 | Close registry-router gap | `routing_condition` column + intent.py refactor + tools_required reconciliation | P1 |
| P4 | Cost + latency per skill | Scorecard extension + new POLICY_REGISTER cost_ceiling rows + `compliance.eval_run` mirror | P1 + P3 |
| P5 | Adversarial canaries | `tests/evals/cassettes/adversarial/` + alerts.json wiring | P2 |
| P6 | Tier B weekly | `.github/workflows/eval-tier-b.yml` + cost ceiling kill switch | P2 + P4 |
| P7 | Promotion gate | `scripts/eval.py promote --skill <id>` + 4-criteria check | P3 + P4 + P5 + P6 |
| P8 | Tests + UAT + closure | `tests/test_eval_harness_v2.py` + UAT report + CHANGELOG + WIP_DASHBOARD | All |

## Verification matrix

| Check | Profile | Cadence |
|:------|:--------|:--------|
| `validate_hlk.py` (full vault) | `pre_commit` | Every commit |
| Per-skill scorecard `--mode canary` (canary 2 from I32 P9) | `pre_commit` | Every commit |
| Replay cassettes `--mode replay` for each `SKILL_REGISTRY` row | `pre_commit` | Every commit |
| Adversarial cassettes pass | `pre_commit` | Every commit |
| Tier B live regression | `eval_tier_b_weekly` | Weekly + on-demand |
| Cost ceiling enforcement | `pre_commit` | Every commit |
| `intent.py` registry-first (no exemplar-only routing) | new test in P3 | Every commit |

## Success metrics (closure conditions)

- 3 eval systems collapsed into 1 CLI (verified: `scripts/eval*.py` count = 1; `scripts/run-evals.py` and `scripts/eval_per_skill.py` are shims)
- ≥5 skills with replay cassettes (one per current `SKILL_REGISTRY` row)
- Cost-per-skill visible in scorecard (Langfuse-scraped `tokens_in/out`, `usd_estimate`)
- Adversarial cassette suite ≥10 probes
- `scripts/eval.py promote` enforces 4-criteria graduation
- 1 weekly Tier B run executed and archived to `compliance.eval_run`
- `intent.py` consults `SKILL_REGISTRY.csv` before exemplars (verified by new test)
- Drift between `tools_required` and `agent-capabilities.json` either reconciled or explicitly waived per skill (zero unwaived mismatches)

## Risks + rollback

See [`risk-register.md`](risk-register.md). Phase rollback strategy: every phase ships a backward-compat shim (P1 in particular); revert is `git revert` of the phase commit.

## Reporting artifacts

- `reports/p<N>-*-YYYY-MM-DD.md` per phase (per AKOS convention from I22+)
- `reports/audit-current-eval-surface-2026-05-01.md` (I45 P0 evidence)
- `reports/uat-i45-live-eval-harness-2026-05-XX.md` (P8 closure)

## Cross-cutting

- Decision IDs: `D-IH-45-A` through `D-IH-45-G` (7 seeded; user-ratified at greenlight 2026-05-01).
- All vault documents carry `language: en` frontmatter (per [`SOP-HLK_LOCALISATION_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/SOP-HLK_LOCALISATION_001.md)).
- WIP_DASHBOARD picks this row up automatically once `master-roadmap.md` is committed (renderer scans frontmatter).
- CHANGELOG entry on closure (P8).

## What this is NOT

- Not a rewrite of Langfuse, pytest, or `akos/eval_harness` — extension only.
- Not multi-tenant scoping (I34).
- Not a public eval leaderboard.
- Not a replacement of MADEIRA's intent classifier — refactor, not rebuild.
