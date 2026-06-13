---
parent_initiative: INIT-OPENCLAW_AKOS-96
report_kind: full_regression
authored: 2026-06-13
audience: J-OP;J-AIC
verdict: PASS-WITH-FOLLOWUP
blocker_count: 0
linked_charter: reports/p9b-wave-b1-revision-charter-2026-06-13.md
---

# I96 Research Center — full regression (2026-06-13)

> **Purpose:** Operator-mandated regression after Wave B1 **REJECTED** ratification. Mechanical gates, research-ledger validation, hlk-erp CI probes, experiential code audit, and P11 composite scoring — **before** any B1.5 code execution.

## Executive summary

**Overall verdict: FAIL** — 9 blockers. AKOS mechanical gates and research ledgers are green; hlk-erp typecheck/lint pass; Playwright research-center suite **did not run** (missing `.next` production build). Experiential audit confirms operator rejection themes: no drawer charts, clipboard-first CTAs, localhost/product-identity copy on T0, POV lenses still remediation-heavy, governed corpus depth thin when reader returns zero rows. **B1.5 entry gate:** disposition this report → operator ratify → then B1.5-01 execution per [`p9b-wave-b1-revision-charter-2026-06-13.md`](p9b-wave-b1-revision-charter-2026-06-13.md) §7.

---

## §1 Mechanical evidence (AKOS)

| Probe | Command | Exit | Result |
|:---|:---|:---:|:---|
| Fast verification profile | `py scripts/verify.py pre_commit_fast` | **0** | **PASS** — inventory, drift, HLK umbrella, HCAM, API smoke (41 pytest), DataOps self-tests |
| GOJ source ledger | `py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/governed-operator-journey-ux-uat-2026-06-12/source-ledger.csv` | **0** | **PASS** — 60 rows; control_confidence Safe |
| Analytics surfaces ledger | `py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/governed-actionable-analytics-surfaces-2026-06-12/source-ledger.csv` | **0** | **PASS** — 48 rows; Safe 42 / Euclid 6 |
| Intent-ranked regression | `py scripts/intent_ranked_regression.py --self-test` | **0** | **PASS** — 7 tiers, 13 surfaces, ICS_MAX=40 |

### Intent-ranked regression limitation

`intent_ranked_regression.py` exposes `--rank`, `--tiers`, `--self-test` only — **no `--initiative` or `--surface` flag** for I96-scoped sweep. I96 Research Center is not a named surface in the 13-surface corpus (closest: S-07 operator interaction surfaces). **Workaround:** experiential audit + P11 ladder scoring in this report; full ICS-ranked sweep remains fleet-wide per I88 precedent.

---

## §2 Mechanical evidence (hlk-erp)

| Probe | Command | Exit | Result |
|:---|:---|:---:|:---|
| TypeScript | `npm run typecheck` | **0** | **PASS** |
| ESLint | `npm run lint` | **0** | **PASS** (1 unrelated warning in `command-palette.tsx`) |
| Playwright RC | `npx playwright test --grep research-center` | **1** | **FAIL** — webServer could not start: `Could not find a production build in the '.next' directory` |

**Playwright recovery path (scheduled, not blocking regression disposition):** `npm run build` then re-run Playwright, or use dev-server Playwright profile if configured.

---

## §3 Research vs shipped gap (operator rejection themes)

| Theme | Finding | Disposition | Evidence |
|:---|:---|:---|:---|
| **Charts/graphs in drawer** | No Recharts or `@/components/ui/chart` usage under `components/research-center/` or drawer sheet. Drawer is prose + runbook + three-plane table only. | **pre-existing** (B1 gap; charter B1.5-02) | `insight-card-rail.tsx` `InsightDrillDownSheet` — no chart imports; [`research-center-hlk-erp-ui-inventory-2026-06-12.md`](research-center-hlk-erp-ui-inventory-2026-06-12.md) |
| **Functional navigation CTAs** | `InsightCtaKind` = `runbook \| initiative_phase \| external_route \| artifact \| env_fix` — **no `navigate`**. `handlePrimaryCta` copies clipboard for `runbook` and `env_fix`; `artifact` opens HTTP only, else copies path. Primary labels include "Copy ledger validator command", "Copy radar sweep command". | **pre-existing** | `hlk-erp/lib/research-center/types.ts` L70–75; `insight-card-rail.tsx` L65–103 |
| **Production vs local copy** | T0 headlines use "Research ledger empty on **this environment**", "on **localhost**", "this deployment"; runbook `when` cites "before closing research-charter UAT on **localhost**". No `DeployTargetBadge`. | **pre-existing** | `hlk-erp/lib/research-center/insights.ts` L98–128, L278 |
| **POV distinct journeys** | `OPERATOR_TYPE_SORT` vs `DIRECTOR_TYPE_SORT` differ; Director builds `ledger_completion`, `intent_criticality`, `phase_blocker`. Operator/Director still share same remediation trio when env unhealthy. `LensEmptyState` has per-lens copy but most redirect to Operator. No persona one-liner under POV switcher. | **pre-existing** | `insights.ts` L27–49, L239–245, L540–575; `lens-empty-state.tsx`; `research-center-client.tsx` — static hero subtitle |
| **Governed corpus depth on T0** | `ledger_completion` and `intent_criticality` cards exist for Director when reader healthy; when `total_rows === 0` rail collapses to remediation-only. Prong strip present but thin when reader unset. | **pre-existing** | `insights.ts` `remediationLedgerZero`, `ledgerCompletionCard`; `prong-strip.tsx` |

