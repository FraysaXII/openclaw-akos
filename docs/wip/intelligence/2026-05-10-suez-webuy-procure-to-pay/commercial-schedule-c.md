# Commercial schedule — Counterparty enterprise (FR) — Variant C (full operationalisation + capability transfer)

> Computed 2026-05-10 from `SOP-ENG_ESTIMATION_DISCIPLINE_001`. Country `FR` (7.0 h/day, 11 public-holiday-equivalent days/year, locale uplift 20%).

## Per-package estimate

| Package | Method | Effort h (min/par/max) | Blended rate €/h (min/par/max) | Cost € pre-mult | Multiplier × | Cost € final (min/par/max) | Duration days (min/par/max) |
|:---|:---|:---|:---|:---|:---|:---|:---|
| `WP-C1-discovery-kickoff` | Discovery — kickoff workshop and framing | 8 / 12 / 18 | 52 / 70 / 88 | 840 | 1.822 (enterprise_premium, bridge_entity, locale_uplift_fr, first_of_kind) | 765 / 1,530 / 2,869 | 1.1 / 1.7 / 2.6 |
| `WP-C2-discovery-interviews` | Discovery — stakeholder interviews + synthesis grid | 12 / 20 / 32 | 56 / 74 / 92 | 1,480 | 1.822 (enterprise_premium, bridge_entity, locale_uplift_fr, first_of_kind) | 1,213 / 2,696 / 5,392 | 1.7 / 2.9 / 4.6 |
| `WP-C3-baseline-synthesis` | Discovery — baseline assessment write-up | 8 / 14 / 24 | 54 / 72 / 90 | 1,008 | 1.822 (enterprise_premium, bridge_entity, locale_uplift_fr, first_of_kind) | 787 / 1,836 / 3,935 | 1.1 / 2.0 / 3.4 |
| `WP-C4-design-workshop` | Design — joint design workshop (counterparty-side) | 10 / 16 / 28 | 69 / 90 / 114 | 1,440 | 1.822 (enterprise_premium, bridge_entity, locale_uplift_fr, first_of_kind) | 1,257 / 2,623 / 5,815 | 1.4 / 2.3 / 4.0 |
| `WP-C5-cdc-functional-spec` | Design — functional + technical specification | 24 / 40 / 72 | 58 / 75 / 95 | 3,000 | 1.822 (enterprise_premium, bridge_entity, locale_uplift_fr, first_of_kind) | 2,514 / 5,465 / 12,460 | 3.4 / 5.7 / 10.3 |
| `WP-C6-feasibility-procurement-portal` | Build — Phase 3 integration feasibility study | 40 / 80 / 140 | 62 / 81 / 103 | 6,480 | 1.822 (enterprise_premium, bridge_entity, locale_uplift_fr, first_of_kind) | 4,554 / 11,804 / 26,267 | 5.7 / 11.4 / 20.0 |
| `WP-C7-feasibility-reporting-layer` | Build — Phase 3 integration feasibility study | 40 / 80 / 140 | 62 / 81 / 103 | 6,480 | 1.822 (enterprise_premium, bridge_entity, locale_uplift_fr, first_of_kind) | 4,554 / 11,804 / 26,267 | 5.7 / 11.4 / 20.0 |
| `WP-C8-poc-phase1-prototype` | Build — Phase 1 Excel/Power Query prototype | 40 / 80 / 140 | 52 / 69 / 87 | 5,520 | 1.822 (enterprise_premium, bridge_entity, locale_uplift_fr, first_of_kind) | 3,825 / 10,055 / 22,187 | 5.7 / 11.4 / 20.0 |
| `WP-C9-poc-phase2-webapp` | Build — Phase 2 lightweight web application | 140 / 240 / 400 | 50 / 66 / 83 | 15,840 | 1.822 (enterprise_premium, bridge_entity, locale_uplift_fr, first_of_kind) | 12,751 / 28,854 / 60,477 | 20.0 / 34.3 / 57.1 |
| `WP-C10-operator-training-wave1` | Transfer — operator training | 12 / 20 / 32 | 55 / 72 / 91 | 1,440 | 1.584 (enterprise_premium, bridge_entity, locale_uplift_fr) | 1,045 / 2,281 / 4,613 | 1.7 / 2.9 / 4.6 |
| `WP-C11-operator-training-wave2` | Transfer — operator training | 12 / 20 / 32 | 55 / 72 / 91 | 1,440 | 1.584 (enterprise_premium, bridge_entity, locale_uplift_fr) | 1,045 / 2,281 / 4,613 | 1.7 / 2.9 / 4.6 |
| `WP-C12-operational-handover` | Transfer — SOP + runbook + handover pack | 12 / 20 / 32 | 56 / 73 / 92 | 1,460 | 1.584 (enterprise_premium, bridge_entity, locale_uplift_fr) | 1,055 / 2,313 / 4,663 | 1.7 / 2.9 / 4.6 |
| `WP-C13-extended-documentation` | Transfer — SOP + runbook + handover pack | 12 / 20 / 32 | 56 / 73 / 92 | 1,460 | 1.584 (enterprise_premium, bridge_entity, locale_uplift_fr) | 1,055 / 2,313 / 4,663 | 1.7 / 2.9 / 4.6 |
| `WP-C14-close-review` | Close — engagement review + lessons-learned | 4 / 8 / 14 | 72 / 95 / 120 | 760 | 1.584 (enterprise_premium, bridge_entity, locale_uplift_fr) | 459 / 1,204 / 2,661 | 0.6 / 1.1 / 2.0 |

