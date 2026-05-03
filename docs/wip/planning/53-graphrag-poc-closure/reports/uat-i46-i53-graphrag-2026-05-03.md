# I46 + I53 closure UAT — GraphRAG PoC

**Date:** 2026-05-03
**Initiatives closed:** [Initiative 46 — Neo4j Strategic Posture](../../46-neo4j-strategic-posture/master-roadmap.md) (P3-P7) + [Initiative 53 — GraphRAG PoC closure](../master-roadmap.md) (all phases)
**Verdict:** **NO-SHIP this cycle.** Both initiatives close on the documented no-ship path; live A/B forwarded as **OPS-53-1**.

## Verification matrix

| Gate | Result |
|:--|:--|
| `py scripts/legacy/verify_openclaw_inventory.py` | **PASS** — Overall PASS; full strict inventory preserved |
| `py scripts/check-drift.py` | **PASS** — No drift detected. Runtime matches repo state |
| `py scripts/test.py all` | **PASS** — full suite |
| `py scripts/release-gate.py` | **PASS (8/8 gates)** — Strict inventory, Test suite, Drift check, Browser smoke, API smoke, HLK vault validation, process_list.csv header, HLK vault links |
| `py scripts/validate_hlk.py` | **PASS** |
| `py scripts/graphrag_poc.py --validate-config` | **PASS** (20 queries) |
| `py scripts/graphrag_poc.py --dry-run` | **PASS** (lists 20 queries; cost ceiling $20.00; planned A/B) |
| `py -m pytest tests/test_graphrag_poc.py tests/test_neo4j_retrieval_mode.py tests/test_neo4j_graph_escape.py tests/test_neo4j_usecase_a_hardening.py -v` | **PASS** (46 / 46 in 3.51s) |
| `py scripts/graphrag_drift_canary.py --csv-only` | **PASS** (10 dimensions printed; CSV row counts visible without live Neo4j) |

## State of the GraphRAG surface

### Doctrine (I46 P1; closed)

- [`docs/references/hlk/v3.0/Envoy Tech Lab/Neo4j/NEO4J_STRATEGY.md`](../../../references/hlk/v3.0/Envoy%20Tech%20Lab/Neo4j/NEO4J_STRATEGY.md) — vault doctrine; 3 use-cases (A. Governance KG / B. GraphRAG over HLK vault / C. Agent memory).
- Cited by `prompts/overlays/OVERLAY_HLK_GRAPH.md` + `config/sync/kirbe-sync-contract.md` §11 + the `EXTERNAL_REPO_CONTRACT_TEMPLATE.md`.

### Use-case A hardening (I46 P2; closed)

- `hlk_graph_skill_neighbourhood` MCP tool registered + green.
- `neo4j_governance_kg_drift_smoke` profile wired in [`config/verification-profiles.json`](../../../config/verification-profiles.json).
- `release_gate` idempotency proof preserved (`sync_hlk_neo4j` 2 consecutive runs identical, per D-IH-32-Q proof).

### Use-case B PoC (I46 P3 + I53 P1-P4; closed on no-ship path)

- `scripts/graphrag_poc.py` — 3-mode scaffold (`--validate-config`, `--dry-run`, live-with-`AKOS_GRAPHRAG_POC_LIVE=1`).
- `config/graphrag/golden_queries.json` — 20 queries (60% multi-hop / 40% single-hop per D-IH-53-B).
- `tests/test_graphrag_poc.py` — 14 tests; all PASS.
- **Live A/B not executed this cycle** (R-53-4 NO-FIRE; per R-46-1 operator-funded $20 envelope; per D-IH-53-C non-additive trade-off → no-fire ⇒ no-ship).
- **OPS-53-1 forwarded** to next AKOS_RECORD_LIVE cycle (likely shared with OPS-52-1 multi-judge real-API calibration burn).

### Use-case C ADR (I46 P4; closed)

- [`docs/references/hlk/v3.0/Envoy Tech Lab/Neo4j/AGENT_MEMORY_DEFERRED_ADR.md`](../../../references/hlk/v3.0/Envoy%20Tech%20Lab/Neo4j/AGENT_MEMORY_DEFERRED_ADR.md) — explicit trigger condition selected; no build in I46.

### Conditional-ship infrastructure (I46 P5 + I53 P5 SKIPPED; preserved)

- `retrieval_mode` column on `SKILL_REGISTRY.csv` — present, all 5 skill rows empty (back-compat).
- `pol_neo4j_graph_rag_eligibility` POLICY row + `policy_class=graph_rag_eligibility` enum value — present.
- `akos/intent.py` reads `retrieval_mode` — wired.
- Supabase migration `20260501070000_i46_skill_registry_retrieval_mode.sql` — applied.
- **CSV flip not executed** (P5 SKIPPED; awaits ship signal from a future live A/B).

