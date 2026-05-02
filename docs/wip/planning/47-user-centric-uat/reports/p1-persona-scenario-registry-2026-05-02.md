---
language: en
status: active
initiative: 47-user-centric-uat
report_kind: phase-report
phase: P1
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-05-02
---

# I47 P1 — PERSONA_SCENARIO_REGISTRY schema landed

## What shipped

- `akos/hlk_persona_scenario_csv.py` — field contract with 16-column header (5 typed dimensions per scenario taxonomy + tenant_id per D-IH-47-K) and 5 valid-enum sets
- `docs/references/hlk/compliance/dimensions/PERSONA_SCENARIO_REGISTRY.csv` — header + 1 scaffold row anchored on OPERATOR pseudo-persona (full library lands P2-P9)
- `scripts/validate_persona_scenario_registry.py` — header check + scenario_id regex + uniqueness + FK to PERSONA_REGISTRY (or OPERATOR pseudo) + FK to SKILL_REGISTRY + enum enforcement on tier/scenario_class/difficulty_class/expected_route/expected_outcome_class/language/lifecycle_status + topic_ids FK + non-empty prompt_text
- Wired into `scripts/validate_hlk.py` dispatcher (after REPO_HEALTH_SNAPSHOT)
- New TOPIC_REGISTRY row `topic_persona_scenario_registry` (28 topics now)
- `supabase/migrations/20260502033000_i47_persona_scenario_registry_mirror.sql` — DDL with `(persona_id, tenant_id)` composite index + partial index on non-NULL tenant_id (D-IH-47-K I34-prep) + RLS deny-anon/auth + service_role-only grant
- Migration applied to MasterData via `npx supabase db push --linked`
- 21 new tests in `tests/test_persona_scenario_registry.py` covering field contract, intent literal sync, validator behavior on bad scenario_id, OPERATOR pseudo-persona acceptance, NULL tenant_id acceptance, migration shape (column presence + composite index + partial index + RLS), dispatcher integration, and end-to-end `validate_hlk` PASS

## Verification

- `py scripts/validate_persona_scenario_registry.py` → PASS (1 row, 1 scenario, 1 persona, difficulty `{trivial: 1}`)
- `py scripts/validate_hlk.py` → OVERALL PASS; new line `PERSONA_SCENARIO_REGISTRY: PASS`
- `py -m pytest tests/test_persona_scenario_registry.py` → 21 / 21 PASS
- Supabase migration push → applied (1 NOTICE for already-existing schema; expected)

## Risks closed / opened

- R-47-12 (tenant_id NULL handling) mitigation surface deployed: column nullable; partial index on non-NULL only; validator accepts both NULL and string
- No new risks; P1 schema is the foundation for P2-P15

## Cross-references

- D-IH-47-A (PERSONA_SCENARIO_REGISTRY.csv as canonical SSOT)
- D-IH-47-K (tenant_id NULL-default joint-axis prep)
- I31 P2 (PERSONA_REGISTRY.csv FK source)
- I32 P2 (SKILL_REGISTRY.csv FK source; same governance pattern)
- I47 P0 scenario-taxonomy.md (5 typed dimensions origin)
