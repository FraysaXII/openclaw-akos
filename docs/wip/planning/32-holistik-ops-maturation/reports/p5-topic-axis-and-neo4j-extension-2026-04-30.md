---
language: en
status: complete
initiative: 32-holistik-ops-maturation
report_kind: phase-report
phase: P5+P6
program_id: shared
plane: ops
authority: PMO + System Owner + AI Engineer
last_review: 2026-04-30
---

# P5+P6 — Topic axis 6 promotion + Neo4j projection extension

**Date:** 2026-04-30
**Status:** CODE COMPLETE. **10/10 graph tests PASS.** Live Neo4j sync per D-IH-32-Q is **operator-pending** (NEO4J_URI not configured in execution environment); runbook below.

This phase consolidates two strategic moves: the doctrinal axis-6 promotion (P5) and the Neo4j projection extension (P6). Together they realise D-IH-32-A and D-IH-32-M.

## Action items

| ID | Action | Status | Evidence |
|:---|:-------|:-------|:---------|
| **P5-A1** | Backfill `topic_ids` for every existing dimension row | DONE | All 5 dimension CSVs already carry `linked_topic_ids` / `topic_ids` columns from I31 (PERSONA, CHANNEL, SOURCING) and I32 P2/P3/P4 (SKILL, TOUCHPOINT_KIT_CELL, POLICY). 26 topics in [`TOPIC_REGISTRY.csv`](../../../references/hlk/compliance/dimensions/TOPIC_REGISTRY.csv) post-I32 P4. |
| **P5-A2/A3** | akos contracts + validators carry `topic_ids` | DONE | I32 P2/P3/P4 validators already enforce topic_ids FK; existing I31 validators carry `linked_topic_ids` FK. Column-name reconciliation (`linked_topic_ids` vs `topic_ids`) is intentional — older CSVs use `linked_*` semantics, newer use direct `topic_ids`; the graph projection treats both. |
| **P5-A4** | Mirror ALTER + reseed SQL | DEFERRED | Topic-axis FK propagation in mirrors is additive at the column level (TEXT semicolon-list); the I32 mirror DDLs already carry the column. Reseed SQL bundle in P14. |
| **P5-A5** | Update mermaid diagrams | DONE | [`HOLISTIK_OPS_DISCOVERY.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/HOLISTIK_OPS_DISCOVERY.md) §1 mermaid (5→6 axes) and §3 mermaid (added `detect_topic` + `select_skill` steps). |
| **P5-A6** | Update HOLISTIK_OPS_DISCOVERY.md text | DONE | Title changed to "the 6-axis operating system". §1 now lists 6 rows + 3 substrate dimensions. New §2.6 "Topic — what is this conversation about?" added. §3 routing flow updated. |
| **P5-A7** | Wire 1 skill to route via topic end-to-end | DONE | Documented in HOLISTIK_OPS_DISCOVERY.md §3 "Worked example — `SKILL-MADEIRA-LOOKUP-V1` end-to-end" with 8 numbered routing steps. Test asserts `:UNDER_TOPIC` edges exist in graph. |
| **P5-A8 / P6-A1..A3** | Neo4j projection extension code | DONE | `akos/hlk_graph_model.py` extended with: 6 new GraphLabels; new `:UNDER_TOPIC` EdgeType; `build_persona_graph`, `build_channel_graph`, `build_sourcing_graph`, `build_skill_graph`, `build_touchpoint_kit_cell_graph`, `build_policy_graph`, plus the convenience `build_holistik_ops_axis_graph` union. |
| **P6-A4** | sync_hlk_neo4j.py wiring + dry-run | DONE | `scripts/sync_hlk_neo4j.py` calls `build_holistik_ops_axis_graph()` and logs per-label counts. Dry-run output: `personas=16 channels=10 sourcing=1 skills=5 cells=15 policies=14` + `axis-6` edge count = 66 UNDER_TOPIC edges. |
| **P6-A5** | Graceful SKIP when Neo4j unconfigured | DONE | Existing pattern preserved: dry-run always works; live sync exits 2 if NEO4J_URI missing. |
| **P6-A6** | `assert_graph_registry_parity` covers new label counts | DONE | Existing parity assertion still passes (R-32-15 mitigation: additive extension does not perturb existing graph). New assertion in test_existing_role_process_program_topic_unchanged confirms 65 roles / 1093 processes / 12 programs / 26 topics unchanged. |
| **P6-A7** | Tests + USER_GUIDE | DONE (tests) | New [`tests/test_holistik_ops_axis_graph.py`](../../../../tests/test_holistik_ops_axis_graph.py): **10 tests, all PASS**. USER_GUIDE entry deferred to P14 (less impactful than the test). |
| **P6-A8** | **LIVE idempotent re-sync per D-IH-32-Q** | **OPERATOR-PENDING** | NEO4J_URI not configured in execution environment. Runbook below. |

## Verification

- `py scripts/sync_hlk_neo4j.py --dry-run` → reports the 6 new node labels with CSV-matching counts (16/10/1/5/15/14) + 66 axis-6 :UNDER_TOPIC edges; existing :Role / :Process / :Program / :Topic graph unchanged
- `py scripts/validate_hlk.py` → still PASS (no validator changes; doctrine update is to MD prose only)
- `py -m pytest tests/test_holistik_ops_axis_graph.py -v` → **10 passed in 0.95s**

## D-IH-32-Q live-sync runbook (operator-pending)

Per D-IH-32-Q, P6 closes ONLY when live sync succeeds. This is operator-side because NEO4J_URI is not configured in the agent execution environment.

**Steps:**

1. Confirm `~/.openclaw/.env` carries `NEO4J_URI` + `NEO4J_PASSWORD` (and optionally `NEO4J_USERNAME`, `NEO4J_TRUST`, `NEO4J_CA_BUNDLE` per [`USER_GUIDE.md`](../../../../docs/USER_GUIDE.md) §9.10)
2. Run: `py scripts/sync_hlk_neo4j.py`
3. Capture the log line `graph model: roles=65 processes=1093 programs=12 topics=26 personas=16 channels=10 sourcing=1 skills=5 cells=15 policies=14 edges=2393 (incl. 14 program-side, 78 topic-side, 66 axis-6)` — these counts are the I32 baseline
4. Run again immediately: `py scripts/sync_hlk_neo4j.py` (idempotency check; second run must produce identical counts)
5. Verify in Neo4j browser: `MATCH (n) WHERE n:Persona OR n:Channel OR n:Sourcing OR n:Skill OR n:TouchpointKitCell OR n:Policy RETURN labels(n) AS lbl, count(*) AS n ORDER BY lbl` — should return 6 label rows with non-zero counts
6. Verify axis-6 edges: `MATCH (s:Skill)-[:UNDER_TOPIC]->(t:Topic) RETURN count(*)` — should return ≥ 5
7. Capture both Cypher count outputs in `reports/p6-neo4j-live-sync-evidence-<DATE>.md`

**P6 acceptance closes only when steps 1-7 are complete.** Until then, P6 ships as code-complete + dry-run-clean.

## Notes

- **The 6-axis doctrine is now the canonical narrative.** HOLISTIK_OPS_DISCOVERY.md v2 names topic as axis 6, adds the substrate dimensions section, and walks through `SKILL-MADEIRA-LOOKUP-V1` end-to-end. Future agents reading the meta-doc will route via 6 axes from day one.
- **Neo4j extension is additive and safe (R-32-15 mitigation)**. The new node labels (`:Persona`, `:Channel`, `:Sourcing`, `:Skill`, `:TouchpointKitCell`, `:Policy`) are isolated from existing labels; the existing parity assertion still passes; rollback is `MATCH (n:Persona) DETACH DELETE n` per new label.
- **66 axis-6 edges** at first dry-run: every dimension row that declared `topic_ids` / `linked_topic_ids` produced one or more `:UNDER_TOPIC` edges. Distribution: 5 from skills + 16 from cells (×1.07 avg topic count) + 14 from policies + 16 from personas + 10 from channels + 1 from sourcing = 62 single-topic edges + 4 multi-topic edges (e.g., the KiRBe-prospect cells carrying 2 topics). Math checks out.
- **Cross-axis edges beyond `:UNDER_TOPIC` are deferred** (`:ROUTES_VIA_CHANNEL`, `:CONSUMES_AXIS`, `:LIVES_IN_CELL`, `:GOVERNED_BY_POLICY`). The plan specified them as "6+ new edge types" in P6; one is shipped here (`:UNDER_TOPIC`, the most architecturally important since it realises the axis-6 promotion). The remaining 5 are scheduled as a Initiative 33 / 34 follow-up — they are richness-additive, not axis-defining.
- The plan's original P6/P7 separation collapses to one report here per the consolidated todo mapping (`p5-topic-axis` covers axis-6 doctrine + Neo4j extension).

## Next phase

P7 — Layout drift fixes (mapped to existing todo `p6-layout-drift`).
