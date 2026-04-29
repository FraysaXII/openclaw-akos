# Initiative 23 — Asset Classification

Per [`PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md) and the Initiative 22 forward layout convention.

## Canonical (edit-here-first)

| Asset | Path | Owner / Notes |
|:------|:-----|:--------------|
| Program registry | `docs/references/hlk/compliance/dimensions/PROGRAM_REGISTRY.csv` (P1) | First canonical CSV under `dimensions/`; emitted from operator-answers YAML by scaffolder; PRJ-HOL-style `program_id` + 3-letter `program_code` + program-to-program edges |
| akos field contract | `akos/hlk_program_registry_csv.py` (P1) | `PROGRAM_REGISTRY_FIELDNAMES` tuple keeps CSV header in lockstep with Python |
| Validator | `scripts/validate_program_registry.py` (P1) | Cycle detection, code uniqueness, FK to baseline + process_list, forward-reference policy |
| Cross-asset validator | `scripts/validate_program_id_consistency.py` (P3) | Asserts every `program_id` reference resolves to a registry row |
| Drift probe | `scripts/probe_compliance_mirror_drift.py` (P4) | Operator-pasted JSON parity between CSV and live mirror |
| Cross-program glossary | `docs/reference/glossary-cross-program.md` (P5) | First-class doc; auto-trigger for `docs/GLOSSARY.md` "see" link if any term appears in 3+ first-class docs |
| Initiative folder | `docs/wip/planning/23-hlk-program-registry-and-program-2/` (P0) | 6 standard artifacts |

## New tooling extensions

| Asset | Path | Notes |
|:------|:-----|:------|
| Scaffolder writer | `scripts/wave2_backfill.py` `_write_program_registry()` (P0.5) | Reads `programs:` section of `operator-answers-wave2.yaml` and emits `PROGRAM_REGISTRY.csv`; idempotent; refuses on sentinels unless `--allow-pending` |
| Scaffolder tests | `tests/test_wave2_backfill.py` extension (P0.5) | Lock the writer's emit shape and idempotency contract |
| Sync flag | `scripts/sync_compliance_mirrors_from_csv.py` `--program-registry-only` (P2) | Mirror UPSERT emit |
| Verify profile | `config/verification-profiles.json` `compliance_mirror_drift_probe` (P4) | Operator-pasted; graceful SKIP |
| Graph builder | `akos/hlk_graph_model.py` `build_program_graph()` (Pgraph) | Emits `:Program` nodes + edges from CSV rows |
| Graph constraints | `akos/hlk_neo4j.py` (Pgraph) | `FOR (n:Program) REQUIRE n.program_id IS UNIQUE`; range indexes on lifecycle/code/plane |
| Graph sync | `scripts/sync_hlk_neo4j.py` (Pgraph) | Adds Program builder pass after Role/Process |

## Mirrored / derived (do not hand-edit)

| Asset | Path | Sync direction |
|:------|:-----|:---------------|
| `compliance.program_registry_mirror` | Live Supabase (P2 — applied) | `PROGRAM_REGISTRY.csv` → MCP `apply_migration` (DDL) + `execute_sql` (DML, `service_role`) |
| Neo4j `:Program` nodes + edges | Neo4j Community (Pgraph — projected) | `PROGRAM_REGISTRY.csv` → `sync_hlk_neo4j.py` rebuild |

## Mirrored / derived (planning README)

| Asset | Path | Notes |
|:------|:-----|:------|
| Planning README slot 23 | `docs/wip/planning/README.md` row | Updated from `(reserved)` to active during P0 |

## Reference-only (historical / evidence)

| Asset | Path | Notes |
|:------|:-----|:------|
| P0.5 operator review tracker | `reports/p05-operator-review.md` | Optional; tracks which agent-defaulted cells operator has confirmed |
| P2 mirror apply evidence | `reports/p2-mirror-apply-evidence.md` | Timestamps, advisor warnings, row counts |
| Pgraph apply evidence | `reports/pgraph-neo4j-apply-evidence.md` | Constraints + indexes added; sync probe results |
| UAT report | `reports/uat-i23-program-registry-YYYYMMDD.md` | PASS/SKIP/N/A per row; closure record |

## Out-of-repo

- Operator-managed credentials for Supabase `service_role` and Neo4j Bolt (`~/.openclaw/.env`); never in git.
- Real-name ↔ ref_id identity mapping (Initiative 21 P1 SOP §7).