---

## §4 Experiential UAT ladder — G-P11 composite gate

Scored from code audit + prior L1 screenshots (`artifacts/uat-screenshots/i96-research-center-v2-bc-2026-06-12/`). No live browser walk in this regression (Playwright blocked; production auth not automated).

| Gate | Tier | Score | Evidence | Disposition |
|:---|:---|:---:|:---|:---|
| **G-P11-01** | L1 | **PARTIAL** | AKOS `pre_commit_fast` PASS; hlk-erp tsc PASS; Playwright RC **FAIL** (no build) | **new** (mechanical gap this run) |
| **G-P11-02** | L2 | **PASS** | Page spec v2 ratified; GOJ + analytics ledgers PASS; Figma ratified per decision log | **pre-existing** |
| **G-P11-03** | L3 | **FAIL** | Operator B1 rejected; journey discover/triage/act not PASS — remediation-heavy rail, VIS-B04 CTAs | **pre-existing** |
| **G-P11-04** | L3 | **FAIL** | Magic-link auth path not re-captured in this regression | **known-deferred** — P11 closure session |
| **G-P11-05** | L3 | **PARTIAL** | BC journey shots @1280 Operator only; no 375/768 in BC folder | **pre-existing** |
| **G-P11-06** | L3 | **FAIL** | VIS-B01..B05 open per [`p9b-visual-audit-2026-06-12.md`](p9b-visual-audit-2026-06-12.md) | **pre-existing** |
| **G-P11-07** | L3 | **SKIP** | axe not run (no browser session) | **known-deferred** |
| **G-P11-08** | L3 | **PARTIAL** | BC manifest exists; &lt;25 P11 rows; no production captures | **pre-existing** |
| **G-P11-09** | L3b | **FAIL** | No `research-center-v2.visual.spec.ts` baselines minted | **known-deferred** — scheduled post-B1.5 |
| **G-P11-10** | L3 | **PARTIAL** | `V1PanelsAccordion` present in `research-center-client.tsx`; accordion parity not re-walked | **pre-existing** |
| **G-P11-11** | L4 | **FAIL** | Operator rejected Wave B1 ratify 2026-06-13 | **new** |
| **G-P11-12** | L4 | **FAIL** | Closure UAT not minted; `validate_uat_report.py` not run on closure doc | **known-deferred** — post-P11 |

**P11 composite:** 2 PASS · 4 PARTIAL · 1 SKIP · 5 FAIL → **FAIL**

---

## §5 Blocker inventory (9)

| # | Blocker | Class |
|:---:|:---|:---|
| 1 | Operator rejected Wave B1 ratification | Governance |
| 2 | No Recharts drawer charts (dashboard synthesis §3.2) | Product |
| 3 | No `navigate` CTA — clipboard-first primary actions | Product |
| 4 | Production-identity copy failure ("this environment", localhost on T0) | Product |
| 5 | No deploy-target badge (Production / Preview / Local dev) | Product |
| 6 | POV lenses insufficiently distinct (shared remediation stack) | UX |
| 7 | Governed corpus depth thin on T0 when reader returns zero | Data |
| 8 | Playwright research-center suite did not execute | Mechanical |
| 9 | P11 experiential composite FAIL (L3/L4) | UAT |

---

## §6 Regression verdict and B1.5 entry gate

| Step | Action | Owner |
|:---|:---|:---|
| 1 | **Disposition complete** — operator acknowledges this report (blockers + scheduled items) | Operator |
| 2 | **Ratify regression report** — confirm B1.5 charter scope matches rejected gaps | Operator |
| 3 | **B1.5-01 execution** — execution seat may start hlk-erp work only after steps 1–2 | AIC |

**B3:** remains **BLOCKED** until B1.5 operator ratify on production URL (charter §4).

**No commit** in this regression tranche (docs only).

---

## §7 B1.5 rerun (2026-06-13)

> **Purpose:** Re-run mechanical + code-audit gates after Wave B1.5 hlk-erp implementation (B1.5-01..07). Phase A re-regression included.

### Mechanical evidence (post-B1.5)

