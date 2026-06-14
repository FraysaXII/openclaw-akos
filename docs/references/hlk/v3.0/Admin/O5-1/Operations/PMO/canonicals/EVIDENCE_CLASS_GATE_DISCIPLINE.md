---
title: Evidence Class Gate Discipline
language: en
intellectual_kind: doctrine
access_level: 4
audience: J-OP;J-AIC
status: active
canonical: true
role_owner: PMO
co_owner_role: COO
area: Operations
entity: Think Big
authored: 2026-06-14
last_review: 2026-06-14
last_review_by: PMO
last_review_decision_id: D-IH-90-AF
methodology_version_at_review: v3.2
ratifying_decisions:
  - D-IH-90-AF
register: internal
linked_canonicals:
  - OPERATIONS_DELIVERY_DISCIPLINE.md
  - OPERATIONS_CROSS_AREA_HANDOFFS.md
  - PMO/canonicals/OPERATIONAL_COHESION_DOCTRINE.md
  - PMO/canonicals/SOP-PMO_VAULT_PROMOTION_GATE_001.md
  - PMO/canonicals/SOP-PMO_EVIDENCE_CLASS_GATE_001.md
  - ../../../Data/Governance/canonicals/dimensions/EVIDENCE_CLASS_REGISTRY.csv
  - ../../../Data/Governance/canonicals/dimensions/PROOF_ADAPTER_REGISTRY.csv
  - ../../People/canonicals/UAT_DISCIPLINE.md
  - ../../People/canonicals/SOP-PEOPLE_UAT_GOVERNANCE_001.md
  - ../../../Research/Methodology/canonicals/RESEARCH_ACTION_DISCIPLINE.md
  - ../../People/canonicals/HOLISTIKA_QUALITY_FABRIC.md
linked_runbooks:
  - scripts/validate_evidence_class_gate.py
  - scripts/run_automated_uat_evidence_sweep.py
  - scripts/validate_research_action.py
  - scripts/validate_uat_report.py
  - scripts/validate_aic_capability_implementation_matrix.py
linked_cursor_rules:
  - .cursor/rules/akos-evidence-class-gate.mdc
  - .cursor/rules/akos-operations-delivery.mdc
  - .cursor/rules/akos-uat-discipline.mdc
  - .cursor/rules/akos-research-action.mdc
linked_skills:
  - .cursor/skills/evidence-class-gate-craft/SKILL.md
  - .cursor/skills/operations-delivery-craft/SKILL.md
companion_to:
  - SOP-PMO_EVIDENCE_CLASS_GATE_001.md
upstream_ssot:
  - docs/wip/planning/90-routing-and-wiring/reports/evidence-class-gate-singularity-ratification-2026-06-14.md
---

# Evidence Class Gate Discipline

> **Operations-owned orchestration** for proof-backed completion claims. WIP (`docs/wip/`)
> is the minting forge; this doctrine names how stable intent promotes into vault SSOT
> per [`SOP-PMO_VAULT_PROMOTION_GATE_001.md`](SOP-PMO_VAULT_PROMOTION_GATE_001.md).
> Sister areas **own** their specialty bar (People UAT, Research ledger, Tech deploy);
> Operations **fires** the cross-surface sweep and blocks dishonest closure.

## 1. Purpose

Validators that check CSV shape or markdown sections are necessary but not sufficient.
I100 showed 780 ledger rows passing schema validation while 463 were synthetic padding.
I96 Track D showed structural UAT PASS while browser evidence was deferred.

This discipline binds every **completion claim** to:

1. An **evidence class** (what kind of proof)
2. A **proof artifact** (repo path or registry row)
3. An optional **proof adapter** (Playwright, Lighthouse, Hotjar, deploy-health probe)

Mechanical SSOT code: `akos/evidence_class_gate.py`. Registry SSOT (Data path):
[`Data/Governance/canonicals/dimensions/EVIDENCE_CLASS_REGISTRY.csv`](../../../Data/Governance/canonicals/dimensions/EVIDENCE_CLASS_REGISTRY.csv).

## 2. WIP forge vs vault (Operations governs the handoff)

