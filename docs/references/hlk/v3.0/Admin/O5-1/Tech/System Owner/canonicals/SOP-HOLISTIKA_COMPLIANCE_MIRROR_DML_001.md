---
title: SOP — Holistika Compliance Mirror DML Apply
language: en
intellectual_kind: holistika-platform-sop
sop_id: SOP-HOLISTIKA_COMPLIANCE_MIRROR_DML_001
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - System Owner
co_authors:
  - PMO
  - Data Governance Lead
last_review: 2026-06-05
last_review_by: System Owner
last_review_decision_id: D-IH-93-CLOSURE
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-GTM-DB-6
  - D-IH-93-CLOSURE
status: active
register: internal
linked_canonicals:
  - SOP-HLK_TOOLING_STANDARDS_001.md
  - ../../../Data/Governance/canonicals/DATAOPS_DISCIPLINE.md
  - ../../../Operations/PMO/canonicals/OPERATIONAL_COHESION_DOCTRINE.md
linked_runbooks:
  - docs/guides/holistika-mirror-dml-apply.md
  - scripts/apply_mirror_batches.ps1
  - scripts/sync_compliance_mirrors_from_csv.py
  - ../../../../../../../config/verification-profiles.json
linked_processes:
  - env_tech_dtp_compliance_mirror_dml_001
  - env_tech_dtp_dataops_quality_001
cadence: gated_operator
cadence_trigger: after mirror emit OR OPS-86-15 / compliance_mirror_emit tranche
---

# SOP — Holistika Compliance Mirror DML Apply

## Purpose

Operationalise the **data plane** half of the Holistika **two-plane** model: after git-canonical
CSVs are emitted to reviewed upsert SQL, the operator loads rows into
`compliance.*_mirror` on the linked **MasterData** Supabase project.

This SOP is the **Ops/Tech executable process** companion to:

- **Data governance** — [`DATAOPS_DISCIPLINE.md`](../../../Data/Governance/canonicals/DATAOPS_DISCIPLINE.md) (DATA-02 parity, emit cadence)
- **Operator SQL gate** — [`operator-sql-gate.md`](../../../../../../../docs/wip/planning/14-holistika-internal-gtm-mops/reports/operator-sql-gate.md) (DDL vs DML separation)
- **Repo runbook** — [`docs/guides/holistika-mirror-dml-apply.md`](../../../../../../../docs/guides/holistika-mirror-dml-apply.md) (step-by-step; **D-GTM-DB-6**)

Sibling repos cite this workflow via [`EXTERNAL_REPO_CONTRACT.md`](../../../../Envoy%20Tech%20Lab/Repositories/EXTERNAL_REPO_CONTRACT_TEMPLATE.md) — they **read** mirrors; only AKOS **authors** CSV SSOT and runs emit+apply.

## Scope

| In scope | Out of scope |
|:---|:---|
| `compliance.*_mirror` row upserts from git CSV emit | `supabase/migrations/` DDL (schema plane) |
| Full bundle (`compliance_mirror_emit`) and scoped emits (`ops8615_mirror_emit`, `--*-only`) | Authoring business data in Dashboard SQL Editor |
| Linked CLI batch apply + psql alternative | Megabyte SQL Editor paste (Dashboard size limit) |

## Preconditions (AC-HUMAN)

1. **DDL applied** — target mirror tables exist (`npm run supabase db push` when migration pending).
2. **Emit complete** — `py scripts/validate_hlk.py` PASS when CSVs changed this tranche.
3. **SQL reviewed** — operator confirms emitted file(s) match git CSV row counts / intent.
4. **Project linked** — `npx supabase link` on MasterData (same session as `db push`).

## Steps (AC-HUMAN)

### 1. Emit (if not already done)

```powershell
py scripts/verify.py compliance_mirror_emit
# or scoped:
py scripts/verify.py ops8615_mirror_emit
```

### 2. Apply (preferred — linked repo)

```powershell
pwsh -File scripts/apply_mirror_batches.ps1 -Preset ops8615
# or:
pwsh -File scripts/apply_mirror_batches.ps1 -BatchDir artifacts/sql/mirror-batches/<date>
```

Uses `npm run supabase db query --linked -f` per batch (see [`SOP-HLK_TOOLING_STANDARDS_001.md`](SOP-HLK_TOOLING_STANDARDS_001.md) §3.1).

### 3. Verify DATA-02

```powershell
py scripts/dataops_quality_check.py --data-fam COMPLIANCE-MIRROR
# and/or row-count probe per holistika-mirror-dml-apply.md
```

### 4. Record evidence

- Tranche report or wave UAT mechanical section cites apply log under `artifacts/sql/`.
- For initiative closure: reference counts + date in verification report.

## Steps (AC-AUTOMATION)

- `config/verification-profiles.json` profiles `compliance_mirror_emit` / `ops8615_mirror_emit` — **emit only**; apply remains **gated_operator** (this SOP).
- `scripts/apply_mirror_batches.ps1` — mechanical driver; non-zero exit stops the batch loop.

## Acceptance criteria

| Surface | Criterion |
|:---|:---|
| AC-HUMAN | System Owner or PMO runs emit → review → apply → DATA-02 verify without break-glass SQL Editor for bulk files |
| AC-AUTOMATION | `apply_mirror_batches.ps1` exits 0; optional `probe_compliance_mirror_drift.py --verify` PASS |

## Anti-patterns

- Pasting multi-megabyte upsert monoliths into Supabase SQL Editor.
- Committing mirror DML as `supabase/migrations/*.sql` (inflates ledger; violates two-plane).
- Applying without emit review when CSV tranche changed the same day.

## Cross-references

- Envoy Tech Lab hub: [`Envoy Tech Lab/Repositories/README.md`](../../../../Envoy%20Tech%20Lab/Repositories/README.md)
- Governance lattice (Data vs Ops): [`docs/guides/holistika-ops-governance-lattice.md`](../../../../../../../docs/guides/holistika-ops-governance-lattice.md)
- Cursor rule: `.cursor/rules/akos-holistika-operations.mdc`
- Process: `env_tech_dtp_compliance_mirror_dml_001` in `process_list.csv`
