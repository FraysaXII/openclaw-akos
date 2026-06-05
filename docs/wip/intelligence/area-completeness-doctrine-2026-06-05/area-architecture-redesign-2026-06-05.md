---
intellectual_kind: research_brainstorm
parent_initiative: INIT-OPENCLAW_AKOS-93
related_initiatives: [88, 86, 79]
authored: 2026-06-05
status: active
language: en
named_decision: D-AREA-DEF (extended scope per operator 2026-06-05)
source_ledger: source-ledger.csv
control_confidence_level: Keter
note: Challenges prior area-shaping decisions; destined for LOGIC_CHANGE_LOG mint after operator review
---

# Area architecture redesign — semantic review + 2-D maturity model + learning loop

> **Operator brief (2026-06-05):** *"full [maturity model] because I have no confidence on
> some topics … we still have drifted folders in the wrong/not-optimal area … help on that
> semantic understanding and challenge my previous decisions all the way … each area's tree
> boundaries are almost non-existent and really inconsistent … it's also about the hierarchy
> of artifacts … find different [issues] than my examples … brainstorm over everything …
> mint this in our logic change log, because this is big … this logic change needs to be
> monitored, improved every time … an ever-value-growing learning loop of governed cross-area
> know-how."*
>
> This document is the **thinking-seat brainstorm** that answer demands. It is deliberately
> opinionated and challenges prior decisions. **No canonical edit happens until operator
> review** (the LOGIC_CHANGE_LOG mint + implementation are gated). Grounded in the 125-source
> ledger; external anchors cited inline by `SRC-AREA-EXT-*`.

## 1. The reframe that unlocks everything — Holistika areas vs the APQC standard

The global standard for "what functions exist and what belongs where" is **APQC's Process
Classification Framework** (`SRC-AREA-EXT-63/64`) — 13 enterprise categories in a 5-level
hierarchy (Category → Process Group → Process → Activity → Task), split into **operating** vs
**management/support**. Mapping our 7 areas to it is the sharpest test of our boundaries:

| Holistika area | Closest APQC category | Boundary verdict |
|:---|:---|:---|
| **Data** | 8.0 Manage IT (data subset) | clean, narrow |
| **Tech** | 8.0 Manage IT + 2.0 Develop Products & Services | clean (Envoy = the 2.0 product-dev intensive arm) |
| **Finance** | 9.0 Manage Financial Resources | clean |
| **Marketing** | 3.0 Market & Sell | clean (but also carries Brand, which APQC scatters) |
| **Operations** | **1.0 Strategy + 6.0 Customer Service + 12.0 External Relationships + parts of 4/5** | **BUNDLED — 4 categories in one area = the blur** |
| **People** | **7.0 Human Capital + 13.0 Develop & Manage Business Capabilities** | **DUAL MANDATE — the overload source** |
| **Research** | 2.0 Develop Products (R&D) + 1.0 Strategy | thin, under-built |

**The load-bearing insight (challenges a prior decision):** Holistika's *"People is the
discipline of disciplines"* (`SRC-AREA-INT-10` §2) is **not** APQC 7.0 (Human Capital / HR).
It is APQC **13.0 — Develop & Manage Business Capabilities**: the meta-function that defines
how every other function operates. This is *correct and defensible* — but it means People
carries **two different mandates** that have never been separated:

- **People-as-13.0** (capability/methodology): legitimately owns cross-area disciplines —
  UAT, inter-wave regression, index-integrity, synthesis-before-tranche, PWF, intent-ranked
  regression, research-action, area-governance, the Quality Fabric, the design-pattern library.
- **People-as-7.0** (human capital): owns Compliance, Ethics, Learning, People Operations,
  engagement models, hiring/payroll lifecycle.

Once you see the dual mandate, the operator's "People has almost every area's canonical"
resolves into a **precise, fixable** statement: People correctly holds *cross-area
methodology* (13.0) but has also absorbed *area-operational disciplines that belong to the
consuming areas* (7.0 confusion). That is drift — and it is identifiable.

## 2. Drift inventory (challenging prior decisions; ★ = NEW, beyond operator's examples)

