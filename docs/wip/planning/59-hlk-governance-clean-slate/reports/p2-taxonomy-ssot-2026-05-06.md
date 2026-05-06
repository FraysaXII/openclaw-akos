---
language: en
initiative: 59-hlk-governance-clean-slate
phase: P2
report_kind: phase-report
report_date: 2026-05-06
status: complete
---

# I59 P2 — Status taxonomy SSOT (frontmatter side)

**Outcome:** the seven-value `InitiativeStatus` taxonomy module shipped in P1 is now wired into both the **WIP dashboard renderer** (section split) and a new **frontmatter validator**. Status drift is now visible at a glance in the dashboard and reported (advisory) by `validate_hlk.py`. P3 (mass status audit + tag) becomes a deterministic write operation against this contract.

## Trigger

D-IH-59-D (status taxonomy ownership): `akos.planning.status_taxonomy.InitiativeStatus` is the single source of truth for initiative statuses. Both the markdown frontmatter side and the CSV side must agree on enum values; the dashboard must render rows grouped by these values.

## Artifacts shipped

### Dashboard renderer section split

[`scripts/render_wip_dashboard.py`](../../../../scripts/render_wip_dashboard.py) updated:

- **Imports the taxonomy SSOT**: `DASHBOARD_SECTION_ORDER`, `DASHBOARD_SECTION_TITLES`, `VALID_INITIATIVE_STATUSES`, `InitiativeStatus`.
- **New `_classify_status(frontmatter_status, body_status_raw)`** function classifies each row into a deterministic taxonomy bucket:
  - Frontmatter `status:` matching the enum → that bucket.
  - Frontmatter `status:` non-empty but not in enum → `unknown` bucket (legacy drift expected; P3 normalises).
  - Legacy body `**Status:**` line → `unknown` bucket, retains the body string for display.
  - Nothing → `unknown` bucket, displays `unknown`.
- **`_read_initiative()`** now extracts the frontmatter `status:` field via a new `FRONTMATTER_STATUS_RE` regex, in addition to the existing body-line scan, and emits both `bucket` and `status` fields per row.
- **New `_render_grouped_table()`** renders rows into seven taxonomy sections plus an `Unknown / unclassified` section, in the canonical order from `DASHBOARD_SECTION_ORDER`. Empty sections still emit their header (`(0)`) with a `_(none)_` placeholder so operators see the full taxonomy at a glance.
- **`main()`** flips from `_render_table` to `_render_grouped_table`. The legacy flat renderer is retained for callers (tests, ad-hoc scripts) that still want the un-grouped variant.

Determinism re-confirmed: `--check-only` post-render returns PASS (sha256 stable across runs).

### Master-roadmap frontmatter validator

New script [`scripts/validate_master_roadmap_frontmatter.py`](../../../../scripts/validate_master_roadmap_frontmatter.py) walks every `docs/wip/planning/<NN>-<slug>/master-roadmap.md` and enforces:

1. The `status:` field (when present) is one of the seven `InitiativeStatus` enum values.
2. Required companion fields per `REQUIRED_COMPANION_FIELDS` are present (e.g. `archived` requires `archived_at` and `superseded_by`; `gated_operator` requires `gated_on` and `operator_action`).

**Mode discipline:**

- **Advisory (default for P1–P2)**: missing frontmatter, missing `status:`, non-taxonomy values, and missing companion fields are all **warnings**. Run does not fail.
- **Strict (`--strict`, gated for P10)**: warnings escalate to errors; missing companion fields fail the run.

Wired into the `validate_hlk.py` dispatcher as the new `MASTER_ROADMAP_FRONTMATTER` entry (no CSV gate; scans the planning workspace directly). Confirmed PASS in default mode; expected FAIL in strict mode (will be re-baselined post-P3).

### Snapshot of current state (after P2 wiring)

```
Master-roadmaps scanned:  47
With valid taxonomy status + companions:  1   (only I59 itself)
Warnings (advisory):                      48
Errors (default mode):                    0
```

The **48 warnings** distribute as:

- **26** missing frontmatter entirely (legacy I01–I26-era initiatives).
- **17** valid frontmatter but missing `status:` field, **or** valid `status:` but missing companion fields.
- **2** non-taxonomy `status:` values needing remap:
  - I55: `active-continuous-loop` → should become `continuous` (with `continuous_rationale`).
  - I56: `bootstrapped-pending-first-advisor-reply` → should become `gated_external` (with `gated_on`).
