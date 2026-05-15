---
language: en
status: active
canonical: true
role_owner: Ethics Advisor
area: People
entity: Holistika
classification: way_of_working
intellectual_kind: sop
ssot: true
authored: 2026-05-15
last_review: 2026-05-15
companion_to:
  - ETHICAL_AUTOMATION_POSTURE.md
  - ../../Learning/canonicals/LEARNING_CHARTER.md
---

# SOP-ETHICS_LEARNING_REVIEW_001 — Quarterly Ethics + Learning co-review

## 1. Purpose

Keep [`ETHICAL_AUTOMATION_POSTURE.md`](ETHICAL_AUTOMATION_POSTURE.md) §5 (*Ethics + Learning inseparability contract*) **live** by scheduling a **quarterly** joint review with the Learning charter owner.

## 2. Scope

**In scope**

- Posture vs curriculum alignment (`ETHICAL_AUTOMATION_POSTURE.md` §2.5 **quarterly** ongoing-review cadence + §5 inseparability clauses).
- [`LEARNING_CHARTER.md`](../../Learning/canonicals/LEARNING_CHARTER.md) versioning anchor + pillar placeholders (forward I75).
- Spot-check that apprentice / cohort flows still cite [`HOLISTIK_RESEARCHER_ONBOARDING_CURRICULUM.md`](../../Learning/canonicals/curriculum/HOLISTIK_RESEARCHER_ONBOARDING_CURRICULUM.md) + [`LEARNING_OPS_BACKLOG.csv`](../../Learning/canonicals/dimensions/LEARNING_OPS_BACKLOG.csv).

**Out of scope**

- Replacing Legal review of contracts or FINOPS payout mechanics (route to existing Finance / People Ops SOPs).
- External-register brand publish — thesis language stays **internal** until Brand promotes per [`BRAND_VOICE_FOUNDATION.md`](../../../Marketing/Brand/canonicals/BRAND_VOICE_FOUNDATION.md).

## 3. Roles (RACI)

| Role | Responsibility |
|:-----|:---------------|
| **Ethics Advisor** (A/R) | Schedules the session, owns minutes, drives escalation to founder if §5 triggers fire. |
| **Learning Curator** (R) | Brings curriculum backlog + methodology-version evidence; confirms cohort coverage. |
| **People Operations Lead** (C) | Optional attendee when apprentice engagements surfaced curriculum defects. |

**C-73-3 ratification:** Ethics-led facilitation with mandatory Learning co-review (inline-ratify default).

## 4. Inputs

- Latest `last_review` stamps on `ETHICAL_AUTOMATION_POSTURE.md` + `LEARNING_CHARTER.md`.
- [`PEOPLE_AREA_RESTRUCTURE.md`](../../canonicals/PEOPLE_AREA_RESTRUCTURE.md) §2–§3 (ownership + thesis framing).
- Advisory checklist output from **`scripts/check_ethics_learning_review_due.py`**.

## 5. Procedure

1. **Calendar** — Book 60 minutes within **15 days after each calendar quarter end** (aligned to [`ETHICAL_AUTOMATION_POSTURE.md`](ETHICAL_AUTOMATION_POSTURE.md) §2.5 quarterly cadence).
2. **Run advisory runbook** — `py scripts/check_ethics_learning_review_due.py` (stdout checklist + staleness advisory when posture `last_review` age exceeds **120 days**).
3. **Review agenda** — Confirm (a) curriculum modules still cite [`access_levels.md`](../../Compliance/canonicals/access_levels.md) / [`source_taxonomy.md`](../../Compliance/canonicals/source_taxonomy.md) / [`confidence_levels.md`](../../Compliance/canonicals/confidence_levels.md); (b) ethics thesis cross-links remain intact in brand foundation doc; (c) no drift vs [`ENGAGEMENT_MODEL_REGISTRY.csv`](../../People%20Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv) apprentice class assumptions.
4. **Record** — File summary under `docs/wip/planning/73-people-operations-and-learning-curriculum/reports/` when findings require initiative tracking; otherwise attach notes to quarterly governance folder per PMO habit.
5. **Stamp** — Update `last_review` frontmatter on `ETHICAL_AUTOMATION_POSTURE.md` when posture conclusions change; bump `LEARNING_CHARTER.md` when curriculum edits land same cycle.

## 6. Outputs

- Escalation note to founder if §5 starvation clause triggers (Learning lapse).
- Optional OPS_REGISTER follow-up row if remediation spans multiple initiatives.

## 7. Failure modes

- **Learning Curator unavailable** — Ethics Advisor runs limited posture review, logs deferral, reschedules within 30 days.
- **Stale posture doc (>120 days)** — Treat as **HIGH** priority queue item; runbook emits advisory text for [`OPERATOR_INBOX.md`](../../../../../../../../wip/planning/OPERATOR_INBOX.md) triage.

## 8. Cross-references

- Paired runbook: [`scripts/check_ethics_learning_review_due.py`](../../../../../../../../scripts/check_ethics_learning_review_due.py)
- Engagement historical patterns (internal): [`HISTORICAL_ENGAGEMENT_CASE_LAW.md`](../../People%20Operations/canonicals/HISTORICAL_ENGAGEMENT_CASE_LAW.md)
- Process row: `hol_peopl_dtp_316` in [`process_list.csv`](../../Compliance/canonicals/process_list.csv)
