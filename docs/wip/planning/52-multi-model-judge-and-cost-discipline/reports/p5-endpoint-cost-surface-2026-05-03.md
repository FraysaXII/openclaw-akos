# I52 / P5 — Endpoint cost surface (RunPod / Kalavai)

**Date:** 2026-05-03
**Phase:** P5 (Endpoint cost surface; G-52-4 wiring + first soft-stub run)
**Initiative:** [I52 — Multi-model LLM-judge and cost discipline](../master-roadmap.md)
**Decisions referenced:** D-IH-52-D, D-IH-52-E
**Gate addressed:** G-52-4 (envelope alarm wired; stub-mode PASS)

---

## Summary

This phase introduces the **per-GPU-hour endpoint cost surface** alongside
the existing per-token cost surface. Two units now coexist in `cost_obs.py`,
governed by an explicit `unit` discriminator on `CostRecord`
(`"token"` | `"gpu_hour"`).

This closes the long-standing gap that token-pricing-based ceilings
(`POL-EVAL-COST-CEILING-MADEIRA-LOOKUP`, …, `POL-EVAL-COST-CEILING-JUDGE-V1`)
could not prevent runaway spend on RunPod / Kalavai serverless endpoints,
where billing is per-hour, not per-token.

Per **D-IH-52-E**, the two units NEVER co-mingle in a single ceiling
computation: separate price SSOTs (`config/eval/model-prices.json` vs
`config/eval/endpoint-prices.json`), separate POLICY rows, separate
aggregation paths (`aggregate_skill_cost` vs `aggregate_endpoint_cost`),
and separate evaluators (`evaluate_cost_ceiling` vs
`evaluate_endpoint_envelope`).

---

## Deliverables

### Code

| File | Status | Purpose |
|:--|:--|:--|
| `akos/eval_harness/cost_obs.py` | edited | Added `CostRecord(unit=…)`, `EndpointPrice`, `EndpointCeiling`, `EndpointMetrics`, `compute_cost_record`, `load_endpoint_prices`, `load_endpoint_ceilings`, `aggregate_endpoint_cost`, `evaluate_endpoint_envelope`. |
| `config/eval/endpoint-prices.json` | new | Per-endpoint per-GPU-hour SSOT. Initial entries: `runpod:a100-80gb` ($1.89/hr), `runpod:h100-80gb` ($3.99/hr), `kalavai:default` ($0.85/hr). FinOps-owned; quarterly refresh. |
| `scripts/endpoint_cost_probe.py` | new | Offline probe; emits markdown report + JSON sidecar to `artifacts/endpoint-cost/`. Stub fixture (`--stub`) for dispatcher validation. |
| `scripts/endpoint_envelope_alarm.py` | new | G-52-4 hard-fail gate; consumes probe sidecar (or built-in stub) and exits non-zero on hard-fail-band breaches. Optional `--warn-as-fail` for stricter canary mode. |
| `tests/test_eval_cost_endpoint.py` | new | 30 tests covering unit discriminator, dispatch, soft-fail loaders, POLICY row contract, aggregation, and envelope bands. |
| `tests/test_eval_cost_obs.py` | edited | Updated `test_policy_register_has_cost_ceiling_rows` count from 8 → 10 to lock in the two new endpoint rows alongside the existing skill-level (5) and runtime-envelope (3) tranches. |

### Governance

| File | Change |
|:--|:--|
| `docs/references/hlk/compliance/dimensions/POLICY_REGISTER.csv` | Added `POL-EVAL-COST-CEILING-ENDPOINT-RUNPOD-V1` (max $4.00/hr) and `POL-EVAL-COST-CEILING-ENDPOINT-KALAVAI-V1` (max $1.00/hr). Both `cost_ceiling` class. |
| `docs/wip/planning/52-multi-model-judge-and-cost-discipline/decision-log.md` | (next commit) Will record D-IH-52-D (unit discriminator) and D-IH-52-E (no mixed-unit aggregation) execution status. |
| `docs/wip/planning/52-multi-model-judge-and-cost-discipline/evidence-matrix.md` | (next commit) P5 evidence row pointing to this report and the stub-mode probe + alarm runs. |

