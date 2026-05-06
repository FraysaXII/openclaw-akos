---
language: en
status: active
initiative: 62-mission-control
report_kind: impeccable-shape
program_id: shared
plane: ops
authority: Founder + System Owner
last_review: 2026-05-06
---

# Impeccable shape — `/initiatives`

> **P0 artefact.** Operator approval gate before P5 build starts.
> Anchors: [`master-roadmap.md`](../master-roadmap.md), [`WIP_DASHBOARD.md`](../../WIP_DASHBOARD.md), `INITIATIVE_REGISTRY.csv`.

## 1. Audience and job-to-be-done

- **Founder (level 6)** — see every initiative across the program line, sliced by status taxonomy (`closed/archived/active/continuous/program_line/gated_external/gated_operator`), with a sparkline of progress + the next concrete action. Drill into the master-roadmap on click.
- **Operator (level 4)** — focus on `active` and `gated_*` rows; understand which decisions are blocking which initiative; spot stale rows (last_review > 14 d → freshness canary).
- **Advisor (showcase only)** — see anonymised but credible governance density: 60+ initiatives, a third closed, the rest in motion.

The **single primary task**: scan status sections, identify stalled or gated initiatives, click into one master-roadmap.

## 2. What's there today

`docs/wip/planning/WIP_DASHBOARD.md` (auto-rendered by `scripts/render_wip_dashboard.py`) groups initiatives into 8 sections by I59 status taxonomy. The ERP side is greenfield. We surface the same SSOT (`compliance.initiative_registry_mirror`) with row interactivity.

## 3. Information architecture

```
[Page header]
  Eyebrow:  Operations · Initiatives
  Title:    Program-line state
  Subtitle: 60+ initiatives across 7 status classes (last sync 19:42 UTC)
  Filters:  [Program ▾] [Plane ▾] [Status ▾] [Authority ▾]   [Search]   [Density ▾]

[Status taxonomy summary band — 7 chips]
  ─────────────────────────────────────────────────────────────────────────
  closed 35  archived 2  active 4  continuous 2  program_line 3  gated_external 1  gated_operator 12
  ─────────────────────────────────────────────────────────────────────────

[Sectioned table — TanStack Table grouped by status]
  ▾ Active (4)
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ ID  │ Title                              │ Owner    │ Last review │ Sparkline  │
  ├─────┼────────────────────────────────────┼──────────┼─────────────┼────────────┤
  │ I32 │ Holistik Ops Maturation             │ Founder  │ 2026-04-30  │ ▁▂▂▃▅▃▂▁  │
  │ I57 │ Cycle closeout live validation     │ Founder  │ 2026-05-04  │ ▁▁▂▃▅▅▆▇  │
  │ I59 │ HLK governance clean slate          │ Founder  │ 2026-05-06  │ ▁▂▃▅▆▇██  │
  │ I62 │ Mission Control                    │ Founder  │ 2026-05-06  │ ▁▁▁▁▁▁▁▁  │ ← in flight, no closure data yet
  └─────────────────────────────────────────────────────────────────────────────┘

  ▸ Continuous (2)   · ▸ Program-line (3)   · ▸ Gated external (1)   · ▸ Gated operator (12)

  ▸ Closed (35) — collapsed by default; click to expand chronological list

  ▸ Archived (2) — collapsed; reasons listed in drawer

[Right-side drawer — opens on row click]
  Header:  I59 · HLK governance clean slate
  Body:
    Status:               closed (2026-05-06)
    Cycle:                2026-Q2 cycle 3
    Authority:            Founder
    Inception decision:   D-IH-59-A
    Closure decision:     D-IH-59-N
    OPS open:             1 (OPS-59-1, telemetry promotion merge)
    Linked initiatives:   I60 candidate, I61 candidate
    Decision count:       14
    Reports:              p3-status-audit · p4-operator-inbox · p6-ops-58-3-rubric-fix · p7-telemetry-triage · p8-process-list-harmonisation-proposal · uat-i59-clean-slate

  Actions:
    [ Open master-roadmap on AKOS ]   [ Open decision-log ]   [ Open closure UAT ]
    [ Subscribe to changes ]          [ Copy citation ]
```

## 4. Brand and Impeccable laws applied

- **Status chips coloured by semantic, not by rainbow**: closed = neutral mute, archived = stripped chrome, active = teal, continuous = teal-muted, program_line = neutral plus cadence indicator, gated_external = amber, gated_operator = amber-strong.
- **Sparkline = 30-day decision-log activity**, not vanity metric. Empty bars for in-flight initiatives are honest, not embarrassing.
- **Initiative ID typography is `font-mono tabular-nums`** so I02 / I32 / I62 align in scan column.
- **Section collapse is sticky** — once you collapse "Closed (35)" the page remembers via `holistika_ops.user_preferences.expanded_sections`.
- **Cmd-K integration**: typing `i59` jumps directly to the initiative drawer; typing `mission control` matches via title.
- **Time-travel slot**: when the user picks "as-of 2026-04-30" from the global time-travel, this page re-queries `erp.vw_initiative_pulse_at(date)` and shows the state of the program line at that date. Visual cue: subtle eyebrow change to "Program-line state · 2026-04-30 (snapshot)".

## 5. Permission matrix

| access_level | Can read | Can write |
|:---:|:---|:---|
| 6 (Founder) | All rows | "subscribe" |
| 4 (Operator) | All rows | "subscribe" |
| 2-3 (Team) | Rows in their distance-band per `baseline_organisation` | "subscribe" |
| 1 (Advisor) | Closed + archived rows only (showcase mode displays anonymised summaries; production mode does not show this page) | None |

## 6. Acceptance criteria for P5

| ID | Criterion | Verification |
|:---|:---|:---|
| IN-A | Sections render for all 7 status taxonomy values; counts match `erp.vw_initiative_pulse` exactly | Snapshot |
| IN-B | Default expansion: active + gated_external + gated_operator open; rest collapsed | Playwright |
| IN-C | Sparkline source: `decision_register WHERE initiative_id = ? AND occurred_at > now() - 30d` grouped by day | Snapshot |
| IN-D | Filtering composes with `?status=active&program=PRJ-HOL-MAD-2026` and survives reload | Playwright |
| IN-E | Drawer "Open master-roadmap on AKOS" links to `https://github.com/FraysaXII/openclaw-akos/blob/main/docs/wip/planning/<NN-slug>/master-roadmap.md` | Unit |
| IN-F | Time-travel "as-of" toggle re-queries the view; eyebrow line changes; URL updates with `?asof=YYYY-MM-DD` | Playwright |
| IN-G | Page renders within budget on a 60-row dataset (LCP < 2.5s, no jank on section toggle) | Lighthouse |
| IN-H | Print stylesheet emits a single linear list grouped by status with title + ID + last review | Manual |
| IN-I | Page brand-jargon clean for showcase variant (no `AKOS`, `RBAC`, etc.); shows "Holística program line" instead of "AKOS planning workspace" in showcase | `npm run lint:jargon -- --route /initiatives --variant showcase` |

## 7. Cross-reference

The ERP page consumes `compliance.initiative_registry_mirror` and `compliance.decision_register_mirror` — both sourced from I59-shipped CSVs. The same data backs `WIP_DASHBOARD.md` AKOS-side; drift between ERP page and dashboard markdown is caught by:

- A nightly comparison job in `compliance.repo_health_snapshot_mirror`.

## 8. Operator approval line

> **Approve this shape doc to start P5 (Initiatives drilldown).**
> Approval signature: ____________________ · date: ____________________
