---
language: en
status: active
intellectual_kind: phase_report
role_owner: System Owner
area: Tech / Holistik Ops
entity: Holistika Research
authority: Founder + System Owner
last_review: 2026-05-01
artifact_role: governed_evidence
topic_ids:
  - topic_holistik_ops_discovery
parent_topic: topic_holistik_ops_discovery
---

# I46 P2 — Use-case A hardening

**Phase:** P2 (governance KG hardening: skill traversal MCP + drift canary + idempotency contract)
**Closes:** I46 P2 + evidence-matrix E3 (axis-6 dimensions have no MCP traversal) + E11 (no drift canary).
**Date:** 2026-05-01

## Actions

1. **New helper** `akos.hlk_neo4j.skill_neighbourhood(session, skill_id, depth, limit)`:
   - Returns `:Skill` + connected `:Topic` (via `:UNDER_TOPIC`) + `:Role` owner (via `:OWNED_BY`)
   - At depth>=2: sibling skills under shared topics
   - Bounded depth [1,3] + limit [1,200]
   - Does NOT expand into POLICY_REGISTER (R-46-7 mitigation; `--include-policies` flag reserved for future)

2. **New MCP tool** `hlk_graph_skill_neighbourhood` registered in `scripts/hlk_graph_mcp_server.py`:
   - First axis-6 traversal surface (skills/cells/policies/personas/channels/sourcing all projected since I32 P5/P6 but only Process + Role have had MCP tools)
   - Same auth/precheck pattern as the 3 existing tools

3. **`config/agent-capabilities.json` updated**: `madeira` role allowlists `hlk_graph_skill_neighbourhood` (joins the existing `hlk_graph_*` 3 tools).

4. **New drift canary** `scripts/graphrag_drift_canary.py`:
   - Compares Neo4j label counts to canonical CSV row counts across all 10 dimensions
   - Tolerance: 1 row deviation per dimension (allows for in-flight syncs)
   - 3 modes: default (Neo4j live), `--csv-only` (skip Neo4j; print CSV summary), `--json` (machine-readable)
   - SKIPs gracefully when Neo4j not configured
   - On drift: exit 1 + per-dimension diff + suggested remediation (`py scripts/sync_hlk_neo4j.py`)

5. **New verification profile** `neo4j_governance_kg_drift_smoke` in `verification-profiles.json`:
   - 1 step: `scripts/graphrag_drift_canary.py`
   - Suitable for nightly cron / pre_commit (when Neo4j configured) — operator decides

6. **10 new tests** in `tests/test_neo4j_usecase_a_hardening.py`:
   - Drift canary (4 tests): CSV-only mode lists all 10 dimensions; SKILL count = 5; SKIP when Neo4j unconfigured; csv_row_count helper unit test
   - skill_neighbourhood helper (3 tests): not_found minimal response shape; depth clamping when found; bounded params
   - MCP tool registration (1 test): import + decorator + function definition present
   - agent-capabilities.json (1 test): madeira allowlist includes the new tool
   - Verification profile (1 test): registered with right step

## Verification

- `py scripts/graphrag_drift_canary.py --csv-only`: lists all 10 dimensions with current row counts (Skill=5, Process=1093, Role=65, Topic=27, Persona=16, Channel=10, Sourcing=1, TouchpointKitCell=15, Policy=21, Program=12).
- `py scripts/graphrag_drift_canary.py` (without Neo4j env): SKIP with explicit reason; exit 0.
- `py scripts/validate_hlk.py`: PASS (152 files; doctrine page from P1 stays green).
- `tests/test_neo4j_usecase_a_hardening.py`: **10/10 PASS** in 0.9s.

## What this does NOT do (deferred)

- **No live Neo4j sync recurring contract** added to release-gate yet — operator can wire by adding `scripts/sync_hlk_neo4j.py` to the release-gate steps + a "must produce identical output 2x" wrapper. The doctrine in P1 documents the idempotency proof from D-IH-32-Q; the recurring contract is operator-scheduled.
- **No similar MCP tools for the other 5 axis-6 dimensions** (Persona / Channel / Sourcing / TouchpointKitCell / Policy) — each could follow the same `*_neighbourhood` pattern when an agent need surfaces. Skill is the highest-traffic axis-6 dimension (5 skill-shaped agent contracts).

## Operator-applied steps

1. **Apply drift canary to nightly cron** (optional): add a row to `config/verification-profiles.json` `pre_commit` profile, OR add a separate GitHub Action that runs `py scripts/graphrag_drift_canary.py` daily.
2. **Idempotency recurring contract** (optional): wrap `scripts/sync_hlk_neo4j.py` in `release-gate.py` with a "run 2x; assert identical output" check, mirroring the D-IH-32-Q proof pattern.

## Next phase

P3 — Use-case B PoC. 1-week LightRAG-style hybrid via `neo4j-graphrag-python`. A/B for `SKILL-MADEIRA-LOOKUP-V1` against 20 golden vault queries. Cost-capped per R-46-1 (`GRAPHRAG_POC_USD_CEILING=$20`).
