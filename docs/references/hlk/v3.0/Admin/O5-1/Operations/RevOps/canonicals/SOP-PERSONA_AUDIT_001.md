---
language: en
status: review
canonical: true
role_owner: CMO
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
---

# SOP-PERSONA_AUDIT_001 — Persona registry audit cycle

> Authored I72 R-B (2026-05-15) per `D-IH-72-AK` (regression-amend SOP backfill). Closes the Rule 1 SOP-pairing gap that the I72 regression review (Q5-A) flagged for the `persona_audit` entry in `REVOPS_PROCESS_CATALOG.yaml`. Operates on `PERSONA_REGISTRY.csv` (Marketing-area canonical) and `PERSONA_SCENARIO_REGISTRY.csv` (Marketing-area canonical) as data sources; the SOP lives at `Operations/RevOps/canonicals/` because the audit cadence is RevOps-orchestrated even though the data is Marketing-owned.

## 1. Purpose

Provide an on-demand audit cycle that:

1. Surfaces stale `PERSONA_REGISTRY.csv` rows (no `last_review_at` update in >180 days, OR no inbound engagement matched against the persona in >180 days).
2. Identifies missing cross-links between persona rows and live engagements (`ENGAGEMENT_REGISTRY.csv`), scenarios (`PERSONA_SCENARIO_REGISTRY.csv`), or counterparty rows (`FINOPS_COUNTERPARTY_REGISTER.csv`).
3. Proposes new persona rows from observed inbound patterns that don't fit any existing persona.
4. Flags persona rows whose handoff_role no longer exists in `baseline_organisation.csv` (lifecycle drift).

## 2. Scope

In scope:

- `PERSONA_REGISTRY.csv` (all rows) and `PERSONA_SCENARIO_REGISTRY.csv` (all rows).
- Cross-links to `ENGAGEMENT_REGISTRY.csv`, `FINOPS_COUNTERPARTY_REGISTER.csv`, and `INTELLIGENCEOPS_REGISTER.csv`.
- New-persona-row proposals (not the row authoring itself — that follows the canonical-CSV operator-gate per `SOP-META_PROCESS_MGMT_001.md`).

Out of scope:

- Brand-voice prose audit on persona descriptions (lives in `validate_brand_voice_register.py` strict-mode runs).
- Scenario authoring (lives in the Marketing sub-area charters per `D-IH-72-G`).

## 3. Steps

### 3.1 Trigger

Cadence: `on_demand` per `REVOPS_PROCESS_CATALOG.yaml` `persona_audit`. Typical triggers:

- Operator notices an inbound pattern that doesn't fit any persona (manual fire).
- New initiative kicks off and needs a persona-coverage audit (e.g., I73 People Operations expansion).
- Quarterly cadence (recommended every Q1 alongside the year-opening QBR cycle).

### 3.2 Validator pass

CMO (or `revops-analyst-aic`) runs `py scripts/validate_persona_registry.py` and `py scripts/validate_persona_scenario_registry.py`. Capture both outputs.

### 3.3 Staleness sweep

For each persona row:

1. Inspect `last_review_at`. If >180 days, mark as `STALE-REVIEW`.
2. Inspect `ENGAGEMENT_REGISTRY.csv` for engagements with `primary_persona_id` matching this persona row's `persona_id`. If 0 in trailing 180 days, mark as `STALE-INBOUND`.
3. Roll up counts per persona; rank by staleness severity.

### 3.4 Cross-link audit

For each persona row:

1. Verify `handoff_role` exists in `baseline_organisation.csv` `role_name` column. If not, mark as `BROKEN-HANDOFF`.
2. Verify each scenario in `PERSONA_SCENARIO_REGISTRY.csv` referencing this persona has at least 1 cited engagement OR explicit `scenario_status: aspirational`. If neither, mark as `ORPHAN-SCENARIO`.

### 3.5 New-persona-row proposals

If §3.3 surfaces inbound patterns not covered by existing personas:

1. Draft a proposed row (persona_id, persona_name, primary_intent, channels, etc.) following the `PERSONA_REGISTRY.csv` schema.
2. Author proposal at `docs/wip/planning/72-marketing-area-governance-and-persona-registry-expansion/reports/persona-audit-YYYY-MM-DD.md` (or successor I7X reports folder when the audit fires under a different initiative).
3. Surface inline-ratify gate via `AskQuestion` per `akos-inline-ratification.mdc` for operator approval before commit.

### 3.6 Audit report authoring

Author audit report at `docs/wip/planning/<active-initiative>/reports/persona-audit-YYYY-MM-DD.md` summarising:

- Rows audited (count); stale-review count; stale-inbound count; broken-handoff count; orphan-scenario count.
- Proposed new persona rows (with rationale).
- Proposed deprecations (existing rows to retire).
- Cross-link fixes needed (handoff_role updates; scenario status flips).

## 4. Failure modes

- `validate_persona_registry.py` fails → fix CSV integrity errors first; re-run audit after.
- `baseline_organisation.csv` role lookup fails → escalate to People Operations Manager (or PMO interim if People Ops Lead row is gated).
- Operator-gate timeout on new-persona-row proposal → defer to next audit cycle; note in OPS_REGISTER if the gap blocks downstream work.

## 5. Acceptance criteria

Per [`akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 5:

- **AC-HUMAN**: CMO (or `revops-analyst-aic`) runs §3 steps manually using only this SOP body and produces the audit report.
- **AC-AUTOMATION**: `validate_persona_registry.py` PASS + `validate_persona_scenario_registry.py` PASS + audit report authored at the canonical reports path.

## 6. Cross-references

- Parent: [`REVOPS_AREA_CHARTER.md`](REVOPS_AREA_CHARTER.md).
- Catalog entry: `REVOPS_PROCESS_CATALOG.yaml` `persona_audit` (cadence: on_demand).
- Data sources: `PERSONA_REGISTRY.csv` (Marketing-area), `PERSONA_SCENARIO_REGISTRY.csv` (Marketing-area), `ENGAGEMENT_REGISTRY.csv`, `FINOPS_COUNTERPARTY_REGISTER.csv`, `INTELLIGENCEOPS_REGISTER.csv`.
- Sister SOPs: [`SOP-REVOPS_QBR_001.md`](SOP-REVOPS_QBR_001.md), [`SOP-REVENUE_ROLLUP_001.md`](SOP-REVENUE_ROLLUP_001.md).
- Runbooks: `scripts/validate_persona_registry.py`, `scripts/validate_persona_scenario_registry.py`.
- Decisions: D-IH-72-AK (this SOP), D-IH-72-G (persona-vs-scenario both registry rows pattern), D-IH-72-N (process catalog architecture).
