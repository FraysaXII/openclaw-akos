# Access Levels

**Item Name**: Access Level Taxonomy
**Item Number**: HLK-COMPLIANCE-ACCESS-001
**Object Class**: Baseline Reference
**Confidence Level**: Safe
**Security Level**: 2 (Internal Use)
**Entity Owner**: Holistika
**Area Owner**: Compliance, Data Architecture
**Version**: 1.0
**Revision Date**: 2026-03-31

---

## Description

This document freezes the canonical access level taxonomy used across all HLK systems, baselines, and compliance surfaces. Access levels govern the security clearance required to interact with data, processes, and organisational assets.

## Access Level Definitions

| Level | Name | Description | Typical roles |
|-------|------|-------------|---------------|
| 0 | Public | Accessible by everyone without restrictions. Default for unauthenticated or blocked users. D-Class is permanently locked at this level. | Public, D-Class |
| 1 | Community | Basic access provided to community members. Entry-level clearance for external collaborators. | Private Researcher, external collaborators |
| 2 | Private | Restricted access for sensitive, internal data. Suitable for junior internal roles with limited scope. | Senior Researcher |
| 3 | Internal | Access limited to internal personnel only. Standard operational clearance for most functional roles. | Data Engineer, Business Analyst, Project Manager, PTP, O2C, Front Office, Pricing, AV, Design, Paid Media Manager, Service Delivery Manager, Account Manager, Asset Manager, Product Owner, Ethics & Learning, Front-End Developer, Back-End Developer, Domain Specialist, Data Steward, Database Owner, UX Designer, Legal Consumer Specialist, Legal Collaborator Specialist, OSINT Analyst, HUMINT Specialist, Lead Researcher |
| 4 | Confidential | Requires proper clearance; used for sensitive operations. Management-level access for area leads and department heads. | PMO, Social Media Manager, Organisation, Talent, Business Controller, Financial Controller, Lead Data Scientist, Holistik Researcher, Compliance, SMO, Brand Manager, DevOPS, System Owner, Data Architect, AI Engineer, Tech Lead, Data Governance Lead, Growth Manager, Legal Counsel, Intelligence Analyst |
| 5 | Highly Confidential | Top-level protection; strict access controls apply. C-level executives and strategic governance roles. | CFO, CPO, COO, CMO, CDO, CTO, AIC, Susana Madeira, O5 |
| 6 | Secret | Highest classification with extremely limited access. Reserved for the Administrator and direct administrative chain. | Admin, 05-1 |

## Governance Rules

- `D-Class` is permanently locked at level 0. One must change the role before upgrading.
- `Public` starts at level 0 and must be manually promoted.
- Access levels are assigned per-role in the baseline organisation, not per-user directly.
- The `access_level` field in `baseline_organisation.csv` uses integer values `0` through `6`.
- The `compliance.access_level` table in KiRBe stores the canonical definitions with UUIDs.

## SOP Security Level Alias Resolution

Legacy SOPs use descriptive labels alongside numeric levels. The following mapping applies:

| SOP label | Canonical level | Canonical name |
|-----------|----------------|----------------|
| 2 (Internal Use) | 2 | Private |
| 3 (Restricted) | 3 | Internal |
| 3 (Commercial Use) | 3 | Internal |
| 4 (Highly Restricted) | 4 | Confidential |
| 4 (Enterprise Critical) | 4 | Confidential |

The numeric part is authoritative. Descriptive suffixes in parentheses are informational only and must not override the canonical name from this document. Validators should strip the parenthetical and map the integer to the canonical name.

## KiRBe Schema Reference

```
compliance.access_level
  id: uuid (PK)
  created_at: timestamptz
  modified_at: timestamptz
  access_level: smallint (NOT NULL)
  access_name: text
  access_description: text
```

## Frozen Values

| UUID | Level | Name |
|------|-------|------|
| 81e0136e-18bb-444b-bdc9-d8d96c215395 | 0 | Public |
| 2e734313-803d-437b-bd82-c7308d2886b9 | 1 | Community |
| 2057d06d-e1c2-4a05-810c-e51a33f86ab1 | 2 | Private |
| 234aad4d-3cdb-409b-a5bd-afa579f16322 | 3 | Internal |
| 76f7818c-f166-434c-930a-e6468b7c153f | 4 | Confidential |
| 822ba590-b537-496c-9a5d-186d6c303065 | 5 | Highly Confidential |
| 2c6b3c9b-3764-4a0b-8a36-9b8e099a3874 | 6 | Secret |
