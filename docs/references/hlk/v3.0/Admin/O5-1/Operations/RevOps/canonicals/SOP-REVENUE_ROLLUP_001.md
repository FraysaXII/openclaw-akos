---
language: en
status: review
canonical: true
role_owner: RevOps Analyst
classification: way_of_working
intellectual_kind: SOP
ssot: true
authored: 2026-05-15
last_review: 2026-05-15
last_review_at: 2026-05-15
last_review_by: CMO
last_review_decision_id: D-IH-72-AK
methodology_version_at_review: v3.0
companion_to:
  - REVOPS_AREA_CHARTER.md
  - REVOPS_PROCESS_CATALOG.yaml
  - SOP-REVOPS_QBR_001.md
---

# SOP-REVENUE_ROLLUP_001 — Per-engagement revenue rollup refresh

> Authored I72 R-B (2026-05-15) per `D-IH-72-AK` (regression-amend SOP backfill). Closes the Rule 1 SOP-pairing gap that the I72 regression review (Q5-A) flagged for the `revenue_rollup` entry in `REVOPS_PROCESS_CATALOG.yaml`. The runbook is `governance.engagement_revenue_view` (Supabase view shipped at I72 P7 per `D-IH-72-M`); this SOP is its operator-facing counterpart.

## 1. Purpose

Refresh the per-engagement revenue rollup view weekly, surface variance-vs-forecast, and trigger ad-hoc QBR-cycle adjustments when variance exceeds the 10% threshold (per `D-IH-72-N` initial cut). Operationalises the value-mapping core function (per `D-IH-72-Y`) at weekly cadence.

## 2. Scope

In scope:

- Querying `governance.engagement_revenue_view` weekly (Mondays 06:00 per `REVOPS_PROCESS_CATALOG.yaml` `revenue_rollup.schedule_cron`).
- Computing per-engagement variance vs the forecast cell stored on each `ENGAGEMENT_REGISTRY.csv` row.
- Surfacing out-of-band engagements to the operator inbox.
- Routing variance >10% to the next QBR cycle (or ad-hoc QBR fire if variance >25%).

Out of scope:

- Stripe-side reconciliation (lives in I19+I20 finops chain via `finops.registered_fact`).
- Forward-pipeline forecast authoring (lives in `SOP-REVOPS_QBR_001.md` §3.2).

## 3. Steps

### 3.1 Weekly view query

RevOps Analyst (or `revops-analyst-aic` per `D-IH-72-S`) runs:

1. Query `governance.engagement_revenue_view` for the trailing 7-day window.
2. Join with `ENGAGEMENT_REGISTRY.csv` on `engagement_id` to pull the forecast cell per active engagement.
3. Compute `variance_pct = (actual - forecast) / forecast` per engagement.

### 3.2 Variance triage

| Variance band | Action |
| --- | --- |
| `\|variance_pct\| ≤ 10%` | No action; record as healthy in the weekly note. |
| `10% < \|variance_pct\| ≤ 25%` | Flag for next QBR cycle agenda; note in operator inbox. |
| `\|variance_pct\| > 25%` | Fire ad-hoc QBR per `SOP-REVOPS_QBR_001.md` §3.4 (out-of-cycle). |

### 3.3 Weekly report authoring

Append a short weekly note at `docs/wip/planning/72-marketing-area-governance-and-persona-registry-expansion/reports/revenue-rollup-YYYY-WW.md` summarising rows queried, healthy/flagged/critical counts, and operator-action follow-ups.

### 3.4 PMO interim handoff

Until the RevOps Manager row flips from `gated_operator` to `active`, the weekly note copies PMO for visibility. Post-flip, RevOps Manager handles the operator-action follow-ups directly.

## 4. Failure modes

- `governance.engagement_revenue_view` query times out → escalate to RevOps Manager (Data-Engineer discipline per D-IH-72-AM); PMO interim until RevOps Manager activates per D-IH-72-AC.
- `ENGAGEMENT_REGISTRY.csv` forecast cell empty → flag the row in the operator inbox; do not compute variance for that engagement.
- Multiple weeks missed → next run authors a backfill note covering the gap window.

## 5. Acceptance criteria

Per [`akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 5:

- **AC-HUMAN**: RevOps Analyst (or `revops-analyst-aic`) runs §3 steps manually using only this SOP body and produces the weekly note.
- **AC-AUTOMATION**: `governance.engagement_revenue_view` query returns rows; per-engagement variance computed; weekly note authored at the canonical reports path; `validate_revops_spine.py` PASS.

## 6. Cross-references

- Parent: [`REVOPS_AREA_CHARTER.md`](REVOPS_AREA_CHARTER.md).
- Catalog entry: `REVOPS_PROCESS_CATALOG.yaml` `revenue_rollup` (cadence: scheduled, weekly).
- Sister SOPs: [`SOP-REVOPS_QBR_001.md`](SOP-REVOPS_QBR_001.md), [`SOP-FINOPS_BRIDGE_001.md`](SOP-FINOPS_BRIDGE_001.md), [`SOP-ENGAGEMENT_SCAFFOLDING_001.md`](SOP-ENGAGEMENT_SCAFFOLDING_001.md).
- Runbook: `governance.engagement_revenue_view` (Supabase migration `20260514260000_i72_adapter_registries_mirrors.sql` + I72 P7 spine migration).
- Decisions: D-IH-72-AK (this SOP), D-IH-72-M (engagement-revenue spine), D-IH-72-N (process catalog architecture), D-IH-72-Y (value-mapping core function).
