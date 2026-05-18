# P2 Pause Record — Stage B Column Promotion

| Key | Value |
|:---|:---|
| Initiative | I86 (initiative-cluster-execution-coordinator) |
| Phase | P2 — promote `program_anchors` from `notes` prefix to first-class semicolon-list FK column |
| Date | 2026-05-17 |
| Pause-point category | **MANDATORY** — canonical-CSV gate + Supabase DDL (per `akos-agent-checkpoint-discipline.mdc` §"Pause-point depth heuristic") |
| Author | Agent (Madeira / AKOS) |
| Posture | Code + canonical CSV mutation **complete**; Supabase remote apply **deferred to operator** per `akos-holistika-operations.mdc` §"Operator SQL gate" |

## Authoring contract (per `akos-agent-checkpoint-discipline.mdc` §"Operator pause point contract")

1. **Stop at the documented stop point** — Yes; agent halts further mutation of remote Supabase until operator ratifies this pause record.
2. **File pause record with mechanical + documentary evidence + approval checklist ≤ 7 items** — this file.
3. **Wait for operator's explicit approval signal** — operator response in this thread, or a commit message that references this file, or an explicit "continue" instruction.

## 1. Mechanical evidence (files, line counts, validator verdicts)

### Files created (this phase)

| Path | Lines | Notes |
|:---|---:|:---|
| [`supabase/migrations/20260517163635_i86_p2_program_anchors_column.sql`](../../../../supabase/migrations/20260517163635_i86_p2_program_anchors_column.sql) | 60 | idempotent `ALTER TABLE ADD COLUMN IF NOT EXISTS program_anchors TEXT` + btree index + `COMMENT ON COLUMN`; rollback inline §"Rollback plan" |
| [`scripts/_oneshot_anchors_notes_to_column.py`](../../../../scripts/_oneshot_anchors_notes_to_column.py) | 230 | single-use; underscore prefix marks "remove on P2 closure"; `--dry-run` default; row-level diff to `reports/p2-oneshot-diff-2026-05-17.md` |
| [`docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/checkpoints/sc-pre-p2-2026-05-17.md`](checkpoints/sc-pre-p2-2026-05-17.md) | 110 | pre-P2 self-checkpoint |
| [`docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/checkpoints/sc-mid-p2-2026-05-17.md`](checkpoints/sc-mid-p2-2026-05-17.md) | 90 | mid-P2 self-checkpoint |
| [`docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/p2-oneshot-diff-2026-05-17.md`](p2-oneshot-diff-2026-05-17.md) | 160 | row-level diff for all 24 migrated rows; BEFORE/AFTER notes |

### Files modified (this phase)

