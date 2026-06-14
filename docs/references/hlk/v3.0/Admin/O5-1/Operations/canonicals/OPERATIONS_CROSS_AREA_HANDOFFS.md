---
language: en
status: active
canonical: true
role_owner: COO
classification: way_of_working
intellectual_kind: doctrine
ssot: true
authored: 2026-06-10
last_review: 2026-06-10
last_review_at: 2026-06-10
last_review_by: COO
last_review_decision_id: D-IH-94-A
methodology_version_at_review: v3.1
companion_to:
  - OPERATIONS_AREA_CHARTER.md
  - OPERATIONS_DELIVERY_DISCIPLINE.md
  - OPERATIONS_PROCESS_CATALOG.yaml
upstream:
  - docs/wip/planning/94-area-architecture-and-completeness-v2/reports/i94-operations-cross-area-execution-map-2026-06-10.md
  - docs/wip/planning/94-area-architecture-and-completeness-v2/reports/i94-operations-p4-p6-execution-spec-2026-06-10.md
---

# OPERATIONS_CROSS_AREA_HANDOFFS — trigger register (Operations DO)

> **Purpose:** Register-only canonical. Operations **fires triggers**; sister areas **own doctrine
> and SSOT**. Each row names: trigger → sister owner → script/runbook → evidence path.
> Upstream map: [`i94-operations-cross-area-execution-map-2026-06-10.md`](../../../../../../docs/wip/planning/94-area-architecture-and-completeness-v2/reports/i94-operations-cross-area-execution-map-2026-06-10.md).

## Design rule (binding)

| Handoff class | Operations owns | Sister area owns |
|:---|:---|:---|
| **OPS-TRIG-MIRROR** | Emit + operator notify | Data — mirror apply, DataOps probes |
| **OPS-TRIG-FINOPS** | Engagement/QBR events | Finance — counterparty, rev-rec, billing facts |
| **OPS-TRIG-COMPLIANCE** | Tranche proposal + validate_hlk | People/Compliance — CSV SSOT, PRECEDENCE |
| **OPS-TRIG-TECH** | Fleet hygiene gate before deploy | Tech — CICD, repo registry, runtime |
| **OPS-TRIG-RESEARCH** | Engagement elicitation hooks | Research — IO SOPs, register freshness |
| **OPS-LOCAL-DO** | Full SOP+runbook pair | — (Operations vault only) |

---

## Data — mirror two-plane handoffs

| Trigger | When Operations fires | Sister owner | Script / runbook | Evidence |
|:---|:---|:---|:---|:---|
| Compliance mirror emit | After canonical CSV tranche commit | Data / System Owner | `py scripts/verify.py compliance_mirror_emit` | [`SOP-OPS_MIRROR_EMIT_TRIGGER_001.md`](../PMO/canonicals/SOP-OPS_MIRROR_EMIT_TRIGGER_001.md) |
| Mirror apply (DML) | Operator approves emitted batches | Data / System Owner | `pwsh -File scripts/apply_mirror_batches.ps1` | [`holistika-mirror-dml-apply.md`](../../../../../../guides/holistika-mirror-dml-apply.md) |
| Schema drift probe | Post-tranche or wave close | Data / System Owner | `py scripts/validate_compliance_schema_drift.py` | [`akos-holistika-operations.mdc`](../../../../../../.cursor/rules/akos-holistika-operations.mdc) |
| DataOps discipline | Engagement data-plane touch | Data Architect | `py scripts/validate_hlk.py` | [`SOP-HOLISTIKA_COMPLIANCE_MIRROR_DML_001`](../../People/Compliance/SOP-HOLISTIKA_COMPLIANCE_MIRROR_DML_001.md) |

---

## People / Compliance — CSV gates and area governance

