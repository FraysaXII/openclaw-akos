---
initiative_id: INIT-OPENCLAW_AKOS-94
phase: P2
intellectual_kind: forward_map
authored: 2026-06-05
status: active
language: en
---

# I94 P2 — v2 area-buildout forward map (any-seat)

> Operator P2 intent: *"improve all of their plans before starting … so this doesn't get lost
> when we go for those other initiatives and so that any seat can do it — do the heavy lifting
> now."* This is the **single any-seat forward map** every remaining phase + the 5-area sweep
> (option D) inherits. The **live SSOT** is the scorer itself
> (`py scripts/validate_area_completeness.py --matrix` / `--area <X> --next`); this map snapshots
> it + assigns each area its phase + acceptance bar so no seat re-derives the work.

## How any seat runs an area to done (the loop)

1. `py scripts/validate_area_completeness.py --area <Area> --next` → ranked worklist.
2. Work it **top-down** (critical-first); use `_templates/` for AREA-02/13; `git mv` drift for AREA-15.
3. Re-run until `--matrix` shows the area's **tier = COMPLETE** (`crit@L3` = N/N).
4. Enhancing items (AREA-09/10/11/13/16) → inline-ratify defer-OPS / accept-as-canon.

**Acceptance bar (all areas):** tier **COMPLETE** (all critical components L3+). The `%` is a
maturity badge, not the gate.

## Per-area snapshot (2026-06-05 v2 matrix) + phase assignment

| Area | kind | entity | owner | crit@L3 | tier | critical gaps | I94 phase |
|:---|:---|:---|:---|:---:|:---|:---|:---|
| **Data** | platform | HLK Tech Lab | CDO | 10/10 | **COMPLETE** | — (AREA-16 enh) | P8 regression (re-confirm on v2) |
| **Finance** | stream_aligned | Think Big | CFO | 10/10 | **COMPLETE** | — (AREA-16 enh) | P8 + then I88 F4 closure |
| **Marketing** | stream_aligned | Think Big | CMO | 10/10 | **COMPLETE** | — (README/rule+skill/AREA-16 enh) | sweep (receives MKTOPS+UX from P4) |
| **Operations** | delivery_capacity | Think Big | COO | 9/10 | INCOMPLETE | 1 critical (PMBOK-domain reframe) | **P3** (PMBOK reframe + evict IntelligenceOps) |
| **Tech** | platform | HLK Tech Lab | CTO | 8/10 | INCOMPLETE | charter + discipline (receives TECHOPS from P4) | **P5** (entity/Envoy research-first) |
| **People** | capability_meta | Holistika | CPO | 8/10 | INCOMPLETE | **AREA-15 drift (4 disciplines out)** + charter | **P4** (Compliance methodology + drift moves) |
| **Research** | stream_aligned | Holistika | Holistik Researcher | 7/10 | INCOMPLETE | charter + discipline + dimensions | sweep (after I75 lineage) |
| **Legal** | stream_aligned | Think Big | Legal Counsel | 6/10 | INCOMPLETE | charter + discipline + dimensions + README | **P6** (Legal research-first / LegalOps) |

## Sweep order (readiness-ranked; option D after P1–P7 land)

1. **Marketing** — already COMPLETE for tier; just absorb MKTOPS+UX (P4) + close enhancing (README/rule).
2. **Operations** — P3 PMBOK reframe closes the 1 critical gap.
3. **People** — P4 drift moves (AREA-15) + Compliance methodology consolidation + charter.
4. **Tech** — P5 entity/Envoy rework + charter/discipline.
5. **Research** — charter + discipline (coordinate with I75 Research-area governance).
6. **Legal** — P6 research-first LegalOps design (most build; operator big-help area).

## v2 acceptance criteria each future area initiative inherits

- Declare **kind + entity** (AREA-14) in `AREA_KIND_ENTITY` before the buildout.
- Reach **all critical components L3** (charter / discipline / process / roles / capability /
  precedence / dimensions / kind-entity / placement-integrity).
- Ship **≥1 contract** (AREA-15) — the area is a product, not a folder.
- **Sub-folder = role/sub_area** (AREA-16) — RACI; functional-sub-area tolerance lands at P7 (W-4).
- Show **≥1 measured outcome (L4)** for tier maturity.
- Use the **templates** + the **`--next` worklist**; file the area score row at close.

## Cross-references

- Scorer (live SSOT): `scripts/validate_area_completeness.py`
- Doctrine: [`AREA_GOVERNANCE_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md) v2
- SOP: [`SOP-PEOPLE_AREA_GOVERNANCE_001.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_AREA_GOVERNANCE_001.md) v2
- I93 gap tracker (v1 superseded by this map): [`area-governance-gap-tracker-2026-06-05.csv`](../../93-data-area-foundation-and-governance/_trackers/area-governance-gap-tracker-2026-06-05.csv)
- Master roadmap: [`master-roadmap.md`](../master-roadmap.md)
