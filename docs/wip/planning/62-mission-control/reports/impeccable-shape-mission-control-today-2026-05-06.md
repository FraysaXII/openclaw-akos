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

# Impeccable shape — `/mission-control` (the Today board)

> **P0 artefact.** Operator approval gate before P4 build starts.
> Anchors: [`master-roadmap.md`](../master-roadmap.md), [PRODUCT.md](../../../../../PRODUCT.md), [DESIGN.md](../../../../../DESIGN.md), [BRAND_VISUAL_PATTERNS.md](../../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VISUAL_PATTERNS.md), Impeccable design laws (`.cursor/skills/impeccable/SKILL.md`).

## 1. Audience and job-to-be-done

Three audiences × one shared job:

- **Founder / System Owner (level 6)** — answer "Is the system safe to ship today?" in one screen, in under 15 seconds, before opening any drilldown.
- **Operator / PMO (level 4)** — answer "What is open against me, and where are the next operator gates?" with one glance + one click into the operator inbox.
- **Advisor / external observer (level 1, demo only)** — see a credible, brand-clean executive summary that proves the platform is real and well-governed.

The **single primary task**: parse the GO/AMBER/NO-GO verdict + last-cycle outcome + top-3 operator inbox items in **less than 3 visual hops**.

## 2. What's there today (audit)

The `app/dashboard/page.tsx` exists but reads `lib/data.ts` mock helpers (~2706 lines of seeded fakes). The `app/tech-lab/project-madeira/page.tsx` hard-codes "99.9% Uptime / 10x Faster / SOC 2 Compliant" — marketing voice on a stub with no real data. There's no Mission Control surface yet; we're shaping greenfield.

## 3. Brand and Impeccable laws applied

| Law | Application |
|:---|:---|
| **Single-screen verdict** | Hero band visible above the fold answers "GO / NO-GO" before any tile loads |
| **Honest numbers only** | Every numeric in the hero comes from `erp.vw_three_lights_status` joined to `validation_runs` + `dossier_run` — never hardcoded |
| **OKLCH brand palette** | Dark slate hero (`oklch(22% 0.05 220)`) + cream-warm cards (`oklch(96% 0.02 80)`) + teal accent (`oklch(72% 0.13 195)`) + amber alert (`oklch(78% 0.16 65)`); no raw hex anywhere |
| **Inter at scale 1.25** | h1 64/72px, h2 28/36px, body 16/24px, mono numbers tabular-nums |
| **Numbered indicators, no decorative ornaments** | Each tile gets a `01`–`07` prefix in eyebrow position; no chevrons, no shadows beyond `0 1px 0 hsla(0,0%,0%,0.04)` |
| **Reduced motion respected** | Tile last-sync soft-pulse only when `prefers-reduced-motion: no-preference` |
| **Keyboard-first** | Tab order: skip-link → verdict chip → seven tiles in reading order → Cmd-K hint → footer freshness ribbon |
| **Live regions** | Verdict chip is `role="status" aria-live="polite"`; data-staleness banner is `role="alert"` when red |
| **Locale toggle** | en / es / fr inline dictionary in page-level JSON; default from `navigator.language`; persisted to `holistika_ops.user_preferences.locale` after auth |

## 4. Information architecture

```
[Top bar — persistent across operator surfaces]
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ [Holística]  [Verdict chip · GO]  [Cmd+K]  [🔔]  [👤 founder ▾]      │
  └─────────────────────────────────────────────────────────────────────────┘

[Hero band — dark slate, full-width]
  Eyebrow:  Mission Control · Today · 2026-05-06
  Title:    GO ─ all three lights green
  Subline:  Last cycle closed 2026-05-06 · 1741/1748 tests · drift clean · MAX_DOSSIER_USD $5/$5
  Actions:  [ View last cycle dossier ]   [ Open operator inbox · 4 ranked ]

[Seven tiles — 4-col grid on desktop, 1-col on mobile, density-toggle 2-col]
  ┌── 01 Three Lights ──────────┬── 02 Operator Inbox preview ──────────┐
  │ ⬤ ⬤ ⬤  GREEN/GREEN/GREEN     │ Top 3 by RICE:                          │
  │ source: vw_three_lights      │  1. OPS-58-2  149                       │
  │ last sync: 2 min ago         │  2. OPS-57-1  142                       │
  │                              │  3. OPS-55-1  118                       │
  │                              │ 4 more → /operator-inbox                │
  ├── 03 Initiative pulse ──────┼── 04 Cost & finance ──────────────────┤
  │ closed/active/gated 35/4/12 │ MTD spend $42 / $80 envelope            │
  │ ▁▂▂▃▅▃▂▁ last 30 d closures  │ judge cap: $0 of $15 fired              │
  │                              │ endpoint: 0/3 alarmed                   │
  ├── 05 Compliance pulse ──────┼── 06 Eval summary ─────────────────────┤
  │ 16/16 mirrors green         │ pass-rate 99.7% (1741/1748)             │
  │ no drift                    │ persona alignment 100% (5w avg)         │
  │                              │ flake: 0 quarantined                    │
  ├── 07 Cycle timeline ────────┴───────────────────────────────────────┤
  │ ████████████████░░░  I59 closed → I62 P0 in flight → I60/I61 reserved│
  │                                                                       │
  └───────────────────────────────────────────────────────────────────────┘

[Footer — freshness ribbon]
  All mirrors fresh · last sync 2026-05-06 19:42 UTC · view /status
```

