---
language: en
status: complete
initiative: 32-holistik-ops-maturation
report_kind: phase-report
phase: P2
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-04-30
---

# P2 — Skill registry (7th canonical dimension)

**Date:** 2026-04-30
**Status:** COMPLETED. Topic registry now at 24. 14 P2 tests + 14 P1 dispatcher regression tests = **28/28 PASS**.

## Action items

| ID | Action | Status | Evidence |
|:---|:-------|:-------|:---------|
| **P2-A1** | Schema + akos contract | DONE | [`akos/hlk_skill_registry_csv.py`](../../../../akos/hlk_skill_registry_csv.py): 14-field tuple, `VALID_AXES` (6), `VALID_LIFECYCLE_STATUSES` (3), `KNOWN_AGENT_IDS` (5), `SHARED_AGENT_ID` constant. |
| **P2-A2** | Validator with FK + tenant_scope rules | DONE | [`scripts/validate_skill_registry.py`](../../../../scripts/validate_skill_registry.py): 14-field header check, `^SKILL-[A-Z0-9-]{4,80}-V\d+$` regex, semver, agent FK, axes enum, owner_role FK to baseline_organisation, topic_ids FK, **tenant_scope `^shared$` enforced per D-IH-32-J**, lifecycle enum, eval_baseline_pct in [0, 100]. |
| **P2-A3** | Mirror DDL + RLS | DONE (staged) | [`supabase/migrations/20260430233100_i32_skill_registry_mirror.sql`](../../../../supabase/migrations/20260430233100_i32_skill_registry_mirror.sql): same pattern as `compliance.persona_registry_mirror`. PK `skill_id`; 4 indexes; RLS deny anon + authenticated; service_role only. |
| **P2-A4** | 5 seed rows | DONE | [`SKILL_REGISTRY.csv`](../../../references/hlk/compliance/dimensions/SKILL_REGISTRY.csv): SKILL-MADEIRA-LOOKUP-V1, SKILL-ARCHITECT-PLAN-V1, SKILL-EXECUTOR-RUN-V1, SKILL-VERIFIER-CHECK-V1, SKILL-SHARED-LOCALE-DETECT-V1. Each row covers one of the 5 documented agents (madeira / architect / executor / verifier / shared). |
| **P2-A5** | topic_skill_registry row | DONE | Row added to [`TOPIC_REGISTRY.csv`](../../../references/hlk/compliance/dimensions/TOPIC_REGISTRY.csv); registry now at **24 rows** (was 23). |
| **P2-A6** | Sync emit support | DEFERRED | `scripts/sync_compliance_mirrors_from_csv.py --skill-registry-only` flag will land alongside the operator-side mirror reseed bundle in P14 (the upsert SQL). Not blocking; mirror DDL is staged. |
| **P2-A7** | Tests | DONE | New [`tests/test_skill_registry.py`](../../../../tests/test_skill_registry.py): 14 tests, all PASS. Locks header, seed cardinality (≥5), skill_id format + uniqueness, agent coverage of all 5 documented agents, axes enum, **D-IH-32-J tenant_scope assertion**, eval_baseline parse, owner_role FK, topic_ids FK, topic_skill_registry row presence, validator script exit, dispatcher integration. |

## Verification

- `py scripts/validate_skill_registry.py` → PASS at 5 rows
- `py scripts/validate_topic_registry.py` → PASS at 24 rows
- `py scripts/validate_hlk.py` → still PASS (legacy CLI behaviour preserved); now includes "SKILL_REGISTRY: PASS" in dispatch output
- `py -m pytest tests/test_skill_registry.py tests/test_validate_hlk_dispatcher.py -v` → **28 passed in 7.97s**

## Notes

- **MADEIRA-SaaS substrate is in place.** The 5 seed rows + tenant-aware schema + lazy-load contract collectively are exactly what `MADEIRA_PLATFORM.md` `TODO[OPERATOR-madeira-saas-window]` needs (skills as versioned, governed, tenant-aware assets). Initiative 34 will open `tenant_scope` regex when the founder commits to a productisation window.
- **Lazy-load pattern (D-IH-32-I) honoured**: `description` field is the cheap-load 1-2 sentence summary. Full skill bodies live in each agent's existing `IDENTITY.md` plus a future per-skill body file (out of I32 scope; defer to first KiRBe SaaS customer needing it).
- **`tools_required` includes Cursor agent tool names** (`Shell`, `Read`, `Write`) for executor/verifier rows; the validator does NOT fail on these (they govern the Cursor runtime, not the openclaw runtime tools in `agent-capabilities.json`). Warnings only on `agent-capabilities.json` mismatches; errors on agent-id and axes-enum mismatches.
- **Topic-axis propagation hook**: every seed row already carries `topic_skill_registry` in its `topic_ids` column. P5 will extend this to per-skill topic specialisation when the topic axis 6 propagation lands.
- Dispatcher unchanged in shape: SKILL_REGISTRY appended to the dispatch table at line ~268 of refactored `validate_hlk.py` (1-line addition).

## Next phase

P3 — Touchpoint-kit cell registry (the FS-vs-CSV drift detector is the keystone test).
