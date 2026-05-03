---
language: en
status: active
initiative: 52-multi-model-judge-and-cost-discipline
report_kind: decision-log
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 52 — Decision log

Six decisions seeded with defaults per the cursor plan; operator-ratified at greenlight 2026-05-03 ("All models we can — we praise ourselves on being multi-model. Cost management for RunPod / Kalavai endpoints.").

## D-IH-52-A — Initial multi-judge roster

**Decision (default):** **Anthropic Sonnet + OpenAI gpt-4o (N=2 flagship consensus).** `AKOS_JUDGE_ROSTER="anthropic:claude-3-5-sonnet,openai:gpt-4o"` at launch.

**Alternatives considered:**

- N=1 single-model pin (rejected — operator direction is "all models we can"; single pin is a known sycophancy risk per R-47-10).
- N=3 (1 Anthropic + 1 OpenAI + 1 cheap-tier) (deferred — adds cost without clear consensus-quality benefit; revisit at P3 burn).
- Per-endpoint judges (RunPod/Kalavai-hosted models) (deferred — eligible for inclusion if alignment ≥80% in P3 burn).

**Rationale:** N=2 across providers gives consensus + cross-provider sanity check at predictable per-token cost (no GPU-hour surprise). Cheap-tier opt-in via `AKOS_JUDGE_ROSTER_CHEAP` env preserves operator agency to A/B against flagship.

**Reversibility:** High — env-var roster; no code change to swap.

---

## D-IH-52-B — Default judging mode

**Decision (default):** **Consensus voting (N=2; tie → tier-priority order).**

**Alternatives considered:**

- Per-axis specialization (deferred — only if P3 burn shows axis-specific gaps).
- Cost-aware tiered escalation (deferred — only if P3 burn proves cheaper than pure-flagship).

**Rationale:** Consensus voting is the most operator-explainable pattern (majority wins; ties broken by a documented priority list). Specialization and tiered escalation are optimizations that should follow evidence, not precede it.

**Reversibility:** High — pattern is a JudgeRoster constructor parameter; no schema change to switch.

---

## D-IH-52-C — `MAX_JUDGE_USD_PER_RUN` envelope

**Decision (default):** **$15 for N=2 consensus** (scales linearly with roster size).

**Rationale:** I47/P12 set `--judge-cost-cap 0.01` per-scenario. A Tier-B run averages ~50-100 scenarios across the matrix; 100 × $0.01 × 2 models = $2 for cheap-tier consensus, ~$10-15 for flagship consensus. $15 is a 1.5x headroom over expected flagship spend. Tier-B persona matrix already caps at `MAX_PERSONA_USD=$1` per cell, so a 5-persona × 2-model_tier × 2-judge run hard-caps at $20 even before this envelope; the new envelope is a defense-in-depth.

**Reversibility:** High — env-var override per workflow_dispatch input.

---

## D-IH-52-D — Endpoint envelope policy (`max_usd_per_day` per endpoint)

**Decision (default):** **$20/day RunPod, $10/day Kalavai** (operator may set per actual deployment via POLICY row edits).

**Rationale:** RunPod 2026-Q2 H100 SXM pricing ≈$2.39/hr; 24h ÷ $20/day = ~8.3 hours of H100 uptime allowed. Operator can scale up envelope for sustained training runs by editing the POLICY row + re-running mirror reseed. Kalavai is community-priced (typically lower), so smaller default; preserves operator agency while preventing silent overspend.

**Reversibility:** High — POLICY rows are CSV-edit + reseed-driven; no code change.

---

## D-IH-52-E — Endpoint envelope breach action

**Decision (default):** **Alarm-only (operator manual scale-down)**; auto-pause-via-API is opt-in once API contracts are pinned and tested under load.

**Rationale:** Auto-pause carries R-52-6 (operator under-sets envelope and CI pauses production endpoint). Alarm-only is safer at I52 launch; operator opts into auto-pause per-endpoint via POLICY row flag once they've calibrated the per-endpoint envelope against actual usage.

**Reversibility:** High — flag on POLICY row.

---

