---
initiative_id: INIT-OPENCLAW_AKOS-96
report_kind: aic-design-pipeline-handoff
authored: 2026-06-12
audience: J-OP;J-AIC
status: active
linked_spec: reports/research-center-page-spec-v2-2026-06-12.md
excalidraw_scene_id: 2yBmIbavOEj
excalidraw_url: https://app.excalidraw.com/s/9pWFxghRFBg/2yBmIbavOEj
handoff_repo: root_cd/hlk-erp
figma_mint_owner: AIC execution seat
operator_gate: inline-ratify on preview URL only
figma_path_status: minted_cursor_figma_mcp_2026-06-12
figma_file_key: GTCcxT0DbEWdnVHXyrde73
figma_url: https://www.figma.com/design/GTCcxT0DbEWdnVHXyrde73/Holistika-ERP-Research-Center-v2
---

# Research Center v2 — AIC design pipeline handoff

Operator approved P9 re-ratify (2026-06-12, post research rework `9699478d`). **Mockup/prototype work is AIC-owned** — handoff runs **between agent seats**, not to the operator as builder. The operator **ratifies** preview URLs (inline-ratify); agents mint wireframes, Figma, and Next.js implementation.

## Three-seat pipeline (binding)

| Seat | Model class | Tool / surface | Deliverable | Status |
|:---|:---|:---|:---|:---|
| **1 — Thinking** | Opus-class | Excalidraw MCP | Wireframe scene | **Done** — `2yBmIbavOEj` |
| **2 — Execution** | Composer-class | Cursor Figma MCP (`use_figma`) → Composio Figma → Figma REST | Governed Figma file + registry draft row | **Minted** — Cursor Figma MCP 2026-06-12; file on Fay's team (`GTCcxT0DbEWdnVHXyrde73`); Holistika team `planKey` invalid; placeholder frames + operator ratify URL |
| **3 — Execution** | Composer-class | Impeccable + hlk-erp Next.js | Live UI against Figma Dev Mode or Excalidraw parity | **P10 in progress** |

**Operator gate:** inline-ratify on **localhost preview URL** (`http://localhost:3010/research-center?pov=…`) or Figma share link when minted — **not** manual Figma construction.

## Figma mint path (execution seat — not operator work)

Priority order for seat 2:

1. **Composio Figma** — `COMPOSIO_SEARCH_TOOLS` + `COMPOSIO_MANAGE_CONNECTIONS` (toolkit `figma`) when connected; mint file under Holistika team.
2. **Figma REST** — personal access token via env (`FIGMA_ACCESS_TOKEN`); programmatic frame create per frame list below.
3. **Interim — Excalidraw+ high-fidelity** — expand scene `2yBmIbavOEj` with one frame per POV lens at 1280 + mobile 375; document explicit gap: *Figma blocked on Composio connection; not operator-deferred work*.

**2026-06-12 mint (Cursor Figma MCP):** File created on Fay's team — https://www.figma.com/design/GTCcxT0DbEWdnVHXyrde73/Holistika-ERP-Research-Center-v2 — placeholder frames per minimum frame list. Holistika team (`team::1359995555907300869`) returned `Invalid planKey`; operator may move file when team billing resolves. `generate_figma_design` html-to-design capture blocked in Cursor browser (CSP); live UI parity verified via localhost UAT screenshot.

**Prior probe:** Composio returned `has_active_connection: false` for toolkit `figma`. Superseded by Cursor Figma MCP for this mint.

## Wireframe reference (seat 1 — done)

| Asset | Value |
|:---|:---|
| Excalidraw collection | `I96 Research Center v2` (`10Y5nfqK4De`) |
| Scene | `I96 RC v2 — wireframes 2026-06-12` |
| Scene ID | `2yBmIbavOEj` |
| URL | https://app.excalidraw.com/s/9pWFxghRFBg/2yBmIbavOEj |

Frames in scene: (01) Hero + POV + freshness 1280, (02) Remediation trio, (03) Operator lens + drawer.

**Interim hi-fi expansion (seat 2 fallback):** add frames `RC-POV-Director-1280`, `RC-POV-Auditor-1280`, `RC-POV-Finance-1280`, `RC-POV-Compliance-1280`, `RC-Operator-375` to the same scene when Figma remains blocked.

## Figma file target (when connection unblocks)

| Field | Recommended value |
|:---|:---|
| File name | `HLK-ERP Research Center v2` |
| Team | Holistika (`team::1359995555907300869` or AIC workspace) |
| Class | `prototype` → promote to `design-system` component subset when stable |
| Page | `Research Center v2` |
| Breakpoint frames | 375 × 667 (mobile), 768 × 1024 (tablet), 1280 × 800 (desktop) |

## Frame list (minimum — execution seat mints)

| Frame ID | Name | Contents |
|:---|:---|:---|
| `RC-POV-Director-1280` | Director lens — desktop | Hero, POV=Director selected, freshness strip v2, 5–7 insight cards (intent-criticality sort) |
| `RC-POV-Operator-1280` | Operator lens — desktop | Remediation trio **above** rail; staleness-sorted cards; one card selected → drawer |
| `RC-POV-Auditor-1280` | Auditor lens — desktop | Evidence/RBAC cards; redacted CTA variant (doc links only) |
| `RC-POV-Finance-1280` | Finance lens — desktop | Settlement-risk cards |
| `RC-POV-Compliance-1280` | Compliance lens — desktop | block_govern + drift cards |
| `RC-Remediation-1280` | Remediation trio (isolated) | Three critical cards: ledger-zero, radar-empty, kirbe-unhealthy |
| `RC-Drawer-Open-1280` | Drill-down drawer | Summary, three-plane row, artifact link, runbook command, initiative hook |
| `RC-Operator-375` | Operator lens — mobile | Stacked POV tabs, remediation cards full-width, rail scroll, drawer full-screen sheet |
| `RC-Accordion-1280` | v1 panels secondary | Collapsed accordion label + one expanded panel preview |

