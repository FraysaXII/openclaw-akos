---
parent_initiative: INIT-OPENCLAW_AKOS-96
report_kind: visual-audit
scope: P9b NOT ratified — visual/broken only
authored: 2026-06-12
audience: J-OP;J-AIC
verdict: FAIL
linked_spec: reports/research-center-page-spec-v2-2026-06-12.md
linked_goj: docs/wip/intelligence/governed-operator-journey-ux-uat-2026-06-12/
screenshot_session: artifacts/uat-screenshots/i96-research-center-v2-2026-06-12/
---

# P9b visual audit — Research Center v2 (GOJ-UX-UAT)

Operator rejection stands: **advancement yes, ugly and broken.** This report is a compulsive screenshot review — not a functional/API audit. It compares live localhost captures against the **Research Center v2 Figma hi-fi** (P9b scope) and the **governed operator journey** content-disposition bar (plain language on cards; codes only in the audit accordion).

## Evidence reviewed

| Source | Path / URL | Notes |
|:---|:---|:---|
| Live cards @ 1280 | `artifacts/uat-screenshots/i96-research-center-v2-2026-06-12/04-tier-a-remediation-cards-1280.png` | **Re-captured** 2026-06-12 via Playwright |
| Live drawer @ 1280 | `artifacts/uat-screenshots/i96-research-center-v2-2026-06-12/05-tier-a-drawer-runbook-1280.png` | **Re-captured** 2026-06-12 |
| Prior POV capture | `artifacts/uat-screenshots/i96-research-center-v2-2026-06-12/01-pov-switcher-remediation-cards-1280.png` | Pre–Tier A copy; POV layout bug still visible |
| Prior drawer | `artifacts/uat-screenshots/i96-research-center-v2-2026-06-12/03-drill-down-sheet-ledger-validator-1280.png` | Pre-GOJ drawer structure |
| Figma Operator @ 1280 | `artifacts/uat-screenshots/i96-research-center-v2-2026-06-12/figma-operator-1280-ref.png` | MCP export node `1:3` |
| Figma drawer @ 1280 | `artifacts/uat-screenshots/i96-research-center-v2-2026-06-12/figma-drawer-1280-ref.png` | MCP export node `1:7` — **Figma frame itself truncated** |
| Manifest | `artifacts/uat-screenshots/i96-research-center-v2-2026-06-12/MANIFEST.json` | sha256 + capture timestamps |
| Live route | http://localhost:3010/api/dev/sign-in?next=/research-center | HTTP 200 at audit time |
| Figma URL | https://www.figma.com/design/GTCcxT0DbEWdnVHXyrde73/Holistika-ERP-Research-Center-v2?node-id=1-3 | Operator lens reference |

**Browser MCP:** not available in this execution seat. Fresh evidence obtained via `node scripts/_one_off/_i96_v2_uat_screenshot.js` in `hlk-erp` (Playwright @ 1280×800).

## Executive summary

The v2 **structure** landed (POV switcher, remediation rail, drill-down sheet, v1 accordion). The **operator experience** does not meet P9b or GOJ Tier A bars:

1. **Journey-aware UI is missing** — no lens guidance, no POV-specific “out of box” actions beyond three identical critical cards, and Auditor/Finance/Compliance lenses are empty shells.
2. **Freshness strip is still v1** — wrong semantics (Radar shows green while remediation says critical), no micro-CTAs, no git-vs-BFF story on the strip.
3. **Tier cards read as a debug console** — `fixture` badges, `BFF` jargon, and `localhost fixture — GitHub reader or env may be unset` are visible on the operator surface (T0), violating Strict T3.
4. **CTAs do not act** — every primary button opens the drawer; copy-command, open-route, env-checklist, and roadmap behaviors from the CTA taxonomy are not wired.
5. **Visual polish gaps** — POV switcher wraps awkwardly, drawer command truncates, three-plane table clips, and live ERP chrome diverges from isolated Figma frames.

**Verdict: FAIL** for P9b ratification. P10-T2 content disposition should remain paused until blockers below are addressed.

