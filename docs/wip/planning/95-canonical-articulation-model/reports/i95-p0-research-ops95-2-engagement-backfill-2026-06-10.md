---
authored: 2026-06-10
tranche: I95-T6
parent_initiative: INIT-OPENCLAW_AKOS-95
ops_id: OPS-95-2
decision_ids:
  - D-IH-73-D
  - D-IH-73-N
  - D-IH-95-G
gate_type: inline-ratify
---

# P0 research — OPS-95-2 engagement_model_id backfill

Evidence sweep before operator ratification of `ENGAGEMENT_REGISTRY.csv` col-17 backfill.

## Problem statement

Prod mirror apply (`ad3e574`, 2026-06-09) cleared **3 invalid FK values** (`tmpl_*` template IDs in an `eng_model_*`-only mirror FK). **4 rows were already empty.** Result: **all 7 engagement rows carry NULL** `engagement_model_id` in git SSOT and `compliance.engagement_registry_mirror`.

Root cause: conflation of **RevOps engagement templates** (`tmpl_*` in `ENGAGEMENT_TEMPLATE_REGISTRY.csv`) with **People Operations engagement models** (`eng_model_*` in `ENGAGEMENT_MODEL_REGISTRY.csv`). Mirror DDL FK targets only the latter (`20260515180001_i73_engagement_registry_add_engagement_model_id.sql`).

## Internal evidence sweep

