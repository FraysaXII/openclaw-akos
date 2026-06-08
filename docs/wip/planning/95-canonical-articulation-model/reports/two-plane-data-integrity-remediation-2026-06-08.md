# Two-plane data integrity remediation — I95 / BT-09 follow-through

**Date:** 2026-06-08  
**Initiative:** INIT-OPENCLAW_AKOS-95  
**Verdict:** PASS (mechanical guards landed; mirrors at SSOT counts after full-sync)

## What broke (and why `validate_hlk` was not enough)

Holistika uses a **two-plane** model:

| Plane | What it is | What validated it (before) |
|:---|:---|:---|
| **T1** | Git CSV SSOT + Pydantic models | `validate_hlk.py` — OVERALL PASS |
| **T2** | Supabase `compliance.*_mirror` DDL + rows | Nothing until `psql` apply |

Two independent failure modes surfaced during mirror-sync apply:

1. **Column shift (D-IH-95-A class)** — `DECISION_REGISTER` row for `D-IH-95-A` had a stray empty field (`summary.",,"notes"`), pushing free text into the `last_review_at` DATE column. Header validation passed; row-width did not.
2. **Enum DDL lag** — `PEOPLE_DESIGN_PATTERN_REGISTRY.pattern_class` gained `area_governance` (I93) and `intent_ranked_regression_cadence` (I88) in Pydantic, but the mirror `CHECK` constraint still listed only 15 values. Apply failed at `pattern_area_buildout`.

Additionally:

3. **Upsert-only orphan drift** — After BT-09 de-densification, upsert-only sync left mirror row counts stale (e.g. capability 1,119 vs CSV 93) until delete-reconcile ran.
4. **Gap-mirror wiring** — OPS-86-15 capability/AIC/audience mirrors were emitted on a separate path and not spliced into the main CI txn until 2026-06-08.

## Remediation delivered (this session)

### Guards (permanent)

| Script | DATA dim | Purpose |
|:---|:---|:---|
| `validate_csv_column_alignment.py` | DATA-05 | Every row = `len(FIELDNAMES)`; DATE cols = `YYYY-MM-DD` |
| `validate_pydantic_mirror_enum_ssot.py` | DATA-05 | Pydantic enum ⊆ latest migration CHECK |
| `validate_mirror_emit_contract.py` | DATA-02 | CSV row count = emitted INSERT count; workflow wiring |
| `validate_mirror_enum_parity.py` | DATA-08 preflight | Emitted values ⊆ live CHECK (CI, before apply) |
| `emit_mirror_delete_reconcile.py` | DATA-02 | `DELETE … NOT IN (csv pks)` for full-sync shrink |

All wired into `validate_hlk.py` + `dataops_quality_check.py` (DATA-02/DATA-05 probes live, not stub).

### Pipeline (`.github/workflows/supabase-mirror-sync.yml`)

1. Emit main + splice OPS-86-15 gap mirrors into same transaction  
2. Delete-reconcile (default ON for push + manual apply)  
3. Enum parity preflight (fail fast with fix ALTER)  
4. Atomic apply (`--single-transaction`)

### Migration SSOT

`supabase/migrations/20260608211500_i95_mirror_enum_parity_design_pattern_class.sql` — extends `people_design_pattern_mirror_class_chk` to 17 values (repo copy of live fix).

## Data remediation (guards caught real defects)

| Surface | Defect | Fix |
|:---|:---|:---|
| `PEOPLE_DESIGN_PATTERN_REGISTRY` line 9 | Unquoted commas in `notes` (`e.g., ...`) → 16 fields | Quoted `notes` field |
| `PEOPLE_DESIGN_PATTERN_REGISTRY` line 27 | `D-IH-93-B,v3.1,...` split into extra columns → 17 fields | Quoted `notes` field |
| `baseline_organisation` RevOps Manager / Analyst / CRO | Empty `org_uuid` since I72 P4 — rows never mirror-emitted | Minted `d4e5f6a7-7070-4bbb-d005-000000000001..003` |
| `validate_pydantic_mirror_enum_ssot.py` | Parser missed `CHECK (col IN (...))` multiline migrations | Extended parser + `\s+CHECK` regex |

`validate_csv_column_alignment.py` now requires non-empty `org_uuid` on every baseline role row (emit-eligible contract).

## Post-remediation mirror counts (MasterData)

| Mirror | CSV SSOT | Mirror (after full-sync) |
|:---|:---|:---|
| `process_list_mirror` | 496 | 496 |
| `capability_registry_mirror` | 93 | 93 |
| `capability_confidence_registry_mirror` | 93 | 93 |
| `topic_registry_mirror` | 58 | 58 |
| `decision_register_mirror` | 526 | 526 |
| `aic_registry_mirror` | 5 | 5 |
| `audience_registry_mirror` | 9 | 9 |

## Operator actions

- **None required** for guards — they run in `validate_hlk` + CI preflight automatically.
- On future enum additions: extend Pydantic **and** add migration **before** mirror apply; `validate_pydantic_mirror_enum_ssot.py` will catch lag.
- Manual full-sync: `gh workflow run supabase-mirror-sync.yml -f apply=true` (reconcile defaults ON).

## Cross-links

- BT-09 milestone: `CHANGELOG.md` + `LOGIC_CHANGE_LOG.md`
- OPS-95-1: **closed** 2026-06-08 — mirror re-sync + two-plane guards
- `DATAOPS_DISCIPLINE.md` §2.1 two-plane contract
