---
title: SOP — Lab Component Registry Maintenance
language: en
intellectual_kind: tech-canonical-sop
sop_id: SOP-LAB_COMPONENT_REGISTRY_MAINTENANCE_001
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - System Owner
last_review: 2026-06-14
last_review_by: System Owner
last_review_decision_id: D-IH-100-A
methodology_version_at_review: v3.1
status: active
register: internal
linked_canonicals:
  - LAB_COMPONENT_ECOSYSTEM_GOVERNANCE.md
  - dimensions/COMPONENT_MODULE_REGISTRY.csv
  - dimensions/VERCEL_PROJECT_SETTINGS_REGISTRY.csv
  - SOP-TECH_LAB_PLATFORM_BINDING_001.md
  - SOP-HLK_COMPONENT_SERVICE_MATRIX_MAINTENANCE_001.md
cadence: scheduled
cadence_trigger: quarterly OR after Wave-1 vendor doc change OR lab incident where registry disagrees with dashboard
---

# SOP — Lab component registry maintenance

> **What this is:** How System Owner keeps **lab component ecosystem registries** aligned with live Vercel, Cloudflare, GitHub, and Wave-2 vendor dashboards. Inventory rows live in `COMPONENT_SERVICE_MATRIX.csv` (separate SOP); this SOP governs **depth promotion** and **probe reconciliation**.

## 1. Scope

| In scope | Out of scope |
|:---|:---|
| `COMPONENT_MODULE_REGISTRY.csv` classification | Supabase DDL (I99 operator SQL gate) |
| Wave-1/2 dimension registry rows | Minting new matrix rows (matrix maintenance SOP) |
| `lab_platform_registry_reconcile.py` runs | Per-vendor standalone SOPs |

## 2. Procedure

1. Run `py scripts/validate_component_module_registry.py --self-test` and `py scripts/validate_lab_platform_registries.py --self-test`.
2. Run `py scripts/lab_platform_registry_reconcile.py` (read-only diff output).
3. For each `PARTIAL` or `DRIFT` finding, update the dimension registry row or open OPS row — never store secrets in git.
4. Bump `last_verified` on touched registry rows; set `next_verify_by` on module registry per Research Radar cadence.
5. If a matrix row needs D0→D2 promotion, add dimension registry rows in one CSV commit (registry gate).

## 3. Paired runbook

`scripts/lab_platform_registry_reconcile.py` — AC-AUTOMATION companion (AC-HUMAN: System Owner or DevOPS reviews diff).

## 4. Cross-references

- Umbrella: `LAB_COMPONENT_ECOSYSTEM_GOVERNANCE.md` §4 Component Documentation Trace
- Lab binding: `SOP-TECH_LAB_PLATFORM_BINDING_001.md`
- Initiative: `docs/wip/planning/100-lab-component-ecosystem-governance/`