## 5. Three Lights — exact source

The hero verdict chip and tile 01 share one source. Definitions (verbatim from `MADEIRA_HARDENING_CONSOLIDATED_PLAN.md` Part H):

| Light | GREEN when | Source |
|:---|:---|:---|
| **Conversational** | persona-fit alignment ≥ 80% over the last 5 cycles | `compliance.eval_run` filtered to `kind='persona_fit'` |
| **Dossier** | most recent closure dossier emitted with `verdict=GO` and within `MAX_DOSSIER_USD` | `compliance.dossier_run` ORDER BY `started_at` DESC LIMIT 1 |
| **Skill quality** | every active skill in SKILL_REGISTRY has at least one passing eval_run in the last 7 days | `compliance.skill_registry` JOIN `compliance.eval_run` |

Composite verdict is the **min** of the three; AMBER if any light is yellow (degraded but not failing).

## 6. Tile microcopy (en, with es / fr dictionaries to follow)

| Tile | Eyebrow | Title | Body |
|:---|:---|:---|:---|
| 01 Three Lights | `01 · System verdict` | `Three Lights` | "Conversational · Dossier · Skill quality — composite verdict drives the hero." |
| 02 Operator Inbox | `02 · Open against you` | `Operator Inbox` | "Top 3 ranked by RICE; click to triage." |
| 03 Initiative pulse | `03 · Cycle motion` | `Initiative pulse` | "Active vs gated vs closed; last 30 days." |
| 04 Cost & finance | `04 · Spend posture` | `Cost & finance` | "MTD vs envelope, with per-cell breakdown." |
| 05 Compliance | `05 · Mirror health` | `Compliance pulse` | "16 mirrors. Last sync per dimension." |
| 06 Eval summary | `06 · Quality bar` | `Eval summary` | "Live pass-rate, persona alignment, flake count." |
| 07 Cycle timeline | `07 · Where we are` | `Cycle timeline` | "Closed → in-flight → reserved candidate slots." |

## 7. Acceptance criteria for P4

| ID | Criterion | Verification |
|:---|:---|:---|
| MC-A | OKLCH palette + tokens declared as CSS custom properties; no raw hex except `transparent` | Stylelint custom rule `no-raw-hex` |
| MC-B | Tab focus visible on every actionable element; Cmd-K opens command palette from anywhere | Playwright + axe-core |
| MC-C | Verdict chip is `role="status" aria-live="polite"`; freshness banner switches to `role="alert"` at >24h | Playwright DOM assertion |
| MC-D | en / es / fr dictionaries declared inline; copy never hardcoded outside dictionary | `npm run lint:i18n-parity` |
| MC-E | Each tile renders within 200ms of mount on cold cache (Lighthouse desktop, throttled 4G) | Lighthouse CI per-route assertion |
| MC-F | Three Lights values match `erp.vw_three_lights_status` exactly; no client-side computation | Playwright assertion comparing DOM to mocked RPC return |
| MC-G | All numbers are tabular-nums, right-aligned in cards, with deterministic decimal precision | Snapshot test |
| MC-H | Hero verdict text + last-cycle line legible at 320px wide without horizontal scroll | Playwright viewport test |
| MC-I | Brand-jargon scan passes on the page (no `AKOS`, `topic_*`, `RBAC`, `RLS`) when rendered in showcase mode | `npm run lint:jargon -- --route /mission-control` |
| MC-J | Density toggle (compact/standard/comfortable) persists to `holistika_ops.user_preferences.density` | Playwright + DB assertion |

## 8. Operator approval line

> **Approve this shape doc to start P4 (Mission Control build).**
> Approval signature: ____________________ · date: ____________________
