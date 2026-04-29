# Re-evaluation trigger — Neo4j graph MCP tooling promotion

**Status**: TEMPLATE / NOT FIRED (2026-04-29).
**Owners**: AI Engineer (primary), CTO (secondary), PMO (UAT evidence).
**Authority**: Wave-2 plan §"Decisions" **D-IH-18**; Initiative 07 [closure](../../07-hlk-neo4j-graph-projection/master-roadmap.md) **D2** (allowlisted Cypher); this initiative's [`decision-log.md`](../decision-log.md).
**Pattern source**: I22-P8 [`re-eval-trigger.md`](../../22-hlk-scalability-and-i21-closures/reports/re-eval-trigger.md).

## Why this template exists

Initiative 23 P-graph shipped the **Neo4j graph projection** for Programs and Topics (`:Program` + `:Topic` nodes, `:CONSUMES` / `:PRODUCES_FOR` / `:PROGRAM_PARENT_OF` / `:PROGRAM_SUBSUMES` / `:DEPENDS_ON` / `:TOPIC_PARENT_OF` / `:RELATED_TO` / `:TOPIC_SUBSUMES` / `:OWNED_BY` / `:UNDER_PROGRAM` edges). The agent overlay [`OVERLAY_HLK_GRAPH.md`](../../../../prompts/overlays/OVERLAY_HLK_GRAPH.md) keeps graph traversal as **optional multi-hop reasoning** *after* CSV-backed ids are resolved — it is **not** mandatory in the agent ladder.

D-IH-18 deferred the question "should graph MCP tools (`hlk_graph_program_neighbours`, `hlk_graph_topic_dependency_path`, etc.) be promoted from optional to mandatory?" until UAT shows operator reliance. This template captures the trigger conditions.

## Why mandatory promotion is non-trivial

Promotion is not a one-line overlay edit. It changes **agent behaviour contract**:

- Today: agent answers cite CSV SSOT first; graph traversal is optional context.
- After promotion: agent must call graph tools whenever the question implies multi-hop traversal (e.g. "which topics depend on `topic_X`?"). The agent learns when to fall back to CSV scanning when graph is unavailable.
- Risk: inconsistent agent ladder behaviour during transition; degraded UX when Neo4j is unconfigured (today: agent silently falls through; after: agent surfaces "graph unavailable" warning).

Therefore the trigger is **operator UAT evidence of reliance**, not just "graph is cool to have".

## Triggers

Reopen the decision when **all three** conditions fire:

1. **Operator UAT shows reliance** — at least 5 dated UAT sessions where the operator's question explicitly required multi-hop graph traversal that CSV scanning could not resolve in <3 seconds. Captured in `docs/uat/hlk_admin_smoke.md` Scenario 8 (graph) or equivalent dated UAT report.
2. **Graph MCP tool stability** — `hlk_graph_*` MCP tools have been live for 30+ days with zero `Neo4j driver unavailable` failures attributable to the projection (transient network errors don't count); REST 503 fallback proven graceful in operator runbooks.
3. **Sync hygiene proven** — `py scripts/sync_hlk_neo4j.py --dry-run` produces byte-identical parity assertions across 3+ consecutive operator runs (i.e. canonical CSV → graph projection is deterministic).

## Trigger record (fill on activation)

```yaml
fired_on: <YYYY-MM-DD>
trigger_kind: graph_mandatory_promotion
detected_by: <role / person>
evidence:
  uat_sessions:
    - { date: <YYYY-MM-DD>, session: <link to docs/uat/* or wip/planning/*/reports/uat-*.md>, multi_hop_question: "..." }
    - <at least 5 entries>
  driver_stability:
    days_without_unattributable_failures: <integer ≥ 30>
    incident_log: <link if any>
  sync_determinism_runs:
    - { date: <YYYY-MM-DD>, output_sha256: <hex>, operator: <name> }
    - <at least 3 entries with matching sha256>
operator_approvals:
  - <AI Engineer | CTO | PMO>
proposed_overlay_edits:
  - prompts/overlays/OVERLAY_HLK_GRAPH.md: change "optional after CSV ids" -> "mandatory after CSV ids"
  - prompts/overlays/OVERLAY_HLK_*.md: peers reviewed for consistency
  - tests/test_madeira_interaction.py: add multi-hop graph reliance scenario
estimated_chunk_size: 1 day (overlay + tests + UAT scenario)
```

## Force-action checklist (do NOT skip steps)

- [ ] **All three triggers documented** above with cited evidence (5 UAT sessions, 30+ days stability, 3+ deterministic sync runs).
- [ ] **Overlay peer review**: every `OVERLAY_HLK_*.md` reviewed for consistency — graph promotion in one overlay must not contradict CSV-citation discipline in others.
- [ ] **CSV-citation discipline preserved**: agent answers still cite CSV SSOT for primary claims; graph traversal is the **multi-hop step**, not the SSOT replacement.
- [ ] **Allowlisted Cypher discipline preserved**: per Initiative 07 D2, no arbitrary Cypher injection from MCP tools; only the named `hlk_graph_*` helpers.
- [ ] **Fallback behaviour documented**: when Neo4j unconfigured, agent surfaces "graph unavailable, falling back to CSV scan" instead of silent degradation.
- [ ] **Test added** to `tests/test_madeira_interaction.py` (or peer) covering the new mandatory traversal scenario.
- [ ] **AI Engineer + CTO approval** in initiative `decision-log.md`.
- [ ] **Mark this template "FIRED + RESOLVED on `<YYYY-MM-DD>`"** with link to the closure PR.

## Cursor-rule guardrails (always-on)

Per [`OVERLAY_HLK_GRAPH.md`](../../../../prompts/overlays/OVERLAY_HLK_GRAPH.md) (current state, pre-promotion):

- Graph is **mirrored read index**, never authoritative over canonical CSVs (per `PRECEDENCE.md`).
- Citations in agent answers must reference CSV filenames, not Neo4j node ids.
- Graph tools are called **after** ids are resolved via `hlk_process` / `hlk_search` / `hlk_role`.

Per Initiative 07 [closure](../../07-hlk-neo4j-graph-projection/master-roadmap.md):

- Allowlisted Cypher only in `akos/hlk_neo4j.py`; no arbitrary query injection.
- Sync = full rebuild via `wipe=True`; no partial mutation.
- Graceful SKIP when `NEO4J_*` unconfigured (REST 503; MCP returns "Neo4j driver unavailable" JSON; CLI exits 2).

These invariants survive the promotion — the trigger only changes the **agent's call ordering**, not the projection contract.

## Cross-references

- [Initiative 26 master roadmap](../master-roadmap.md)
- [Initiative 26 decision log](../decision-log.md)
- [Wave-2 plan §"Decisions" D-IH-18](~/.cursor/plans/hlk_scalability_wave_2_initiatives_639a02d7.plan.md)
- [Initiative 07 master roadmap](../../07-hlk-neo4j-graph-projection/master-roadmap.md) — establishes the discipline this template would extend
- [`OVERLAY_HLK_GRAPH.md`](../../../../prompts/overlays/OVERLAY_HLK_GRAPH.md) — the file that would change on trigger fire
- [Initiative 23 P-graph](../../23-hlk-program-registry-and-program-2/master-roadmap.md) — the projection extension this would promote
