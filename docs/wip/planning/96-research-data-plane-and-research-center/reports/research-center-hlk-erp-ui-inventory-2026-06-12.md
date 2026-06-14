---
parent_initiative: INIT-OPENCLAW_AKOS-96
report_kind: ui-inventory
authored: 2026-06-12
audience: J-OP;J-AIC
implementation_repo: root_cd/hlk-erp
---

# Research Center — hlk-erp UI inventory (2026-06-12)

**Repo:** `c:\Users\Shadow\cd_shadow\root_cd\hlk-erp`  
**Consumer initiative:** I96 Research Data Plane & Research Center  
**Purpose:** Dashboard/UI reuse inventory for **Phase B journey-aware insight widgets** (P9b revision tranche)  
**Scope:** shadcn, charts, dashboard shells, design tokens, layout, existing Research Center surface

---

## Executive summary

hlk-erp is a **Next.js 14 + shadcn/ui + Tailwind CSS variables** app with a mature component library (54 `components/ui/*` files), a **Recharts wrapper** (`components/ui/chart.tsx`), and a **partially built Research Center v2** (11 components + 4 BFF routes). Phase A polish is largely landed in code (semantic freshness pills, remediation stack layout, POV Select @375, drawer T1/T3 tiers, `LensEmptyState`, CTA copy/toast). **Phase B is mostly net-new presentational components** plus **BFF expansion** in `lib/research-center/insights.ts` — the insight type system already anticipates Director/Finance cards but only Operator/Director remediation cards are populated today.

---

## shadcn components

**Config:** `c:\Users\Shadow\cd_shadow\root_cd\hlk-erp\components.json` — style `default`, baseColor `neutral`, CSS variables, Lucide icons.

**Inventory (54 files under `components/ui/`):**

| Category | Components | Phase B relevance |
|:---|:---|:---|
| **Layout / chrome** | `sidebar`, `separator`, `scroll-area`, `resizable` | Reuse for page shell; no RC-specific sidebar |
| **Surfaces** | `card`, `sheet`, `drawer` (vaul), `dialog`, `alert`, `alert-dialog` | **Reuse** — insight cards, drill-down drawer |
| **Navigation** | `tabs`, `accordion`, `collapsible`, `breadcrumb`, `navigation-menu`, `menubar` | **Reuse** — v1 audit accordion, drawer T3 collapse |
| **Input / control** | `button`, `badge`, `toggle`, `toggle-group`, `select`, `checkbox`, `switch`, `slider`, `input`, `textarea`, `form`, `label`, `calendar`, `input-otp` | **Reuse** — POV switcher, CTAs, severity badges |
| **Feedback** | `toast`, `toaster`, `sonner`, `progress`, `skeleton`, `tooltip`, `hover-card`, `popover` | **Reuse** — runbook copy feedback (Sonner) |
| **Data display** | `table`, `responsive-table`, `chart`, `mermaid`, `avatar`, `carousel`, `command`, `pagination` | Table in drawer govern section; **chart unused in RC today** |
| **Mobile** | `use-mobile.tsx` | Available for responsive patterns |

**Provider guardrails:** `.cursor/rules/providers.mdc` + `__tests__/guards/providers.spec.ts` — direct `recharts` imports forbidden outside `components/ui/chart.tsx` (legacy `components/dashboard/*` exempt).

---

## Chart libraries

| Library | Version | Entry point | RC usage |
|:---|:---|:---|:---|
| **Recharts** | `latest` (~3.8) | `components/ui/chart.tsx` | **Not used in Research Center** |
| Legacy dashboard | direct recharts | `components/dashboard/{bar-chart,line-chart,pie-chart,overview}.tsx` | Demo/legacy only — **avoid for Phase B** (Impeccable bans hero-metric templates) |

**Phase B guidance:** Insight widgets should stay **card + badge + sentence** shaped (GOJ matrix, Impeccable IF-03). If charts are needed later (Director ICS sparkline), use `@/components/ui/chart` only — not legacy dashboard charts.

---

