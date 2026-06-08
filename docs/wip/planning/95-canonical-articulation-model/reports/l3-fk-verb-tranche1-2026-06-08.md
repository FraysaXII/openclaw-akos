# I95 L3 FK→verb tranche-1 — process_list + baseline_organisation

**Date:** 2026-06-08  
**Lane:** L3 (R2-05)  
**Verdict:** PASS (mechanical)

## Delivered

| Artifact | Purpose |
|:---|:---|
| `akos/hlk_canonical_articulation.py` `L3_TRANCHE1_FK_BINDINGS` | 10 mandatory CSV column → HCAM triple bindings |
| `scripts/validate_fk_verb_coverage.py` | Active-triple FK token resolution + L3 binding gate |
| `CANONICAL_RELATIONSHIP_REGISTRY.csv` fixes | TRP-003 `sub_area` on baseline; TRP-005 column prefix; TRP-031/032/036 layer FKs |
| `validate_hlk.py` `FK_VERB_COVERAGE` | Wired into HLK umbrella |
| `pre_commit_fast` profile + `.github/workflows/pre-commit-fast.yml` | ~2-4 min CI path |

## L3 tranche-1 bindings (10)

| CSV column | HCAM triple | Verb |
|:---|:---|:---|
| `process_list.role_owner` | TRP-001 | assignment → process |
| `process_list.item_parent_*_id` | TRP-005 | composition → process |
| `process_list.inherited_pattern_id` | TRP-007 | realization → pattern |
| `process_list.engagement_template_id` | TRP-008 | serving → engagement |
| `process_list.persona_id` | TRP-009 | serving → persona |
| `baseline_organisation.reports_to` | TRP-002 | composition → role |
| `baseline_organisation.area` | TRP-004 | aggregation → role |
| `baseline_organisation.sub_area` | TRP-003 | composition → area |
| `baseline_organisation.components_used` | TRP-027 | serving → role |

## Next tranche (L3-2)

- `CAPABILITY_REGISTRY` FK columns (role_owner, originating_process_ids, skill_ids, substrate_id)
- `DECISION_REGISTER` / `OPS_REGISTER` linked columns
- Promote planned triples with concrete `current_fk` (TRP-030 AIC→process via matrix)