| Source | Trust | Finding |
|:---|:---|:---|
| [`ENGAGEMENT_REGISTRY.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.csv) | SSOT | 7 data rows; col-17 empty on all 7 |
| [`ENGAGEMENT_MODEL_REGISTRY.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv) | SSOT | 11 rows; **active** `eng_model_*` slugs for People taxonomy: 7 core (D-IH-73-D) + 3 schema-extension (saas/rpp/one_off) |
| [`ENGAGEMENT_TEMPLATE_REGISTRY.csv`](../../../../references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/dimensions/ENGAGEMENT_TEMPLATE_REGISTRY.csv) | SSOT | 6 `tmpl_*` scaffolds; each names a **modeled-on** `eng_*` instance — pairing table below |
| `git show ad3e574` | Audit | Cleared: `eng_2026_suez_webuy` ← `tmpl_customer_outbound_full_v1`; `eng_2026_websitz_shopify` + `eng_2026_websitz_use_case_2_rushly` ← `tmpl_partner_outbound_short_pilot_v1` |
| [`operator-mirror-apply-execution-2026-06-09.md`](operator-mirror-apply-execution-2026-06-09.md) | Report | FK fail batch 156; parity PASS @ 7 engagement rows after NULL clear |
| [`OPS_REGISTER.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv) **OPS-95-2** | Tracker | Open; canonical CSV gate; mirror re-emit after backfill |
| [`COLLABORATOR_SHARE_REGISTRY.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions/COLLABORATOR_SHARE_REGISTRY.csv) | Cross-signal | SUEZ/Websitz rows use `eng_model_delivery_engagement` (invalid slug — **out of OPS-95-2 scope**; separate hygiene) |
| [`ENGAGEMENT_REGISTRY.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.md) §2 | Spec | Col-17 optional pre-backfill; non-empty MUST resolve to D-IH-73-D class |
| [`i95-full-regression-2026-06-09.md`](i95-full-regression-2026-06-09.md) **F-12** | Regression | Named forward charter; OPS-95-2 minted |

## Mirror parity (prod @ 2026-06-09 apply)

| Check | Git SSOT | Prod mirror | Parity |
|:---|:---|:---|:---|
| Row count | 7 | 7 (`engagement_reg`) | PASS |
| `engagement_model_id` non-NULL | 0 | 0 (NULL) | PASS (both empty) |
| FK to `engagement_model_registry_mirror` | N/A (all empty) | satisfied | PASS |

Post-backfill: re-emit scoped engagement_registry chunk + operator apply per [`holistika-mirror-dml-apply.md`](../../../../guides/holistika-mirror-dml-apply.md).

## Template ↔ instance pairing (RevOps scaffold → live row)

| `engagement_id` | `engagement_class` | `status` | Modeled-on template (`ENGAGEMENT_TEMPLATE_REGISTRY`) | Prior col-17 (pre-ad3e574) |
|:---|:---|:---|:---|:---|
| `eng_2026_suez_webuy` | customer-outbound | active | `tmpl_customer_outbound_full_v1` (milestone / msa_sow) | `tmpl_customer_outbound_full_v1` |
| `eng_2026_efa_collab` | partner-outbound | active | `tmpl_partner_outbound_cobrand_v1` (quarterly_subscription) | *(never set)* |
| `eng_2026_asesoria_hosteleria` | sister-business-outbound-internal | active | `tmpl_sister_business_outbound_internal_v1` (milestone / internal) | *(never set)* |
| `eng_2026_shadowgpu_inbound` | collaborator-inbound | active | `tmpl_collaborator_inbound_advisory_v1` (one_time / dpa_only) | *(never set)* |
| `eng_2026_internal_service_management_ssot` | internal | active | `tmpl_internal_service_management_v1` (one_time / internal) | *(never set)* |
| `eng_2026_websitz_shopify` | partner-outbound | active | **Mismatch:** was `tmpl_partner_outbound_short_pilot_v1`; SHARE + Hygiene C = ongoing deep-partner delivery | `tmpl_partner_outbound_short_pilot_v1` |
| `eng_2026_websitz_use_case_2_rushly` | partner-outbound | archived | `tmpl_partner_outbound_short_pilot_v1` (short pilot) | `tmpl_partner_outbound_short_pilot_v1` |

## Valid FK target set (mirror-enforced)

Only slugs present in `ENGAGEMENT_MODEL_REGISTRY.csv` with `status=active` or `planned` (mirror CHECK includes both). For OPS-95-2 backfill, restrict to **People engagement-model taxonomy** rows operators classify engagements under:

| `engagement_model_id` | Functional name | Retribution pattern |
|:---|:---|:---|
| `eng_model_hourly_consultant` | Hourly consultant | hourly |
| `eng_model_milestone_consultant` | Milestone consultant | milestone |
| `eng_model_percentage_collaborator` | Percentage collaborator | percentage |
| `eng_model_apprentice_learner` | Apprentice learner | barter_for_training |
| `eng_model_investor_advisor` | Investor advisor | equity_advisor |
| `eng_model_outsourced_helper` | Outsourced helper | hourly_low_trust |
| `eng_model_operator_self` | Operator self (internal baseline) | operator_self |

Schema-extension rows (`eng_model_saas_subscription`, `eng_model_rpp_vendor`, `eng_model_one_off_invoice`) are billing-plane routing classes — **not** appropriate for these 7 People-engagement instances per I73 charter.

## Novelty test

Backfill is **refinement** of D-IH-73-N / D-IH-73-D (I73 P9 deferred gate now triggered by mirror integrity). External citation optional.

## Structural disposition (AskQuestion batch 1)

| Option | Label | When |
|:---|:---|:---|
| **A** | Backfill `eng_model_*` per row *(recommended)* | Preserves D-IH-73-N column semantics; templates stay in RevOps registry |
| **B** | Rename col-17 → `engagement_template_id` | Rejects I73 FK design; requires DDL + Pydantic + validator churn |
| **C** | Add 18th col `engagement_template_id`; backfill both | Dual FK; scope expansion — forward charter |
| **D** | Ratify intentional NULL on all 7 until I73 P9 | Mirror stays NULL; OPS-95-2 deferred |

## Per-row proposed mapping (AskQuestion batch 2 — see proposals CSV)

Detailed options: [`i95-ops95-2-proposals.csv`](i95-ops95-2-proposals.csv).

## Scope boundary

**In (after ratify):** `ENGAGEMENT_REGISTRY.csv` col-17 only; `validate_hlk.py`; tracker + cluster map; mirror re-emit **notes** (apply may be operator-only `SUPABASE_DB_URL`).

**Out:** DDL migrations; `ENGAGEMENT_TEMPLATE_REGISTRY` edits; `COLLABORATOR_SHARE_REGISTRY` `eng_model_delivery_engagement` hygiene; PMO sweep reorg (next tranche).

## Verification (post-ratify)

```powershell
py scripts/validate_hlk.py
py scripts/verify.py pre_commit_fast
# Mirror (operator):
py scripts/verify.py compliance_mirror_emit
# Then scoped apply per holistika-mirror-dml-apply.md
```
