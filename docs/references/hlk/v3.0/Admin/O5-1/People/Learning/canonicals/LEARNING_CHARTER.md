---
language: en
status: active
canonical: true
role_owner: Learning Curator
area: People
entity: Holistika
classification: charter
intellectual_kind: learning_operating_model
ssot: true
authored: 2026-05-15
last_review: 2026-05-15
companion_to:
  - ../Ethics/canonicals/ETHICAL_AUTOMATION_POSTURE.md
  - ../canonicals/PEOPLE_AREA_RESTRUCTURE.md
---

# LEARNING_CHARTER — Holistik Researcher + methodology coaching

> **I73 P2 deliverable (Strand A).** Establishes Learning as the discipline that keeps operators and apprentice-class engagements aligned with current methodology — inseparable from Ethics per [`PEOPLE_AREA_RESTRUCTURE.md`](../canonicals/PEOPLE_AREA_RESTRUCTURE.md) §3.

## 1. Purpose

- Maintain a **single readable charter** for cohort-based onboarding (Holistik Researcher track) and methodology-pillar coaching cadence.
- Bind apprentice-class engagements (`eng_model_apprentice_learner` per [`ENGAGEMENT_MODEL_REGISTRY.csv`](../../People%20Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv)) to the onboarding curriculum and cohort backlog.
- Keep Learning and Ethics cross-linked: Ethics owns [`ETHICAL_AUTOMATION_POSTURE.md`](../Ethics/canonicals/ETHICAL_AUTOMATION_POSTURE.md); Learning owns curriculum freshness so posture decisions remain evidence-backed.

## 2. Scope

**In scope:** Holistik Researcher onboarding curriculum; cohort tracking via `LEARNING_OPS_BACKLOG.csv`; research artefact info-handling literacy (access / source / confidence taxonomies); pillar placeholders pending I75 methodology SOPs.

**Out of scope:** Compliance regulatory perimeter (owned by Compliance); baseline CSV splits deferred per `PEOPLE_AREA_RESTRUCTURE.md` §5; KB persona routes (I73 P7); methodology IP filing decisions (I73 P8).

## 3. Roles

| Role | Responsibility |
|:---|:---|
| **Learning Curator** | Authors curriculum revisions; coaches pillar application; maintains `LEARNING_OPS_BACKLOG.csv` integrity with People Operations at apprentice intake. |
| **Ethics Advisor** | Owns ethical posture canonical; co-reviews quarterly per [`ETHICAL_AUTOMATION_POSTURE.md`](../Ethics/canonicals/ETHICAL_AUTOMATION_POSTURE.md) §5 (paired `SOP-ETHICS_LEARNING_REVIEW_001.md` ships at I73 P5). |
| **People Operations Manager** | Executes apprentice curriculum assignment process [`tbi_peopl_dtp_apprentice_curriculum_assignment_001`](../../Compliance/canonicals/process_list.csv) at intake; parameterized engagements per engagement model registry. |

## 4. Curriculum versioning anchor (C-73-2)

Default versioning anchor for cohort onboarding is **`methodology-anchor`**: cohort rows record `methodology_version_at_onboarding = methodology-anchor` in [`dimensions/LEARNING_OPS_BACKLOG.csv`](dimensions/LEARNING_OPS_BACKLOG.csv), aligned with the I71 review-stamp posture (`methodology_version_at_review` on mirrored canonicals). Detailed pillar stamps advance when [`LOGIC_CHANGE_LOG.md`](../canonicals/LOGIC_CHANGE_LOG.md) BT rows increment; curriculum exercises cite vault SSOT paths, not floating copies.

## 5. Methodology pillars (I75 placeholders)

Per [`docs/wip/planning/_candidates/i75-research-area-governance.md`](../../../../../../../../wip/planning/_candidates/i75-research-area-governance.md), Research Methodology discipline will publish ~6–8 pillar SOPs. Until I75 P1 lands, the onboarding curriculum uses **stub pillar IDs** (`PILLAR_PLACEHOLDER_01` … `PILLAR_PLACEHOLDER_06`) in [`curriculum/HOLISTIK_RESEARCHER_ONBOARDING_CURRICULUM.md`](curriculum/HOLISTIK_RESEARCHER_ONBOARDING_CURRICULUM.md). Replace placeholders when I75 publishes canonical pillar IDs (bidirectional loose-coupling; neither initiative blocks the other).

## 6. Ethics + Learning inseparability

Cross-links:

- [`ETHICAL_AUTOMATION_POSTURE.md`](../Ethics/canonicals/ETHICAL_AUTOMATION_POSTURE.md) §5 — quarterly / annual cadence; escalation when curriculum lapses.
- [`PEOPLE_AREA_RESTRUCTURE.md`](../canonicals/PEOPLE_AREA_RESTRUCTURE.md) §3 — brand thesis “we become unethical when we unlearn”.

## 7. Operational artefacts

| Artefact | Role |
|:---|:---|
| [`curriculum/HOLISTIK_RESEARCHER_ONBOARDING_CURRICULUM.md`](curriculum/HOLISTIK_RESEARCHER_ONBOARDING_CURRICULUM.md) | Cohort modules + info-handling module |
| [`dimensions/LEARNING_OPS_BACKLOG.csv`](dimensions/LEARNING_OPS_BACKLOG.csv) | Cohort + `engagement_model_id` + versioning anchor |
| `scripts/peopl_engagement_apprentice_curriculum_assign.py` | Paired runbook for apprentice curriculum assignment |

## 8. Cohort size default (C-73-1)

First Holistik Researcher cohort default size = **1** (bootstrapping posture; avoids premature scaling). Larger cohorts require explicit founder / Learning Curator ratification recorded in backlog `notes`.
