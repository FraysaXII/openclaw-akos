---
language: en
---

# HLK Canonical Precedence Contract

**Item Name**: Canonical Precedence Contract
**Item Number**: HLK-PRECEDENCE-001
**Version**: 1.0
**Revision Date**: 2026-04-09
**Entity Owner**: Admin
**Area Owner**: Data Architecture, Compliance

---

## Purpose

Define which HLK assets are canonical (the place where meaning is authored), which are mirrored (derived from canonical and kept in sync), and which are reference-only (historical snapshots not to be hand-edited).

## Precedence Rules

### Canonical assets (edit here first)

These are the authoritative sources of business truth. All other representations must be derived from or synchronized with these files.

| Asset | Location | Format | Scope |
|-------|----------|--------|-------|
| Organisation baseline | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv` | CSV | Roles, hierarchy, areas, entities, access levels, descriptions |
| Process baseline | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv` | CSV | Process items, granularity, ownership, metadata; optional `item_parent_1_id` / `item_parent_2_id` (stable parent `item_id`) dual-written with name columns; **`item_name` must be unique** across rows so parent pointers resolve (`py scripts/validate_hlk.py`) |
| Component and service matrix | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/COMPONENT_SERVICE_MATRIX.csv` | CSV | CTO-chain SSOT for systems, services, integrations, and platforms; joins to `baseline_organisation.csv` (`role_name`), `process_list.csv` (`item_id`), and `REPOSITORIES_REGISTRY.md` (`repo_slug`); validated with `py scripts/validate_component_service_matrix.py` (also run from `validate_hlk.py` when the file exists) |
| FINOPS counterparty register | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/FINOPS_COUNTERPARTY_REGISTER.csv` | CSV | Business Controller / CFO-chain SSOT for **counterparty** metadata (vendors, customers, partners; no monetary amounts); joins to `baseline_organisation.csv` (`role_name`), `process_list.csv` (`item_id` under `thi_finan_*`), optional `COMPONENT_SERVICE_MATRIX.csv` (`component_id`), and `REPOSITORIES_REGISTRY.md` (`repo_slug`); validated with `py scripts/validate_finops_counterparty_register.py` (also run from `validate_hlk.py` when the file exists); maintenance SOP `docs/references/hlk/v3.0/Admin/O5-1/Finance/Business Controller/SOP-HLK_FINOPS_COUNTERPARTY_REGISTER_MAINTENANCE_001.md` |
| GOI/POI register (knowledge dimension) | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/GOI_POI_REGISTER.csv` | CSV | Compliance-chain SSOT for **Groups of Interest** (organisations) and **Persons of Interest** (positions / individuals). Documents reference `ref_id` only; private entities use obfuscated display names safe for public repository visibility. Joins to `baseline_organisation.csv` (`role_owner`), `process_list.csv` (`process_item_id`). Validated with `py scripts/validate_goipoi_register.py` (also run from `validate_hlk.py` when the file exists). Maintenance SOP `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md` (Initiative [21](../../../wip/planning/21-hlk-adviser-engagement-and-goipoi/master-roadmap.md); **relocated to `dimensions/` in Initiative 32 P7 per D-IH-32-D**; legacy path `compliance/GOI_POI_REGISTER.csv` kept as deprecation alias for one cycle). **P13.4 (D-W13-D)** added optional `related_party` boolean column (enum `true`/`false`/empty; default empty backwards-compatible) to flag rows where SOC disclosure norms apply (family-owned counterparties, board members, advisors-with-equity); mirror DDL extended via `supabase/migrations/20260511020000_p13_4_goipoi_related_party.sql`. |
| ADVOPS adviser engagement disciplines | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/ADVISER_ENGAGEMENT_DISCIPLINES.csv` | CSV | PMO-chain SSOT lookup for **External Adviser Engagement plane** disciplines (Legal, Fiscal, IP, Banking, Certification, Notary, …); FK target for adviser open questions and filed instruments registers. Joins to `baseline_organisation.csv` (`canonical_role`) and `process_list.csv` (`default_process_item_id`). Validated with `py scripts/validate_adviser_disciplines.py` (also run from `validate_hlk.py`). Plane SOP `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md`; router `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/EXTERNAL_ADVISER_ROUTER.md` (Initiative [21](../../../wip/planning/21-hlk-adviser-engagement-and-goipoi/master-roadmap.md)) |
| ADVOPS adviser open questions register | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/ADVISER_OPEN_QUESTIONS.csv` | CSV | PMO/Legal-chain SSOT for adviser-facing questions and actions across all disciplines and programs. Replaces `FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md` as SSOT; vault MD becomes a derived per-discipline view. Joins to `ADVISER_ENGAGEMENT_DISCIPLINES.csv` (`discipline_id`), `GOI_POI_REGISTER.csv` (`poi_ref_id` / `goi_ref_id`), `baseline_organisation.csv` (`owner_role`). Validated with `py scripts/validate_adviser_questions.py` (also run from `validate_hlk.py`). (Initiative [21](../../../wip/planning/21-hlk-adviser-engagement-and-goipoi/master-roadmap.md)) |
| Founder filed instruments register | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/FOUNDER_FILED_INSTRUMENTS.csv` | CSV | Legal-chain SSOT for **legal/fiscal/IP/banking/certification/notary** instruments (drafts → signed → filed): tracks status, jurisdiction, dates, storage location, owner role, and counterparty GOI. Replaces `FOUNDER_FILED_INSTRUMENT_REGISTER.md` as SSOT; vault MD becomes a derived per-discipline view. Joins to `ADVISER_ENGAGEMENT_DISCIPLINES.csv` (`discipline_id`), `GOI_POI_REGISTER.csv` (`counterparty_goi_ref_id`), `baseline_organisation.csv` (`primary_owner_role`). Validated with `py scripts/validate_founder_filed_instruments.py` (also run from `validate_hlk.py`). (Initiative [21](../../../wip/planning/21-hlk-adviser-engagement-and-goipoi/master-roadmap.md)) |
| Program registry (cross-cutting dimension) | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PROGRAM_REGISTRY.csv` | CSV | PMO/Governance-chain SSOT for **programs** as a first-class axis (separate from `process_list.csv` projects). PRJ-HOL-style `program_id` (e.g. `PRJ-HOL-FOUNDING-2026`, `PRJ-HOL-KIR-2026`) is path-stable; `process_item_id` is the FK to `process_list.csv` `item_id` of `item_granularity = project` rows when one exists; `program_code` (3-letter unique, `^[A-Z]{3}$`) is the short handle for graph nodes. Program-to-program edges (`parent_program_id`, `consumes_program_ids`, `produces_for_program_ids`, `subsumes_program_ids`) are denormalized text in CSV/Postgres + typed relationships in Neo4j. First canonical CSV under the new `dimensions/` subfolder per the Initiative 22 forward layout convention. Validated with `py scripts/validate_program_registry.py` (also run from `validate_hlk.py`; cycle detection, code uniqueness, FK to baseline + process_list, STRICT forward-reference policy). Maintenance via `scripts/wave2_backfill.py --section programs` reading `docs/wip/planning/22a-i22-post-closure-followups/operator-answers-wave2.yaml`. (Initiative [23](../../../wip/planning/23-hlk-program-registry-and-program-2/master-roadmap.md)) |
| Brand voice foundation | `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VOICE_FOUNDATION.md` + `BRAND_REGISTER_MATRIX.md` + `BRAND_DO_DONT.md` + per-locale `BRAND_FRENCH_PATTERNS.md` (I66 P1) + `BRAND_SPANISH_PATTERNS.md` (I66 P1) + `BRAND_ENGLISH_PATTERNS.md` (I71 P1 Pack A1) + `BRAND_LLM_TONE_TELLS.md` (I71 P1 Pack A1, anti-LLM-tone catalog, strict-day-1) + `BRAND_LOCALISED_FORMATS.md` (I71 P2 Addition 11; per-locale number/currency/date format rules) + `canonicals/_validators/README.md` + `canonicals/_validators/register-pack.yml` + `canonicals/_validators/gantt-pack.yml` (I71 P2; Pack A2 + Addition 11 surfaces) + `canonicals/_validators/multilingual-pack.yml` (I71 P2; Pack A3 surfaces) (operator-editable rule overrides) | MD | Brand Manager-chain SSOT for **brand voice** (charter, archetype, narrative pillars, voice IS / IS NOT, register matrix, per-locale patterns, anti-LLM-tone catalog, per-locale number/currency/date formats, operator-editable rule packs). Operator's lived protocols are the source per D-IH-17 — agent does **not** invent brand craft from CSVs. **Scaffold-staged** until operator fills `operator-answers-wave2.yaml` Section 2 and runs `py scripts/wave2_backfill.py --section brand_voice`; YAML key→canonical MD writer is the I24-P0a scaffolder writer. Cited (not duplicated) by `SOP-HLK_COMMUNICATION_METHODOLOGY_001.md` Layer 1. **Validator surfaces**: `scripts/validate_brand_voice_register.py` (extended to 10 layers at I71 P1 Pack A1; strict-day-1 default per D-IH-71-F) + `scripts/validate_brand_gantt_confidence.py` (I71 P2 Pack A2; 5-level confidence ladder + 4-quadrant audience matrix + Addition 11 localised-format co-location) + `scripts/validate_brand_multilingual.py` (I71 P2 Pack A3; 3-file pattern + per-locale frontmatter cohesion). (Initiatives [24](../../../wip/planning/24-hlk-communication-methodology/master-roadmap.md), [66](../../../wip/planning/66-brand-vision-ops-sweep/master-roadmap.md), [71](../../../wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md); D-IH-17 + D-IH-24-A + D-IH-66-D + D-IH-71-A + D-IH-71-F..K + D-IH-71-L..O) |
| Communication methodology SOP (4 layers) | `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/SOP-HLK_COMMUNICATION_METHODOLOGY_001.md` | MD | Joint Brand Manager + PMO + Compliance SSOT for the four-layer methodology (brand foundation + concept + use-case + eloquence). Layer 1 cites `BRAND_VOICE_FOUNDATION.md`; Layer 2 cites canonical CSVs (GOI/POI, ADVISER_*, FOUNDER_FILED_INSTRUMENTS, PROGRAM_REGISTRY); Layer 3 resolves recipient + lens + sharing label + discipline; Layer 4 (eloquence) operates **inside** the brand voice envelope. Composer (`scripts/compose_adviser_message.py`, Initiative 24 P4) automates layer resolution; operator finalises and sends. `process_list.csv` row `thi_mkt_dtp_293` "Communication methodology maintenance" under `thi_mkt_ws_3` is the maintenance discipline (G-24-2). (Initiative [24](../../../wip/planning/24-hlk-communication-methodology/master-roadmap.md), D-IH-10) |
| Topic registry (cross-cutting dimension) | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/TOPIC_REGISTRY.csv` | CSV | KM-chain SSOT for **topics** as a first-class cross-program dimension. `topic_id` matches `^topic_[a-z0-9_]{2,64}$` and is unique. Cross-topic edges (`parent_topic`, `related_topics`, `depends_on`, `subsumes`, `subsumed_by`) are denormalized text in CSV/Postgres + typed relationships in Neo4j (`:DEPENDS_ON`, `:TOPIC_PARENT_OF`, `:RELATED_TO`, `:TOPIC_SUBSUMES`). `program_id` FK-resolves into `PROGRAM_REGISTRY.csv` or is `shared` for cross-program topics. `manifest_path` resolves to a per-topic `*.manifest.md` under `_assets/<plane>/<program_id>/<topic_id>/`. The per-topic manifest's `topic_ids:` is a **projection** that **must FK-resolve** into this CSV; drift = canonical wins. Validated with `py scripts/validate_topic_registry.py` (also run from `validate_hlk.py`; cycle detection on `parent_topic` + `depends_on`, FK to PROGRAM_REGISTRY/baseline_org, manifest_path existence). Maintenance via direct CSV edit (no scaffolder writer; topics are agent-discoverable from `_assets/`). (Initiative [25](../../../wip/planning/25-hlk-topic-graph-and-km-scalability/master-roadmap.md), D-IH-12) |
| Compliance taxonomy | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/access_levels.md` | Markdown | Access level definitions |
| Compliance taxonomy | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/confidence_levels.md` | Markdown | Confidence level definitions |
| Compliance taxonomy | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/source_taxonomy.md` | Markdown | Source categories and levels |
| Meta-SOP | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/SOP-META_PROCESS_MGMT_001.md` | Markdown | Governing procedure for all process definitions |
| Release taxonomy SOP | `docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-RELEASE_TAXONOMY_001.md` | Markdown | I71 P3 — System Owner-chain SSOT for the three release lanes (methodology `major.minor` carried by `LOGIC_CHANGE_LOG.md`; HLK vault folder path `v3.0/`; openclaw-akos SemVer + CHANGELOG + git tag) and the customer-invisible versioning posture (per `D-IH-71-D` three-lane ratification + `D-IH-71-P` SOP authoring + §6 customer-invisible posture codification). `CHANGELOG.md` policy header points here. Cross-links to `WORKSPACE_BLUEPRINT_HOLISTIKA.md` §10 + §16 (render pipeline ownership co-enforces §6 customer-invisible posture). (Initiative [71](../../../wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md), D-IH-71-D + D-IH-71-P) |
| Knowledge management contract | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/HLK_KM_TOPIC_FACT_SOURCE.md` | Markdown | Topic, Fact, Source model; output types 0–4; Output 1 manifest rules; Obsidian tag governance |
| SOPs and role-owned canonical docs | `docs/references/hlk/v3.0/.../` role-owned folders | Markdown | Individual operational procedures and case-owned canonical business documents |
| GitHub repository index (Holistika-tracked) | `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/REPOSITORIES_REGISTRY.md` | Markdown | Canonical registry of which GitHub repos Holistika tracks (URL, class, owner role, topic links); see companion `Repositories/README.md`. **Two-layer SSOT** with `REPOSITORY_REGISTRY.csv` (machine-readable canonical for metadata; markdown remains canonical for prose). Sync enforced by `py scripts/validate_repository_registry_md_csv_sync.py`. (Initiative [59](../../wip/planning/59-hlk-governance-clean-slate/master-roadmap.md), D-IH-59-D) |
| Repository registry (machine-readable) | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPOSITORY_REGISTRY.csv` | CSV | I59 P1.1 promotion of `REPOSITORIES_REGISTRY.md` into a CSV-backed dimension. Primary key `repo_slug`. FKs: `primary_owner_role` → `baseline_organisation.csv`, `topic_ids` / `api_topic_id` → `TOPIC_REGISTRY.csv`. Validated with `py scripts/validate_repository_registry.py` (header, slug format/uniqueness, github_url prefix, enums, FKs). Maintenance: edit MD + CSV in lockstep; sync validator enforces slug-set agreement. (Initiative [59](../../wip/planning/59-hlk-governance-clean-slate/master-roadmap.md), D-IH-59-D) |
| Initiative registry | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv` | CSV | I59 P1.2 — central registry for every planning initiative (across all repos). Primary key `initiative_id` (e.g. `i59_hlk_governance`). FKs: `repo_slug` → `REPOSITORY_REGISTRY.csv`, `cycle_id` → `CYCLE_REGISTER.csv`, `inception_decision_id` / `closure_decision_id` / `superseded_by` → `DECISION_REGISTER.csv` / self, `linked_topic_ids` → `TOPIC_REGISTRY.csv`, `manifests_processes` → `process_list.csv`. **Status authority** owned by `akos.planning.status_taxonomy` (`InitiativeStatus` enum + companion fields). Master-roadmap.md frontmatter is canonical for prose; CSV is canonical for metadata. Sync enforced by `py scripts/validate_initiative_registry_frontmatter_sync.py`. Validated with `py scripts/validate_initiative_registry.py`. (Initiative [59](../../wip/planning/59-hlk-governance-clean-slate/master-roadmap.md), D-IH-59-A/B/C/E) |
| OPS register | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv` | CSV | I59 P1.3 — formalises every `OPS-XX-Y` action with RICE scores, owner_class, owner_role, status, and forwarding pointers. Primary key `ops_action_id` (e.g. `OPS-58-1`). FKs: `originating_initiative_id` / `forwarded_to_initiative_id` → `INITIATIVE_REGISTRY.csv`, `owner_role` → `baseline_organisation.csv`, `linked_decision_ids` → `DECISION_REGISTER.csv`. Operator/mixed-owned rows feed `docs/wip/planning/OPERATOR_INBOX.md` (auto-rendered, P4). Validated with `py scripts/validate_ops_register.py`. (Initiative [59](../../wip/planning/59-hlk-governance-clean-slate/master-roadmap.md), D-IH-59-A/F) |
| Cycle register | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/CYCLE_REGISTER.csv` | CSV | I59 P1.4 — governs coordinating cycles (e.g. I58 multi-track forward, I59 governance). Primary key `cycle_id`. FKs: `coordinating_initiative_id` / `coordinated_initiative_ids` → `INITIATIVE_REGISTRY.csv`, `linked_topic_ids` → `TOPIC_REGISTRY.csv`. Counts (`coordinated_count`, `closed_count`) auto-recompute from registry membership. Validated with `py scripts/validate_cycle_register.py`. (Initiative [59](../../wip/planning/59-hlk-governance-clean-slate/master-roadmap.md), D-IH-59-A) |
| Engagement template registry | `docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/dimensions/ENGAGEMENT_TEMPLATE_REGISTRY.csv` | CSV | Initiative 72 P2 — Operations/RevOps-chain SSOT for **engagement templates** (versioned bundles of repeatable engagement patterns). Sibling to `ENGAGEMENT_REGISTRY.csv` (which holds active engagement instances) per `D-IH-72-F` (NOT a column-extension). Path migrated to `Operations/RevOps/canonicals/dimensions/` per `D-IH-72-Y` Round 7 (RevOps area canonicals live under `Operations/RevOps/canonicals/`, not the legacy `People/Compliance/canonicals/dimensions/` location). Primary key `template_id`. FKs: `owner_role` / `last_review_by` → `baseline_organisation.csv`, `promotion_decision_id` / `last_review_decision_id` → `DECISION_REGISTER.csv`, `ssot_path` → repo file/folder. Validated with `py scripts/validate_engagement_template_registry.py` (also run from `validate_hlk.py`). Promotion lifecycle codified in `SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md` (Initiative 72 P3 deliverable at `Operations/RevOps/canonicals/`). Mirror DDL at `supabase/migrations/20260514220000_i72_engagement_template_registry_mirror.sql`. (Initiative [72](../../../../wip/planning/72-marketing-area-governance-and-persona-registry-expansion/master-roadmap.md), D-IH-72-A + D-IH-72-F + D-IH-72-Y + D-IH-72-AH) |
| Decision register | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv` | CSV | I59 P1.5 — every governance decision (`D-IH-XX-Y` plus closure-form `D-IH-XX-CLOSURE-…`) with class, status, reversibility, decided_at, supersedes pointer, FK linkages. Primary key `decision_id`. FKs: `initiating_initiative_id` / `linked_initiative_ids` → `INITIATIVE_REGISTRY.csv`, `linked_ops_action_ids` → `OPS_REGISTER.csv`, `linked_policies` → `POLICY_REGISTER.csv`, `linked_topic_ids` → `TOPIC_REGISTRY.csv`. Markdown decision-log files remain canonical for prose; CSV is canonical for metadata. Sync (advisory) enforced by `py scripts/validate_decision_register_decision_log_md_sync.py`. Validated with `py scripts/validate_decision_register.py`. (Initiative [59](../../wip/planning/59-hlk-governance-clean-slate/master-roadmap.md), D-IH-59-E) |
| This contract | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md` | Markdown | This document |

### Layout convention (forward — Initiative 22)

A **forward layout convention** for canonical compliance assets is documented in [`README.md`](README.md) (Initiative 22 P1, 2026-04-29). Three axes — **plane**, **program / engagement**, and **topic / register name** — drive a target subfolder layout (`compliance/<plane>/`, `compliance/dimensions/`, `_assets/<plane>/<program_id>/<topic_id>/`, `<role>/programs/<program_id>/`). **Existing files stay at their current paths** until a dedicated migration initiative moves them; the README contains the deprecation-alias map. New canonical CSVs introduced after Initiative 22 must land in their target plane subfolder directly. This contract takes precedence over any inferred legacy convention.

### Process list: program grouping (convention, not a new granularity)

A **program** is an optional intermediate **workstream** row (`item_granularity=workstream`) placed between a **project** and its child workstreams, using the same duplicate-parent pattern as other nested workstreams in `process_list.csv` (`item_parent_1` and `item_parent_2` both set to the immediate ancestor `item_name` where applicable). There is **no** separate `item_granularity` value for program and **no** `item_parent_3` column—deeper trees are expressed only as additional named rows in this single CSV. Operator-approved CSV tranches: see `docs/wip/planning/02-hlk-on-akos-madeira/reports/canonical-csv-tranche-operator-approval-template.md`.

### Mirrored assets (derived, do not hand-edit without syncing back)

| Asset | Location | Sync direction | Notes |
|-------|----------|----------------|-------|
| KiRBe Supabase tables | `public.baseline_organisation`, `compliance.*` | Canonical CSV/MD --> KiRBe | Ingested from canonical; do not treat DB as the first authoring surface |
| `compliance.finops_counterparty_register_mirror` | Supabase (Postgres) | `FINOPS_COUNTERPARTY_REGISTER.csv` --> mirror | Same pattern as `process_list_mirror`: `source_git_sha`, `synced_at`; upserts via `py scripts/sync_compliance_mirrors_from_csv.py --finops-counterparty-register-only` or profile `compliance_mirror_emit`; DDL `supabase/migrations/` + staging `scripts/sql/i18_phase1_staging/`; **server-only** (`service_role`); deny `anon` / `authenticated` |
| `compliance.goipoi_register_mirror` | Supabase (Postgres) | `GOI_POI_REGISTER.csv` --> mirror | Same pattern as other compliance mirrors: `source_git_sha`, `synced_at`; upserts via `py scripts/sync_compliance_mirrors_from_csv.py --goipoi-register-only`; DDL `supabase/migrations/` + staging `scripts/sql/i21_phase1_staging/`; **server-only** (`service_role`); deny `anon` / `authenticated` (Initiative [21](../../../wip/planning/21-hlk-adviser-engagement-and-goipoi/master-roadmap.md)) |
| `compliance.adviser_engagement_disciplines_mirror` | Supabase (Postgres) | `ADVISER_ENGAGEMENT_DISCIPLINES.csv` --> mirror | Same pattern; upserts via `py scripts/sync_compliance_mirrors_from_csv.py --adviser-disciplines-only`; DDL `supabase/migrations/` + staging `scripts/sql/i21_phase1_staging/`; **server-only** (`service_role`); deny `anon` / `authenticated` (Initiative [21](../../../wip/planning/21-hlk-adviser-engagement-and-goipoi/master-roadmap.md)) |
| `compliance.adviser_open_questions_mirror` | Supabase (Postgres) | `ADVISER_OPEN_QUESTIONS.csv` --> mirror | Same pattern; upserts via `py scripts/sync_compliance_mirrors_from_csv.py --adviser-questions-only`; DDL `supabase/migrations/` + staging `scripts/sql/i21_phase1_staging/`; **server-only** (`service_role`); deny `anon` / `authenticated` (Initiative [21](../../../wip/planning/21-hlk-adviser-engagement-and-goipoi/master-roadmap.md)) |
| `compliance.founder_filed_instruments_mirror` | Supabase (Postgres) | `FOUNDER_FILED_INSTRUMENTS.csv` --> mirror | Same pattern; upserts via `py scripts/sync_compliance_mirrors_from_csv.py --founder-filed-instruments-only`; DDL `supabase/migrations/` + staging `scripts/sql/i21_phase1_staging/`; **server-only** (`service_role`); deny `anon` / `authenticated` (Initiative [21](../../../wip/planning/21-hlk-adviser-engagement-and-goipoi/master-roadmap.md)) |
| `compliance.program_registry_mirror` | Supabase (Postgres) | `PROGRAM_REGISTRY.csv` --> mirror | Same pattern; upserts via `py scripts/sync_compliance_mirrors_from_csv.py --program-registry-only`; DDL `supabase/migrations/20260429164717_i23_compliance_program_registry_mirror.sql` + staging `scripts/sql/i23_phase1_staging/`; **server-only** (`service_role`); deny `anon` / `authenticated`. Semicolon-list edge columns stored verbatim as TEXT (DAMA-pure projection of CSV); Neo4j projects typed relationships from the same edges (D-IH-18). (Initiative [23](../../../wip/planning/23-hlk-program-registry-and-program-2/master-roadmap.md)) |
| `compliance.topic_registry_mirror` | Supabase (Postgres) | `TOPIC_REGISTRY.csv` --> mirror | Same pattern; upserts via `py scripts/sync_compliance_mirrors_from_csv.py --topic-registry-only`; DDL `supabase/migrations/20260429173828_i25_compliance_topic_registry_mirror.sql` + staging `scripts/sql/i25_phase1_staging/`; **server-only** (`service_role`); deny `anon` / `authenticated`. Semicolon-list edge columns stored verbatim as TEXT (DAMA-pure projection); Neo4j projects typed relationships from the same edges (D-IH-12). (Initiative [25](../../../wip/planning/25-hlk-topic-graph-and-km-scalability/master-roadmap.md)) |
| `compliance.repository_registry_mirror` | Supabase (Postgres) | `REPOSITORY_REGISTRY.csv` --> mirror | Same pattern; upserts via `py scripts/sync_compliance_mirrors_from_csv.py --repository-registry-only`; DDL `supabase/migrations/20260506120000_i59_repository_registry_mirror.sql`; **server-only** (`service_role`); deny `anon` / `authenticated`. (Initiative [59](../../../wip/planning/59-hlk-governance-clean-slate/master-roadmap.md), D-IH-59-D) |
| `compliance.initiative_registry_mirror` | Supabase (Postgres) | `INITIATIVE_REGISTRY.csv` --> mirror | Same pattern; upserts via `py scripts/sync_compliance_mirrors_from_csv.py --initiative-registry-only`; DDL `supabase/migrations/20260506120100_i59_initiative_registry_mirror.sql`; **server-only** (`service_role`); deny `anon` / `authenticated`. Status enum CHECK constraint matches `akos.planning.status_taxonomy.InitiativeStatus`. (Initiative [59](../../../wip/planning/59-hlk-governance-clean-slate/master-roadmap.md), D-IH-59-A/B/C) |
| `compliance.ops_register_mirror` | Supabase (Postgres) | `OPS_REGISTER.csv` --> mirror | Same pattern; upserts via `py scripts/sync_compliance_mirrors_from_csv.py --ops-register-only`; DDL `supabase/migrations/20260506120200_i59_ops_register_mirror.sql`; **server-only** (`service_role`); deny `anon` / `authenticated`. Index on `rice_score DESC NULLS LAST` for inbox prioritisation queries. (Initiative [59](../../../wip/planning/59-hlk-governance-clean-slate/master-roadmap.md), D-IH-59-A/F) |
| `compliance.cycle_register_mirror` | Supabase (Postgres) | `CYCLE_REGISTER.csv` --> mirror | Same pattern; upserts via `py scripts/sync_compliance_mirrors_from_csv.py --cycle-register-only`; DDL `supabase/migrations/20260506120300_i59_cycle_register_mirror.sql`; **server-only** (`service_role`); deny `anon` / `authenticated`. (Initiative [59](../../../wip/planning/59-hlk-governance-clean-slate/master-roadmap.md), D-IH-59-A) |
| `compliance.decision_register_mirror` | Supabase (Postgres) | `DECISION_REGISTER.csv` --> mirror | Same pattern; upserts via `py scripts/sync_compliance_mirrors_from_csv.py --decision-register-only`; DDL `supabase/migrations/20260506120400_i59_decision_register_mirror.sql`; **server-only** (`service_role`); deny `anon` / `authenticated`. Markdown decision-log files remain canonical for prose. Index on `decided_at DESC` for chronology queries. (Initiative [59](../../../wip/planning/59-hlk-governance-clean-slate/master-roadmap.md), D-IH-59-E) |
| Neo4j `:Program` + `:Topic` nodes + program/topic edges | Neo4j Community (Bolt) | `PROGRAM_REGISTRY.csv` + `TOPIC_REGISTRY.csv` --> rebuilt projection via `scripts/sync_hlk_neo4j.py` | **Mirrored read index** for graph queries; **never** authoring surface (Initiative 07 D2). Constraints: `Program.program_id IS UNIQUE`, `Topic.topic_id IS UNIQUE`. Range indexes on `Program.{lifecycle_status, program_code, default_plane}` and `Topic.{lifecycle_status, topic_class, plane}`. Edges: `:CONSUMES`, `:PRODUCES_FOR`, `:PROGRAM_PARENT_OF`, `:PROGRAM_SUBSUMES` (programs); `:DEPENDS_ON`, `:TOPIC_PARENT_OF`, `:RELATED_TO`, `:TOPIC_SUBSUMES` (topics); `:UNDER_PROGRAM` (topic → program); `:OWNED_BY` (program/topic → role). Edge naming **disambiguated** to coexist with the existing `:PARENT_OF` (process → process). Graceful SKIP when Neo4j unconfigured (Initiative [23](../../../wip/planning/23-hlk-program-registry-and-program-2/master-roadmap.md) + [25](../../../wip/planning/25-hlk-topic-graph-and-km-scalability/master-roadmap.md), D-IH-18) |
| `finops.registered_fact` | Supabase (Postgres) | Operator / system writes --> Postgres | **Derived / operational** ledger-shaped facts (optional `amount_minor`, `fact_type`, joins via `counterparty_id` slug + optional Stripe ids); **not** git-canonical; CSV + Stripe authority unchanged; DDL `supabase/migrations/` + staging `scripts/sql/i19_phase1_staging/`; **server-only** (`service_role`); deny `anon` / `authenticated`; Initiative [19](../../../wip/planning/19-hlk-finops-ledger/master-roadmap.md) |
| Stripe read plane (`stripe_gtm` foreign tables) | Supabase (Postgres) | Stripe API --> Wrappers FDW | **Mirrored / derived** read projection (e.g. schema `stripe_gtm`, server `stripe_gtm_server`); **Stripe API authoritative**; do not hand-edit; `service_role`-only SELECT posture; not an HLK CSV—see Initiative 18 runbook |
| Drive folder hierarchy | Google Drive mirror | Canonical structure --> Drive | Folders map to entity/area/role tree |
| `supabase.ts` typings | Reference only until regenerated | Schema reference | Treat as typed contract snapshot |
| `compliance_001.sop_documents` | Supabase | Canonical MD SOPs --> structured mirror | Markdown is authored first; DB records are downstream |
| GitHub repository file trees | Per-repository remotes on github.com (or equivalent) | Git remote --> local clone; optional git submodule into this monorepo | **SSOT for source code** and in-repo technical docs; the vault registry row is authoritative for *membership and metadata*, not for replacing the remote tree |
| Neo4j Community graph (HLK CSV + optional v3.0 document links) | Operator or CI Neo4j instance | Canonical CSV + validated v3.0 markdown --> ``py scripts/sync_hlk_neo4j.py`` | **Mirrored read index** for multi-hop exploration; **never** an authoring surface for baselines; rebuild after canonical changes; credentials in ``~/.openclaw/.env`` (`NEO4J_*`) |

### Reference-only assets (historical, do not edit)

| Asset | Location | Notes |
|-------|----------|-------|
| SQL dumps | `full_dump.sql`, `hlk.sql`, `hlk-database-*.txt` | Migration and forensic reference only |
| Older CSV exports | `Research & Logic/.../baseline_organisation_rows (4).csv` | Superseded by `baseline_organisation.csv`; kept in Research & Logic tree only |
| Older process exports | `Research & Logic/.../process_list_1 - process_list_1.csv` | Superseded by `process_list.csv`; kept in Research & Logic tree only |

## Vault Version Governance

### v3.0 (active)

- Location: `docs/references/hlk/v3.0/`
- Status: **Active canonical vault**. All new documents go here.
- Structure: mirrors the organigram from `baseline_organisation.csv`. Folders cascade from `Admin/O5-1/` through area heads to leaf roles.
- Navigation: see `v3.0/index.md` for the full structure and usage guide.
- Platforms: Obsidian, Drive, SharePoint, Git, KiRBe, MADEIRA.

### Repository copy vs Google Drive layout

**Google Drive (operator mirror):** A parent folder such as **Research & Logic** may contain **sibling** folders for **v3.0** (active vault), **Holistik_v1.3**, and **Holistika Research v2.7**. Authoring and sync for **current** business logic target **v3.0** and **compliance** only; v1.3 and v2.7 remain historical. The **v3** designation marks a **business-logic phase** and is treated as **definitive** for active operations (it is not renamed on every edit).

**This git repository:** The path `docs/references/hlk/Research & Logic/` is a **reference-only** subtree for packaging and traceability (historical snapshots; do not treat as the active vault root). Canonical active paths in-repo are `docs/references/hlk/v3.0/` and `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/`. Obsidian or Drive roots should map to those active paths when editing canonical knowledge.

### GitHub repositories vs vault authority

Holistika uses **many GitHub repositories** (platform, internal tooling, client-delivery). The **canonical index** of which repos are tracked, how they are classified, and which `role_name` owns the relationship lives in `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/REPOSITORIES_REGISTRY.md` (policy: `Repositories/README.md`). This is analogous to the PMO Trello registry: **GitHub is not demoted as a tool**, but the **vault row** is the canonical *Holistika-facing* record for governance and topic linking. Default practice is **pointer-only** (URL + metadata in the registry and topic indexes); **git submodules** into this monorepo are optional and require explicit justification (see Repositories README). **Think Big** vault folders hold **non-repository** client/program artifacts (e.g. commercials, SOWs); see `docs/references/hlk/v3.0/Think Big/README.md`.

### v2.7 (historical reference)

- Location: `docs/references/hlk/Research & Logic/Holistika Research v2.7/`
- Status: **Read-only historical reference**. Do not edit or add new files.
- Purpose: preserves the original Obsidian vault, Drive mirror, Envoy Tech Lab showcases, and Research Dept methodology notes that informed v3.0.
- Use: reference for context, methodology sourcing, and traceability. MADEIRA may read v2.7 for context but treats v3.0 as authoritative when both cover the same topic.

### compliance/ (shared)

- Location: `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/`
- Status: **Shared governance root**. Governs both v2.7 and v3.0.
- Contents: PRECEDENCE.md, baseline_organisation.csv, process_list.csv, access_levels.md, confidence_levels.md, source_taxonomy.md, SOP-META_PROCESS_MGMT_001.md, HLK_KM_TOPIC_FACT_SOURCE.md.

### Role-owned document rule

- New active SOPs and case-owned canonical business documents live under `docs/references/hlk/v3.0/` in the owner role's folder.
- Legacy SOPs that remain under `Research & Logic/` are historical reference unless explicitly re-promoted into `v3.0/`.

### previous-project-for-product-owner-example-only/ (reference)

- Location: `docs/references/hlk/previous-project-for-product-owner-example-only/`
- Status: **Reference-only project example**. Not part of the active vault.

## Migration Note

Phase 1 consolidated the multiple mirrors into single canonical files:

- `baseline_organisation_rows.txt` and `baseline_organisation_rows (4).csv` are superseded by `baseline_organisation.csv`
- `process_list_1.csv` (semicolon) and `process_list_1 - process_list_1.csv` (comma) are superseded by `process_list.csv`

The superseded files in the `compliance/` directory have been deleted. Older copies that remain under `Research & Logic/` are reference-only and must not be edited.

## Conflict Resolution

When canonical and mirrored assets disagree:

1. Canonical wins.
2. Investigate the source of drift.
3. Resync the mirror from canonical.
4. Document the incident in the Phase report.

## SOP Role Title Mapping

Legacy SOPs use role titles that do not always match `baseline_organisation.csv` `role_name` values. The following mapping is authoritative:

| SOP role title | Canonical role_name | Notes |
|----------------|---------------------|-------|
| Application Development Lead | Tech Lead | Maps to Tech Lead (org_042) |
| System Architect | CTO or System Owner | CTO for strategic, System Owner for operational |
| Security Officer | DevOPS | Security responsibilities under DevOPS until a dedicated role exists |
| Chief Technology Officer | CTO | Normalize long-form to short-form |
| Process Owner | PMO | Generic SOP-META term; not a job title. Maps to PMO function. |
| Technical Writer | PMO | SOP authoring function under PMO |
| TBD | PMO | Placeholder for processes whose ownership is not yet assigned. Default to PMO until resolved. |

### Roles now formalized in baseline_organisation.csv

The following roles were previously aliases but are now formal org rows. They should be referenced by their canonical `role_name` directly:

| role_name | org_id | reports_to | access_level | Added |
|-----------|--------|------------|--------------|-------|
| AI Engineer | org_041 | CTO | 4 | Phase 1 |
| Tech Lead | org_042 | CTO | 4 | Phase 1 |
| Front-End Developer | org_043 | DevOPS | 3 | Phase 1 |
| Back-End Developer | org_044 | DevOPS | 3 | Phase 1 |
| Domain Specialist | org_045 | System Owner | 3 | Phase 1 |
| Data Governance Lead | org_046 | CDO | 4 | Phase 1 |
| Data Steward | org_047 | Data Governance Lead | 3 | Phase 1 |
| Database Owner | org_048 | Data Governance Lead | 3 | Phase 1 |
| UX Designer | org_049 | Brand Manager | 3 | Phase 1 |
| Growth Manager | org_050 | CMO | 4 | Phase 1 |
| Legal Counsel | org_051 | CPO | 4 | Phase 1 |
| Legal Consumer Specialist | org_052 | Legal Counsel | 3 | Phase 1 |
| Legal Collaborator Specialist | org_053 | Legal Counsel | 3 | Phase 1 |
| Intelligence Analyst | org_054 | Holistik Researcher | 4 | Phase 1 (Research formalization) |
| OSINT Analyst | org_055 | Holistik Researcher | 3 | Phase 1 (Research formalization) |
| HUMINT Specialist | org_056 | Lead Researcher | 3 | Phase 1 (Research formalization) |

### Research area promotion (Phase 1)

Research was promoted from a function under People to a formal top-level area. The Holistik Researcher now reports directly to O5-1 as an area head, peer to CFO, CPO, COO, CMO, CDO, and CTO. All researcher roles moved from `area=People` to `area=Research`. The "Research" generic alias in process_list.csv was replaced with specific role names (Holistik Researcher, Lead Researcher, Intelligence Analyst, HUMINT Specialist, OSINT Analyst).

When ingesting SOPs into `process_list.csv`, use the canonical `role_name` from the right column. If a new role is genuinely needed, add it to `baseline_organisation.csv` first.

## Config Template Convention (`.example` vs direct canonical)

AKOS and HLK use two different conventions for config files, both valid for their specific purpose:

### AKOS convention: `.example` suffix

Files like `openclaw.json.example`, `mcporter.json.example`, and `*.env.example` use the `.example` suffix because they contain `${VAR}` placeholders for secrets and environment-specific values. They are NOT optional examples -- they are the **canonical committed templates** that bootstrap translates into runtime files. The `.example` suffix signals "contains placeholders, not real credentials."

These files are:
- **Canonical templates**: the SSOT for gateway, MCP, and environment configuration
- **Bootstrap inputs**: `scripts/bootstrap.py` reads them and produces runtime files
- **Drift targets**: `scripts/check-drift.py` compares runtime against them
- **Test fixtures**: `tests/validate_configs.py` validates them

They should NOT be confused with disposable samples. They are governed artifacts.

### HLK convention: direct canonical (no `.example` suffix)

HLK compliance baselines (`baseline_organisation.csv`, `process_list.csv`, taxonomy docs) do NOT use the `.example` suffix because they contain no secrets and are directly the canonical authored truth. This is the preferred convention for any file that does not require credential placeholder substitution.

### Rule

- Use `.example` suffix ONLY when the file contains `${VAR}` credential placeholders that must not be committed with real values.
- Use direct naming (no suffix) for all other canonical files.
- Never treat an `.example` file as optional or disposable -- in AKOS, it is the committed SSOT template.

## Sync Discipline

- Do not start bulk sync automation until this contract, the compliance taxonomy, and the stable-key policy are frozen.
- Prefer deterministic, rebuildable sync over manual copy-paste between assets.
- All sync operations should be traceable and idempotent.
