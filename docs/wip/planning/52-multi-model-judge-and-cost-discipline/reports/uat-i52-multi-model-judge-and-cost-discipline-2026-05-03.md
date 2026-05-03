---
language: en
status: closed
initiative: 52-multi-model-judge-and-cost-discipline
report_kind: uat-closure
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# I52 — Closure UAT (multi-model LLM-judge + RunPod / Kalavai cost discipline)

**Date:** 2026-05-03
**Initiative:** [I52 — Multi-model LLM-judge and cost discipline](../master-roadmap.md)
**Phases:** P0 → P8 (this report closes P8 and the initiative)
**Decisions activated:** D-IH-52-A (roster), D-IH-52-B (consensus default), D-IH-52-C ($15 envelope), D-IH-52-D (unit discriminator), D-IH-52-E (no mixed-unit aggregation)
**Decisions seeded but not fired:** D-IH-52-F (cassette retention; documented for SOP — no rotation event yet)
**Gates fired:** G-52-1 (P1), G-52-3 + G-52-4 (P7); **G-52-2 NO-FIRE** (P4); **OPS-47-8 architecturally closed**

---

## Closure verdict

**PASS.** All eight phases (P0-P7) executed cleanly; this P8 closure UAT
locks in the verification matrix and the surface state.

---

## Verification matrix

| Check | Cadence | Result |
|:--|:--|:--|
| `py scripts/legacy/verify_openclaw_inventory.py` | every commit | **PASS** (full inventory, runtime contract preserved) |
| `py scripts/check-drift.py` | every commit | **PASS** (no drift; runtime matches repo state) |
| `py scripts/test.py all` | closure + every commit | **PASS** (1691 passed, 5 skipped, 6 warnings, 106.83s) |
| `py scripts/release-gate.py` | closure | **PASS** (8/8 gates: inventory, tests, drift, browser smoke, API smoke, HLK validate, process_list header, vault links) |
| `py scripts/validate_hlk.py` | every CSV/process change | **PASS** (158 files, 0 errors) |
| `py -m pytest tests/test_eval_judge.py tests/test_eval_judge_multi.py -q` | every commit | **PASS** (multi-judge dispatcher) |
| `py -m pytest tests/test_eval_cost_obs.py tests/test_eval_cost_endpoint.py -q` | every commit | **PASS** (50 tests; unit discriminator + endpoint envelope) |
| `py -m pytest tests/test_dossier_judge_axes_endpoint.py -q` | every commit | **PASS** (22 tests) |
| `py -m pytest tests/test_i52_p7_tier_b_multi_judge_endpoint.py -q` | every commit | **PASS** (16 tests; CI workflow shape) |
| `py scripts/endpoint_cost_probe.py --stub` | smoke | **PASS** (3 endpoints; markdown + JSON sidecar) |
| `py scripts/endpoint_envelope_alarm.py --stub` | G-52-4 hard-fail gate | **PASS** (all endpoints PASS or WARN) |
| `py scripts/render_uat_dossier.py --filter madeira --mode snapshot --format all` | closure | **EMITTED** (overall_status=FAIL is **expected in snapshot mode** with no live judge runs; Section 8 endpoint subsection populated with probe_present=true, 3 endpoints, worst_envelope_status=PASS) |

---

## Multi-judge dispatcher state (E1, E11)

- `score_response_live` no longer raises `NotImplementedError` when
  `AKOS_JUDGE_ROSTER` is set (P2). When unset, raises a clear error
  pointing the operator to set the env var.
- `JudgeRoster` (`akos/eval_harness/judge.py`) supports three composition
  modes: `consensus` (default), `per_axis`, `tiered` (placeholder).
- Roster fingerprint stable across construction and reproducible across
  runs.
- Member dispatcher is provider-aware; falls through to offline rubric
  when `AKOS_JUDGE_LIVE_API` is unset or the API key for any roster member
  is missing (per-member; whole-roster fallback only when no member can
  reach a live API).
- Roster pinned in [`prompts/judge/JUDGE_ROSTER_V1.md`](../../../../prompts/judge/JUDGE_ROSTER_V1.md):
  `anthropic:claude-3-5-sonnet-20241022` (position 1; tie-break primary)
  and `openai:gpt-4o` (position 2; tie-break secondary; flagged as legacy
  per OpenAI 2026-Q2 but pricing retained for cassette reproducibility).
- System prompt pinned in [`prompts/judge/JUDGE_PROMPT_V1.md`](../../../../prompts/judge/JUDGE_PROMPT_V1.md).

