---
language: en
Item Name: Operational cohesion index render
Item Number: SOP-PMO_OPERATIONAL_COHESION_INDEX_RENDER_001
Object Class: Guideline and Procedure
Confidence Level: Safe
Security Level: 2 (Internal Use)
Entity Owner: Holistika
Area Owner: Operations — PMO
Process Owner: PMO
Version: 1.0
Revision Date: 2026-06-10
Status: active
Inherited Pattern: pattern_paired_sop_runbook
linked_runbooks:
  - scripts/render_operational_cohesion_index.py
Acceptance Criteria Human: PMO + System Owner can walk OPERATIONAL_COHESION_DOCTRINE quarterly without the runbook.
Acceptance Criteria Automation: render_operational_cohesion_index.py validate exits 0 on CI.
---

## 1. Purpose

Validate and optionally emit the operational cohesion routing index backing [`OPERATIONAL_COHESION_DOCTRINE.md`](OPERATIONAL_COHESION_DOCTRINE.md) (D-IH-86-AM + AN).

## 2. Scope

In scope: doctrine frontmatter paths, J-* audience codes, governance_rules FK to `.cursor/rules/`.

Out of scope: editing doctrine prose (separate initiative); ERP panel implementation (I89).

## 3. Procedure

1. Run `py scripts/render_operational_cohesion_index.py validate` (default subcommand).
2. On FAIL, fix broken `linked_canonicals:` or audience drift; re-run until PASS.
3. Optionally emit index stub: `py scripts/render_operational_cohesion_index.py index`.
4. Quarterly: combine with cohesion review process (`ops_pmo_dtp_cohesion_quarterly_001`).

## 4. Failure modes

| Symptom | Action |
|:---|:---|
| Missing canonical path | Restore file or update doctrine frontmatter |
| Unknown J-* audience | Add row to AUDIENCE_REGISTRY.csv or fix typo |
| Missing cursor rule | Mint rule or remove stale governance_rules entry |

## 5. Cross-references

- Doctrine: [`OPERATIONAL_COHESION_DOCTRINE.md`](OPERATIONAL_COHESION_DOCTRINE.md)
- Runbook: [`scripts/render_operational_cohesion_index.py`](../../../../../../../scripts/render_operational_cohesion_index.py)
- Catalog: [`OPERATIONS_PROCESS_CATALOG.yaml`](../../canonicals/OPERATIONS_PROCESS_CATALOG.yaml)
