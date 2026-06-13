---
parent_initiative: INIT-OPENCLAW_AKOS-96
report_kind: process-catalog-e2e
authored: 2026-06-13
audience: J-OP;J-AIC
status: active
---

# Research Center — process catalog e2e wiring (2026-06-13)

> **Functional name:** The executable process catalog — `process_list.csv` rows paired with SOPs and automation runbooks. This doc maps those processes to Research Center **navigate** CTAs and drawer runbook URLs.

## Legend

| CTA status | Meaning |
|:---|:---|
| **wired** | Primary card CTA opens ERP route, GitHub blob, or KiRBe — B1.5 evidence |
| **drawer-only** | Runbook in drawer; card CTA does not execute process |
| **clipboard** | Copy command only — no navigate |
| **missing** | Process exists in catalog; no RC surface yet |

## Core research processes

| process_list `item_id` | Functional name | SOP | Runbook(s) | RC CTA / surface | Status | Gap |
|:---|:---|:---|:---|:---|:---:|:---|
| `hol_resea_dtp_research_radar_001` | Research radar freshness sweep | `SOP-RESEARCH_RADAR_001.md` | `scripts/research_radar_sweep.py`, `scripts/validate_research_radar.py` | Freshness strip micro-CTA · staleness cards · "Open intelligence register" navigate | **wired** (partial) | Card navigates to register path; **does not** auto-run sweep — drawer should show `py scripts/research_radar_sweep.py` |
| `hol_resea_dtp_research_action_001` | Research action 8-stage loop | `SOP-RESEARCH_ACTION_001.md` | `scripts/validate_research_action.py` | Ledger summary navigate · WIP pack list in v1 accordion | **wired** (partial) | No CTA to **start** new research action folder; validate command drawer-only |
| `env_tech_dtp_substrate_landscape_mtnce_001` | Substrate landscape via radar | `SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md` | `scripts/research_radar_sweep.py --include-substrate`, `scripts/peopl_research_substrate_audit_cadence.py` | Compliance lens stub · substrate drift cards | **missing** | No Director/Compliance navigate to substrate audit report or sweep flag |
| `env_tech_dtp_madeira_uxreview_001` | MADEIRA quarterly UX review (Impeccable) | `SOP-MADEIRA_UX_REVIEW_001` | Impeccable disposition docs | Auditor lens · Impeccable audit links | **drawer-only** | No navigate to `impeccable-audit-research-center-*` from card face |
| `env_tech_dtp_madeira_verdict_001` | MADEIRA verdict review | `SOP-MADEIRA_VERDICT_AND_CADENCE_001` | `scripts/render_uat_dossier.py` (MADEIRA modes) | — | **missing** | No RC card for verdict cadence |
| `env_tech_dtp_madeira_dossier_001` | MADEIRA dossier emit | same | `scripts/render_uat_dossier.py` | — | **missing** | Linked from MADEIRA program, not RC |
| `hol_peopl_dtp_uat_governance_001` | UAT governance (closure bar) | `SOP-PEOPLE_UAT_GOVERNANCE_001` | `scripts/validate_uat_report.py` | v1 accordion manifest links | **drawer-only** | Charter links not on insight rail |
| `hol_peopl_dtp_pwf_governance_001` | PASS-WITH-FOLLOWUP governance | `SOP-PEOPLE_PWF_GOVERNANCE_001` | `scripts/validate_pwf_governance.py` | B1.5 PWF experiential report link | **wired** (indirect) | Via check-links, not card CTA |

## RC navigate CTA inventory (B1.5 localhost evidence)

| CTA label (Operator/Director) | Destination class | Process wired |
|:---|:---|:---|
| Open intelligence register | GitHub / vault `INTELLIGENCEOPS_REGISTER.csv` | `hol_resea_dtp_research_radar_001` |
| Open KiRBe program | ERP route / program hub | KiRBe ingest (I96 contract) |
| Open ledger summary | Ledger reader / validation | `hol_resea_dtp_research_action_001` |

## Adapter metadata gaps (P-G4 Composer tranche)

| Gap ID | Process | Required adapter metadata | RC change |
|:---|:---|:---|:---|
| PC-E2E-01 | `hol_resea_dtp_research_radar_001` | `cta_kind=runbook` + `navigateHref` to register + `command=py scripts/research_radar_sweep.py` | BFF `insights.ts` builder for radar remediation |
| PC-E2E-02 | `hol_resea_dtp_research_action_001` | `cta_kind=artifact` + ledger path + validate command | Already partial — add **govern stage** link to WIP folder |
| PC-E2E-03 | `env_tech_dtp_substrate_landscape_mtnce_001` | `cta_kind=runbook` + `--include-substrate` | Compliance card when `SUBSTRATE_REGISTRY` stale |
| PC-E2E-04 | MADEIRA UX cluster | `cta_kind=doc_link` to experiential charter + UAT ladder | Director "program phase" strip |
| PC-E2E-05 | Executable process catalog (AOS) | `TECH_AUTOMATION_REGISTRY` crosswalk | Navigate CTAs for automation adapters — see [`tech-automation-registry-crosswalk-2026-06-11.md`](tech-automation-registry-crosswalk-2026-06-11.md) |

## Executable process catalog discipline

Per the executable process catalog rule: each net-new CTA that runs a governed process should cite:

- `process_ids` in hlk-erp change PR
- `linked_sop_path` + `linked_runbook_path` in BFF drawer payload
- `adapter_status` when automation is INFO-only (substrate audit cadence SOP still `review`)

## Verification (e2e)

| Step | PASS |
|:---|:---|
| Operator clicks staleness card primary CTA | Lands on register blob or ERP route — not marketing apex |
| Drawer runbook command | Matches `linked_runbook_path` from process_list row |
| Compliance lens (when seeded) | Substrate maintenance CTA or honest empty state |
| `py scripts/validate_hlk.py` | process_list rows unchanged in this doc-only tranche |

## Cross-references

- Master tranche P-G4: [`research-center-gap-closure-deploy-uat-tranche-2026-06-13.md`](research-center-gap-closure-deploy-uat-tranche-2026-06-13.md)
- Journey gap analysis: [`research-center-journey-gap-2026-06-12.md`](research-center-journey-gap-2026-06-12.md)
- Tech automation crosswalk: [`tech-automation-registry-crosswalk-2026-06-11.md`](tech-automation-registry-crosswalk-2026-06-11.md)