---

## Verification

```text
py -m pytest tests/test_eval_cost_obs.py tests/test_eval_cost_endpoint.py -q
50 passed in 0.24s

py scripts/endpoint_cost_probe.py --stub
[probe] markdown: artifacts/endpoint-cost/endpoint-cost-probe-2026-05-03T18-49-19Z.md
[probe] json    : artifacts/endpoint-cost/endpoint-cost-probe-2026-05-03T18-49-19Z.json

py scripts/endpoint_envelope_alarm.py --stub
  - kalavai:default:  PASS  per_hour=$0.8500  daily_proj=$20.40  ceiling=$1.0000  (delta -15.0%)
  - runpod:a100-80gb: PASS  per_hour=$1.8900  daily_proj=$45.36  ceiling=$4.0000  (delta -52.8%)
[alarm] result: PASS

py scripts/check-drift.py
  No drift detected. Runtime matches repo state.

py scripts/validate_hlk.py
  OVERALL: PASS  (158 files, 0 errors)
```

---

## Decisions executed

### D-IH-52-D — `CostRecord.unit` discriminator (token | gpu_hour)

**Decision:** Every cost-bearing event in the eval harness must carry an
explicit `unit` field. `compute_cost_record(unit=…)` is the single dispatch
entry point. Constructing a `CostRecord` with `unit="token"` but no
`model_id` (or `unit="gpu_hour"` but no `endpoint_id`) raises immediately.

**Status:** Active. Test coverage:
`test_cost_record_token_unit_requires_model_id`,
`test_cost_record_gpu_hour_unit_requires_endpoint_id`,
`test_cost_record_rejects_unknown_unit`, plus dispatch tests.

### D-IH-52-E — No mixed-unit aggregation in ceilings

**Decision:** The two cost surfaces NEVER aggregate into a shared
"per-run total" or "per-skill total". Two SSOTs, two POLICY tranches, two
aggregators, two evaluators.

**Status:** Active. Implemented as physical separation in `cost_obs.py`:
`load_model_prices` ↔ `load_endpoint_prices`,
`aggregate_skill_cost` ↔ `aggregate_endpoint_cost`,
`evaluate_cost_ceiling` ↔ `evaluate_endpoint_envelope`. The token pathway
is unchanged; the endpoint pathway is additive.

---

## Notes for the operator

1. **First real RunPod / Kalavai run** — the entries in `endpoint-prices.json`
   are placeholder pricing per RunPod 2026-Q2 published rates. Before any
   `AKOS_RECORD_LIVE=1` endpoint run, FinOps must verify the operator's
   contracted rate against their RunPod / Kalavai dashboard and refresh the
   JSON. The `_2026_q2_review_note` field documents this contract.

2. **Daily projection is informational, not a gate.** Only the
   `cost_usd_per_hour_avg` metric drives the envelope alarm; the
   `projected_daily_usd` field exists for human-readable dashboards
   (per the I52 plan refinement: "human-readable dashboards for cost
   visibility — per-token vs per-GPU-hour"). A 24h projection assumes the
   endpoint stays at the observed rate for a full day; for spiky workloads
   this overstates the true daily spend.

3. **Stub mode safety.** Both `--stub` paths are documented with a
   "DISPATCHER VALIDATION ONLY" framing in the report header, mirroring
   the I52 P3 calibration burn convention so stub runs cannot be
   misread as production cost evidence.

4. **G-52-4 will fire on first FAIL.** The alarm script returns exit code
   2 when any endpoint exceeds its hard-fail band (>20% over ceiling).
   When wired into `eval-tier-b.yml` in P7, this becomes a blocking gate
   alongside the existing per-token and calibration-drift gates.

---

## Forward-carry

- **OPS-52-2 (new):** First real-API RunPod or Kalavai run. Will validate
  observed rate against `endpoint-prices.json` and exercise
  `aggregate_endpoint_cost` end-to-end with non-stub data. Bound to the
  next operator-driven AKOS_RECORD_LIVE cycle.
- **G-52-4 dispatcher status:** WIRED (this phase). Live activation
  deferred to P7 CI integration.