## Design tokens

| Asset | Path | Notes |
|:---|:---|:---|
| **Primary CSS variables** | `app/globals.css` | `--background`, `--foreground`, `--card`, `--muted`, `--destructive`, `--border`, `--radius`, **sidebar-*** tokens |
| **Extended themes** | `app/globals.css` | `.dark`, `.dark-blue`, `.light-blue`, `.brown`, `.white` |
| **Tailwind mapping** | `tailwind.config.ts` | Maps HSL vars to `bg-card`, `text-muted-foreground`, `sidebar.*` |
| **Chart tokens** | `styles/globals.css` (secondary) | `--chart-1` … `--chart-5` light/dark |
| **Theme provider** | `components/theme-provider` + `next-themes` | System + 7 named themes in root layout |

**Phase B reuse:** Freshness pills, badges, cards already use semantic tokens (`border-border`, `bg-muted/50`, `Badge variant`). **Do not** reintroduce hardcoded `bg-emerald-50` / `bg-amber-50` (IF-01).  
**Gap:** `components/freshness/freshness-ribbon.tsx` (global footer) still uses light-only amber/red — out of RC scope but same anti-pattern.

---

## Layout shells

| Shell | Path | Pattern | RC fit |
|:---|:---|:---|:---|
| **Root app layout** | `app/layout.tsx` | Sticky header + `SidebarNav` + main scroll + `FreshnessRibbon` footer | Research Center inherits this (not operator-segment) |
| **Operator segment** | `app/(operator)/layout.tsx` | Auth gate + `StaleBanner` | RC is **outside** `(operator)` — uses `requireLevel(4)` on page |
| **RC page wrapper** | `app/research-center/page.tsx` | `container mx-auto px-4 py-8` | Current shell — extend, don't replace |
| **Dashboard shell** | `components/dashboard/dashboard-shell.tsx` | Simple responsive grid gap | Too generic; prefer RC-specific rhythm (IF-02) |
| **Mission Control** | `app/(operator)/mission-control/page.tsx` | Hero + numbered tile grid | **Pattern reference** for verdict/hero tone — not drop-in |
| **Mission Control tile** | `components/mission-control/tile.tsx` | Numbered eyebrow + Card | Reusable **visual language** for future "program health chip" |
| **Governance verdict band** | `components/governance/verdict-band.tsx` | Sentence-shaped band (I64) | **Reuse pattern** for `ProgramHealthSummary` / `VerifyBanner` copy shape |

**Navigation:** Research Center linked from `config/site.tsx`, `components/sidebar-nav.tsx`, `components/mobile-nav.tsx` (Overview + Facts sub-routes).

---

## Existing dashboard pages

| Route | Path | Reusable for Phase B? |
|:---|:---|:---|
| **Mission Control** | `app/(operator)/mission-control/page.tsx` | Tile grid + hero verdict — **pattern only** |
| **Compliance pulse** | `app/(operator)/compliance-pulse/page.tsx` | Governance pulse tiles |
| **Eval quality** | `app/(operator)/eval-quality/page.tsx` | Quality/regression surfaces |
| **Planning workspace** | `app/(operator)/planning/**` | Initiative/roadmap links for Director CTAs |
| **Legacy dashboard** | `app/dashboard/page.tsx` | Stat-card grid + placeholder charts — **anti-pattern for RC** (IF-03/IF-04) |
| **Tech lab data-viz** | `app/tech-lab/data-viz/page.tsx` | Chart demos |
| **RC Facts (v1)** | `app/research-center/facts/page.tsx` | Large legacy facts UI — separate from v2 insight rail |

**Stat card primitive:** `components/dashboard/stat-card.tsx` — large `text-2xl` numerals; **do not reuse** on T0 insight face (Impeccable IF-03).

---

## Research Center folder (6.1–6.3)

### 6.1 Components (`components/research-center/`)

