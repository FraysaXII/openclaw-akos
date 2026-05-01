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

# I46 P5 — Conditional GraphRAG ship (scaffold; activation operator-pending)

**Phase:** P5 (D-IH-46-E + D-IH-46-A operationalized: schema slot + policy template; activation conditional on P3 PoC outcome)
**Closes:** I46 P5 scaffold portion. Per-skill activation lands when operator runs the P3 PoC live + records the ship-or-no-ship verdict.
**Date:** 2026-05-01

## Actions

1. **`SKILL_REGISTRY.csv` extended with `retrieval_mode` column** (back-compat: empty default for all 5 existing rows):
   - `akos.hlk_skill_registry_csv.SKILL_REGISTRY_FIELDNAMES` extended (16 fields)
   - New `VALID_RETRIEVAL_MODES = {"", "vector_only", "graph_rag", "hybrid"}` enum
   - `scripts/validate_skill_registry.py` enforces the enum (rejects typos like "graphRAG", "rag", "knowledge_graph")
   - All 5 existing skills carry empty `retrieval_mode` (back-compat; current path)
   - SKILL-MADEIRA-LOOKUP-V1 notes column documents: "I46 P5 retrieval_mode: empty (operator activates 'graph_rag' if P3 PoC ships)"

2. **`POLICY_REGISTER.csv` extended with template row** `POL-NEO4J-GRAPH-RAG-ELIGIBILITY-TEMPLATE` (`policy_class=graph_rag_eligibility`):
   - **Template-only** (not policy-active until operator clones per topic_class with PoC numbers)
   - Default posture: NO topic_class is graph_rag-eligible until explicit per-class policy exists
   - Cross-references NEO4J_STRATEGY.md use-case B + the I46 P3 ship-or-no-ship decision

3. **Supabase migration** [`20260501070000_i46_skill_registry_retrieval_mode.sql`](../../../../supabase/migrations/20260501070000_i46_skill_registry_retrieval_mode.sql):
   - `ALTER TABLE compliance.skill_registry_mirror ADD COLUMN IF NOT EXISTS retrieval_mode TEXT`
   - Idempotent (`IF NOT EXISTS`); operator applies via `npx supabase db push`
   - Partial index on non-empty `retrieval_mode` for query efficiency
   - COMMENT ON COLUMN documents the enum + activation policy

4. **`akos/eval_harness.py` legacy-deletion staged**: the file was removed when I45 P1 converted the module to a package (`akos/eval_harness/__init__.py`). The deletion was on the filesystem but the index hadn't tracked it. P5 commit picks it up.

5. **12 new tests** in `tests/test_neo4j_retrieval_mode.py`:
   - Schema extension (2 tests): SKILL_REGISTRY_FIELDNAMES + VALID_RETRIEVAL_MODES enum
   - CSV column present (2 tests): header has retrieval_mode + all 5 rows valid enum value
   - Validator (2 tests): live CSV passes validator + enum rejects typos
   - POLICY_REGISTER template (2 tests): template row exists with correct policy_id + class enum updated
   - Supabase migration (3 tests): file exists + ALTER TABLE present + partial index present
   - Cross-coupling with I45 P3 (1 test): both `routing_condition` and `retrieval_mode` columns coexist; correct field order

## Verification

- `py scripts/validate_skill_registry.py`: PASS (5 rows; new column accepts empty default)
- `py scripts/validate_policy_register.py`: PASS (template row's `policy_class=graph_rag_eligibility` recognized via I45 P4 enum extension)
- `py scripts/validate_hlk.py`: PASS (full vault unchanged)
- Regression check across 5 suites (`tests/test_skill_registry.py`, `test_skill_router.py`, `test_neo4j_usecase_a_hardening.py`, `test_neo4j_retrieval_mode.py`, `test_policy_register.py`): **75/75 PASS** in 10.1s
- `tests/test_neo4j_retrieval_mode.py` standalone: **12/12 PASS** in 0.4s

## What this does NOT do (operator-pending)

- **No skill activated yet** — all 5 skills carry empty `retrieval_mode`. Activation flow:
  1. Operator runs P3 PoC live (`AKOS_GRAPHRAG_POC_LIVE=1 py scripts/graphrag_poc.py`)
  2. PoC emits `reports/graphrag-poc-results-YYYY-MM-DD.md` with A/B numbers
  3. Operator records ship/no-ship in I46 decision-log as `D-IH-46-Decision-P3-2026-MM-DD`
  4. **If ship**: operator edits SKILL-MADEIRA-LOOKUP-V1 row to `retrieval_mode=graph_rag`, clones the POLICY_REGISTER template into a per-topic-class row (e.g., `POL-NEO4J-GRAPH-RAG-ELIGIBILITY-TOPIC-MADEIRA-LOOKUP`), and applies via `sync_compliance_mirrors_from_csv.py --skill-only --policy-only`
  5. **If no-ship**: operator records the decision-not-to-ship with PoC numbers; column stays empty across all skills

- **No router-side wiring** for `retrieval_mode` yet — when activated, `akos/skill_router.py` (I45 P3) needs an extension that respects `retrieval_mode`. That extension lands as a P5 follow-up commit when the first skill activates.

## Operator-applied steps

1. **Apply migration**: `npx supabase db push` (lands `retrieval_mode` column on `compliance.skill_registry_mirror`)
2. **Reseed POLICY_REGISTER mirror**: `py scripts/sync_compliance_mirrors_from_csv.py --policy-only` (picks up the new TEMPLATE row)
3. **Reseed SKILL_REGISTRY mirror**: `py scripts/sync_compliance_mirrors_from_csv.py --skill-only` (re-upserts the 5 rows with the new column = empty)
4. **Run P3 PoC live** when ready (cost-gated; see P3 phase report)

## Decision log entry to add when P3 PoC completes

```
- D-IH-46-Decision-P3-2026-MM-DD: GraphRAG PoC outcome
  Bar evaluated: any of (>=3pp accuracy lift / >=30% latency reduction /
                          >=40% cost reduction) on 20 golden queries
  Result: <PASS|FAIL>
  Numbers: <accuracy A% vs B%; latency Ams vs Bms; cost A$ vs B$>
  Verdict: <SHIP for SKILL-MADEIRA-LOOKUP-V1 | NO-SHIP; column stays empty>
  Decided by: <operator>
  Decided at: 2026-MM-DD
```

## Next phase

P6 — Test wiring. GraphRAG cassettes via I45 P2 recorder (probe_kind extension `graph_rag_query`); adversarial probes for graph escape (queries that should NOT route via graph); Neo4j health canary added to WIP_DASHBOARD.
