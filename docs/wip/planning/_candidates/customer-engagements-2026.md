---
language: en
status: candidate
initiative: (none) — pointer placeholder for in-flight customer engagements
seeded_by: SUEZ WeBuy first-customer engagement (2026-05-10)
last_review: 2026-05-10
authority: O5-1 + Project Manager + Account Manager
trigger_status: rolling — promotes to a chartered initiative when ≥ 2 customer engagements are simultaneously in flight
---

# Customer engagements 2026 — pointer placeholder

> **This is a pointer, not a charter.** Per `_candidates/` convention (see `i60-process-list-harmonisation.md`, `i69-inframonitor-saas-product.md`), this one-page file documents *the next decision moment* without committing scope or budget. It promotes to a chartered initiative only when operator surfaces a multi-engagement coordination need.

## Purpose

In-flight customer engagements live under [`docs/wip/intelligence/<YYYY-MM-DD>-<engagement-slug>/`](../../intelligence/) for working-space artefacts and [`docs/references/hlk/v3.0/_assets/advops/<engagement-slug>/`](../../../references/hlk/v3.0/_assets/advops/) for outward-facing deliverables. This pointer simply lists them so the operator and agents can see what is open without grepping.

## Active engagements

| Slug | Counterparty | Bridge | Status | Working space | Outward space |
|:---|:---|:---|:---|:---|:---|
| `2026-05-10-suez-webuy-procure-to-pay` | `GOI-CUS-SUEZ-2026` (French enterprise; procure-to-pay automation) | `GOI-PRT-EFA-2026` | Discovery — meeting Mon 11 May | [`docs/wip/intelligence/2026-05-10-suez-webuy-procure-to-pay/`](../../intelligence/2026-05-10-suez-webuy-procure-to-pay/) | [`docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/`](../../../references/hlk/v3.0/Think%20Big/Clients/2026-suez-webuy/) (relocated from `_assets/advops/shared/` in P12.3) |

## When to promote to a chartered initiative

* Two or more engagements are open simultaneously and need shared scheduling, shared estimation discipline tweaks, or shared lessons-learned cycles.
* A repeat counterparty triggers an account-management workstream (renewal, expansion, multi-year framework).
* The estimation discipline (`SOP-ENG_ESTIMATION_DISCIPLINE_001`) collects enough engagement data for a calibration review.

Until then, each engagement carries its own intelligence + advops folders and self-checkpoints under its own `checkpoints/` subdirectory; there is no umbrella initiative to maintain.

## Cross-references

* `GOI_POI_REGISTER.csv` — counterparty rows (rows for EFA + SUEZ landed 2026-05-10).
* `SOP-ENG_DISCOVERY_QUESTIONNAIRE_001` — discovery questionnaire SOP.
* `SOP-ENG_PROPOSAL_001` — proposal SOP.
* `SOP-ENG_ENGAGEMENT_DESIGN_001` — multi-cell engagement design.
* `SOP-ENG_ESTIMATION_DISCIPLINE_001` *(in flight P3)* — pricing + effort + duration discipline.
