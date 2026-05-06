---
language: en
initiative: 59-hlk-governance-clean-slate
phase: P1
report_kind: phase-report
report_date: 2026-05-06
status: complete
---

# I59 P1 — HLK governance dimensions (architectural addition)

**Outcome:** the planning workspace gets five new HLK-governed compliance dimensions (REPOSITORY / INITIATIVE / OPS / CYCLE / DECISION), wired end-to-end through the established HLK pattern (Pydantic schema → CSV → validator → sync validator → Supabase mirror → PRECEDENCE row). Two new PMO SOPs codify the lifecycle and the process_list harmonisation recipe at `status: review`. P1 is **purely architectural** — no initiative status flips, no operator approval gates, no `process_list.csv` minting (those land in P3 and the I60 candidate respectively).

## Trigger

D-IH-59-A through D-IH-59-G (recorded in [`decision-log.md`](../decision-log.md)) enumerate the seven foundational decisions that bound P1: atomic dimension landing, two-layer SSOT, REPOSITORY_REGISTRY promotion, status taxonomy ownership, DECISION_REGISTER inclusion, process_list deferral to I60, and nullable FKs.

## Artifacts shipped

### Pydantic schema modules (5)

```
akos/hlk_repository_registry_csv.py        # I59 P1.1
akos/hlk_initiative_registry_csv.py        # I59 P1.2
akos/hlk_ops_register_csv.py               # I59 P1.3
akos/hlk_cycle_register_csv.py             # I59 P1.4
akos/hlk_decision_register_csv.py          # I59 P1.5
```

Each module exports `<DIMENSION>_FIELDNAMES` (header contract tuple) and the relevant `VALID_*` frozensets (status enums, classes, reversibility, etc.). Per the I59 plan, these modules expose **header contracts**, not per-row Pydantic models — alignment with the existing HLK dimension pattern (e.g. `hlk_skill_registry_csv.py`).

### Canonical CSVs (5)

```
docs/references/hlk/compliance/REPOSITORY_REGISTRY.csv     # 6 rows seeded
docs/references/hlk/compliance/INITIATIVE_REGISTRY.csv     # headers only — bulk seed in P3
docs/references/hlk/compliance/OPS_REGISTER.csv            # headers only — bulk seed in P3
docs/references/hlk/compliance/CYCLE_REGISTER.csv          # headers only — bulk seed in P3
docs/references/hlk/compliance/DECISION_REGISTER.csv       # headers only — bulk seed in P3
```

REPOSITORY_REGISTRY.csv is the **only** dimension seeded in P1 because it has a stable upstream source (`REPOSITORIES_REGISTRY.md`) and **no incoming FKs** from peer dimensions. The other four would create circular FK pressure if seeded before P3 (DECISION ↔ INITIATIVE; INITIATIVE ↔ CYCLE; OPS → INITIATIVE → DECISION). Seeding in lockstep at P3 lets validators assert real FKs against fully-populated tables.

### Procedural validators (5)

```
scripts/validate_repository_registry.py
scripts/validate_initiative_registry.py
scripts/validate_ops_register.py
scripts/validate_cycle_register.py
scripts/validate_decision_register.py
```

Each enforces: header contract vs FIELDNAMES, primary-key format and uniqueness, enum values (status / class / reversibility / cadence / impact), FK resolution against canonical CSVs (`baseline_organisation.csv`, `process_list.csv`, `TOPIC_REGISTRY.csv`, peer dimensions, self-FK for supersedes), companion-field rules per `akos/planning/status_taxonomy.py`, ISO date format, advisory existence checks for `decision_log_path`. All validators return 0 for PASS/SKIP and 1 for FAIL.

### Sync validators (3)

```
scripts/validate_repository_registry_md_csv_sync.py
scripts/validate_initiative_registry_frontmatter_sync.py
scripts/validate_decision_register_decision_log_md_sync.py
```

