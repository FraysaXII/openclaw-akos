---
title: Lab platform dimension harmonization proposal
language: en
intellectual_kind: research-synthesis
audience: J-OP;J-AIC
status: ratified
parent_initiative: INIT-OPENCLAW_AKOS-100
ratifying_decision_target: D-IH-100-I
governance_owner: Data Governance Office
execution_owner: System Owner
source_ledger: source-ledger.csv
authored: 2026-06-14
---

# Lab platform dimension harmonization (proposal)

> **Pending operator ratification (`D-IH-100-I`).** Mechanical P0–P8 landed registry *inventory* but not a
> Data-Governance-owned **lexicon**. That is why the minted vault reads unharmonized against
> `DATA_GOVERNANCE_POLICY.md`, Supabase EG, and cross-initiative OPS demand.

## 1. Lexicon (binding if ratified)

| Term | Layer | What it means for Holistika | SSOT home | Example |
|:---|:---|:---|:---|:---|
| **Module** | Taxonomy | One matrix `component_id` classified by governance depth D0–D3; optional pointer to a dimension registry | `COMPONENT_MODULE_REGISTRY.csv` | `comp_matriz_00015` → D2 `vercel` family |
| **Setting** | Deploy/build plane | A knob on a hosted project whose value should match git intent (Node version, env var sensitivity, region) | `dimension_kind=setting` | `build.node_version`, `env.allow_preview_dev_signin` |
| **Surface** | Edge/DNS/email plane | A public or semi-public routing artifact (DNS record, alias, SPF/DKIM) | `dimension_kind=surface` | `preview.erp.holistikaresearch.com`, SPF include |
| **Posture** | As-built vs required bar | Observed integration state against an SOP or baseline (CI workflow inventory, error budget hook, adapter status) | `dimension_kind=posture` | GitHub check-runs bound to Vercel deployment check |

**Rule (DATA governs vocabulary; Tech executes probes):**

- **Module** answers *which component* and *how deep we govern it*.
- **Setting / surface / posture** answer *which observable dimension* we reconcile for D2+ modules.
- Do **not** overload “module” for Vercel env vars or Cloudflare DNS rows — that caused the Wave-1/2 suffix drift (`*_SETTINGS_*`, `*_ZONE_SURFACE_*`, `*_POSTURE_*`).

## 2. Consolidation target

Replace nine Wave-1/2 dimension CSVs with one registry:

**Path:** `docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/dimensions/LAB_PLATFORM_DIMENSION_REGISTRY.csv`

| Column | Purpose |
|:---|:---|
| `dimension_id` | Stable key (`LAB-DIM-VER-001`) |
| `dimension_kind` | `setting` \| `surface` \| `posture` |
| `platform_slug` | `vercel` \| `cloudflare` \| `github` \| `sentry` \| … |
| `resource_ref` | Project slug, zone id, repo slug |
| `dimension_key` | Dot-path semantic key (`deploy.deployment_check`) |
| `expected_value` | Git-canonical intent |
| `probe_command` | Human or AC-AUTOMATION probe |
| `governed_status` | `inventory` \| `partial` \| `governed` |
| `owner_role` | FK `baseline_organisation.csv` |
| `component_fk` | Matrix notes tokens |
| `contract_fk` | Optional `DATA_CONTRACT_REGISTRY` |
| `last_verified` | ISO date |
| `notes` | Drift, alias, carryover |

**Deprecation:** Old CSV paths remain as **read aliases** for one release cycle; validator emits WARN then FAIL.

**Pydantic / validator:** Extend `akos/hlk_lab_platform_dimension_registry.py` (new) + fold `validate_lab_platform_registries.py`.

## 3. What stays separate

| Artifact | Why not merged |
|:---|:---|
| `COMPONENT_MODULE_REGISTRY.csv` | Taxonomy + D0–D3 depth; 1:1 matrix rows |
| `SUPABASE_MODULE_REGISTRY.csv` | Owned by Data Architecture (I99); indexed only |
| `DATA_CONTRACT_REGISTRY.csv` | Cross-area contract bar (`DC-HOL-LAB-PLATFORM-ENV-001`) |
| Vendor-specific **SOPs** when process-bound | e.g. quarterly app governance — not every DNS row |

## 4. Automation honesty (intent preservation)

| Layer | Preserves today | Does **not** preserve |
|:---|:---|:---|
| `validate_component_module_registry.py` | Row shape, enums, matrix FK tokens, D-depth consistency | Live dashboard == `expected_value` |
| `validate_lab_platform_registries.py` | Schema + cross-row FKs | Probe execution |
| `lab_platform_registry_reconcile.py` | Lists probe commands (scaffold) | Scheduled CI/cron diffs |
| `SOP-LAB_COMPONENT_REGISTRY_MAINTENANCE_001` | Quarterly human reconcile cadence | Unattended drift detection |

**Ratified automation tranche (post-harmonization):** wire AC-AUTOMATION probes into `pre_commit_fast` read-only mode (no registry mutation on failure) + optional weekly cron emitting diff artifact to `docs/wip/planning/100-.../reports/`.

## 5. Cross-area wiring

| Register | I100 harmonization action |
|:---|:---|
| `OPS_REGISTER.csv` | Reopen `OPS-100-1` note; add `OPS-100-2` harmonization tranche; **partial satisfy** `OPS-83-3` matrix backfill via posture rows — SOP forward-charter remains |
| `CAPABILITY_REGISTRY.csv` | Keep three-tier family: `CAP-TECHOPS-RELIABILITY-OBSERVABILITY` (parent) → binding → component ecosystem |
| `CAPABILITY_CONFIDENCE_REGISTRY.csv` | Seed confidence rows for both `CAP-LAB-*` (currently missing) |
| `INTELLIGENCEOPS_REGISTER.csv` | Add lab vendor doc-trace targets with per-vendor volatility |
| `process_list.csv` | Extend maintenance process AC-AUTOMATION after probe CI lands |
| `DATA_GOVERNANCE_POLICY.md` | Add § federated platform-dimension lexicon pointer (DGO edit) |

## 6. Research bar (this tranche)

| Deliverable | Status |
|:---|:---|
| Source ledger ≥750 rows | **Done** — 780 rows, `validate_research_action.py` PASS |
| Prong syntheses | This folder (`research-synthesis-*-2026-06-14.md`) |
| Research radar rows | Pending canonical mint with harmonization |
| I100 closure | **Superseded pending** `D-IH-100-I` + harmonization UAT |

## 7. Ratification ask

See inline AskQuestion: consolidate registries now vs phased; `OPS-83-3` disposition; formal I100 reopen.