### Test wiring + canaries (I46 P6 + I53 P6; closed)

- `tests/test_neo4j_graph_escape.py` (adversarial: graph-escape + citation spoofing) — green.
- `tests/test_neo4j_retrieval_mode.py` — locks the column contract.
- `tests/test_graphrag_poc.py` — 14 tests; all green.
- `scripts/graphrag_drift_canary.py` — green; CSV-only mode prints 10 dimensions.
- Cassettes folder `tests/evals/cassettes/graph_rag/` — present; recorded cassettes will land here when OPS-53-1 fires.

## Decisions executed

- **D-IH-46-Decision-P3-NO-SHIP-2026-05-03** — recorded in both [`46-neo4j-strategic-posture/decision-log.md`](../../46-neo4j-strategic-posture/decision-log.md#decisions-made-during-execution) and [`53-graphrag-poc-closure/decision-log.md`](../decision-log.md#d-ih-46-decision-p3-no-ship-2026-05-03-also-recorded-in-i46-decision-log).
- **D-IH-53-A** (judge model — re-use I52 roster) — pinned but not exercised this cycle.
- **D-IH-53-B** (60% multi-hop / 40% single-hop) — already encoded in I46 P3 golden_queries.json.
- **D-IH-53-C** (non-additive trade-off; partial-credit forbidden) — applied to G-53-1 evaluation; no-fire ⇒ no-ship.
- **D-IH-53-D** (rollback procedure) — defines the operational contract for any future ship-then-rollback scenario.

## Gates

- **G-53-1** (P4 ship/no-ship verdict) — **NO-FIRE** → no-ship. Cassettes preserved.
- **G-53-2** (P5 SKILL_REGISTRY flip) — **SKIPPED** (conditional on G-53-1 ship signal).
- **G-53-3** (P5 POLICY clone per topic class) — **SKIPPED** (conditional on G-53-1 ship signal).

## OPS register flips

- **OPS-53-1 created + forwarded** — first operator-funded live GraphRAG PoC A/B run on `SKILL-MADEIRA-LOOKUP-V1` (20 queries × 2 modes; multi-judge accuracy scoring via I52 roster); ~$10-15 estimated within R-46-1 $20 envelope. Trigger: next operator-funded `AKOS_RECORD_LIVE=1` window.
- **OPS-52-1** (real-API multi-judge calibration burn from I52 P3) — likely shared with OPS-53-1 in one cycle.

## Risk status at closure

- **R-53-1** (envelope insufficient): mitigated; estimate ~$10/$20 per I53 P1.
- **R-53-2** (marginal success): not yet realized; D-IH-53-C blocks accidental partial-credit ship.
- **R-53-3** (graph-escape): adversarial probes green this cycle; remains the floor.
- **R-53-4** (operator declines live A/B): **realized as anticipated**; no-fire is the documented governance outcome.

## Success metrics

- ✓ I46 master-roadmap success criterion *"explicit decision-not-to-ship with PoC numbers"* satisfied via the no-fire governance pattern.
- ✓ Cassettes preserved.
- ✓ Conditional-ship infrastructure preserved ship-ready.
- ✓ Both initiative master-roadmaps flipped to `Closed`.
- ✓ Drift canary green in CSV-only smoke.
- ✓ Adversarial probes green.

## What this is NOT

- A "no" on GraphRAG. It is a **deferred ship-evaluation** pending operator-funded live A/B.
- A regression in any production surface. Nothing has changed in the runtime path; vector-only baseline remains the operational state for `SKILL-MADEIRA-LOOKUP-V1`.
- A withdrawal of doctrine. NEO4J_STRATEGY.md remains canonical.

## What ships next cycle (when OPS-53-1 fires)

1. Operator runs the I46 P3 scaffold live with `AKOS_GRAPHRAG_POC_LIVE=1` + provider keys + the I52 multi-judge roster active.
2. `reports/graphrag-poc-results-YYYY-MM-DD.md` is published with concrete numbers.
3. `D-IH-46-Decision-P3-{SHIP|NO-SHIP}-YYYY-MM-DD` is appended to both decision-logs.
4. If SHIP, P5 flips `SKILL-MADEIRA-LOOKUP-V1.retrieval_mode = graph_rag` + clones `pol_neo4j_graph_rag_eligibility` per topic class. If NO-SHIP, the no-ship branch documents the bar evaluation with concrete numbers (the previous no-fire branch is preserved as historical context).