- **2** valid taxonomy values but missing companions (I05 `archived` lacks `archived_at` and `superseded_by`; I20 same).
- **1** is the closure-form `closed` rows that lack `closed_at` companion (I28 / I29 / I30 / I31 / I32 / I45 / I46 / I47 / I48 / I49 / I50 / I51 / I52 / I53 / I54 / I57 / I58).

P3 closes all 48 warnings with a deterministic mass tag operation.

### Dashboard rendering — visual verification

After re-render, [`docs/wip/planning/WIP_DASHBOARD.md`](../../WIP_DASHBOARD.md) shows the seven sections in canonical order:

| Section | Count |
|---------|------:|
| Active (in execution) | 1 |
| Gated on external event | 0 |
| Gated on operator action | 0 |
| Continuous loops (active by design) | 0 |
| Program lines (cadence-driven) | 0 |
| Closed | 17 |
| Archived (superseded) | 2 |
| Unknown / unclassified | 27 |

The 27-row Unknown section is exactly the legacy drift that P3 will resolve. The split makes it impossible to confuse "active by design" (Continuous / Program lines) with "active in execution" (Active) — the original ambiguity I59 was created to fix.

## Decisions confirmed in code

| ID | Confirmation |
|----|--------------|
| D-IH-59-D | Status taxonomy SSOT lives in `akos.planning.status_taxonomy`; renderer + validator both import it. |
| D-IH-59-B | Two-layer SSOT enforced via the existing `validate_initiative_registry_frontmatter_sync.py` (P1) and now by the frontmatter-side enum validator. |

## Verification (P2 gate)

| Check | Result |
|------|--------|
| `py scripts/validate_master_roadmap_frontmatter.py` (default) | **PASS** (48 advisory warnings) |
| `py scripts/validate_master_roadmap_frontmatter.py --strict` | FAIL (expected; gated to P10) |
| `py scripts/render_wip_dashboard.py` | re-render succeeded; 8 sections visible |
| `py scripts/render_wip_dashboard.py --check-only` | **PASS** (deterministic; sha256 stable) |
| `py scripts/validate_hlk.py` | **PASS** (`OVERALL: PASS`) — `MASTER_ROADMAP_FRONTMATTER: PASS` |
| Linter (3 files: renderer + new validator + dispatcher) | clean |

## Forward residual (P3)

1. Mass-flip the 27 unknown-bucket initiatives. Algorithm:
   - Pure metadata-only / done-decades-ago initiatives (I01, I06, I09) → `archived` with `archived_at` and `superseded_by`.
   - Active programmes still progressing (I04, I08, I14) → `program_line` with `cadence`.
   - Quality-of-life loops (I06, I55) → `continuous` with `continuous_rationale`.
   - Operator-blocked (I12, I24, I56) → `gated_external` or `gated_operator` with companion fields.
   - Genuinely active engineering work (I22a, I32, I46, …) → `active` with up-to-date `last_review`.
   - Closeable today (I02, I07, I15) → `closed` with `closed_at` and a closure UAT report.
2. Bulk-seed `INITIATIVE_REGISTRY.csv` with one row per master-roadmap; verify the frontmatter↔CSV sync gate PASSes strict.
3. Bulk-seed `OPS_REGISTER.csv` from existing OPS-XX-Y references in CHANGELOG.md and master-roadmaps.
4. Bulk-seed `CYCLE_REGISTER.csv` with retroactive rows for I57 / I58 / I59.
5. Bulk-seed `DECISION_REGISTER.csv` with the ~104 historical D-IH-XX-Y decisions surfaced by the advisory sync validator.

These five seeds turn the four header-only CSVs into fully populated dimensions, after which the frontmatter↔CSV sync validators flip from advisory to strict.

## Linkage to predecessors

- **I32 P10** (WIP dashboard auto-renderer): P2 inherits the auto-render contract verbatim and only changes the rendering function. The hand-written content above and below the markers is preserved exactly as before.
- **I59 P1**: the taxonomy SSOT module created in P1 is now consumed by two callers (the renderer and the frontmatter validator), proving the SSOT pattern works as designed.
