# I52 / P7 — CI activation (G-52-3 + G-52-4)

**Date:** 2026-05-03
**Phase:** P7 (Tier-B CI activation: multi-judge env + endpoint envelope gate)
**Initiative:** [I52 — Multi-model LLM-judge and cost discipline](../master-roadmap.md)
**Decisions referenced:** D-IH-52-A, D-IH-52-C, D-IH-52-D, D-IH-52-E
**Gates fired:** **G-52-3 (multi-judge in CI)**, **G-52-4 (endpoint envelope alarm in CI)**

---

## Summary

This phase activates the multi-judge dispatcher and the endpoint envelope
alarm in the weekly Tier-B GitHub Actions workflow. The workflow now has
three jobs:

1. **`tier-b` (matrix; existing).**
   The 4-D matrix (`model_tier × persona`) is unchanged but now exposes
   `AKOS_JUDGE_ROSTER` and `MAX_JUDGE_USD_PER_RUN` env vars to every cell.
   Default roster is **empty** so legacy single-judge / offline behaviour
   is preserved unless the operator opts in via:
   - `workflow_dispatch` input `judge_roster=anthropic:…,openai:…`, or
   - repo-level `vars.AKOS_JUDGE_ROSTER` (sticky across runs).

2. **`calibration-drift-gate` (existing; from I51 P5).**
   Untouched.

3. **`endpoint-envelope-gate` (new; G-52-4).**
   Runs once per workflow after `tier-b`. Calls
   `scripts/endpoint_cost_probe.py --stub` then
   `scripts/endpoint_envelope_alarm.py --stub` and exits non-zero if any
   endpoint exceeds the hard-fail band (>20% over its
   `POL-EVAL-COST-CEILING-ENDPOINT-{RUNPOD,KALAVAI}-V1` ceiling). Uploads
   the probe markdown + JSON sidecar as workflow artefacts.

`--stub` is the deliberate ground truth until OPS-52-2 ships real
RunPod / Kalavai run-log JSONLs. The contract (alarm → exit-2 →
workflow-fails) is identical for stub and real-data invocations, so the
gate behaviour locks in now and only the input source changes later.

---

## Deliverables

### Code

| File | Status | Purpose |
|:--|:--|:--|
| `.github/workflows/eval-tier-b.yml` | edited | (a) Header docs reference I52 P7, G-52-3, G-52-4; (b) new `workflow_dispatch` inputs `judge_roster`, `max_judge_usd_per_run`; (c) `AKOS_JUDGE_ROSTER`, `MAX_JUDGE_USD_PER_RUN` env wired into matrix; (d) new `endpoint-envelope-gate` job with stub probe + alarm + artefact upload. |
| `tests/test_i52_p7_tier_b_multi_judge_endpoint.py` | new | 16 workflow-shape tests covering multi-judge env vars, the new gate job, parsable YAML, and backward compatibility with `calibration-drift-gate` (I51 P5). |

### Default values (sticky)

| Knob | Default | Source | Notes |
|:--|:--:|:--|:--|
| `AKOS_JUDGE_ROSTER` | `''` | workflow input → `vars` → empty | Empty preserves legacy path; opt-in by setting comma-separated `model_id`s matching `prompts/judge/JUDGE_ROSTER_V1.md`. |
| `MAX_JUDGE_USD_PER_RUN` | `15.0` | workflow input | D-IH-52-C: scales with roster size (N=2 consensus). |
| `AKOS_JUDGE_COST_CAP` | `0.01` | workflow input (existing) | I47 P14 + POL-EVAL-COST-CEILING-JUDGE-V1; per-scenario. |
| `MAX_PERSONA_USD` | `1.0` | workflow input (existing) | POL-EVAL-COST-CEILING-PERSONA-V1; per-cell. |
| Endpoint envelope source | `--stub` | hardcoded today | Pivots to `--runs-jsonl` once OPS-52-2 produces operator-curated run logs. |

---

## Verification

