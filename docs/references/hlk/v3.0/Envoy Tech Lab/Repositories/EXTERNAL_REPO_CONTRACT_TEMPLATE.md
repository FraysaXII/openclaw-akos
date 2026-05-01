---
language: en
status: active
intellectual_kind: contract_template
role_owner: System Owner + PMO
area: Tech / Envoy Tech Lab
entity: Holistika Research
authority: Founder + System Owner
last_review: 2026-04-30
artifact_role: canonical_template
topic_ids:
  - topic_holistik_ops_discovery
parent_topic: topic_holistik_ops_discovery
---

# EXTERNAL_REPO_CONTRACT — Holistika SSOT consumer agreement (template)

> **Template canonical home:** `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/EXTERNAL_REPO_CONTRACT_TEMPLATE.md` (this file).
> **Instance location:** the **root** of every external repo Holistika tracks (alongside README.md). Per D-IH-32-K + D-IH-32-Q9 (P0 recommendation: at root for visibility to all rule loaders).

## What this is

A 1-page contract that pins an external Holistika-tracked repository (`boilerplate`, `hlk-erp`, `kirbe`, plus future client-delivery and platform repos) to the AKOS HLK doctrine. The repository agrees to consume the canonical knowledge dimensions read-only and not to author HLK SSOT locally.

This is part of Initiative 32 P7 (cross-repo extraction discipline, D-IH-32-K + D-IH-32-L). AKOS stays SSOT for HLK doctrine; external repos consume; nothing flows from external to AKOS as authoring.

## Repository identity

- **Repo class:** `<one of: platform | internal | client-delivery | reference>` (FK to [`REPOSITORIES_REGISTRY.md`](REPOSITORIES_REGISTRY.md))
- **Repo slug:** `<repo_slug from REPOSITORIES_REGISTRY.md>`
- **Primary owner role:** `<role_name from baseline_organisation.csv>`
- **Vault doc root in AKOS:** `<path under v3.0/Envoy Tech Lab/, or — if none>`
- **Last contract review:** `<YYYY-MM-DD>`

## The 3 invariants this repository agrees to

These are non-negotiable. Any future PR that breaks one of them will be flagged by the AKOS-side weekly REPO_HEALTH_SNAPSHOT and surfaced in the next initiative cycle.

### 1. Language frontmatter

Every canonical Markdown file in this repository declares `language: en|es|fr` in YAML frontmatter, per [`SOP-HLK_LOCALISATION_001.md`](../../Admin/O5-1/Marketing/Brand/SOP-HLK_LOCALISATION_001.md) (relocated to Brand in I32 P7).

The audience-canonical exception (D-IH-31-A) applies: artifacts whose deck-bound block feeds a single-locale external surface use the audience language.

### 2. Brand-jargon audit on external prose

Any prose this repository ships externally (dossiers, web pages, deck slides, cover-emails, public READMEs) must not contain forbidden tokens from [`BRAND_JARGON_AUDIT.md`](../../Admin/O5-1/Marketing/Brand/BRAND_JARGON_AUDIT.md) §4: internal codenames (`AKOS`, `topic_*`, `plane`), stack jargon (`RBAC`, `RLS`, `pgvector`, `FDW`, `kirbe.*`), methodology shorthand (`KM`, `MASTER`), operator-side process tokens (`TODO[OPERATOR-x]`, `dtp_`).

Internal-only prose (developer comments, implementation notes, internal SOPs) is unrestricted.

### 3. Git-canonical for source code; mirror-derived for HLK doctrine

This repository's own GitHub remote is **SSOT for its source code**. The AKOS [`REPOSITORIES_REGISTRY.md`](REPOSITORIES_REGISTRY.md) row is authoritative for *membership and metadata only* (URL, class, owner role, topic links).

For HLK doctrine (process_list, baseline_organisation, all 12 + 4 compliance.* mirrors), this repository **reads** from AKOS via the appropriate `compliance.*_mirror` Postgres tables (RLS read-only) or the dated handoff bundle when no Postgres access is available. It does NOT author HLK CSVs locally.

