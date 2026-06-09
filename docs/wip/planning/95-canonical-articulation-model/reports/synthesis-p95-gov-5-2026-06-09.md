---
tranche_id: P95-GOV-5
tranche_class: canonical_csv_mint
ratifying_decisions:
  - D-IH-95-B
  - D-IH-72-O
  - D-IH-72-F
  - D-IH-86-BG
reversibility_class: medium
synthesis_complete: true
verdict: PASS
---

# Synthesis — P95-GOV-5 (mirror emit gap closure)

**Date:** 2026-06-09  
**Tranche:** Wire compliance mirror emit for DDL-backed surfaces without emit (extended scope)

## Fire set (canonical_csv_mint)

| Dimension | Status | Note |
|:---|:---:|:---|
| SYN-01 Audience completeness | PASS | J-OP internal; RevOps + PMO + Marketing adapter surfaces named |
| SYN-04 Brand register | PASS | N/A — no external prose |
| SYN-05 Ratification lineage | PASS | D-IH-95-B + adapter/template/output-arch precedents cited |
| SYN-07 Tranche atomicity | PASS | emit + registry + tests + synthesis in one commit |
| SYN-08 Reversibility | PASS | medium — revert emit wiring; registry profiles roll back |
| SYN-09 Closing-loop test | PASS | `validate_mirror_emit_contract.py` + `compliance_mirror_emit` + `validate_hlk.py` |
| SYN-02/03/06/10 | INFO | No new dashboard surface in this tranche |

## Scope guard honored

No new DDL (P95-GOV-7 forward-charter mirrors unchanged). RPA adapter remains `forward_charter`.

## Deliverables

| Surface | Emit profile | Sync policy | Mirror table |
|:---|:---:|:---:|:---|
| 8 adapter registries | `main` | `active` | `compliance.*_adapter_registry_mirror` |
| `ENGAGEMENT_TEMPLATE_REGISTRY.csv` | `main` | `active` | `engagement_template_registry_mirror` |
| `ENGAGEMENT_REGISTRY.csv` | `main` | `active` | `engagement_registry_mirror` |
| Output architecture ×3 | `main` | `active` | `output_type` / `artifact_class` / `component_primitive` mirrors |

## Mirror apply evidence stub (mirror-before-merge gate)

| Step | Status | Note |
|:---|:---:|:---|
| Prod DDL inventory (read-only) | **PENDING-OPERATOR** | Confirm I72 adapter + engagement-template + I70 engagement_registry + I86 output-arch DDL on prod before `apply=true` |
| `gh workflow run supabase-mirror-sync.yml -f apply=true` | **NOT RUN** | Blocked on operator SQL gate per Holistika ops lattice |
| Post-apply row-count parity | **NOT RUN** | Run after apply; compare `validate_mirror_emit_contract.py` INSERT counts vs prod `SELECT COUNT(*)` |

Operator path: [`docs/guides/holistika-mirror-dml-apply.md`](../../../../guides/holistika-mirror-dml-apply.md) · SOP `SOP-HOLISTIKA_COMPLIANCE_MIRROR_DML_001`.

## Verification (mechanical)

```text
py scripts/validate_mirror_emit_contract.py
py scripts/verify.py compliance_mirror_emit
py scripts/validate_canonical_governance_registry.py
py scripts/validate_hlk.py
py scripts/synthesis_before_tranche_check.py --tranche-id P95-GOV-5 --tranche-class canonical_csv_mint --ratifying-decisions D-IH-95-B --reversibility medium --closing-loop-test validate_mirror_emit_contract.py
py -m pytest tests/test_sync_compliance_mirrors_from_csv.py tests/test_validate_mirror_emit_contract.py -v
py scripts/verify.py pre_commit_fast
```

## DIM-4 disposition

Finance + RPA + DATA_CONTRACT forward-charter DDL remains **scope-extend** to P95-GOV-7 (not regressions).