| File | Role | Phase B disposition |
|:---|:---|:---|
| `research-center-client.tsx` | Page composition: header → strip → prong → rail → accordion | **Extend** — mount Phase B chrome here |
| `pov-switcher.tsx` | 5 lenses; Select @sm-, ToggleGroup scroll @sm+ | **Reuse as-is** |
| `freshness-strip.tsx` | 3-badge ledger/radar/KiRBe strip | **Extend → FreshnessStripV2** (micro-CTA per badge) |
| `prong-strip.tsx` | BL-* prong chips from ledger BFF | **Reuse** (Director discover) |
| `insight-card-rail.tsx` | ≤7 cards, remediation stack, Sheet drawer T1/T2/T3 | **Extend** — extract `InsightRailHeader`; POV-specific layouts |
| `lens-empty-state.tsx` | Per-lens empty copy + CTA | **Reuse / extend** for Auditor/Finance/Compliance stubs |
| `v1-panels-accordion.tsx` | Collapsed default audit panels | **Reuse** |
| `ledger-summary-panel.tsx` | Accordion T3 ledger aggregate | **Reuse** (audit tier) |
| `radar-queue-panel.tsx` | Register excerpt table | **Reuse**; has `isBlockGovern` row highlight |
| `wip-packs-panel.tsx` | WIP pack list | **Reuse** |
| `kirbe-search-panel.tsx` | KiRBe health/search | **Reuse** |

### 6.2 Lib / BFF (`lib/research-center/` + `app/api/research-center/`)

| Module | API route | Live today |
|:---|:---|:---|
| `insights.ts` | `GET /api/research-center/insights?pov=` | **Remediation only** (ledger zero, radar empty, KiRBe unhealthy) for operator + director |
| `ledger-stats.ts` | `GET /api/research-center/ledger-stats` | Prong breakdown, completion % |
| `radar-queue.ts` | `GET /api/research-center/radar-queue` | Overdue + block_govern counts |
| `kirbe-health.ts` | via `GET /api/kirbe/health` | Execute-plane probe |
| `wip-packs.ts` | `GET /api/research-center/wip-packs` | GitHub WIP list |
| `queries.ts` | React Query hooks | Client data layer |
| `types.ts` | — | **Insight types already include** `intent_criticality`, `settlement_risk`, `staleness`, `drift`, `env_deploy`, `evidence_gap` |

### 6.3 Auth & tests

- Route gate: `lib/auth/route-matrix.ts` — `/research-center` + `/api/research-center/*` require level 4  
- E2E: `tests/e2e/research-center.spec.ts`  
- Dev sign-in: `app/api/dev/sign-in/route.ts` → `?next=/research-center`

---

## Phase B reusable vs net-new (7.1–7.5 summary table)

Mapped to P9b §Phase B + GOJ journey-component matrix.

### 7.1 Shared journey chrome (all lenses)

| Planned component | Verdict | Reuse from | Net-new work |
|:---|:---|:---|:---|
| **JourneyStepIndicator** | **Net-new** | No stepper in repo; closest: Mission Control tile ordinals | New `components/research-center/journey-step-indicator.tsx`; wire in `research-center-client.tsx` |
| **FreshnessStripV2** | **Extend** | `freshness-strip.tsx` | Add micro-CTA `Button` per badge (run sweep / open status / env checklist) |
| **InsightRailHeader** | **Partial → extract** | Inline h2 in `insight-card-rail.tsx` | Extract component; add lens label + count + "≤7 signals" hint |
| **VerifyBanner** | **Net-new** | Pattern: `GovernanceVerdictBand`, `MissionControlHero` sentence shape | Post-CTA banner + freshness re-check prompt; client state after copy/run |

### 7.2 Operator lens

| Planned component | Verdict | Notes |
|:---|:---|:---|
| **RemediationPriorityStack** | **Mostly done** | `insight-card-rail.tsx` uses `flex flex-col gap-3` when `remediationFirst` |
| **EnvGapCallout** | **Extend BFF + small UI** | `readerConfigured` flags exist on ledger/radar/wip BFFs; add inline callout when false |
| **RunbookCopyBlock** | **Reuse** | Already in drawer T1 (`InsightDrillDownSheet`) |
| **Staleness overdue card** | **Net-new BFF** | Types exist; need `insights.ts` card from `radar-queue` overdue rows |
| **Mirror drift / env deploy / WIP stale cards** | **Net-new BFF** | Conditional T2 cards per matrix — no UI primitive beyond existing `InsightCardItem` |