These enforce the **two-layer SSOT** contract (D-IH-59-B): markdown is canonical for prose, CSV is canonical for metadata. The decision-log sync is intentionally **advisory** during P1–P2 (104 historical D-IH-XX-Y headers in MD have no CSV row yet — that's expected; bulk seeding lands in P3). It will become strict from P10 onward.

### Status taxonomy SSOT module

```
akos/planning/__init__.py
akos/planning/status_taxonomy.py      # InitiativeStatus StrEnum + companion fields
```

Seven values (`closed`, `archived`, `active`, `continuous`, `program_line`, `gated_external`, `gated_operator`) with explicit companion-field requirements (e.g. `gated_operator` requires at least one back-pointing OPS_REGISTER row). The two new validators above import this module to apply the rules.

### Supabase migrations (5)

```
supabase/migrations/20260506120000_i59_repository_registry_mirror.sql
supabase/migrations/20260506120100_i59_initiative_registry_mirror.sql
supabase/migrations/20260506120200_i59_ops_register_mirror.sql
supabase/migrations/20260506120300_i59_cycle_register_mirror.sql
supabase/migrations/20260506120400_i59_decision_register_mirror.sql
```

Each includes DDL with `CHECK` constraints matching the corresponding `VALID_*` enums, `COMMENT` clauses citing the canonical CSV path, indexes matching expected query patterns (e.g. `rice_score DESC NULLS LAST` on `ops_register_mirror`, `decided_at DESC` on `decision_register_mirror`), and `ROW LEVEL SECURITY` policies (`deny_authenticated`, `deny_anon`, `service_role`) — server-only access posture per the established compliance-mirror convention.

### Mirror-emit helpers (5)

Wired into `scripts/sync_compliance_mirrors_from_csv.py`:

- 5 imports added (FIELDNAMES from new schema modules)
- 5 path constants added (`*_CSV` constants, all under `docs/references/hlk/compliance/`)
- 5 `_emit_*_upserts()` helpers added (compact pattern matching the I32 P2/P3/P4/P7 dimensions)
- 5 argparse `--*-only` flags added
- 5 entries added to the `mode_flags` tuple and the multi-mode error message
- New `_i59_mirror_specs` factory block (parallel to `_i32_mirror_specs`)
- 5 entries added to count-only output and full-bundle conditional emission

Smoke-tested:

```
py scripts/sync_compliance_mirrors_from_csv.py --count-only
  ...
  repository_registry_rows=6
  initiative_registry_rows=0
  ops_register_rows=0
  cycle_register_rows=0
  decision_register_rows=0

py scripts/sync_compliance_mirrors_from_csv.py --repository-registry-only --no-begin-commit
  -- 6 INSERT INTO compliance.repository_registry_mirror statements emitted

py scripts/sync_compliance_mirrors_from_csv.py --output sync_smoke_full.sql
  Wrote sync_smoke_full.sql bytes= 2,852,491
  6 INSERT INTO compliance.repository_registry_mirror lines present in full bundle
```

### `validate_hlk.py` dispatch table

8 new entries (5 dimension + 3 sync validators) added to the central dispatcher. `OVERALL: PASS` confirmed.

### PRECEDENCE.md registration

10 new rows added (5 canonical asset rows + 5 mirror rows), each citing the canonical CSV path, validator script, sync validator (where applicable), Supabase migration filename, and the relevant I59 decision IDs.

### New PMO SOPs (2, both at `status: review`)

```
docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-INITIATIVE_GOVERNANCE_001.md
docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-INITIATIVE_PROCESS_HARMONISATION_001.md
```

The first codifies the seven-status taxonomy and the inception → active → cycle membership → closure lifecycle. The second codifies the two cases (manifests existing vs mints new) for linking initiatives to `process_list.csv`. Both are at `status: review` pending operator approval gate G-59-D in P9.

### Markdown SSOT update

`REPOSITORIES_REGISTRY.md` updated: the AKOS workspace now lists `repo_slug=openclaw-akos` (the canonical GitHub remote) — the legacy `madeira-hlk-runtime` slug retained as a parenthetical alias note. This eliminates the markdown↔CSV sync drift that the new sync validator surfaced on first run.

## KM manifests — deferred (justified)

The five new dimensions are CSV/text-only governance assets with no visual diagram, raster, SVG, or Mermaid source. The existing KM manifest pattern (`docs/references/hlk/v3.0/_assets/**/*.manifest.md`) requires those files. Rather than ship empty visual scaffolds, manifests are deferred to:

- The **2 new SOP** manifests in P9 (which covers KM manifests for the SOP files themselves — this is the existing pattern for SOP files).
- Any future visual diagram of the dimension graph (e.g. an entity-relationship visualisation across the 5 new dimensions) — out of scope for P1 and tracked as a non-blocking nice-to-have.

P10 verification matrix already lists `validate_hlk_km_manifests.py` and the gate passes today (no `_assets/` entries for P1 dimensions = no validation failure).

## Decisions captured (P1 lockdown)

| ID | Title | Status |
|----|-------|--------|
| D-IH-59-A | Atomic dimension landing (5 dimensions in lockstep, single P1 commit) | accepted |
| D-IH-59-B | Two-layer SSOT (markdown for prose, CSV for metadata) | accepted |
| D-IH-59-C | REPOSITORY_REGISTRY promotion path (CSV joins markdown as canonical) | accepted |
| D-IH-59-D | Status taxonomy ownership (akos.planning.status_taxonomy) | accepted |
| D-IH-59-E | DECISION_REGISTER inclusion in I59 (vs. defer to I60) | accepted |
| D-IH-59-F | Nullable FKs (manifests_processes; coordinated_initiative_ids) | accepted |
| D-IH-59-G | manifests_processes column on INITIATIVE_REGISTRY (vs. inverse on process_list) | accepted |

(All seeded in P0 — see [`decision-log.md`](../decision-log.md). P1 confirms them in code without re-litigation.)

## Risks captured / cleared

| Risk | Status after P1 | Note |
|------|-----------------|------|
| R-59-1 (audit misclassification) | mitigated | Status enum has explicit companion fields preventing ambiguous tagging in P3 |
| R-59-2 (dashboard regression) | not yet exercised | P2 will exercise the section split |
| R-59-3 (markdown↔CSV drift) | mitigated | 3 sync validators + advisory mode for decision-log handoff to P3 |
| R-59-4 (FK violations during P3 seed) | mitigated by ordering | Header-only CSVs + lockstep P3 bulk seed sidesteps circularity |
| R-59-5 (RLS / migration breakage) | mitigated | All 5 migrations follow the same RLS pattern as I32 P2/P3/P4/P7 |
| R-59-13 (audit incompleteness) | not yet exercised | P3 will run the full audit |

## Verification (P1 gate)

| Check | Result |
|------|--------|
| `py scripts/validate_hlk.py` (incl. 8 new validators) | **PASS** (`OVERALL: PASS`) |
| `scripts/sync_compliance_mirrors_from_csv.py --count-only` | PASS — 22 dimensions count out cleanly |
| `scripts/sync_compliance_mirrors_from_csv.py --repository-registry-only --no-begin-commit` | PASS — 6 INSERTs emitted |
| `scripts/sync_compliance_mirrors_from_csv.py` (full bundle) | PASS — 2.85 MiB bundle includes all I59 inserts |
| Linter (8 modified scripts + 5 new schemas + 8 new validators) | clean |
| Pre-existing tests | not yet re-run; P10 verification matrix runs `py scripts/test.py all` |

## Forward residual

- **P2:** wire `akos.planning.status_taxonomy` into the dashboard renderer (section split) and the master-roadmap frontmatter validator. The status taxonomy module is **already** importable and used by `validate_initiative_registry.py`; P2 only adds the rendering side.
- **P3:** bulk-seed the four header-only CSVs (INITIATIVE / OPS / CYCLE / DECISION). This is gated by G-59-A/B/C operator approval per the plan.
- **P4:** auto-render `OPERATOR_INBOX.md` from `OPS_REGISTER.csv`.
- **P5:** cycle staleness canary using `INITIATIVE_REGISTRY.csv.last_review`.
- **P9:** ratify the 2 new SOPs from `status: review` to `status: active`.

## Linkage to predecessors

- **I32 (HLK Repository Health Snapshot):** P1 reuses the I32 P2/P3/P4/P7 dimension pattern (compact factory in the sync script, RLS migration template, validator structure). The 5 new dimensions follow that template byte-for-byte.
- **I47 / I49:** the persona scenario registry validator's structure (FK chains, semicolon-list parsing) was the closest precedent for the new dimensions' multi-FK columns. Identical idioms are used for `linked_*` and `coordinated_initiative_ids`.
- **I22:** the `dimensions/` subfolder convention applies to new compliance assets going forward; the 5 new dimensions land under `compliance/` directly (not under `dimensions/`) because they are **planning-workspace metadata** rather than business-domain dimensions. PRECEDENCE.md documents this.
