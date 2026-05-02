---
language: en
status: active
artifact_role: canonical
authority: System Owner
last_review: 2026-05-03
---

STANDARD OPERATING PROCEDURE

* Item Name: MADEIRA scenario lifecycle and telemetry feedback  
* Item Number: SOP-MADEIRA_SCENARIO_LIFECYCLE_001  
* Related process registry IDs: `env_tech_dtp_madeira_lifecycle`, `env_tech_dtp_madeira_telemetry` (parent workstream `env_tech_ws_madeira_quality` under MADEIRA Platform `env_tech_prj_3`)  
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

Govern how **persona scenarios** in `PERSONA_SCENARIO_REGISTRY.csv` move through **scaffold → active → quarantined → deprecated**, how **priority fields** are refreshed, and how **telemetry** produces **JSON proposals** for new scenarios without auto-merging registry rows.

---

## 2. Scope and process linkage

| `item_id` | `item_name` | Granularity |
|:----------|:------------|:-----------|
| `env_tech_dtp_madeira_lifecycle` | MADEIRA scenario lifecycle (promote quarantine deprecate) | process |
| `env_tech_dtp_madeira_telemetry` | MADEIRA telemetry registry feedback loop | process |

**Lifecycle states:** `scaffold`, `active`, `quarantined`, `deprecated` (Initiative 49 extends prior three-state model with `quarantined` per decision D-IH-49-C).

---

## 3. Roles and responsibilities

| Role | Accountability |
|:-----|:---------------|
| **AI Engineer** | Maintains scenario rows, runs promotion and quarantine tooling, triages telemetry JSON proposals |
| **System Owner** | Approves net-new canonical rows or schema-affecting field changes per governance rulebook |
| **DevOps** | Ensures mirror emit jobs pick up approved CSV after operator SQL apply when Supabase path is used |

---

## 4. Cadence and triggers

| Cadence | Action |
|:--------|:-------|
| Per merge touching `PERSONA_SCENARIO_REGISTRY.csv` | `py scripts/validate_persona_scenario_registry.py` + targeted `eval.py` slice |
| Weekly | Review Langfuse or local telemetry JSONL for novel failure clusters |
| Monthly | Recompute `priority_score` via `scripts/recalculate_persona_scenario_priorities.py` or `calibrate_scenarios.py --write-priority-scores` after difficulty adjustments |

---

## 5. Procedure

### 5.1 Promotion (scaffold → active)

1. Fill all required CSV columns (persona, skill, scenario class, difficulty, route, outcome, topics).  
2. Ensure validator PASS and at least one passing eval path (Tier-1 or replay) documents the scenario.  
3. Set `lifecycle_status=active` with operator note in `notes`.  

### 5.2 Quarantine (active → quarantined)

1. After **three** consecutive failing runs without a merged fix, run `scripts/quarantine_scenario.py --scenario-id SCN-... --reason "<text>"`.  
2. Quarantined scenarios **do not** count toward monthly GO verdict numerators but remain visible in dossier sub-tables when implemented.  

### 5.3 Deprecation

1. Mark `lifecycle_status=deprecated` when superseded; keep id stable for historical dossier references.  

### 5.4 Telemetry promotion (proposal only)

1. Run `scripts/promote_telemetry_to_scenario.py` to emit **JSON proposals** under `artifacts/` (path chosen by script help).  
2. Operator reviews and manually applies rows to CSV; **no** auto-merge to git SSOT.  

---

## 6. Verification and dossier contract

| Source | Dossier section | Signal |
|:-------|:----------------|:-------|
| Validator output for registry | Section 4 scenario health | Confirms schema + enum integrity |
| `eval.py` persona matrix slice | Section 5–6 | Shows active vs quarantined mix when renderer adds sub-table |
| Telemetry proposal JSON | Appendix or Section 4 note when linked | Documents feedback loop without claiming merged rows |
| `priority_score` rewrite log | Section 4 trend text when operator includes | Shows backlog ordering integrity |

**Bidirectional contract:** Section 4 headers reference this SOP when scenario inventory changes land in the reporting window; this SOP cites Section 4 and Section 5 for proof of lifecycle execution.

---

## 7. Escalation

Schema expansions (new columns, new lifecycle enum value) require **explicit** decision log entry (`49-madeira-management-rollup/decision-log.md`) before merge, per `akos-governance-remediation.mdc` canonical CSV gate.

---

## 8. References

* `docs/references/hlk/compliance/dimensions/PERSONA_SCENARIO_REGISTRY.csv`  
* `scripts/migrate_persona_registry_i49_columns.py`  
* `scripts/recalculate_persona_scenario_priorities.py`  
* `SOP-MADEIRA_INCIDENT_RESPONSE_001.md`  
* `SOP-MADEIRA_VERDICT_AND_CADENCE_001.md`  

---

## 9. Decision log (within-SOP)

| Date | Decision | Rationale |
|:-----|:---------|:----------|
| 2026-05-03 | Initial publication; `quarantined` state adopted | Initiative 49 D-IH-49-C |
