---
initiative_id: INIT-OPENCLAW_AKOS-97
initiative_slug: 97-infonomics-holistika-data-economics
title: "I97 — Infonomics / Holistika Data Economics"
status: active
authored: 2026-06-12
last_review: 2026-06-12
inception_decision_id: D-IH-97-A
owner_role: Operator
linked_decisions:
  - D-IH-97-A
  - D-IH-97-B
  - D-IH-97-C
  - D-IH-97-D
language: en
authoritative_plan: docs/wip/planning/97-infonomics-holistika-data-economics/master-roadmap.md
---

# I97 — Infonomics / Holistika Data Economics

> **Glossary (carryover posture):** **scheduled** = will happen at named phase — **not dropped**. Vault mint is **scheduled for P6**, not optional. See [`carryover-posture-index.md`](../_trackers/carryover-posture-index.md).
>
> **Active spine (2026-06-12):** This program until registry pause #1. AIC executes; you decide. [`OPERATOR_STEERING_AND_CARRYOVER.md`](../OPERATOR_STEERING_AND_CARRYOVER.md).

Enterprise Infonomics research: 800-row source ledger, 14 BL prong syntheses, govern-gated vault tranches. Full phase plan in Cursor plan `i97_infonomics_research_991a9503.plan.md`.

**Research pack (P1 shell):** [`docs/wip/intelligence/infonomics-holistika-data-economics-2026-06-12/`](../../../intelligence/infonomics-holistika-data-economics-2026-06-12/)

## Pause points

| Pause | Phase | Gate |
|:---|:---|:---|
| ~~#1~~ | ~~P0~~ | ~~INITIATIVE_REGISTRY (`D-IH-97-A`)~~ — **cleared 2026-06-12** |
| ~~#2~~ | ~~P5~~ | ~~Govern ratify vault scope~~ — **cleared 2026-06-13** |
| #3 | P6a→P6b | DCAM level axis (P6a) then doctrine mint (P6b) |

## Phase plan

| Phase | Purpose | Key deliverable |
|:---|:---|:---|
| **P0** | Initiative scaffold | Six-artifact set + cluster map (this commit) |
| **P1** | Research pack shell | Intelligence folder + ledger header — [`pack`](../../../intelligence/infonomics-holistika-data-economics-2026-06-12/) ✅ |
| **P2** | Internal ~300 CORPINT | baseline-state + ledger rows — ✅ [`baseline`](../../../intelligence/infonomics-holistika-data-economics-2026-06-12/baseline-state-2026-06-12.md) |
| **P3** | External ~500 OSINT | 800 total ledger — ✅ [`p3 report`](reports/p3-external-osint-2026-06-12.md) |
| **P4** | Synthesize | 14 prong files + HXPESTAL master — ✅ [`p4 report`](reports/p4-prong-syntheses-2026-06-13.md) |
| **P5** | Govern ratify | p5-govern-ratify report — ✅ [`p5 report`](reports/p5-govern-ratify-2026-06-13.md) |
| **P6a** | DCAM level axis (area completeness) | Prerequisite tranche — **scheduled** |
| **P6b** | Vault doctrine mint | `INFONOMICS_DISCIPLINE` — **scheduled** |
| **P6c** | Optional process_list | D-IH-97-F — optional |
| **P6d** | I94 extension | D-IH-97-G — optional / forward |
| **P7** | Closure UAT | 11-section uat-i97 |
| **P8** | Index sync | README, dependencies, dashboard |

## Verification (P1)

```powershell
py scripts/validate_research_action.py --self-test
py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/infonomics-holistika-data-economics-2026-06-12/source-ledger.csv
py scripts/validate_carryover_posture.py --index docs/wip/planning/_trackers/carryover-posture-index.md --strict
```

## Cross-references

- Overlap tracker: [`../_trackers/i96-i97-infonomics-scope-overlap-tracker.md`](../_trackers/i96-i97-infonomics-scope-overlap-tracker.md)
- Carryover index rows: CO-97-001..004
