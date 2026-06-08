# I95 L3 FK→verb tranche-2 — capability + decision + ops registers

**Date:** 2026-06-08  
**Lane:** L3 (R2-05)  
**Verdict:** PASS (local `validate_fk_verb_coverage.py` + `validate_hlk.py`)

## Deliverables

| Artifact | Change |
|:---|:---|
| `akos/hlk_canonical_articulation.py` `L3_TRANCHE2_FK_BINDINGS` | 8 mandatory bindings; `L3_FK_BINDINGS` unions tranche-1 + tranche-2 |
| `scripts/validate_fk_verb_coverage.py` | Enforces all 18 L3 bindings |
| `CANONICAL_RELATIONSHIP_REGISTRY.csv` | Normalize `CAPABILITY_REGISTRY` → `capability_registry` on TRP-006/039/040/041 |

## L3 tranche-2 bindings (8)

| CSV column | Triple | Verb semantics |
|:---|:---|:---|
| `capability_registry.role_owner` | TRP-039 | capability assignment → role |
| `capability_registry.skill_ids` | TRP-040 | capability aggregation → skill |
| `capability_registry.substrate_id` | TRP-041 | substrate serving → capability |
| `capability_registry.originating_process_ids` | TRP-006 | process realization → capability |
| `decision_register.linked` | TRP-016 / TRP-017 | decision influence → area / process |
| `decision_register.linked_initiative_ids` | TRP-018 | decision influence → initiative |
| `ops_register.linked` | TRP-020 | ops_action influence → initiative |

## Deferred (planned triples)

- TRP-030 AIC→process via `aic_capability_implementation_matrix` (status `planned`)
- TRP-031/032/036 workstream/program/initiative composition via `process_list` layers
