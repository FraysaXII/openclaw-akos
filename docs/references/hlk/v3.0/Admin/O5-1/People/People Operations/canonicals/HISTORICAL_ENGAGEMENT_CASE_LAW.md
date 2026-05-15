---
canonical: true
status: active
classification: internal_wayfinding
access_level: 5
language: en
register: internal
role_owner: People Operations Lead
area: People
entity: Holistika
intellectual_kind: internal_case_patterns
ssot: true
authored: 2026-05-15
last_review: 2026-05-15
companion_to:
  - ../../../canonicals/FOUNDER_TRAJECTORY_INTERNAL.md
  - ../dimensions/ENGAGEMENT_MODEL_REGISTRY.csv
  - ../../../Ethics/canonicals/ETHICAL_AUTOMATION_POSTURE.md
---

# Historical engagement patterns — internal case-law index

> **Internal only.** Wayfinding for People Operations when classifying live engagements against [`ENGAGEMENT_MODEL_REGISTRY.csv`](../dimensions/ENGAGEMENT_MODEL_REGISTRY.csv). Narrative evidence is drawn from [`FOUNDER_TRAJECTORY_INTERNAL.md`](../../../canonicals/FOUNDER_TRAJECTORY_INTERNAL.md) §2 et seq.; **counterparty and employer proper names are deliberately omitted here** (full-detail internal register stays in that companion). This document is **not legal advice**.

## 1. Purpose

- Give repeatable **pattern labels** operators can use in intake workshops without reopening full biography each time.
- Map each pattern to a **recommended primary `engagement_model_id`** (secondary classes noted where hybrids were material).

## 2. Anonymized anchor patterns

| Codename | Pattern summary (no proper names) | Typical hybrid notes |
|:---------|:------------------------------------|:---------------------|
| **Bâtard-style startup** | Early-stage venture where the founder combined **consulting-style delivery**, **hands-on product/org leadership**, **capital participation**, and **train-the-team** obligations in one relationship bundle. | Often mixes milestone or hourly consulting with **percentage-of-outcome** economics and **investor-style** instruments later in the arc. |
| **Mark-II-style apprentice arc** | Long-form **work-for-training** path: junior contributor progressively earns cleared access while executing real delivery under supervision; graduation implies promotion or certification milestone. | Maps cleanly to **barter-for-training** posture; avoid confusing with revenue-share unless contract introduces percentage terms. |
| **Alias-V-style reduced-hours researcher** | High-intensity employer role reduced to **part-time hours** so the contributor can complete a **structured research / training track** in parallel; converts to full employer analytics track after training gate. | Apprentice / training framing dominates even when W-2 or equivalent exists — classify by **retribution + KB scope**, not payroll channel alone. |
| **RCD-Legal-style transformation** | Consulting engagement delivering **many parallel initiatives** under **plain-language + executive-facing discipline** (heavy jargon allergy); often evolves into **ongoing strategic partner** posture. | Frequently combines **hourly or milestone consulting** with **percentage or success-linked** components once trust deepens. Name the firm only if operator explicitly approves external attribution — **default stays anonymized**. |
| **Operator-self / enterprise-employment carrier** | Founder’s **external employment** funds bootstrap operations while Holistika engagements stay governance-distinct — carrier role is **`operator_self`** (single instance). | Do **not** copy employer brands into customer-facing artefact registers; see [`BRAND_BASELINE_REALITY_MATRIX.md`](../../../Marketing/Brand/BRAND_BASELINE_REALITY_MATRIX.md) dual-register rules for anything leaving internal vault. |

## 3. Pattern → `engagement_model_id` mapping

| Pattern | Primary `engagement_model_id` | When to consider secondary classes |
|:--------|:------------------------------|:-----------------------------------|
| Bâtard-style startup | `eng_model_percentage_collaborator` or `eng_model_milestone_consultant` (pick by dominant retribution) | Add `eng_model_investor_advisor` when cap-table or SAFE-like instruments appear |
| Mark-II-style apprentice arc | `eng_model_apprentice_learner` | — |
| Alias-V-style reduced-hours researcher | `eng_model_apprentice_learner` | If contract introduces revenue share without training obligations, revisit toward `eng_model_percentage_collaborator` |
| RCD-Legal-style transformation | `eng_model_milestone_consultant` (program-heavy) or `eng_model_hourly_consultant` (time-heavy) | Add `eng_model_percentage_collaborator` when economics tie to customer outcomes |
| Operator-self / enterprise-employment carrier | `eng_model_operator_self` | Never used for collaborators — only the designated operator baseline |

Authoritative field semantics remain in [`ENGAGEMENT_MODEL_REGISTRY.md`](../dimensions/ENGAGEMENT_MODEL_REGISTRY.md).

## 4. Non-goals

- **Not legal advice** — contracts, IP clauses, and SOC posture still route through Legal templates + [`FINOPS_COUNTERPARTY_REGISTER.csv`](../../Compliance/canonicals/FINOPS_COUNTERPARTY_REGISTER.csv) (counterparty SSOT; no duplicate registers).
- **Not a second engagement registry** — live instances stay in [`ENGAGEMENT_REGISTRY.csv`](../../Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.csv); this file is narrative index only.
- **Not external-register prose** — keep employer/counterparty codenames internal; public decks and proposals must follow external-register hygiene.

## 5. Governance notes

- **C-73-8 (anonymization scope)** — default **full anonymization** of counterparties and employers in this index; cite [`FOUNDER_TRAJECTORY_INTERNAL.md`](../../../canonicals/FOUNDER_TRAJECTORY_INTERNAL.md) as upstream evidence, not verbatim extracts.
- Refresh when `ENGAGEMENT_MODEL_REGISTRY` adds classes or when operator authorizes named case studies.

## 6. Cross-references

- [`ENGAGEMENT_MODEL_REGISTRY.csv`](../dimensions/ENGAGEMENT_MODEL_REGISTRY.csv) — SSOT for classes.
- [`SOP-ENGAGEMENT_HIRING_LIFECYCLE_001.md`](SOP-ENGAGEMENT_HIRING_LIFECYCLE_001.md) — intake classification discipline.
- [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) — engagement folder inheritance.
- [`ETHICAL_AUTOMATION_POSTURE.md`](../../../Ethics/canonicals/ETHICAL_AUTOMATION_POSTURE.md) — workforce-impact + learning/ethics cadence context.
