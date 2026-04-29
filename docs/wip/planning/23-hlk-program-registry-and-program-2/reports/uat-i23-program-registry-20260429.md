# UAT — Initiative 23 (Program Registry + Onboarding Program 2)

**Date**: 2026-04-29  
**Operator approvals captured (Wave-2 plan §"Operator approval gates" + I23 master roadmap)**:

- **G-23-1** — Postgres mirror DDL apply via MCP `apply_migration` + DML seed via `service_role` `execute_sql`: **APPLIED** (this run; 12 program rows seeded, RETURNING all program_ids).
- **G-23-2** — `process_list.csv` named tranche for KiRBe onboarding: **N/A this PR** — `env_tech_prj_2 KiRBe Platform` already exists in `process_list.csv` (project granularity); no new tranche required for I23-P6.
- **G-23-3** — `baseline_organisation.csv` change for new role: **NOT TRIGGERED** — KiRBe onboarding role roots reuse existing roles (System Owner, Data Governance Lead, Data Architect, Business Controller, PMO).
- **G-23-4** — Neo4j projection extension applied: **DRY-RUN PARITY ASSERT PASS** (12 programs + 14 program-side edges; live Bolt apply on next operator-driven sync; SKIPs gracefully when Neo4j unconfigured).

## Verification matrix

| Check | Result |
|:------|:------:|
| `py scripts/validate_hlk.py` (incl. PROGRAM_REGISTRY + PROGRAM_ID_CONSISTENCY) | **PASS** |
| `py scripts/validate_hlk_vault_links.py` | **PASS** |
| `py scripts/validate_hlk_km_manifests.py` | **PASS** (manifest sha256 matches rendered PNG) |
| `py scripts/validate_program_registry.py` | **PASS** (12 programs, 12 unique codes) |
| `py scripts/validate_program_id_consistency.py` | **PASS** (30 references scanned, 2 distinct ids: PRJ-HOL-FOUNDING-2026, PRJ-HOL-KIR-2026) |
| `py -m pytest tests/test_wave2_backfill.py -v` | **17/17 PASS** |
| `py -m pytest tests/test_validate_program_id_consistency.py -v` | **7/7 PASS** |
| `py -m pytest tests/test_probe_compliance_mirror_drift.py -v` | **13/13 PASS** |
| `py scripts/sync_compliance_mirrors_from_csv.py --count-only` | reports `program_registry_rows=12` |
| `py scripts/sync_hlk_neo4j.py --dry-run` | `programs=12 edges=2245 (incl. 14 program-side)` |
| MCP `execute_sql` row-count probe (program_registry_mirror) | **12 rows** matching CSV |
| MCP `execute_sql` row-count probe (process_list_mirror after drift fix) | **1091 rows** = CSV (was 1083 before P4 reseed) |
| `py scripts/verify.py compliance_mirror_drift_probe` | **PASS** (8/8 mirrors at parity) |
| `py scripts/verify.py wave2_backfill_check` | informational (sentinels remain in `brand_voice`, `kirbe_duality`, `g_24_3_signoff` per design) |

## Manual review items

- **Operator review of agent-defaulted Tier-3 cells in `operator-answers-wave2.yaml` `programs:`** (D-IH-23-A). Target: 2026-05-15 or before next program onboarding, whichever is sooner. The 11 process-list-keyed programs carry agent defaults for `lifecycle_status`, `risk_class`, `start_date`, `target_close_date`, `consumes_program_ids`, `notes`; PRJ-HOL-FOUNDING-2026 was already operator-filled.
- **Decision D-IH-23-B**: product programs use 3-letter `program_code` as the canonical slug (e.g. `PRJ-HOL-KIR-2026`, not `PRJ-HOL-KIRBE-2026`). Casework programs (e.g. `PRJ-HOL-FOUNDING-2026`) keep the long form. Operator may flip later via a single-commit rename cascade.
- **G-24-1 (Initiative 24)**: GOI/POI mirror DDL ALTER for voice columns is **deferred** to Initiative 24 P2.

## Closure

Initiative 23 phases P0–P8 are **complete**:

- P0 — folder bootstrap with 6 standard artifacts (PR #13).
- P0.5 — operator answers with agent-defaulted Tier-3 cells (PR #13).
- P1 — `PROGRAM_REGISTRY.csv` + akos contract + validator + `validate_hlk.py` integration (PR #13).
- P2 — Postgres mirror DDL applied via MCP; 12 rows seeded; RLS deny anon/authenticated; ledger parity preserved (PR #13).
- Pgraph — Neo4j projection extension (`:Program` + `:CONSUMES` / `:PRODUCES_FOR` / `:PROGRAM_PARENT_OF` / `:PROGRAM_SUBSUMES` / `:OWNED_BY`); edge naming disambiguated; graceful SKIP (PR #13).
- P3 — cross-asset `program_id` consistency validator (PR #14).
- P4 — operator-pasted compliance mirror drift probe + verify profile; surfaced and fixed real drift on `process_list_mirror` (1083 → 1091) (PR #14).
- P5 — cross-program glossary at `docs/reference/glossary-cross-program.md` + `docs/GLOSSARY.md` "see" rows (PR #14).
- P6 — onboarded `PRJ-HOL-KIR-2026` with **6 evidence-based role roots** (Tech/System Owner, Data/Governance, Data/Architecture, Finance/Business Controller, People, Operations/PMO), one KM topic asset (`_assets/techops/PRJ-HOL-KIR-2026/topic_kirbe_billing_plane_routing/`) with `.mmd` source-of-truth + manifest + companion + rendered PNG/SVG, and exercised the `consumes_program_ids` edge to PRJ-HOL-FOUNDING-2026.
- P7 — docs/rules sync (this PR includes UAT + closure note; cursor-rules trigger updates ride with the docs sync).
- P8 — UAT (this report); closure note in master roadmap.

## Cross-references

- Plan: `~/.cursor/plans/hlk_scalability_wave_2_initiatives_639a02d7.plan.md`
- Decision log: [`decision-log.md`](../decision-log.md) (D-IH-8 / D-IH-9 / D-IH-16 / D-IH-18 / D-IH-23-A / D-IH-23-B)
- Risk register: [`risk-register.md`](../risk-register.md) (PR-23-1..PR-23-8)
- Asset classification: [`asset-classification.md`](../asset-classification.md)
- Evidence matrix: [`evidence-matrix.md`](../evidence-matrix.md)
- Drift probe artifact (operator-local; gitignored): `artifacts/probes/mirror-drift-20260429.json`
