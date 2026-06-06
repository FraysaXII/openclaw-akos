---
pause_record_id: P1-PAUSE-2026-05-15
initiative_id: INIT-OPENCLAW_AKOS-73
phase: P1
phase_title: Strand E ENGAGEMENT_MODEL_REGISTRY canonical CSV gate
pause_class: canonical-CSV gate
authored: 2026-05-15
authored_by: Agent (Claude Opus 4.7)
operator_review_required: yes
mandatory_gate: yes
language: en
---

# I73 P1 — Pause record (canonical-CSV gate)

> Filed per [`akos-agent-checkpoint-discipline.mdc`](../../../../.cursor/rules/akos-agent-checkpoint-discipline.mdc) §"Operator pause point contract". P1 is a **mandatory pause point** because it touches canonical compliance CSVs (`process_list.csv`, `DECISION_REGISTER.csv`, `INITIATIVE_REGISTRY.csv`, `PRECEDENCE.md`) + extends an existing canonical (`ENGAGEMENT_REGISTRY.csv` 16→17 col) + mints a new canonical (`ENGAGEMENT_MODEL_REGISTRY.csv` sibling dimension at People Operations per D-IH-73-C). Operator approval acknowledged via inline-ratify Gate B + Gate C skip-recommended-default per operator's task-spec rule ("If operator skips any gate: treat as recommended-default-accepted"). The full P1 deliverable surface is below; this record is the audit-grade evidence + operator approval checklist for re-confirmation.

## Mechanical evidence

### Files created (new at P1 commit) — 7 files

| Path | Size hint | Purpose |
|---|---|---|
| [`docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/People%20Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv) | 16 cols × 7 rows + header | Canonical 7-class engagement-model taxonomy (D-IH-73-D) |
| [`docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/People%20Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.md) | ~180 lines | Schema spec + 7-class taxonomy table + cross-refs + maintenance cadence |
| [`akos/hlk_engagement_model_csv.py`](../../../../../akos/hlk_engagement_model_csv.py) | ~180 lines | Pydantic SSOT (EngagementModelRow + ENGAGEMENT_MODEL_FIELDNAMES + VALID_* frozensets + Literal enums) |
| [`scripts/validate_engagement_model_registry.py`](../../../../../scripts/validate_engagement_model_registry.py) | ~130 lines | CLI validator (header drift + Pydantic per-row + FK + 7-class completeness) |
| [`tests/test_validate_engagement_model_registry.py`](../../../../../tests/test_validate_engagement_model_registry.py) | ~240 lines / 18 tests | Test pairs (valid + invalid + integration smoke) |
| [`supabase/migrations/20260515180000_i73_compliance_engagement_model_mirror.sql`](../../../../../supabase/migrations/20260515180000_i73_compliance_engagement_model_mirror.sql) | ~140 lines | Mirror DDL + CHECK constraints + RLS deny + governance view |
| [`supabase/migrations/20260515180001_i73_engagement_registry_add_engagement_model_id.sql`](../../../../../supabase/migrations/20260515180001_i73_engagement_registry_add_engagement_model_id.sql) | ~40 lines | ALTER TABLE engagement_registry_mirror ADD COLUMN engagement_model_id + FK NOT VALID |

### Files modified (existing canonical CSVs + scripts + docs) — 11 files

| Path | Change kind | Lines delta (approx) | Purpose |
|---|---|---|---|
| [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv) | data-row-append | +7 rows | 7 `tbi_peopl_dtp_engagement_*` rows |
| [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) | data-row-append | +7 rows | D-IH-73-H..N |
| [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv) | modified | +1 / -1 | I73 row last_review bump to D-IH-73-N + manifests_processes populated + gated_on narrative update |
| [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md) | modified | +2 rows | Canonical + mirror row entries |
| [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.csv) | modified | +1 col / 6 rows backfilled empty | Add 17th `engagement_model_id` FK column per D-IH-73-N |
| [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.md) | modified | +1 row in schema table | §2 updated to 17-col schema |
| [`scripts/sync_compliance_mirrors_from_csv.py`](../../../../../scripts/sync_compliance_mirrors_from_csv.py) | modified | +60 lines | `_emit_engagement_model_upserts` + `--engagement-model-only` flag + count + bundle integration |
| [`scripts/validate_compliance_schema_drift.py`](../../../../../scripts/validate_compliance_schema_drift.py) | modified | +6 lines | `_REGISTRY` tuple appended |
| [`scripts/validate_hlk.py`](../../../../../scripts/validate_hlk.py) | modified | +5 lines | Dispatcher row for ENGAGEMENT_MODEL_REGISTRY |
| [`docs/wip/planning/73-people-operations-and-learning-curriculum/decision-log.md`](../decision-log.md) | modified | +70 lines | D-IH-73-H..N rationale + alternatives + decision_source |
| [`docs/wip/planning/OPERATOR_INBOX.md`](../../OPERATOR_INBOX.md) | modified (regen) | sha256 update | Pre-existing staleness from I73 P0; regenerated as part of P1 cleanup |
| [`config/verification-profiles.json`](../../../../../config/verification-profiles.json) | modified | +9 lines | `engagement_model_registry_smoke` profile |
| [`docs/DEVELOPER_CHECKLIST.md`](../../../../DEVELOPER_CHECKLIST.md) | modified | +1 row | Pre-commit row 7-i73 |
| [`CHANGELOG.md`](../../../../../CHANGELOG.md) | modified | +1 row | `[Unreleased]` `### Added` line for I73 P1 |

