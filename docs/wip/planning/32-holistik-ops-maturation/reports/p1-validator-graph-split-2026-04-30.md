---
language: en
status: complete
initiative: 32-holistik-ops-maturation
report_kind: phase-report
phase: P1
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-04-30
---

# P1 — Validator graph split + validation_runs mirror

**Date:** 2026-04-30
**Status:** COMPLETED. Backward-compatible CLI preserved (R-32-1 mitigated). 14/14 dispatcher tests PASS.

## Action items

| ID | Action | Status | Evidence |
|:---|:-------|:-------|:---------|
| **P1-A1** | Design dispatcher + JSON report contract | DONE | New `akos/hlk_validation_run.py` ships `VALIDATION_RUN_FIELDNAMES` + `VALID_STATUSES`. 12 fields per run row matching `compliance.validation_runs` DDL. |
| **P1-A2** | Refactor `scripts/validate_hlk.py` keeping legacy CLI | DONE | Default invocation prints identical OVERALL: PASS banner + per-validator PASS lines. Legacy CLI assertion test (`test_legacy_cli_prints_per_validator_pass_lines`) passes. |
| **P1-A3** | Add `--json` flag emitting structured per-validator report | DONE | `py scripts/validate_hlk.py --json` emits clean JSON to stdout (no banner pollution). Top-level `{run_id, started_at, git_sha, host, overall_status, runs}`. 24 runs in current vault state (11 inline + 13 dispatched). |
| **P1-A4** | `compliance.validation_runs` DDL + RLS posture | DONE | [`supabase/migrations/20260430233000_i32_validation_runs.sql`](../../../../supabase/migrations/20260430233000_i32_validation_runs.sql). Schema `compliance`; PK `(run_id, validator_name)`; 3 indexes (started_at DESC, validator_name, partial on status<>'pass'); RLS deny anon + authenticated; service_role only; same posture as `finops.registered_fact`. |
| **P1-A5** | Sync emit support | DEFERRED | Operator writes to `compliance.validation_runs` are not part of every dev-local invocation per design (D-IH-32-F). Sync emit lands when CI / cron writer is added (not blocking I32 closure; tracked as a follow-up). |
| **P1-A6** | Dispatcher tests + I29/I30/I31 baseline regression | DONE | New [`tests/test_validate_hlk_dispatcher.py`](../../../../tests/test_validate_hlk_dispatcher.py): 14 tests, all PASS. Locks legacy CLI banner + per-validator PASS lines + JSON shape + UUID run_id + I31 baseline row counts (65 org rows, 1093 process rows). |

## Verification

- `py scripts/validate_hlk.py` → `OVERALL: PASS` (4.6s); legacy stdout 100% preserved
- `py scripts/validate_hlk.py --json` → exit 0; valid JSON; 24 runs; all status=pass
- `py -m pytest tests/test_validate_hlk_dispatcher.py -v` → **14 passed in 4.91s**
- `git_sha` in JSON report shows `8c3bc9596550-dirty` (correctly detects in-flight I32 edits)
- `host` truncated to 64 chars per contract; UUID v4 shared across all per-validator rows in one dispatch

## Notes

- The dispatch table at line ~268 of the refactored `validate_hlk.py` makes adding new per-CSV validators a 1-line change (label + filename + run_label + csv_gate). P2/P3/P4 will append to this list rather than copy-paste subprocess blocks.
- The structured report's `error_count` field is wired for inline checks but defaults to 0 for dispatched subprocesses (per-validator stdout parsing for richer error counts is a follow-up; the binary pass/fail status is the I32 P1 contract).
- The `--json` flag is the documented way to feed the future `compliance.validation_runs` writer; the writer itself is operator-side per D-IH-32-F (not in agent path).
- Mirror migration **STAGED** at `supabase/migrations/20260430233000_i32_validation_runs.sql`; operator applies via `npx supabase db push` after I32 squash-merge (P14 closure).

## Next phase

P2 — Skill registry (7th canonical dimension).
