---
status: complete
classification: working
access_level: 5
language: en
register: internal
phase: P3a
phase_name: Mint estimation discipline (SOP + Python module + CLI + tests + worksheet)
recorded_at: 2026-05-10
---

# P3a — Mint estimation discipline self-checkpoint

## Files created

| File | Purpose | LOC (approx.) |
|:---|:---|---:|
| `akos/engagement_estimation.py` | Pydantic models + PERT math + role blending + multipliers + country calendar + Mermaid Gantt | ~360 |
| `scripts/estimate_engagement.py` | Operator CLI (loads scope.yaml, role rates, calendar; renders commercial-schedule.md) | ~150 |
| `tests/test_engagement_estimation.py` | 35 cases — PERT math, role blending, calendar math, multiplier compounding, Mermaid Gantt, end-to-end engagement estimation | ~270 |
| `tests/test_estimation_constants_match_sop.py` | 4 drift-safeguard cases — SOP §3 method table ↔ `METHODS`, SOP §5 multiplier table ↔ `MULTIPLIERS` | ~80 |
| `docs/references/hlk/v3.0/Admin/O5-1/Operations/Engagement/SOP-ENG_ESTIMATION_DISCIPLINE_001.md` | Canonical SOP body | ~120 |
| `docs/references/hlk/v3.0/_assets/operations/engagement/estimation/estimation-template.md` | Operator worksheet template | ~85 |

## Verification

```
py -m pytest tests/test_engagement_estimation.py -v
==> 33 passed, 2 skipped (P3b CSV-loaders smoke + SUEZ scope.yaml smoke; will pass after P3b/P3c)

py -m pytest tests/test_estimation_constants_match_sop.py -v
==> 4 passed
```

## Design notes

* Method library lists 12 reusable methods. Each has min/par/max effort hours (PERT triangle) and a default role mix; both are calibrated to the Madrid SME consulting baseline.
* Roles in the default role mix use canonical `role_name` values from `baseline_organisation.csv` (e.g. `O5-1`, `Project Manager`, `Tech Lead`); blending fails fast on unknown roles.
* Multipliers compound onto **price only**, not effort. Five multipliers shipped: `enterprise_premium` (×1.20), `bridge_entity` (×1.10), `locale_uplift_fr` (×1.20), `first_of_kind` (×1.15), `repeat_counterparty` (×0.90).
* Country calendar logic: working-days = effort_hours / legal_hours_per_day; end-date math advances skipping weekends and applying a public-holiday bump from `public_holidays_per_year_avg × span_days / 365`.
* Mermaid Gantt rendering uses `par`-day durations only (deterministic visual); min/par/max appear in the surrounding markdown table.
* Drift safeguard: 4 tests parse the SOP §3/§5 tables and assert one-to-one equivalence with the Python `METHODS` and `MULTIPLIERS` registries. CI fails on drift in either direction.

## Next

P3b — Canonical CSV extensions. Extend `baseline_organisation.csv` (62-row 6-tier rate population), `process_list.csv` (engagement-execution `time_hours_min/max` columns), mint `COUNTRY_WORK_CALENDAR.csv`. Re-run the 2 skipped tests to confirm end-to-end with canonical data.
