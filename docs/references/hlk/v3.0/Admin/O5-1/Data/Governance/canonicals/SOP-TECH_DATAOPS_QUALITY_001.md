---
title: SOP — Tech DataOps Quality Check
language: en
intellectual_kind: data-canonical-sop
sop_id: SOP-TECH_DATAOPS_QUALITY_001
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - System Owner
co_authors:
  - Data Governance Office
  - PMO
last_review: 2026-06-04
last_review_by: Data Governance Office
last_review_decision_id: D-IH-93-C
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-86-BV
  - D-IH-90-AA
  - D-IH-93-C
  - D-IH-93-H
status: active
register: internal
linked_canonicals:
  - DATAOPS_DISCIPLINE.md
  - ../../../People/canonicals/HOLISTIKA_QUALITY_FABRIC.md
  - ../../../People/canonicals/INTER_WAVE_REGRESSION_DISCIPLINE.md
  - ../../canonicals/DATA_AREA_CHARTER.md
linked_runbooks:
  - scripts/dataops_quality_check.py
  - scripts/validate_hlk.py
  - scripts/sync_compliance_mirrors_from_csv.py
  - scripts/apply_mirror_batches.ps1
  - docs/guides/holistika-mirror-dml-apply.md
linked_processes:
  - env_tech_dtp_dataops_quality_001
  - env_tech_dtp_compliance_mirror_dml_001
cadence: event_triggered
cadence_trigger: canonical-CSV mint OR mirror upsert OR wave-close touching compliance CSVs
---

# SOP — Tech DataOps Quality Check

## Purpose

Operationalise the seven data-quality dimensions in
[`DATAOPS_DISCIPLINE.md`](DATAOPS_DISCIPLINE.md).
Every canonical CSV mint, mirror upsert, or wave-close that touches compliance
artefacts runs the DataOps quality bar before the commit lands or the wave
UAT verdict is filled in.

## Scope

| In scope | Out of scope |
|:---|:---|
| Canonical CSVs under `People/Compliance/canonicals/` and area-local registries | One-off scripts under `scripts/legacy/` |
| Pydantic SSOT modules `akos/hlk_*_csv.py` | Ephemeral debugging artefacts |
| Supabase `compliance.*_mirror` parity | Hand-edited FDW rows as business SSOT |
| FDW server health when FDW changes | Non-Holistika client-delivery repos |

## Steps (AC-HUMAN)

1. **Classify the data surface** — one of `canonical_csv` / `mirror_table` /
   `fdw_projection` / `manifest_md` / `pydantic_ssot` / `observability_evidence`.
2. **Run the seven probes** from the doctrine section 2 table (DATA-01..07).
3. **Disposition findings** via inline-ratify when WARN/FAIL (rework-now default
   for schema drift and FK gaps).
4. **Record evidence** in the wave UAT mechanical section or the tranche
   synthesis report when the change is tranche-class.

### Mirror DML apply (when emit produces SQL batches)

After emit, operator applies reviewed SQL to the linked Holistika project per
[`docs/guides/holistika-mirror-dml-apply.md`](../../../../../../../docs/guides/holistika-mirror-dml-apply.md)
(**D-GTM-DB-6**):

```powershell
pwsh -File scripts/apply_mirror_batches.ps1 -Preset ops8615
# or: -BatchDir artifacts/sql/mirror-batches/<date>
```

Verify DATA-02 row counts (`npm run supabase -- db query --linked` or
`py scripts/probe_compliance_mirror_drift.py --verify`).

## Steps (AC-AUTOMATION)

```powershell
py scripts/dataops_quality_check.py --self-test
py scripts/dataops_quality_check.py --sweep --data-surface canonical_csv
py scripts/validate_hlk.py
```

- `--self-test` exits 0 at every `pre_commit` (chassis circuit-breaker).
- Full `--sweep` runs at canonical-CSV mint + mirror-sync events (stub probes
  emit `skip` until live wiring lands; INFO ramp per doctrine section 4).

## Acceptance criteria

| Surface | Human | Automation |
|:---|:---|:---|
| AC-HUMAN | Data Governance Office or System Owner walks DATA-01..07 for the touched surface | N/A |
| AC-AUTOMATION | N/A | `--self-test` PASS at pre_commit; `--sweep` + `validate_hlk.py` PASS at mint time |

## Cross-references

- Area charter: [`DATA_AREA_CHARTER.md`](../../canonicals/DATA_AREA_CHARTER.md).
- Cursor rule: `.cursor/rules/akos-dataops-discipline.mdc`
- Holistika ops: `.cursor/rules/akos-holistika-operations.mdc` (two-plane model)
- Tracker closure: `docs/wip/planning/_trackers/dataops-activation-tracker.md`
