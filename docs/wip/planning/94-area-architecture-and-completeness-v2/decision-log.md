---
initiative_id: INIT-OPENCLAW_AKOS-94
language: en
last_review: 2026-06-05
---

# I94 — Decision log

## D-IH-94-A — Area Architecture & Completeness v2 inception (rounds 1–3 ratified)

- **Decided:** 2026-06-05 (operator, across 3 ratification rounds)
- **Class:** architecture · **Reversibility:** medium · **Status:** active
- **Extends:** `D-IH-93-B` (area-governance meta-process; not superseded)
- **Evidence:** 131-source research action `docs/wip/intelligence/area-completeness-doctrine-2026-06-05/`

**Decision.** Launch I94 to evolve area governance from the flat 14-component checklist (v1)
to a **2-D capability-maturity model v2**, grounded in external standards (DAMA-DMBOK, DCAM,
CMMI, COBIT, ISO/IEC 38500, DDD bounded contexts, Team Topologies, Data Mesh, APQC PCF,
PMBOK 7/8, ITIL 4) and the internal evidence sweep. The ratified model:

1. **Scoring (1C):** component × maturity-level grid (L0 Absent → L5 Optimizing); critical
   components must reach L3 (Defined/governed); enhancing components weighted; keep the
   deterministic heuristic (intersubjective verifiability).
2. **Boundary (2A):** an area = a bounded context (internally consistent model) aligned to a
   value stream, sized to a role-owner's cognitive load, owned end-to-end, exposing a governed
   contract, of a declared **kind** (stream-aligned / platform / capability-meta / human-capital).
3. **Outcome (3A):** new **AREA-15 placement-integrity** — every canonical belongs to its area
   (no drift) + the area ships ≥1 consumed contract/SLO.
4. **Threshold (4B):** per-area **tier** + critical-must-pass overrides a single global %.
5. **Operations (Q-OPS):** Operations = delivery/execution-capacity area scored on the **PMBOK 7
   performance domains**; project/service as a tag; **IntelligenceOps evicted** (research-application).
6. **People (Q-PEOPLE):** cross-area disciplines home = **People/Compliance** (methodology-
   enforcement; "the methodology is the product"); area-ops disciplines (MKTOPS/TECHOPS/DATAOPS/
   UX) drift OUT to their areas. Three-verb pipeline: Research authors → People mints → Compliance enforces.
7. **Entity (Q-ENTITY):** add an **entity axis** (Holistika / Think Big / HLK Tech Lab); fold
   `Envoy Tech Lab/` under Tech-area governance + make matrix-visible (careful research-first rework).
8. **Legal (Q-LEGAL):** promote **Legal to the 8th scored area** + design LegalOps (research-first).
9. **File-plan (Q-SUBFOLDER):** **AREA-16 sub-folder = role/sub-area FK** (validator-enforced RACI doctrine).
10. **Bugs:** BUG-1 (Legal unscored) + BUG-2 (entity axis unmodeled) fixed by the above.

**Why now.** Operator: "do it now to maintain momentum … improve all of their plans before
starting … heavy lifting now." Sequencing it before the 5-area sweep prevents re-measuring five
areas with a known-incomplete ruler.

**Mint set (this commit / P0).** INITIATIVE_REGISTRY row I94; this decision row; planning README
row; supporting artifacts. Doctrine + code v2 (P1) and all canonical-CSV / file-move changes
(P3/P4/P7) carry their own operator gates per `akos-baseline-governance.mdc`.

## Reserved (forward)

- **D-IH-94-B** — P1 doctrine + `hlk_area_completeness.py` v2 + LOGIC_CHANGE_LOG ratification.
- **D-IH-94-C** — Operations PMBOK reframe + IntelligenceOps relocation target.
- **D-IH-94-D** — Legal 8th-area + LegalOps design.
- **D-IH-94-E** — Envoy/entity-axis rework.
