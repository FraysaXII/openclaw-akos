---
language: en
status: charter
initiative: 64-governance-mission-control
initiative_id: INIT-OPENCLAW_AKOS-64
report_kind: master-roadmap
program_id: shared
plane: ops
authority: Founder + System Owner
last_review: 2026-05-07
---

# Initiative 64 — Governance Mission Control (in hlk-erp)

**Folder:** `docs/wip/planning/64-governance-mission-control/`
**Status:** **Charter** — created 2026-05-07 alongside I63 P5 close as a sibling initiative to [I62](../62-mission-control/master-roadmap.md) (operator dashboard for MADEIRA + ERP) and [I63](../63-external-repo-governance-codification/master-roadmap.md) (external repo governance codification). Promotion to `active` requires operator approval of the page spec in [`reports/page-spec-2026-05-06.md`](reports/page-spec-2026-05-06.md).

## Outcome

Render the External Repo Bless Pattern as a first-class operator
surface inside hlk-erp at `/operator/governance/external-repos/`, so
the governance health that today lives in `REPO_HEALTH_SNAPSHOT.csv`
+ release-gate stdout + Slack pings becomes a single visual control
plane with one-click drill-down + (optionally) write actions.

The 6-panel surface:

1. **Repo health grid** — one row per `REPOSITORY_REGISTRY.csv` row.
   Columns: blessed Y/N, last_blessed_at, drift status (✓/⚠/✗), CI
   posture score, license OK, sentry OK, last commit on main, secrets
   nearing expiry. Color-coded.
2. **"Bless this repo" action panel** — picker over un-blessed registry
   rows → triggers a GitHub Actions workflow that runs
   `bless_external_repo.py --auto-pr` for the selected slug. Renders
   the resulting PR URL.
3. **Drift inbox** — list of detected drifts across all repos with
   one-click "open auto-PR" per row. Optimistic UI; confirms when the
   PR URL is returned.
4. **Secret rotation calendar** — heatmap of upcoming/overdue rotations
   per repo, ranked by urgency. Reads from each blessed repo's
   `.github/.akos-bless/` SHA stamps + the runbook frontmatter.
5. **Canonical change broadcast log** — last 30 days of canonical CSV
   changes + which consumer repos got pinged + their type-regen status.
   Backed by an append-only Supabase table populated by
   `notify_consumers_of_canonical_change.py`.
6. **SOP + decision-log surface** — for each automated process, link
   to the active SOP (`SOP-EXTERNAL_REPO_BLESSING_001` etc.) and the
   decision-log entry that authorized it. Closes the "governance is
   just docs" gap by surfacing the doctrine inside the operator UI.

Plus a **summary panel on the existing MADEIRA Mission Control
dashboard** rendering "X blessed repos, Y drifting, Z secrets due
this week" so the governance health is visible without leaving the
home page.

## Why now

- I62 (Mission Control) shipped the operator dashboard chrome but did
  not surface external-repo governance — that surface ended in
  release-gate stdout.
- I63 (External Repo Bless Pattern + governance codification) shipped
  the data + canonical SOPs + 9 automation scripts. Without I64, the
  health of those loops is invisible to a non-CLI operator.
- Operator-stated need (2026-05-07): *"Shouldn't we have a magnificent
  control for this and more in hlk-erp?"* — yes, this initiative is
  that control.

## Scope decisions

| In scope | Out of scope |
|:---|:---|
| Read-only governance dashboard (panels 1, 4, 5, 6) | Generic "monitor everything" dashboard |
| Trigger actions via GitHub Actions workflows (panels 2, 3) | Long-running operations executed in the browser |
| Reuse existing AKOS Python scripts as the truth-source via REST | Re-implementing the bless / drift / regen logic in TS |
| Supabase table `governance.canonical_change_log` for panel 5 | Net-new canonical CSVs in AKOS |
| Auth via existing hlk-erp middleware (operator-only RBAC) | Public/anonymous access |
| Locale: en + es per existing hlk-erp i18n parity check | New languages |

## Asset classification (per [`PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md))

See [`asset-classification.md`](asset-classification.md). Summary:

- **Canonical (proposed)**: 1 new Supabase migration for the
  `governance.canonical_change_log` table; rendering of repo health
  data is computed from existing canonical sources.
- **Mirrored / derived**: TypeScript types under
  `hlk-erp/lib/types/akos-mirrors.generated.ts` regenerated from
  `regen_consumer_types.py` (already wired in I63).
- **Reference-only**: this charter folder.

## Phase dependency

```mermaid
flowchart TD
    P0[P0 Charter + page spec]
    P1[P1 Backend: GitHub Actions wrappers + Supabase change log table]
    P2[P2 Frontend: panels 1, 4, 6 (read-only)]
    P3[P3 Frontend: panels 2, 3, 5 + summary tile on MADEIRA home]
    P4[P4 RBAC + audit logging + dry-run / live toggle]
    P5[P5 UAT + docs + I64 closure]

    P0 --> P1
    P1 --> P2
    P2 --> P3
    P2 --> P4
    P3 --> P5
    P4 --> P5
```

