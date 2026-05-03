---
language: en
status: complete
initiative: 52-multi-model-judge-and-cost-discipline
report_kind: phase-report
phase: P1
decision_executed: D-IH-52-A
gate_evaluated: G-52-1
last_review: 2026-05-03
authority: Founder
---

# I52 / P1 — Roster survey + selection (G-52-1)

**Date:** 2026-05-03
**Phase scope:** D-IH-52-A — pick the initial multi-judge roster and commit it to a governed file at `prompts/judge/JUDGE_ROSTER_V1.md`. **G-52-1 GREEN.**
**Plan reference:** §"Initiative 52" P1 of the master roadmap.

## Outcome

Initial roster pinned at **N=2 flagship consensus across two providers** (D-IH-52-A default executed):

| Position | `model_id` | Tier | Provider |
|:--:|:--|:--|:--|
| 1 | `anthropic:claude-3-5-sonnet-20241022` | flagship | Anthropic |
| 2 | `openai:gpt-4o` | flagship | OpenAI |

Roster string: `AKOS_JUDGE_ROSTER="anthropic:claude-3-5-sonnet-20241022,openai:gpt-4o"`.

Two new vault assets:

- [`prompts/judge/JUDGE_ROSTER_V1.md`](../../../../prompts/judge/JUDGE_ROSTER_V1.md) — the gate artefact for G-52-1; pins members, composition modes, opt-in cheap-tier, per-endpoint eligibility rules, reproducibility contract.
- [`prompts/judge/JUDGE_PROMPT_V1.md`](../../../../prompts/judge/JUDGE_PROMPT_V1.md) — the system prompt every roster member receives; output schema is JSON-only; malformed output triggers offline fallback.

## Why these two members

**Cross-provider consensus is the brand promise.** Operator direction (2026-05-03): "All models we can — we praise ourselves on being multi-model." Single-pin live mode would replicate one provider's blind spots (R-47-10 sycophancy). N=2 flagship across providers gives consensus + cross-provider sanity check at predictable per-token cost (no GPU-hour surprise).

**`anthropic:claude-3-5-sonnet-20241022`** — present in `config/eval/model-prices.json` at $3/M in + $15/M out (verified I50/P2 against 2026-Q2 published rates). Position 1 by tie-break convention.

**`openai:gpt-4o`** — present in `config/eval/model-prices.json` at $2.50/M in + $10/M out (verified I50/P2). **Legacy classification per OpenAI 2026-Q2** (superseded by gpt-5.x), but pricing retained for cassette reproducibility per I50/P2 `_2026_q2_review_note`. The legacy status is noted explicitly in `JUDGE_ROSTER_V1.md` and is the first known rotation candidate for the next quarterly review.

## What was deliberately deferred

| Surface | Status | Rationale |
|:------|:------|:----------|
| Mistral / Cohere / Vertex | Not added at launch | Adds cost without clear consensus-quality benefit at N=2; revisit at P3 burn |
| RunPod-hosted / Kalavai-hosted judges | Not added at launch | Eligible only after P3 confirms ≥80% alignment with per-token roster; isolating the multi-model dispatcher signal from the GPU-hour cost-discipline signal (P5) is cleaner |
| `openai:gpt-4o-mini` cheap-tier | Documented as opt-in via `AKOS_JUDGE_ROSTER_CHEAP` env | Produces a shadow scorecard; non-gating until promotion to primary (P3 / P4 decision) |

## Composition modes

The roster file pre-declares all three composition modes (consensus / per-axis / cost-aware tiered) so the P2 dispatcher must support all three from day one:

| Mode | Active at I52 P2 launch | Activation criterion |
|:--|:--:|:--|
| **Consensus voting (default)** | YES | All axes; majority rule; ties → position-1 wins |
| Per-axis specialization | NO (deferred) | P3 calibration burn shows axis-specific gaps |
| Cost-aware tiered escalation | NO (deferred) | P3 calibration burn proves it cheaper than pure-flagship |

## Roster rotation cadence

- **Quarterly review** (aligned with I50/P2 `_2026_q2_review_note` cadence on `model-prices.json`).
- **Out-of-band rotation** when any provider deprecates a member or releases a flagship rev that supersedes the current pin.
- **Operator approval (G-52-1)** required for every rotation — `JUDGE_ROSTER_V1.md` is the audit trail.

## Cost discipline contract (for P2 dispatcher)

The P2 dispatcher MUST:

1. Read the roster from `AKOS_JUDGE_ROSTER` env var (comma-separated `model_id` list).
2. For each scenario, score against every roster member with the same `JUDGE_PROMPT_V1.md` system prompt.
3. Capture every member's raw output + the prompt's `sha256` in the cassette.
4. Apply the active composition mode (default consensus).
5. Track per-member cost via `model-prices.json` lookup; refuse to score if any roster member's `model_id` is missing from `model-prices.json` (no silent zero-cost fallback for judges).
6. Aggregate to `JudgeResult.cost_usd` summed across roster members; `aggregate_judge_cost_under_cap` continues to enforce the per-scenario cap.

The `MAX_JUDGE_USD_PER_RUN` envelope (D-IH-52-C; default $15 for N=2 consensus) wires into Tier-B in P7, not P2.

## Verification

| Check | Result |
|:------|:------|
| `JUDGE_ROSTER_V1.md` exists with `language: en` frontmatter | OK |
| `JUDGE_PROMPT_V1.md` exists with `language: en` frontmatter | OK |
| Both members in `model-prices.json` with non-zero per-token rates | OK (`anthropic:claude-3-5-sonnet-20241022` + `openai:gpt-4o`) |
| `py scripts/validate_hlk.py` (LANGUAGE_FRONTMATTER pass) | PASS |
| `py scripts/check-drift.py` | PASS (no schema drift) |
| Roster string round-trips through `AKOS_JUDGE_ROSTER` env (formal contract) | Will be exercised by the P2 dispatcher tests |

## Operator-pending follow-ups (carried to P2/P3)

1. P2 dispatcher reads `AKOS_JUDGE_ROSTER` env at runtime; default at unset → `score_response_offline` (preserves CI semantics).
2. P3 calibration burn produces alignment numbers per axis per member; D-IH-52-B activation decision (consensus / per-axis / tiered) lands at P3 closure.
3. Rotation candidate: `openai:gpt-4o` → current OpenAI flagship (gpt-5.x family) when operator confirms a stable `model-prices.json` entry. Captured in `JUDGE_ROSTER_V1.md` as the first known rotation candidate; **does not block I52 P2 dispatcher implementation**.

## Carrier closes / forwards

- **Closes (this phase):** none yet (G-52-1 fires this phase; OPS-47-8 closes at P2 once dispatcher replaces `NotImplementedError`).
- **Forwards (to P2):** `JUDGE_ROSTER_V1.md` becomes the dispatcher's input contract.
- **Forwards (to P3):** roster string becomes the calibration-burn target.

## Cross-references

- Decision: D-IH-52-A in [`decision-log.md`](../decision-log.md).
- Evidence: E1, E7 in [`evidence-matrix.md`](../evidence-matrix.md).
- Predecessor phase: I52 P0 bootstrap (this folder's six governance artefacts).
- Roster: [`prompts/judge/JUDGE_ROSTER_V1.md`](../../../../prompts/judge/JUDGE_ROSTER_V1.md).
- Prompt: [`prompts/judge/JUDGE_PROMPT_V1.md`](../../../../prompts/judge/JUDGE_PROMPT_V1.md).
- Cost SSOT: [`config/eval/model-prices.json`](../../../../config/eval/model-prices.json).
