# I95 P2 (=C) — Neo4j edge unify + competency queries (D-IH-95-C)

**Date:** 2026-06-05 · **Coupled with:** I91 (enterprise graph store coverage) ·
**Posture:** additive / non-destructive (Neo4j preflight-blocked per I91 — no live mutation)

## 1. What P2 delivers (and what it defers)

P2 builds the **migration map + derivation queries + parity proof** that make the eventual
Neo4j edge rename mechanical and safe. It does **not** mutate the live projection
(`akos/hlk_graph_model.py`), its parity assertions, or `sync_hlk_neo4j.py` — those stay intact
until the **gated cutover** (Semantic Council ratify + I91 unblock with `NEO4J_*`).

Module: `akos/hlk_graph_articulation.py`. Tests: `tests/test_validate_canonical_articulation.py`.

## 2. The de-fork — 13 legacy edges → 6 unified verb-edges

| Unified Neo4j edge | ArchiMate verb | Legacy edges it absorbs |
|:---|:---|:---|
| **COMPOSED_OF** | composition | `REPORTS_TO`, `PARENT_OF`, `PROGRAM_PARENT_OF`, `UNDER_PROGRAM`, `TOPIC_PARENT_OF` |
| **AGGREGATES** | aggregation | `PROGRAM_SUBSUMES`, `TOPIC_SUBSUMES`, `UNDER_TOPIC` |
| **ASSIGNED_TO** | assignment | `OWNED_BY` |
| **FLOWS_TO** | flow | `CONSUMES`, `PRODUCES_FOR` |
| **SERVES** | serving | `DEPENDS_ON` |
| **ASSOCIATED_WITH** | association | `RELATED_TO` (last-resort; Council review) |

**The headline:** the three forked `*_PARENT_OF` edges (the original smoking gun) all become one
`COMPOSED_OF`; node labels disambiguate context. Edge-type count drops 13 → 6 with no loss of
meaning (verified by `assert_edge_coverage()`).

## 3. Competency questions (acceptance test — unified-edge Cypher)

| CQ | Question | Derivation |
|:---|:---|:---|
| CQ1 | Which processes is role R assigned to, and which capabilities do those realize? | assignment ∘ realization |
| CQ2 | What serves engagement E end-to-end, back to the roles that perform it? | serving + transfer over assignment |
| CQ3 | If capability C is retired, which areas/roles/engagements are impacted? | realization impact (reverse) |
| CQ4 | Show process P's full layer path (project → … → task) | composition transitive closure |
| CQ5 | Is every canonical in area A wired (no orphans)? | articulation-completeness (area v3) |

Cypher sketches live in `COMPETENCY_QUESTIONS` (specs, not executed — I91 preflight-blocked).

## 4. Cutover plan (gated — D-IH-95-C scope boundary)

1. **Now (this phase):** migration map + queries + parity test committed (additive).
2. **On I91 unblock (`NEO4J_*` present):** add a unified-edge emit mode to `hlk_graph_model.py`
   keyed off `LEGACY_EDGE_TO_UNIFIED`; dual-emit (legacy + unified) for one cycle; parity-check.
3. **Semantic Council ratify:** flip consumers (`hlk_graph_mcp_server`, explorer) to unified edges;
   retire legacy edge emission; update `graph_parity_counts`.
4. **Verify:** the 5 competency questions run green on the live graph.

## 5. Verification (this phase)
- `py -c "from akos.hlk_graph_articulation import assert_edge_coverage; assert_edge_coverage()"` → 13→6.
- `py -m pytest tests/test_validate_canonical_articulation.py` → 9 PASS.
- No change to `hlk_graph_model.py` → live projection + parity untouched (runtime contract preserved).

## 6. Cross-references
- HCAM model: `docs/references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/CANONICAL_ARTICULATION_MODEL.md`
- Verb→edge SSOT: `akos/hlk_canonical_articulation.py` (`VERB_TO_NEO4J_EDGE`)
- Legacy projection: `akos/hlk_graph_model.py`; I91: `docs/wip/planning/91-enterprise-graph-store-coverage/`
- Decision: `D-IH-95-C`
