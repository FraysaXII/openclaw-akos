---
report_type: uat-charter
intellectual_kind: uat_evidence
parent_initiative: INIT-OPENCLAW_AKOS-96
phase: P11-v2-uat
sharing_label: internal_only
authored: 2026-06-12
audience: J-OP
language: en
status: draft
verdict: PENDING-OPERATOR-WALK
supersedes_browser_uat: reports/uat-i96-research-center-browser-2026-06-11.md
linked_research: docs/wip/intelligence/governed-actionable-analytics-surfaces-2026-06-12/
---

# UAT charter — Research Center v2 (insight machine)

> **Purpose:** Capture operator guidance + v1 gap findings that v2 must close. v1 browser UAT remains **PASS-WITH-FOLLOWUP** on [`uat-i96-research-center-browser-2026-06-11.md`](uat-i96-research-center-browser-2026-06-11.md). This charter defines the **v2 acceptance bar** — not a retroactive v1 rewrite.

## Operator guidance (binding intent, 2026-06-12)

Research Center v1 **works** (auth fixed, panels render) but lacks:

1. **Multi-POV views** — Director, Operator, Auditor, Finance, Compliance see different prioritized questions
2. **Actionable BI insight** — dashboards as **insight machines**, not status boards
3. **Ground-up rethink** using AKOS session methodology and existing disciplines (research radar, intent-ranked regression, quality fabric, FINOPS, graph-explorer UAT patterns, mission control panels)

v2 UAT PASS requires evidence that an operator can **act** from the page without opening five other tools first.

## v1 gap findings (screenshot-grounded)

Evidence: [`artifacts/uat-screenshots/i96-research-center-2026-06-11/MANIFEST.json`](../../../../artifacts/uat-screenshots/i96-research-center-2026-06-11/MANIFEST.json) + session 5 walk.

| Gap ID | Observation | Screenshot / evidence | v2 acceptance criterion |
|:---|:---|:---|:---|
| G1 | **Ledger 0 rows** — TOTAL ROWS 0, COMPLETION 0% while git ledger has 483 rows | `18-panel-ledger-summary-1280-mcp.png` | Director lens card explains gap + CTA to validator or env fix; drill-down cites three-plane row |
| G2 | **Radar empty** — "No radar targets loaded" | `19-panel-radar-queue-1280-mcp.png` | Operator lens card distinguishes empty register vs error; CTA to radar sweep / register path |
| G3 | **KiRBe red** — unhealthy; missing DB view | `20-panel-kirbe-search-1280-mcp.png`, strip v2 | Operator env card with `KIRBE_API_URL` + I83 handoff link |
| G4 | **No drill-down** — metrics not clickable to artifacts | All panel shots | Every insight card opens drawer with govern path + runbook |
| G5 | **Single layout** — same 2×2 for all roles | `11`–`13` full page | POV switcher changes card rail content (snapshot per lens) |
| G6 | **Strip without action** — colors only | `14-freshness-strip-1280-v2.png` | Strip v2 adds why + micro-CTA per badge |
| G7 | **WIP packs list only** — no priority | CDP extract session 5 | Operator/Director cards for stale packs (when data available) |

### v1 session arc (context for v2)

| Session | Outcome |
|:---|:---|
| 1–3 | Auth blocked — magic link Site URL fallback; redirect loops |
| 4 | Role-mapping fix (`1782680a`) — dev sign-in lands on panels |
| 5 | **PWF** — panel walk + 20+ manifest entries + Impeccable KiRBe relabel |
| 6–7 | Magic-link allow-list + exact-match callback fix — operator retest pending |
| 8 | Email rate limit — dev-password workaround documented |

v2 UAT inherits P7 mechanical bar (Playwright + MCP + manifest + Impeccable) **plus** POV lens matrix below.

## v2 UAT dimensions

> **Experiential ladder:** Dimensions 1–15 map to **L3–L4** of [`research-center-experiential-uat-ladder-2026-06-12.md`](research-center-experiential-uat-ladder-2026-06-12.md). L1 (CI/Playwright anonymous) and L2 (spec/Figma/GOJ contract) are **prerequisites** — charter dimensions assume they are green before P11 execution.

