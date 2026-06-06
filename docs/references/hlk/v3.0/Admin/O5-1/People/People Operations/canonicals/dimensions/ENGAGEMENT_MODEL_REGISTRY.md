---
status: active
last_review: 2026-05-15
authoring_initiative: I73 P1
canonical_id: engagement_model_registry
owning_area: People
owning_role: People Operations Manager
artifact_type: dimension_schema_spec
language: en
---

# ENGAGEMENT_MODEL_REGISTRY — schema specification

> Schema reference for the canonical 7-class engagement-model taxonomy that codifies the retribution + SOC + IP + knowledge-access posture for every engagement Holistika operates. The CSV lives next to this file at [`ENGAGEMENT_MODEL_REGISTRY.csv`](ENGAGEMENT_MODEL_REGISTRY.csv); the Supabase mirror is `compliance.engagement_model_registry_mirror`; this is a **sibling dimension** to [`ENGAGEMENT_REGISTRY.csv`](../../../Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.csv) (which holds active engagement instances) per D-IH-73-C (NOT a column-extension; engagement-instance and engagement-model have distinct lifecycles, distinct ownership, distinct mirror tables).

## 1. Why this registry

Before I73 P1 the engagement landscape was tracked across three places:

1. Ad-hoc operator memory + folder names for active engagements (`docs/wip/intelligence/<engagement>/checkpoints/`).
2. [`ENGAGEMENT_REGISTRY.csv`](../../../Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.csv) — engagement *instances* with `engagement_class` enum (customer-outbound / partner-outbound / etc.) keyed on **money-flow direction**, not on **retribution structure**.
3. Implicit case-law in operator history (Bâtard 2020 / Mark-II / Alias V / RCD Legal / L'Oréal arrangement) per [`FOUNDER_TRAJECTORY_INTERNAL.md`](../../../canonicals/FOUNDER_TRAJECTORY_INTERNAL.md) §2 — never codified into a queryable taxonomy.

The registry promotes the **retribution × SOC × IP × knowledge-access** axes into a single queryable governance table so that:

- Per-engagement rows in [`ENGAGEMENT_REGISTRY.csv`](../../../Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.csv) can `engagement_model_id` FK into a stable retribution-pattern class (17th column added at I73 P1; backfill at P9 UAT).
- P3 engagement-lifecycle SOPs (hiring / onboarding / payroll / offboarding) parameterize by `engagement_model_id` instead of forking 4×7=28 SOPs (per C-73-4 default).
- P7 KB-views filter routes filter by `engagement_model_id` for the 4 KB persona views (operator-managed / cleared-collaborator / low-trust-outsourced / apprentice) per D-IH-73-G.
- The Learning curriculum (P2) routes `apprentice_learner` engagements to the Holistik Researcher curriculum (binds `apprentice_learner` ↔ curriculum at P2 commit).
- The Methodology IP minting path (P8) reads `ip_clause_class` to know which IP template to apply per engagement.

## 2. Schema (16 columns)

| Column | Type | Required | Description |
| --- | --- | --- | --- |
| `engagement_model_id` | text | yes | Unique slug `^eng_model_[a-z0-9_]+$`. Stable across renames. |
| `engagement_model_name` | text | yes | Human-readable name. |
| `retribution_pattern` | enum | yes | One of: `hourly`, `milestone`, `percentage`, `barter_for_training`, `equity_advisor`, `hourly_low_trust`, `operator_self`. The shape of the value-capture function. |
| `retribution_unit` | text | yes | Free-text unit (`hour`, `milestone_deliverable`, `percent_of_deal_revenue`, `none_barter`, `equity_share_or_advisor_grant`, `hour_capped`, `none`). |
| `typical_duration` | text | yes | Free-text duration (`3_to_6_months`, `per_deal_outcome`, `continuous`, etc.). |
| `access_level_default` | int | yes | Integer 0-6 per [`access_levels.md`](../../../Compliance/canonicals/access_levels.md). Default access for newly-onboarded engagements of this class. |
| `soc_posture` | enum | yes | One of: `standard`, `cleared`, `low_trust`, `training_only`, `internal`. The trust-classification of the engagement's collaborator. |
| `ip_clause_class` | enum | yes | One of: `standard_consultant`, `milestone_handoff`, `collaborator_share`, `training_recipient`, `advisor_nda`, `outsourced_workproduct_only`, `operator_owns_all`. The IP-clause family for the engagement's contract. |
| `knowledge_access_level` | enum | yes | One of: `full_by_engagement`, `partial_by_engagement`, `training_curriculum_only`, `work_product_scope_only`, `full_internal`. The KB-routing posture for the engagement (consumed by P7 KB-views). |
| `onboarding_pattern` | text | yes | Free-text descriptor of the onboarding flow (P3 SOP parameterization key). |
| `offboarding_pattern` | text | yes | Free-text descriptor of the offboarding flow (P3 SOP parameterization key). |
| `payment_cadence` | enum | yes | One of: `per_hour`, `per_milestone`, `per_deal_outcome`, `barter_continuous`, `per_round`, `per_hour_capped`, `none`. The retribution cadence (P3 payroll SOP key). |
| `legal_template_default` | text | yes | Free-text default legal-template label (NDA + SoW family). Actual template authoring deferred to operator + Legal Counsel (forward-charter for I73-followup). |
| `historical_examples` | text | optional | Free-text case-codename reference (Bâtard / Mark-II / Alias V / RCD Legal / L'Oréal arrangement etc.). Anchors P4 case-law cross-link. |
| `status` | enum | yes | One of: `active`, `deprecated`, `planned`. Lifecycle status per [`akos-executable-process-catalog.mdc`](../../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 2. |
| `notes` | text | optional | Free-form context; cross-references to D-IH-73-* decisions; per-row caveats. |

## 3. Seven-class taxonomy (D-IH-73-D ratified at P0; per-class enum rows ratified at P1 via D-IH-73-H..M)

| Engagement Model ID | Retribution Pattern | SOC Posture | Access Default | IP Clause Class | Historical Anchor | D-IH-73-* |
| --- | --- | --- | --- | --- | --- | --- |
| `eng_model_hourly_consultant` | `hourly` | `cleared` | 4 | `standard_consultant` | pre-bootstrapping consultant pattern | H |
| `eng_model_milestone_consultant` | `milestone` | `cleared` | 4 | `milestone_handoff` | RCD Legal as customer (Bâtard pattern) | I |
| `eng_model_percentage_collaborator` | `percentage` | `cleared` | 4 | `collaborator_share` | Bâtard 2020 (Mark-II + others) | J |
| `eng_model_apprentice_learner` | `barter_for_training` | `training_only` | 3 | `training_recipient` | Mark-II 1.5y + Alias V researcher 9mo | K |
| `eng_model_investor_advisor` | `equity_advisor` | `cleared` | 5 | `advisor_nda` | Bâtard 2020 investor pattern | L |
| `eng_model_outsourced_helper` | `hourly_low_trust` | `low_trust` | 1 | `outsourced_workproduct_only` | Fiverr/Cameroon helper pattern | M |
| `eng_model_operator_self` | `operator_self` | `internal` | 6 | `operator_owns_all` | current L'Oréal Europe arrangement | D (baseline) |

## 4. Cross-references

- Parent decision: [`decision-log.md`](../../../../../../../wip/planning/73-people-operations-and-learning-curriculum/decision-log.md) — D-IH-73-C sibling-dimension placement + D-IH-73-D 7-class taxonomy + D-IH-73-E outsourced SOC posture + D-IH-73-H..M per-class enum ratifications.
- Sibling dimension: [`ENGAGEMENT_REGISTRY.csv`](../../../Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.csv) — engagement *instances*; carries `engagement_model_id` FK column added at I73 P1.
- [`access_levels.md`](../../../Compliance/canonicals/access_levels.md) — `access_level_default` integer 0-6.
- [`baseline_organisation.csv`](../../../Compliance/canonicals/baseline_organisation.csv) — Data Owner = `People Operations Manager` (org_uuid `d4e5f6a7-7070-4bbb-d002-000000000003`; sub_area=People Operations).
- [`FOUNDER_TRAJECTORY_INTERNAL.md`](../../../canonicals/FOUNDER_TRAJECTORY_INTERNAL.md) §2 — case-law evidence (Bâtard / Mark-II / Alias V / RCD Legal / L'Oréal arrangement); `access_level=5 register=internal`.
- [`PRECEDENCE.md`](../../../Compliance/canonicals/PRECEDENCE.md) — canonical + mirror class declaration.
- [`HLK_KM_TOPIC_FACT_SOURCE.md`](../../../Compliance/canonicals/HLK_KM_TOPIC_FACT_SOURCE.md) — KM Topic-Fact-Source contract; engagement-models are facts about engagement-class governance.

## 5. Mirror + view + RLS

DDL applied at [`supabase/migrations/20260515180000_i73_compliance_engagement_model_mirror.sql`](../../../../../../../../supabase/migrations/20260515180000_i73_compliance_engagement_model_mirror.sql):

- `compliance.engagement_model_registry_mirror` — base mirror (CHECK constraints on `retribution_pattern`, `soc_posture`, `ip_clause_class`, `knowledge_access_level`, `payment_cadence`, `status` enums; RLS denies anon + authenticated by default; `service_role` ALL for sync jobs).
- `governance.engagement_model_registry_view` — operator-facing view filtered to `status='active'` for P7 KB-views consumption.

The companion DDL [`supabase/migrations/20260515180001_i73_engagement_registry_add_engagement_model_id.sql`](../../../../../../../../supabase/migrations/20260515180001_i73_engagement_registry_add_engagement_model_id.sql) adds the `engagement_model_id` FK column to `compliance.engagement_registry_mirror` with a referential constraint pointing at this mirror.

## 6. Maintenance cadence

- **Add engagement-model class**: governed by [`SOP-ENGAGEMENT_MODEL_REGISTRY_MAINTENANCE_001.md`](../SOP-ENGAGEMENT_MODEL_REGISTRY_MAINTENANCE_001.md) (forward-charter; authored at P3 alongside the 4 engagement-lifecycle SOPs). Operator approval gate required because adding a class touches the canonical CSV.
- **Deprecate a class**: set `status=deprecated` + add deprecation note. Existing `ENGAGEMENT_REGISTRY.csv` rows referencing the deprecated `engagement_model_id` MUST be reassigned or archived; never silent-drop.
- **Rename a class**: never change `engagement_model_id`. Update `engagement_model_name` only.
- **Backfill existing ENGAGEMENT_REGISTRY rows with `engagement_model_id`**: deferred to P9 UAT per operator's first-engagement-onboarded scenario (D-IH-73-B charter-satisfies-gate). Validator allows empty `engagement_model_id` on existing rows; enforces FK only on non-empty values.

## 7. Related SOPs and process_list rows

- `tbi_peopl_dtp_engagement_model_registry_mtnce_001` — Engagement Model Registry maintenance (P1 mint; Data Owner: People Operations Manager).
- `tbi_peopl_dtp_engagement_model_classification_001` — Per-engagement classification at intake (P1 mint; called from P3 SOP-ENGAGEMENT_HIRING_LIFECYCLE_001).
- `tbi_peopl_dtp_engagement_lifecycle_routing_001` — Routing engagement to correct lifecycle SOP at intake (P1 mint).
- `tbi_peopl_dtp_outsourced_helper_soc_review_001` — SOC posture review for outsourced helpers (P1 mint per D-IH-73-E).
- `tbi_peopl_dtp_apprentice_curriculum_assignment_001` — Apprentice ↔ curriculum binding (P1 mint; cross-link to P2 Learning charter).
- `tbi_peopl_dtp_percentage_collaborator_payout_001` — % collaborator payout reconciliation (P1 mint; cross-link to FINOPS).
- `tbi_peopl_dtp_investor_advisor_round_review_001` — Investor/advisor round review cadence (P1 mint).

The four lifecycle SOPs (P3 deliverables) — [`SOP-ENGAGEMENT_HIRING_LIFECYCLE_001.md`](../SOP-ENGAGEMENT_HIRING_LIFECYCLE_001.md) / [`SOP-ENGAGEMENT_ONBOARDING_001.md`](../SOP-ENGAGEMENT_ONBOARDING_001.md) / [`SOP-ENGAGEMENT_PAYROLL_OPS_001.md`](../SOP-ENGAGEMENT_PAYROLL_OPS_001.md) / [`SOP-ENGAGEMENT_OFFBOARDING_001.md`](../SOP-ENGAGEMENT_OFFBOARDING_001.md) — are forward-linked here; they parameterize by `engagement_model_id` from this registry.

## 8. Validators

- [`scripts/validate_engagement_model_registry.py`](../../../../../../../../scripts/validate_engagement_model_registry.py) — header drift gate + per-row enum + access_level integer 0-6 + slug regex.
- [`scripts/validate_compliance_schema_drift.py`](../../../../../../../../scripts/validate_compliance_schema_drift.py) — `_REGISTRY` tuple appended at I73 P1; gates header parity with [`akos/hlk_engagement_model_csv.py`](../../../../../../../../akos/hlk_engagement_model_csv.py) `ENGAGEMENT_MODEL_FIELDNAMES`.
- [`scripts/validate_hlk.py`](../../../../../../../../scripts/validate_hlk.py) — dispatcher graph appended at I73 P1.

Validators are wired into [`config/verification-profiles.json`](../../../../../../../../config/verification-profiles.json) profile `engagement_model_registry_smoke` and into `pre_commit` via the standard release-gate composition.
