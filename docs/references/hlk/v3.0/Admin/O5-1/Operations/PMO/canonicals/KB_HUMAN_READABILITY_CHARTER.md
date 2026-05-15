---
language: en
status: active
canonical: true
role_owner: PMO
classification: way_of_working
intellectual_kind: charter
ssot: true
authored: 2026-05-15
last_review: 2026-05-15
linked_decisions:
  - D-IH-73-G
  - D-IH-73-E
companion_to:
  - ../../../People/Compliance/canonicals/HLK_KM_TOPIC_FACT_SOURCE.md
  - ../../../People/People%20Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv
---

# KB Human Readability Charter

> **Additive overlays only.** This charter prescribes **how humans navigate and trust Knowledge Base material** layered on top of existing KM governance. It **does not** replace [`HLK_KM_TOPIC_FACT_SOURCE.md`](../../../People/Compliance/canonicals/HLK_KM_TOPIC_FACT_SOURCE.md), Output-1 manifests, or the canonical vault hierarchy. Operators implement persona-scoped surfaces (HLK-ERP sibling routes described in initiative [`reports/kb-human-readability-erp-route-spec.md`](../../../../../../../wip/planning/73-people-operations-and-learning-curriculum/reports/kb-human-readability-erp-route-spec.md)) **as filters and wayfinding overlays** tied to **`engagement_model_id`** presets from [`ENGAGEMENT_MODEL_REGISTRY.csv`](../../../People/People%20Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv).

---

## Purpose

Holistika’s KM SSOT stays in git-canonical prose, CSV registers, manifests, and `v3.0/` structure. Humans with different engagement and clearance postures nevertheless need predictable **landing paths**, **confidence in what they may cite**, and **navigation that matches SOC + access semantics**. This charter aligns those readability goals with **`engagement_model_id`** — the engagement-class discriminator ratified under **D-IH-73-D** — so KB tooling (HLK-ERP panels, dossiers, future Madeira-run surfaces) exposes **trust-consistent projections** rather than accidental full-vault leakage.

---

## Personas mapped to engagement model presets

The four readability personas (**D-IH-73-G**) map **one-to-one to engagement buckets** used for KB projection. Filters always select against the **declared FK** (`engagement_model_id`) attached to engagements, mirrors, or operator session context — never inferred from prose alone.

| Persona slug (tooling/API) | Human description | Mapped `engagement_model_id` values (presets) | Registry `access_level_default` (heuristic anchor) |
|:---|:---|:---|:---|
| **`operator_managed`** | Operator baseline carrier and full internal stewardship (Holistika OS operator). | `eng_model_operator_self` | **6** (Secret) — full internal methodological and governance stack per registry row notes. |
| **`cleared_collaborator`** | Cleared collaborators: consultants, collaborators, advisors under NDA-style cleared SOC. | `eng_model_hourly_consultant`; `eng_model_milestone_consultant`; `eng_model_percentage_collaborator`; `eng_model_investor_advisor` | **4–5** (Confidential / Highly Confidential) per engagement; default column **4** except investor **5** — tighten per-role from [`baseline_organisation.csv`](../../../People/Compliance/canonicals/baseline_organisation.csv) + engagement record. |
| **`low_trust_outsourced`** | Portal-mediated or low-clearance outsourced work (**D-IH-73-E**: extra SOC; work-product scope). | `eng_model_outsourced_helper` | **1** (Community) default in registry — **enforce** capped topic lists, redaction, and work-product-only views in tooling. |
| **`apprentice`** | Apprentice / barter-training learners bound to curated curriculum intake. | `eng_model_apprentice_learner` | **3** (Internal) default — tooling must prioritize curriculum-linked topics + Learning charter paths over raw governance internals. |

**Implementation note.** “Cleared collaborator” intentionally **fans out to four IDs** — one persona row in ERP/UI, four eligible `engagement_model_id` predicates in queries (OR filter). Conversely, apprentice and outsourced personas each map to a **single** model ID.

---

## Access heuristic (via access levels taxonomy)

Operational clarity uses two layers:

1. **Numeric `access_level` (0–6)** — canonical meanings in [`access_levels.md`](../../../People/Compliance/canonicals/access_levels.md): Public through Secret. Roles receive levels via `baseline_organisation.csv`; artefacts carry levels via frontmatter and registry classification.
2. **`engagement_model_id` SOC posture** — from [`ENGAGEMENT_MODEL_REGISTRY.csv`](../../../People/People%20Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv) (`soc_posture`, `knowledge_access_level`, `access_level_default`).

**Combined rule-of-thumb:** an overlay never elevates what's visible beyond the **minimum** of session role `access_level` and engagement-model **knowledge access** posture. Outsourced-helper routes additionally apply **work-product-only** and **methodology-non-exposure** constraints per **D-IH-73-E** (aligned with registry `soc_posture: low_trust`).

---

## Navigation and wayfinding

- **Start from role + engagement.** Landing pages should expose: current persona preset, declared `engagement_model_id`, and effective `access_level` (no silent upgrades).
- **Topic → manifest → artefacts.** Preserve the KM chain defined in [`HLK_KM_TOPIC_FACT_SOURCE.md`](../../../People/Compliance/canonicals/HLK_KM_TOPIC_FACT_SOURCE.md): Topic identity, manifests under `_assets/<plane>/<program_id>/<topic_id>/`, and governed sources. Persona overlays **narrow** indexes; they do not fork SSOT directories.
- **Engagement-folder discipline.** Operational human workpapers continue to follow [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](WORKSPACE_BLUEPRINT_HOLISTIKA.md) (four-channel persistence, `_engagement-template/` shapes). KB readability routes should **deep-link** to engagement-scoped readme packs where curriculum or client delivery context applies.
- **Labels and breadcrumbs.** Prefer external-register vocabulary on any surface that leaves the operator perimeter (dual-register posture per brand rules). Internal-register tokens remain acceptable in vault-only charters and CRMINT-style internal briefings.

---

## Links to KM and People canonicals

| Subject | Canonical link |
|:---|:---|
| KM Topic–Fact–Source doctrine | [`HLK_KM_TOPIC_FACT_SOURCE.md`](../../../People/Compliance/canonicals/HLK_KM_TOPIC_FACT_SOURCE.md) |
| Engagement model presets (SOC + access defaults) | [`ENGAGEMENT_MODEL_REGISTRY.csv`](../../../People/People%20Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv) |
| Engagement instances (FK to models) | [`ENGAGEMENT_REGISTRY.csv`](../../../People/Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.csv) |
| People Compliance vs Ethics routing (artefact ownership) | [`PEOPLE_COMPLIANCE_VS_ETHICS_BOUNDARY.md`](../../../People/Compliance/canonicals/PEOPLE_COMPLIANCE_VS_ETHICS_BOUNDARY.md) |
| Workspace + engagement-folder template | [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](WORKSPACE_BLUEPRINT_HOLISTIKA.md) |

---

## Verification

When adding or altering KB overlay routes (sibling **`hlk-erp`** PRs), rerun:

`py scripts/validate_hlk_language_frontmatter.py` · `py scripts/validate_hlk_vault_links.py` · `py scripts/validate_hlk.py`

