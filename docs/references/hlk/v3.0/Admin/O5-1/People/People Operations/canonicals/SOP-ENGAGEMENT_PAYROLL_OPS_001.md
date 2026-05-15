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
process_list_ids: tbi_peopl_dtp_outsourced_helper_soc_review_001;tbi_peopl_dtp_percentage_collaborator_payout_001
paired_runbooks: scripts/peopl_engagement_outsourced_soc_review.py;scripts/peopl_engagement_percentage_payout.py
---

# SOP-ENGAGEMENT_PAYROLL_OPS_001 — Payroll-adjacent ops + outsourced SOC review

## 1. Purpose

Operate payroll-adjacent engagements **without** creating a second counterparty SSOT: monetary identifiers remain grounded in [`FINOPS_COUNTERPARTY_REGISTER.csv`](../../Compliance/canonicals/FINOPS_COUNTERPARTY_REGISTER.csv) per [`akos-holistika-operations.mdc`](../../../../../../../../.cursor/rules/akos-holistika-operations.mdc). Include quarterly SOC review for `eng_model_outsourced_helper` (`D-IH-73-M`).

## 2. Scope

- Outsourced helper SOC audits (`access_level` 1–2; methodology exposure forbidden).
- Percentage collaborator payout reconciliation when revenue facts land in `finops.registered_fact` (operational plane — not re-authored here).

## 3. Inputs

- Registry SOC + payment cadence fields.
- FINOPS counterparty slug references for payouts.

## 4. Steps (outsourced SOC quarterly)

1. List engagements classified `eng_model_outsourced_helper`.
2. Verify KB/tool access still scoped + redacted; confirm work-product-only deliveries (`D-IH-73-E`).
3. Validate €400/mo cap compliance where applicable.
4. Document findings in engagement internal checkpoint folder.

## 5. Steps (percentage collaborator payout — event)

1. Confirm deal event recorded per FINOPS ledger governance.
2. Compute collaborator share per agreement; never mint parallel counterparty registers — link existing FINOPS slug.

## 6. Outputs

- OPS notes / FINOPS linkage refreshed; escalations to Ethics if automation posture conflicts arise ([`ETHICAL_AUTOMATION_POSTURE.md`](../../Ethics/canonicals/ETHICAL_AUTOMATION_POSTURE.md)).

## 7. Failure modes

- Attempt to track counterparty metadata solely in People canonicals — STOP; use FINOPS register.

## 8. Cross-references

- Runbooks: [`scripts/peopl_engagement_outsourced_soc_review.py`](../../../../../../../../scripts/peopl_engagement_outsourced_soc_review.py), [`scripts/peopl_engagement_percentage_payout.py`](../../../../../../../../scripts/peopl_engagement_percentage_payout.py).
- Workspace doctrine: [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §1 + §3–§4.
