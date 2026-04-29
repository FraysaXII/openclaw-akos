# Re-evaluation trigger — `compliance/<plane>/` physical relocation

**Status**: TEMPLATE / NOT FIRED (2026-04-29).
**Owners**: Compliance (primary), Data Architect (secondary), PMO (initiative orchestration).
**Authority**: Wave-2 plan §"Decisions" **D-IH-15**; Initiative 22 [`decision-log.md`](../../22-hlk-scalability-and-i21-closures/decision-log.md) **D-IH-1**; this initiative's [`decision-log.md`](../decision-log.md) **D-IH-26-E**.
**Pattern source**: I22-P8 [`re-eval-trigger.md`](../../22-hlk-scalability-and-i21-closures/reports/re-eval-trigger.md).

## Why this template exists

Initiative 22 D-IH-1 elected **convention-only** for `compliance/` CSV physical moves: legacy flat files (`GOI_POI_REGISTER.csv`, `ADVISER_*.csv`, `FOUNDER_FILED_INSTRUMENTS.csv`, `FINOPS_COUNTERPARTY_REGISTER.csv`, `COMPONENT_SERVICE_MATRIX.csv`) stay at the `compliance/` root; the **deprecation alias map** in [`docs/references/hlk/compliance/README.md`](../../../references/hlk/compliance/README.md) documents the forward target paths under `compliance/<plane>/` (`advops/`, `finops/`, `techops/`, `dimensions/`).

The Wave-2 plan §"D-IH-15" + this initiative's D-IH-26-E keep that posture **DEFERRED** until concrete friction surfaces. As of 2026-04-29 (KIR onboarded smoothly in I23-P6, the only new canonical CSV under `dimensions/` is `PROGRAM_REGISTRY.csv` which already lands at the target path), no friction has surfaced.

This template captures the conditions under which the relocation initiative should ship.

## Triggers

Reopen the decision when **either** condition fires:

1. **Program 2 friction** — onboarding `PRJ-HOL-KIRBE-2026` (or any future program 2/3) surfaces actual file-naming pain. Examples that would qualify:
   - Operator confusion about whether a new CSV belongs at `compliance/` root or `compliance/<plane>/` (decisions get made differently across operators).
   - File-name collisions between programs (e.g. `FOUNDER_FILED_INSTRUMENTS.csv` is implicitly founder-only — adding a `KIRBE_FILED_INSTRUMENTS.csv` would expose the implicit-program coupling).
   - Tooling that scans `compliance/*.csv` flatly cannot disambiguate plane ownership without convention-by-filename (which ties brittleness to filename).
2. **Second canonical CSV in any plane** — a new ADVOPS / FINOPS / TECHOPS / MKTOPS / OPS canonical CSV joins the existing one. Examples:
   - FINOPS adds a contract / SLA register (would qualify under D-IH-14 trigger too).
   - ADVOPS adds a per-discipline workflow register beyond `ADVISER_ENGAGEMENT_DISCIPLINES.csv` + `ADVISER_OPEN_QUESTIONS.csv` + `FOUNDER_FILED_INSTRUMENTS.csv`.

## Trigger record (fill on activation)

```yaml
fired_on: <YYYY-MM-DD>
trigger_kind: <program_2_friction | second_csv_in_plane>
detected_by: <role / person>
evidence:
  - <link to operator confusion incident, file-name collision, tooling brittleness>
  - <link to second-CSV initiative if that's the trigger>
scope_to_relocate:
  - <list of files to git mv, e.g. compliance/GOI_POI_REGISTER.csv -> compliance/dimensions/GOI_POI_REGISTER.csv>
  - <…>
ripple_files_to_update:
  - akos/hlk_*_csv.py: <which fieldname-tuple file paths reference the old CSV path>
  - scripts/validate_*.py: <which validators reference REPO_ROOT-relative path>
  - scripts/validate_hlk.py: <integration site>
  - scripts/sync_compliance_mirrors_from_csv.py: <CSV path constants>
  - supabase/migrations/*_compliance_*.sql: <COMMENT references>
  - scripts/sql/*_staging/*.sql: <as above>
  - SOPs that cite CSV path: <list>
  - tests/test_*.py: <which tests reference path>
operator_approvals:
  - <Compliance | Data Architect | PMO>
proposed_initiative_slot: <NN-compliance-plane-relocation>
estimated_chunk_size: ~2 days (single-commit cascade)
```

## Force-action checklist (do NOT skip steps)

- [ ] **Trigger documented** above. The trigger MUST fall into one of the two categories.
- [ ] **Ripple impact mapped** — the cascade hits ~25 files (akos modules, validators, sync script, mirror DDL comments, staging SQL, SOPs, tests). Pre-list every file before P0.
- [ ] **`git mv` for history preservation** — never `git rm` + `git add`; that loses blame chains.
- [ ] **Single commit per phase** per [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) §"Commit and phase discipline".
- [ ] **Validators run on each step**: `validate_hlk.py`, `validate_hlk_vault_links.py`, `validate_hlk_km_manifests.py` — all must PASS after each chunk.
- [ ] **Compliance + Data Architect + PMO approval** captured in initiative `decision-log.md`.
- [ ] **Update `compliance/README.md` deprecation alias map** — each migrated row shows "MIGRATED on `<date>`".
- [ ] **Update `PRECEDENCE.md` row paths** to point at the new locations.
- [ ] **`db push` Supabase migration parity** confirmed (mirror DDL comments updated; no schema drift).
- [ ] **Mark this template "FIRED + RESOLVED on `<YYYY-MM-DD>`"** with link to the closure PR after the relocation initiative ships.

## Cursor-rule guardrails (always-on)

Per [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) §"Forward layout convention (Initiative 22)":

- **New planes added going forward** MUST land their canonical CSVs **directly** under `compliance/<plane>/` (not at root). The relocation initiative addresses **legacy** flat files only.
- **Existing flat files stay in place** until this trigger fires; do not anticipate the relocation by leaving stub files in `compliance/<plane>/`.
- **The deprecation alias map in [`compliance/README.md`](../../../references/hlk/compliance/README.md)** is the single record of where each legacy file should eventually land. When the relocation initiative ships, the alias map is updated, not deleted.

## Cross-references

- [Initiative 26 master roadmap](../master-roadmap.md)
- [Initiative 26 decision log](../decision-log.md) — D-IH-26-E
- [Initiative 22 decision log](../../22-hlk-scalability-and-i21-closures/decision-log.md) — D-IH-1 (Hybrid-light refactor strategy)
- [Wave-2 plan §"Decisions" D-IH-15](~/.cursor/plans/hlk_scalability_wave_2_initiatives_639a02d7.plan.md)
- [Compliance README alias map](../../../references/hlk/compliance/README.md) §"Deprecation alias map (current ↔ forward)"
