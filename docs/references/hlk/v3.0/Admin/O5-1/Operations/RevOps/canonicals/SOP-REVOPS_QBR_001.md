---
language: en
status: review
canonical: true
role_owner: PMO + RevOps Lead (forward; activates at P4 per D-IH-72-AC)
classification: way_of_working
intellectual_kind: SOP
ssot: true
authored: 2026-05-14
last_review: 2026-05-14
last_review_at: 2026-05-14
last_review_by: CMO
last_review_decision_id: D-IH-72-A
methodology_version_at_review: v3.0
companion_to:
  - REVOPS_AREA_CHARTER.md
  - dimensions/ENGAGEMENT_TEMPLATE_REGISTRY.csv
  - SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md
  - ../../../Marketing/Resonance/Account Management/canonicals/ACCOUNT_MANAGEMENT_CHARTER.md
---

# SOP-REVOPS_QBR_001 — RevOps Quarterly Business Review cadence

> Authored I72 P4 per `D-IH-72-A` (P0 charter) + `D-IH-72-AC` (RevOps activation gating) + `D-IH-72-AH` (Round 8 Operations/RevOps area charter at P1). Codifies the **quarterly cadence** through which RevOps connects Marketing demand-side activity (Reach captures + Resonance retention) to Finance revenue + Sales pipeline through the engagement-template + engagement-revenue spine. Paired with `SOP-ACCOUNT_QBR_001.md` (P8 deliverable; per-account QBR owned by Marketing/Resonance/Account Management). This SOP is the **operator-facing canonical**; paired runbook (per [`akos-executable-process-catalog.mdc`](../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1) is `scripts/validate_engagement_template_registry.py` + `scripts/validate_engagement_template_promotion.py` (gate validators run as part of the QBR portfolio-review step).

## 1. Purpose

Establish a deterministic quarterly review cadence that:

1. **Reconciles per-engagement revenue attribution** against the engagement-template + engagement-revenue spine (P7 deliverable; pre-spine: per-engagement manual reconciliation).
2. **Surfaces engagement-template promotion candidates** (templates that have crossed the 3-engagement instance threshold per `D-IH-72-B` and are eligible for `scaffold → active` promotion via `SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md`).
3. **Calibrates forward-pipeline confidence** across Marketing/Reach captures + Marketing/Resonance retention forecasts.
4. **Identifies cross-area portfolio risks** (concentration risk, billing-cadence collisions, contract-kind mismatches).
5. **Triggers strategic adjustments** to the discipline-mix axis cells in `process_list.csv` (Round 8 D-IH-72-AF schema) when revenue-attribution patterns reveal gaps.

## 2. Scope

In scope:
- All engagements in `ENGAGEMENT_REGISTRY.csv` with `status=active` during the review quarter.
- All templates in `ENGAGEMENT_TEMPLATE_REGISTRY.csv`.
- Cross-area metrics: per-engagement revenue (Finance), per-engagement Marketing reach + retention (Marketing), per-engagement delivery cost (Operations), per-engagement risk surface (Account Management).
- The 4-axis value-mapping schema cells on `process_list.csv` (D-IH-72-AF + D-IH-72-AG): `m3_sub_area`, `engagement_template_id`, `persona_id`, `cadence_type`.

Out of scope:
- Per-account relationship-health review (owned by `SOP-ACCOUNT_QBR_001.md` at Marketing/Resonance/Account Management/canonicals/; P8 deliverable).
- Per-customer service catalog + SLA review (owned by `SOP-SERVICE_MGMT_001.md` at Operations/SMO/canonicals/).
- Headcount / org-structure review (owned by People/CPO).

## 3. Inputs

- `ENGAGEMENT_REGISTRY.csv` rows for the quarter.
- `ENGAGEMENT_TEMPLATE_REGISTRY.csv` rows (all statuses).
- `governance.engagement_revenue_view` (P7 deliverable) — Supabase view joining engagement_id + template_id to `finops.registered_fact`. Pre-P7: manual per-engagement reconciliation against `FINOPS_COUNTERPARTY_REGISTER.csv`.
- `process_list.csv` rows where `m3_sub_area` or `engagement_template_id` cells are populated (sparse population; expanding over time).
- Last QBR's report under `docs/wip/planning/72-marketing-area-governance-and-persona-registry-expansion/reports/qbr-YYYY-Qn.md` (this SOP creates the first one).

## 4. Steps

### 4.1 Pre-QBR data assembly (T-7 days)

The role_owner (PMO interim until P4 activation; RevOps Analyst post-activation) assembles:

1. **Engagement-revenue reconciliation table**: per active engagement, the registered revenue (`finops.registered_fact`) joined to its `engagement_id` + `template_id`. Variance per engagement.
2. **Template-portfolio table**: per template, the count of active engagements consuming it + the running average revenue per engagement + the gap between template's `par_rev_value_eur` and observed mean.
3. **Promotion-candidate list**: templates with `lifecycle_status=scaffold` that have crossed the 3-engagement instance threshold per `D-IH-72-B`.
4. **Risk-surface scan**: cross-engagement concentration risk + billing-cadence collisions + per-counterparty exposure.

### 4.2 QBR session (T-0; ~2-4 hours)

Attendees: PMO + RevOps Lead (post-activation) + RevOps Analyst (post-activation) + CMO + COO (when activated). Agenda:

1. **Reconciliation review** (~30 min): per-engagement revenue vs forecast; variance triage.
2. **Template-portfolio review** (~30 min): per-template performance + promotion-candidate decisions.
3. **Forward-pipeline calibration** (~45 min): Marketing/Reach capture + Resonance retention forecasts; updated forward-pipeline confidence per engagement segment.
4. **Cross-area risk discussion** (~30 min): concentration + collision + contract-kind risks; mitigation owner assignments.
5. **Schema cell updates** (~30 min): adjust `min_rev_value_eur` / `par_rev_value_eur` / `max_rev_value_eur` cells on relevant `process_list.csv` rows when patterns warrant.

### 4.3 Post-QBR canonical updates (T+7 days)

1. **Promotion ratifications**: surface new `D-IH-72-*` decision rows for each ratified template promotion; trigger `SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md` workflow per promoted template.
2. **process_list.csv axis cell updates** (canonical-CSV gate): operator approval before commit.
3. **QBR report**: author `docs/wip/planning/72-marketing-area-governance-and-persona-registry-expansion/reports/qbr-YYYY-Qn.md` with all reconciliation tables + decisions ratified + risks logged + schema updates applied.

### 4.4 Validator gate

```
py scripts/validate_engagement_template_registry.py
py scripts/validate_engagement_template_promotion.py
py scripts/validate_hlk.py
```

All MUST be `PASS / OVERALL: PASS` before commit closes the QBR cycle.

## 5. Outputs

- QBR report at `docs/wip/planning/72-marketing-area-governance-and-persona-registry-expansion/reports/qbr-YYYY-Qn.md`.
- 0+ new template promotion decision rows in `DECISION_REGISTER.csv`.
- 0+ template `lifecycle_status` transitions in `ENGAGEMENT_TEMPLATE_REGISTRY.csv`.
- 0+ axis cell updates on `process_list.csv`.
- Validator runs all PASS.

## 6. Acceptance criteria

Per [`akos-executable-process-catalog.mdc`](../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 5:

- **`acceptance_criteria_human`**: a human or AIC role_owner (PMO interim, RevOps Lead post-activation) can run the full §4 cycle manually using only the SOP body. Validator gates surface drift; humans/AICs make the decisions.
- **`acceptance_criteria_automation`**: the paired runbook validators fire unattended in CI; release-gate flips to FAIL on any promotion-gate violation surfaced by the QBR cycle's CSV updates.

## 7. Failure modes

- **No engagement-revenue spine yet (pre-P7)**: manual per-engagement reconciliation against `FINOPS_COUNTERPARTY_REGISTER.csv`; QBR proceeds with manual data; report flags pre-spine reconciliation.
- **RevOps Lead + RevOps Analyst not yet activated (pre-P4 activation post-I71 P5)**: PMO interim runs the QBR with reduced rigor; activation triggers re-baseline.
- **Template-portfolio table reveals collision** (e.g., 2 templates serving same engagement_class with conflicting billing_cadence): block promotion candidates; surface at next QBR with merged-template proposal.
- **Operator unavailable for QBR**: cycle-skipped report drafted; risks flagged for asynchronous review; next QBR catches up backlog.

## 8. Cross-references

- Parent area charter: [`REVOPS_AREA_CHARTER.md`](REVOPS_AREA_CHARTER.md) §5 (process catalog) + §6 (lifecycle).
- Sister SOP: [`SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md`](SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md) (per-template promotion gate; QBR triggers promotion candidates).
- Cross-area sister SOP: `SOP-ACCOUNT_QBR_001.md` (P8 deliverable at Marketing/Resonance/Account Management/canonicals/; per-account QBR — paired with this SOP for revenue-impact mapping).
- Cross-area sister SOP: `SOP-SERVICE_MGMT_001.md` (Operations/SMO/canonicals/; per-customer service catalog + SLA review — RevOps QBR feeds revenue context to SMO service review).
- Canonicals: `ENGAGEMENT_REGISTRY.csv`, [`dimensions/ENGAGEMENT_TEMPLATE_REGISTRY.csv`](dimensions/ENGAGEMENT_TEMPLATE_REGISTRY.csv), `FINOPS_COUNTERPARTY_REGISTER.csv`, `process_list.csv` (Round 8 D-IH-72-AF schema).
- Forward-link: P7 RevOps Spine deliverable (`governance.engagement_revenue_view`).
- Cursor rule: [`akos-executable-process-catalog.mdc`](../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rules 1 + 3 + 4 + 5.
- Process row: `tbi_ops_dtp_revops_qbr_001` in `process_list.csv` (cadence: `scheduled`; quarterly).
- Decisions: `D-IH-72-A` (P0 charter), `D-IH-72-AC` (RevOps activation gating), `D-IH-72-AD` (CRO/COO forward-charter + reporting chain), `D-IH-72-AF` (process_list 7-col schema), `D-IH-72-AG` (multi-axis ontology), `D-IH-72-AH` (Round 8 Operations/RevOps area charter at P1), `D-IH-72-B` (3-engagement template promotion threshold).