| Path | Δ | Change summary |
|:---|---:|:---|
| [`akos/hlk_initiative_registry_csv.py`](../../../../akos/hlk_initiative_registry_csv.py) | +1 | `program_anchors` inserted in `INITIATIVE_REGISTRY_FIELDNAMES` tuple between `linked_topic_ids` and `notes` |
| [`scripts/validate_initiative_registry.py`](../../../../scripts/validate_initiative_registry.py) | +6 | new `PROGRAM_CSV` constant + `program_ids` load + FK-resolution block mirroring `linked_topic_ids` pattern |
| [`scripts/validate_initiative_program_anchors.py`](../../../../scripts/validate_initiative_program_anchors.py) | rewrite (+150 -120) | column-read default; `--legacy-notes-parser` opt-in; `--strict` for cutover-hygiene fail-loud; structured `ValidationOutcome` dataclass |
| [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv`](../../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv) | header +1 col; 24 rows mutated | new `program_anchors` column header; 24 rows: prefix stripped from `notes`, anchors moved to column |
| [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/CANONICAL_REGISTRY.csv`](../../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/CANONICAL_REGISTRY.csv) | row 31 | `last_review: 2026-05-12 → 2026-05-17`; notes extended with D-IH-86-J column-promotion record |
| [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md`](../../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md) | L49 + L96 | canonical-CSV narrative + mirror narrative extended with D-IH-86-J / program_anchors column |
| [`tests/test_validate_initiative_program_anchors.py`](../../../../tests/test_validate_initiative_program_anchors.py) | +95 -55 | split into Stage A (`_evaluate_legacy_notes`) + Stage B (`_evaluate_column_read`) blocks; added cutover-hygiene WARN test |

### Validator verdicts (mechanical)

| Surface | Verdict |
|:---|:---|
| `py scripts/validate_initiative_registry.py` | **PASS** (68 rows; FK block green) |
| `py scripts/validate_initiative_program_anchors.py` | **PASS** (column-read default; 24 column-populated rows; 0 residual notes prefix) |
| `py scripts/validate_initiative_program_anchors.py --legacy-notes-parser` | **PASS** (0 prefix rows — cutover clean) |
| `py scripts/validate_hlk.py` | **OVERALL PASS** |
| `py -m pytest tests/test_validate_initiative_program_anchors.py tests/test_pmo_program_anchor_backfill.py -v` | **22 passed** in 1.04s |
| `py scripts/verify.py compliance_mirror_emit` | **PASS** — emitted SQL includes `program_anchors` in INSERT + ON CONFLICT UPDATE clauses |

## 2. Documentary evidence

### Decisions encoded

| Decision | Status entering | Status exiting | Outcome |
|:---|:---|:---|:---|
| D-IH-86-J | ratified at Round 2 (P0) | **operationalised** at P2 | Stage B column-promotion shipped (code + CSV + tests + validator cutover); Supabase DDL authored, awaiting operator apply |
| D-IH-86-I | ratified at Round 2 (P0) | reaffirmed | Charter-scope amendment continues to cover the FK chassis evolution as governance tooling not new SSOT |

### Cross-canon link integrity

- `CANONICAL_REGISTRY.csv` row 31 last_review bumped; notes updated.
- `PRECEDENCE.md` canonical-CSV row (L49) and mirror row (L96) both extended with D-IH-86-J + new column.
- `INITIATIVE_REGISTRY.csv` header + 24 rows mutated; FK targets in `PROGRAM_REGISTRY.csv` resolve cleanly (validator green).
- `compliance.initiative_registry_mirror` schema is **NOT yet** updated on remote Supabase — pending operator apply of `supabase/migrations/20260517163635_i86_p2_program_anchors_column.sql`.

### CHANGELOG entry

To be appended in P2 closure commit (see operator approval checklist below).

## 3. Operator approval checklist (≤ 7 items)

The operator must verify each before ratifying P2 closure. Mark each as ☑ in a reply (or commit message referencing this file).

1. **Migration file** `supabase/migrations/20260517163635_i86_p2_program_anchors_column.sql` exists, is idempotent (`ADD COLUMN IF NOT EXISTS`), declares rollback inline, and adds no CHECK constraint (matches I71 P4 review-stamp shape). ☐
2. **Canonical CSV mutation** `INITIATIVE_REGISTRY.csv` carries the new `program_anchors` column header between `linked_topic_ids` and `notes`; 24 rows are populated; notes prefix removed; agent-side validators are clean. ☐
3. **One-shot script** `scripts/_oneshot_anchors_notes_to_column.py` exists, was run in `--apply` mode against the canonical CSV (mutation evidence in `p2-oneshot-diff-2026-05-17.md`), and should be **deleted in the P2 closure commit** to enforce single-use semantics. ☐
4. **Validators** `validate_initiative_registry.py` (FK block) + `validate_initiative_program_anchors.py` (column-read default) + the `--legacy-notes-parser` deprecation path all pass; tests are green; `validate_hlk.py` OVERALL PASS. ☐
5. **Supabase apply** (operator-side residual): operator runs MCP `apply_migration` against the remote project with the migration body, verifies `supabase migration list` shows the new timestamp, and runs `compliance_mirror_emit` + applies the emitted SQL to refresh `compliance.initiative_registry_mirror` rows with the new column data. ☐
6. **Security posture** (operator-side residual): operator runs MCP `get_advisors(security)` and confirms no new advisories attributable to the additive column (none expected; column is `NULL`-tolerant and existing RLS inherits). ☐
7. **Docs sync**: `CANONICAL_REGISTRY.csv` row 31 + `PRECEDENCE.md` L49 + L96 carry D-IH-86-J narrative extension; `CHANGELOG.md` will carry P2 entry; `master-roadmap.md` P2 marked complete in the P2 closure commit. ☐

## 4. R-IH-86-10 risk window (CSV-mirror schema drift)

Until the operator applies the migration, the canonical CSV is **ahead** of the remote `compliance.initiative_registry_mirror` schema by one column. `compliance_mirror_emit` will continue to emit valid SQL because:

- The CSV is the SSOT; the validator is green; the emitted SQL is well-formed.
- ON CONFLICT UPDATE statements that reference `program_anchors = EXCLUDED.program_anchors` will fail to apply against the un-extended mirror schema until the migration lands. The operator-side residual sequence is: (a) apply migration → (b) re-emit SQL → (c) apply emitted SQL.

**Tolerable window**: ≤ 1 week. Past that, the catalog of valid emitted SQL accumulates rows the operator hasn't yet applied; CHANGELOG carries a reminder. If the window extends beyond a week, surface via I86 risk-register row R-IH-86-10 in the next operator audit.

## 5. References

- Plan body: `~/.cursor/plans/i86_program_anchor_robustness_3e15859c.plan.md` §P2.
- D-IH-86-J ratification: [`decision-log.md`](../decision-log.md) §J.
- Pre-P2 self-checkpoint: [`checkpoints/sc-pre-p2-2026-05-17.md`](checkpoints/sc-pre-p2-2026-05-17.md).
- Mid-P2 self-checkpoint: [`checkpoints/sc-mid-p2-2026-05-17.md`](checkpoints/sc-mid-p2-2026-05-17.md).
- One-shot diff report: [`p2-oneshot-diff-2026-05-17.md`](p2-oneshot-diff-2026-05-17.md).
- Sister rules: [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) §"Operator SQL gate"; [`akos-agent-checkpoint-discipline.mdc`](../../../../.cursor/rules/akos-agent-checkpoint-discipline.mdc) §"Operator pause point contract".
