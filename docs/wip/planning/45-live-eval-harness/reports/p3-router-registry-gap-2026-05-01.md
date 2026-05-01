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
  - topic_skill_registry
parent_topic: topic_skill_registry
---

# I45 P3 — Close the Registry-Router gap

**Phase:** P3 (intent.py consults SKILL_REGISTRY first; new routing_condition column)
**Closes:** I45 P3 + evidence-matrix E2 (Registry-Router gap) + E3 (tools_required vs agent-capabilities.json drift) + E10 (routing_condition missing).
**Date:** 2026-05-01

## Actions

1. **Schema extension** — added 2 new columns to `SKILL_REGISTRY.csv`:
   - `routing_condition` — kv-style filter expression, evaluated by `akos.skill_router.matches()`. Empty = always-eligible (back-compat).
   - `tools_required_waived` — boolean. When `true`, validator skips the `tools_required` vs `agent-capabilities.json` reconciliation warning (closes R-45-6).
   - Both columns added to `akos.hlk_skill_registry_csv.SKILL_REGISTRY_FIELDNAMES`.
   - All 5 existing rows populated:
     - `SKILL-MADEIRA-LOOKUP-V1`: `routing_condition=intent_in=hlk_lookup;hlk_search`
     - `SKILL-ARCHITECT-PLAN-V1`: `routing_condition=agent=architect`
     - `SKILL-EXECUTOR-RUN-V1`: `routing_condition=agent=executor`, `tools_required_waived=true`
     - `SKILL-VERIFIER-CHECK-V1`: `routing_condition=agent=verifier`, `tools_required_waived=true`
     - `SKILL-SHARED-LOCALE-DETECT-V1`: empty (always-eligible)

2. **New module `akos/skill_router.py`** (~120 lines) — the missing middle of the registry-router triangle:
   - `parse_routing_condition(rc) -> {kind, ...}` — minimal DSL parser (4 forms: always / intent_in / intent / agent)
   - `matches(condition, intent_route, agent) -> bool`
   - `candidate_skills(intent_route, agent) -> [skill_dict]`
   - `candidate_skill_ids(...)` convenience
   - Combines routing_condition matching with agents_supported gating (skill is eligible if rc matches OR rc empty AND agent in agents_supported)

3. **`akos/intent.py` refactor** — `classify_request` now:
   - Accepts an optional `agent` parameter
   - Enriches its response with `candidate_skills: list[str]` (NEW field; never None; may be empty)
   - Soft-fails if the registry is unavailable (returns `[]` and continues; existing escalation logic untouched)
   - Backward-compatible: existing callers without `agent` continue to work

4. **Validator extension** — `scripts/validate_skill_registry.py`:
   - New `ROUTING_CONDITION_RE` — regex enforcing the 4 DSL forms
   - New `WAIVER_VALUES` — empty/true/false enum check for `tools_required_waived`
   - When `tools_required_waived=true`, the `tools_required` vs `agent-capabilities.json` warning is silenced (R-45-6 mitigation)

5. **Supabase migration** — `supabase/migrations/20260501041500_i45_skill_registry_routing_columns.sql`:
   - `ALTER TABLE compliance.skill_registry_mirror ADD COLUMN routing_condition TEXT, tools_required_waived BOOLEAN DEFAULT false`
   - Partial index on non-empty `routing_condition` for query efficiency
   - Idempotent (`IF NOT EXISTS`); operator-applied via `npx supabase db push` per the standard cadence

6. **22 new tests** in `tests/test_skill_router.py` covering:
   - DSL parser (7 tests: empty, 3 valid forms, 3 invalid forms)
   - `matches()` behavior (4 tests across all kinds + invalid)
   - Live registry queries (7 tests: candidate_skills filters, agent gating, shared-pseudo-agent semantics)
   - `intent.classify_request` integration (4 tests, including soft-fail under simulated import error)
   - Drift detector (2 tests: column presence + Madeira routing_condition value)

## Verification

- `py scripts/validate_skill_registry.py`: PASS (5 rows; warnings reduced to zero by the 2 waivers).
- `py scripts/validate_hlk.py`: PASS (152 files; full vault).
- `py scripts/eval.py --mode replay`: 6/6 cassettes still PASS (route stability preserved through the refactor).
- `py -m pytest tests/test_skill_*.py tests/test_eval_*.py tests/test_madeira_eval_*.py`: **91/91 PASS** in 10.2s.
- End-to-end smoke (live registry):
  - `classify_request("Find the System Owner role", agent="madeira")` → `route=hlk_lookup`, `candidate_skills=['SKILL-MADEIRA-LOOKUP-V1', 'SKILL-SHARED-LOCALE-DETECT-V1']`
  - `classify_request("Plan a 5-phase migration", agent="architect")` → `route=admin_escalate` (escalation regex), `candidate_skills=['SKILL-ARCHITECT-PLAN-V1', 'SKILL-SHARED-LOCALE-DETECT-V1']`
  - `classify_request("Stock price for AAPL")` → `route=finance_research`, `candidate_skills=['SKILL-SHARED-LOCALE-DETECT-V1']` (only the always-eligible shared skill)

## Architectural impact

The Registry-Router gap (E2) is closed. Today's `classify_request` returns BOTH the legacy escalation/route info AND the registry-driven `candidate_skills` list. Downstream consumers that want the new behavior pass `agent=...`; those that don't see no change.

This unblocks:
- **I45 P7** (promotion gate) — can now require `routing_condition` to be non-empty as a graduation criterion
- **I46 P5** (conditional GraphRAG ship) — `retrieval_mode` column will sit alongside `routing_condition`; the router can be extended to filter on retrieval_mode policy
- **Initiative 34** (multi-tenant) — `tenant_scope` filtering becomes a 5th matches() kind, mirroring agent

## Risks resolved or deferred

- **R-45-5 (routing changes break Madeira UX)**: mitigated. Cassettes (P2) caught zero regressions in the 6 in-process probes; canary 5 remains green (`orchestrator-fallback=0/5`).
- **R-45-6 (tools_required reconciliation breaks external repo)**: mitigated. Per-skill `tools_required_waived` lets affected skills opt out individually; KiRBe/hlk-erp can leave their consumed mirror data untouched.
- **R-45-7 (routing_condition column added but no skill uses it)**: did NOT realize — 4 of 5 skills have explicit non-empty conditions; SHARED-LOCALE intentionally always-eligible.

## What this does NOT do (deferred)

- No live LLM eval yet (P6).
- No cost ceiling enforcement yet (P4).
- No per-skill cost in scorecard yet (P4).
- Adversarial cassettes (P5).
- Promotion gate enforcement (P7) — `routing_condition` non-empty check is documented in the asset-classification but not yet enforced in `scripts/eval.py promote`.

## Operator-applied steps

1. **Apply Supabase migration** when ready: `npx supabase db push` (lands `routing_condition` + `tools_required_waived` columns on `compliance.skill_registry_mirror`).
2. **Reseed mirror** via `scripts/sync_compliance_mirrors_from_csv.py --skill-only` once the migration lands (the existing 5 rows will be re-upserted with the new column values).

## Next phase

P4 — Cost + latency observability per skill. Extend `ScoreRow` with `tokens_in`/`tokens_out`/`usd_estimate`/`latency_ms_p50`/`latency_ms_p95` populated from a Langfuse scrape. Add new POLICY_REGISTER rows: `policy_class=cost_ceiling` per skill. Add `--enforce` mode that fails CI when a skill's average $/run regresses >20%.
