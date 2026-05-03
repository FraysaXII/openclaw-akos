---
language: en
initiative: 51-persona-calibration-cleanup
phase: P1
report_kind: phase-report
status: completed
date: 2026-05-03
authority: Founder
last_review: 2026-05-03
closes: [OPS-47-9]
---

# I51 / P1 — Mirror reseed (closes OPS-47-9)

**Phase scope:** add a `_emit_persona_scenario_registry_upserts()` emitter to
`scripts/sync_compliance_mirrors_from_csv.py`, expose a
`--persona-scenario-registry-only` CLI mode, wire the count-only +
bundled-emit pathways, and verify CSV row-count parity with the SQL output.

**Phase non-scope:** the actual `service_role` apply (operator gate; this phase
ships the SQL emitter, not a Supabase mutation). I51/P2 calibration audit and
I51/P3 rebalance run **after** the operator applies this SQL via
`mcp_supabase_apply_migration` against the staging mirror, but the gate stays
on the operator side. CSV authority is unchanged: PERSONA_SCENARIO_REGISTRY.csv
remains the SSOT and the mirror is a queryable projection.

## Carrier closed

**OPS-47-9** — `compliance.persona_scenario_registry_mirror` was created at I47
P1 (`supabase/migrations/20260502033000_i47_persona_scenario_registry_mirror.sql`)
and extended at I49 with the `priority_score` / `safety_lane` /
`release_blocking` columns
(`supabase/migrations/20260503120000_i49_persona_scenario_registry_priority_columns.sql`),
but the CSV-to-mirror reseeder was never wired up. As of I51/P1 the emitter is
in place and tested.

## Deliverables

1. **Emitter** — `_emit_persona_scenario_registry_upserts()` in
   `scripts/sync_compliance_mirrors_from_csv.py`:
   - Same DAMA-pure projection shape as `_emit_persona_registry_upserts()`.
   - Honours D-IH-47-K shared-scenario semantics: empty `tenant_id` is emitted
     as `NULL` (not `''`), preserving the "shared scenario applies to all
     tenants" default carried in the I47 DDL comment.
   - Semicolon-list columns (`expected_keywords`, `forbidden_keywords`,
     `topic_ids`) are stored verbatim as TEXT — same convention as the rest of
     the I32 mirror cohort.
2. **CLI surface** — `--persona-scenario-registry-only` flag:
   - Exposed in argparse and the mode-flag mutex check.
   - Branch reads CSV with header-drift validation against
     `PERSONA_SCENARIO_REGISTRY_FIELDNAMES` (19 columns; I47 + I49).
   - `--count-only` returns `persona_scenario_registry_rows=N`.
   - `--no-begin-commit` mode emits the bare INSERT...ON CONFLICT statements
     for splicing into operator-curated SQL, mirroring sibling mirrors.
3. **Bundled emit** — full-bundle path now reads
   `PERSONA_SCENARIO_REGISTRY.csv`, increments `persona_scenario_registry_rows`
   in `--count-only` output, and includes the upsert block in the bundled
   output (provided `--process-list-only` / `--baseline-only` are not set).
4. **Tests** — `tests/test_sync_compliance_mirrors_from_csv.py`:
   - Updated `test_sync_compliance_mirrors_count_only` to assert
     `persona_scenario_registry_rows=329`.
   - Updated `test_sync_full_emit_includes_counterparty_upserts` to assert
     the persona-scenario mirror upserts are present in the bundled output.
   - New `test_sync_persona_scenario_registry_only_sql` test covering:
     header anchoring (`SCN-OP-001-V1`), telemetry-promoted scaffold
     anchoring (`SCN-OP-TP-001-V1`; I50 P5 lineage), `tenant_id NULL` emission,
     and exact 329-row count parity with the CSV.

## CSV ↔ mirror parity

| Source | Row count |
|--------|----------:|
| `PERSONA_SCENARIO_REGISTRY.csv` (header-anchored) | 329 |
| `--count-only` `persona_scenario_registry_rows=` | 329 |
| `--persona-scenario-registry-only` emitted INSERTs | 329 |

Parity confirmed across all three signals. The `--count-only` output is the
authoritative line for operator-side parity checks; the `INSERT` count in the
emitted SQL is the wire-level confirmation.

## Verification

```text
$ py scripts/sync_compliance_mirrors_from_csv.py --persona-scenario-registry-only --count-only
source_git_sha=166e8c7546bcc5ba6bf49275ea005b7e8341947c
persona_scenario_registry_rows=329

$ py -m pytest tests/test_sync_compliance_mirrors_from_csv.py -v
... 5 passed in 1.13s
```

## Operator handoff

The SQL is operator-applied — this phase **does not** trigger
`mcp_supabase_apply_migration`. To apply the reseed against the staging mirror:

```text
py scripts/sync_compliance_mirrors_from_csv.py \
   --persona-scenario-registry-only \
   --output /tmp/i51-p1-persona-scenario-mirror.sql

# Operator review, then apply via mcp_supabase or psql under service_role.
```

After apply, parity check:

```sql
SELECT COUNT(*) FROM compliance.persona_scenario_registry_mirror;  -- expect 329
```

Mirror reseed cadence is governed by **D-IH-51-D** (default: after every CSV
tranche edit), recorded in `decision-log.md`.

## Tier-B / governance impact

- **No CSV edits.** Canonical SSOT (`PERSONA_SCENARIO_REGISTRY.csv`) is
  unchanged; G-51-1 (P3 rebalance gate) does **not** fire here.
- **No DDL changes.** I47 P1 mirror DDL + I49 priority columns remain authoritative.
- **No POLICY edits.** `POLICY_REGISTER.csv` unchanged in this phase.
- **No drift impact.** `scripts/check-drift.py` is unaffected (this is repo →
  mirror direction, not config → repo).

## Risk register touch

- **R-51-3 (mirror reseed surfaces stale state)** — mitigation now active:
  emitter is idempotent; `ON CONFLICT (scenario_id) DO UPDATE SET` ensures
  re-running the SQL converges to the CSV state without producing duplicates
  or losing `synced_at` provenance.

## Closes

- **OPS-47-9** — wired up; one operator-applied reseed away from full closure
  on the data-plane side.

## Out-of-scope (forwarded)

- Operator-driven calibration analysis lives in **I51/P2** (calibration audit:
  the 13-outlier remediation report).
- Cassette wiring for Tier-B hot-path personas (OPS-50-1 overlap) lives in
  **I51/P3** under the operator-chosen rebalance path (G-51-1).
