---
parent_initiative: INIT-OPENCLAW_AKOS-96
report_kind: journey-gap-analysis
authored: 2026-06-12
updated: 2026-06-13
audience: J-OP;J-AIC
baseline_matrix: docs/wip/intelligence/governed-operator-journey-ux-uat-2026-06-12/journey-component-matrix-2026-06-12.md
implementation_repo: root_cd/hlk-erp
---

# Research Center — journey gap analysis (post Phase A)

**Baseline:** [`journey-component-matrix-2026-06-12.md`](../../../intelligence/governed-operator-journey-ux-uat-2026-06-12/journey-component-matrix-2026-06-12.md)  
**Implementation:** `root_cd/hlk-erp` after P9b Phase A ([`p9b-phase-a-status-2026-06-13.md`](p9b-phase-a-status-2026-06-13.md))  
**Scope:** Phase A = visual polish + remediation rail; Phase B = journey-aware tactical cards (not started)

## Executive summary

Phase A delivered shared chrome (hero, POV switcher, freshness strip, prong strip, remediation rail, drawer runbook, v1 audit accordion). **~35% of T2 Operator components** and **~15% of T2 Director components** are live. Auditor, Finance, and Compliance lenses are **stub empty states only**. The biggest Phase B gap is **BFF insight population** — `insights.ts` only emits three remediation cards; matrix types (`staleness`, `intent_criticality`, etc.) exist in `types.ts` but have no builders.

---

## Status legend

| Status | Meaning |
|:---|:---|
| **shipped** | Matches matrix intent at correct tier |
| **partial** | UI or data exists but wrong POV, tier, or surface |
| **missing** | No implementation |
| **blocked-on-data** | Needs new BFF field / external script output before UI can ship |

---

## Shared chrome (all POV)

| Stage | Component | Status | Evidence / gap |
|:---|:---|:---|:---|
| Discover | Hero + program name | **shipped** | `research-center-client.tsx` |
| Triage | Insight card shell | **shipped** | `insight-card-rail.tsx` |
| Act | Drill-down Sheet (T1–T2) | **shipped** | Runbook + govern + T3 collapsible |
| Audit | v1 four-panel accordion | **shipped** | WIP, ledger, radar, KiRBe — collapsed default |
| Discover | Card question framework (what/when/why/how) | **partial** | Drawer has outcome/when/command; card face is headline + detail only |

**Phase B additions (plan §B.1):** `JourneyStepIndicator`, `FreshnessStripV2` (micro-CTA per badge), `InsightRailHeader`, `VerifyBanner` — all **missing**.

---

## Operator lens (T2 first — 17 matrix rows)

| Stage | Component | Min | Status | Notes |
|:---|:---|:---:|:---|:---|
| Discover | POV segmented switcher | 1 | **shipped** | URL `?pov=` + session; Select @375 |
| Discover | Freshness strip — ledger badge | 1 | **shipped** | `freshness-strip.tsx` |
| Discover | Freshness strip — radar badge | 1 | **shipped** | Overdue / block_govern in badge detail |
| Discover | Freshness strip — KiRBe badge | 1 | **shipped** | Health probe |
| Discover | Freshness strip v2 micro-CTA | — | **missing** | Phase B; badges are display-only |
| Triage | Remediation — ledger zero | 1 | **shipped** | `insights.ts` → `remediation-ledger-zero` |
| Triage | Remediation — radar empty | 1 | **shipped** | `remediation-radar-empty` |
| Triage | Remediation — KiRBe unhealthy | 1 | **shipped** | `remediation-kirbe-unhealthy` |
| Triage | Staleness overdue card | 1 | **blocked-on-data** | Radar BFF has `overdueCount` / rows; no insight card |
| Triage | Mirror drift card | 0 | **blocked-on-data** | No `check-drift.py` BFF hook |
| Triage | Env / deploy gap card | 0 | **partial** | Reader-not-configured woven into remediation copy, not standalone card |
| Triage | WIP pack stale card | 0 | **blocked-on-data** | WIP panel in accordion only; no stale-card logic |
| Act | Primary CTA — runbook sweep | 1 | **shipped** | Copy-to-clipboard + toast |
| Act | Runbook outcome block (T1) | 1 | **shipped** | Drawer Act section |
| Act | Env fix micro-CTA (strip) | 1 | **missing** | Phase B FreshnessStripV2 |
| Act | Artifact open — source ledger | 0 | **partial** | Drill-down govern link; not primary CTA |
| Audit | v1 ledger panel | 1 | **shipped** | Accordion; stats inline (IF-03) |
| Audit | v1 radar panel | 1 | **shipped** | Register excerpt table |
| Audit | Validator stdout link | 0 | **missing** | No last-verdict feed |

