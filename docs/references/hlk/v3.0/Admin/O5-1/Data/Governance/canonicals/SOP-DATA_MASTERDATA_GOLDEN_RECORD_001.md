---
title: SOP — Enterprise Master Data Golden Record
language: en
intellectual_kind: data-canonical-sop
sop_id: SOP-DATA_MASTERDATA_GOLDEN_RECORD_001
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - Data Steward
co_authors:
  - Data Governance Office
  - CDO
last_review: 2026-06-04
last_review_by: Data Steward
last_review_decision_id: D-IH-93-D
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-93-D
status: active
register: internal
linked_canonicals:
  - DATA_GOVERNANCE_POLICY.md
  - DATA_PRIVACY_RETENTION_POLICY.md
  - ../../../People/Compliance/canonicals/dimensions/GOI_POI_REGISTER.csv
  - ../../../People/Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.csv
linked_runbooks:
  - scripts/mdm_golden_record_check.py
linked_processes:
  - thi_data_dtp_32
cadence: scheduled
cadence_trigger: quarterly golden-record review OR post GOI/POI tranche OR engagement ID reconciliation (P7)
---

# SOP — Enterprise Master Data Golden Record

## Purpose

Operationalise **golden-record stewardship** for Holistika party and engagement master
data. Pairs `thi_data_dtp_32` (Enterprise MasterData — Relationship Management).

The authoritative golden record for **organisations and persons of interest** is
`GOI_POI_REGISTER.csv` keyed by stable `ref_id`. Real entity names stay off-repo per
`POL-PII-GOIPOI-DISPLAY-NAME-OBFUSCATION`; `ref_id` is the only cross-CSV join handle.

## Scope

| In scope | Out of scope |
|:---|:---|
| `GOI_POI_REGISTER.csv` add/amend/merge review | Full MDM platform procurement |
| `ref_id` uniqueness + `bridge_via` integrity | Engagement `eng_*` ↔ `ENG-*` alias resolution (I93 P7) |
| Classification alignment with privacy policy | Counterparty monetary amounts (finops operational tables only) |
| Quarterly steward sign-off | Automated entity-resolution ML pipelines |

## Roles

| Role | Responsibility |
|:---|:---|
| **Data Steward** | Runs golden-record review; proposes merges |
| **Data Governance Office** | Ratifies merge decisions; updates decision log on conflicts |
| **Account Manager / PMO** | Business authority for partner/client GOI rows |

## Match / merge rules

1. **Golden key:** `ref_id` is immutable once published. Never rename in place — mint successor row + deprecate old ref in notes.
2. **Duplicate detection:** Same `entity_kind` + `class` + `program_id` + overlapping `bridge_via` → steward review before second GOI mint.
3. **POI → GOI link:** `bridge_via` on POI rows must reference an existing GOI `ref_id`.
4. **Sensitivity:** Must use enum from `DATA_PRIVACY_RETENTION_POLICY.md` §2 (`internal` | `confidential` for GOI/POI today).
5. **Public entity flag:** `is_public_entity=true` only when display_name may appear on cleared external surfaces without obfuscation.

## Procedure

### AC-HUMAN (Data Steward)

1. Run `py scripts/mdm_golden_record_check.py --report` (or `--json` for ERP panel).
2. Review FAIL/WARN rows: duplicate keys, orphan `bridge_via`, invalid sensitivity.
3. For proposed merges: document in initiative decision log; obtain Data Governance Office ratification.
4. Apply CSV edits in single atomic commit with `validate_hlk.py` PASS.
5. Record quarterly review date on affected rows (`last_review_at`).

### AC-AUTOMATION

- `py scripts/mdm_golden_record_check.py --self-test` exits 0 at pre_commit when GOI/POI registry present.
- `validate_hlk.py` continues to enforce GOI/POI schema via existing validators.

## Acceptance criteria

- Zero duplicate `ref_id` values.
- All POI `bridge_via` targets resolve to GOI rows (when non-empty).
- Sensitivity values ⊆ privacy-policy classification enum.
- Steward review logged at least quarterly or after each GOI tranche.

## Cross-references

- Privacy classification + retention: `DATA_PRIVACY_RETENTION_POLICY.md`
- Engagement facts (consumer): `ENGAGEMENT_REGISTRY.csv` — ID reconciliation at I93 P7
- Data contracts citing parties: `DATA_CONTRACT_REGISTRY.csv`