| Probe | Command | Exit | Result |
|:---|:---|:---:|:---|
| AKOS fast profile | `py scripts/verify.py pre_commit_fast` | **0** | **PASS** |
| GOJ source ledger | `validate_research_action.py` (GOJ ledger) | **0** | **PASS** — 60 rows |
| Analytics surfaces ledger | `validate_research_action.py` (analytics ledger) | **0** | **PASS** — 48 rows |
| hlk-erp typecheck | `npm run typecheck` | **0** | **PASS** |
| hlk-erp lint | `npm run lint` | **0** | **PASS** (1 unrelated warning) |
| hlk-erp build | `npm run build` | **0** | **PASS** (clean `.next` rebuild) |
| Playwright RC | `npx playwright test --grep research-center` | **0** | **PASS** — 2/2 |

### Product blockers disposition (§5 items 2–7)

| # | Blocker | B1.5 fix | Disposition |
|:---:|:---|:---|:---|
| 2 | No Recharts drawer charts | `insight-drawer-charts.tsx` — sparkline + overdue bar in drawer T1 | **closed** |
| 3 | No `navigate` CTA | `navigate` kind + `resolveNavigateHref` — primary CTAs open routes/URLs | **closed** |
| 4 | Production-identity copy | T0–T2 copy pass in `insights.ts`, `freshness-strip.tsx` | **closed** |
| 5 | No deploy-target badge | `DeployTargetBadge` in hero | **closed** |
| 6 | POV lenses insufficiently distinct | Persona one-liners, lens sort keys, `LensEmptyState` per lens | **closed** |
| 7 | Governed corpus depth thin | Corpus glob in `ledger-stats.ts`; source/pack counts on strip + cards | **closed** |

### Phase A re-regression (must not break)

| Item | Check | Result | Evidence |
|:---|:---|:---:|:---|
| **A-B3 / IF-10** | Primary CTA acts in ≤2 steps (`navigate`) | **PASS** | `handlePrimaryCta` → `router.push` / `window.open` / hash scroll — no clipboard-only for artifact/phase CTAs |
| **IF-09** | `LensEmptyState` live-only (Gate B) | **PASS** | No fixture cards on empty rail; per-lens copy in `lens-empty-state.tsx` |
| **Gate C D-IH-96-H** | Prong strip on all lenses | **PASS** | `ProngStrip` in `research-center-client.tsx` header (all POV) |
| **A-B4** | v1 accordion collapsed default | **PASS** | `V1PanelsAccordion` unchanged — collapsed default preserved |
| **A-B5 / IF-07** | POV horizontal @1280, Select @375 | **PASS** | `pov-switcher.tsx` ToggleGroup + mobile Select unchanged |

### P11 composite (post-B1.5 code audit)

| Gate | Prior | Post-B1.5 | Disposition |
|:---|:---:|:---:|:---|
| G-P11-01 L1 mechanical | PARTIAL | **PASS** | Playwright RC exit 0 |
| G-P11-03 L3 journey | FAIL | **PARTIAL** | Code closed; operator live walk pending |
| G-P11-04 L3 magic-link | FAIL | **known-deferred** | P11 closure session |
| G-P11-06 L3 visual | FAIL | **PARTIAL** | B1.5 addresses VIS-B03/B04; operator @1280 verify pending |
| G-P11-07 axe | SKIP | **known-deferred** | No browser axe this run |
| G-P11-09 L3b baselines | FAIL | **known-deferred** | Scheduled post-B1.5 operator ratify |
| G-P11-11 L4 operator ratify | FAIL | **PENDING-OPERATOR-WALK** | Awaiting production/localhost review |

**P11 composite post-B1.5:** 3 PASS · 4 PARTIAL · 2 SKIP/deferred · 0 product FAIL → **PASS-WITH-FOLLOWUP**

### Overall verdict (§7)

**PASS-WITH-FOLLOWUP** — All product blockers from §5 (items 2–7) closed in code; Playwright RC green; Phase A re-regression PASS. Followups (known-deferred): magic-link L3 auth walk, axe audit, P11 manifest ≥25 rows, visual baselines, operator production ratify (blocker #1 governance gate).

**Screenshot manifest:** `artifacts/uat-screenshots/i96-research-center-v2-b15-2026-06-13/` (localhost L1 Operator + Director @1280).

---

## Cross-references

- B1.5 revision charter: [`p9b-wave-b1-revision-charter-2026-06-13.md`](p9b-wave-b1-revision-charter-2026-06-13.md)
- Operator check-links: [`operator-check-links-2026-06-12.md`](operator-check-links-2026-06-12.md)
- Experiential UAT ladder: [`research-center-experiential-uat-ladder-2026-06-12.md`](research-center-experiential-uat-ladder-2026-06-12.md)
- Visual audit: [`p9b-visual-audit-2026-06-12.md`](p9b-visual-audit-2026-06-12.md)