## The 5 "do not" rules

1. **Do not author HLK CSVs locally.** New rows in PERSONA_REGISTRY, CHANNEL_TOUCHPOINT_REGISTRY, SOURCING_REGISTER, SKILL_REGISTRY, TOUCHPOINT_KIT_CELL_REGISTRY, POLICY_REGISTER, PROGRAM_REGISTRY, TOPIC_REGISTRY, GOI_POI_REGISTER, ADVISER_*, FOUNDER_FILED_INSTRUMENTS, FINOPS_COUNTERPARTY_REGISTER, COMPONENT_SERVICE_MATRIX, baseline_organisation, process_list — request via PR to AKOS.
2. **Do not denormalise mirror data into local schemas as SSOT.** A local cache for performance is OK; calling it "the source of truth" is not.
3. **Do not skip the operator SQL gate.** Per [`operator-sql-gate.md`](../../../../wip/planning/14-holistika-internal-gtm-mops/reports/operator-sql-gate.md): no ad-hoc production DDL; proposals → operator approval → versioned migration.
4. **Do not embed AKOS HLK content as code comments.** Cite by URL or PRECEDENCE.md row reference; do not copy.
5. **Do not invent persona / channel / sourcing / skill / topic / program / GOI/POI IDs locally.** Request via PR; AKOS validators enforce ID format and FK at PR time.

## The 1 "do" rule

Read AKOS canonicals via the appropriate `compliance.*_mirror` (RLS read-only, server-side via your repository's `service_role`-scoped sync job) **or** via the dated handoff bundle if no Postgres access is available (e.g., light-touch reference-only repos like `boilerplate`).

## How AKOS observes this repository

A weekly snapshot (`scripts/snapshot_external_repos.py`) writes one row per repo into [`compliance/REPO_HEALTH_SNAPSHOT.csv`](../../../compliance/REPO_HEALTH_SNAPSHOT.csv) tracking:

- Whether this `EXTERNAL_REPO_CONTRACT.md` exists at the repo root (`has_external_repo_contract`)
- Whether `.cursor/rules/akos-mirror.mdc` exists (`has_akos_mirror_rule`; not applicable to repos without `.cursor/rules/`)
- Language-frontmatter compliance percentage on `.md` files
- Brand-jargon violation count on external-shipping surfaces
- Whether an embedded Obsidian snapshot is present (boilerplate-specific watch per D-IH-32-N)

A 4-consecutive-week regression on any external repo triggers Initiative 42 (cross-repo CI integration via GitHub Actions).

## Cross-references

- [`PRECEDENCE.md`](../../../compliance/PRECEDENCE.md) — canonical precedence ledger
- [`HOLISTIK_OPS_DISCOVERY.md`](../../Admin/O5-1/Operations/PMO/HOLISTIK_OPS_DISCOVERY.md) — 6-axis Holistik Ops doctrine
- [`SOP-HLK_LOCALISATION_001.md`](../../Admin/O5-1/Marketing/Brand/SOP-HLK_LOCALISATION_001.md) — locale policy
- [`BRAND_JARGON_AUDIT.md`](../../Admin/O5-1/Marketing/Brand/BRAND_JARGON_AUDIT.md) — forbidden tokens
- [`REPOSITORIES_REGISTRY.md`](REPOSITORIES_REGISTRY.md) — Holistika-tracked repository index
- [`operator-sql-gate.md`](../../../../wip/planning/14-holistika-internal-gtm-mops/reports/operator-sql-gate.md) — DDL approval workflow
- Initiative 32 master roadmap: [`32-holistik-ops-maturation/master-roadmap.md`](../../../../wip/planning/32-holistik-ops-maturation/master-roadmap.md)
- D-IH-32-K (cross-repo contract), D-IH-32-L (pull-based extraction), D-IH-32-N (boilerplate reference-only)
