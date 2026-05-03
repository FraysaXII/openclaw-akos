---
language: en
status: closed
initiative: 50-live-cycle-closure
report_kind: phase-report
phase: P4
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# I50 P4 — First Tier-B controlled cell smoke

## Outcome

Tier-B infrastructure exercised end-to-end across three runs; **`overall_status: pass`** for all. Cost ceiling **$5.00 per run** announced + honored (no breach; **$0.00 actual spend**). The 2-cell smoke (D-IH-50-C: `(OPERATOR, hard)` + `(PERSONA-INVESTOR-COLD, hard)`) returned `rows_after_filter=0` because **`tests/evals/cassettes/` is empty** — persona-conditioned scenarios need cassette wiring before they exercise replay/canary/rubric modes against scenario data. That wiring is the I51 P3 deliverable. New OPS follow-up captured: **OPS-50-1 — Tier-B persona cassette population** (deferred to I51 P3).

## Commands

```text
$env:AKOS_RECORD_LIVE = "1"
$env:MAX_TIER_B_USD   = "5"
```

### Cell 0 — Tier-B baseline (no filter; broader smoke)

```text
py scripts/eval.py --tier B --mode all --max-spend 5 --judge-cost-cap 0.01 --no-judge \
                   --no-exit-on-fail --json
```

| Field | Value |
|:---|:---|
| overall_status | **pass** |
| modes_run | `smoke`, `canary`, `rubric` (all three dispatched) |
| rows | **14** |
| all rows status | PASS |
| skill_ids covered | `SKILL-ARCHITECT-PLAN-V1`, `SKILL-EXECUTOR-RUN-V1`, `SKILL-MADEIRA-LOOKUP-V1`, `SKILL-SHARED-LOCALE-DETECT-V1`, `SKILL-VERIFIER-CHECK-V1`, `classify_request_smoke`, `csv_load:POLICY_REGISTER.csv`, `csv_load:REPO_HEALTH_SNAPSHOT.csv`, `csv_load:SKILL_REGISTRY.csv`, `csv_load:TOUCHPOINT_KIT_CELL_REGISTRY.csv`, `env_bootstrap`, `intent_5_probes`, `suite:madeira-operator-coverage`, `suite:pathc-research-spine` |
| `eval_run_writer.skipped` | 14 (rows would have written to `compliance.eval_run` mirror; no Supabase service-role configured locally) |
| `eval_run_writer.errors` | 0 |
| `eval_run_writer.written` | 0 |
| elapsed | 968 ms |

### Cell 1 — `(OPERATOR, hard)`

```text
py scripts/eval.py --tier B --mode all --persona OPERATOR --difficulty hard \
                   --max-spend 5 --judge-cost-cap 0.01 --no-judge --no-exit-on-fail --json
```

| Field | Value |
|:---|:---|
| overall_status | **pass** |
| modes_run | `smoke`, `canary`, `rubric` |
| `i47_filter.rows_after_filter` | **0** |
| `eval_run_writer` | 0 errors / 0 skipped / 0 written |
| elapsed | 1035 ms |

### Cell 2 — `(PERSONA-INVESTOR-COLD, hard)`

```text
py scripts/eval.py --tier B --mode all --persona PERSONA-INVESTOR-COLD --difficulty hard \
                   --max-spend 5 --judge-cost-cap 0.01 --no-judge --no-exit-on-fail --json
```

| Field | Value |
|:---|:---|
| overall_status | **pass** |
| modes_run | `smoke`, `canary`, `rubric` |
| `i47_filter.rows_after_filter` | **0** |
| `eval_run_writer` | 0 errors / 0 skipped / 0 written |
| elapsed | 730 ms |

## What Tier-B preflight + cost guard verified

- `--tier B` engages the Tier-B preflight log line: `[eval --tier B] Live regression mode. Cost ceiling: $5.00 per run.`
- Without `AKOS_RECORD_LIVE=1`, the preflight refuses (cost-control guard, scripts/eval.py:326-328) — verified by separate dry-run during P4 setup.
- `--max-spend 5` honors `POL-EVAL-COST-CEILING-PERSONA-V1` ($5/persona) end-to-end through cost-guard wiring; **R-50-2 + R-50-3 did not fire**.
- `MAX_TIER_B_USD` env var ($5) provided as backup cost gate.
- All three modes (`smoke`, `canary`, `rubric`) dispatch correctly with Tier-B flag set.
- `--no-judge` disables the LLM-judge axis cleanly (no I52 multi-judge calls fired in this phase; that is I52 territory).

## Why filtered cells returned 0 rows

`tests/evals/cassettes/` is empty (`Glob` confirmed 0 files). The 326 scenarios in `PERSONA_SCENARIO_REGISTRY.csv` are not yet wired to executable cassettes; replay/canary/rubric modes therefore have no persona-conditioned data to exercise when filtered to specific personas. The unfiltered Cell 0 baseline exercises the 14 module-level / CSV-load / skill-coverage smoke probes that DO have data wiring.

This is a known I47 closure observation (4-D matrix infra exists; cassette population is the next prerequisite). Documented as evidence-matrix E5 in I47 closure UAT.

## OPS follow-up created

**OPS-50-1 — Tier-B persona cassette population.** Records cassettes for the 326 persona-conditioned scenarios (or a triaged subset of the highest-value cells) so Tier-B persona-filtered runs return non-zero rows. Owner: System Owner. Target: **I51 P3** (cassette generation for persona calibration cleanup is the natural carrier; I51 already needs to record cassettes to compute per-persona PASS rates for OPS-47-6/9 closure).

## Cost-discipline evidence

| Field | Value |
|:---|:---|
| Envelope (POLICY anchor) | `POL-EVAL-COST-CEILING-PERSONA-V1` → `max_usd_per_persona=5.00` |
| Env override | `MAX_TIER_B_USD=5` |
| CLI override | `--max-spend 5` |
| Total spend across 3 runs | **$0.00** (no live LLM calls fired; modes ran against the smoke probes + canary deltas only) |
| Cost guard raised? | **NO** |
| `tier_b_killed_for_budget` flag | not set |

## What this proves

- Tier-B preflight + cost guard work end-to-end (preflight refuses without `AKOS_RECORD_LIVE=1`; engages with cost ceiling announcement when set).
- Three Tier-B runs PASS overall_status under the $5 envelope with $0 spend.
- POLICY anchor `POL-EVAL-COST-CEILING-PERSONA-V1` (added in P2) is the canonical envelope source; env var + CLI overrides functioning.
- `eval_run_writer` correctly skips when no Supabase service-role configured (no errors, no false writes); will engage automatically when the operator stands up service-role env (no code change needed).

## What this does NOT prove (deferred)

- Persona-conditioned scenarios under live LLM scoring (waits on cassette wiring → OPS-50-1 / I51 P3).
- Multi-judge consensus voting under Tier-B → I52 P3.
- `compliance.eval_run` mirror writes — depends on Supabase service-role env (operator-side; no I50 code change needed).

## Cross-references

- E5 in [`evidence-matrix.md`](../evidence-matrix.md) (Tier-B never run; now exercised).
- D-IH-50-C executed: 2-cell smoke selected as `(OPERATOR, hard)` + `(PERSONA-INVESTOR-COLD, hard)`.
- POL-EVAL-COST-CEILING-PERSONA-V1 (P2 ship) anchored end-to-end.
- R-50-3 (Tier-B production regression) — NOT FIRED; no scenarios under live load yet.
- OPS-50-1 created (cassette wiring; carries to I51 P3).