---

## Findings (severity × area)

### Blockers

| ID | Area | Finding | Screenshot ref | Suggested fix (plain language) |
|:---|:---|:---|:---|:---|
| **VIS-B01** | POV / journey | **Auditor, Finance, and Compliance lenses show no cards** — switching POV re-labels the page but the insight rail is empty except Operator/Director remediation. Spec requires ≥2–3 cards per lens when data exists; journey map expects tranche-2 Operator + Director first, but empty lenses look broken to an operator click-test. | `04-tier-a-remediation-cards-1280.png` (Operator only captured; code confirms `povShowsRemediation` gates cards) | Add lens-specific stub or live cards per page spec §2.1 (evidence, settlement risk, block_govern). Show a deliberate empty state with “switch to Operator lens” guidance — not a blank rail. |
| **VIS-B02** | Freshness strip | **Strip contradicts the remediation rail.** Radar badge is green (“0 targets current”) while the card below is critical (“staleness queue unavailable”). Ledger shows “No commit metadata” instead of v2 copy (“0 rows in BFF — env path” + action). No micro-CTA buttons on any badge (page spec §2.5). | `04-tier-a-remediation-cards-1280.png` vs Figma `figma-operator-1280-ref.png` | Align strip tone with card severity; add short why line + micro-CTA (Fix path / Run sweep / Review env). Match Figma v2 badge copy. |
| **VIS-B03** | Content / T3 | **Developer debug strings on T0 operator surface.** “localhost fixture — GitHub reader or env may be unset” appears beside the insight rail; every card carries a `fixture` chip; drawer and cards use **BFF** without plain-language bridge. Strict T3 says codes and engineering terms stay in the collapsed audit accordion only. | `04-tier-a-remediation-cards-1280.png`, `05-tier-a-drawer-runbook-1280.png` | Move fixture/env diagnostics to T3 accordion or a “Technical detail” expando inside the drawer. Replace BFF with “Research Center data reader” on T0–T2. |
| **VIS-B04** | CTA taxonomy | **Primary CTAs only open the drawer** — they do not copy the runbook command, open the govern artifact, open the KiRBe program roadmap, or start an env checklist. Operator journey expects glance → act in ≤2 steps; extra click with no action is friction. | `05-tier-a-drawer-runbook-1280.png` | Wire `cta_kind`: runbook → copy + toast; artifact → repo link; env_fix → checklist sheet; initiative_phase → roadmap route. Keep drawer as secondary detail. |
| **VIS-B05** | Missing components | **No user-journey or research/intelligence tactical UI.** Missing: lens picker guidance (“start here as Operator”), programme health summary, topic/WIP pack quick links on the v2 hero, freshness→card linking, Director intent-criticality cards, and POV-specific quick actions (sweep queue, ledger validator shortcut, KiRBe env wizard). Sidebar sub-nav (Overview / Documentation / POI/GOI / Facts) does not connect to v2 insight flow. | `04-tier-a-remediation-cards-1280.png`, v1 `16-research-center-full-1280.png` | Add journey strip under hero (sign-in → pick lens → fix top card → verify strip). Surface standard research panels as tactical chips linking into accordion panels without requiring expand-first. |

### Major

