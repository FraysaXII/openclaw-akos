---
language: en
status: active
initiative: 62-mission-control
report_kind: risk-register
last_review: 2026-05-06
---

> **Superseded hosts (2026-06-13):** Showcase host is **`showcase.holistikaresearch.com`**. See [I96 P-G1](../../96-research-data-plane-and-research-center/reports/subdomains-registry-reconciliation-proposal-2026-06-13.md).

# I62 Risk Register

| ID | Risk | Likelihood | Impact | Mitigation | Owner |
|:---|:---|:---:|:---:|:---|:---|
| **R-62-1** | AKOS DDL gate slows execution because P1.3 + P2.3 + P3.1 each propose a separate SQL gate | Medium | Medium | Batch all three SQL proposals in **one** review session at P0/P2 boundary; operator approves once for the entire schema set | Founder |
| **R-62-2** | Demo data drifts from live schema shape after AKOS-side migrations | Medium | Low | `seed-demo.ts` reads live `compliance.*` schema and asserts column parity; CI fails on drift | AI Engineer |
| **R-62-3** | Founder impersonation feature abused or accidentally left enabled in production | Low | High | Audit-log every start/stop with IP + UA; weekly Founder review of `audit_log WHERE action LIKE 'impersonate.%'`; gate visible only at access_level 6 | System Owner |
| **R-62-4** | Showcase deploy accidentally leaks real `SUPABASE_SERVICE_ROLE_KEY` | Low | Critical | Separate Vercel project (no shared env); code-level guard `if (DATA_MODE === 'demo' && process.env.SUPABASE_SERVICE_ROLE_KEY) throw`; CI assertion that showcase build fails when service-role key is set | System Owner |
| **R-62-5** | Brand-jargon lint creeps onto operator surfaces and breaks legitimate internal copy | Low | Medium | Strict path glob `app/showcase/**` + `app/(marketing)/**`; never extends to `app/(operator)/**`; documented in [BRAND_JARGON_AUDIT.md](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_JARGON_AUDIT.md) §3 register split | Brand Manager |
| **R-62-6** | Mirror sync lag misleads operator into thinking governance is current when it's stale | Medium | Medium | Freshness ribbon + 24h yellow / 48h red banners; `erp.vw_mirror_health` returns last_sync_at per mirror | AI Engineer |
| **R-62-7** | Vendor lock-in (Supabase) blocks future migration | Low | Low | Schemas portable to vanilla Postgres; auth could move to Auth.js; no Supabase-specific extensions on critical paths; documented in `docs/architecture.md` | System Owner |
| **R-62-8** | RBAC drifts from AKOS access-level over time as roles change in `baseline_organisation.csv` | Medium | Medium | Daily sync job from `compliance.baseline_organisation_mirror` to `holistika_ops.user_role_mapping` reconciles; deltas surfaced in operator inbox | AI Engineer |
| **R-62-9** | Lighthouse perf budget too tight for the seven-tile board | Medium | Low | If LCP > 2.5s after P9 polish, defer non-critical tiles to client-side hydration after FCP; document in P9.2 report | AI Engineer |
| **R-62-10** | `showcase.holistikaresearch.com` URL becomes confusable with the AKOS Madeira agent endpoint | Low | Low | Add subtitle on showcase landing page: "Live demo of the Holistika operations console"; future agent public surface TBD | Brand Manager |
| **R-62-11** | First-time team-member onboarding fails because `holistika_ops.user_role_mapping` is empty | High | Medium | First-login flow at `/auth/role-resolve`: if no row, show "request access from <Founder name>" message; Founder grants in `/mission-control/admin/users` | Founder |
| **R-62-12** | Cmd+K palette query latency unacceptable on 10k+ row mirrors | Medium | Low | Server-side full-text search via Supabase RPC `mission_control_search`; client-side fuzzy filter only on the top 200 results | AI Engineer |
| **R-62-13** | Time-travel queries blow up Supabase egress (point-in-time PIT scans) | Low | Medium | Daily snapshot table `erp.daily_snapshot` populated by a small cron Edge Function; time-travel reads from snapshot, not from PIT | AI Engineer |
| **R-62-14** | AI assist (Cmd+J) leaks confidential rows when the user's access_level is below threshold | Medium | High | RPC `mission_control_ask` always re-applies RLS for the calling user; Madeira agent endpoint verified to honour `service_role` boundary; explicit test in P9.1 | AI Engineer |
| **R-62-15** | Sentry retention too short for advisor share-out incidents (free tier 90d) | Low | Low | Critical incident reports archived to `docs/wip/planning/62-mission-control/reports/incidents/` within 30 days; upgrade to paid Sentry only if incident frequency demands it | System Owner |
| **R-62-16** | DR drill RTO miss because Vercel + Supabase + DNS + secrets all need coordinated restore | Medium | High | Quarterly DR drill restoring staging from yesterday's `pg_dump`; runbook with explicit DNS-cutover steps; warm standby Supabase project optional later | System Owner |
| **R-62-17** | Subdomain registry drift when ad-hoc Vercel subdomains added without PR | High | Low | `validate_subdomains_registry.py` queries Vercel MCP and fails on registry/Vercel mismatch; adds drift to `repo_health_snapshot_mirror` | DevOPS |
| **R-62-18** | Operator overwhelmed by notifications drawer noise | Medium | Low | Sensible defaults (only validation_runs failures + three-lights flips + cycle closures); user-tunable thresholds in `/settings/notifications`; "Snooze 24h" affordance per category | Founder |

## Cycle-1 specific risks (will close at P11 if not earlier)

| ID | Risk | Mitigation status |
|:---|:---|:---|
| **R-62-C1** | First UAT (P11.5) finds a category of bugs (RBAC matrix mismatch, demo data shape drift) that requires re-running P1 or P2 | Mitigation: P1 + P2 each end with a small UAT row before P3 starts; matrix mismatch caught at P1 close, demo drift caught at P3 close |
| **R-62-C2** | Three Lights logic disagrees with `MADEIRA_HARDENING_CONSOLIDATED_PLAN.md` Part H definitions | Mitigation: Three Lights view body is sourced verbatim from Part H formulas; diverges only when Part H itself changes (caught by AKOS validators) |
| **R-62-C3** | Showcase advisor preview triggers brand-jargon violation in copy that wasn't covered by the lint glob | Mitigation: P11.5 includes a manual brand-voice scan of every showcase string before declaring closure |
