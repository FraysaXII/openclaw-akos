---
language: en
status: charter
initiative: 64-governance-mission-control
report_kind: decision-log
last_review: 2026-05-07
---

# Decision log — Initiative 64

## D-IH-64-A — I64 as a sibling initiative to I62 + I63, not a phase of either

- **Date:** 2026-05-07
- **Decision:** Charter I64 (Governance Mission Control) as its own
  initiative folder rather than tacking it onto I62 (operator
  dashboard) or I63 (External Repo Bless Pattern codification).
- **Rationale:** I62 is product-shaped (operator dashboard for
  MADEIRA + ERP). I63 is governance-shaped (canonical CSV / SOP
  codification of the bless loops). I64 is integration-shaped
  (rendering the I63 governance loops as I62-style operator UI).
  Each initiative reads cleaner with its own audit trail.
- **Alternative considered:** Fold the dashboard into I62 P11+.
  Rejected: I62 closed at P10 with its own UAT; reopening would
  blur its scope.

## D-IH-64-B — 6-panel layout, not single-feed feed

- **Date:** 2026-05-07
- **Decision:** The dashboard surfaces 6 distinct panels (repo health
  grid, bless action, drift inbox, secret rotation, broadcast log,
  SOP/decision-log) rather than a Twitter-style single feed.
- **Rationale:** Each panel has a different cadence, owner, and
  interaction model. A single feed would conflate read-only health
  signals with action-oriented controls, increasing operator error.
- **Implication:** P2 ships read-only first (panels 1, 4, 6); P3 adds
  action panels (2, 3, 5); ordering reduces blast radius if the
  action wiring needs more time.

## D-IH-64-C — Re-use AKOS scripts via GitHub Actions, not re-implement in TS

- **Date:** 2026-05-07
- **Decision:** When the dashboard needs to bless / regen / broadcast,
  it triggers a GitHub Actions workflow which calls the existing AKOS
  Python script. The dashboard itself never re-implements the
  business logic.
- **Rationale:** The Python scripts are the canonical, tested,
  governance-aware implementations (Track K + L). Re-implementing in
  TS would create a second source of truth and double the maintenance
  burden. Per the AKOS rule "Reuse/extension only (no duplication)".
- **Implication:** P1 ships three reusable GH Actions workflows (one
  per loop). The dashboard's frontend is presentation + workflow
  trigger only.

## D-IH-64-D — Dashboard data via Supabase, not direct AKOS GitHub API reads

- **Date:** 2026-05-07
- **Decision:** Repo health, drift state, and broadcast log read from
  Supabase tables populated by AKOS automation, not by direct
  GitHub API calls from the dashboard.
- **Rationale:** Supabase already has RLS posture for cross-repo
  governance data (per I59 P1.1). Direct GitHub API reads would
  require Sentry-tier secret management on the frontend, hit GitHub
  rate limits per page-view, and undermine the existing demo-mode
  toggle.
- **Implication:** P1 adds one new Supabase table
  (`governance.canonical_change_log`) and updates AKOS automation to
  upsert into it on each invocation. Existing tables
  (`compliance.repository_registry_mirror`,
  `compliance.repo_health_snapshot_mirror`) cover the rest.
