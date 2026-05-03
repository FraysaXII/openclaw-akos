---
language: en
status: active
initiative: 52-multi-model-judge-and-cost-discipline
report_kind: evidence-matrix
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 52 — Evidence matrix

| ID | Observation | Source | Impact |
|:---|:------------|:-------|:-------|
| E1 | `akos/eval_harness/judge.py::score_response_live` raises `NotImplementedError` (I47/P12); offline rubric is the only path today | Grep on `akos/eval_harness/judge.py` | I52 P2 ships the live dispatcher |
| E2 | 3 `judge_threshold` POLICY rows live (`POL-EVAL-JUDGE-THRESHOLD-{BRAND_VOICE,CITATION,PERSONA_FIT}-V1`; `min_pass_score=4`) | I47/P12 + `POLICY_REGISTER.csv` | P4 conditionally edits these if calibration burn surfaces drift |
| E3 | `model-prices.json` is per-token (5 entries: anthropic / openai / openai-mini / ollama / deterministic); RunPod/Kalavai cost discipline is **structurally absent** | Grep on `config/eval/model-prices.json` | P5 introduces `endpoint-prices.json` parallel + `unit` discriminator on `CostRecord` |
| E4 | Tier-B 4-D matrix wired (I47/P14) but offline-default; `--judge-cost-cap 0.01` per-scenario; `MAX_PERSONA_USD=$1` per cell; no `MAX_JUDGE_USD_PER_RUN` envelope | `.github/workflows/eval-tier-b.yml` | P7 wires `MAX_JUDGE_USD_PER_RUN=15` (D-IH-52-C) |
| E5 | I50/P2 `cost_ceiling` `policy_class` extension landed (3 runtime-envelope rows: DOSSIER / PERSONA / JUDGE); **endpoint envelope reuses the same `policy_class`** | `POLICY_REGISTER.csv`; I50/P2 phase report | P5 reuses the enum without DDL change; only new row inserts |
| E6 | OPS-51-1 forwarded from I51/P3: cassette dispatch is `(skill_id, probe_id)`-keyed; persona-keyed dispatch needs a new harness mode | I51/P3 phase report; `tests/evals/cassettes/` layout | P3 calibration burn establishes the persona-keyed mode naturally — multi-judge harness must dispatch by persona to score persona_fit correctly |
| E7 | Operator direction (2026-05-03): "All models we can — we praise ourselves on being multi-model" | User message | D-IH-52-A defaults to N=2 flagship consensus (not single-pin) |
| E8 | Operator direction (2026-05-03): "Cost management for RunPod endpoints (what happens if we deploy a huge model there?)" | User message | P5 ships `endpoint_cost_probe.py` + `endpoint_envelope_alarm.py` + per-endpoint POLICY rows; Section 8 dossier subsection answers the question in <1 click |
| E9 | I50/P3 first live dossier shows `judge_score_*_mean: null` — judge hasn't actually run live yet | `artifacts/dossier-i51-closure/manifest.json` section 03 (carryover) | P8 closure dossier should show non-null axis means with multi-judge attribution |
| E10 | I52/P5 ships unit-discriminated cost surface: `CostRecord.unit ∈ {"token","gpu_hour"}`, separate SSOTs (`model-prices.json` ↔ `endpoint-prices.json`), separate POLICY rows (`POL-EVAL-COST-CEILING-ENDPOINT-{RUNPOD,KALAVAI}-V1`); 50/50 cost tests pass; check-drift PASS; HLK validate PASS | [`reports/p5-endpoint-cost-surface-2026-05-03.md`](reports/p5-endpoint-cost-surface-2026-05-03.md) | G-52-4 wired (alarm script returns exit-2 on hard-fail-band breach); live CI integration is P7 |
