---
language: en
status: active
initiative: 47-user-centric-uat
report_kind: phase-report
phase: P14
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-05-02
---

# I47 P14 — Tier B 4-D matrix extension (D-IH-47-H)

## What shipped

Extended `.github/workflows/eval-tier-b.yml` from a 1-D matrix (model_tier) to a 4-D matrix per D-IH-47-H. Per-cell artifacts + cost discipline + P13 item 4 wiring.

## Matrix expansion

| Dimension | Default values | Cardinality | Notes |
|:---|:---|:---:|:---|
| `model_tier` | `cheap`, `flagship` | 2 | Unchanged (D-IH-45-C) |
| `persona` | `OPERATOR`, `PERSONA-INVESTOR-COLD`, `PERSONA-INVESTOR-WARM`, `PERSONA-ADVISOR-REFERRAL`, `PERSONA-CUSTOMER-KIRBE-PROSPECT` | 5 | Tier-1 + OPERATOR (D-IH-47-H) |
| `scenario_class` | (aggregated in scorecard markdown) | n/a | Surfaced by Scorecard.to_markdown() per-persona section, not matrix dim |
| `judge_axis` | (aggregated in scorecard markdown) | n/a | Surfaced by Scorecard.to_markdown() LLM-judge section, not matrix dim |

**Default cell count: 2 × 5 = 10 cells per weekly run** (previously 2). The remaining 2 dimensions (scenario_class + judge_axis) are aggregated by the scorecard renderer rather than expanded into matrix cells — the eval harness already aggregates by both, and 4-D matrix expansion (2 × 16 × 7 × 3 = 672 cells) would be infeasible.

## Tier-3 / Tier-2 exclusion (D-IH-47-H)

Tier-2 (8 personas) and Tier-3 (4 personas) are NOT in the default weekly matrix. They opt-in via `workflow_dispatch` `persona_filter` input. This is the operator-recommended posture per the cursor plan: weekly run focuses on highest strategic value (operator + investor + advisor + customer-prospect); Tier-2/3 personas run on-demand for specific debugging needs.

## Cost discipline

| Var | Default | Purpose |
|:---|:---|:---|
| `MAX_TIER_B_USD` | $5.00 | Per-RUN spend cap (existing P6) |
| `MAX_PERSONA_USD` | $1.00 | I47 P14: per-persona-per-cell spend cap (R-47-3) |
| `AKOS_JUDGE_COST_CAP` | $0.01 | I47 P14: per-scenario LLM-judge cost cap (R-47-11) |
| `--regression-pp` | 5.0 | Per-skill regression hard-fail threshold (existing P6) |

Estimated worst-case weekly spend: 10 cells × $1/cell = $10/week (before judge), or ~$77/week with judge active per P12 cost envelope (D-IH-47-J).

## P13 item 4 dependency wired

`SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` exposed in workflow env so `akos.eval_harness.eval_run_writer` activates during Tier B runs. Each cell will write its scorecard rows to `compliance.eval_run` with `persona_id` + `difficulty_class` + `scenario_class` + `judge_scores` populated.

Job summary now surfaces:

```
- compliance.eval_run writes: N written, M skipped, K errors
```

per cell, so operator can verify writes are landing.

## Implementation details

### preflight step picks persona

```yaml
PERSONA="${{ github.event.inputs.persona_filter || matrix.persona }}"
echo "persona=$PERSONA" >> $GITHUB_OUTPUT
```

`persona_filter` (workflow_dispatch input) takes precedence over matrix.persona, allowing operator to run a single persona end-to-end via on-demand trigger.

### `--persona` flag passed to all 3 eval invocations

```yaml
python scripts/eval.py --mode all \
  --persona "${{ steps.preflight.outputs.persona }}" \
  --json > tier-a-${{ matrix.model_tier }}-${{ matrix.persona }}.json
```

Same for `--mode replay` and `--mode adversarial` Tier B steps.

### Per-cell artifact naming

```
tier-a-${{ matrix.model_tier }}-${{ matrix.persona }}.json
tier-b-${{ matrix.model_tier }}-${{ matrix.persona }}.json
tier-b-adv-${{ matrix.model_tier }}-${{ matrix.persona }}.json
```

Uploaded as artifact `eval-scorecards-${{ matrix.model_tier }}-${{ matrix.persona }}` with 90-day retention.

## Verification

- 20 new tests in `tests/test_i47_p14_tier_b_persona_matrix.py` PASS:
  - Workflow shape preserved (4 tests)
  - 4-D matrix extension correct (4 tests)
  - Persona filter input + matrix exclusion of Tier-2/3 (3 tests)
  - Cost discipline env vars + per-persona caps (3 tests)
  - --persona flag wired through all 3 invocations (2 tests)
  - SUPABASE secrets exposed for P13 item 4 (2 tests)
  - Artifact naming + job summary references (2 tests)
- Existing eval-tier-b workflow shape preserved (still gated by `vars.AKOS_TIER_B_ENABLED`)

## Cross-references

- D-IH-47-H (extend existing eval-tier-b.yml with persona matrix dim)
- R-47-3 (per-persona spend cap mitigation)
- R-47-11 (judge cost runaway mitigation via per-scenario cap)
- I45 P6 (Tier B baseline workflow extended)
- I47 P10 (`--persona` flag wired in scripts/eval.py)
- I47 P12 (`--judge-cost-cap` flag wired)
- I47 P13 item 4 (`SUPABASE_URL` + service role key dependency for live writes)
