---
language: en
status: active
initiative: 52-multi-model-judge-and-cost-discipline
report_kind: master-roadmap
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 52 — Multi-model LLM-judge live activation + RunPod/Kalavai cost discipline

**Folder:** `docs/wip/planning/52-multi-model-judge-and-cost-discipline/`

**Status:** Execution starting 2026-05-03; depends on I51 closure ✓ (calibrated baseline at 0 / 17 outliers).

**Authoritative Cursor plan:** `~/.cursor/plans/i50–i56_madeira_kb_completion_87cc767e.plan.md` §"Initiative 52".

**Origin:**

- **D-IH-47-J** (LLM-as-judge live activation deferred from I47 P12). `akos/eval_harness/judge.py::score_response_live` raises `NotImplementedError`.
- **OPS-47-8** ("approve LLM-judge live mode + pin model_id") is the operator-on-demand carrier this initiative closes.
- **OPS-51-1** (forwarded from I51 P3): persona-keyed cassette dispatch architecture aligns with multi-judge harness mode and lands here in P3/P4.
- **Operator direction (2026-05-03)**: "All models we can — we praise ourselves on being multi-model. Also we need cost management for RunPod endpoints (what happens if we deploy a huge model there?)."

## Outcome

(a) Replace `NotImplementedError` in `score_response_live` with a **multi-model judge framework** (consensus voting OR per-axis specialization OR cost-aware tiered escalation; default consensus N=2);
(b) extend cost surface to handle **per-token providers** (Anthropic / OpenAI / Mistral / etc.) AND **per-GPU-hour endpoints** (RunPod / Kalavai / future) without conflating units;
(c) ship a human-readable cost dashboard so a huge-model deployment is visible in <1 click;
(d) calibrate offline↔live alignment ≥80% per axis;
(e) refresh `POL-EVAL-JUDGE-THRESHOLD-*` rows if alignment forces threshold edits;
(f) surface judge axes + cost-per-endpoint in dossier;
(g) activate multi-judge in Tier-B with bounded envelope per-tier.

Bidirectional contract: `dossier_run.cost_breakdown` distinguishes `judge_usd_per_token` vs `endpoint_usd_per_hour`; **R-47-10** (judge sycophancy) mitigated by **multi-model consensus** rather than single-model pin.

## Multi-model judge approach

| Pattern | Description | When to use |
|:--|:--|:--|
| **Consensus voting (default)** | N≥2 models score each axis; majority wins; ties broken by tier-priority list | Default for all axes; clear operator-explainable |
| **Per-axis specialization** | Each axis routed to a model that historically aligns best (e.g., citation → flagship; brand_voice → cheap-pinned) | Activated only after P3 calibration shows axis-specific gaps |
| **Cost-aware tiered escalation** | Cheap model first; escalate to flagship only when cheap model's confidence < threshold (or 2 cheap models disagree) | Activated only if P3 burns reveal escalation is cheaper than pure-flagship |

Default at launch: **consensus voting with N=2 (1 Anthropic + 1 OpenAI)**; cheap-tier consensus offered as opt-in via env. Per-endpoint (RunPod/Kalavai) judges are eligible if alignment ≥80% in P3 burn.

## RunPod / Kalavai cost discipline

**The unit-mismatch problem:** today `model-prices.json` is per-token. RunPod/Kalavai charge per **GPU-hour** when an endpoint is up — even if zero requests land. A "huge model" deployment burns regardless of usage.

**The clever-and-scalable answer:**

- New `config/eval/endpoint-prices.json` parallels `model-prices.json` but keys on `endpoint_id` and emits `usd_per_hour` (not per-token).
- `akos/eval_harness/cost_obs.py` extension: cost record carries `unit ∈ {"token", "gpu_hour"}` discriminator; aggregator never adds different units; dashboard renders both side-by-side with a 24h projected forecast per endpoint.
- **Per-endpoint envelope POLICY rows:** `POL-EVAL-COST-CEILING-ENDPOINT-{RUNPOD,KALAVAI,...}-V1` with `max_usd_per_day` (operator-set). Probe at runtime: when ≥80% of envelope consumed, alarm; at 100%, **auto-pause** endpoint via API (or operator alarm if API not reachable) and write a `pol_endpoint_envelope_breach` row.
- **Human-digest dashboard:** new `Section08OperationalHealth` subsection "Endpoint cost surface" — shows endpoints up vs idle, projected 24h burn, operator one-line action ("scale-down idle Kalavai endpoint X to save ~$Y/day"). Ships in same `--filter madeira` flavor.

