# Initiative 22a — Post-closure follow-ups + Wave-2 bootstrap

**Folder:** `docs/wip/planning/22a-i22-post-closure-followups/`
**Status:** **Closed (P1–P6 complete; P7 Supabase parity reconciled 2026-05-04 via D-IH-OPS-1/2/3).** Two upstream emit-script defects spun out as open follow-ups (see "Open follow-ups").
**Authoritative Cursor plan:** `~/.cursor/plans/hlk_scalability_wave_2_initiatives_639a02d7.plan.md` (Pre-Wave §1-§5 of Wave-2 plan).
**Initiative 22 stays closed** — see [`22-hlk-scalability-and-i21-closures/master-roadmap.md`](../22-hlk-scalability-and-i21-closures/master-roadmap.md). This folder carries the few items that fell out of I22's closure as actionable follow-ups + the Wave-2 unblocker (operator-answers YAML + scaffolder).

## Outcome

Five items, each addressed in [`reports/post-closure-followups-20260429.md`](reports/post-closure-followups-20260429.md):

1. **`supabase migration list` parity check** — operator slot.
2. **`mmdc` install** (pinned `@^11`) — operator slot.
3. **FINOPS / TECHOPS second-CSV assessment** — recommendation: **DO NOT ADD**. Persistent re-eval-trigger template lands in I26-P0.
4. **Planning README slot 27 reservation** — `(reserved)` row added to [`docs/wip/planning/README.md`](../README.md) so Wave-2 (23-26) lands contiguously.
5. **Operator-answers YAML + scaffolder bootstrap** — the single artifact the rest of Wave-2 depends on. Files:
   - [`operator-answers-wave2.yaml`](operator-answers-wave2.yaml) — pre-filled with derivable values; sentinels for the rest.
   - [`scripts/wave2_backfill.py`](../../../../scripts/wave2_backfill.py) — single-command scaffolder (`--dry-run`, `--section`, `--check-only`).
   - Verify profile `wave2_backfill_check` in [`config/verification-profiles.json`](../../../../config/verification-profiles.json).

## Phase at a glance

| Phase | Purpose | Key deliverable | Status |
|:-----:|:--------|:----------------|:------:|
| **P1** | Operator parity check + mmdc install | one-line evidence rows in the report | DONE (2026-05-04 via P7) |
| **P2** | FINOPS / TECHOPS assessment | DO-NOT-ADD recommendation captured | DONE |
| **P3** | Planning README slot 27 reservation | `(reserved)` row added | DONE |
| **P4** | Operator-answers YAML bootstrap | YAML pre-filled; sentinels for Tier-3 cells | DONE |
| **P5** | Scaffolder bootstrap | `wave2_backfill.py` + verify profile + tests | DONE |
| **P6** | Verification | `validate_hlk*` green; YAML loads; `--check-only` reports pending sentinels | DONE |
| **P7** | Supabase MasterData parity reconciliation | 28 ledger entries; 17/17 mirrors row-for-row to canonical CSV; advisor regression GREEN; idempotency rehearsed | DONE (2026-05-04, D-IH-OPS-1/2/3) |

## Verification matrix

- `py scripts/validate_hlk.py`
- `py scripts/validate_hlk_vault_links.py`
- `py scripts/wave2_backfill.py --check-only` (reports pending sentinels per section; informational, not blocking until phases consume the YAML)
- `py -m pytest tests/test_wave2_backfill.py -v`

Per [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc): operator UAT row in the report records P1 outcomes by date.

## Out of scope (explicit)

- Reopening Initiative 22 (closed). All artifacts under this folder.
- Filling the operator-answers YAML — that is operator work, batched, ~5-7 hours.
- Wave-2 phase work (I23/I24/I25/I26) — pending pre-execution clearance + YAML fill.

## Open follow-ups (P7 Supabase apply spinoff)

Two upstream defects in `scripts/verify.py compliance_mirror_emit` were detected during the per-table batch apply (2026-05-04). Both are 1-row-per-cycle severity (cosmetic at scale) and were patched locally in the gitignored batch files; rows are in canonical state on the database. **Filing for proper upstream fix in the next maintenance window:**

| Follow-up | Bug | Fix scope | Suggested owner |
|:----------|:----|:----------|:----------------|
| **F-22a-EMIT-1** | Empty CSV cell for DATE columns emitted as `''` instead of `NULL`. Hit on `compliance.sourcing_register_mirror.last_engagement_date`. | `scripts/verify.py compliance_mirror_emit` value coercion: detect empty strings for DATE/TIMESTAMP columns and emit `NULL`. Add a regression test. | System Owner |
| **F-22a-EMIT-2** | Empty CSV cell for NOT NULL bool columns (no default) emitted as `NULL`. Hit on `compliance.skill_registry_mirror.tools_required_waived`. | Same script: emit column-aware default for NOT NULL booleans (most semantically `false`); fail loudly if no default is known instead of silently producing `NULL`. Add a regression test. | System Owner |

Both defects observable in [`reports/uat-i24-supabase-apply-20260504.md`](reports/uat-i24-supabase-apply-20260504.md) "Manual patches applied" section.

## Links

- [Reports](reports/post-closure-followups-20260429.md)
- [Operator-answers YAML](operator-answers-wave2.yaml)
- [Wave-2 plan (Cursor)](~/.cursor/plans/hlk_scalability_wave_2_initiatives_639a02d7.plan.md)
- [I22 closure](../22-hlk-scalability-and-i21-closures/master-roadmap.md)
- [Backfill scaffolder](../../../../scripts/wave2_backfill.py)
