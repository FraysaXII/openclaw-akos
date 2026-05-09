---
sop_id: SOP-LEGAL_TRADEMARK_MONITORING_001
title: Trademark Monitoring
version: 1.0
status: active
classification: canonical
access_level: 4
register: internal
language: en
process_id: hol_lgl_prc_trademark_monitoring_001
role_owner: Legal Counsel
role_parent_1: CPO
area: Legal
entity: Holistika
governance:
  - D-IH-66-C (per-jurisdiction filing matrix)
linked_initiative: I66
created: 2026-05-08
last_review: 2026-05-08
sister_sops:
  - SOP-LEGAL_IP_REGISTER_MAINTENANCE_001
---

# SOP-LEGAL_TRADEMARK_MONITORING_001 — Trademark Monitoring

> Legal-Counsel-owned **quarterly process** that monitors EUIPO + OEPM filing status for all Holistika marks (umbrella + 3 sub-marks + 5 product marks per `BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md`).

## 1. Purpose

Maintain awareness of:

- Filing-status progression (filed → opposition window → registered).
- Opposition events from third parties (deadline-driven response required).
- Renewal-due dates (EU 10-year terms; reminders at 12 / 6 / 3 / 1 months out).
- Conflicting third-party filings on similar marks (collision risks for next-tranche filings).
- Geographic-coverage gaps (countries where Holistika operates but marks aren't registered).

## 2. Cadence

**Quarterly** (4 cycles per year). Out-of-cycle on:

- Opposition notice received (≤ 24h response window).
- Mark-level event (registration grant, refusal, allowance, renewal).
- Pre-tranche-filing collision check (before any new filing under §3 of BRAND_HIERARCHY).

## 3. Inputs

- `BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md` — frozen filing strings + per-jurisdiction filing matrix.
- EUIPO online-search portal: `https://euipo.europa.eu/eSearch/`.
- OEPM online-search portal (Spain): `https://sitadex.oepm.es/sitadex/`.
- WIPO Madrid Monitor (for Madrid Protocol filings, if any): `https://www3.wipo.int/madrid/monitor/`.
- Last quarter's monitoring report.
- Holistika's own IP register (governed by SOP-LEGAL_IP_REGISTER_MAINTENANCE_001 — P3-followup deliverable).

## 4. Process steps

### Step 1 — Status check on each Holistika mark (60 min)

For each of the 8 marks (1 umbrella `Holistika` + 3 sub-marks + 5 product marks), check EUIPO + OEPM (and WIPO if applicable):

| Mark | EUIPO status | OEPM status | Last status change | Next deadline | Action needed |
|:---|:---|:---|:---|:---|:---|

Record any change since last quarter.

### Step 2 — Opposition / objection scan (30 min)

Search EUIPO + OEPM for filings on similar marks (distance metric: edit-distance ≤ 2 from any of our marks; phonetic similarity to umbrella or sub-mark names).

For each potentially-conflicting third-party filing:

- Document the filing details.
- Assess collision risk (low / medium / high).
- Recommend action (no action / monitor / file opposition / negotiate coexistence).

### Step 3 — Renewal calendar review (15 min)

For each registered mark, calculate days-to-renewal-deadline. Flag:

- Marks within 12 months: add to next quarterly review with action plan.
- Marks within 6 months: add to monthly check-in cadence.
- Marks within 3 months: dispatch to operator immediately for renewal action.

### Step 4 — Geographic-coverage gap review (15 min)

Per `BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md` §"per-jurisdiction filing matrix", check whether Holistika has expanded to new geographies in the last quarter that warrant new filings (e.g., LATAM expansion, US presence). Recommend new filings if so.

### Step 5 — File quarterly monitoring report (15 min)

Under `docs/wip/planning/<active-initiative-slug>/reports/` (or dedicated legal-ops directory):

```
trademark-monitoring-<YYYY-Q[1-4]>.md
```

Containing: status table, opposition findings, renewal calendar, coverage gaps, recommended actions.

### Step 6 — Operator review and dispatch (variable)

Review with operator. Time-critical actions (oppositions, renewals < 3 months) get immediate dispatch; non-critical actions enter the annual filing-tranche planning.

## 5. Outputs

- Quarterly monitoring report (Step 5 file).
- Per-mark status updates in the IP register (sister SOP).
- Action items dispatched to operator and legal advisor.

## 6. Cross-references

- [`BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md`](BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md)
- Sister SOP: `SOP-LEGAL_IP_REGISTER_MAINTENANCE_001.md` (P3-followup deliverable)
- D-IH-66-C (per-jurisdiction filing matrix)
- I66 P4 (trademark filing strategy + filing prep packets) — this SOP operates after P4 closes.
