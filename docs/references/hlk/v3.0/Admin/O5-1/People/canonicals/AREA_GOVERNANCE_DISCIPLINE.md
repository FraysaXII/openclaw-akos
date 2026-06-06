---
title: Area Governance Discipline
language: en
intellectual_kind: people-canonical
access_level: 4
audience: J-OP;J-AIC
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - Founder/CEO
co_authors:
  - CPO
  - PMO
  - System Owner
last_review: 2026-06-06
last_review_by: Founder/CEO
last_review_at: 2026-06-06
last_review_decision_id: D-IH-95-D
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-93-B
  - D-IH-94-A
  - D-IH-95-D
status: charter
register: internal
doctrine_version: v3
linked_canonicals:
  - HOLISTIKA_QUALITY_FABRIC.md
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - PEOPLE_DESIGN_PATTERN_LIBRARY.md
  - LOGIC_CHANGE_LOG.md
  - ../Compliance/canonicals/PRECEDENCE.md
  - ../Compliance/canonicals/baseline_organisation.csv
  - ../../Data/Architecture/canonicals/CANONICAL_ARTICULATION_MODEL.md
linked_cursor_rules:
  - .cursor/rules/akos-area-governance.mdc
  - .cursor/rules/akos-people-discipline-of-disciplines.mdc
  - .cursor/rules/akos-quality-fabric.mdc
linked_skills:
  - .cursor/skills/area-governance-craft/SKILL.md
companion_to:
  - HOLISTIKA_QUALITY_FABRIC.md
research_grounding: docs/wip/intelligence/area-completeness-doctrine-2026-06-05/
forward_charters:
  - akos/hlk_area_completeness.py v2 (2-D maturity grid + kind + entity + AREA-15/16)
  - scripts/validate_area_completeness.py v2 (maturity + placement + file-plan probes)
  - I94 P2-P9 (plan-improvement, Operations reframe, People-Compliance, entity/Envoy, Legal, subfolder=role, DATA regression, closure)
---

# Area Governance Discipline (v3)

> Seventeenth Quality Fabric specialty. People mints the **area-completeness shape** any O5-1
> area inherits when created or matured. **v3** (`D-IH-95-D`, I95) adds the **articulation
> tier** (§7.5): completeness = *present* (the v2 grid) **and** *wired* (every owned canonical
> participates in an active HCAM triple) — paired Data-federated. **v1** (`D-IH-93-B`, I93 P0)
> defined a flat 14-component checklist. **v2** (`D-IH-94-A`, I94) evolves it — grounded in a 131-source
> research action ([`area-completeness-doctrine-2026-06-05/`](../../../../../wip/intelligence/area-completeness-doctrine-2026-06-05/))
> spanning DAMA-DMBOK, DCAM, CMMI, COBIT, ISO/IEC 38500, DDD bounded contexts, Team Topologies,
> Data Mesh, APQC PCF, PMBOK 7/8 and ITIL 4 — into a **2-D capability-maturity model** with
> area **kinds**, an **entity axis**, **placement integrity**, a **file-plan**, and **per-tier
> thresholds**, while **keeping the deterministic heuristic** (the rare strength v1 already had).

## 1. Purpose + what changed v1 → v2

Holistika areas must be **governable at comparable depth** — not ad-hoc folder trees. v1 made
that countable with a flat 14-component checklist. v2 fixes five things the research showed the
flat checklist collapsed (master-synthesis §1-3 + area-architecture-redesign + round3-assessment):

| Axis | v1 | v2 |
|:---|:---|:---|
| Scoring | flat pass/partial/gap count | **2-D grid**: each component scored on a **maturity level L0–L5** |
| Criticality | all components equal weight | **critical** components must reach **L3**; **enhancing** weighted, non-gating |
| Boundary | "a folder exists" | **bounded-context definition** + a declared area **kind** |
| Threshold | one global 88% | **per-area tier** + critical-must-pass overrides the % |
| Outcome / placement | artifact-presence only | **AREA-15 placement-integrity** (what-belongs-where + a shipped contract) |
| Structure | unmodeled | **AREA-16 file-plan** (sub-folder = role/sub-area) + **entity axis** |

v2 **does not invalidate** the Data (92%) or Finance (93%) closures: both already meet
critical-at-L3; they gain a maturity badge + the AREA-15/16 checks.

## 2. What an area IS (the v2 definition)

> An **area** is a **bounded capability domain** — a slice of Holistika's operating model with an
> internally consistent model + language (DDD bounded context), **aligned to an APQC-mappable
> function**, **owned end-to-end by a role-owner whose cognitive load it fits** (Team Topologies),
> **exposing a governed contract** to consuming areas (Data Mesh), and **of a declared *kind***
> that sets its expected governance density.

