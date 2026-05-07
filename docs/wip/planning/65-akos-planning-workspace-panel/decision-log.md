---
language: en
status: active
initiative: 65-akos-planning-workspace-panel
report_kind: decision-log
last_review: 2026-05-07
---

# I65 Decision Log

Format: ID · question · options considered · decision · rationale · date · status.

## D-IH-65-A — Panel placement

- **Q.** Where should the AKOS planning workspace panel live in `hlk-erp` so operators can find it intuitively?
- **Options.**
  1. **Enhance `/operator/initiatives`** in place — promote the existing CSV-registry table to a full panel by appending tabs for decisions/operations/reports.
  2. **Nest under `/mission-control/planning/`** — keep all panels under MC.
  3. **New top-level operator group `/operator/planning/`** — sibling to `/operator/governance/`, parallel to `/operator/initiatives`, `/operator/decisions`, `/operator/cycle-closures`.
- **Decision.** Option 3 — new top-level group `/operator/planning/`. The existing `/operator/initiatives`, `/operator/decisions`, `/operator/cycle-closures` drilldowns stay as they are (registry-rolled views, accessed from MC tiles); the new `/operator/planning/` group is the workspace-aware view that surfaces *folder content* (master-roadmap.md, reports/*, decision-log.md as text) rather than registry rows.
- **Rationale.** Two routes ≠ duplication when they answer different questions. `/operator/initiatives` answers "what do my CSV registries say?" `/operator/planning/` answers "what's in `docs/wip/planning/`?" — the former is registry truth, the latter is workspace truth. They share data sources and cross-link, but their reading order is different. Nesting under MC (option 2) would tip MC's tile count to 8 and break J-MC-1 (the 8-second glance). Enhancing `/operator/initiatives` (option 1) would mix two reading orders and confuse personas.
- **Implication.** I65 introduces a new operator-route segment; existing routes are unchanged. The MADEIRA Mission Control hero gets one new chip (parallel to I64's governance chip), no new tile.
- **Date.** 2026-05-07 · **Status.** Active.

## D-IH-65-B — Markdown rendering source

- **Q.** Where does the rendered markdown for `master-roadmap.md`, `decision-log.md`, and `reports/*` come from at request time?
- **Options.**
  1. **Live GitHub Contents API** — fetch raw markdown on each request, MDX-compile server-side, 60s TanStack Query cache.
  2. **Nightly Supabase mirror** — a job that ingests every `docs/wip/planning/**` markdown file into a `governance.workspace_markdown_mirror` table; serve from the table.
  3. **Deploy-time prebuild** — the hlk-erp Vercel build pulls AKOS at build time and bakes the markdown into the bundle.
- **Decision.** Option 1 — live GitHub Contents API with 60s in-memory + TanStack Query cache, plus an optional `?ref=<sha>` for time-travel.
- **Rationale.** GitHub is the SSOT; mirror lag would mean operators read stale planning data on a Friday afternoon when the relevant Markdown was edited 20 minutes ago. Mirror also doubles the storage cost and adds an ingestion failure mode. Deploy-time prebuild bakes the workspace into the bundle and forces a redeploy on every doc change — unacceptable. The 60s cache is enough to cushion bursts of clicks; rate-limit headroom on the GitHub API is comfortable for an internal-only operator surface (typical traffic <100 reqs/hour). The fallback for a GitHub outage is a graceful "live workspace temporarily unavailable, last known state from <timestamp>" banner backed by a 5-minute TTL secondary cache in Supabase (this falls back, not the primary path).
- **Implication.** P1 ships `lib/planning/github-reader.ts` + the secondary 5-minute cache. The primary table created by P1 is `governance.planning_workspace_view` (joins over already-mirrored CSVs); markdown body content does *not* live in Supabase.
- **Date.** 2026-05-07 · **Status.** Active.

## D-IH-65-C — Time-travel implementation

- **Q.** Should v1 of the panel support "what did the workspace look like N days ago"?
- **Options.**
  1. **No time-travel in v1** — only render `main` HEAD; defer.
  2. **`?ref=<sha>` query string** — pass through to the GitHub Contents API call; UI shows a "Viewing historical state at <date>" banner with "back to live" chip.
  3. **Supabase historical snapshots** — daily snapshot job stores diffs; UI lets operator pick from a calendar.
- **Decision.** Option 2 — `?ref=<sha>` query string (and `?ref=<branch>` for advisor preview branches), plus a date-picker UI helper that resolves a date to the most-recent merged commit on `main` at that time.
- **Rationale.** Git already stores history. Building Supabase historical snapshots duplicates git and risks drift between the two stores; option 3 is rejected for v1. Option 1 (no time-travel) is rejected because cycle closures and post-mortems frequently need "what was active 14 days ago"; without it the panel is half-useful. Option 2 leverages git natively, costs zero extra storage, and the only complexity is the date→SHA resolver, which is a one-shot REST call against `git rev-list --before`. The date-picker is a separate, small UI component (`components/planning/time-travel.tsx`) and is feature-flagged off if it's not ready by P3.
- **Implication.** Adds `lib/planning/time-travel.ts` (date→SHA resolver) and a banner chip `<TimeTravelBanner>`. RBAC: time-travel respects current access_level — historical content does not bypass RLS on registries.
- **Date.** 2026-05-07 · **Status.** Active.
