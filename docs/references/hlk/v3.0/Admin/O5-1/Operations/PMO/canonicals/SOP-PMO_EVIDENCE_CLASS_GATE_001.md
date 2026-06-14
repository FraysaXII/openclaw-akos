---
language: en
Item Name: PMO evidence class gate (WIP forge proof orchestration)
Item Number: SOP-PMO_EVIDENCE_CLASS_GATE_001
Object Class: Guideline and Procedure
Confidence Level: Safe
Security Level: 2 (Internal Use)
Entity Owner: Think Big
Area Owner: Operations
Associated Workstream: Holistika Process Governance Framework
Version: 1.0
Revision Date: 2026-06-14
Inherited Pattern: pattern_paired_sop_runbook
linked_runbooks:
  - scripts/run_automated_uat_evidence_sweep.py
  - scripts/validate_evidence_class_gate.py
Paired Runbook: scripts/run_automated_uat_evidence_sweep.py
Acceptance Criteria Human: PMO ensures completion claims cite evidence_class + proof before PASS closure UAT on/after 2026-06-14.
Acceptance Criteria Automation: run_automated_uat_evidence_sweep.py exit 0; validate_hlk.py EVIDENCE_CLASS_REGISTRY + PROOF_ADAPTER_REGISTRY PASS.
linked_canonicals:
  - EVIDENCE_CLASS_GATE_DISCIPLINE.md
  - ../../../Data/Governance/canonicals/dimensions/EVIDENCE_CLASS_REGISTRY.csv
  - ../../../Data/Governance/canonicals/dimensions/PROOF_ADAPTER_REGISTRY.csv
---

# SOP-PMO_EVIDENCE_CLASS_GATE_001

## Purpose

Operations PMO orchestrates **proof-backed completion** across WIP forge surfaces
(planning UAT, intelligence ledgers, initiative close) without duplicating sister-area
doctrine. This SOP is the human contract; the paired runbook automates the sweep.

## Scope

- `docs/wip/planning/**/reports/uat-*.md` forward closure reports
- `docs/wip/intelligence/**/source-ledger.csv` research packs
- `INITIATIVE_REGISTRY.csv` status → closed (forward closes)
- `AIC_CAPABILITY_IMPLEMENTATION_MATRIX.csv` implemented+confirmed cells
- Future UX adapters (Lighthouse, Hotjar) via `PROOF_ADAPTER_REGISTRY.csv`

## AC-HUMAN

1. Before PASS on forward closure UAT: set `evidence_class` + `evidence_proof_ref`.
2. After bulk ledger seed: run strip script; never ask operator to verify padded rows.
3. On initiative close: confirm latest closure UAT path + evidence bar.
4. To add Lighthouse/Hotjar: mint adapter row (charter) → implement script → ramp severity.

## AC-AUTOMATION

1. `py scripts/run_automated_uat_evidence_sweep.py` — exit 0 before merge on UAT-touching PRs.
2. `py scripts/validate_evidence_class_registry.py` — registry FK integrity.
3. `py scripts/validate_evidence_class_gate.py --self-test` — pre_commit_fast.
4. Component validators per EVIDENCE_CLASS_REGISTRY `validator_script` column.

## Adapter severity ramp (Lighthouse / Hotjar / new tools)

| Stage | Registry `status` | Binding `severity` | Trigger |
|:---|:---|:---|:---|
| 1 Charter | adapter `charter` | ECB row `INFO` | Design + privacy review |
| 2 Pilot | adapter `active` | `WARN` | One clean artifact bundle |
| 3 Production | adapter `active` | `FAIL` | Operator decision row |

New adapters **extend** the registry; they do not fork parallel validator frameworks.

## Escalation

| Signal | Action |
|:---|:---|
| RA-EC-01/02 | `strip_padded_source_ledger.py --write` |
| UAT-FM-12 | Add frontmatter or FAIL/PWF |
| Initiative close blocked | Fix closure UAT or keep active |
| Adapter charter stuck | OPS row + inline-ratify for FAIL ramp |

## Out of scope

- Replacing UAT_DISCIPLINE 11-section bar (People owns)
- Replacing research prong lattice (Research owns)
- Live Hotjar/Lighthouse production keys in repo (Tech secrets plane)

## Cross-references

- Doctrine: [`EVIDENCE_CLASS_GATE_DISCIPLINE.md`](EVIDENCE_CLASS_GATE_DISCIPLINE.md)
- Vault promotion: [`SOP-PMO_VAULT_PROMOTION_GATE_001.md`](SOP-PMO_VAULT_PROMOTION_GATE_001.md)