### 2.1 Area kinds (sets the tier)

| Kind | Definition | Areas | Expected density |
|:---|:---|:---|:---|
| **stream_aligned** | owns a value stream end-to-end | Finance, Marketing, Research, Legal | full bar |
| **platform** | self-serve substrate for all areas | Tech, Data | full bar + SLO |
| **capability_meta** | mints patterns every area inherits (APQC 13.0) | People (methodology half) | full bar + pattern-adoption metric |
| **delivery_capacity** | the cross-cutting execution layer ("projects end, operations continue") scored on PMBOK 7 performance domains | Operations | PMBOK-domain bar |

### 2.2 The entity axis (new)

Every area declares its **entity** — the legal/brand vehicle that executes it, per
`baseline_organisation.entity`: **Holistika** (parent/governance), **Think Big** (business
operations), **HLK Tech Lab** (engineering entity; the `Envoy Tech Lab/` tree is its home, under
Tech-area governance). The entity is a governed tag, not a second scored unit.

### 2.3 The eight scored areas (v2)

**Data, Tech, Finance, Marketing, Operations, People, Research, Legal** — v2 adds **Legal**
(a first-class `area` in `baseline_organisation.csv` that v1 omitted; BUG-1 fix).

## 3. The 16 components (v2), by dimension + criticality

| Dim | Component | Critical? |
|:---|:---|:---:|
| Identity & boundary | AREA-01 parent tree · AREA-02 area charter · **AREA-14 KIND+ENTITY+APQC mapping** | critical |
| Doctrine | AREA-03 discipline charters · AREA-07 canonical/precedence | critical |
| Execution | AREA-04 process-list · AREA-05 baseline roles · AREA-09 paired SOP+runbook | critical |
| Data & contract | AREA-06 capability/confidence · AREA-08 dimension registries · cross-area contract | critical |
| Surfacing | AREA-11 cursor rule+skill · AREA-13 README | enhancing |
| Mirror | AREA-10 Supabase mirrors | enhancing (skip-allowed) |
| **AREA-15 PLACEMENT-INTEGRITY** | every canonical belongs to the area (no drift in/out) **and** the area ships ≥1 consumed contract/SLO | **critical** |
| **AREA-16 FILE-PLAN** | area sub-folder names FK to `baseline_organisation` role/`sub_area` (RACI doctrine) | enhancing |

## 4. The maturity ladder (CMMI-grounded)

| Level | Name | Meaning for a component |
|:---:|:---|:---|
| L0 | Absent | not present (= v1 `gap`) |
| L1 | Initial | present but ad-hoc (= weak `partial`) |
| L2 | Managed | exists + owned + maintained |
| L3 | **Defined** | governed: validator/SOP/registry-backed (= v1 `pass`; **critical-pass bar**) |
| L4 | Measured | quantitatively tracked (metric/SLO) |
| L5 | Optimizing | self-improving via the learning loop (§6) |

## 5. The compose_AREA v2 rule

```
compose_AREA(governance) -> 16-component x 6-level grid per area
  where:
    scored_areas = {Data, Tech, Finance, Marketing, Operations, People, Research, Legal}
    kinds        = {stream_aligned, platform, capability_meta, delivery_capacity}
    entities     = {Holistika, Think Big, HLK Tech Lab}
    levels       = {L0, L1, L2, L3, L4, L5}
    criticality  = {critical, enhancing}
    complete_for_tier(area) :=
        ALL critical components >= L3
        AND per-area acceptance criteria pass
        AND >= 1 component at L4 (a measured outcome)
    enhancing components -> weighted badge, never gating
    conservative_posture = emit skip/L0 when live evidence unavailable
    deterministic = same inputs -> same grid (intersubjective verifiability; keep from v1)
    runbook = scripts/validate_area_completeness.py ; matrix_mode = --matrix
```

Operations is scored on the **PMBOK 7 performance domains** (Governance, Scope, Schedule,
Finance, Stakeholders, Resources, Risk) mapped onto the 16 components; project-vs-service is a
**tag, not a split**.

## 6. The continuous learning loop (D-IH-94-A — "ever-value-growing governed know-how")

Area governance is a **standing discipline that matures every wave**, not a one-time edit:

1. **Sweep** at wave-close: maturity grid + placement-integrity + file-plan (`--matrix`).
2. **Disposition** findings via the inter-wave 5-option enum (rework-now / forward-charter /
   defer-OPS / accept-as-canon / escalate-to-blocker).