| ID | Area | Finding | Screenshot ref | Suggested fix |
|:---|:---|:---|:---|:---|
| **VIS-M01** | POV switcher | **Compliance tab wraps alone on a second row** inside the POV box, leaving dead space. Reads as layout bug, not intentional design. | `01-pov-switcher-remediation-cards-1280.png`, `04-tier-a-remediation-cards-1280.png` | Single-row segmented control with horizontal scroll or 5 equal segments; match Figma `RC-POV-Operator-1280` tab row. |
| **VIS-M02** | Layout / typography | **Hero competes with rail** — long subtitle + uppercase eyebrow + POV box + strip + rail heading stacks ~280px before actionable cards. Card grid uses heavy black buttons and thin rose side borders on every card — identical weight for all three critical items (no sort story). | `04-tier-a-remediation-cards-1280.png` | Tighten hero to one line + POV; use filled critical styling on #1 card only; secondary cards muted. Cap rail at visual “top 3” with overflow affordance. |
| **VIS-M03** | Drawer | **Runbook command truncates** in the monospace block (`…inte`); three-plane table **clips at drawer bottom** on 1280×800. Operator cannot copy a complete command from the screenshot evidence. | `05-tier-a-drawer-runbook-1280.png` | `pre` with wrap or horizontal scroll + **Copy command** button; drawer `max-w-lg` → `max-w-xl` or sticky footer; ensure table scroll. |
| **VIS-M04** | Figma parity | **Live ERP shell ≠ Figma isolated frame.** Figma P9b is a standalone canvas (no sidebar, no demo banner, no RED pill). Live embeds v2 inside full Holistika ERP chrome — POV placement, strip width, and card gutters diverge. Figma freshness uses uniform red semantic pills; live mixes grey/green/red inconsistently. | `figma-operator-1280-ref.png` vs `04-tier-a-remediation-cards-1280.png` | Either extend Figma with ERP shell frame for parity checks, or add Dev Mode spec for in-shell spacing. Implement Figma card dimensions (380×220, 16px gap, solid critical chip). |
| **VIS-M05** | Figma quality | **Figma drawer frame `RC-Drawer-Open-1280` is itself broken** — right sheet text truncates horizontally in the design source. Operator cannot ratify a broken reference. | `figma-drawer-1280-ref.png` | Fix Figma auto-layout min widths before asking operator to ratify P9b hi-fi. |
| **VIS-M06** | Accessibility | **KiRBe strip badge** uses red text on pink background; **POV toggle** may not expose a single `radiogroup` with arrow-key semantics (ToggleGroup without visible `role` description). | `04-tier-a-remediation-cards-1280.png` | Meet WCAG 2.2 contrast on error pills; add `aria-label="Viewpoint lens"` and focus ring on segment. |
| **VIS-M07** | Accordion | **v1 accordion is present but invisible in journey** — collapsed default is correct, but no preview chips hint that WIP packs / ledger / radar / KiRBe tools exist below. Operator must discover by scrolling. | `04-tier-a-remediation-cards-1280.png` (accordion below fold) | Add “4 audit panels below” hint row with icons, or tactical links from cards to accordion sections. |

### Minor

| ID | Area | Finding | Screenshot ref | Suggested fix |
|:---|:---|:---|:---|:---|
| **VIS-N01** | Copy drift | Pre-GOJ capture `01-…` still shows old headlines (“Source ledger shows 0 rows in BFF”) vs Tier A `04-…` — evidence folder mixes generations. | `01-pov-switcher-remediation-cards-1280.png` vs `04-tier-a-remediation-cards-1280.png` | Archive or relabel `01`/`03` as superseded in MANIFEST; avoid operator confusion. |
| **VIS-N02** | Mobile | **No v2 capture at 375px** — P9b requires `RC-Operator-375`; charter requires multi-viewport. | MANIFEST (1280 only) | Add Playwright captures at 375 and 768 before P11. |
| **VIS-N03** | Chrome | **RED status pill** in global header is unexplained on this page — adds anxiety without context. | `04-tier-a-remediation-cards-1280.png` | Tooltip or link to freshness strip; hide when unrelated to Research Center. |
| **VIS-N04** | Drawer IA | Drawer section order differs from GOJ T1→T2 flow: Runbook appears before Govern artifact / three-plane in live sheet; Figma lists Runbook (T1) then Three-plane (T2) but live interleaves “Why this matters” and paired SOP without visual separators. | `05-tier-a-drawer-runbook-1280.png` | Use titled sections with dividers: **Act (T1)** → **Govern (T2)** → optional **Program phase** footer. |

---

## Impeccable-style critique (condensed)

