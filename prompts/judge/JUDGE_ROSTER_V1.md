---
language: en
status: active
initiative: 52-multi-model-judge-and-cost-discipline
phase: P1
decision_executed: D-IH-52-A
gate_evaluated: G-52-1
last_review: 2026-05-03
authority: Founder
---

# JUDGE_ROSTER_V1 — Initial multi-model LLM-judge roster (G-52-1)

**Initiative:** I52 P1 (`docs/wip/planning/52-multi-model-judge-and-cost-discipline/`).
**Decision:** [D-IH-52-A](../../docs/wip/planning/52-multi-model-judge-and-cost-discipline/decision-log.md#d-ih-52-a--initial-multi-judge-roster).
**Gate:** **G-52-1 (this file is the gate artefact).**

## Why a roster, not a single pin

I47/P12 set up `akos/eval_harness/judge.py` with `score_response_offline` (deterministic; ships) + `score_response_live` (raises `NotImplementedError`). At I47/P12 closure, R-47-10 ("LLM-judge sycophancy") was an open mitigation: a single-model live pin would replicate one provider's blind spots into our brand-voice + citation + persona_fit signals. **Multi-model is a brand promise** and a sycophancy mitigation in the same move.

**The roster is the unit of operator agency:** it carries identity (`model_id`s), composition mode (consensus / per-axis / cost-aware tiered), and per-axis priority. CI consumes it via `AKOS_JUDGE_ROSTER` env (comma-separated `model_id` list).

## Members at launch

Two flagship judges, one per provider, for cross-provider sanity at predictable per-token cost.

| Position | `model_id` | Provider | Tier | `model-prices.json` row | Notes |
|:--:|:--|:--|:--|:--|:--|
| 1 | `anthropic:claude-3-5-sonnet-20241022` | Anthropic | flagship | present | Released 2024-10-22; 2026-Q2 pricing $3/M in + $15/M out (verified I50/P2). Tie-break primary. |
| 2 | `openai:gpt-4o` | OpenAI | flagship | present | 2026-Q2 pricing $2.50/M in + $10/M out (verified I50/P2). **Legacy classification per OpenAI 2026-Q2** — superseded by gpt-5.x; pricing retained for cassette reproducibility. Tie-break secondary. |

### Roster string

```text
AKOS_JUDGE_ROSTER="anthropic:claude-3-5-sonnet-20241022,openai:gpt-4o"
```

### Ordering convention

Position 1 wins ties under the default consensus mode (D-IH-52-B). Position is **stable** — adding a member at the end of the list does not reshuffle existing positions, so cassette reproducibility holds across roster expansion.

## Composition modes (D-IH-52-B)

| Mode | Active at I52 P2 launch | Activation criterion |
|:--|:--:|:--|
| **Consensus voting (default)** | YES | All axes; majority rule; ties → position-1 wins |
| Per-axis specialization | NO (deferred) | P3 calibration burn shows axis-specific gaps |
| Cost-aware tiered escalation | NO (deferred) | P3 calibration burn proves it cheaper than pure-flagship |

The dispatcher in `akos/eval_harness/judge.py` (P2 deliverable) MUST support all three modes from day one. Only one is activated at launch; the rest are flag-flipped post-P3 if evidence supports them.

## Cheap-tier opt-in

Operator may A/B against cheap-tier consensus by setting:

```text
AKOS_JUDGE_ROSTER_CHEAP="openai:gpt-4o-mini"
```

Cheap-tier roster is **not active by default**. When set, it produces a **shadow scorecard** that is logged but does not gate. Promotion to primary roster is an explicit P3 / P4 decision based on alignment.

## Per-endpoint judge eligibility

Per-endpoint (RunPod / Kalavai-hosted) judges are eligible for inclusion **after** P3 calibration burn confirms ≥80% alignment with the per-token roster. Initial roster is per-token-only to isolate the multi-model dispatcher signal from the GPU-hour cost-discipline signal (P5).

## Reproducibility contract

- Every cassette MUST capture the full roster `model_id` list at recording time.
- Cassette retention is governed by [D-IH-52-F](../../docs/wip/planning/52-multi-model-judge-and-cost-discipline/decision-log.md#d-ih-52-f--cassette-retention-for-multi-judge-cassettes) — kept until any roster `model_id` is rotated.
- Roster rotation triggers a re-baseline burn before old cassettes are expired.

## Roster rotation cadence

- **Quarterly review** (aligned with I50/P2 `_2026_q2_review_note` cadence on `model-prices.json`).
- **Out-of-band rotation** when any provider deprecates a member or releases a flagship rev that supersedes the current pin.
- **Operator approval (G-52-1)** required for every rotation — this file is the audit trail.

## Cross-references

- [`config/eval/model-prices.json`](../../config/eval/model-prices.json) — every `model_id` here MUST have a row there (no silent zero-cost fallback for judges).
- [`POLICY_REGISTER.csv`](../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/POLICY_REGISTER.csv) — `POL-EVAL-JUDGE-THRESHOLD-{BRAND_VOICE,CITATION,PERSONA_FIT}-V1` (`min_pass_score=4`) gate the dispatcher's pass/fail verdict.
- [`prompts/judge/JUDGE_PROMPT_V1.md`](JUDGE_PROMPT_V1.md) — the system prompt sent to every roster member.
- I52 master roadmap: [`master-roadmap.md`](../../docs/wip/planning/52-multi-model-judge-and-cost-discipline/master-roadmap.md).

## Operator-pending follow-ups (from this file)

1. Rotate Position 2 (`openai:gpt-4o` → current OpenAI flagship) when operator confirms the gpt-5.x pricing entries are stable enough to add a `model-prices.json` row + re-record cassettes. Captured here as the first known rotation candidate; **does not block I52 P2 dispatcher implementation.**
2. After P3 calibration burn, decide D-IH-52-B (consensus default vs per-axis specialization vs cost-aware tiered escalation).

## Approval

| Field | Value |
|:------|:------|
| Authored | 2026-05-03 (I52 P1) |
| Approved by | Founder |
| Effective | I52 P2 launch (P2 dispatcher reads this file's roster string) |
| Next review | Quarterly + on any provider rotation event |