| ID | Drift | Where it is | Where it belongs | Grounding |
|:---|:---|:---|:---|:---|
| **★ DRIFT-1** | `MKTOPS_DISCIPLINE.md` (Marketing ops) parked in People | `People/canonicals/` | **Marketing** area | It is area-operational, not a cross-area pattern (`SRC-AREA-EXT-24` bounded context: model belongs where it's consumed) |
| **★ DRIFT-2** | `TECHOPS_DISCIPLINE.md` (Tech reliability ops) parked in People | `People/canonicals/` | **Tech** area | same |
| **★ DRIFT-3** | `DATAOPS_DISCIPLINE.md` (Data quality ops) parked in People | `People/canonicals/` | **Data** area | Data scores 92% yet its own ops discipline lives in People — a placement-integrity miss |
| **★ DRIFT-4** | `UX_DISCIPLINE.md` parked in People | `People/canonicals/` | **Marketing** (a `UX Designer` sub-area already exists under Marketing/Brand) | UX is consumer-surface, not capability-meta |
| **★ DRIFT-5** | Two research disciplines, two different homes | `RESEARCH_HEAD_DISCIPLINE` in People; `RESEARCH_ACTION_DISCIPLINE` in `Research/Methodology/` | reconcile to one home | Inconsistent placement of sibling doctrine |
| **DRIFT-6** | Operations bundles BizOps + RevOps + SMO + IntelligenceOps + Engagement | `Operations/` | split per scope | BizOps = company-wide chassis; RevOps = revenue child (`SRC-AREA-EXT-67/68/69`) — industry treats these as distinct |
| **DRIFT-7** | People's 13.0 methodology canonicals sit flat next to the People manifesto | `People/canonicals/` (≈30 files, no sub-area) | a labelled `People/Methodology/` (or QualityFabric) sub-area | tree-hierarchy inconsistency; cognitive-load (`SRC-AREA-EXT-29`) |
| **★ DRIFT-8** | Business-strategy artifacts (PRICING_MODEL, UNIT_ECONOMICS, INVESTMENT_THESIS, SALES_MOTION, MARKET_THESIS) under Operations/PMO | `Operations/PMO/canonicals/business-strategy/` | PRICING_MODEL ↔ **Finance/Marketing**; theses ↔ **Strategy (APQC 1.0)** | strategy + pricing are not PMO process artifacts |
| **DRIFT-9** | Tech physically split `Tech/` + `Envoy Tech Lab/`; matrix scores only `Tech` | two roots | **keep separate** (operator: deliberate engagement-intensive separation) but make Envoy **visible** to the matrix | Team Topologies: Envoy = complicated-subsystem/platform team (`SRC-AREA-EXT-32`) — legitimate, but currently an observability blind spot |

**Tree-hierarchy inconsistency (the operator's "trees are almost non-existent and
inconsistent"):** areas disagree on depth — some put SOPs at area root
(`People/Legal/SOP-*.md`), others under `canonicals/` (`People/Legal/canonicals/`); some have
`canonicals/dimensions/` for CSVs, others scatter CSVs; Data/Finance use a clean
`Governance/canonicals/` while Operations sprawls across PMO/RevOps/SMO/Engagement/IntelligenceOps
with no consistent `canonicals/` discipline. There is **no standard area file-plan** — which is
exactly what APQC's 5-level hierarchy (`SRC-AREA-EXT-64`) and records-management file-plans
exist to provide. **This is a missing component, not just untidiness** (see §4, AREA-16).

## 3. What an area IS — the refined definition (challenge-grade)

Synthesising DDD bounded context (`EXT-24/26`), Team Topologies (`EXT-29/32`), Data Mesh
(`EXT-33/34`), Wardley (`EXT-41`), and APQC (`EXT-63`):

> **An area is a bounded capability domain** — an internally consistent model + language
> (DDD), **aligned to one APQC-mappable function**, **owned end-to-end by a role-owner whose
> cognitive load it fits** (Team Topologies), **exposing a governed contract** to consuming
> areas (Data Mesh), and **of a declared *kind*** that sets its expected governance density:

| Area kind | Definition | Holistika examples | Expected density |
|:---|:---|:---|:---|
| **stream-aligned** | owns a value stream end-to-end | Finance, Marketing, Research | full bar |
| **platform** | provides self-serve substrate to all areas | Tech (+ Envoy as its product-dev arm), Data | full bar + SLO |
| **capability-meta** | mints patterns every area inherits (APQC 13.0) | **People (13.0 half)** | full bar + pattern-adoption metric |
| **human-capital** | the 7.0 HR function | **People (7.0 half)** | standard bar |

The **kind** is the missing variable. It explains why People feels different (it's two kinds
at once), why Tech/Envoy is legitimately split (platform + its intensive subsystem), and why
Operations is blurry (it's several kinds bundled). It also sets the **per-area tier** (decision 4B).

## 4. The 2-D maturity model (decision 1C + 3A + 4B, designed)

Replace the flat 14-item count with a **component × maturity-level grid** — the shape every
external model uses (DCAM `EXT-04`, CMMI `EXT-07`, Stanford `EXT-13`, capability heat-maps
`EXT-40`) — while **keeping our deterministic heuristic** (the rare strength, `EXT-14/15`).

**Maturity levels (CMMI-grounded, `SRC-AREA-EXT-07`):**

| Level | Name | Meaning for an area component |
|:---:|:---|:---|
| L0 | Absent | not present (= today's `gap`) |
| L1 | Initial | present but ad-hoc (= today's weak `partial`) |
| L2 | Managed | exists + owned + maintained |
| L3 | **Defined** | governed: validator/SOP/registry-backed (= today's `pass`; **the critical-pass bar**) |
| L4 | Measured | quantitatively tracked (metric/SLO) |
| L5 | Optimizing | self-improving via the learning loop (§6) |

**Components, reorganised into dimensions (Stanford-style), with criticality:**

| Dim | Components | Critical? (must reach L3) |
|:---|:---|:---|
| **Identity & boundary** | AREA-01 tree, AREA-02 charter, **AREA-14-KIND** (new: declared kind + APQC mapping) | ✅ critical |
| **Doctrine** | AREA-03 discipline, AREA-07 precedence | ✅ critical |
| **Execution** | AREA-04 process, AREA-05 roles, AREA-09 paired SOP+runbook | ✅ critical (AREA-09 threshold realistic — see F-4) |
| **Data & contract** | AREA-06 capability/confidence, AREA-08 dimensions, **cross-area contract** | ✅ critical |
| **Surfacing** | AREA-11 rule+skill, AREA-13 README | ⚪ enhancing (weighted) |
| **Mirror** | AREA-10 Supabase | ⚪ enhancing (skip-allowed) |
| **★ AREA-15 PLACEMENT-INTEGRITY** | *every canonical in the area belongs to it (no drift in/out per §2) AND it ships ≥1 consumed contract/SLO* | ✅ critical (the "what-belongs-where" outcome the operator named) |
| **★ AREA-16 FILE-PLAN** | *area tree conforms to the standard file-plan (canonicals/ + dimensions/ + SOP placement)* | ⚪ enhancing (the tree-consistency component) |

**Score** = NOT a flat %. An area is **complete for its tier** when (a) all **critical**
components reach **L3+**, (b) its **per-area acceptance criteria** pass (decision 3B kept as a
thin layer), and (c) ≥1 component reaches **L4** (a measured outcome — decision 3A). Enhancing
components contribute a weighted sub-score and a maturity badge (L0–L5) but never block.

This **does not invalidate** Data/Finance closures: both already meet critical-at-L3; they
simply gain a maturity badge and an explicit AREA-15 placement check (which would *catch
DRIFT-3* — Data's own ops discipline living in People).

## 5. Per-area target shaping (the recommendations to ratify)

1. **People → split the dual mandate in the tree.** Create `People/Methodology/` (the 13.0
   capability-meta home: Quality Fabric + the cross-area disciplines + design-pattern library)
   distinct from the 7.0 sub-areas (Compliance/Ethics/Learning/People Operations). The manifesto
   stays at People root. *Migrate DRIFT-1..4 out* to their consuming areas.
2. **Operations → resolve into scoped sub-areas** mapped to APQC: PMO (1.0 strategy/governance),
   RevOps (3.0/revenue), SMO (6.0 service), IntelligenceOps (research-adjacent), Engagement.
   Decide whether "Operations" is one area with clear sub-area contracts or splits (BizOps vs
   RevOps per `EXT-67`). **Open question O-1 for operator.**
3. **Tech + Envoy → declare the kind.** Tech = platform; Envoy Tech Lab = its complicated-
   subsystem/engagement-intensive arm. Keep separate (operator-confirmed) but make Envoy
   **matrix-visible** (AREA-01 counts both roots). Resolve the "heavy lifting sometimes leaks
   into other areas" concern via explicit Tech↔area contracts (AREA-15).
4. **Marketing → absorb UX (DRIFT-4) + clarify Brand.** UX_DISCIPLINE → Marketing; Brand stays.
5. **Research → build the charter + discipline** it's missing (it's the thinnest stream-aligned
   area; R&D = APQC 2.0).
6. **Finance / Data → add AREA-15 placement + AREA-14 kind**; otherwise hold (they're the bar).
7. **All areas → adopt the standard file-plan (AREA-16)** so trees stop being inconsistent.

## 6. The continuous learning loop (the operator's "ever-value-growing governed know-how")

This is **not** a one-time rulebook edit. It is a standing discipline that **improves every
cycle**, wired into the sweep machinery we already run:

```
            ┌─────────────────────────────────────────────┐
            ▼                                             │
  area-architecture sweep (wave-close)                    │
   = matrix (maturity grid) + placement-integrity (drift) │
            │                                             │
            ▼                                             │
  findings → 5-option disposition (inter-wave enum)       │
   rework-now / forward-charter / defer-OPS /             │
   accept-as-canon / escalate-to-blocker                  │
            │                                             │
            ▼                                             │
  learnings fold back: new drift patterns become          │
  AREA-NN components OR weights adjust OR kinds refine ────┘
   (the model gets smarter each wave = value compounding)
```

- **Cadence governed by research-radar** (`SRC-AREA-EXT` freshness posture) — not a hardcoded interval.
- **Value order by intent-ranked ICS** (`SRC-AREA-INT-27`) — fix highest-criticality drift first.
- **Mechanical safety-net by inter-wave regression** (`SRC-AREA-INT-23`) — the full sweep never deleted.
- **Each cycle's learnings are minted** — new components, new weights, new kinds — so the
  definition of "complete" *itself matures* (an L5 "Optimizing" property applied to the bar).
- **Governed cross-area know-how** accumulates in the placement-integrity history: every "this
  artifact belongs in area X not Y" decision becomes reusable doctrine — a good Holistika person
  (and a good agent) learns where things go *from the accumulated loop*, which is the operator's
  "a good Holistika personnel would know what to put from what area where."

## 7. What to mint (gated on operator review) + LOGIC_CHANGE_LOG framing

Because this revises foundational doctrine, it is a **methodology version bump** logged in
`LOGIC_CHANGE_LOG.md` (`SRC-AREA-INT` LOGIC_CHANGE_LOG) + a `D-IH-NN-X` decision. Proposed mint set:

1. **`AREA_GOVERNANCE_DISCIPLINE.md` v2** — refined area definition (§3), kinds, 2-D maturity
   model (§4), AREA-14/15/16, per-tier thresholds, the learning loop (§6).
2. **`akos/hlk_area_completeness.py` v2** — component × level grid; criticality flags; kind enum;
   placement-integrity + file-plan probes; tier thresholds. Keep deterministic.
3. **`scripts/validate_area_completeness.py` v2** — emit maturity grid + drift report.
4. **`LOGIC_CHANGE_LOG.md`** entry — "Area governance v1→v2: flat checklist → tiered 2-D
   capability-maturity model with placement integrity + learning loop."
5. **Drift remediation tranche** — migrate DRIFT-1..5/8 (operator-gated CSV/file moves).
6. **Learning-loop wiring** — area-architecture sweep into wave-close cadence + OPS anchor.

## 8. Open questions for the operator (the challenges)

- **O-1 (Operations):** one area with scoped sub-areas, OR split BizOps/RevOps/ServiceOps?
- **O-2 (People):** in-tree sub-area split (`People/Methodology/` for 13.0) — agree?
- **O-3 (drift moves):** approve migrating MKTOPS/TECHOPS/DATAOPS/UX out of People to their areas?
- **O-4 (Envoy):** keep separate + make matrix-visible (recommended), or fold into Tech?
- **O-5 (scope):** do this as a **new initiative** (it's initiative-sized) or a phase under I93?
- **O-6 (depth):** full 2-D model now (1C), or stage it (criticality-weighting first, levels next)?

## 9. Cross-references

- [`master-synthesis.md`](master-synthesis.md) (the 4 sub-decisions; operator picked 1C/2A/3A/4B)
- [`baseline-state-2026-06-05.md`](baseline-state-2026-06-05.md) (matrix + topography + F-TOPO-1/2/3)
- Prongs [`A`](prong-a-internal-doctrine.md)/[`B`](prong-b-external-maturity.md)/[`C`](prong-c-domain-boundaries.md)/[`D`](prong-d-completeness-value.md)
- [`source-ledger.csv`](source-ledger.csv) (125 sources)
- Subject: [`AREA_GOVERNANCE_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md) · [`HOLISTIKA_ORGANISING_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_ORGANISING_DOCTRINE.md) · `LOGIC_CHANGE_LOG.md`
