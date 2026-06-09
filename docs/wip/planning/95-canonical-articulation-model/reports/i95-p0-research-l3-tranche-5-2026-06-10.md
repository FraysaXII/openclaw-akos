---
parent_initiative: INIT-OPENCLAW_AKOS-95
authored: 2026-06-10
audience: J-OP
lane: L3-FK-verb-tranche-5
ratifying_decisions:
  - D-IH-95-G
  - D-IH-95-I
linked_canonicals:
  - CANONICAL_RELATIONSHIP_REGISTRY.csv
  - i95-full-regression-2026-06-09.md
---

# P0 research — I95 L3 tranche-5 (10 unbound active triples)

## Scope choice (Tranche 1)

| Option | Functional name | Session fit | Gate |
|:---|:---|:---|:---|
| **A (deferred)** | I86 Wave N INDEX_INTEGRITY + planning README refresh | Multi-initiative; Wave N backlog + INITIATIVE_DEPENDENCIES regen | I86 coordinator; likely multi-session |
| **B (executed)** | I95 L3 tranche-5 — FK→verb bindings for F-11 gap | Bounded: 10 triples, code + relationship-registry slug normalize | No canonical-CSV row mint; relationship registry column edits only |

Operator burndown rank 1 (INDEX_INTEGRITY) unlocks all initiatives but exceeds one-session scope. Rank 2 (L3 tranche-5) is the highest-value **I95-only** ship unit per cluster map and PMO sweep §4.

## Internal evidence sweep

| Source | Trust | Finding |
|:---|:---|:---|
| [`i95-full-regression-2026-06-09.md`](i95-full-regression-2026-06-09.md) F-11 | High (same-day regression) | 40 active triples; 34 L3 bindings; **10 unbound**: TRP-019/022/023/024/025/026/028/048/049/050 |
| [`i95-round2-askquestion2-ratification-2026-06-09.md`](i95-round2-askquestion2-ratification-2026-06-09.md) | High | Tranche-4 pattern: add `L3_TRANCHE*n_FK_BINDINGS` + normalize `current_fk` slugs to lowercase registry slugs |
| [`akos/hlk_canonical_articulation.py`](../../../../akos/hlk_canonical_articulation.py) | SSOT | `L3_FK_BINDINGS` aggregates tranches 1–4; `FK_NON_CSV_REGISTRY_PREFIXES` already lists policy_register, intelligence_matrix, channel_touchpoint_registry, frontmatter |
| [`CANONICAL_RELATIONSHIP_REGISTRY.csv`](../../../../references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/dimensions/CANONICAL_RELATIONSHIP_REGISTRY.csv) | SSOT | Unbound triples already carry `current_fk` tokens; uppercase legacy slugs on TRP-026/028/048–050 |
| [`decision-log.md`](../decision-log.md) D-IH-95-I | High | L2 capability collapse **COMPLETE** 2026-06-08 (1,119→93); not re-opened for this tranche |
| [`i95-l2-state-audit-2026-06-09.md`](i95-l2-state-audit-2026-06-09.md) | High | Confirms 93 capability rows; L2 lane closed |

## Novelty test

**Refinement** of ratified R2-05 per-registry tranche pattern (D-IH-95-G). No new doctrine framing. External research sweep **not required** per applied-research RULE 2 refinement path.

## Synthesis — binding inventory (tranche-5)

| Triple | Verb cluster | Binding surface | Notes |
|:---|:---|:---|:---|
| TRP-019 | policy→process influence | `policy_register` (non-CSV) | Approved non-CSV surface |
| TRP-022 | topic→source_fact aggregation | `intelligence_matrix` (non-CSV) | Research/intelligence plane |
| TRP-023 | channel→audience serving | `channel_touchpoint_registry` (non-CSV) | Marketing channel doctrine |
| TRP-024 | canonical→pattern realization | `frontmatter.inherited_pattern_id` (non-CSV) | Vault markdown frontmatter |
| TRP-025 | persona_scenario→persona | `persona_scenario_registry.persona_id` | CSV-backed |
| TRP-026 | metric→data_contract access | `metrics_registry.source_contract_id` | Slug normalized from METRICS_REGISTRY |
| TRP-028 | skill→role assignment | `skill_registry.owner_role` | Slug normalized from SKILL_REGISTRY |
| TRP-048 | component→bi_consumer realization | `bi_consumer_registry.component_id` | BI consumer cluster |
| TRP-049 | bi_consumer→data_store access | `bi_consumer_registry.data_surfaces` | BI consumer cluster |
| TRP-050 | area→bi_consumer aggregation | `area_bi_profile.primary_consumer_ids` | AREA_BI_PROFILE |

## Execution plan

1. Mint `L3_TRANCHE5_FK_BINDINGS` + extend `L3_FK_BINDINGS`.
2. Normalize uppercase `current_fk` slugs in relationship registry (TRP-026/028/048–050).
3. Extend `validate_fk_verb_coverage.py` bare non-CSV binding check for tranche-5 surfaces.
4. Gates: `validate_fk_verb_coverage.py`, `validate_hlk.py`, `validate_canonical_articulation.py`.

## Verification commands

```powershell
py scripts/validate_fk_verb_coverage.py
py scripts/validate_canonical_articulation.py
py scripts/validate_hlk.py
```
