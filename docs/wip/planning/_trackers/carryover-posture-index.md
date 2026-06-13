---
intellectual_kind: carryover_posture_index
sharing_label: internal_only
authored: 2026-06-12
last_review: 2026-06-12
next_review_trigger: Weekly index staleness review OR any initiative closure touches a row
linked_decisions:
  - D-IH-98-A
  - D-IH-98-STEERING
status: active
role_owner: PMO
language: en
---

# Carryover posture index (cross-initiative)

> **Purpose.** Single discoverability surface for work-item carryover across initiatives.
> **Operator steering (2026-06-12):** AIC executes; you decide. Single spine = Infonomics P0 until registry gate. See [`OPERATOR_STEERING_AND_CARRYOVER.md`](../OPERATOR_STEERING_AND_CARRYOVER.md).
>
> **SSOT enum:** [`akos/planning/carryover_posture.py`](../../../akos/planning/carryover_posture.py)
> **Row template:** [`../_templates/carryover-posture-row.md`](../_templates/carryover-posture-row.md)
> **Validator:** `py scripts/validate_carryover_posture.py --index docs/wip/planning/_trackers/carryover-posture-index.md`

## Glossary (one line each)

| Posture | Meaning |
|:---|:---|
| **scheduled** | Will happen; gated on evidence or phase — **not dropped** |
| **forward_charter** | Successor initiative/chat owns continuation |
| **overlap_pending** | Sibling consolidation at named phase ratify gate |
| **blocked** | Activation gates not met (see blocker tracker) |
| **dropped** | Explicitly out of scope / decommissioned |
| **superseded** | Replaced by a ratified decision |
| **monitoring** | Shipped; PWF-style closure obligation remains |

---

## Active index rows

| index_id | posture | item_id | target / successor | activation_trigger | next_review | owner | discoverability_path |
|:---|:---|:---|:---|:---|:---|:---|:---|
| CO-97-001 | superseded | D-IH-97-E | I97 P6b vault doctrine | Closed 2026-06-13 — INFONOMICS_DISCIPLINE minted | Archive | Operator | `docs/wip/planning/97-infonomics-holistika-data-economics/reports/p6b-doctrine-mint-2026-06-13.md` |
| CO-97-002 | scheduled | D-IH-97-F | Forward: PMO process_list row | I97 closed without P6c — canonical CSV gate | PMO ratify OR I94 ops sweep | PMO | `docs/wip/planning/97-infonomics-holistika-data-economics/decision-log.md#D-IH-97-F` |
| CO-97-003 | scheduled | D-IH-97-G | Forward: I94 AREA economic hook | I97 closed without P6d — out of closure scope | I94 area extension tranche | CDO | `docs/wip/planning/97-infonomics-holistika-data-economics/decision-log.md#D-IH-97-G` |
| CO-97-004 | superseded | D-IH-97-D | I96 consumes I97 P6b doctrine | Ratified Option B 2026-06-13 | Archive unless I96 dependency reopens | Operator | `docs/wip/planning/97-infonomics-holistika-data-economics/reports/p5-govern-ratify-2026-06-13.md` |
| CO-98-001 | scheduled | D-IH-98-C | vault carryover discipline | Operator requests vault OR I97 P6 doctrine stable | 2026-07-15 OR I97 P6 close | Operator | `docs/wip/planning/98-carryover-posture-clarity/decision-log.md#D-IH-98-C` |
| CO-96-001 | scheduled | D-IH-96-D | I96 P10 multi-channel feed | Research Center v1 PASS + Track D stable | I96 P9 close OR 2026-07-01 | PMO | `docs/wip/planning/96-research-data-plane-and-research-center/decision-log.md` |
| CO-76-001 | overlap_pending | I11/I13/I17 | I76 P1/P3/P4 gates | Per sibling ratify (mostly closed 2026-05-21) | Archive if all siblings closed | System Owner | `docs/wip/planning/_trackers/i11-i13-i17-scope-overlap-tracker.md` |
| CO-76-002 | blocked | I74 promotion | TRIGGER-2 or sibling closure | OPS-76-2 quarterly review | OPS-76-2 due date | PMO | `docs/wip/planning/_blockers/i74-promotion-blocker-tracker.md` |
| CO-76-003 | blocked | I75 promotion | I72/I73 P0 + Research Director | OPS-76-3 review | OPS-76-3 due date | PMO | `docs/wip/planning/_blockers/i75-promotion-blocker-tracker.md` |
| CO-76-004 | blocked | I83 promotion | I82 P4 USE_CASE_ARCHIVE | OPS-76-4 review | OPS-76-4 due date | PMO | `docs/wip/planning/_blockers/i83-promotion-blocker-tracker.md` |
| CO-88-001 | scheduled | DataOps SOP pairing | doctrine activation | dataops-activation-tracker §3 green | dataops tracker next review | CDO | `docs/wip/planning/_trackers/dataops-activation-tracker.md` |
| CO-91-001 | forward_charter | UX research SOP | I91 P2 | ux_quality_check.py ships | I91 P2 entry OR 2026-07-01 | People Ops | `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/UX Designer/canonicals/UX_DISCIPLINE.md` |
| CO-95-001 | forward_charter | PMO business-strategy placement | I94 P5 ratify | I95 tracker operator ratify | I94 P5 session | PMO | `docs/wip/planning/_trackers/i95-operations-pmo-business-strategy-placement-tracker.md` |

---

## Carryover edges (mirror for INITIATIVE_DEPENDENCIES)

| from_initiative | to_initiative | posture | activation_trigger | owner_decision_id | index_row |
|:---|:---|:---|:---|:---|:---|
| INIT-OPENCLAW_AKOS-97 | INIT-OPENCLAW_AKOS-96 | scheduled | I97 P6b doctrine stable; I96 Track D consumes | D-IH-97-D | CO-97-004 |
| INIT-OPENCLAW_AKOS-98 | — | scheduled | I98 P4 govern ratify | D-IH-98-C | CO-98-001 |