## Asset classification

| Class | Paths | Rule |
|:------|:------|:-----|
| **Modified canonical (code)** | [`akos/eval_harness/judge.py`](../../../akos/eval_harness/judge.py) | Multi-model dispatcher (`JudgeRoster`); `score_response_live` calls dispatcher; cassette captures all member `model_id`s |
| **Modified canonical (code)** | [`akos/eval_harness/cost_obs.py`](../../../akos/eval_harness/cost_obs.py) | `CostRecord.unit ∈ {"token", "gpu_hour"}`; aggregator forbids unit-mixing |
| **New canonical (config)** | `config/eval/endpoint-prices.json` (USD per GPU-hour) | Parallels `model-prices.json`; FinOps role-owned |
| **New canonical (POLICY rows)** | `POL-EVAL-COST-CEILING-ENDPOINT-{RUNPOD,KALAVAI,...}-V1` in [`POLICY_REGISTER.csv`](../../../docs/references/hlk/compliance/dimensions/POLICY_REGISTER.csv); reuses `cost_ceiling` policy_class from I50 D-IH-50-A | Per-endpoint envelope; operator-set `max_usd_per_day` |
| **Modified canonical (POLICY rows)** | `POL-EVAL-JUDGE-THRESHOLD-*-V1` | Edit only if P3 calibration burn surfaces drift |
| **New canonical (vault)** | `prompts/judge/JUDGE_PROMPT_V1.md` + per-model variants if calibration shows divergence; `prompts/judge/JUDGE_ROSTER_V1.md` (commits roster) | Operator-pinned judge prompt(s); committed for reproducibility |
| **Modified canonical (dossier)** | [`akos/dossier/sections.py`](../../../akos/dossier/sections.py) Section 03/04/08 | Per-axis fail count + worst-axis trend (madeira); **new Section 8 endpoint cost subsection** |
| **Modified CI** | [`.github/workflows/eval-tier-b.yml`](../../../.github/workflows/eval-tier-b.yml) | `MAX_JUDGE_USD_PER_RUN` envelope (default $15 for N=2 consensus); cassette-replay default for pre-commit |
| **New scripts** | `scripts/endpoint_cost_probe.py` (queries RunPod/Kalavai APIs for live endpoint state + projected burn); `scripts/endpoint_envelope_alarm.py` (alarms + auto-pause hook) | |
| **New tests** | `tests/test_eval_judge_multi.py` (consensus + tie-breaking + fallback), `tests/test_endpoint_cost_unit.py` (no unit-mixing), `tests/test_endpoint_envelope.py` (envelope breach + alarm), dossier endpoint-cost assertions in `tests/test_dossier_madeira_flavor.py` | |

## Phase plan (~5-7 op-days)

