---
tranche_id: P95-GOV-6
tranche_class: internal_governance
ratifying_decisions:
  - D-IH-95-J
  - D-IH-95-B
reversibility_class: low
synthesis_complete: true
verdict: PASS
---

# Synthesis — P95-GOV-6 (Plane-1 universal hardening)

**Date:** 2026-06-09  
**Tranche:** Wire all governance-registry plane-1 validators into `validate_hlk.py`; COLLABORATOR_SHARE FAIL ramp

## Fire set (internal_governance)

| Dimension | Status | Note |
|:---|:---:|:---|
| SYN-05 Ratification lineage | PASS | D-IH-95-J minted; operator mandate from charter §10 |
| SYN-07 Tranche atomicity | PASS | registry + validate_hlk + profiles + decision + synthesis in one commit |
| SYN-08 Reversibility | PASS | low — revert dispatch rows + restore pre_commit MADEIRA steps |
| SYN-09 Closing-loop test | PASS | `validate_hlk.py` + `validate_collaborator_share.py --strict` |
| SYN-01/02/03/04/06/10 | INFO | J-OP internal; no external prose |

## Deliverables

| Surface | Change |
|:---|:---|
| `validate_hlk.py` | MADEIRA trio + CANONICAL_REGISTRY + COMPLIANCE_SCHEMA_DRIFT + CS `--strict` |
| `CANONICAL_GOVERNANCE_REGISTRY.csv` | 73/73 `plane1_in_validate_hlk=true` |
| `DECISION_REGISTER.csv` | D-IH-95-J |
| `release-gate.py` / `verification-profiles.json` | MADEIRA + schema-drift deduped to umbrella |

## Verification (mechanical)

```text
py scripts/validate_hlk.py
py scripts/validate_collaborator_share.py --strict
py scripts/validate_canonical_governance_registry.py
py scripts/synthesis_before_tranche_check.py --tranche-id P95-GOV-6 --tranche-class internal_governance --ratifying-decisions D-IH-95-J --reversibility low --closing-loop-test validate_hlk.py
py scripts/verify.py pre_commit_fast
```
