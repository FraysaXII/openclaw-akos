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
| Organisation baseline | `docs/references/hlk/compliance/baseline_organisation.csv` | CSV | Roles, hierarchy, areas, entities, access levels, descriptions |
| Process baseline | `docs/references/hlk/compliance/process_list.csv` | CSV | Process items, granularity, ownership, metadata; optional `item_parent_1_id` / `item_parent_2_id` (stable parent `item_id`) dual-written with name columns; **`item_name` must be unique** across rows so parent pointers resolve (`py scripts/validate_hlk.py`) |
| Compliance taxonomy | `docs/references/hlk/compliance/access_levels.md` | Markdown | Access level definitions |
| Compliance taxonomy | `docs/references/hlk/compliance/confidence_levels.md` | Markdown | Confidence level definitions |
| Compliance taxonomy | `docs/references/hlk/compliance/source_taxonomy.md` | Markdown | Source categories and levels |
| Meta-SOP | `docs/references/hlk/compliance/SOP-META_PROCESS_MGMT_001.md` | Markdown | Governing procedure for all process definitions |
| Knowledge management contract | `docs/references/hlk/compliance/HLK_KM_TOPIC_FACT_SOURCE.md` | Markdown | Topic, Fact, Source model; output types 0–4; Output 1 manifest rules; Obsidian tag governance |
| SOPs and role-owned canonical docs | `docs/references/hlk/v3.0/.../` role-owned folders | Markdown | Individual operational procedures and case-owned canonical business documents |
| GitHub repository index (Holistika-tracked) | `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/REPOSITORIES_REGISTRY.md` | Markdown | Canonical registry of which GitHub repos Holistika tracks (URL, class, owner role, topic links); see companion `Repositories/README.md` |
| This contract | `docs/references/hlk/compliance/PRECEDENCE.md` | Markdown | This document |

### Process list: program grouping (convention, not a new granularity)

A **program** is an optional intermediate **workstream** row (`item_granularity=workstream`) placed between a **project** and its child workstreams, using the same duplicate-parent pattern as other nested workstreams in `process_list.csv` (`item_parent_1` and `item_parent_2` both set to the immediate ancestor `item_name` where applicable). There is **no** separate `item_granularity` value for program and **no** `item_parent_3` column—deeper trees are expressed only as additional named rows in this single CSV. Operator-approved CSV tranches: see `docs/wip/planning/02-hlk-on-akos-madeira/reports/canonical-csv-tranche-operator-approval-template.md`.

### Mirrored assets (derived, do not hand-edit without syncing back)

| Asset | Location | Sync direction | Notes |
|-------|----------|----------------|-------|
| KiRBe Supabase tables | `public.baseline_organisation`, `compliance.*` | Canonical CSV/MD --> KiRBe | Ingested from canonical; do not treat DB as the first authoring surface |
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

**This git repository:** The path `docs/references/hlk/Research & Logic/` is a **reference-only** subtree for packaging and traceability (historical snapshots; do not treat as the active vault root). Canonical active paths in-repo are `docs/references/hlk/v3.0/` and `docs/references/hlk/compliance/`. Obsidian or Drive roots should map to those active paths when editing canonical knowledge.

### GitHub repositories vs vault authority

Holistika uses **many GitHub repositories** (platform, internal tooling, client-delivery). The **canonical index** of which repos are tracked, how they are classified, and which `role_name` owns the relationship lives in `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/REPOSITORIES_REGISTRY.md` (policy: `Repositories/README.md`). This is analogous to the PMO Trello registry: **GitHub is not demoted as a tool**, but the **vault row** is the canonical *Holistika-facing* record for governance and topic linking. Default practice is **pointer-only** (URL + metadata in the registry and topic indexes); **git submodules** into this monorepo are optional and require explicit justification (see Repositories README). **Think Big** vault folders hold **non-repository** client/program artifacts (e.g. commercials, SOWs); see `docs/references/hlk/v3.0/Think Big/README.md`.

### v2.7 (historical reference)

- Location: `docs/references/hlk/Research & Logic/Holistika Research v2.7/`
- Status: **Read-only historical reference**. Do not edit or add new files.
- Purpose: preserves the original Obsidian vault, Drive mirror, Envoy Tech Lab showcases, and Research Dept methodology notes that informed v3.0.
- Use: reference for context, methodology sourcing, and traceability. MADEIRA may read v2.7 for context but treats v3.0 as authoritative when both cover the same topic.

### compliance/ (shared)

- Location: `docs/references/hlk/compliance/`
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
