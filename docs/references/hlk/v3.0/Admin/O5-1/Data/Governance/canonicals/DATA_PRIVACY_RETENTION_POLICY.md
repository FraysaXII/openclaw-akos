---
title: Data Privacy and Retention Policy
language: en
intellectual_kind: data-canonical
access_level: 4
audience: J-OP;J-AIC;J-ENISA
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - Data Governance Lead
co_authors:
  - Legal Counsel
  - Compliance
  - CDO
last_review: 2026-06-04
last_review_by: Data Governance Lead
last_review_at: 2026-06-04
last_review_decision_id: D-IH-93-D
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-93-D
status: active
register: internal
linked_canonicals:
  - DATA_GOVERNANCE_POLICY.md
  - DATA_CONTRACT_STANDARD.md
  - SOP-DATA_MASTERDATA_GOLDEN_RECORD_001.md
  - ../../../People/Compliance/canonicals/access_levels.md
  - ../../../People/Compliance/canonicals/dimensions/POLICY_REGISTER.csv
  - ../../../People/Compliance/canonicals/techops/COMPONENT_SERVICE_MATRIX.csv
companion_to:
  - DATA_GOVERNANCE_POLICY.md
---

# Data Privacy and Retention Policy

> Holistika **classification lattice** and **retention schedule registry** for data
> surfaces across git-canonical CSVs, Supabase mirrors, and operational stores.
> Composes existing `POLICY_REGISTER.csv` PII rows; does not replace Legal-owned redaction SOPs.
> Feeds `DATA_CONTRACT_REGISTRY.classification`, `COMPONENT_SERVICE_MATRIX.data_classification`,
> and `retention_policy_ref` population (I93 P7).

## 1. Purpose

Declare how Holistika classifies data sensitivity, how long categories are retained,
and when **legal hold** suspends deletion. Aligns with GDPR storage-limitation posture
(Art.5(1)(e)) and ENISA evidence-pack cadence already in vault.

## 2. Data classification enum

Canonical values for `classification` / `data_classification` columns:

| Value | Meaning | Typical access level | Example surfaces |
|:---|:---|:---|:---|
| `public` | Cleared for unauthenticated or public render | 0 | Marketing copy, public docs |
| `community` | External collaborators under NDA/community tier | 1 | Partner preview decks |
| `internal` | Holistika workforce default | 2–3 | Most git-canonical CSVs, internal SOPs |
| `confidential` | Named entities, engagement facts, fiscal metadata | 4–5 | GOI/POI, engagement mirrors, ENISA pack |
| `restricted` | Legal hold, regulatory submission, pre-redaction raw | 6 | Operator-only stores; legal-hold flag required |

**Mapping rule:** When a surface has numeric `access_level_data`, use the band above.
GOI/POI `sensitivity` maps: `internal` → `internal`; `confidential` → `confidential`.

**Contract registry:** `DATA_CONTRACT_REGISTRY.classification` MUST use this enum (P5+).

## 3. Retention schedule registry

Schedule IDs referenced by `retention_policy_ref` columns:

| Schedule ID | Applies to | Default period | Trim / action |
|:---|:---|:---|:---|
| `POL-DATA-GIT-CSV-DEFAULT` | Git-canonical governance CSVs | Indefinite (git history) | Amend in place; no delete |
| `POL-DATA-MIRROR-OPERATIONAL` | Supabase `compliance.*_mirror` rows | Rolling 24 months inactive | Steward-reviewed trim |
| `POL-DATA-ENGAGEMENT-FACT` | Engagement registry mirrors | Life of engagement + 7 years | Legal review before purge |
| `POL-DATA-TELEMETRY-OBS` | AIC/runtime telemetry | 90 days hot / 1 year cold | Automated roll-off |
| `POL-DOSSIER-RUN-RETENTION-V1` | `compliance.dossier_run` trends | 180 days / 1000 rows | Existing POL row — composed here |
| `POL-DATA-LEGAL-HOLD` | Any `restricted` + `legal_hold=true` | Until Legal clears hold | No automated deletion |

New schedules mint in `POLICY_REGISTER.csv` with `policy_kind=retention` when a surface
needs a bespoke period; reference the schedule ID from contracts and component matrix.

## 4. Legal hold

1. **Trigger:** Legal Counsel or Compliance sets `legal_hold=true` on `COMPONENT_SERVICE_MATRIX`
   row or opens hold ticket referencing `ref_id` / `engagement_id`.
2. **Effect:** Retention schedules pause; trim jobs skip held rows.
3. **Release:** Legal documents release in decision log; steward clears hold flag in next tranche.

## 5. GDPR / ENISA posture

| Topic | Holistika posture |
|:---|:---|
| **Storage limitation** | Schedules in §3; mirrors trimmed per schedule unless legal hold |
| **Erasure (Art.17)** | Route to Legal + Compliance; git immutability — supersede canonical rows, redact mirrors |
| **PII off-repo** | Real names in GOI/POI obfuscated per `POL-PII-GOIPOI-DISPLAY-NAME-OBFUSCATION` |
| **Amounts off-repo** | `POL-PII-FINOPS-NO-AMOUNTS-IN-GIT` — finops operational tables only |
| **ENISA evidence** | Evidence pack retention follows `confidential` + quarterly Compliance review |

## 6. Stewardship cadence

| Activity | Cadence | Owner |
|:---|:---|:---|
| Classification spot-check on new contract rows | Per tranche | Data Steward |
| Component matrix sensitivity backfill | I93 P7 tranche | Data Steward + System Owner |
| Retention trim (mirrors) | Quarterly | Data Steward + DevOPS |
| Legal-hold registry review | Quarterly | Legal Counsel |

## 7. Cross-references

- MDM golden record: `SOP-DATA_MASTERDATA_GOLDEN_RECORD_001.md`
- Data contracts: `DATA_CONTRACT_STANDARD.md` §2.1 `classification` column
- Access lattice: `access_levels.md`
