---
parent_initiative: INIT-OPENCLAW_AKOS-96
report_kind: revision-charter
wave: B1.5
authored: 2026-06-13
audience: J-OP;J-AIC
status: draft
blocks: Phase B Wave B3 (VerifyBanner + drawer tiers)
supersedes_ratify: Wave B1 operator ratify (REJECTED 2026-06-13)
linked_research:
  - docs/wip/intelligence/governed-actionable-analytics-surfaces-2026-06-12/research-synthesis-dashboard-patterns-2026-06-12.md
  - docs/wip/intelligence/governed-operator-journey-ux-uat-2026-06-12/journey-component-matrix-2026-06-12.md
linked_evidence:
  - docs/wip/planning/96-research-data-plane-and-research-center/reports/p9b-visual-audit-2026-06-12.md
  - docs/wip/planning/96-research-data-plane-and-research-center/reports/operator-check-links-2026-06-12.md
  - docs/wip/planning/96-research-data-plane-and-research-center/reports/i96-research-center-full-regression-2026-06-13.md
---

# P9b Wave B1.5 revision charter — Research Center insight machine (2026-06-13)

> **Binding operator rejection (2026-06-13):** Wave B1 ratification **REJECTED**. Do **not** proceed to Wave B3 until B1.5 clears operator ratify via check-links **and** the full regression report in [`i96-research-center-full-regression-2026-06-13.md`](i96-research-center-full-regression-2026-06-13.md) is dispositioned. This charter names the gap between research promise and B1/B2 shipped state, and the ordered work items that close it.

## 1. Product identity block

Research Center is a **production module inside the Holistika ERP web app** at `https://erp.holistikaresearch.com/research-center`, deployed through Vercel CI/CD on the `hlk-erp` consumer repo — the same surface operators and research staff use when signed in to the live ERP, not a separate product. It is the **governed insight machine** for research operations: a POV-filtered card rail that tells each reader what needs attention now, why it matters, and what to run or open next, backed by the three-plane research data contract (govern corpus, experience BFF, runbook layer). Research Center is **not** a local MADEIRA/AIC governance console, a Cursor workspace charter viewer, or a developer dashboard for AKOS repo paths — those belong in planning docs and agent sessions, not on the operator-facing T0–T2 surfaces. Copy, CTAs, and env badges must speak in **ERP product language** (program health, research packs, staleness queue, initiative phase) and only expose localhost or repo-relative paths in the collapsed T3 audit accordion when the operator explicitly drills for evidence. Spreading the current B1/B2 patterns unchanged to Director, Auditor, Finance, and Compliance lenses would **amplify confusion** — each lens must carry a distinct user story, sort policy, and empty state, not a relabelled remediation trio.

---

## 2. Gap table — research promise vs B1/B2 shipped

