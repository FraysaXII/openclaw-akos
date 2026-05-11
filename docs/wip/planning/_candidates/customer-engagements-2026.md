---
language: en
status: candidate
initiative: (none) — pointer placeholder for in-flight engagements (outbound + inbound)
seeded_by: SUEZ WeBuy first-customer engagement (2026-05-10); broadened in P13.5 (2026-05-11) to include inbound adviser engagements per the workspace blueprint two-root model
last_review: 2026-05-11
authority: O5-1 + Project Manager + Account Manager
trigger_status: rolling — promotes to a chartered initiative when ≥ 2 simultaneous engagements per direction (outbound or inbound) need shared coordination
---

# Engagements 2026 — pointer placeholder (outbound + inbound)

> **This is a pointer, not a charter.** Per `_candidates/` convention (see `i60-process-list-harmonisation.md`, `i69-inframonitor-saas-product.md`), this one-page file documents *the next decision moment* without committing scope or budget. It promotes to a chartered initiative only when operator surfaces a multi-engagement coordination need. **Filename retained** as `customer-engagements-2026.md` for link stability; **content scope broadened in P13.5** to cover both engagement directions per [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md).

## Purpose

In-flight engagements live in two parallel surfaces:

- **Working space** (wip-side analysis, raw evidence, in-flight notes): [`docs/wip/intelligence/<YYYY-MM-DD>-<engagement-slug>/`](../../intelligence/)
- **Outward space** (canonical engagement folder; what Drive readers see): under [`docs/references/hlk/v3.0/Think Big/Clients/`](../../../references/hlk/v3.0/Think%20Big/Clients/) for **outbound** (Holistika provides) or [`docs/references/hlk/v3.0/Think Big/Advisers/`](../../../references/hlk/v3.0/Think%20Big/Advisers/) for **inbound** (Holistika is the customer)

This pointer simply lists open engagements so the operator and agents can see what is in flight without grepping.

## Active outbound engagements (Clients/)

External-customer + partner + product engagements use `<YYYY>-<slug>/`. Internal-capacity engagements use the reserved `<YYYY>-internal-<slug>/` prefix.

| Slug | Primary GOI | Type | Status | Working space | Outward space |
|:---|:---|:---|:---|:---|:---|
| `2026-05-10-suez-webuy-procure-to-pay` | `GOI-CUS-SUEZ-2026` (French enterprise; procure-to-pay automation) | external customer + EFA partner | Discovery — meeting Mon 11 May | [`docs/wip/intelligence/2026-05-10-suez-webuy-procure-to-pay/`](../../intelligence/2026-05-10-suez-webuy-procure-to-pay/) | [`docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/`](../../../references/hlk/v3.0/Think%20Big/Clients/2026-suez-webuy/) |
| `2026-asesoria-hosteleria` | `GOI-CUS-ASES-2026` (Asesoría Hostelería; related-party SME) | external customer (related-party flagged) | Folder seeded P13.4 (2026-05-11) — engagement not yet formally chartered | n/a (no wip working space yet) | [`docs/references/hlk/v3.0/Think Big/Clients/2026-asesoria-hosteleria/`](../../../references/hlk/v3.0/Think%20Big/Clients/2026-asesoria-hosteleria/) |

## Active inbound engagements (Advisers/)

| Slug | Primary GOI | Discipline cluster | Status | Working space | Outward space |
|:---|:---|:---|:---|:---|:---|
| `2026-holistika-incorporation` | `GOI-ADV-ENTITY-2026`, `GOI-BNK-INC-2026` | legal_constitution + banking_kyc + fiscal_readiness + enisa_certification | Mandate-phase 2 — active; canonical content in role-owner SOPs cross-linked from the Advisers folder | (canonical material lives in `Admin/O5-1/People/Legal/`, `People/Compliance/`, `Operations/PMO/`) | [`docs/references/hlk/v3.0/Think Big/Advisers/2026-holistika-incorporation/`](../../../references/hlk/v3.0/Think%20Big/Advisers/2026-holistika-incorporation/) |

## When to promote to a chartered initiative

* Two or more engagements (per direction) are open simultaneously and need shared scheduling, shared estimation discipline tweaks, or shared lessons-learned cycles.
* A repeat counterparty triggers an account-management workstream (renewal, expansion, multi-year framework).
* The estimation discipline (`SOP-ENG_ESTIMATION_DISCIPLINE_001`) collects enough engagement data for a calibration review.
* For inbound: more than one adviser-discipline cluster is open in parallel and needs shared mandate-phase tracking.

Until then, each engagement carries its own intelligence + outward folders and self-checkpoints under its own `checkpoints/` subdirectory; there is no umbrella initiative to maintain.

## Cross-references

* `WORKSPACE_BLUEPRINT_HOLISTIKA.md` — two-root model; engagement-types matrix; per-root folder shape.
* `GOI_POI_REGISTER.csv` — counterparty rows; filter `program_id = PRJ-HOL-*` or `class = external_adviser` for the inbound set.
* `SOP-ENG_DISCOVERY_QUESTIONNAIRE_001` — discovery questionnaire SOP (outbound).
* `SOP-ENG_PROPOSAL_001` — proposal SOP (outbound).
* `SOP-ENG_ENGAGEMENT_DESIGN_001` — multi-cell engagement design (outbound).
* `SOP-ENG_ESTIMATION_DISCIPLINE_001` *(in flight P3)* — pricing + effort + duration discipline (outbound).
* `SOP-EXTERNAL_ADVISER_ENGAGEMENT_001` — ADVOPS operator runbook (inbound).
* `EXTERNAL_ADVISER_ROUTER.md` — disciplines / triage map (inbound).