### Validators run + verdicts

| Validator | Command | Verdict | Notes |
|---|---|---|---|
| Engagement model registry | `py scripts/validate_engagement_model_registry.py` | **PASS** | 7 rows × 16 cols; Data Owner verified |
| Compliance schema drift | `py scripts/validate_compliance_schema_drift.py` | **PASS** | 23 canonicals registered (was 22; +1 for ENGAGEMENT_MODEL_REGISTRY) |
| Pytest test suite | `py -m pytest tests/test_validate_engagement_model_registry.py -v` | **PASS** | 18/18 tests green |
| Sync count-only | `py scripts/sync_compliance_mirrors_from_csv.py --count-only` | **PASS** | reports `engagement_model_registry_rows=7` |
| HLK umbrella | `py scripts/validate_hlk.py` | **PASS** | OVERALL: PASS (ENGAGEMENT_MODEL_REGISTRY + DECISION_REGISTER + INITIATIVE_REGISTRY + PROCESS_LIST_PAIRING all green) |
| Release gate | `py scripts/release-gate.py` | **FAIL (pre-existing only)** | I73-attributable rows PASS; FAILs are documented carry-overs per CHANGELOG (Test suite + Browser smoke + BRAND voice register + BRAND voice Vale sibling). No NEW I73-attributable failures. |

### Tests added

`tests/test_validate_engagement_model_registry.py` — 18 tests covering:

- `test_csv_exists` + `test_csv_header_matches_fieldnames_tuple` + `test_csv_column_count_is_16` (structural).
- `test_seven_classes_present` + `test_every_row_pydantic_validates` (data integrity).
- `test_outsourced_helper_carries_d_ih_73_e_soc_posture` + `test_operator_self_carries_baseline_internal_posture` + `test_apprentice_learner_carries_training_posture` (per-class enum semantics aligned with D-IH-73-D/E/K/M).
- 6 enum-membership tests (status / retribution_pattern / soc_posture / ip_clause_class / knowledge_access_level / payment_cadence).
- `test_invalid_slug_rejected` + `test_invalid_enum_rejected` + `test_invalid_access_level_rejected` (invalid-input pairs per CONTRIBUTING.md §"Python Code Standards").
- `test_validator_script_exits_zero` (validator CLI integration smoke).

## Documentary evidence

### Decisions encoded (D-IH-73-H..N)

