---
Item Name: Inbound Response SLA (Holistika Services)
Item Number: holistika_gtm_dtp_003
Object Class: Guideline and Procedure
Confidence Level: Safe
Security Level: 2 (Internal Use)
Entity Owner: Think Big
Area Owner: MKT
Associated Workstream: End-to-End Marketing Lead Flow
Version: 1.0
Revision Date: 2026-04-17
---

## Purpose

Define **first-response and routing SLAs** for inbound marketing and services leads aligned to [`End-to-End Marketing Lead Flow` `thi_opera_dtp_289`](../../../../../../hlk/compliance/process_list.csv) and the merged process row **`holistika_gtm_dtp_003`**.

## Scope

Applies to **Growth**, **Brand**, and **Operations/PMO** handoffs when leads enter via web forms, email, or paid/organic social into **Supabase** (or successor CRM tables) and **Calendly** scheduling.

## Procedure

1. **Capture:** Every inbound creates or updates a **single relationship record** in the CRM of record (Supabase-backed); no shadow spreadsheets.
2. **Time-to-acknowledge:** Business hours target (set by CMO): acknowledge within **4 hours** on business days unless a different number is recorded in the team calendar policy and [`decision-log.md`](../../../../../../../wip/planning/14-holistika-internal-gtm-mops/decision-log.md).
3. **Routing:** Use [`LEADS WEB Centralization and BD Routing` `thi_opera_dtp_288`](../../../../../../compliance/process_list.csv) logic—filter by lead type, assign BD or account owner per `process_list` owners.
4. **SLA breach:** Escalate to **PMO** queue with reason code (capacity, missing data, tool failure).

## Roles

- **Growth Manager:** Triage and first-line enrichment.
- **CMO:** SLA policy owner.
- **PMO:** Escalation and weekly metrics aggregation (see **SOP-GTM_WEEKLY_METRICS_REVIEW_001**).

## Verification

- Weekly sample of leads with timestamps from form → first human touch.

## Execution runbook

### Daily (Growth on-call)

- [ ] Triage new rows in CRM of record; no leads only in chat or email without a CRM row.
- [ ] For each new lead: set **first-touch timestamp** and assign owner per routing table.
- [ ] If SLA at risk before acknowledge: post in escalation channel with lead ID and blocker.

### CRM minimum fields (set in team config)

| Field | Required |
|-------|----------|
| `source` / UTM | Yes |
| `intent` (services vs product) | Yes |
| `consent_scope` | Yes |
| `first_human_touch_at` | Yes |
| `assigned_owner` | Yes |

### RACI

| Activity | Accountable | Consulted | Informed |
|----------|-------------|-----------|----------|
| SLA policy (numeric target) | CMO | Legal (if consent changes) | PMO |
| First-line triage | Growth Manager | Brand | BD |
| Escalation for tool failure | PMO | Tech | CMO |