## Phases

### P0 Charter + page spec

- This folder: `master-roadmap.md`, `decision-log.md`, `asset-classification.md`, `evidence-matrix.md`, `risk-register.md`.
- `reports/page-spec-2026-05-06.md` — the operator-facing UI specification (panel-by-panel data contracts, route plan, RBAC matrix, error-state behaviour).
- README.md row added under `docs/wip/planning/README.md`.

**Verification**: Operator review approves the page spec.

### P1 Backend wiring

Two pieces:

1. **GitHub Actions wrappers** (in AKOS) — three reusable workflows
   under `.github/workflows/`:
   - `governance-bless-repo.yml`: workflow_dispatch input `slug`,
     runs `py scripts/bless_external_repo.py --repo-slug $slug
     --auto-pr`, returns PR URL via job summary.
   - `governance-regen-types.yml`: similar shape for
     `regen_consumer_types.py --repo-slug $slug --auto-pr`.
   - `governance-broadcast-change.yml`: similar shape for
     `notify_consumers_of_canonical_change.py --changed $csv`.
2. **Supabase `governance.canonical_change_log` table** + RLS — append
   on each `notify_consumers_of_canonical_change` invocation; mirror
   pattern from I59 P1.

**Verification**: GitHub Actions dry-runs succeed; Supabase migration
applies cleanly to staging; insert via service-role works.

### P2 Frontend panels 1, 4, 6 (read-only)

- `app/operator/governance/external-repos/page.tsx`: top-level page.
- `components/governance/repo-health-grid.tsx`: panel 1.
- `components/governance/secret-rotation-calendar.tsx`: panel 4.
- `components/governance/sop-decision-log-surface.tsx`: panel 6.
- `lib/governance/data.ts`: server-side data fetchers reading from
  Supabase + AKOS canonical mirrors.

**Verification**: Playwright e2e covers the read paths; Lighthouse
scores ≥90 on perf/a11y; type regen test passes.

### P3 Frontend panels 2, 3, 5 + home tile

- `components/governance/bless-action-panel.tsx`: panel 2.
- `components/governance/drift-inbox.tsx`: panel 3.
- `components/governance/canonical-broadcast-log.tsx`: panel 5.
- `components/governance/home-summary-tile.tsx`: tile on the MADEIRA
  home page.

**Verification**: Playwright e2e covers a full "find drift → click
auto-PR → see PR URL" flow against a sandbox repo.

### P4 RBAC + audit + safety

- Tighten the `/operator/governance/*` route to operator-only (already
  the default; verify against middleware).
- Audit log every write action (panel 2, 3, 5 invocations) to
  Supabase `governance.action_audit`.
- Confirm-modal pattern for any action that would open a real PR or
  send a real Slack message (no surprise side effects).
- Demo data mode toggle (existing hlk-erp pattern) so the dashboard
  is presentable without secrets configured.

### P5 UAT + closure

- Operator UAT walking through every panel with a real bless / drift
  / change-broadcast flow.
- Docs: USER_GUIDE §24.13 ¶4 documents the dashboard.
- I64 closure decision logged.

## Verification matrix

| Phase | Command |
|:---|:---|
| P0 | Operator review approves page spec |
| P1 | `gh workflow run governance-bless-repo.yml -f slug=hlk-erp` returns success; Supabase migration applies on staging |
| P2 | `pnpm test:e2e -- --grep governance-read`; `pnpm lighthouse` ≥90 |
| P3 | `pnpm test:e2e -- --grep governance-write` |
| P4 | RBAC penetration check (anonymous → 403; non-operator → 403); audit log table populated |
| P5 | UAT report at `reports/uat-i64-2026-05-XX.md` + I64 master-roadmap flips closed |

## Cross-references

- [I62](../62-mission-control/master-roadmap.md) — sibling. Mission Control on hlk-erp.
- [I63](../63-external-repo-governance-codification/master-roadmap.md) — sibling. Codified the governance loops we now visualise.
- [`SOP-EXTERNAL_REPO_BLESSING_001`](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/External%20Repos/SOP-EXTERNAL_REPO_BLESSING_001.md) — bless action SOP (panel 2).
- [`SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001`](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/External%20Repos/SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001.md) — drift action SOP (panel 3).
- [`SOP-CROSS_REPO_SCHEMA_PROPAGATION_001`](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/Cross%20Repo/SOP-CROSS_REPO_SCHEMA_PROPAGATION_001.md) — broadcast action SOP (panel 5).
- [`secrets-walkthrough-2026-05-06.md`](../63-external-repo-governance-codification/reports/secrets-walkthrough-2026-05-06.md) — operator-side secrets the dashboard reflects.