| Trigger | When Operations fires | Sister owner | Script / runbook | Evidence |
|:---|:---|:---|:---|:---|
| process_list tranche | AREA-09 pairing or net-new process row | People / PMO | `py scripts/i94_area09_process_list_tranche.py` | [`SOP-PMO_PROCESS_LIST_CSV_MAINTENANCE_001.md`](../PMO/SOP-PMO_PROCESS_LIST_CSV_MAINTENANCE_001.md) |
| Canonical CSV gate | Hooks block commit on baseline/process CSV | People / Compliance | `.cursor/hooks.json` + `py scripts/validate_hlk.py` | [`PRECEDENCE.md`](../../People/Compliance/canonicals/PRECEDENCE.md) |
| Initiative harmonisation | New initiative manifests_processes FK | People / PMO | `py scripts/validate_initiative_registry.py` | [`SOP-INITIATIVE_PROCESS_HARMONISATION_001.md`](../PMO/SOP-INITIATIVE_PROCESS_HARMONISATION_001.md) |
| Vault promotion | WIP → process_list promotion | People / PMO | `py scripts/validate_hlk.py` | [`SOP-PMO_VAULT_PROMOTION_GATE_001.md`](../PMO/canonicals/SOP-PMO_VAULT_PROMOTION_GATE_001.md) |
| Area completeness | Ops tranche / wave close | People (AREA governance) | `py scripts/validate_area_completeness.py --area Operations` | [`SOP-OPS_AREA_COMPLETENESS_SWEEP_001.md`](../PMO/canonicals/SOP-OPS_AREA_COMPLETENESS_SWEEP_001.md) |
| Evidence-class gate | WIP closure / ledger govern / initiative close | **Operations PMO** (orchestrator) | `py scripts/run_automated_uat_evidence_sweep.py` | [`SOP-PMO_EVIDENCE_CLASS_GATE_001.md`](../PMO/canonicals/SOP-PMO_EVIDENCE_CLASS_GATE_001.md) |
| Evidence registry SSOT | Registry mint / ECB row change | **Data / Data Steward** | `py scripts/validate_evidence_class_registry.py` | [`DATA_GOVERNANCE_POLICY.md`](../../Data/Governance/canonicals/DATA_GOVERNANCE_POLICY.md) |
| MKTOps LP deploy → UX proof | Campaign landing-page deploy (MKT-03) | Marketing / Reach | Optional `artifacts/ux-audit/lighthouse-*.json` | [`MKTOPS_DISCIPLINE.md`](../../Marketing/canonicals/MKTOPS_DISCIPLINE.md) → ECB-0010 |
| UAT shape + FM-12 | Forward closure UAT PASS | People / PMO | `py scripts/validate_uat_report.py` | [`UAT_DISCIPLINE.md`](../../People/canonicals/UAT_DISCIPLINE.md) |
| Research ledger honesty | Source ledger tranche | Research / Lead Researcher | `py scripts/validate_research_action.py` | [`RESEARCH_ACTION_DISCIPLINE.md`](../../../Research/Methodology/canonicals/RESEARCH_ACTION_DISCIPLINE.md) |
| ADVOPS register maintenance | Adviser open questions refresh | People / Legal | `py scripts/validate_adviser_questions.py` | [`SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md`](../PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md) |

---

## Finance — FINOPS bridge handoffs

| Trigger | When Operations fires | Sister owner | Script / runbook | Evidence |
|:---|:---|:---|:---|:---|
| Engagement signed | ENGAGEMENT_REGISTRY status → active | Finance / RevOps | `py scripts/revops_dispatch.py` | [`SOP-FINOPS_BRIDGE_001.md`](../RevOps/canonicals/SOP-FINOPS_BRIDGE_001.md) |
| Revenue rollup refresh | Weekly RevOps cadence | Finance / RevOps | `py scripts/validate_revops_spine.py` | [`SOP-REVENUE_ROLLUP_001.md`](../RevOps/canonicals/SOP-REVENUE_ROLLUP_001.md) |
| LEADS WEB centralization | BD routing to counterparty | Finance / RevOps | `py scripts/revops_dispatch.py` | [`SOP-FINOPS_BRIDGE_001.md`](../RevOps/canonicals/SOP-FINOPS_BRIDGE_001.md) |
| QBR cycle | Quarterly business review | Finance / CMO | `py scripts/validate_engagement_template_registry.py` | [`SOP-REVOPS_QBR_001.md`](../RevOps/canonicals/SOP-REVOPS_QBR_001.md) |

---