| Phase | Focus |
|:-:|:----|
| **P0** | Bootstrap initiative folder + 6 artefacts; README row. |
| **P1** | **Roster survey + selection (G-52-1):** WebSearch 2026-Q2 model availability across providers (Anthropic / OpenAI / Mistral / Cohere / Vertex / on-RunPod / on-Kalavai); operator picks initial roster (default: 1 Anthropic flagship + 1 OpenAI flagship; cheap-tier opt-in); commit roster to `prompts/judge/JUDGE_ROSTER_V1.md`. |
| **P2** | **Multi-judge dispatcher:** Implement `JudgeRoster` class in `akos/eval_harness/judge.py` (consensus voting; tie-break order; per-axis routing toggle); `score_response_live` calls dispatcher; gated by `AKOS_JUDGE_ROSTER` env (comma-separated model_ids). |
| **P3** | **Calibration burn:** Replay 50 representative scenarios across the roster; produce `reports/judge-live-calibration-YYYY-MM-DD.md` with per-model and consensus alignment vs offline rubric per axis; target ≥80% consensus alignment. Decide D-IH-52-B (consensus default vs per-axis specialization). Also closes **OPS-51-1** (persona-keyed cassette dispatch wiring through multi-judge harness mode). |
| **P4** | **Threshold refresh (G-52-2, conditional):** if any axis < 80%, propose `POL-EVAL-JUDGE-THRESHOLD-*` edits OR per-axis routing override; operator approves. |
| **P5** | **Endpoint cost surface (RunPod/Kalavai):** Author `config/eval/endpoint-prices.json`; extend `cost_obs.py` with unit discriminator; ship `endpoint_cost_probe.py` + `endpoint_envelope_alarm.py`; add per-endpoint POL rows (G-52-4); test with mock RunPod/Kalavai responses. |
| **P6** | **Dossier surface:** Section 03/04 fail counts + worst-axis trend (madeira flavor); **new Section 8 "Endpoint cost surface"** subsection with up/idle/projected-24h-burn + operator one-line action. |
| **P7** | **CI activation (G-52-3):** Tier-B `eval-tier-b.yml` runs multi-judge consensus on `model_tier × persona × scenario_class × judge_axis` matrix with `MAX_JUDGE_USD_PER_RUN` cap (default $15 for N=2; D-IH-52-C); endpoint envelope alarm wired; pre-commit + `release_gate` stay offline (cassette replay). |
| **P8** | **Closure:** pytest sweep, dossier emission with multi-judge + endpoint cost subsection, CHANGELOG, README row, WIP_DASHBOARD; flip OPS-47-8 status. |

## Verification matrix

| Check | Cadence |
|:------|:--------|
| `py scripts/validate_policy_register.py` (incl. revised judge_threshold rows if P4 fires + new endpoint cost-ceiling rows) | Every commit |
| `py -m pytest tests/test_eval_judge.py tests/test_eval_judge_multi.py tests/test_endpoint_cost_unit.py tests/test_endpoint_envelope.py -v` | Every commit |
| Multi-judge live smoke (`AKOS_RECORD_LIVE=1 AKOS_JUDGE_ROSTER=<csv>`) on 5 scenarios | P3 + P8 |
| `py scripts/endpoint_cost_probe.py` returns live endpoint inventory | P5 + ongoing |
| `aggregate_judge_cost_under_cap` enforces per-run + per-endpoint caps; **unit-mismatch raises** | P7 + every commit (offline) |
| `dossier --filter madeira` shows worst-axis trend + endpoint cost subsection | P6 + P8 |
| Tier-B weekly run honors `MAX_JUDGE_USD_PER_RUN` and per-endpoint envelopes | P7 first run + ongoing |

## Operator approval gates

- **G-52-1** (P1) — Initial multi-judge roster (model selection); updates `AKOS_JUDGE_ROSTER` env documentation in `SOP` and `USER_GUIDE`.
- **G-52-2** (P4, conditional) — `POL-EVAL-JUDGE-THRESHOLD-*` edits or per-axis routing overrides.
- **G-52-3** (P7) — Multi-judge active in Tier-B CI with budget envelopes.
- **G-52-4** (P5) — `POL-EVAL-COST-CEILING-ENDPOINT-*-V1` per-endpoint envelopes (operator sets `max_usd_per_day` per endpoint type).

## Decisions seeded

See [`decision-log.md`](decision-log.md). Six decisions D-IH-52-A..F.

## Risks (R-52-1..6)

See [`risk-register.md`](risk-register.md).

## Reporting artefacts

- `reports/p<N>-*-YYYY-MM-DD.md` per phase
- `reports/judge-live-calibration-YYYY-MM-DD.md` (P3)
- `reports/uat-i52-multi-model-judge-and-cost-discipline-YYYY-MM-DD.md` (P8 closure)

## Cross-cutting

- Decision IDs: `D-IH-52-A` through `D-IH-52-F` (6 seeded; defaults documented in [`decision-log.md`](decision-log.md)).
- `language: en` frontmatter on all vault docs.
- WIP_DASHBOARD picks this row up automatically.
- CHANGELOG entry on closure (P8).

## What this is NOT

- Building our own LLM judge model (we use vendor models + roster discipline).
- Public benchmark adoption (D-DEFER-47-γ stays deferred).
- Replacing the offline rubric (offline stays as cassette-replay default).
- Auto-purchasing or auto-renting GPU capacity (alarm-only by default; operator decides on scale).
- A wholesale FinOps replacement; this is judge + endpoint cost discipline only.