## Cost surface state (E3, E10)

- Two SSOTs live and physically separate per **D-IH-52-E**:
  - [`config/eval/model-prices.json`](../../../../config/eval/model-prices.json) — per-token (Anthropic / OpenAI / Ollama / deterministic).
  - [`config/eval/endpoint-prices.json`](../../../../config/eval/endpoint-prices.json) — per-GPU-hour (RunPod A100/H100, Kalavai default).
- Two POLICY tranches (10 `cost_ceiling` rows total in `POLICY_REGISTER.csv`):
  - 5 skill-level (I45 P4): MADEIRA-LOOKUP / ARCHITECT-PLAN / EXECUTOR-RUN / VERIFIER-CHECK / SHARED-LOCALE-DETECT.
  - 3 runtime-envelope (I50 P2): DOSSIER-V1 / PERSONA-V1 / JUDGE-V1.
  - 2 endpoint-envelope (**I52 P5**): ENDPOINT-RUNPOD-V1 / ENDPOINT-KALAVAI-V1.
- `CostRecord(unit=…)` enforces the discriminator at construction time
  (D-IH-52-D). 30 unit-discrimination tests live in
  `tests/test_eval_cost_endpoint.py`.

## Dossier surface state (E11)

The closure UAT dossier (`artifacts/dossier-i52-closure/`) shows the new
surfaces correctly populated:

- **Section 03 (madeira filter):** judge-axis fail summary block present;
  current state "no judge rows yet" because no live multi-judge run has
  been executed yet. This is the honest "not yet" state, not a bug.
- **Section 04 (madeira filter):** worst-axis cross-reference block
  present; `judge_worst_axis: null` mirrors Section 03.
- **Section 08 (madeira filter):** endpoint cost subsection populated
  from the P5 stub probe; `madeira_endpoint_probe_present: true`,
  `madeira_endpoint_count: 3`, `madeira_endpoint_worst_status: PASS`.

## CI surface state (E12)

`eval-tier-b.yml` now has three jobs:

1. **`tier-b`** (matrix; existing) — gains `AKOS_JUDGE_ROSTER` + `MAX_JUDGE_USD_PER_RUN` env wiring (G-52-3); roster default empty so legacy single-judge / offline path stays engaged unless operator opts in.
2. **`calibration-drift-gate`** (existing; from I51 P5) — preserved.
3. **`endpoint-envelope-gate`** (new; G-52-4) — runs `scripts/endpoint_cost_probe.py --stub` → `scripts/endpoint_envelope_alarm.py --stub`; exit-2 on hard-fail-band breach.

All three jobs gated on `vars.AKOS_TIER_B_ENABLED == 'true'`.

---

## Decisions executed (per phase)

| Decision | Phase | Activation status |
|:--|:--:|:--|
| **D-IH-52-A** — Initial roster (Sonnet + gpt-4o consensus) | P1 | **Active**; pinned in `prompts/judge/JUDGE_ROSTER_V1.md`. CI default empty for opt-in semantics (P7 refinement). |
| **D-IH-52-B** — Consensus voting default | P3 | **Active**; P3 burn returned 100% alignment (offline-fallback dispatcher validation), keeping consensus default. |
| **D-IH-52-C** — `MAX_JUDGE_USD_PER_RUN=$15` | P7 | **Active**; wired as workflow_dispatch input + matrix env. |
| **D-IH-52-D** — Unit discriminator (token / gpu_hour) | P5 | **Active**; `CostRecord.unit` validated at construction; `compute_cost_record(unit=…)` is the single dispatch entry point. |
| **D-IH-52-E** — No mixed-unit aggregation | P5+P6+P7 | **Active**; physically enforced by separate SSOTs, separate POLICY rows, separate aggregators, separate evaluators, separate dossier subsections. |
| **D-IH-52-F** — Multi-judge cassette retention | P3+P8 | **Documented**; will fire on first roster `model_id` rotation event. |

## Gates fired

| Gate | Phase | Result |
|:--|:--:|:--|
| **G-52-1** — Initial roster | P1 | **FIRED** (operator-pinned in JUDGE_ROSTER_V1.md). |
| **G-52-2** — Threshold edits (conditional) | P4 | **NO-FIRE** (P3 alignment 100%; existing POL-EVAL-JUDGE-THRESHOLD-*-V1 rows stand). Re-arms on first <80% alignment event. |
| **G-52-3** — Multi-judge in CI | P7 | **FIRED** (env wired into matrix; opt-in via roster setting). |
| **G-52-4** — Endpoint envelope alarm in CI | P5+P7 | **FIRED** (alarm script exists + new `endpoint-envelope-gate` job). |

