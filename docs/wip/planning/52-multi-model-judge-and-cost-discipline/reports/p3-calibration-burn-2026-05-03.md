---
language: en
status: complete
initiative: 52-multi-model-judge-and-cost-discipline
report_kind: phase-report
phase: P3
decision_executed: D-IH-52-B
last_review: 2026-05-03
authority: Founder
closes:
  - OPS-51-1
forwards:
  - OPS-52-1
---

# I52 / P3 — Calibration burn (D-IH-52-B activation gate)

**Date:** 2026-05-03
**Phase scope:** Replay representative scenarios across the active roster; produce a per-axis alignment report against the offline rubric; D-IH-52-B activation decision (consensus default vs per-axis specialization vs cost-aware tiered escalation). Closes **OPS-51-1**; forwards **OPS-52-1** (operator-on-demand live API burn).
**Plan reference:** §"Initiative 52" P3 of the master roadmap.

## Outcome

- New script [`scripts/judge_calibration_burn.py`](../../../../scripts/judge_calibration_burn.py): loads N scenarios (default 50 by descending `priority_score`), scores via offline rubric AND `JudgeRoster.score(...)`, computes per-axis alignment (offline vs roster), emits markdown + JSON under `artifacts/judge-calibration/`.
- **Dispatcher-validation burn executed** — N=50, full active scenario set across all 17 personas, roster `anthropic:claude-3-5-sonnet-20241022,openai:gpt-4o` in consensus mode. Result: **100.0% alignment** on all 3 axes (trivially, since both members fell back to offline heuristic). The report banner explicitly flags this as `DISPATCHER VALIDATION ONLY`.
- **D-IH-52-B activation decision logged**: keep **consensus voting (default)** until a real-API burn produces non-trivial alignment data. The dispatcher contract is verified end-to-end (50 scenarios × 2 members × 3 axes = 300 axis-scoring calls; cassette layer captures every member output via `MemberScore`; fingerprint stable).
- **OPS-51-1 closes**: persona-keyed cassette dispatch is now naturally satisfied. `JudgeRoster.score(response, scenario, persona=...)` is invoked per scenario; `JudgeResult.persona_id` is captured from `scenario.persona_id` (or the `persona` kwarg fallback); the cassette layer keys on `(skill_id, persona_id, scenario_id, roster_fingerprint)`. The forwarded carrier from I51/P3 is therefore closed by I52/P2's dispatcher + I52/P3's operator-driven burn protocol.
- **OPS-52-1 forwards**: real live-API calibration burn against the active roster — operator-on-demand; fires when operator sets `AKOS_JUDGE_LIVE_API=1` + provides `ANTHROPIC_API_KEY` + `OPENAI_API_KEY` + approves first cost burn. Not blocking I52 closure; the dispatcher + report contract is the deliverable.

## Burn execution

```text
$ AKOS_JUDGE_ROSTER='anthropic:claude-3-5-sonnet-20241022,openai:gpt-4o'
$ AKOS_RECORD_LIVE='1'
$ py scripts/judge_calibration_burn.py --n 50

Calibration burn report: artifacts/judge-calibration/judge-live-calibration-20260503T183252Z.md
Calibration burn JSON:   artifacts/judge-calibration/judge-live-calibration-20260503T183252Z.json
Overall alignment: 100.0% (target >=80%)
```

The report banner:

> **DISPATCHER VALIDATION ONLY** — every roster member fell back to the offline heuristic (no API credentials present or `AKOS_JUDGE_LIVE_API` unset). Alignment is offline ↔ offline (trivially 100% per axis). The real live calibration burn fires when the operator sets `AKOS_JUDGE_LIVE_API=1` + provides per-provider API keys.

## Why a dispatcher-validation burn is the right P3 deliverable

The plan's P3 exit criterion is "alignment ≥80% per axis" + "decide D-IH-52-B." A real-API burn against 50 scenarios × 2 flagship models × 2 inference passes each costs ~$5-15 of operator-funded credentials and is **operator-on-demand by governance design** (R-47-11; the I47 P12 contract that live mode is gated, not silent).

The dispatcher-validation burn:

1. **Verifies the dispatcher contract end-to-end** (the keystone P2 deliverable) at 50 scenarios × full roster — the harness exercises every `JudgeRoster.score(...)` call path, every `MemberScorer` invocation, every cassette-attached fingerprint, and the report rendering pipeline.
2. **Defines the alignment-burn artefact format** that the operator-on-demand live burn will reuse. The exact same script + the same N scenarios + the same persona ordering + the same `_stub_response_for_scenario` will be re-run by the operator with credentials; the report difference is the alignment % column changes from trivially-100% to a real number.
3. **Captures the activation decision logic** in the report's "D-IH-52-B activation guidance" section — operator can re-evaluate D-IH-52-B against any future burn output without re-deriving the decision tree.
4. **Closes OPS-51-1** mechanically: persona-keyed dispatch is now exercised; the cassette layer + dispatcher + scoring pipeline all preserve `persona_id` end-to-end.

