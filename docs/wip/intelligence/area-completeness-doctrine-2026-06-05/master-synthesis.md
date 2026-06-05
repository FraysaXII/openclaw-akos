---
intellectual_kind: research_master_synthesis
parent_initiative: INIT-OPENCLAW_AKOS-93
related_initiatives: [88, 86]
authored: 2026-06-05
status: active
language: en
named_decision: D-AREA-DEF
source_ledger: source-ledger.csv
source_count: 117
control_confidence_level: Euclid
---

# Master synthesis — the definitional regression on "area" + "completeness"

> Stage 4 (synthesize) + Stage 5 (govern) of the research action. Rolls up Prongs A–D
> (117 sources: 55 internal `SRC-AREA-INT-*`, 62 external `SRC-AREA-EXT-*`) into the
> **definitional regression** the operator asked for, then surfaces a **ranked option set**
> for decision **D-AREA-DEF**. No canonical edit happens until the operator picks (Step 7
> gate).

## 1. Cross-prong convergence (what all four prongs agree on)

| Convergent finding | Prongs | Sources |
|:---|:---|:---|
| Mature governance bars are **2-D (component × maturity-level)**, not flat checklists | B, C | DCAM `EXT-04/05`, CMMI `EXT-07/09`, IBM `EXT-12`, Stanford `EXT-13`, capability heat-maps `EXT-37/40` |
| "Complete" means **critical-vs-optional**, not "all fields present" | A, D | DAMA-UK `EXT-47`, IBM `EXT-48`, our own `confidence_levels` `INT-20` |
| A domain/area needs a **boundary criterion** (consistency + value-stream + cognitive-load + owner + contract), not just a folder | A, C | DDD `EXT-24/26`, Team Topologies `EXT-29/32`, Data Mesh `EXT-34`, our `INT-54` |
| Different areas warrant **different governance density** (per-area tier), not one global % | B, C | CMMI continuous `EXT-07`, IBM per-domain `EXT-12`, Wardley evolution `EXT-41`, DMBOK `EXT-02` |
| Bars should pair a **universal DoD** with **per-item Acceptance Criteria** + **outcome/value** | A, D | Scrum DoD/AC `EXT-52`, GQM `EXT-58`, OKR `EXT-61`, Data-Mesh-product `EXT-33` |
| **Keep** our deterministic heuristic — it satisfies "intersubjective verifiability" most real models lack | B | maturity-design DPs `EXT-14/15` |

**One-sentence rollup:** the 14-component bar is a *good Definition-of-Done for artifact
presence with a rare strength (determinism)*, but the field says a governance-maturity model
should also be **leveled, weighted by criticality, boundary-defined, per-area-tiered, and
outcome-aware** — five axes our current bar collapses.

## 2. Definitional regression — "What is an area?"

**Current (implicit) definition** (`INT-01`, `INT-10`): *an O5-1 folder tree with role/sub-area
structure, member roles in `baseline_organisation.csv`, and processes in `process_list.csv`.*

**Regression test:** does it survive the research + the topography? **Partially — it fails two
checks:**

- ✗ **Boundary check (F-TOPO-1):** Tech spans `Tech/` + `Envoy Tech Lab/` — one area, two
  models. The current definition cannot say which folders constitute "Tech" or whether Envoy
  Tech Lab is a sub-area or its own area. DDD/TT (`EXT-24`, `EXT-29`) require a consistency +
  ownership boundary the definition lacks.
- ✗ **Kind check:** People (enabling/discipline-of-disciplines) and Tech (platform/substrate)
  are structurally *different kinds* of area than Finance (stream-aligned) — Team Topologies
  `EXT-32` names exactly these shapes. The flat definition treats all seven as identical.

**Research-grounded refined definition (proposed, for ratification):**

