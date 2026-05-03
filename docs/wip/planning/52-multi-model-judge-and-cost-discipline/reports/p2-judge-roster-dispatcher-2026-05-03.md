---
language: en
status: complete
initiative: 52-multi-model-judge-and-cost-discipline
report_kind: phase-report
phase: P2
decision_executed: D-IH-52-A
last_review: 2026-05-03
authority: Founder
---

# I52 / P2 — Multi-judge dispatcher (`JudgeRoster`)

**Date:** 2026-05-03
**Phase scope:** Replace `NotImplementedError` in `akos.eval_harness.judge.score_response_live` with a roster-driven dispatcher; gate live mode on `AKOS_JUDGE_ROSTER` env; preserve CI-safe offline default.
**Plan reference:** §"Initiative 52" P2 of the master roadmap.

## Outcome

- New module surface in `akos/eval_harness/judge.py`:
  - `JudgeRoster` dataclass (`from_env`, `score`, `fingerprint`).
  - `MemberScore` dataclass (per-member raw output + per-axis notes + cost).
  - `MemberScorer` callable type alias (test-injection seam).
  - `_default_member_scorer` (per-provider dispatch with offline fallback).
  - `_call_member_via_api` (placeholder; raises NotImplementedError; activated in P3 calibration burn).
  - `_compose_consensus`, `_compose_per_axis`, `_compose_tiered` composition functions.
  - `JUDGE_ROSTER_ENV`, `JUDGE_ROSTER_CHEAP_ENV`, `JUDGE_MODE_ENV`, `VALID_JUDGE_MODES`, `DEFAULT_JUDGE_MODE` module constants.
- `score_response_live` now routes through `JudgeRoster.score(...)` when `AKOS_JUDGE_ROSTER` is set; raises `NotImplementedError` with an actionable message when it isn't (preserves the I47/P12 contract that live mode is gated, not silent).
- Operator-facing `score_response` dispatcher decision tree updated:
  1. `AKOS_RECORD_LIVE != "1"` → offline (CI default).
  2. `AKOS_JUDGE_ROSTER` set → `JudgeRoster` (multi-model consensus).
  3. `AKOS_JUDGE_MODEL` set → single-model fallback (raises until roster-or-model env set).
  4. Else → offline.
- New test suite [`tests/test_eval_judge_multi.py`](../../../../tests/test_eval_judge_multi.py) — 32 tests covering env construction, fingerprint, consensus, per-axis, tiered, member fallback, dispatcher routing, reproducibility.
- Updated 1 pre-existing test in [`tests/test_eval_judge.py`](../../../../tests/test_eval_judge.py) (the `NotImplementedError` regex changed from `gated` to `AKOS_JUDGE_ROSTER`; the gating semantics are preserved — only the message text changed).

## Test results

| Suite | Tests | Result |
|:------|:--:|:--|
| `tests/test_eval_judge.py` (pre-existing; +1 patched) | 24 | **24 / 24 PASS** |
| `tests/test_eval_judge_multi.py` (new) | 32 | **32 / 32 PASS** |

Combined: **56 / 56 PASS** in 0.22s.

## Design notes

### Why a `MemberScorer` test-injection seam

`JudgeRoster.score(...)` accepts an optional `member_scorer: MemberScorer | None` kwarg. Production callers leave it `None` and the default scorer (`_default_member_scorer`) dispatches per-provider. Tests inject a deterministic stub. This isolates:

- **CI semantics**: tests never need API keys to run; scoring is deterministic.
- **Cassette layer**: the real API call is wrapped in `_call_member_via_api`, which currently raises `NotImplementedError` — the default scorer catches and falls back to offline with `fallback_offline=True` and `raw_error` populated. Operator can read the error from `JudgeResult.notes` without burning credentials.

### Why fingerprint is in `JudgeResult.model_id`

The cassette layer needs a stable, queryable identifier per scoring run. Putting `roster[a:1,b:2]/mode=consensus` in `model_id` (instead of just `"live"`) means cassettes can be filtered by roster identity and we can detect cassette↔roster mismatches without parsing notes.

### Per-axis composition routes a missing axis to position-1

If `per_axis_routing` is empty or doesn't contain a given axis, `_compose_per_axis` falls through to position-1's score for that axis. This preserves the operator's ability to phase-in per-axis routing one axis at a time.

### Tiered mode collapses to position-1 at P2

The full cost-aware tiered escalation logic (cheap members first; flagship only on disagreement or low-confidence) requires alignment data per axis per member, which arrives at P3. The P2 implementation is a placeholder that returns position-1's scores so the dispatcher contract is exercised end-to-end without baking in the wrong escalation heuristic.

### `_call_member_via_api` is intentionally NotImplementedError

Activating real Anthropic / OpenAI HTTP calls before the P3 calibration burn would conflate two debugging surfaces (does the dispatcher work? do the live calls work?). The default scorer catches the NotImplementedError and falls back to offline with `fallback_offline=True`, so the dispatcher contract is exercised with the full code path of a "live" model_id without burning credentials. P3 will replace the body with stdlib-urllib HTTP calls (symmetric with I47/P13 item 4 `eval_run_writer`).

## Carrier closes / forwards

- **OPS-47-8 (LLM-judge live mode + pin model_id):** **closes architecturally** at this phase — the dispatcher is wired and gated by `AKOS_JUDGE_ROSTER`; the operator-pinned roster lives in a governed file (P1). Activating real API calls is a P3 deliverable, but the P2 dispatcher is the keystone contract and the carrier is now blocked only on calibration evidence, not architecture.
- **Forwards (to P3):** real `_call_member_via_api` body; calibration burn against 50 representative scenarios; D-IH-52-B activation decision (consensus / per-axis / tiered).

## Verification

```text
$ py -m pytest tests/test_eval_judge.py tests/test_eval_judge_multi.py -q
........................................................                 [100%]
56 passed in 0.22s

$ py scripts/check-drift.py
  No drift detected. Runtime matches repo state.
```

## Cross-references

- Decision: D-IH-52-A in [`decision-log.md`](../decision-log.md).
- Predecessor phase: [`p1-roster-survey-2026-05-03.md`](p1-roster-survey-2026-05-03.md).
- Code: [`akos/eval_harness/judge.py`](../../../../akos/eval_harness/judge.py).
- Tests: [`tests/test_eval_judge_multi.py`](../../../../tests/test_eval_judge_multi.py).
- Roster contract: [`prompts/judge/JUDGE_ROSTER_V1.md`](../../../../prompts/judge/JUDGE_ROSTER_V1.md).
- Prompt contract: [`prompts/judge/JUDGE_PROMPT_V1.md`](../../../../prompts/judge/JUDGE_PROMPT_V1.md).
