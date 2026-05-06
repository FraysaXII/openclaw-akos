---
language: en
status: active
initiative: 63-external-repo-governance-codification
initiative_id: INIT-OPENCLAW_AKOS-63
report_kind: master-roadmap
program_id: shared
plane: ops
authority: Founder + System Owner
last_review: 2026-05-07
---

# Initiative 63 — External Repo Governance Codification

**Folder:** `docs/wip/planning/63-external-repo-governance-codification/`
**Status:** **Active** — created 2026-05-06 alongside the External Repo Bless Pattern automation as a sibling to [I62](../62-mission-control/master-roadmap.md). Operator-approved 2026-05-07 (D-IH-63-D, D-IH-63-E); P0-P4 closed (charter + SOPs + canonical CSV updates applied + SOPs flipped to `active`). Continuing through P5-P7 (commit/push, dry-run evidence, I64 scaffolding).

## Outcome

Codify the External Repo Bless Pattern (today an executable scaffolder + 9
automation scripts + 12 templates) into the AKOS canonical artefact stack so
that the same governance is process-traceable, not just code-traceable:

1. **Canonical CSV updates** — extend `REPOSITORY_REGISTRY.csv` with three new
   columns (`consumes_compliance_types`, `consumes_mirrors`, `path`) and add
   ~3 process rows to `process_list.csv` for the new SOPs.
2. **SOP authoring** — three new SOPs at `status: review` in the v3.0 vault:
   - `SOP-EXTERNAL_REPO_BLESSING_001.md`
   - `SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001.md`
   - `SOP-CROSS_REPO_SCHEMA_PROPAGATION_001.md`
3. **KM manifests** — manifest stubs under `v3.0/_assets/techops/` so the
   Topic-Fact-Source layer can index the new SOPs.
4. **Cursor rule pointer** — extend `.cursor/rules/akos-mirror-template.mdc`
   to reference the three new SOPs once promoted to `active`.

This initiative does **not** add net-new automation. It codifies what the
External Repo Bless Pattern already runs into the asset classes that AKOS
governance respects (process_list rows minted before SOPs go active per
`SOP-META_PROCESS_MGMT_001.md` §4.2-4.3).

## Why now

- The External Repo Bless Pattern bootstrapped 9 scripts + 12 templates +
  4 workflow templates that touch core operator processes (blessing,
  drift remediation, schema propagation). Without canonical SOPs, this is
  "agent code" rather than "doctrine".
- Per the user concern raised 2026-05-06: *"with all this, we're touching
  core processes, do we need to touch our canonical artifacts and vault and
  build well designed SOPs?"* — yes, and that is the scope of this
  initiative.
- Pattern alignment: I62 already shows the right shape (canonical
  `SUBDOMAINS_REGISTRY.md` + validator + release-gate hook). I63 follows
  the same shape for processes/SOPs.

## Scope decisions

| In scope | Out of scope |
|:---|:---|
| Three new SOPs at `status: review` in v3.0 vault | Promoting them to `status: active` (requires operator gate per SOP-META) |
| `REPOSITORY_REGISTRY.csv` column proposal (no edit yet) | Editing `REPOSITORY_REGISTRY.csv` rows (operator approval required) |
| `process_list.csv` row proposal (no edit yet) | Editing `process_list.csv` (canonical CSV gate) |
| KM manifest stubs under `v3.0/_assets/techops/` | Topic-Fact-Source backfill against the new SOPs |
| Cursor rule pointer extension after promotion | Generating new persona/skill/topic IDs |
| Docs cross-link in USER_GUIDE §24.13 | Replacing the External Repo Bless Pattern automation |

## Asset classification (per [`PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md))

See [`asset-classification.md`](asset-classification.md). Summary:

- **Canonical (proposed)**: 3 new rows in `process_list.csv`, 3 new columns in
  `REPOSITORY_REGISTRY.csv`. Operator-gated; this initiative produces the
  proposal report only.
- **Canonical (drafted, status: review)**: 3 SOP markdowns under
  `v3.0/Admin/O5-1/Envoy Tech Lab/External Repos/` and
  `v3.0/Admin/O5-1/Envoy Tech Lab/Cross Repo/`.
- **Reference-only**: this charter folder.

## Phase dependency

```mermaid
flowchart TD
    P0[P0 Charter (this file + sibling artefacts)]
    P1[P1 SOP authoring at status: review]
    P2[P2 KM manifest stubs]
    P3[P3 Operator review of CSV proposal]
    P4[P4 Canonical CSV edits (operator-gated)]
    P5[P5 SOP promotion to status: active]
    P6[P6 Cursor rule pointer + USER_GUIDE update]

    P0 --> P1
    P0 --> P2
    P0 --> P3
    P3 --> P4
    P4 --> P5
    P5 --> P6
```

## Phases

### P0 Charter

- This folder: `master-roadmap.md`, `decision-log.md`, `asset-classification.md`,
  `evidence-matrix.md`, `risk-register.md`.
- `reports/csv-proposal-2026-05-06.md` (the operator-facing proposal).
- README.md row added under `docs/wip/planning/README.md`.

**Verification**: this charter is consistent with `docs/USER_GUIDE.md` §24.13 cross-references and the Cursor plan that bootstrapped it.

### P1 SOP authoring (status: review)

