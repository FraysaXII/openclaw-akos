---
title: SOP - Research Radar
language: en
intellectual_kind: research-area-canonical-sop
sop_id: SOP-RESEARCH_RADAR_001
access_level: 4
confidence_level: Euclid
source_taxonomy: holistika-internal-sop
authors:
  - Research Director
  - KM Officer
last_review: 2026-05-29
last_review_by: Founder
last_review_decision_id: D-IH-86-FG
methodology_version_at_review: v3.2
ratifying_decisions:
  - D-IH-86-FG
status: charter
register: internal
linked_canonicals:
  - RESEARCH_RADAR_DISCIPLINE.md
  - RESEARCH_ACTION_DISCIPLINE.md
linked_runbooks:
  - scripts/research_radar_sweep.py
  - scripts/validate_research_radar.py
cadence: scheduled
---

# SOP - Research Radar

## Purpose

Run the Research Radar freshness sweep before Research Action govern stage when volatile targets may have gone stale.

## Acceptance Criteria

- **AC-HUMAN**: Research Director, KM Officer, or PMO interim can read `INTELLIGENCEOPS_REGISTER.csv`, interpret per-row `staleness_days` / `next_verify_by`, and disposition stale rows via inline-ratify without invoking the runbook.
- **AC-AUTOMATION**: `py scripts/research_radar_sweep.py` emits a stale/DUE queue from register data; `py scripts/validate_research_radar.py --self-test` PASS at pre_commit.

## Steps

1. Confirm IntelligenceOps rows carry `volatility_class`, `staleness_days`, `staleness_posture`, `next_verify_by` (never a global constant).
2. Run `py scripts/research_radar_sweep.py` (add `--include-substrate` when substrate landscape maintenance is in scope).
3. For each `STALE` or `DUE` row, open Research Action govern with ranked re-verify options.
4. Apply `staleness_posture`: `block_govern` blocks govern until operator ratifies; `cite_and_flag` allows govern with explicit stale citation.
5. After verification, bump `last_review_at` and recompute `next_verify_by` on the register row.

## Verification

```powershell
py scripts/validate_research_radar.py --self-test
py scripts/research_radar_sweep.py
```
