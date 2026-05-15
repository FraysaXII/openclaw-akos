---
language: en
status: draft
role_owner: PMO
classification: reference
intellectual_kind: implementation_specification
initiative_id: INIT-OPENCLAW_AKOS-73
phase: P7
linked_canonical:
  - docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/KB_HUMAN_READABILITY_CHARTER.md
  - docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/HLK_ERP_ARCHITECTURE.md
---

# KB human-readability — HLK-ERP route specification (cross-repo)

> **`hlk-erp` does not live in `openclaw-akos`.** This document is the **implementation contract** for a **sibling-repo pull request** against [`hlk-erp`](https://github.com/FraysaXII/hlk-erp), following [`SOP-CROSS_REPO_SCHEMA_PROPAGATION_001.md`](../../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/Cross%20Repo/SOP-CROSS_REPO_SCHEMA_PROPAGATION_001.md) and [`HLK_ERP_ARCHITECTURE.md`](../../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/HLK_ERP_ARCHITECTURE.md). No fictional Next.js routes are committed inside AKOS beyond this spec.

## Route table (minimal App Router surfaces)

Assume Next.js 14 App Router authenticated operator shell (see HLK ERP architecture §auth posture).

| Route path | Purpose | Primary `engagement_model_id` filter (OR where noted) | Access overlay |
|:---|:---|:---|:---|
| **`/operator/people/kb-views/operator`** | Operator-managed full internal readability (baseline carrier). | `eng_model_operator_self` | Session `access_level` ≥ **6** (Secret) aligned to Admin/O5 doctrine; KM index **unmasked** subject to numeric level. |
| **`/operator/people/kb-views/cleared`** | Cleared collaborator readability. | `eng_model_hourly_consultant` OR `eng_model_milestone_consultant` OR `eng_model_percentage_collaborator` OR `eng_model_investor_advisor` | Effective level **≤ min**(session role, **4–5** per engagement assignment). Exclude Secret-only topics by manifest / registry classification. |
| **`/operator/people/kb-views/low-trust`** | Outsourced-helper posture (**D-IH-73-E**). | `eng_model_outsourced_helper` | Force **Community / Private** band (levels **1–2**) for KB lists; scoped manifests; redaction; **work-product-only** handoff slices; block methodology-corpus shortcuts. |
| **`/operator/people/kb-views/apprentice`** | Apprentice / training-bound readability. | `eng_model_apprentice_learner` | Prefer **Internal** (**3**) and curriculum-linked manifests; suppress highly confidential governance unless explicitly in assigned module allowlist (`LEARNING_OPS_BACKLOG.csv` linkage). |

**Breadcrumb**: `People` → `KB views` → `{preset slug}` · Panel header cites [`KB_HUMAN_READABILITY_CHARTER.md`](../../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/KB_HUMAN_READABILITY_CHARTER.md) `item` classification badge per HLK ERP design grammar.

## Props / data contract (suggested TS shape)

Implement as server-component fetch + shared filter helper (exact module path is consumer-repo choice):

```ts
type EngagementModelPreset = "operator_managed" | "cleared_collaborator" | "low_trust_outsourced" | "apprentice";

type KBViewPageProps = {
  preset: EngagementModelPreset;
  engagementModelIds: string[];        // verbatim slugs from compliance mirror / ENGAGEMENT_MODEL_REGISTRY CSV regen
  maxAccessLevel: 0 | 1 | 2 | 3 | 4 | 5 | 6;
  methodologyExposure: "full" | "curriculum_only" | "none";
};
```

**Data sources:**

- Postgres mirror `compliance.engagement_model_registry_mirror` (+ view `governance.engagement_model_registry_view` per I73 P1 changelog) — **active** engagement-model rows drive filter enums.
- Joined session engagement context (future): `ENGAGEMENT_REGISTRY.engagement_model_id` FK after P9 backfill; until then ERP may default to persona-only filters for **demo** panels.

## Governance

- AKOS retains **canonical** charter + KM doctrine; **`hlk-erp`** ships UX only — no parallel KB registries in the consumer repo ([`akos-mirror-template.mdc`](../../../../../.cursor/rules/akos-mirror-template.mdc)).
- TypeScript enums / route constants **must** regen from the same slug set validated by [`scripts/validate_engagement_model_registry.py`](../../../../../scripts/validate_engagement_model_registry.py).

## Acceptance (sibling PR)

1. Four routes render without 404 behind authenticated shell.  
2. Filter unit tests fixture **7 engagement_model_id** slug coverage from CSV.  
3. `low-trust` route rejects topics above access level **2** in smoke test harness.  

