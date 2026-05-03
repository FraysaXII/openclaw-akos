---
language: en
status: active
initiative: 52-multi-model-judge-and-cost-discipline
report_kind: risk-register
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 52 — Risk register

| ID | Risk | Likelihood | Impact | Mitigation | Trigger |
|:---|:-----|:--:|:--:|:-----------|:--------|
| R-52-1 | Multi-judge cost runaway (N=2 doubles cost vs single judge) | Medium | High | `MAX_JUDGE_USD_PER_RUN=$15` envelope (D-IH-52-C); cassette-replay default for pre-commit; operator may downscope to N=1 after P3 if calibration unjustifies consensus | P7 first Tier-B run > envelope |
| R-52-2 | Multi-judge sycophancy / collective drift across model rev | Medium | Medium | Roster `model_id`s captured in every cassette; re-baseline burns triggered when any roster member's `model_id` changes; operator alarm on drift | Provider rev announcement |
| R-52-3 | Multi-judge consensus contradicts offline rubric on edge cases | High at first | Medium | P3 calibration burn surfaces these before activation; P4 threshold/routing refresh is the resolution path | P3 alignment < 80% on any axis |
| R-52-4 | RunPod/Kalavai API contracts drift; cost probe stops working silently | Medium | Medium | `endpoint_cost_probe.py` smoke test + dashboard "last successful probe" timestamp; operator alarm if > 1h stale | Probe returns < 200 / structurally invalid |
| R-52-5 | Huge-model deployment passes the envelope before the alarm fires (e.g., one-shot 70B inference burns daily envelope in < 1h) | Low | High | Per-hour micro-envelope (`max_usd_per_hour = max_usd_per_day / 24 × 1.5`); auto-pause hook (D-IH-52-E opt-in once API contracts pinned) | Hourly burn rate exceeds micro-envelope |
| R-52-6 | Operator under-sets endpoint envelope and CI auto-pauses production endpoint | Low | High | Per-endpoint POLICY row requires operator-approved `max_usd_per_day`; **auto-pause is opt-in only** (D-IH-52-E); alarm-only is default | First auto-pause request without operator-approved POLICY row |
