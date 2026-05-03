# `artifacts/judge-calibration/`

**Initiative 52 P3 deliverable** — multi-judge calibration burn output directory.

## What lives here

`judge-live-calibration-<UTC-timestamp>.{md,json}` pairs emitted by `scripts/judge_calibration_burn.py`. Each pair is a per-axis alignment report between the offline rubric and the active `JudgeRoster`-composed score across N representative scenarios.

## Gitignore posture

The `*.md` and `*.json` files are gitignored (regenerable). Only this `README.md` is committed.

## Operator workflow

```text
# 1. Pin the roster (per JUDGE_ROSTER_V1.md):
$env:AKOS_JUDGE_ROSTER='anthropic:claude-3-5-sonnet-20241022,openai:gpt-4o'
$env:AKOS_RECORD_LIVE='1'

# 2. Optional: enable real API calls (otherwise dispatcher-validation only):
$env:AKOS_JUDGE_LIVE_API='1'
$env:ANTHROPIC_API_KEY='...'
$env:OPENAI_API_KEY='...'

# 3. Run burn (default N=50):
py scripts/judge_calibration_burn.py
py scripts/judge_calibration_burn.py --n 5         # smoke
py scripts/judge_calibration_burn.py --persona OPERATOR

# 4. Review report under artifacts/judge-calibration/.
```

## Activation gate (D-IH-52-B)

The report's "D-IH-52-B activation guidance" section tells the operator how to read the alignment numbers:

- All axes >= 80% → keep **consensus voting (default)**.
- Any axis < 80% with one member systematically diverging → consider **per-axis specialization**.
- All axes < 80% AND a cheap-tier member aligns equally → consider **cost-aware tiered escalation**.

## Cross-references

- `prompts/judge/JUDGE_ROSTER_V1.md`
- `prompts/judge/JUDGE_PROMPT_V1.md`
- `docs/wip/planning/52-multi-model-judge-and-cost-discipline/decision-log.md` (D-IH-52-B)
- `scripts/judge_calibration_burn.py`