| Location | Role | Operations hook |
|:---|:---|:---|
| `docs/wip/planning/` | Initiative roadmaps, closure UAT drafts | Vault promotion gate SOP |
| `docs/wip/intelligence/` | Research packs, source ledgers | Strip + validate before govern |
| `docs/references/hlk/v3.0/Admin/O5-1/Operations/` | **Orchestration doctrine + SOP** | Area owner PMO + COO |
| `Data/Governance/canonicals/dimensions/` | **Registry SSOT** (`EVIDENCE_CLASS_REGISTRY.csv`, `PROOF_ADAPTER_REGISTRY.csv`) | Data Steward schema; PMO binding semantics |
| Sister canonicals | Specialty depth (UAT §11, research prongs, UX bar) | Cross-area handoff register |

Physical path of WIP does not change ownership: **Operations PMO** orchestrates promotion;
People Compliance holds CSV gates; Research owns ledger semantics.

## 3. Evidence classes

**Core six** (always valid when `status=active` in registry):

| Class | Proves |
|:---|:---|
| `git_shape` | Schema / header / FK / validator stdout |
| `url_verify` | External URL reachable |
| `live_probe` | Runtime / deploy probe succeeded |
| `browser_experiential` | Operator-visible UI journey + manifest |
| `operator_ratify` | Explicit human decision row |
| `meta_regression` | Intent-ranked regression after validator change |

**Extension classes** (registry-driven; `charter` until adapter + FAIL ramp):

| Class | Adapter | Tool |
|:---|:---|:---|
| `ux_lighthouse_audit` | PAD-002 | Google Lighthouse |
| `ux_heatmap_session` | PAD-003 | Hotjar / heatmap export |

Adding Lighthouse or Hotjar **does not require rewriting validators** — mint a
`PROOF_ADAPTER_REGISTRY.csv` row + `EVIDENCE_CLASS_REGISTRY.csv` binding, implement the
adapter script, then promote adapter `status` from `charter` → `active` and severity
INFO → WARN → FAIL per the ramp in [`SOP-PMO_EVIDENCE_CLASS_GATE_001.md`](SOP-PMO_EVIDENCE_CLASS_GATE_001.md).

## 4. Sister discipline composition

| Claim surface | Operations fires | Sister doctrine owns |
|:---|:---|:---|
| Research ledger | RA-EC-01/02 strip + validate | RESEARCH_ACTION_DISCIPLINE |
| Closure UAT PASS | FM-12 + automated sweep | UAT_DISCIPLINE + PWF discipline |
| Visual browser UAT | Manifest + screenshot validator | SOP-PEOPLE_UAT_VISUAL_EVIDENCE_001 |
| ACIM implemented+confirmed | Matrix proof tokens | HOLISTIKA_AGENTIC_DOCTRINE |
| Initiative close | Closure UAT cross-check | INITIATIVE governance SOPs |
| UX Lighthouse / Hotjar | Adapter charter rows ECB-0010/0011 | UX_DISCIPLINE + brand surfaces |

## 5. Automated UAT sweep (binding for AIC)

On every wave-close, initiative closure tranche, or evidence-gate validator edit, AIC runs:

```powershell
py scripts/run_automated_uat_evidence_sweep.py
```

This composite runbook executes forward closure-UAT validation, evidence-class initiative
cross-check, and writes `artifacts/evidence-gate/uat-sweep-*.json` for `evidence_proof_ref`
citation. Operators do not manually re-read every historical UAT — the sweep surfaces FAIL.

## 6. Watershed

Forward enforcement from **2026-06-14** (`EVIDENCE_GATE_WATERSHED_ISO_DATE` in code).
Pre-watershed artifacts remain exempt unless amended.

## 7. Cross-references

- Governance design (minting narrative): `docs/wip/planning/90-routing-and-wiring/reports/evidence-class-gate-governance-design-2026-06-14.md`
- I90 charter: `docs/wip/planning/90-routing-and-wiring/reports/evidence-class-gate-charter-2026-06-14.md`
- Handoffs: [`OPERATIONS_CROSS_AREA_HANDOFFS.md`](../../canonicals/OPERATIONS_CROSS_AREA_HANDOFFS.md)