## D-IH-52-F — Cassette retention for multi-judge cassettes

**Decision (default):** **Keep until any roster `model_id` is rotated**; expiry rule documented in SOP-EVAL_HARNESS_001 §X (TBD-P8).

**Rationale:** Cassettes are reproducibility artefacts. When a roster member's `model_id` changes (provider rev), the old cassettes become non-reproducible against the new roster. Expiring them on rotation prevents stale cassette drift; preserving them across non-rotation cycles preserves operator forensic ability.

**Reversibility:** Medium — expiry policy is an operator-driven cleanup (no auto-delete); preserved cassettes can always be re-evaluated against archived roster state.

---

## Decisions made during execution

### 2026-05-03 — P2 multi-judge dispatcher landed; OPS-47-8 closes architecturally

I52/P2 lands the `JudgeRoster` dispatcher in `akos/eval_harness/judge.py`:
- `JudgeRoster` (`from_env`, `score`, `fingerprint`)
- `MemberScore` + `MemberScorer` test-injection seam
- `_compose_consensus` + `_compose_per_axis` + `_compose_tiered` (consensus
  active by default; per-axis routes through `per_axis_routing` dict; tiered
  collapses to position-1 until P3 alignment data arrives)
- `_default_member_scorer` (per-provider dispatch with offline fallback;
  catches NotImplementedError from `_call_member_via_api` placeholder)
- 32 new tests in `tests/test_eval_judge_multi.py` (32 / 32 PASS); 1
  pre-existing test in `tests/test_eval_judge.py` patched for the new
  NotImplementedError message; combined 56 / 56 PASS.

`score_response_live` no longer raises blanket NotImplementedError — it
routes through `JudgeRoster.score(...)` when `AKOS_JUDGE_ROSTER` is set
and raises an actionable NotImplementedError when it isn't. Operator-
facing `score_response` decision tree: offline (CI default) → roster
(if `AKOS_RECORD_LIVE=1` AND `AKOS_JUDGE_ROSTER` set) → single-model
(legacy path; preserved) → offline.

**OPS-47-8 closes architecturally** — the dispatcher is wired and gated
by `AKOS_JUDGE_ROSTER`; the operator-pinned roster lives in
`prompts/judge/JUDGE_ROSTER_V1.md` (P1). Activating real API calls is a
P3 deliverable, but the P2 dispatcher is the keystone contract; the
carrier is now blocked only on calibration evidence, not architecture.

Phase report: [`reports/p2-judge-roster-dispatcher-2026-05-03.md`](reports/p2-judge-roster-dispatcher-2026-05-03.md).

### 2026-05-03 — P1 D-IH-52-A executed; G-52-1 GREEN

I52/P1 lands the initial multi-judge roster as committed at
[`prompts/judge/JUDGE_ROSTER_V1.md`](../../../prompts/judge/JUDGE_ROSTER_V1.md):

- Position 1: `anthropic:claude-3-5-sonnet-20241022` (flagship; tie-break primary)
- Position 2: `openai:gpt-4o` (flagship; tie-break secondary; legacy classification per OpenAI 2026-Q2 — first known rotation candidate)

Both members pinned in `config/eval/model-prices.json` with non-zero
per-token rates (verified I50/P2 against 2026-Q2 published rates).
Composition modes (consensus / per-axis / cost-aware tiered) are
pre-declared in the roster file so the P2 dispatcher must support all
three from day one — only consensus is active at launch.

Cheap-tier (`openai:gpt-4o-mini`) and per-endpoint (RunPod / Kalavai)
judges are documented as opt-in via `AKOS_JUDGE_ROSTER_CHEAP` env and
P3 calibration-burn eligibility respectively. The system prompt
[`prompts/judge/JUDGE_PROMPT_V1.md`](../../../prompts/judge/JUDGE_PROMPT_V1.md)
is JSON-schema-locked; malformed roster output triggers offline
fallback.

Phase report: [`reports/p1-roster-survey-2026-05-03.md`](reports/p1-roster-survey-2026-05-03.md).

_Append further phased ratifications below as they land._