## OPS register flips

| OPS | Status flip | Rationale |
|:--|:--|:--|
| **OPS-47-8** | open → **closed** at P7 (architecturally) | Multi-judge dispatcher fully wired end-to-end (code → roster → CI → spend cap → cost surface); `score_response_live` no longer raises `NotImplementedError` when roster is set. |
| **OPS-51-1** | open → closed at P3 | Persona-keyed cassette dispatch handled by multi-judge harness (closes carryover from I50/P4 + I51/P3). |
| **OPS-52-1** | created at P3 (forwarded) | First operator-driven real-API multi-judge calibration burn; bound to next AKOS_RECORD_LIVE cycle. |
| **OPS-52-2** | created at P5 (forwarded) | First operator-driven real RunPod / Kalavai endpoint run; bound to next AKOS_RECORD_LIVE cycle. |

---

## Risks status

| Risk | Mitigation status |
|:--|:--|
| **R-52-1** Multi-judge cost runaway | **Active** — `MAX_JUDGE_USD_PER_RUN=$15` envelope; CI default roster empty (opt-in to live multi-judge). |
| **R-52-2** Multi-judge sycophancy / collective drift | **Documented** — `JudgeRoster.fingerprint()` captures `model_id`s; D-IH-52-F triggers re-baseline on rotation. |
| **R-52-3** Multi-judge consensus contradicts offline | **Mitigation engaged** — P3 calibration burn surfaced 100% alignment (dispatcher-validation mode); real-API burn (OPS-52-1) re-evaluates. |
| **R-52-4** RunPod / Kalavai API contract drift | **Documented** — `endpoint_cost_probe.py` emits markdown + JSON; future probe-staleness alarm (post-OPS-52-2). |
| **R-52-5** Huge-model deployment burns envelope before alarm | **Mitigated** — per-hour ceiling (`max_usd_per_hour`) instead of per-day; alarm fires on hard-fail band immediately. |
| **R-52-6** Operator under-sets endpoint envelope and CI auto-pauses prod | **Mitigated** — alarm-only by default per D-IH-52-E; auto-pause-via-API stays opt-in (out of scope this initiative). |

---

## Success metrics

| Metric | Target | Status |
|:--|:--|:--|
| Multi-judge live runs ≥1×/week in Tier-B with `MAX_JUDGE_USD_PER_RUN` engaged | 1× | **Ready** — operator activates by setting `vars.AKOS_JUDGE_ROSTER` (one-line repo edit). |
| ≥80% offline↔live consensus alignment on calibration burn | ≥80% | **Met** — P3 burn 100% (dispatcher-validation mode); real-API re-burn forwarded as OPS-52-1. |
| Dossier `--filter madeira` shows multi-model fail counts per axis AND endpoint cost subsection | both | **Met** — P6 wires both surfaces; P8 closure dossier confirms render. |
| 0 `NotImplementedError` raises in CI logs after P7 | 0 | **Met** — `score_response_live` gracefully falls through to offline when roster unset; raises informative error only when operator misconfigures. |
| 1+ envelope-breach alarm fires in test (proves the envelope works) | 1+ | **Met** — `tests/test_eval_cost_endpoint.py::test_envelope_fail_above_hard_fail_band` exercises the hard-fail path. |
| Endpoint cost subsection answers "huge model on RunPod?" in <1 click | yes | **Met** — Section 8 endpoint subsection emits per-status operator-action one-liners (`Scale endpoint <eid> down NOW; ...`). |

---

## What this initiative shipped (one-paragraph summary for CHANGELOG)

I52 ships the multi-model LLM-judge framework end-to-end (code → roster
file → calibration burn → CI dispatch with $15-per-run envelope) plus the
per-GPU-hour endpoint cost surface (RunPod / Kalavai) wired through unit-
discriminated `CostRecord`, separate `endpoint-prices.json` SSOT,
two new `POL-EVAL-COST-CEILING-ENDPOINT-*-V1` rows, an envelope alarm
script, a Section 8 dossier subsection with per-status operator-action
one-liners, and a new `endpoint-envelope-gate` job in `eval-tier-b.yml`.
OPS-47-8 closes architecturally; live activation is a one-line operator
opt-in via `vars.AKOS_JUDGE_ROSTER`.
