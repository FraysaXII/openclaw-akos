---
title: SOP — Data Contract Registry Maintenance
language: en
intellectual_kind: data-canonical-sop
sop_id: SOP-DATA_CONTRACT_REGISTRY_MAINTENANCE_001
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - Data Governance Lead
co_authors:
  - Data Steward
  - CDO
last_review: 2026-06-04
last_review_by: Data Governance Lead
last_review_decision_id: D-IH-93-D
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-93-D
  - D-IH-93-C
status: active
register: internal
linked_canonicals:
  - DATA_CONTRACT_STANDARD.md
  - DATA_GOVERNANCE_POLICY.md
  - DATA_CATALOG_INTEGRATION_POSTURE.md
  - dimensions/DATA_CONTRACT_REGISTRY.csv
  - ../../../People/Compliance/canonicals/process_list.csv
  - ../../../People/Compliance/canonicals/dimensions/CAPABILITY_REGISTRY.csv
linked_runbooks:
  - scripts/data_contract_registry_check.py
  - scripts/validate_data_contract_registry.py
  - scripts/dataops_quality_check.py
linked_processes:
  - hol_data_dtp_contract_registry_mtnce_001
cadence: event_triggered
cadence_trigger: new data surface mint OR DATA-FAM tranche OR contract breach OR quarterly stewardship review
---

# SOP — Data Contract Registry Maintenance

## Purpose

Operationalise **when and how** Data Steward + Data Governance Lead add,
amend, or deprecate rows in `DATA_CONTRACT_REGISTRY.csv` without duplicating
`process_list` or `CAPABILITY_REGISTRY`. Paired to the operating-model report
`docs/wip/planning/93-data-area-foundation-and-governance/reports/data-contract-registry-operating-model-2026-06-04.md`.

## Scope

| In scope | Out of scope |
|:---|:---|
| Rows in `DATA_CONTRACT_REGISTRY.csv` | Minting new process_list projects |
| One row per `(producer_process_id × data_surface)` | Replacing CAPABILITY_REGISTRY rows |
| Draft → active → deprecated lifecycle | Supabase mirror DDL (Tech/DevOPS; forward-charter) |
| P6 bulk tranches by DATA-FAM family | ODCS YAML export tooling (forward-charter per catalog posture) |

## Preconditions

1. `producer_process_id` exists in `process_list.csv`.
2. `owner_role` resolves in `baseline_organisation.csv`.
3. `quality_rules` use **DATA-01..07 only** (see `DATAOPS_DISCIPLINE.md`).
4. For `schema_ref` under `docs/`, path must exist on disk at commit time.

## Steps (AC-HUMAN)

1. **Classify the surface** — pick `data_surface` (`canonical_csv` | `mirror_table` |
   `fdw_projection` | `graph`). If both CSV and mirror exist, **two rows**.
2. **Name producer vs enforcer** — business producer (Data Owner role) on
   canonical rows; DataOps/mirror emit on mirror rows when appropriate.
3. **Draft the row** — `status=draft`; fill semantics, SLA, quality_rules, notes
   (mark forward declarations explicitly).
4. **Run validators** — see AC-AUTOMATION; fix FAIL before operator gate.
5. **Operator gate** — canonical-CSV tranche approval for net-new rows (baseline
   governance); Data Governance Lead promotes `draft` → `active`.
6. **Deprecate** — set `status=deprecated`; successor row must exist; semver bump
   on material changes to active rows.
7. **Record evidence** — tranche charter or wave UAT cites contract IDs touched.

## Steps (AC-AUTOMATION)

```powershell
py scripts/validate_data_contract_registry.py
py scripts/data_contract_registry_check.py --coverage-report
py scripts/validate_hlk.py
```

At P6+: add `py scripts/dataops_quality_check.py --sweep --data-fam <FAMILY>` when
probe profiles land.

## Cadence

| Trigger | Action |
|:---|:---|
| New governed CSV / mirror / FDW | Add or amend contract row(s) before wave-close |
| DATA-FAM tranche (P6) | Bulk rows per family batch |
| Quarterly stewardship | Run `--coverage-report`; disposition gaps inline-ratify |
| Contract probe FAIL | Amend row or fix surface; do not silence validator |

## Escalation

Data Steward → Data Governance Lead → CDO per `DATA_GOVERNANCE_POLICY.md` §3.

## Cross-references

- Standard: `DATA_CONTRACT_STANDARD.md` §2.3 (three-register model)
- Posture: `DATA_CATALOG_INTEGRATION_POSTURE.md`
- Research: `reports/research-p2b-registry-operating-model-2026-06-04.md`