| Dimension | Research / spec promise | B1/B2 shipped (2026-06-13) | Gap severity |
|:---|:---|:---|:---|
| **Insight machine framing** | Governed insight machine: action cards + freshness + POV sort + drawer analysis tier ([`research-synthesis-dashboard-patterns-2026-06-12.md`](../../../intelligence/governed-actionable-analytics-surfaces-2026-06-12/research-synthesis-dashboard-patterns-2026-06-12.md) §Executive outcome) | Journey chrome landed (`JourneyStepIndicator`, `InsightRailHeader`, strip micro-CTAs); rail still remediation-heavy | **Blocker** |
| **Charts / graphs** | Recharts in **drawer T1**: ledger completion sparkline (30-day % trend); radar overdue **horizontal bar** sorted by days ([dashboard synthesis §3.2](../../../intelligence/governed-actionable-analytics-surfaces-2026-06-12/research-synthesis-dashboard-patterns-2026-06-12.md)) | No Recharts in Research Center; drawer is prose + runbook only ([`research-center-hlk-erp-ui-inventory-2026-06-12.md`](research-center-hlk-erp-ui-inventory-2026-06-12.md)) | **Blocker** |
| **Cross-filter / linked views** | Future drawer cross-filter (bar + table pair) — scheduled post-P10 unless BFF ships aggregates ([dashboard synthesis §3.3](../../../intelligence/governed-actionable-analytics-surfaces-2026-06-12/research-synthesis-dashboard-patterns-2026-06-12.md)) | Not started | **Scheduled** (B1.5 optional stretch; not B3 gate) |
| **CTA taxonomy** | Six kinds + **act in ≤2 steps**: runbook copy, **open artifact route**, env checklist, initiative phase, doc link, ticket ([page spec v2 §2.6](research-center-page-spec-v2-2026-06-12.md)) | Primary CTA ≈ copy-to-clipboard runbook or drawer-only; no deep links to KiRBe, planning README, GitHub governed paths, deploy/CICD surfaces ([`p9b-visual-audit-2026-06-12.md`](p9b-visual-audit-2026-06-12.md) VIS-B04) | **Blocker** |
| **`navigate` CTA (new)** | Implied by artifact / initiative_phase / doc_link — must open **internal ERP routes** + **external governed URLs** | Not in schema; clipboard-only | **Blocker** (B1.5 adds explicit `navigate` kind) |
| **Production copy** | ERP module voice; functional discipline names on T0–T2; codes T3 only (Strict T3 / D-IH-96-F) | "This environment", localhost fixture strings, BFF jargon on card face ([VIS-B03](p9b-visual-audit-2026-06-12.md)) | **Blocker** |
| **Deploy-target badge** | Operator knows **production vs preview vs local** without reading debug chips | Per-card `fixture` chips; no global deploy-target badge | **Major** |
| **Per-POV persona** | Distinct journeys: Operator remediation-first; Director ICS-first; Auditor evidence; Finance settlement; Compliance block_govern ([`journey-component-matrix-2026-06-12.md`](../../../intelligence/governed-operator-journey-ux-uat-2026-06-12/journey-component-matrix-2026-06-12.md)) | POV switcher re-sorts partially; lenses feel copy-pasted; same remediation stack visible across lenses | **Blocker** |
| **Per-POV rail sort** | Operator: `remediation > staleness > env_deploy > drift`; Director: `intent_criticality > ledger_completion > phase_blocker` ([phase BC plan §B.2–B.3](research-center-phase-bc-tranche-plan-2026-06-12.md)) | B2 added Director card types + sort — operator still reports insufficient distinction vs Operator | **Major** |
| **Lens-specific empty states** | Honest empty + lens guidance ([GOV.UK incomplete pattern](research-synthesis-dashboard-patterns-2026-06-12.md) §5.2) | `LensEmptyState` exists but generic | **Major** |
| **Governed corpus depth** | Surface prong/source counts, pack coverage, ICS, phase blockers from ledger + registers — not only "zero rows" remediation | BFF still remediation-centric; huge `source-ledger.csv` corpus invisible on T0 ([operator rejection #5](operator-check-links-2026-06-12.md)) | **Blocker** |
| **Freshness strip v2** | Label + status + **why** + micro-CTA; strip tone matches card severity ([dashboard synthesis §4](../../../intelligence/governed-actionable-analytics-surfaces-2026-06-12/research-synthesis-dashboard-patterns-2026-06-12.md)) | B1 added micro-CTAs; strip/card contradiction noted in visual audit VIS-B02 | **Major** (re-verify in B1.5) |
| **Verification URL** | Production ERP is SSOT for operator sign-off | Check-links localhost-first only | **Blocker** (fixed in §6 + check-links update) |

---

## 3. Wave B1.5 scope — ordered work items

**Tranche class:** internal_governance + sibling-repo (`hlk-erp`)  
**Repos:** `root_cd/hlk-erp` (primary); `openclaw-akos` (docs + check-links only)  
**Out of scope:** Wave B3 (`VerifyBanner`, drawer tier hardening beyond chart + CTA fixes), full Auditor/Finance/Compliance T3 build, vault canonical mint, new npm deps.

### Work item order (binding sequence)

| # | ID | Work item | Repo / files | Acceptance (PASS) |
|:---:|:---|:---|:---|:---|
| 1 | **B1.5-01** | **CTA taxonomy: add `navigate`** — extend `cta_kind` union + handlers: internal Next routes (`/planning`, `/kirbe`, FINOPS route stubs) + external governed URLs (GitHub blob paths, Vercel deploy dashboard, planning README on GitHub). Keep `runbook` copy+toast; `navigate` = `window.open` / `Link` with audit log in drawer T2. | `hlk-erp/lib/research-center/types.ts`, `insight-card.tsx`, `insight-card-rail.tsx`, BFF spec alignment [`research-center-bff-live-data-spec-2026-06-12.md`](research-center-bff-live-data-spec-2026-06-12.md) | Operator clicks **Open research planning index** → lands governed URL; **Review program phase** → initiative roadmap; no clipboard-only for `artifact` / `initiative_phase` / `doc_link` primary CTAs |
| 2 | **B1.5-02** | **Recharts drawer charts (dashboard synthesis §3.2)** — use existing `@/components/ui/chart` wrapper: (a) **Ledger completion** line/area sparkline — 30-day completion % from git ledger aggregate; (b) **Radar overdue** horizontal bar chart — sorted by overdue days. Charts live in drawer T1 only; glance rail stays chart-free. | `hlk-erp/components/research-center/insight-drawer.tsx` (or equivalent), `lib/research-center/ledger-stats.ts`, `radar-stats.ts` | Director **Ledger completion** drawer shows sparkline; Operator **Staleness** drawer shows overdue bar when queue has rows |
| 3 | **B1.5-03** | **Production-first copy pass** — ban T0–T2 strings: "this environment", "localhost fixture", raw AKOS repo paths, bare "BFF". Replace with ERP product copy per page spec v2 §2.2 anti-jargon. Move technical env diagnostics to T3 accordion only. | `hlk-erp/lib/research-center/insights.ts`, `freshness-strip.tsx`, card builders | Visual scan @1280 production: zero debug/fixture chips on card face ([VIS-B03](p9b-visual-audit-2026-06-12.md) cleared) |
| 4 | **B1.5-04** | **Deploy-target env badge** — single hero badge: `Production` / `Preview` / `Local dev` derived from `VERCEL_ENV` + hostname (`erp.holistikaresearch.com` → Production). Distinct from per-insight severity. | `hlk-erp/components/research-center/deploy-target-badge.tsx`, `research-center-client.tsx` | Production deploy shows **Production** badge; localhost shows **Local dev**; preview deploy shows **Preview** |
| 5 | **B1.5-05** | **Per-POV persona one-liner** — under POV switcher, lens-specific subtitle from matrix: Operator "Fix env gaps and run staleness sweeps first"; Director "Program phase and research-pack completion". | `journey-component-matrix` Operator + Director rows; `research-center-client.tsx` | Switching POV changes subtitle + rail header label; not identical copy |
| 6 | **B1.5-06** | **Distinct rail sort + lens-specific empty states** — enforce matrix sort keys per lens; replace generic `LensEmptyState` with lens copy + suggested next lens CTA (Auditor → manifest link; Director → "No phase blockers — see ledger completion"). | `lib/research-center/insights.ts` sort functions; `lens-empty-state.tsx` | Director healthy env shows ≥3 non-remediation cards; Auditor empty state names evidence path, not "no data" |
| 7 | **B1.5-07** | **BFF: ledger corpus depth** — surface `prong_breakdown`, `source_count`, active pack tallies from git `source-ledger.csv` glob; emit `ledger_completion`, `staleness`, `intent_criticality` cards from aggregates, not only remediation when `total_rows === 0`. | `lib/research-center/ledger-stats.ts`, `insights.ts`, `prong-coverage-strip.tsx` | Director rail shows completion % card with real prong counts when git reader healthy; Operator shows staleness card when radar overdue > 0 |
| 8 | **B1.5-08** | **AKOS traceability** — mint this charter; update check-links §B1.5 + production URLs; append `files-modified.csv`; L1 journey screenshots on **production** primary. | `openclaw-akos` reports only | Check-links updated; production screenshots in `artifacts/uat-screenshots/i96-research-center-v2-b15-<date>/` |

### Deferred (scheduled, not dropped)

| Item | Posture | Fires when |
|:---|:---|:---|
| Drawer cross-filter (bar + table linked selection) | **Scheduled** post-B1.5 | BFF linked aggregates land or P10.3 inline-ratify |
| Wave B3 `VerifyBanner` + drawer tier polish | **Scheduled** | After B1.5 operator ratify |
| Full Auditor/Finance/Compliance T3 cards | **Scheduled** P10-T3 | Per phase BC plan §B.4 |

---

## 4. Pause gate — B3 blocked

| Gate | Rule |
|:---|:---|
| **B3 entry** | **BLOCKED** until operator ratifies **Wave B1.5** via [`operator-check-links-2026-06-12.md`](operator-check-links-2026-06-12.md) §B1.5 checklist (all rows PASS or N/A-with-reason). |
| **Ratify method** | Operator opens production URLs first (§6), then localhost dev fallback; confirms charts in drawer, navigate CTAs, production copy, POV distinction, corpus-depth cards. |
| **Agent rule** | Execution seat MUST NOT start B3 (`VerifyBanner`, drawer-tier-only work) on rejection carryover — cite this charter §4. |

---

## 5. Verification matrix (B1.5)

### Mechanical (hlk-erp)

```powershell
cd root_cd/hlk-erp
npm run typecheck
npm run lint
npx playwright test --grep research-center
```

### Operator experiential (production primary)

| Step | Production URL (PRIMARY) | Dev fallback |
|:---|:---|:---|
| Sign-in → Research Center | https://erp.holistikaresearch.com/research-center | http://localhost:3010/api/dev/sign-in?next=/research-center |
| Operator lens | https://erp.holistikaresearch.com/research-center?pov=operator | http://localhost:3010/research-center?pov=operator |
| Director lens | https://erp.holistikaresearch.com/research-center?pov=director | http://localhost:3010/research-center?pov=director |
| Deploy proof | Vercel MCP `get_deployment` for `hlk-erp` production target | n/a |

### B1.5 ratify checklist (operator)

- [ ] **Production** deploy-target badge visible on `erp.holistikaresearch.com`
- [ ] No localhost/fixture/BFF jargon on T0–T2 card faces @1280
- [ ] Primary CTA **navigates** to at least one governed artifact URL (not clipboard-only)
- [ ] Drawer shows **ledger sparkline** (Director) and/or **radar overdue bar** (Operator) when data exists
- [ ] POV subtitle + empty states differ per lens (Operator vs Director minimum)
- [ ] Director shows ≥3 non-remediation cards when git reader healthy
- [ ] Prong/source counts visible (strip or card), not remediation-only

Screenshot manifest: `artifacts/uat-screenshots/i96-research-center-v2-b15-2026-06-13/` (production rows mandatory).

---

## 6. Check-links update (executor packet B1.5-08)

See [`operator-check-links-2026-06-12.md`](operator-check-links-2026-06-12.md) — production URLs at top; §Wave B1 REJECTED; §Full regression 2026-06-13; §Wave B1.5 PENDING.

---

## 7. Full regression gate (binding — no B1.5 code until disposition)

**Operator requirement (2026-06-13):** Wave B1 was rejected before ratify. A **full regression** must complete and be **dispositioned** before any B1.5 hlk-erp code lands.

| Rule | Detail |
|:---|:---|
| **Regression report** | [`i96-research-center-full-regression-2026-06-13.md`](i96-research-center-full-regression-2026-06-13.md) — mechanical + experiential + P11 composite gate scores |
| **Entry condition for B1.5-01..07** | Operator reads regression report → ratifies disposition (acknowledge blockers + carryover posture) → then execution seat may start B1.5-01 |
| **No silent skip** | Mechanical PASS alone does **not** clear this gate — experiential blockers from operator rejection remain FAIL until B1.5 work closes them |
| **B3 remains blocked** | Even after regression disposition, B3 stays blocked until B1.5 operator ratify (§4) |

**Disposition options (intent-ranked regression enum):**

- **new** — finding introduced by B1/B2 tranche
- **pre-existing** — documented before B1 (visual audit, journey gap)
- **known-deferred** — scheduled in charter §3 deferred table with tracker path

---

## Cross-references

- Full regression report: [`i96-research-center-full-regression-2026-06-13.md`](i96-research-center-full-regression-2026-06-13.md)
- Dashboard pattern synthesis: [`research-synthesis-dashboard-patterns-2026-06-12.md`](../../../intelligence/governed-actionable-analytics-surfaces-2026-06-12/research-synthesis-dashboard-patterns-2026-06-12.md)
- Journey × component matrix: [`journey-component-matrix-2026-06-12.md`](../../../intelligence/governed-operator-journey-ux-uat-2026-06-12/journey-component-matrix-2026-06-12.md)
- Visual audit (FAIL): [`p9b-visual-audit-2026-06-12.md`](p9b-visual-audit-2026-06-12.md)
- Phase B+C plan: [`research-center-phase-bc-tranche-plan-2026-06-12.md`](research-center-phase-bc-tranche-plan-2026-06-12.md)
- BFF live-data spec: [`research-center-bff-live-data-spec-2026-06-12.md`](research-center-bff-live-data-spec-2026-06-12.md)
- Experiential UAT ladder: [`research-center-experiential-uat-ladder-2026-06-12.md`](research-center-experiential-uat-ladder-2026-06-12.md)