```text
py -m pytest tests/test_i52_p7_tier_b_multi_judge_endpoint.py -q
16 passed in 0.14s

py -m pytest tests/test_i47_p14_tier_b_persona_matrix.py \
             tests/test_i52_p7_tier_b_multi_judge_endpoint.py \
             tests/test_eval_tier_b.py -q
47 passed in 5.96s

py -c "import yaml; yaml.safe_load(open('.github/workflows/eval-tier-b.yml'))"
(no output; YAML parses)

py scripts/check-drift.py
  No drift detected. Runtime matches repo state.
```

---

## Decisions executed

### D-IH-52-A — Initial roster (env-var-driven; CI-default-empty)

The CI default is **empty roster** — not the P1-pinned
`anthropic:claude-3-5-sonnet-20241022,openai:gpt-4o`. This is intentional:

- Live multi-judge spend is governed by `MAX_JUDGE_USD_PER_RUN` ($15
  default) but only the operator should opt into it from the CI surface.
- Empty roster keeps the legacy `score_response_offline` path engaged for
  the weekly cadence; operator promotes the workflow to live-multi-judge
  by setting `vars.AKOS_JUDGE_ROSTER` once they're ready to spend.
- Manual `workflow_dispatch` runs can override per-invocation via the
  `judge_roster` input.

This preserves operator agency without surrendering the CI gate (which
still fires on offline-rubric regressions).

### D-IH-52-C — `MAX_JUDGE_USD_PER_RUN` envelope ($15 default)

Wired as a workflow_dispatch input plus a top-level matrix env var. The
default is the I52 P0 plan's $15 for N=2 consensus; the operator overrides
per workflow_dispatch invocation when scaling roster size.

### D-IH-52-D + D-IH-52-E — Endpoint envelope gate behaviour

The new `endpoint-envelope-gate` job is the CI manifestation of the
unit-discriminated cost surface. It does NOT consume `model-prices.json`,
only `endpoint-prices.json` + endpoint POLICY rows. The gate cannot
silently aggregate token and gpu_hour costs because the alarm script
only reads the gpu_hour pathway.

---

## Notes for the operator

1. **First end-to-end multi-judge live run.**
   To activate G-52-3 in production:
   ```
   gh workflow run eval-tier-b.yml \
     -f judge_roster='anthropic:claude-3-5-sonnet-20241022,openai:gpt-4o' \
     -f max_judge_usd_per_run='15.0'
   ```
   The first such run is the I52 success-metric "multi-judge live runs
   ≥1×/week in Tier-B with `MAX_JUDGE_USD_PER_RUN` engaged".

2. **First real RunPod / Kalavai endpoint probe.**
   When OPS-52-2 produces the first observed run-log JSONL, swap the
   stub commands in the `endpoint-envelope-gate` job to:
   ```
   python scripts/endpoint_cost_probe.py --runs-jsonl artifacts/endpoint-cost/observed-runs-*.jsonl
   python scripts/endpoint_envelope_alarm.py --probe-json artifacts/endpoint-cost/endpoint-cost-probe-*.json
   ```
   The gate's exit-code contract stays identical; only the data source
   changes. This keeps the workflow change small and reviewable.

3. **Staying offline by default.**
   Pre-commit and `release_gate` continue to run cassette replay only
   (no live API calls). The `eval-tier-b.yml` workflow is the **only**
   place where `AKOS_RECORD_LIVE=1` is wired, and `AKOS_TIER_B_ENABLED`
   repo-var gating means even that workflow is operator-opt-in.

---

## Forward-carry

- **OPS-52-2** (first real-API endpoint run) — still bound to next
  AKOS_RECORD_LIVE cycle; the CI surface is now ready to consume it.
- **OPS-47-8** (multi-judge live activation) — architecturally closed at
  P2 (dispatcher landed); fully wired to CI as of this phase. Final
  status flip lives in P8 closure.
- **G-52-1** (P1) — recorded; multi-judge roster pinned in
  `prompts/judge/JUDGE_ROSTER_V1.md`.
- **G-52-2** (P4) — no-fire this cycle; re-arms on first live drift.
- **G-52-3** (P7) — **fired** (this phase). CI surface live.
- **G-52-4** (P5+P7) — **fired** (this phase). Alarm gate live.

P8 (closure) is the next and final I52 phase.
