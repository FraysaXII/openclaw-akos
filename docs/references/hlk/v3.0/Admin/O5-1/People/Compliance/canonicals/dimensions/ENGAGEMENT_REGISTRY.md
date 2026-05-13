---
status: active
last_review: 2026-05-13
authoring_initiative: I70 P8.1
canonical_id: engagement_registry
owning_area: Operations
owning_role: PMO
artifact_type: dimension_schema_spec
language: en
---

# ENGAGEMENT_REGISTRY — schema specification

> Schema reference for the canonical engagement-row registry that catalogs every external/internal engagement Holistika operates. The CSV lives next to this file at [`ENGAGEMENT_REGISTRY.csv`](ENGAGEMENT_REGISTRY.csv); the Supabase mirror is `compliance.engagement_registry_mirror`; the ERP panel slot is `op_pmo_engagements`.

## 1. Why this registry

Engagements were tracked across three places before I70 P8.1:

1. Free-text mentions in `docs/wip/intelligence/<engagement>/checkpoints/` (per-engagement workspace).
2. Initiative master-roadmaps that cite client/partner engagements ad hoc.
3. Operator memory + Trello/Drive folders not visible to the agent.

The registry promotes engagement metadata into a queryable governance table so that:

- Per-engagement deliverables resolve to a single registry row (`deliverable_path`).
- The ERP panel can list active engagements per owner role.
- Cross-references from `INITIATIVE_REGISTRY.csv` and `process_list.csv` resolve back to a stable `engagement_id`.
- The 9-class enum (`engagement_class`) is the audit-grade source of truth used by GOI/POI ratifications (per §8.17 hunt).

## 2. Schema (16 columns)

| Column | Type | Required | Description |
| --- | --- | --- | --- |
| `engagement_id` | text | yes | Unique slug `^eng_[0-9]{4}_[a-z0-9_]+$`. Stable across renames. |
| `engagement_name` | text | yes | Human-readable name (operator-visible). |
| `engagement_class` | enum | yes | One of: `customer-outbound`, `partner-outbound`, `sister-business-outbound-internal`, `collaborator-inbound`, `advisor-outbound-internal`, `internal`, `trainee`, `investor-inbound`, `legal-counsel-outbound-internal`. Enum extends per §8.17 GOI hunt ratifications. |
| `counterparty_org_id` | text | conditional | External org name; empty for `internal`. |
| `owner_role` | text | yes | FK to `baseline_organisation.csv` `role_name` (or `role_owner`). |
| `status` | enum | yes | One of: `active`, `paused`, `archived`, `closed`. |
| `started_at` | date | yes | ISO `YYYY-MM-DD`. |
| `ended_at` | date | conditional | ISO `YYYY-MM-DD`. Required if `status in ('archived','closed')`. |
| `language_primary` | text | yes | ISO 639-1 (`en`, `fr`, `es`, `pt`). |
| `language_secondary` | text | optional | Same domain. |
| `deliverable_path` | text | optional | Repo-relative path to the engagement's primary deliverable workspace. |
| `supabase_mirror` | text | optional | Mirror table name (defaults to `compliance.engagement_registry_mirror`). |
| `panel_slot` | text | optional | ERP panel slot ID (`op_pmo_engagements`). |
| `related_initiatives` | text | optional | Semicolon-list of initiative IDs (`I12;I66`). |
| `classification` | text | optional | Semicolon-list per `CLASSIFICATION_LATTICE.md` axes (`fact;source`, `way_of_working`, etc.). |
| `notes` | text | optional | Free-form context. |

## 3. Engagement class enum (current)

| Class | Direction | Money flow | Example |
| --- | --- | --- | --- |
| `customer-outbound` | external | inbound (we get paid) | SUEZ × WeBuy procure-to-pay |
| `partner-outbound` | external | varies (revenue share / barter) | EFA Académie cobranding |
| `sister-business-outbound-internal` | sister-entity | internal | Holistika Hospitality |
| `collaborator-inbound` | external | none / barter | Shadow GPU technical inbound advisory |
| `advisor-outbound-internal` | internal advisor relation | none | Internal advisor council |
| `internal` | none | none | Internal Service Management SSOT |
| `trainee` | inbound | inbound (training fee) | Holistik Researcher trainee cohort |
| `investor-inbound` | external | inbound (term sheet / convertible) | Future raise window |
| `legal-counsel-outbound-internal` | external counsel | outbound (we pay) | Trademark filing counsel |

## 4. Cross-references

- [`CANONICAL_REGISTRY.csv`](../CANONICAL_REGISTRY.csv) — registry row for `engagement_registry`.
- [`baseline_organisation.csv`](../baseline_organisation.csv) — `owner_role` FK target.
- [`INITIATIVE_REGISTRY.csv`](../INITIATIVE_REGISTRY.csv) — `related_initiatives` reverse links.
- [`GOI_POI_REGISTER.csv`](GOI_POI_REGISTER.csv) — engagement-class enum is the audit-grade source for class regression hunt (§8.17).
- [`HLK_ERP_ARCHITECTURE.md`](../../../../Operations/PMO/canonicals/HLK_ERP_ARCHITECTURE.md) §4 — `op_pmo_engagements` panel slot specification.
- [`PRECEDENCE.md`](../PRECEDENCE.md) — overall compliance ranking.

## 5. Mirror + view + RLS

DDL applied at `supabase/migrations/20260513120000_engagement_registry_mirror.sql`:

- `compliance.engagement_registry_mirror` — base mirror (CHECK constraints on enums; RLS denies anon + authenticated by default).
- `governance.engagement_registry_view` — operator-facing view filtered to `status != 'archived'`.
- `compliance.engagement_registry_view_archived` — operator-facing read of archived rows for audit.

## 6. Maintenance cadence

- **Add engagement**: when a new external engagement begins, the operator (or PMO agent) appends a row + writes a row in `INITIATIVE_REGISTRY.csv` if the engagement spawns initiative work.
- **Archive**: when an engagement closes, set `status=archived` + `ended_at` + add an audit note. Row stays for historical reference.
- **Rename**: never change `engagement_id`. Update `engagement_name`.

## 7. Related SOPs

- [`SOP-ENG_DISCOVERY_QUESTIONNAIRE_001.md`](../../../../Operations/Engagement/canonicals/SOP-ENG_DISCOVERY_QUESTIONNAIRE_001.md) — engagement intake.
- [`SOP-ENG_ESTIMATION_DISCIPLINE_001.md`](../../../../Operations/Engagement/canonicals/SOP-ENG_ESTIMATION_DISCIPLINE_001.md) — engagement effort estimation.