**Operator T2 score:** 11 shipped · 3 partial · 4 missing/blocked · **3/3 min triage cards met** when env gaps exist; **0/1 staleness card** when radar has overdue rows but env OK.

---

## Director lens (T2 first — 14 matrix rows)

| Stage | Component | Min | Status | Notes |
|:---|:---|:---:|:---|:---|
| Discover | POV switcher (Director) | 1 | **shipped** | Shared switcher |
| Discover | Program health summary chip | 0 | **missing** | No roadmap phase rollup BFF |
| Triage | Intent-criticality (ICS top) | 1 | **blocked-on-data** | Type in schema; no `intent_ranked_regression` feed |
| Triage | Ledger completion card | 1 | **partial** | BFF has `completionPct`; shown in accordion + prong strip, not Director card |
| Triage | Phase blocker card | 1 | **blocked-on-data** | No initiative registry / roadmap BFF |
| Triage | Research pack staleness | 0 | **blocked-on-data** | WIP panel data not surfaced as card |
| Triage | Quality Fabric gap card | 0 | **missing** | No UAT/synthesis findings feed |
| Triage | Remediation when env blocks | 0 | **partial** | Director gets same 3 remediation cards as Operator |
| Triage | Prong coverage mini-strip | 0 | **shipped** | `ProngStrip` on **all** lenses (Gate C / D-IH-96-H) |
| Act | Initiative phase CTA | 1 | **missing** | No Director-specific phase deep links |
| Act | ICS-ranked finding drawer | 0 | **missing** | — |
| Act | Planning README cross-link | 0 | **missing** | — |
| Audit | Raw ICS dimension scores | 0 | **missing** | T3 |
| Audit | Initiative code table | 0 | **missing** | T3 |

**Director T2 score:** When env healthy → **LensEmptyState only** — **0/3 min cards**. Phase B must populate non-remediation cards.

---

## Auditor lens (T3 — 11 rows)

| Stage | Component | Min | Status | Notes |
|:---|:---|:---:|:---|:---|
| Discover | POV switcher (Auditor) | 1 | **shipped** | — |
| Discover | RBAC proof strip | 1 | **missing** | No demo redaction banner |
| Triage | Panel presence card | 1 | **partial** | Panels exist in accordion; no triage card |
| Triage | UAT manifest link card | 1 | **missing** | Empty state defers to “later release” |
| Triage | Auth path evidence card | 1 | **missing** | — |
| Triage | Figma divergence card | 0 | **missing** | — |
| Triage | axe / a11y disposition | 0 | **missing** | — |
| Act | Doc-link CTA (redacted) | 1 | **missing** | CTAs are full runbook copy, not redacted |
| Act | Three-plane evidence row | 1 | **partial** | In remediation drawer only |
| Audit | Manifest sha256 table | 1 | **missing** | — |
| Audit | Impeccable audit excerpt | 0 | **missing** | — |

**Auditor:** **1/11 shipped** (POV only). Plan §B.2 allows stubs until T3 polish.

---

## Finance lens (T3 — 8 rows)

| Stage | Component | Min | Status |
|:---|:---|:---:|:---|
| Discover | POV switcher | 1 | **shipped** |
| Triage | Settlement risk card | 1 | **missing** (empty state stub) |
| Triage | Recon gap card | 0 | **missing** |
| Triage | Registered fact gate | 0 | **missing** |
| Triage | Counterparty exposure strip | 0 | **missing** |
| Act | FINOPS dashboard CTA | 1 | **missing** |
| Act | Recon runbook block | 0 | **missing** |
| Audit | Raw register excerpt | 0 | **missing** |

---

## Compliance lens (T3 — 9 rows)

| Stage | Component | Min | Status |
|:---|:---|:---:|:---|
| Discover | POV switcher | 1 | **shipped** |
| Triage | block_govern staleness card | 1 | **partial** | Radar panel highlights rows; no Compliance triage card |
| Triage | Canonical vs mirror drift | 1 | **blocked-on-data** | No drift BFF |
| Triage | CSV gate pending | 0 | **missing** |
| Triage | SSOT registry audit | 0 | **missing** |
| Triage | Decision register freshness | 0 | **missing** |
| Act | HLK validator runbook CTA | 1 | **missing** |
| Act | Mirror DML guide link | 0 | **missing** |
| Audit | PRECEDENCE excerpt | 0 | **missing** |