## Totals

| Aggregate | min | par (PERT-expected) | max |
|:---|---:|---:|---:|
| Effort hours | 374 | 670 (E=698) | 1136 |
| Cost (€) | 36,881 | 87,059 (E=95,333) | 186,882 |
| Duration (working days) | 53 | 96 (E=100) | 162 |

## Visual schedule (Mermaid Gantt)

```mermaid
gantt
  title Calendrier prévisionnel — Counterparty enterprise (FR) — Variant C (full operationalisation + capability transfer)
  dateFormat  YYYY-MM-DD
  axisFormat  %d %b
  excludes    weekends
  section Engagement
  Discovery — kickoff workshop and framing : WP_C1_discovery_kickoff, 2026-05-19, 2d
  Discovery — stakeholder interviews + synthesis grid : WP_C2_discovery_interviews, 2026-05-21, 3d
  Discovery — baseline assessment write-up : WP_C3_baseline_synthesis, 2026-05-26, 2d
  Design — joint design workshop (counterparty-side) : WP_C4_design_workshop, 2026-05-28, 2d
  Design — functional + technical specification : WP_C5_cdc_functional_spec, 2026-06-01, 6d
  Build — Phase 3 integration feasibility study : WP_C6_feasibility_procurement_portal, 2026-06-09, 11d
  Build — Phase 3 integration feasibility study : WP_C7_feasibility_reporting_layer, 2026-06-24, 11d
  Build — Phase 1 Excel/Power Query prototype : WP_C8_poc_phase1_prototype, 2026-07-09, 11d
  Build — Phase 2 lightweight web application : WP_C9_poc_phase2_webapp, 2026-07-24, 34d
  Transfer — operator training : WP_C10_operator_training_wave1, 2026-09-11, 3d
  Transfer — operator training : WP_C11_operator_training_wave2, 2026-09-16, 3d
  Transfer — SOP + runbook + handover pack : WP_C12_operational_handover, 2026-09-21, 3d
  Transfer — SOP + runbook + handover pack : WP_C13_extended_documentation, 2026-09-24, 3d
  Close — engagement review + lessons-learned : WP_C14_close_review, 2026-09-29, 1d
```

## Notes

Variant C — full operationalisation. Adds a Phase 2 multi-category lightweight web application,
an additional operator training wave, and an extended documentation handover on top of Variant B.
Web application stays inside Holistika's compliance-friendly delivery environment until counterparty
IT validates a future production migration (out of scope of this engagement). Bridge entity
present. Brand Manager not assigned to any package for an automation + SOP scope.

