---
Item Name: Weekly GTM and marketing metrics review
Item Number: SOP-GTM_WEEKLY_METRICS_REVIEW_001
Object Class: Guideline and Procedure
Confidence Level: Safe
Security Level: 2 (Internal Use)
Entity Owner: Think Big
Area Owner: Operations
Associated Workstream: Go-To-Market Strategy
Associated process rows: thi_mkt_dtp_210, thi_opera_dtp_289, env_tech_dtp_243
Version: 1.0
Revision Date: 2026-04-17
---

## Purpose

Weekly **metrics forum** for Holistika internal GTM—pipeline contribution, velocity, inbound SLA adherence, and campaign health. **Not** a separate `item_id`; operationalizes cadence across [`Go-To-Market Strategy` `thi_mkt_dtp_210`](../../../../../../../hlk/compliance/process_list.csv), [`End-to-End Marketing Lead Flow` `thi_opera_dtp_289`](../../../../../../../hlk/compliance/process_list.csv), and event taxonomy [`env_tech_dtp_243`](../../../../../../../hlk/compliance/process_list.csv).

## Agenda (30–45 min)

1. Inbound volume and SLA (see **SOP-GTM_INBOUND_SLA_001** / `holistika_gtm_dtp_003`).
2. Qualification and BD handoff conversion (see **SOP-GTM_BD_HANDOFF_001**).
3. Channel experiments and **event taxonomy** alignment [`env_tech_dtp_243`](../../../../../../../hlk/compliance/process_list.csv).
4. Risks and blockers (tools, consent, data quality).

## Roles

- **PMO:** Facilitator; notes to decision log if priorities shift.
- **CMO:** Decision owner for budget and segment focus.

## Outputs

- Action items with owner and date.
- Escalations to **Data Governance** or **Legal** when PII or attribution rules change.

## Execution runbook

### Before the meeting (PMO)

- [ ] Pull last 7 days: inbound count, SLA breaches (from **SOP-GTM_INBOUND_SLA_001**), qualification→BD conversion.
- [ ] Pull campaign / channel table from Growth; flag anomalies vs prior week.
- [ ] Confirm **event taxonomy** checklist against [`env_tech_dtp_243`](../../../../../../../hlk/compliance/process_list.csv) owner (Tech) if new tags shipped.

### During (30–45 min)

- [ ] Timebox each agenda section; park deep dives to async.
- [ ] Log **action items** with owner + due date in shared tracker.
- [ ] One **decision** line in [`decision-log.md`](../../../../../../../wip/planning/14-holistika-internal-gtm-mops/decision-log.md) if priorities or budget shift.

### After

- [ ] Distribute notes within **24 hours**.
- [ ] Open escalation ticket if tool or consent blocker exceeds 1 week.

### RACI

| Role | Responsibility |
|------|----------------|
| PMO | Facilitate; notes; follow-up hygiene |
| CMO | Decisions on budget and segment |
| Growth | Data pulls for inbound and campaigns |
| Tech (as needed) | Event taxonomy / pipeline integrity |