## Component inventory → code mapping

| Figma component | shadcn / library | hlk-erp target | Notes |
|:---|:---|:---|:---|
| `InsightCard` | `Card`, `CardHeader`, `CardFooter`, `Badge`, `Button` | `components/research-center/insight-card.tsx` (new) | severity → Badge variant; type chip → outline Badge |
| `RemediationCard` | Same + `destructive` border | extends `InsightCard` `type=remediation` | Always critical; render first |
| `PovSwitcher` | `Tabs` or segmented `ToggleGroup` | `components/research-center/pov-switcher.tsx` | Persist `?pov=` + sessionStorage |
| `FreshnessBadge` | Custom pill (extend v1) | `components/research-center/freshness-strip.tsx` | Add micro-CTA button per badge |
| `DrillDownDrawer` | `Sheet`, `SheetContent`, `ScrollArea` | `components/research-center/insight-drawer.tsx` | Right sheet desktop; full sheet mobile |
| `ThreePlaneRow` | `Table` (TanStack) | `components/research-center/three-plane-row.tsx` | Single-row table from field mapping |
| `Sparkline` (optional) | **Recharts** `LineChart` | inside drawer only | Not on glance rail |
| ~~Tremor Metric~~ | **Not used** | — | P9 spike: defer Tremor dep; shadcn Card sufficient |

## Dev Mode / token alignment (hlk-erp)

Map Figma variables to existing Tailwind / CSS tokens (see [`BRAND_VISUAL_PATTERNS.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_VISUAL_PATTERNS.md) §1 and hlk-erp `app/globals.css`):

| Semantic | Figma variable | Tailwind / CSS | Usage |
|:---|:---|:---|:---|
| Page background | `color/background` | `bg-background` | Shell |
| Card surface | `color/card` | `bg-card` | Insight cards |
| Critical | `color/destructive` | `border-rose-200 bg-rose-50 text-rose-900` | Matches v1 freshness error tone |
| Warning | `color/warning` | `border-amber-200 bg-amber-50 text-amber-900` | warning severity |
| OK | `color/success` | `border-emerald-200 bg-emerald-50 text-emerald-900` | info/ok badges |
| Primary CTA | `color/primary` | `bg-primary text-primary-foreground` | Button default |
| Muted detail | `color/muted-foreground` | `text-muted-foreground` | one-line detail |
| Radius | `radius/md` | `rounded-md` | Cards, badges |
| Font | `font/sans` | Geist / Inter stack | Match ERP layout |

Typography scale for Dev Mode:

| Role | Size | Weight |
|:---|:---|:---|
| Hero title | 30–36px | semibold |
| Card headline | 16–18px | medium |
| Card detail | 12–14px | regular |
| CTA button | 14px | medium |
| Type chip | 11–12px | medium, uppercase optional |

## FIGMA_FILES_REGISTRY.csv row (draft — do not commit without operator CSV gate)

```csv
# file_slug,figma_url,team_key,class,primary_owner_role,topic_ids,linked_yaml_ssot,notes
# holistika-erp-research-center-v2,https://www.figma.com/design/GTCcxT0DbEWdnVHXyrde73/Holistika-ERP-Research-Center-v2,team::1297934312456731046,prototype,Brand Manager,topic_brand_visual_identity,docs/wip/planning/96-research-data-plane-and-research-center/reports/research-center-page-spec-v2-2026-06-12.md,"I96 Track D v2 Research Center insight machine. Frames: 5 POV lenses + remediation trio + drawer + mobile 375. Excalidraw wireframe 2yBmIbavOEj. Minted Cursor Figma MCP 2026-06-12 (Fay team; Holistika planKey invalid)."
```

After mint: add `paths.figma_url` to any KM manifest if Output-1 registration is required.

## P10 entry checklist (AIC-owned)

1. Execution seat mints Figma file (Composio or REST) **or** expands Excalidraw hi-fi frames with gap note documented above.
2. Execution seat implements Next.js against Excalidraw + this spec (Figma URL optional until P11 divergence row).
3. Remediation cards land first (P10 #1 binding).
4. Operator inline-ratifies preview URL when ready — **does not build Figma**.
5. Playwright `research-center-v2.spec.ts` covers POV switch + remediation visibility.

## Cross-references

- Page spec v2: [`research-center-page-spec-v2-2026-06-12.md`](research-center-page-spec-v2-2026-06-12.md)
- Implementation spec: [`implementation-spec-2026-06-12.md`](../../../intelligence/governed-actionable-analytics-surfaces-2026-06-12/implementation-spec-2026-06-12.md)
- MADEIRA experiential UAT charter (mockup ownership rule): [`charter.md`](../../../intelligence/aic-madeira-experiential-uat-2026-06-11/charter.md)
- Registry SSOT: [`FIGMA_FILES_REGISTRY.md`](../../../references/hlk/v3.0/Envoy Tech Lab/Repositories/FIGMA_FILES_REGISTRY.md)