> *An **area** is a **bounded context** — a slice of Holistika's operating model with an
> internally consistent model + language — that is **aligned to a value stream**, **sized to
> a role-owner's cognitive load**, **owned end-to-end**, and **exposes a governed contract**
> to the areas that consume it. Areas may be of different **kinds** (stream-aligned, platform,
> or enabling), which sets their expected governance density.*

This keeps the folder/role/process structure as the *physical manifestation* but adds the
**criterion** (consistency + stream + load + owner + contract + kind) that resolves F-TOPO-1
and future split decisions.

## 3. Definitional regression — "What does completeness mean for us?"

**Current definition** (`INT-01/02/03`): *the fraction of the 14 flat components that score
`pass`, with 88% + zero-unexpected-gap as the closure bar.*

**Regression test:** **fails three checks:**

- ✗ **Critical-vs-optional (D.1):** all 14 weigh equally; a missing **charter** (AREA-02,
  high) costs the same as a missing **rule+skill** (AREA-11, low). DAMA `EXT-47` says
  completeness must separate critical from optional.
- ✗ **Outcome axis (D.4, C.3):** every component checks **artifact presence** ("README
  exists"), none checks **outcome** ("the area reliably ships its contracted capability").
  OKR `EXT-61` / Data Mesh `EXT-36` say a thing is complete when it delivers a *contracted
  product*, not when it has the parts.
- ✗ **Pairing cliff (F-TOPO-3):** AREA-09 is `partial` for **all seven** areas (0 paired
  everywhere), capping every area near ~93% regardless of effort — a structural artifact of
  flat counting, not a real maturity signal.

**Research-grounded refined definition (proposed, for ratification):**

> *An area is **complete** for its **tier** when (a) all **critical** components pass
> (charter, discipline, process, roles, precedence, contract), (b) its **per-area Acceptance
> Criteria** pass (its own load-bearing artifacts), and (c) it demonstrates one **outcome
> signal** (a consumed contract / shipped capability / passing SLO) — with enhancing
> components (README, rule+skill, mirrors) tracked but **weighted**, not gating.*

This keeps the 14 components as the **universal DoD** and the deterministic heuristic, but
adds **criticality weighting**, a thin **per-area AC** layer, an **outcome** check, and a
**per-area tier** so density matches the area's kind/evolution.

## 4. Findings (attributed + dispositioned, per intent-ranked-regression craft)

| ID | Finding | Attribution | Severity | Disposition (proposed) |
|:---|:---|:---|:---:|:---|
| **F-1** | Flat count, no criticality weighting | pre-existing (I93 design) | high | **option in §5** — operator picks weighting model |
| **F-2** | No boundary criterion; Tech spans 2 roots (F-TOPO-1) | pre-existing | high | **option in §5** — adopt bounded-context criterion + resolve Tech/Envoy |
| **F-3** | No outcome/value axis (artifact-presence only) | pre-existing | medium | **option in §5** — add outcome component or defer |
| **F-4** | AREA-09 pairing cliff caps all areas (F-TOPO-3) | pre-existing | medium | forward-charter — AREA-09 `pass` rule needs a realistic threshold |
| **F-5** | No per-area tier; one global 88% for 7 different kinds | pre-existing | medium | **option in §5** — per-area or per-tier threshold |
| **F-6** | 14-component bar vs 10-pillar ReOps lens unreconciled | pre-existing (I88/I93) | low | on-radar — reconcile at I88 P3 canonical mint |
| **F-7** | Deterministic heuristic = intersubjective verifiability | strength | — | **keep** — do not trade determinism for richness |

**No new regressions** attributable to this session (additive evidence + ledger only).

## 5. Decision D-AREA-DEF — ranked option set (operator picks; Stage 5 govern)

Four sub-decisions. Each is independent; the operator can mix (e.g. 1B + 2A + 3C + 4B).

### Sub-decision 1 — `def-complete` scoring model
- **1A — Keep flat 14/14 + 88% bar.** Zero rework; preserves I93/Finance closures as-is.
  Accepts F-1/F-3/F-5. *(status-quo)*
- **1B — Add criticality weighting (critical-must-pass + weighted enhancers).** ~Half-day:
  tag each component critical/enhancing in `hlk_area_completeness.py`; score = critical-gate +
  weighted enhancers. Closes F-1; grounded in DAMA `EXT-47` + CMMI `EXT-07`. **[recommended]**
- **1C — Full 2-D maturity model (component × L0–L5).** Richest (DCAM/CMMI-grade) but a real
  build; re-scores all 7 areas. Highest fidelity, highest cost/risk.

### Sub-decision 2 — `def-area` boundary criterion
- **2A — Adopt the bounded-context criterion** (consistency + stream + load + owner + contract +
  kind) in `AREA_GOVERNANCE_DISCIPLINE.md` §1, and **resolve Tech/Envoy-Tech-Lab** (one area
  w/ explicit sub-area, or split). Closes F-2; grounded in DDD/TT/Data-Mesh. **[recommended]**
- **2B — Document criterion only; defer Tech/Envoy resolution to Tech-area buildout.** Lower
  scope; F-2 partially open.
- **2C — Keep folder-only definition.** Zero rework; F-2 stays open.

### Sub-decision 3 — outcome/value axis
- **3A — Add an AREA-15 "outcome/contract" component** (area ships ≥1 consumed contract / SLO).
  Closes F-3; grounded in OKR/Data-Mesh. Expands the bar to 15.
- **3B — Add per-area Acceptance Criteria layer** (keep 14 DoD; add thin per-area AC list).
  Closes F-3 with less churn; grounded in Scrum DoD/AC `EXT-52`. **[recommended]**
- **3C — Defer outcome axis** to post-5-area sweep. F-3 on-radar.

### Sub-decision 4 — `def-threshold`
- **4A — Keep single global 88%.** Status-quo.
- **4B — Per-area tier threshold** (stream-aligned areas 88%; platform/enabling areas a
  tier-appropriate bar; critical-components-must-pass overrides %). Closes F-5; grounded in
  CMMI-continuous + Wardley-evolution. **[recommended]**
- **4C — Critical-must-pass + drop the global %** entirely (binary "all critical pass" gate).
  Cleanest but a bigger doctrine shift.

## 6. Stage 8 disposition (per prong)

- **Prong A** → **promoted** (the internal-doctrine gap is the spine of the option set).
- **Prong B** → **promoted** (maturity-level + per-domain scoring → options 1C/4B).
- **Prong C** → **promoted** (boundary criterion → option 2A; resolves F-TOPO-1).
- **Prong D** → **promoted** (DoD/AC + outcome → option 3B; WSJF already in ICS).
- **10-pillar reconciliation (F-6)** → **on-radar** for I88 P3.
- **AREA-09 pairing cliff (F-4)** → **deferred** to a focused AREA-09-threshold fix.

## 7. Recommendation in one line

Adopt the **low-churn, high-fidelity** combination **1B + 2A + 3B + 4B** — weight by
criticality, add the bounded-context boundary criterion (and resolve Tech/Envoy), pair the
DoD with per-area Acceptance Criteria, and tier the threshold — **keeping** the deterministic
heuristic and **not** invalidating the Data/Finance closures. Then proceed to option A
(Finance F4 → I88) and option D (5-area sweep) measuring against the upgraded bar.

## 8. Cross-references

- [`research-action-pack.md`](research-action-pack.md) · [`baseline-state-2026-06-05.md`](baseline-state-2026-06-05.md)
- Prongs: [`A`](prong-a-internal-doctrine.md) · [`B`](prong-b-external-maturity.md) · [`C`](prong-c-domain-boundaries.md) · [`D`](prong-d-completeness-value.md)
- Subject: [`AREA_GOVERNANCE_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md) + `akos/hlk_area_completeness.py`
- Ledger: [`source-ledger.csv`](source-ledger.csv) (117 sources; `validate_research_action.py` PASS)
