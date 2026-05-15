---
language: en
status: active
canonical: true
role_owner: People Operations Lead
area: People
entity: Holistika
intellectual_kind: sop
authored: 2026-05-15
last_review: 2026-05-15
process_list_id: tbi_peopl_dtp_investor_advisor_round_review_001
paired_runbook: scripts/peopl_engagement_investor_round_review.py
---

# SOP-ENGAGEMENT_OFFBOARDING_001 — Offboarding + investor-advisor round reviews

## 1. Purpose

Close engagements safely: revoke access, archive four-channel artefacts per [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md), and run investor-advisor round checkpoints (`D-IH-73-L`) including cap-table + SAFE/convertible hygiene.

## 2. Scope

Investor/advisor class engagements primarily; other classes reuse offboarding mechanics where applicable. Does **not** provide legal advice — Legal Counsel remains authoritative for instruments.

## 3. Inputs

- Latest registry row for `eng_model_investor_advisor`.
- Methodology IP tension cases defer to **I73 P8** `METHODOLOGY_IP_MINTING_PATH` deliverable (Marketing/Brand; filing-time matrix per `D-IH-73-F`).

## 4. Steps

1. Confirm engagement_model_id still valid; freeze folder snapshots (git tags / Drive export checklist).
2. Run round review checklist (cap table, vesting events, advisor obligations).
3. If advisor contributes methodology IP — invoke `D-IH-73-F` matrix at filing time (no premature brand decisions).
4. Revoke technical access consistent with [`access_levels.md`](../../Compliance/canonicals/access_levels.md).

## 5. Outputs

- Archived engagement README + mirror reconciliation notes.

## 6. Failure modes

- Missing Legal sign-off on instrument changes — block archive promotion.

## 7. Cross-references

- Runbook: [`scripts/peopl_engagement_investor_round_review.py`](../../../../../../../../scripts/peopl_engagement_investor_round_review.py).
