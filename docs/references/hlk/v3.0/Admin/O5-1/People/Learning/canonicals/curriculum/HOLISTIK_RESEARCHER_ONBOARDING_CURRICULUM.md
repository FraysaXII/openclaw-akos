---
language: en
status: active
canonical: true
role_owner: Learning Curator
classification: curriculum
ssot: true
authored: 2026-05-15
last_review: 2026-05-15
companion_to:
  - ../LEARNING_CHARTER.md
  - ../../Compliance/canonicals/access_levels.md
  - ../../Compliance/canonicals/source_taxonomy.md
  - ../../Compliance/canonicals/confidence_levels.md
---

# Holistik Researcher onboarding curriculum

> **I73 P2.** Cohort-shaped onboarding for `eng_model_apprentice_learner` (and percentage-collaborator overlays that include a training clause — coordinate via People Operations). Reading surfaces stay in v3.0 vault paths cited below.

## 1. Cohort cadence (default)

| Week | Focus | Outputs |
|:---:|:---|:---|
| 0 | Kickoff + vault navigation | Reading map acknowledged; engagement folder stub reviewed |
| 1 | Research programme info-handling | Exercise §3 complete |
| 2–3 | Methodology pillar stubs (`PILLAR_PLACEHOLDER_*`) | One exercise per pillar (short memo) |
| 4 | Ethics + automation posture read | Cross-check vs live methodology stamps |
| 5+ | Stretch: Intelligence / Diagnosis stubs | Links only until I75 ships discipline SOPs |

Default cohort size = **1** (C-73-1). Peer review optional when cohort >1.

## 2. Core reading list (vault SSOT)

- [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) — four-channel persistence; `_engagement-template/` copy targets; file-tracking policy.
- [`HLK_KM_TOPIC_FACT_SOURCE.md`](../../Compliance/canonicals/HLK_KM_TOPIC_FACT_SOURCE.md) — Topic–Fact–Source; Output 1 discipline.
- [`ETHICAL_AUTOMATION_POSTURE.md`](../../Ethics/canonicals/ETHICAL_AUTOMATION_POSTURE.md) — CSOLT lesson + coexistence design constraint.
- [`ENGAGEMENT_MODEL_REGISTRY.md`](../../People%20Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.md) — class parameterization for engagements.

## 3. Module — research-program info-handling

Every artefact produced or consumed in a research programme MUST be classified using:

| Canonical | Use |
|:---|:---|
| [`access_levels.md`](../../Compliance/canonicals/access_levels.md) | Who may see it (1–6 scale). |
| [`source_taxonomy.md`](../../Compliance/canonicals/source_taxonomy.md) | What kind of source evidence it is. |
| [`confidence_levels.md`](../../Compliance/canonicals/confidence_levels.md) | How strongly we stand behind the claim. |

**Exercise:** Take one Tier-1 WIP note from `docs/wip/intelligence/` (redact names) and annotate: access_level, primary source_taxonomy label, confidence_level — then route promotion candidate per WORKSPACE_BLUEPRINT WIP topology.

## 4. Methodology pillar exercises (I75 placeholders)

| Stub ID | Exercise (until I75 pillar SOP exists) |
|:---|:---|
| `PILLAR_PLACEHOLDER_01` | Summarise how [`LOGIC_CHANGE_LOG.md`](../../canonicals/LOGIC_CHANGE_LOG.md) BT-01..BT-03 constrain methodology edits. |
| `PILLAR_PLACEHOLDER_02` | Map one founder principle from [`FOUNDER_METHODOLOGY_VERSIONING.md`](../../canonicals/FOUNDER_METHODOLOGY_VERSIONING.md) to a live vault example. |
| `PILLAR_PLACEHOLDER_03` | Draft outline for AI-coexistence gate using ETHICAL_AUTOMATION_POSTURE §2.2 pattern. |
| `PILLAR_PLACEHOLDER_04` | Trace one KM manifest requirement from HLK_KM_TOPIC_FACT_SOURCE §_output contracts. |
| `PILLAR_PLACEHOLDER_05` | Compare Intelligence vs Validation discipline stubs in I75 candidate §2 Strand A table (reading only). |
| `PILLAR_PLACEHOLDER_06` | List three diagnostic signals that belong in Research vs PMO engagement artefacts (per I75 Strand D forward-link). |

Replace stubs when [`docs/wip/planning/_candidates/i75-research-area-governance.md`](../../../../../../../../../wip/planning/_candidates/i75-research-area-governance.md) promotes and publishes pillar SOPs.

## 5. Completion criteria

- Backlog row exists in [`../dimensions/LEARNING_OPS_BACKLOG.csv`](../dimensions/LEARNING_OPS_BACKLOG.csv) with `engagement_model_id = eng_model_apprentice_learner` (unless overridden per engagement) and `methodology_version_at_onboarding = methodology-anchor`.
- Learning Curator signs off `status` transition `planned → active → completed` with date notes.

## 6. Runbook pairing

Human path: this curriculum + [`LEARNING_CHARTER.md`](../LEARNING_CHARTER.md).

Automation / agent path: [`scripts/peopl_engagement_apprentice_curriculum_assign.py`](../../../../../../../../scripts/peopl_engagement_apprentice_curriculum_assign.py) (logs cohort assignment contract; CSV append remains operator-gated).
