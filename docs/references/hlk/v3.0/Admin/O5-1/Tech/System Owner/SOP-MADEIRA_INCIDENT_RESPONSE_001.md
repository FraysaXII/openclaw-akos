---
language: en
status: active
artifact_role: canonical
authority: System Owner
last_review: 2026-05-03
---

STANDARD OPERATING PROCEDURE

* Item Name: MADEIRA incident response  
* Item Number: SOP-MADEIRA_INCIDENT_RESPONSE_001  
* Related process registry ID: `env_tech_dtp_madeira_incident` (parent workstream `env_tech_ws_madeira_quality` under MADEIRA Platform `env_tech_prj_3`)  
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

Provide a **repeatable triage path** when MADEIRA shows regression signals (log-watcher alerts, operator-reported unsafe outputs, golden routing failures, or finance or HLK tool misroutes) so impact is contained, scenarios are quarantined when needed, and evidence is captured for the next verdict cycle.

---

## 2. Scope and process linkage

| `item_id` | `item_name` | Granularity |
|:----------|:------------|:-----------|
| `env_tech_dtp_madeira_incident` | MADEIRA incident response (event-driven) | process |

**In scope:** Triage, containment, prompt or registry adjustments, re-run of targeted eval slices, documentation in initiative reports.

**Out of scope:** Cross-tenant customer recovery (track separately under customer security runbooks); arbitrary gateway capability expansion without Orchestrator and HITL flows.

---

## 3. Roles and responsibilities

| Role | Accountability |
|:-----|:---------------|
| **System Owner** | Final decision on quarantine vs hotfix, approves release-unblock after recovery |
| **AI Engineer** | Executes scenario quarantine tool, authors registry note text, ships prompt diffs under review |
| **DevOps** | Restores CI green for targeted profiles, captures artefacts for dossier snapshot |

---

## 4. Cadence and triggers

**Event-driven:** any **SEV-1** style alert (unsafe tool execution claims, repeated fabrication on golden prompts, finance path returning unsourced numbers) or **two consecutive** weekly runs failing conversational light on the same persona slice.

---

## 5. Procedure

1. **Detect:** acknowledge alert source (`scripts/log-watcher.py` output, operator report, CI failure on `madeira`-tagged tests).
2. **Classify:** map to UC-ID from `docs/wip/planning/17-madeira-cursor-mode-parity/coverage-matrix.md` when applicable; record repro without pasting secrets.
3. **Contain:** if scenario isolated, run `scripts/quarantine_scenario.py` (Initiative 49) to set `lifecycle_status=quarantined` with explicit **notes** rationale; otherwise roll back last prompt or routing change via git revert under normal review.
4. **Harden:** patch prompt overlay, registry row, or eval expectation; add or refresh cassette only when operator policy allows live capture.
5. **Verify:** `py scripts/eval.py` targeted slice for affected persona; `py scripts/browser-smoke.py` HTTP Scenario-0 when routing touched; optional Playwright with `AKOS_REQUIRE_DOCKER_PREFLIGHT=1` when sandbox strictness is in scope.
6. **Close:** append dated entry to `docs/wip/planning/49-madeira-management-rollup/reports/` with PASS / FOLLOW-UP and link to commits.

---

## 6. Verification and dossier contract

| Source | Dossier section | Signal |
|:-------|:----------------|:-------|
| Log-watcher JSONL under `~/.openclaw/telemetry/` | Section 5 adversarial or quality envelope when ingested | Confirms incident class |
| Targeted `eval.py` markdown scorecard | Section 5–6 | Proves recovery on conversational axis |
| `browser-smoke.py` JSON results | Section 8 operational health | Proves operator HTTP lane |
| Quarantine table (registry excerpt) | Section 4 calibration / scenario health when extended | Shows containment |

**Bidirectional contract:** this SOP’s verification rows **must** appear in the next MADEIRA-flavored dossier (`--filter madeira`) after a SEV-1 class incident; Section 4/5/8 header footers reference `SOP-MADEIRA_INCIDENT_RESPONSE_001` when incidents occurred in the reporting window.

---

## 7. Escalation

If containment fails after two fix attempts, **pause** Tier-3 WebChat demos, notify System Owner, and open a cross-initiative decision in `49-madeira-management-rollup/decision-log.md` before re-enabling.

---

## 8. References

* `SOP-MADEIRA_SCENARIO_LIFECYCLE_001.md` (quarantine and promotion)  
* `SOP-MADEIRA_VERDICT_AND_CADENCE_001.md` (post-incident verdict)  
* `docs/uat/madeira_use_case_matrix.md`  
* `docs/uat/hlk_admin_smoke.md`  

---

## 9. Decision log (within-SOP)

| Date | Decision | Rationale |
|:-----|:---------|:----------|
| 2026-05-03 | Initial publication under Initiative 49 | Codifies triage + dossier evidence loop |
