---
language: en
status: active
artifact_role: canonical
authority: System Owner
last_review: 2026-05-03
---

STANDARD OPERATING PROCEDURE

* Item Name: MADEIRA quarterly UX review (control plane surface)  
* Item Number: SOP-MADEIRA_UX_REVIEW_001  
* Related process registry ID: `env_tech_dtp_madeira_uxreview` (parent workstream `env_tech_ws_madeira_quality` under MADEIRA Platform `env_tech_prj_3`)  
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

Keep **`static/madeira_control.html`** and related dashboard entrypoints aligned with Holistika **brand**, **accessibility**, and **localisation** expectations so the third **surface light** in the MADEIRA verdict can be adjudicated objectively.

---

## 2. Scope and process linkage

| `item_id` | `item_name` | Granularity |
|:----------|:------------|:-----------|
| `env_tech_dtp_madeira_uxreview` | MADEIRA quarterly UX review (Impeccable) | process |

**In scope:** `/madeira/control` HTML served by AKOS FastAPI shell; keyboard paths; aria labelling on dynamic status; locale toggles documented in Initiative 49 plan.

**Out of scope:** OpenClaw WebChat markup (upstream UI); unrelated dashboard pages unless explicitly added by future initiative charter.

---

## 3. Roles and responsibilities

| Role | Accountability |
|:-----|:---------------|
| **System Owner** | Approves ship / no-ship verdict for surface light after quarterly review pack |
| **AI Engineer / Developer** | Lands HTML/CSS fixes, wires tests |
| **UX reviewer (operator)** | Runs Impeccable critique artefact pathway and attaches report under initiative `reports/` folder |

---

## 4. Cadence and triggers

**Quarterly** calendar reminder; additionally **within 10 business days** after any materially visible rewrite of `static/madeira_control.html`.

---

## 5. Procedure

1. Ensure **baseline gates** PASS: FastAPI `/madeira/control` returns 200 in dev environment.  
2. Run **automated critique** pathway per Initiative 49 plan (`impeccable-critique-madeira-control-<date>.md` under `docs/wip/planning/49-madeira-management-rollup/reports/`).  
3. Run **axe** (via Playwright when available in repo CI image) capturing violations list; remediate WCAG-AA blockers prior to declaring surface light green.  
4. Exercise **locale toggles** (en/es/fr strings) verifying no hard-coded copy remains on primary controls without translation entry.  
5. Store evidence paths in dossier Operational health subsection when MADEIRA dossier flavour is emitted.  

---

## 6. Verification and dossier contract

| Source | Dossier section | Signal |
|:-------|:----------------|:-------|
| Impeccable critique markdown | Section 8 surface UX subsection | Narrative UX verdict |
| `tests/test_madeira_control_a11y.py` (when present) | Section 8 | Machine accessibility signal |
| `tests/test_madeira_control_i18n.py` (when present) | Section 8 | Translation completeness |
| `scripts/lint_brand_voice_offline.py` stdout (when surfaced) | Section 8 | Low-cost jargon guard on nearby prompts |

**Bidirectional contract:** Section 8 MADEIRA subsection lists `produces_for_sop: SOP-MADEIRA_UX_REVIEW_001`; this SOP verification table names those artefacts by filename pattern.

---

## 7. Escalation

If WCAG-AA blockers cannot be cleared within the quarterly window, System Owner declares **surface light amber**, documents compensating controls (manual operator checklist only when automated fix impossible), and links follow-up charter.

---

## 8. References

* `.cursor/rules/akos-madeira-management.mdc`  
* Initiative 49 rollup `master-roadmap.md`  
* `DESIGN.md` / `PRODUCT.md` brand bridges  
* `SOP-MADEIRA_VERDICT_AND_CADENCE_001.md`  

---

## 9. Decision log (within-SOP)

| Date | Decision | Rationale |
|:-----|:---------|:----------|
| 2026-05-03 | Initial publication under Initiative 49 | Surfaces third-light evidentiary pathway |