3. **Fold learnings back**: recurring drift becomes a new component, weight, or kind — so the
   definition of "complete" itself reaches L5 (Optimizing).

Cadence governed by research-radar; value order by intent-ranked ICS; mechanical safety-net by
inter-wave regression. Accumulated placement decisions become the reusable
"a good Holistika person knows what goes where" know-how (the AREA-15 history).

## 7. Cadence + INFO → FAIL ramp

- **on_demand** — operator/agent requests a baseline grid.
- **area_buildout** — before closing an area charter / CSV tranche.
- **wave_close** — the learning-loop sweep (§6).
- **pre_commit_self_test** — Pydantic + probe-registry chassis only (~2s; always-on circuit-breaker).

v2 lands at **charter** with INFO posture. Promotion to FAIL requires: (1) Data + Finance score
at/above tier on the v2 grid (I94 P8); (2) a full 8-area sweep with operator sign-off; (3) an
operator-explicit FAIL-promotion decision (`D-IH-94-A` successor).

## 7.5 Articulation completeness (v3 — D-IH-95-D)

**v3 adds a second lens to "complete": not just *present* (the 16-component grid) but *wired*.**
Grounded in the 168-source HCAM research action and the Canonical Articulation Model
([`CANONICAL_ARTICULATION_MODEL.md`](../../Data/Architecture/canonicals/CANONICAL_ARTICULATION_MODEL.md)),
articulation completeness asks the operator's real question: *is every canonical this area owns
actually linked into the enterprise model, or is it an orphan?*

> An area is **articulation-complete** when every entity type it owns (per `ENTITY_CATALOG.csv`)
> participates in **≥1 active HCAM triple** (`CANONICAL_RELATIONSHIP_REGISTRY.csv`) — i.e. its
> roles are *assigned* to processes, its processes *realize* capabilities, it *serves* a contract.
> Orphans (present but no active triple) are surfaced for the Semantic Council to disposition.

- This **subsumes, not replaces** v2: AREA-15 placement-integrity already answers *belongs-here*
  (the right canonicals are in the area); articulation completeness adds *linked-here* (those
  canonicals are wired to the rest of the model). The 16-component × L0–L5 grid is unchanged.
- **Runnable (CQ5):** `py scripts/validate_canonical_articulation.py --articulation <Area>` —
  reports `wired/owned` + the orphan list. **Advisory** (the Semantic Council dispositions
  orphans via `SOP-DATA_SEMANTIC_COUNCIL_001.md`); it does **not** gate the v2 completion bar, so
  Data/Finance/People closures are preserved.
- **Ownership:** the articulation tier is **Data-federated** (HCAM is a Data-Architecture canonical,
  `D-IH-95-A`); People keeps the area-governance *methodology* (this discipline). The two are paired,
  not merged.

## 8. Cross-references

- HCAM articulation model (v3 tier): [`CANONICAL_ARTICULATION_MODEL.md`](../../Data/Architecture/canonicals/CANONICAL_ARTICULATION_MODEL.md) · Council SOP: [`SOP-DATA_SEMANTIC_COUNCIL_001.md`](../../Data/Governance/canonicals/SOP-DATA_SEMANTIC_COUNCIL_001.md)
- Articulation research (168 sources): [`canonical-articulation-model-2026-06-05/`](../../../../../wip/intelligence/canonical-articulation-model-2026-06-05/)
- Research grounding: [`area-completeness-doctrine-2026-06-05/`](../../../../../wip/intelligence/area-completeness-doctrine-2026-06-05/) (131 sources)
- Initiative: [`docs/wip/planning/94-area-architecture-and-completeness-v2/`](../../../../../wip/planning/94-area-architecture-and-completeness-v2/master-roadmap.md)
- Pydantic SSOT: [`akos/hlk_area_completeness.py`](../../../../../../akos/hlk_area_completeness.py) (v2 forward-charter)
- Runbook: [`scripts/validate_area_completeness.py`](../../../../../../scripts/validate_area_completeness.py) (v2 forward-charter)
- Pattern: `pattern_area_buildout` in `PEOPLE_DESIGN_PATTERN_REGISTRY.csv`
- SOP: [`SOP-PEOPLE_AREA_GOVERNANCE_001.md`](SOP-PEOPLE_AREA_GOVERNANCE_001.md)
- Methodology version: [`LOGIC_CHANGE_LOG.md`](LOGIC_CHANGE_LOG.md) BT-07 (v2 mint)
- v1 lineage: `D-IH-93-B` (I93 P0); v2: `D-IH-94-A` (I94)
