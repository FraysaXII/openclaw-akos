---
language: en
status: active
artifact_role: canonical
authority: System Owner
last_review: 2026-05-03
---

STANDARD OPERATING PROCEDURE

* Item Name: MADEIRA verdict and cadence governance  
* Item Number: SOP-MADEIRA_VERDICT_AND_CADENCE_001  
* Related process registry IDs: `env_tech_dtp_madeira_verdict`, `env_tech_dtp_madeira_dossier` (parent workstream `env_tech_ws_madeira_quality` under MADEIRA Platform `env_tech_prj_3`)  
* Object Class: Guideline & Procedure  
* Confidence Level: High  
* Security Level: 2 (Internal Use)  
* Entity Owner: HLK Tech Lab  
* Area Owner: Tech  
* Associated Workstream: MADEIRA quality and verdict management (`env_tech_ws_madeira_quality`)  
* Version: 1.0  
* Revision Date: 2026-05-03  

---

## Table of Contents

1. Purpose  
2. Scope and process linkage  
3. Roles and responsibilities  
4. Cadence and triggers  
5. Procedure  
6. Verification and dossier contract  
7. Escalation  
8. References  
9. Decision log (within-SOP)  

---

## 1. Purpose

Define how Holistika **reviews MADEIRA readiness** using the **three-light** model (conversational, operator, surface) and how **operator dossier emits** capture evidence on a repeatable calendar. Makes the MADEIRA verdict **auditable**: the same gates run locally, in CI, and during weekly or monthly cadences.

---

## 2. Scope and process linkage

| `item_id` | `item_name` | Granularity |
|:----------|:------------|:-----------|
| `env_tech_dtp_madeira_verdict` | MADEIRA verdict review (weekly) | process |
| `env_tech_dtp_madeira_dossier` | MADEIRA dossier emit (cadence-bound) | process |

**In scope:** Operator verdict review against three lights; scheduling dossier emits; archiving manifests; interpreting trend lines without changing dossier section order.

**Out of scope:** Rewriting MADEIRA prompts (separate governed change workflow); rebuilding the eval harness; OpenClaw gateway feature work.

---

## 3. Roles and responsibilities

| Role | Accountability |
|:-----|:---------------|
| **System Owner** | Owns three-light thresholds, monthly Tier-3 UAT verdict sign-off, and exceptions |
| **DevOps** | Runs cadence-bound dossier emissions, verifies artifacts land under `artifacts/uat-dossier/`, optional mirror writer health |
| **AI Engineer** | Supports interpretation of conversational-light regressions with persona or scenario deltas |

---

## 4. Cadence and triggers

| Cadence | Action | Threshold (summary) |
|:--------|:-------|:---------------------|
| Pre-commit / CI | Tier-1 persona rubric slice, Scenario-0 HTTP checks where applicable | All automated gates configured in repository profiles PASS |
| Weekly | MADEIRA dossier emit (focused or full at operator choice) | Per-persona cost and judge thresholds per policy registers; conversational calibration within ±5 percentage points vs D-IH-47-C target |
| Monthly | MADEIRA verdict review | Top-ranked Tier-3 use-case IDs exercised; three-light verdict documented in initiative report |

**Triggers outside cadence:** production incident invoking `SOP-MADEIRA_INCIDENT_RESPONSE_001`; major prompt or registry merge touching MADEIRA intents or persona scenario library.

---

## 5. Procedure

1. Confirm **foundation tools** run cleanly: `py scripts/validate_hlk.py`; `scripts/validate_persona_scenario_registry.py` subset when registry scope changed.
2. For **weekly dossier**, run `py scripts/render_uat_dossier.py` in `snapshot` or `live` mode per Initiative 48 operator guide; when MADEIRA specialization is enabled, use `--filter madeira` per operator workflow doc.
3. Collect **artifacts**: `dossier.md`, `manifest.json`; optional PDF/HTML when format policy requires archive copies.
4. Evaluate **three lights** using thresholds in `docs/wip/planning/02-hlk-on-akos-madeira/MADEIRA_HARDENING_CONSOLIDATED_PLAN.md` Part H and initiative 49 rollup planning folder.
5. Record outcome in dated initiative report (`docs/wip/planning/49-madeira-management-rollup/reports/`) as PASS, NO-GO, or FOLLOW-UPS with rationale (no undocumented silent drift).
6. If **surface light** amber, route to UX review cadence (`SOP-MADEIRA_UX_REVIEW_001`).

---

## 6. Verification and dossier contract

**Bidirectional mapping:** dossier fragments **consume** verification outputs from scripts below; dossier Sections **supply** verdict evidence cited back by this SOP.

| Artifact / script | Dossier section | Signal |
|:------------------|:----------------|:-------|
| `py scripts/eval.py` scorecards (+ calibration via `scripts/calibrate_scenarios.py` when personas drifted) | Section 5–7 envelopes (stress, drift, personas) per live run | Conversational-light |
| `py scripts/browser-smoke.py` (+ optional Playwright) + dated Tier-3 UAT notes | Operational health envelopes | Operator-light |
| Impeccable critique artefacts + axe-style logs + brand voice lint (when surfaced in dossier) | Section 8 operational health subsection when MADEIRA flavor | Surface-light |
| Trend rollups / `artifacts/uat-dossier/index.json` | Section 11 trend lines when history exists | Tracks weekly cadence fidelity |

Registry rows `env_tech_dtp_madeira_verdict` and `env_tech_dtp_madeira_dossier` are satisfied when the above artefacts exist for the window under review.

---

## 7. Escalation

Repeated **NO-GO** on conversational light escalates to System Owner plus AI Engineer pairing for scenario quarantine versus prompt fix per `SOP-MADEIRA_SCENARIO_LIFECYCLE_001`. Operator-light failures involving Docker sandbox reachability escalate through `scripts/doctor.py --docker-sandbox` playbook in `docs/USER_GUIDE.md` section **14.3b**.

---

## 8. References

* `docs/wip/planning/49-madeira-management-rollup/madeira-program-index.md`
* `docs/wip/planning/49-madeira-management-rollup/decision-log.md`
* `docs/guides/madeira_operator_quickstart.md` (nine-hundred card)
* `docs/guides/madeira_dossier_workflow.md`
* Initiative 48 dossier specs under `docs/wip/planning/48-operator-dossier/`

---

## 9. Decision log (within-SOP)

| Date | Decision | Rationale |
|:-----|:---------|:----------|
| 2026-05-03 | Initial publication under Initiative 49 | Operationalises three-light doctrine and dossier emits |
