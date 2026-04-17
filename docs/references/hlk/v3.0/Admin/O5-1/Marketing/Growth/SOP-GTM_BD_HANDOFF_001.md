---
Item Name: BD handoff from marketing qualification
Item Number: thi_opera_dtp_289
Object Class: Guideline and Procedure
Confidence Level: Safe
Security Level: 2 (Internal Use)
Entity Owner: Think Big
Area Owner: Operations
Associated Workstream: End-to-End Marketing Lead Flow
Version: 1.0
Revision Date: 2026-04-17
---

## Purpose

Standardize **handoff from marketing qualification to Business Development** for leads under [`End-to-End Marketing Lead Flow` `thi_opera_dtp_289`](../../../../../../compliance/process_list.csv) and parent [`LEADS WEB Centralization and BD Routing` `thi_opera_dtp_288`](../../../../../../compliance/process_list.csv).

## Procedure

1. **Minimum data:** Contact, company (if B2B), source channel, intent (services vs product), consent scope.
2. **Score or tag:** Apply team qualification rubric (document in CRM fields).
3. **Handoff:** Assign **BD owner** per org routing table; notify in agreed channel (email/ERP task).
4. **SLA:** Handoff within **one business day** of “qualified” status unless exception logged.

## Roles

- **Growth Manager:** Qualification owner.
- **BD / Account owner:** Accepts lead in CRM.

## Execution runbook

### Per lead (same business day as “qualified”)

- [ ] Verify minimum data set per §Procedure step 1 (no handoff without company name for B2B unless sole prop).
- [ ] Set CRM status to **Qualified** and **BD owner** from routing table.
- [ ] Notify BD in agreed channel (email or task ID); include CRM deep link.
- [ ] BD acknowledges acceptance in CRM or declines with reason code.

### RACI

| Activity | Accountable | Consulted | Informed |
|----------|-------------|-----------|----------|
| Qualification rubric | Growth Manager | CMO | PMO |
| BD assignment | BD lead | Ops | Growth |
| Routing table updates | PMO | CMO | Leadership |

### Escalation

- Lead unowned after **1 business day:** escalate to PMO with CRM ID and last activity timestamp.