7 new rows in [`DECISION_REGISTER.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) + full rationale in [`decision-log.md`](../decision-log.md):

| Decision ID | Title | Class | Status | Supersedes |
|---|---|---|---|---|
| D-IH-73-H | eng_model_hourly_consultant enum ratification | architecture | active | D-IH-73-D |
| D-IH-73-I | eng_model_milestone_consultant enum ratification | architecture | active | D-IH-73-D |
| D-IH-73-J | eng_model_percentage_collaborator enum ratification | architecture | active | D-IH-73-D |
| D-IH-73-K | eng_model_apprentice_learner enum ratification | architecture | active | D-IH-73-D |
| D-IH-73-L | eng_model_investor_advisor enum ratification | architecture | active | D-IH-73-D |
| D-IH-73-M | eng_model_outsourced_helper enum ratification (cross-link to D-IH-73-E SOC posture) | architecture | active | D-IH-73-E |
| D-IH-73-N | ENGAGEMENT_REGISTRY.csv 17-col extension (add `engagement_model_id` FK column) | architecture | active | — |

All 7 carry `decision_source: operator_inline_default_accepted_via_skip` per task-spec rule ("If operator skips any gate: treat as recommended-default-accepted").

### Cross-canon link integrity

- [`PRECEDENCE.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md) — Engagement Model Registry canonical row + `compliance.engagement_model_registry_mirror` mirror row both registered.
- [`ENGAGEMENT_REGISTRY.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.md) §2 schema spec updated to 17-col (new `engagement_model_id` row at end of table) with cross-link to sibling dimension.
- [`scripts/validate_hlk.py`](../../../../../scripts/validate_hlk.py) dispatcher graph appended with ENGAGEMENT_MODEL_REGISTRY row + CSV gate path.
- [`scripts/validate_compliance_schema_drift.py`](../../../../../scripts/validate_compliance_schema_drift.py) `_REGISTRY` tuple appended (23rd canonical).
- [`config/verification-profiles.json`](../../../../../config/verification-profiles.json) `engagement_model_registry_smoke` profile registered.
- [`docs/DEVELOPER_CHECKLIST.md`](../../../../DEVELOPER_CHECKLIST.md) pre-commit row 7-i73 added.

### CHANGELOG entry

`[Unreleased]` `### Added` line authored in [`CHANGELOG.md`](../../../../../CHANGELOG.md) describing the full I73 P1 deliverable surface (above the existing I73 P0 charter entry).

## Operator approval checklist (≤ 7 items)

Operator confirms by inspection (or by explicit reply / commit-msg reference / proceed signal):

1. **Architecture preserved**: 7-class taxonomy (D-IH-73-D) matches operator brief 2026-05-15; sibling-dimension placement (D-IH-73-C) at `People/People Operations/canonicals/dimensions/` (not Compliance/dimensions/ or Operations/RevOps); outsourced_helper carries separate SOC class (D-IH-73-E) with `access_level=1` + `soc_posture=low_trust` + `knowledge_access_level=work_product_scope_only`.
2. **Enum values match operator spec**: `retribution_pattern` 7 values, `soc_posture` 5 values, `ip_clause_class` 7 values, `knowledge_access_level` 5 values, `payment_cadence` 7 values, `status` 3 values — all match the operator-provided enum lists from the task spec verbatim (with `knowledge_access_level=full_by_engagement` for rows 1/3/5 instead of bare `full` — harmonized from row drafts).
3. **process_list tranche ratified**: 7 `tbi_peopl_dtp_engagement_*` rows owned by `People Operations Manager` with paired-SOP forward-charter via `TODO[I73-P2-SOP-PATH]` or `TODO[I73-P3-SOP-PATH]` markers per D-IH-72-W feature-flag pattern. Cadence: 3× scheduled (quarterly), 4× event_triggered. No baseline_organisation tranche required (all 3 forward-charter roles — People Operations Manager, Learning Curator, Ethics Advisor — already exist from I70 P8.5 D-IH-70-Q split).
4. **ENGAGEMENT_REGISTRY 17-col extension ratified (D-IH-73-N)**: existing 6 rows backfill empty; FK constraint NOT VALID until P9 backfill. Companion migration `20260515180001_i73_engagement_registry_add_engagement_model_id.sql` lands as the second migration of P1.
5. **Validator suite green**: `validate_engagement_model_registry.py` PASS; `validate_compliance_schema_drift.py` PASS (23 canonicals); `validate_hlk.py` umbrella OVERALL PASS; 18/18 tests green; release-gate FAILs are pre-existing carry-overs (Test suite + Browser smoke + BRAND voice register + Vale exit=2 per I73 P0 CHANGELOG `### Fixed` note).
6. **No NEW I73-attributable validator failures**: release-gate exit code 1 is from pre-existing failures only; the new validator + dispatcher entries all PASS.
7. **Atomic commit + no push**: this P1 commit lands as a single atomic commit on `main` per the I73 master plan's one-commit-per-phase cadence; `git push` deferred to operator instruction.

If any of these are not OK, surface via `opt-stop-report` posture (write `reports/p1-blocker-<date>.md` and stop) per `akos-governance-remediation.mdc`. If all OK, commit.

## What ships next (forward-charter; not in P1)

- **P2** — Strand A Learning charter + Holistik Researcher curriculum + LEARNING_OPS_BACKLOG.csv. C-73-1 + C-73-2 inline-ratify gates. Apprentice ↔ curriculum binding closes the `tbi_peopl_dtp_apprentice_curriculum_assignment_001` forward-charter from P1.
- **P3** — Strand C 4 Engagement-lifecycle SOPs (hiring / onboarding / payroll / offboarding) parameterized by `engagement_model_id`. C-73-4 inline-ratify gate. Closes the 4 P3-forward TODO[I73-P3-SOP-PATH] markers from P1 process_list rows.
- **P5** — Strand B Ethics+Learning SOP-ETHICS_LEARNING_REVIEW_001.md.
- P2, P3, P4, P5 may proceed in parallel after P1 lands per the phase dependency diagram in [`master-roadmap.md`](../master-roadmap.md).

## Cross-references

- Pre-author SC: [`checkpoints/sc-pre-p1-2026-05-15.md`](checkpoints/sc-pre-p1-2026-05-15.md).
- Post-CSV-draft SC: [`checkpoints/sc-post-csv-draft-p1-2026-05-15.md`](checkpoints/sc-post-csv-draft-p1-2026-05-15.md).
- Authoritative Cursor plan: `~/.cursor/plans/i73-people-ops-engagement-models-methodology-ip-c9d4e7f3.plan.md` §"P1 deep section".
- Workspace mirror: [`../master-roadmap.md`](../master-roadmap.md) phase-at-a-glance.
- Decision log: [`../decision-log.md`](../decision-log.md) D-IH-73-H..N.
- Files-modified CSV: [`../files-modified.csv`](../files-modified.csv) (appended for P1 commit).