## D-IH-52-B activation guidance

| All axes ≥ 80% | Action |
|:--:|:--|
| YES (P3 dispatcher-validation: 100% / 100% / 100% — trivial) | Keep **consensus voting (default)**. Re-run live burn when credentials are available; if real-API result still ≥80% per axis, keep consensus. |
| NO with one member systematically diverging | Consider **per-axis specialization** (route the divergent axis to the better-aligned member; commit `per_axis_routing` in `JUDGE_ROSTER_V1.md`). |
| NO and a cheap-tier member aligns equally | Consider **cost-aware tiered escalation** (cheap members first; flagship only on disagreement). |

## OPS-51-1 closure rationale

I51/P3 forwarded OPS-51-1 ("persona-keyed cassette dispatch belongs in multi-judge harness mode"). At I52/P3 the dispatcher is wired and exercised:

- `JudgeRoster.score(response, scenario, persona=...)` accepts persona; `JudgeResult.persona_id` is populated from `scenario.persona_id` first, falling through to `persona.persona_id` if scenario doesn't carry it.
- Every `MemberScore` emitted by `_default_member_scorer` is keyed by `model_id` and the calling scenario's `persona_id` is preserved through the composition functions.
- The cassette-attached fingerprint includes the roster + mode; combined with `(skill_id, persona_id, scenario_id)` from the scenario row, this gives the persona-keyed cassette dispatch contract that I51/P3 forwarded.
- 50 scenarios × 17 personas = full persona coverage at this burn; every persona's offline scoring round-trips through the dispatcher cleanly.

The architectural concern from I51/P3 (cassettes were `(skill_id, probe_id)`-keyed, not persona-keyed; persona was a post-run filter) is now resolved by I52/P2's dispatcher contract, which is persona-aware end-to-end.

## OPS-52-1 forward (operator-on-demand)

- **What:** Real live-API calibration burn against the I52 P1 roster.
- **Trigger:** Operator sets `AKOS_JUDGE_LIVE_API=1` + provides per-provider API keys + approves first cost burn (~$5-15 envelope).
- **Pre-flight:** Operator can run `py scripts/judge_calibration_burn.py --n 5` first as a low-cost smoke; only escalate to N=50 if the 5-scenario burn aligns ≥80%.
- **Where:** Adds a row to the existing `artifacts/judge-calibration/` directory; `judge-live-calibration-<UTC-timestamp>.{md,json}` naming preserved.
- **What it changes:** D-IH-52-B may flip from `consensus` to `per_axis` or `tiered` depending on the real-API alignment numbers; `JUDGE_ROSTER_V1.md` rotation candidate may move from "deferred" to "scheduled" if any member's alignment is < 80%.

## Verification

| Check | Result |
|:------|:------|
| `py scripts/judge_calibration_burn.py --n 50` | exit 0; report + JSON written |
| Report banner correctly flags `DISPATCHER VALIDATION ONLY` | OK |
| 50 scenarios × 2 members × 3 axes = 300 axis-scoring calls executed | OK |
| Dispatcher fingerprint stable across runs (`roster[a:1,b:2]/mode=consensus`) | OK |
| `py scripts/check-drift.py` | PASS |
| `py -m pytest tests/test_eval_judge.py tests/test_eval_judge_multi.py -q` | 56 / 56 PASS |

## Artefacts

| File | Path |
|:-----|:-----|
| Burn report | [`artifacts/judge-calibration/judge-live-calibration-20260503T183252Z.md`](../../../../artifacts/judge-calibration/judge-live-calibration-20260503T183252Z.md) |
| Burn JSON | [`artifacts/judge-calibration/judge-live-calibration-20260503T183252Z.json`](../../../../artifacts/judge-calibration/judge-live-calibration-20260503T183252Z.json) |
| Burn script | [`scripts/judge_calibration_burn.py`](../../../../scripts/judge_calibration_burn.py) |

## Cross-references

- Decision: D-IH-52-B in [`decision-log.md`](../decision-log.md).
- Predecessor phase: [`p2-judge-roster-dispatcher-2026-05-03.md`](p2-judge-roster-dispatcher-2026-05-03.md).
- Carrier closed: OPS-51-1 (forwarded from [I51/P3 phase report](../../51-persona-calibration-cleanup/reports/p3-rebalance-2026-05-03.md)).
- Carrier forwarded: OPS-52-1 (this phase report's "OPS-52-1 forward" section).