| # | Dimension | Method | PASS criteria |
|:---|:---|:---|:---|
| 1 | Remediation cards | Operator lens @ 1280 | Three cards OR honest `source: fixture` labels for ledger 0, radar empty, KiRBe red |
| 2 | POV switcher | Browser MCP @ 1280 | Five lenses switch; URL `?pov=` persists; content differs per lens |
| 3 | Insight cards | Per-lens walk | ≥1 card with primary CTA visible per lens (fixture OK if labeled) |
| 4 | Drill-down | Click card | Drawer shows three-plane mapping + artifact path + runbook command |
| 5 | Director lens | Dedicated walk | Intent-criticality or ledger narrative; remediation when ledger 0 |
| 6 | Operator lens | Dedicated walk | Remediation cards sort first; staleness/env CTAs present |
| 7 | Auditor lens | Dedicated walk | RBAC proof + manifest link; demo redaction at level 1+ |
| 8 | Finance lens | Dedicated walk | Settlement-risk or FINOPS stub card with CTA |
| 9 | Compliance lens | Dedicated walk | block_govern or drift type when register seeded |
| 10 | Figma parity | Compare frames | v2 chrome matches approved Figma at 1280 (Quality Fabric RULE 4) |
| 11 | v1 regression | Accordion expand | Four panels still render (parity with v1 UAT) |
| 12 | Responsive | 375 / 768 / 1280 | POV + rail usable per lens sample screenshot |
| 13 | Manifest | Per-lens walk + **ladder naming** | `artifacts/uat-screenshots/i96-research-center-v2-p11-<date>/` — `{seq}-{lens}-{stage}-…-{viewport}-{auth}.png` + unified `captures[]` MANIFEST; ≥25 rows at P11 PASS (see ladder §manifest) |
| 14 | Impeccable | Audit report | Card hierarchy + cognitive load disposition |
| 15 | axe | Python 3.12 or a11y.spec | Per route post-login; severity not color-only |

## Pre-requisites (P10 complete)

- [ ] Topic research pack PASS (`validate_research_action.py` on 32-row ledger)
- [ ] Page spec v2 ratified (P9 inline-ratify — **pending operator re-ratify** after research rework)
- [ ] **Figma mockup** AIC-minted + operator inline-ratify on preview URL + `FIGMA_FILES_REGISTRY.csv` row (primary gate)
- [ ] Excalidraw+ wireframe optional (BFF overlay only — not sufficient alone)
- [ ] Remediation cards live for ledger 0 / radar empty / KiRBe red
- [ ] BFF `/insights` endpoint deployed to localhost:3010
- [ ] Playwright spec `research-center-v2.spec.ts` (or extended v1 spec)

## Follow-ups carried from v1 (not v2 blockers unless regressed)

| Item | v1 tracker | v2 note |
|:---|:---|:---|
| Magic-link retest | uat browser §10 | Independent auth track |
| KiRBe env | PWF | Operator lens must surface remediation |
| axe Python 3.12 | SKIP documented | v2 should PASS or document N/A |
| Production SSL MCP -107 | workflow notes | Localhost-first unchanged |

## Verdict line (placeholder)

**PENDING-OPERATOR-WALK** until **G-P11-01..12** in [`research-center-experiential-uat-ladder-2026-06-12.md`](research-center-experiential-uat-ladder-2026-06-12.md) §"When P11 PASS" are satisfied. Charter dimensions alone do not constitute PASS.

## Cross-references

- v1 UAT: [`uat-i96-research-center-browser-2026-06-11.md`](uat-i96-research-center-browser-2026-06-11.md)
- Page spec v2: [`research-center-page-spec-v2-2026-06-12.md`](research-center-page-spec-v2-2026-06-12.md)
- Topic research: [`governed-actionable-analytics-surfaces-2026-06-12/`](../../../intelligence/governed-actionable-analytics-surfaces-2026-06-12/)
- Research synthesis: [`research-synthesis-2026-06-12.md`](../../../intelligence/governed-actionable-analytics-surfaces-2026-06-12/research-synthesis-2026-06-12.md)
- MADEIRA experiential: [`../../../intelligence/aic-madeira-experiential-uat-2026-06-11/charter.md`](../../../intelligence/aic-madeira-experiential-uat-2026-06-11/charter.md)
- Experiential ladder: [`research-center-experiential-uat-ladder-2026-06-12.md`](research-center-experiential-uat-ladder-2026-06-12.md)