### 7.3 Director lens

| Planned component | Verdict | Notes |
|:---|:---|:---|
| **IntentCriticalityCard** | **Net-new** | Type `intent_criticality` in types; **no BFF population**; needs ICS data source or placeholder |
| **ProgramHealthSummary** | **Net-new** | Chip/band linking freshness clearance; pattern from `MissionControlTile` eyebrow |
| **Ledger completion card** | **Net-new BFF** | Data in `ledger-stats.ts`; not yet an insight card |
| **Phase blocker card** | **Net-new BFF** | Needs initiative/roadmap reader |
| **Prong coverage mini-strip** | **Reuse** | `prong-strip.tsx` already on all lenses |

### 7.4 Auditor / Finance / Compliance (stubs)

| Planned component | Verdict | Notes |
|:---|:---|:---|
| **ReadOnlyCtaBanner** | **Net-new** | RBAC-aware banner; disable runbook copy for auditor POV |
| **SettlementRiskPlaceholder** | **Extend** | `LensEmptyState` finance copy exists; upgrade to structured placeholder card |
| **BlockGovernPlaceholder** | **Extend** | `LensEmptyState` compliance copy + radar `blockGovernCount` in strip |

### 7.5 Summary table

| Category | Count | Items |
|:---|:---|:---|
| **Reuse as-is** | 8 | POV switcher, prong strip, v1 accordion, lens empty (base), drawer T1 runbook, Sonner toasts, shadcn Card/Badge/Sheet, React Query hooks |
| **Extend existing** | 6 | FreshnessStrip→V2, insight rail header/stack, env callout, lens empty stubs, `research-center-client` layout rhythm |
| **Net-new UI** | 4 | JourneyStepIndicator, VerifyBanner, ReadOnlyCtaBanner, InsightRailHeader (if not extract-only) |
| **Net-new BFF / insights** | 8+ | Director cards (ICS, completion, phase blocker), staleness/drift/env/WIP cards, POV-specific card filtering |

**Charts for Phase B:** **Not recommended** — matrix and Impeccable bar favor cards + badges + sentence bands.

---

## Recommended build order

1. Extract **InsightRailHeader** + add **JourneyStepIndicator** (pure UI, no BFF).  
2. **FreshnessStripV2** micro-CTAs (wire to existing runbook commands).  
3. Expand **`insights.ts`** for Director: ledger completion + radar overdue (data already in parallel fetches).  
4. **VerifyBanner** client state after primary CTA.  
5. Auditor/Finance/Compliance: upgrade **LensEmptyState** → dedicated placeholder components.  
6. Optional: **ReadOnlyCtaBanner** when `pov === "auditor"`.

---

## Verification

```powershell
cd c:\Users\Shadow\cd_shadow\root_cd\hlk-erp
npm run typecheck
npm run lint
npx playwright test --grep research-center
```

Manual: `http://localhost:3010/api/dev/sign-in?next=/research-center` @ 375/768/1280, all five POV lenses.

---

## Cross-references

| Doc | Path |
|:---|:---|
| P9b revision plan Phase B | `docs/wip/planning/96-research-data-plane-and-research-center/reports/p9b-revision-tranche-plan-2026-06-12.md` |
| Journey component matrix | `docs/wip/intelligence/governed-operator-journey-ux-uat-2026-06-12/journey-component-matrix-2026-06-12.md` |
| Page spec v2 | `docs/wip/planning/96-research-data-plane-and-research-center/reports/research-center-page-spec-v2-2026-06-12.md` |
| Operator check-links | `docs/wip/planning/96-research-data-plane-and-research-center/reports/operator-check-links-2026-06-12.md` |