- `v3.0/Admin/O5-1/Envoy Tech Lab/External Repos/SOP-EXTERNAL_REPO_BLESSING_001.md`
- `v3.0/Admin/O5-1/Envoy Tech Lab/External Repos/SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001.md`
- `v3.0/Admin/O5-1/Envoy Tech Lab/Cross Repo/SOP-CROSS_REPO_SCHEMA_PROPAGATION_001.md`

Each SOP carries `status: review`, references the relevant scripts, and
mirrors the `SOP-META_PROCESS_MGMT_001.md` shape.

**Verification**: `py scripts/validate_hlk.py` (no broken cross-references) +
`py scripts/validate_hlk_vault_links.py` clean.

### P2 KM manifest stubs

Stubs under `docs/references/hlk/v3.0/_assets/techops/` so the KM layer can
discover the new SOPs once they're promoted.

**Verification**: `py scripts/validate_hlk_km_manifests.py` clean.

### P3 Operator review of CSV proposal — CLOSED 2026-05-07

Operator-gated: review `reports/csv-proposal-2026-05-06.md`, decide on
column names + process item_ids + role_owner mappings.

**Outcome:** Approved with revisions. Schema corrected (no fictional
`plane` column), `path` → `local_path`, comma → semicolon for
`consumes_mirrors`, `item_id` harmonised to canonical `SOP-<NAME>_001`
shape. **D-IH-63-D** (CSV approval) and **D-IH-63-E** (DevOPS / System
Owner role-owner split) recorded.

### P4 Canonical CSV edits — CLOSED 2026-05-07

Applied:

- `process_list.csv` +3 rows (lines 1105-1107): blessing (DevOPS),
  drift remediation (DevOPS), schema propagation (System Owner). Total
  rows: 1100 → 1103.
- `REPOSITORY_REGISTRY.csv` schema extended with 3 columns
  (`consumes_compliance_types`, `consumes_mirrors`, `local_path`); all
  6 existing rows annotated.
- `akos/hlk_repository_registry_csv.py:REPOSITORY_REGISTRY_FIELDNAMES`
  extended to keep the field contract in sync.
- `GOVERNANCE_MOAT.md` count refreshed: 1.103 procesos gobernados.

**Verification:** `py scripts/validate_repository_registry.py` PASS;
`py scripts/validate_repository_registry_md_csv_sync.py` PASS;
`py scripts/check_process_list_header.py` PASS;
`py scripts/sync_compliance_mirrors_from_csv.py --count-only` reports
`process_list_rows=1103`, `repository_registry_rows=6`.

### P5 SOP promotion — CLOSED 2026-05-07

All three SOPs flipped `status: review` → `status: active`,
`Version: 0.1` → `Version: 1.0`, with `process_id` + `role_owner`
fields added to frontmatter cross-linking back to `process_list.csv`.

### P6 Cursor rule pointer + USER_GUIDE update — CLOSED 2026-05-06

Already shipped in the External Repo Bless Pattern plan (Track O):
`.cursor/rules/akos-mirror-template.mdc` references the three SOPs;
USER_GUIDE §24.13 ¶3 documents the continuous loops.

### P7 Dry-run evidence + push to main — IN PROGRESS

- Add `--dry-run` / `--report-only` flags where missing.
- Run all loops against hlk-erp end-to-end; capture evidence at
  `reports/dryrun-evidence-2026-05-06.md`.
- Commit + push AKOS, hlk-erp, kirbe to `origin/main`.

### P8 Operator surface (governance dashboard in hlk-erp) — DEFERRED to I64

Sister initiative scaffolded with the standard 6-panel governance
dashboard (repo health grid, drift inbox, secret rotation calendar,
canonical broadcast log, SOP/decision-log surface). See
[I64 master-roadmap](../64-governance-mission-control/master-roadmap.md).

## Verification matrix

| Phase | Command | Status |
|:---|:---|:---|
| P0 | `py scripts/release-gate.py` (existing checks pass) | ✓ |
| P1 | `py scripts/validate_hlk.py` and `py scripts/validate_hlk_vault_links.py` | ✓ |
| P2 | `py scripts/validate_hlk_km_manifests.py` (incl. SOP `intellectual_kind` extension) | ✓ |
| P3 | Operator review and decision (D-IH-63-D, D-IH-63-E) | ✓ |
| P4 | `py scripts/validate_repository_registry.py` + `validate_repository_registry_md_csv_sync.py` + `check_process_list_header.py` + `sync_compliance_mirrors_from_csv.py --count-only` | ✓ |
| P5 | `py scripts/validate_hlk.py` after SOP `status: active` flip | ✓ |
| P6 | `py scripts/release-gate.py` (final) | ✓ |
| P7 | Dry-run evidence + commit/push (this section) | in progress |
| P8 | Deferred to [I64](../64-governance-mission-control/master-roadmap.md) | deferred |

## Cross-references

- [I62](../62-mission-control/master-roadmap.md) — sibling initiative that
  bootstrapped the External Repo Bless Pattern.
- [`USER_GUIDE.md` §24.13](../../../USER_GUIDE.md) — operator flow for
  blessing.
- [`SOP-META_PROCESS_MGMT_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-META_PROCESS_MGMT_001.md) — process minting order (CSV before SOP).
- [`PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md) — asset
  classification rubric.
- [`REPOSITORY_REGISTRY.csv`](../../../references/hlk/compliance/REPOSITORY_REGISTRY.csv) — canonical registry receiving proposed columns.