---

## Aggregate gap summary

| POV | Shipped | Partial | Missing / blocked | T2 min met? |
|:---|:---:|:---:|:---:|:---:|
| **Operator** | 11 | 3 | 5 | Yes *if env broken*; No *if healthy + overdue radar* |
| **Director** | 2 | 2 | 10 | **No** (empty rail when healthy) |
| **Auditor** | 1 | 2 | 8 | **No** |
| **Finance** | 1 | 0 | 7 | **No** |
| **Compliance** | 1 | 1 | 7 | **No** |
| **Shared chrome** | 4 | 1 | 4 (Phase B chrome) | — |

---

## Phase B build order (recommended)

Hard sequence per revision plan: **Phase A operator verify → Phase B → Phase C Figma**.

### Wave B1 — Operator T2 completion (unblocks P11 happy path)

| Priority | Component | Work | Primary file(s) |
|:---:|:---|:---|:---|
| **B1.1** | Staleness overdue card | Map `radar.overdueCount` + `blockGovernCount` → `type: "staleness"` insight when >0 | `lib/research-center/insights.ts` |
| **B1.2** | FreshnessStripV2 micro-CTA | Per-badge action (copy sweep cmd, open env doc) | `freshness-strip.tsx` |
| **B1.3** | InsightRailHeader | Lens label + card count + “≤7 signals” | `insight-card-rail.tsx` |
| **B1.4** | Env / deploy gap card | Standalone when `readerConfigured === false` | `insights.ts` |

### Wave B2 — Director T2 core (fixes empty Director rail)

| Priority | Component | Work | Dependency |
|:---:|:---|:---|:---|
| **B2.1** | Ledger completion card | Surface `completionPct`, prong top-N on T0 card | Ledger BFF (exists) |
| **B2.2** | Intent-criticality card | ICS placeholder → live when regression JSON available | **blocked-on-data** until AKOS artifact path |
| **B2.3** | Phase blocker card | `master-roadmap` / initiative registry reader | **blocked-on-data** — new BFF |
| **B2.4** | Initiative phase CTA | Drawer links to planning deep sections | B2.3 or static I96 links |

### Wave B3 — Journey chrome + verify loop

| Priority | Component | Work |
|:---:|:---|:---|
| **B3.1** | JourneyStepIndicator | Sign-in → Lens → Act → Verify |
| **B3.2** | VerifyBanner | Post-CTA freshness re-check prompt |
| **B3.3** | Drawer tier split | Explicit T1/T2/T3 collapsibles per plan §B.3 |

### Wave B4 — Operator conditionals (when data lands)

| Priority | Component | Blocker |
|:---:|:---|:---|
| **B4.1** | WIP pack stale card | GitHub WIP list + frontmatter `last_review` |
| **B4.2** | Mirror drift card | `check-drift.py` or compliance mirror delta API |
| **B4.3** | Validator stdout link (T3) | Last `validate_research_action.py` verdict artifact |

### Wave B5 — T3 lens stubs (Auditor / Finance / Compliance)

Per plan §B.2: replace `LensEmptyState` with minimum 2–3 cards each — **after** B1–B2 stable.

| Lens | First cards to ship |
|:---|:---|
| **Auditor** | UAT manifest link · panel presence · read-only doc-link CTA |
| **Finance** | Settlement risk placeholder → FINOPS register feed |
| **Compliance** | block_govern card from radar · HLK validator runbook CTA |

---

## Cross-references

| Artifact | Path |
|:---|:---|
| Phase B+C unified plan | [`research-center-phase-bc-tranche-plan-2026-06-12.md`](research-center-phase-bc-tranche-plan-2026-06-12.md) |
| hlk-erp UI inventory | [`research-center-hlk-erp-ui-inventory-2026-06-12.md`](research-center-hlk-erp-ui-inventory-2026-06-12.md) |
| BFF live-data spec | [`research-center-bff-live-data-spec-2026-06-12.md`](research-center-bff-live-data-spec-2026-06-12.md) |
| Operator check-links | [`operator-check-links-2026-06-12.md`](operator-check-links-2026-06-12.md) |