| Axis | Assessment |
|:---|:---|
| **Layout** | Vertical rhythm is loose; POV switcher floats right while strip spans full width — no cohesive hero band. Card grid is three equal towers (identical-card-grid anti-pattern). |
| **Typography** | Mixed registers: uppercase eyebrow, sentence case body, lowercase severity badges. Headlines improved in Tier A but detail lines still read engineering-first. |
| **Spacing** | Excess whitespace between hero, strip, and rail; drawer paragraphs lack breathing room between T1 and T2 blocks. |
| **Color** | Semantic drift: green “ok” strip + red critical cards side by side. Thin rose borders feel like debug outlines, not enterprise notification pattern (Carbon actionable inline). |
| **Broken UI** | Command truncation, table clip, empty POV lenses, non-acting CTAs. |
| **Accessibility** | Contrast risk on error pills; long env error strings wrap unevenly in strip thirds. |
| **Mobile** | Not evidenced in v2 folder. |
| **POV switcher** | Functional for Operator/Director URL persist; visually broken wrap; no lens description. |
| **Accordion** | Mechanically present; journey-dead without preview. |
| **Drawer** | Sheet pattern correct; content density and truncation undermine “runbook you can run.” |

---

## Live vs Figma — operator lens @ 1280

| Element | Figma P9b (`1:3`) | Live localhost | Match? |
|:---|:---|:---|:---|
| POV tabs | 5 in one horizontal row | 5 with Compliance wrapped | **No** |
| Freshness copy | “0 rows in BFF — env path” / “Queue empty” / “Unhealthy” | “No commit metadata” / green “0 targets” / long env error | **No** |
| Freshness micro-CTA | Implied in spec; not in Figma static frame | Absent | **No** |
| Card copy (Tier A) | GOJ headlines + CTAs | Matches Tier A text | **Yes** |
| Card chrome | 380×220, solid red critical chip | shadcn Card, outline badges, variable height | **Partial** |
| ERP shell | Absent in Figma | Full sidebar + demo banner | **N/A — document gap** |
| Drawer | Figma frame truncated | Live drawer better but command still clips | **Both weak** |

---

## Top 5 blockers (coordinator packet)

1. **VIS-B05** — Missing journey-aware + research/intelligence tactical UI; POV-specific out-of-box actions absent.
2. **VIS-B03** — Debug/fixture/BFF jargon exposed on T0 operator surface (Strict T3 violation).
3. **VIS-B04** — CTAs do not execute taxonomy (copy, open, env fix, roadmap).
4. **VIS-B02** — Freshness strip v2 not implemented; contradicts remediation cards.
5. **VIS-B01** — Non-Operator POV lenses render empty insight rail.

---

## Open questions for operator inline-ratify

1. **Figma scope:** Should P9b hi-fi include the **full ERP shell** (sidebar, demo banner) or remain an isolated content canvas with a separate “in-shell” frame?
2. **Fixture labeling:** On localhost, is it acceptable to show a single plain-language banner (“Sample data — actions may differ on production”) instead of per-card `fixture` chips?
3. **Empty lenses:** For P9b, do you want **placeholder journey cards** on Auditor/Finance/Compliance, or hide those lenses until P10-T3?
4. **RED header pill:** Should Research Center UAT documents global RED status, or is it out of scope for I96?
5. **Drawer width:** Prefer wider sheet (readable commands) or full-width mobile sheet only at 375?

---

## Cross-references

- Operator check-links: [`operator-check-links-2026-06-12.md`](operator-check-links-2026-06-12.md)
- Page spec v2: [`research-center-page-spec-v2-2026-06-12.md`](research-center-page-spec-v2-2026-06-12.md)
- GOJ implementation spec: [`docs/wip/intelligence/governed-operator-journey-ux-uat-2026-06-12/implementation-spec-2026-06-12.md`](../../../intelligence/governed-operator-journey-ux-uat-2026-06-12/implementation-spec-2026-06-12.md)
- v2 UAT charter: [`uat-i96-research-center-v2-charter-2026-06-12.md`](uat-i96-research-center-v2-charter-2026-06-12.md)
- Implementation (hlk-erp): `components/research-center/insight-card-rail.tsx`, `freshness-strip.tsx`, `lib/research-center/insights.ts`