## Tech — fleet hygiene and deploy gates

| Trigger | When Operations fires | Sister owner | Script / runbook | Evidence |
|:---|:---|:---|:---|:---|
| Consumer-repo work | Before sibling-repo PR / deploy | Tech / System Owner | `py scripts/check_external_repo_ci_posture.py` | [`akos-deploy-health.mdc`](../../../../../../.cursor/rules/akos-deploy-health.mdc) |
| Workspace fleet hygiene | Weekly Mon rhythm | Tech / System Owner | `py scripts/workspace_fleet_hygiene_sweep.py` | [`SOP-CICD_BASELINE_001.md`](../../Tech/System Owner/SOP-CICD_BASELINE_001.md) |
| Runtime inventory | AKOS config / provider change | Tech / System Owner | `py scripts/legacy/verify_openclaw_inventory.py` | [`docs/ARCHITECTURE.md`](../../../../../../ARCHITECTURE.md) |
| Release gate | Pre-merge / wave close | Tech / System Owner | `py scripts/release-gate.py` | [`docs/DEVELOPER_CHECKLIST.md`](../../../../../../DEVELOPER_CHECKLIST.md) |

---

## Research — IntelligenceOps pointer (post OPS-86-26 eviction)

| Trigger | When Operations fires | Sister owner | Script / runbook | Evidence |
|:---|:---|:---|:---|:---|
| Pre-engagement counterparty work | Discovery / elicitation phase | Research / Lead Researcher | `py scripts/research_radar_sweep.py` | [`SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT_001.md`](../../../Research/Intelligence/canonicals/SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT_001.md) |
| Reliability grading | Source ledger govern stage | Research / Lead Researcher | `py scripts/validate_research_action.py` | [`SOP-IO_RELIABILITY_GRADING_001.md`](../../../Research/Intelligence/canonicals/SOP-IO_RELIABILITY_GRADING_001.md) |
| Regulator / media checkpoint | RevOps quarterly or event-triggered review | Research / Research Director | `py scripts/revops_dispatch.py` | [`INTELLIGENCEOPS_REGISTER.csv`](../../../Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv) |
| Holistic orchestration research | Agent session friction / capability gaps | Research / Research Director | WIP pack under `docs/wip/intelligence/holistic-agentic-capability-orchestration-2026-06-10/` | [`IO-CAP-HOLISTIC-AGENTIC-ORCHESTRATION-2026-001`](../../../Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv) |

---

## Solo operator + AIC daily spine (reference)

| Cadence | Operations scripts | Handoff class | Evidence |
|:---|:---|:---|:---|
| Daily | `render_operator_inbox.py`, `render_wip_dashboard.py --check-only` | OPS-LOCAL-DO | — |
| Event | `run_automated_uat_evidence_sweep.py` | OPS-LOCAL-DO | [`SOP-PMO_EVIDENCE_CLASS_GATE_001.md`](../PMO/canonicals/SOP-PMO_EVIDENCE_CLASS_GATE_001.md) |
| Weekly | SMO catalog review, `workspace_fleet_hygiene_sweep.py` | OPS-LOCAL-DO / OPS-TRIG-TECH | — |
| Event | `compliance_mirror_emit`, `scaffold_engagement.py`, `validate_area_completeness --next` | MIXED | — |
| Quarterly | `render_operational_cohesion_index.py`, RevOps QBR | OPS-LOCAL-DO / OPS-TRIG-TECH | — |

---

## Cross-references

- Area charter: [`OPERATIONS_AREA_CHARTER.md`](../OPERATIONS_AREA_CHARTER.md)
- Delivery doctrine §handoffs: [`OPERATIONS_DELIVERY_DISCIPLINE.md`](../OPERATIONS_DELIVERY_DISCIPLINE.md)
- Executable catalog: [`OPERATIONS_PROCESS_CATALOG.yaml`](OPERATIONS_PROCESS_CATALOG.yaml)
- I94 execution spec: [`i94-operations-p4-p6-execution-spec-2026-06-10.md`](../../../../../../docs/wip/planning/94-area-architecture-and-completeness-v2/reports/i94-operations-p4-p6-execution-spec-2026-06-10.md)
