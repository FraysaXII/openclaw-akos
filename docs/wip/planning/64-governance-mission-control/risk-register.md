---
language: en
status: charter
initiative: 64-governance-mission-control
report_kind: risk-register
last_review: 2026-05-07
---

# Risk register — Initiative 64

| Id | Risk | Likelihood | Impact | Mitigation |
|:---|:---|:---|:---|:---|
| R-64-1 | Dashboard write actions trigger unintended PRs / Slack pings | M | H | Confirm-modal pattern for any write action; demo-mode + `--dry-run` tier; feature flag `GOVERNANCE_WRITE_ACTIONS_ENABLED` defaults off in non-prod. |
| R-64-2 | GH Actions workflow secret expansion exposes a token | L | H | Use fine-grained `GH_PAT_AUTOPR` PAT scoped to consumer repos only; rotate per `secret_rotation_reminders.py` cadence; never echo into job summaries. |
| R-64-3 | Supabase `governance.canonical_change_log` grows unbounded | L | M | Append-only table with 365-day TTL via Supabase scheduled function; index on (changed_at DESC); query the dashboard via TanStack Query with sane page sizes. |
| R-64-4 | Frontend re-implements bless / drift logic and drifts from AKOS | M | H | D-IH-64-C explicitly forbids this; PR review checklist enforces "all governance writes go through GH Actions wrappers". |
| R-64-5 | Operator misreads the dashboard and acts on stale data | M | M | Each panel renders `last_synced_at` timestamp + "refresh" button; staleness ≥5min triggers a banner; SHA-stamp footer documents the source SHA of every signal. |
| R-64-6 | Adding a 7th panel becomes a slippery slope | M | M | Panel count locked in D-IH-64-B; new requests open a follow-up initiative or a P-NN extension. |
| R-64-7 | RBAC misconfiguration leaks governance data to non-operators | L | H | E2E test `governance-rbac.spec.ts` (anonymous → 403; non-operator → 403); audit log every read access in P4. |
| R-64-8 | Dashboard breaks the existing MADEIRA Mission Control home if the home tile errors | M | M | Home tile uses an isolated error boundary; failed load renders "governance unreachable" without breaking siblings. |
| R-64-9 | Dependency on Supabase being up — dashboard goes blank during outage | L | M | Each panel renders a degraded state from cached data + last-known timestamps; the AKOS canonical CSVs themselves are the ultimate source-of-truth. |
| R-64-10 | Localisation drift (en vs es) | L | L | Existing `pnpm check-i18n-parity` script (already wired in hlk-erp) gates every PR. |
