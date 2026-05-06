---
language: en
status: active
initiative: 62-mission-control
report_kind: impeccable-shape
program_id: shared
plane: ops
authority: Founder + Operator
last_review: 2026-05-06
---

# Impeccable shape — `/operator-inbox`

> **P0 artefact.** Operator approval gate before P5 build starts.
> Anchors: [`master-roadmap.md`](../master-roadmap.md), [`OPERATOR_INBOX.md`](../../OPERATOR_INBOX.md) (the AKOS-side render), [`scripts/render_operator_inbox.py`](../../../../../scripts/render_operator_inbox.py).

## 1. Audience and job-to-be-done

The **Operator** (level 4) wakes up, opens this page, and triages:

1. What is **open against me / mixed-owned** today?
2. Ordered by RICE descending — what's the highest-leverage thing I should do first?
3. For the top item, what's the **next concrete action** + **how do I unblock it**?

Secondary: filter by program / plane / cycle / owner_class; mark items "in progress" or "done" (which writes to `OPS_REGISTER.csv` via the AKOS PR flow, not directly into Supabase).

## 2. What's there today

`OPERATOR_INBOX.md` is auto-rendered AKOS-side from `OPS_REGISTER.csv` (status=open AND owner_class IN (operator, mixed) ORDER BY rice_score DESC). I59 P4 ships the renderer. The ERP side is greenfield — we present the same data with row affordances (drawer drill-down, snooze, "in progress" toggle).

## 3. Information architecture

```
[Page header]
  Eyebrow:  Operations · Operator Inbox
  Title:    What's open against me
  Subtitle: Ranked by RICE, sourced from OPS_REGISTER.csv (last sync 19:42 UTC)
  Filters:  [Program ▾] [Plane ▾] [Owner ▾] [Cycle ▾] [Saved view ▾]   [Search]   [Export CSV]

[Empty state when filters return 0 rows]
  Illustration: numbered checklist with all boxes ticked
  Title:        "Inbox zero"
  Subline:      "Nothing is open against you in this filter scope. Nice."

[Table — TanStack Table with virtualization above 200 rows]
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ ▾ │ Rank │ ID         │ Title                          │ Owner   │ RICE  │
  ├───┼──────┼────────────┼────────────────────────────────┼─────────┼───────┤
  │ ▸ │   1  │ OPS-58-2   │ OpenAI key rotation            │ operator│ 149   │
  │ ▸ │   2  │ OPS-57-1   │ Live AKOS_RECORD_LIVE window   │ mixed   │ 142   │
  │ ▸ │   3  │ OPS-55-1   │ Wave-2 voice profile fill      │ operator│ 118   │
  │ ▸ │   4  │ OPS-59-1   │ Telemetry promotion merge      │ operator│  95   │
  └─────────────────────────────────────────────────────────────────────────┘

[Right-side drawer — opens on row click via Vaul]
  Header:  OPS-58-2 · OpenAI key rotation
  Body:
    RICE breakdown:    R 9  ·  I 4  ·  C 0.7  ·  E 0.17  →  149
    Owner class:       operator
    Initiative:        I58 (closed); next-cycle window
    Provider:          OpenAI
    Cadence:           quarterly per POL-API-KEY-ROTATION-V1
    Linked decision:   D-IH-58-G
    Linked report:     reports/ops-58-1-2026-05-06.md
    Acceptance:        New key configured in ~/.openclaw/.env, old key revoked, cycle log entry added

  Actions:
    [ Mark in progress ]  [ Snooze 24h ]  [ Open AKOS PR template ]  [ Copy ID ]
    [ View on AKOS-side OPERATOR_INBOX.md ]

[Saved views — left-rail collapsible]
  · Default (everything open against me)
  · This cycle only
  · Mixed-owned (collaboration)
  · High RICE only (≥ 100)
  · [+ New view]

[Footer ribbon]
  Last sync 2026-05-06 19:42 UTC · click to refresh · /status
```

## 4. Brand and Impeccable laws applied

- **Numbered indicators on rank** (`01`–`NN`), tabular-nums, right-aligned. Operator scans top-3 by ordinal.
- **No decorative chrome**. The table is the surface; nothing competes with it.
- **Density toggle** in the page-level kebab menu: compact (44px row) / standard (52px) / comfortable (60px).
- **Sticky filter bar** at the top; sticky pagination at the bottom; never two scrollbars.
- **Empty state is a destination**, not an error: cream-warm card, encouraging copy, suggests next saved view.
- **Color is semantic only**: rank stays neutral; only the RICE badge picks up `oklch(72% 0.13 195)` (teal) at ≥100 and `oklch(78% 0.16 65)` (amber) at <50.
- **Reduced motion respected.** Drawer slide animation skipped when `prefers-reduced-motion`.
- **All actions keyboard-reachable.** `j/k` to navigate rows, `Enter` to open drawer, `Esc` to close, `g i` for "go to operator inbox", `?` for shortcut overlay.

## 5. Permission matrix

| access_level | Can read | Can write |
|:---:|:---|:---|
| 6 (Founder) | All rows | "in progress" + "snooze" + impersonate |
| 4 (Operator) | All rows | "in progress" + "snooze" + saved views |
| 2-3 (Team) | Rows where `owner_class='mixed'` only | "in progress" on rows assigned to them |
| 1 (Advisor) | None — page is gated | None |

In demo mode (`app.data_mode = 'demo'`), the table is read-only regardless of access level (no writes against `demo.*`).

## 6. Acceptance criteria for P5

| ID | Criterion | Verification |
|:---|:---|:---|
| OI-A | Default sort: status=open AND owner_class IN (operator, mixed) ORDER BY rice_score DESC | Snapshot test |
| OI-B | RICE column shows R/I/C/E breakdown on hover (tooltip) and in drawer | Playwright |
| OI-C | Filters compose with `?program=PRJ-HOL-MAD-2026&plane=ops&cycle=I62` and survive page reload | Playwright |
| OI-D | "Mark in progress" updates `OPS_REGISTER.csv` via a generated PR template (no direct DB write) | Manual + unit test on PR template generator |
| OI-E | Saved views persist to `holistika_ops.user_preferences.saved_views[]` with shape `{ id, name, filters, sort }` | DB assertion + Playwright |
| OI-F | CSV export emits the visible rows with deterministic column order matching the table | Snapshot test |
| OI-G | Print stylesheet hides filter bar + drawer + actions; renders rank/ID/title/owner/RICE in a single readable column | Manual |
| OI-H | Empty state surfaces when 0 rows match; never a blank page | Playwright |
| OI-I | Page renders within budget on a 200-row inbox (LCP < 2.5s, virtualization at >200) | Lighthouse |
| OI-J | en / es / fr dictionaries declared inline | `npm run lint:i18n-parity` |
| OI-K | All actions keyboard-reachable; `?` opens shortcut overlay | axe-core + Playwright |

## 7. Cross-reference

This page consumes the same SSOT as the AKOS-side `OPERATOR_INBOX.md`. They diverge on **affordances** (the ERP has snooze + drawer + saved views; the markdown is read-only) but **never on content**. Drift is caught by:

- A weekly cron job comparing the row set in `OPERATOR_INBOX.md` (parsed) to `erp.vw_operator_inbox_top` (queried). Any delta logs to `compliance.repo_health_snapshot_mirror.akos_erp_inbox_drift`.

## 8. Operator approval line

> **Approve this shape doc to start P5 (Operator Inbox drilldown).**
> Approval signature: ____________________ · date: ____________________
