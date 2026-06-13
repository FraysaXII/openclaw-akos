---
intellectual_kind: research_crosswalk
parent_initiative: INIT-OPENCLAW_AKOS-97
phase: P6a
authored: 2026-06-13
language: en
---

# DCAM ↔ Holistika area completeness crosswalk (P6a)

> **Purpose:** Satisfy I97 P5 **Option D** prerequisite — enterprise **2-D maturity shape** (component × level)
> before Infonomics doctrine mint (P6b). Evidence: I94 **`D-IH-94-A`** already minted L0–L5 grid in
> [`AREA_GOVERNANCE_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md)
> + `akos/hlk_area_completeness.py`.

## DCAM v3 components → Holistika AREA components

| DCAM component (EDM Council) | Holistika AREA dimension | Infonomics hook (P6b) |
|:---|:---|:---|
| Strategy & business alignment | AREA-02 charter + AREA-14 kind/entity | Value stream + tier sets economic density |
| Program / project governance | AREA-04 process-list + AREA-09 paired SOP | Handoff cost in RevOps spine |
| Data architecture | AREA-08 dimension registries + AREA-15 placement | Contract inventory = asset register |
| Data quality | AREA-06 capability confidence + validators | Quality ROI vs verify TCO |
| Data governance | AREA-03 discipline + AREA-07 PRECEDENCE | CSV gate cost = mint economics |
| Data operations | AREA-10 mirrors + AREA-09 runbooks | Mirror emit carrying cost |
| Analytics / insights | AREA-12 Quality Fabric + BI surfaces | Insight-machine value (I96 consumes P6b) |
| Business data knowledge | AREA-15 shipped contract + semantic layer | Consumer registry = revenue attribution |

Full AREA component list: [`AREA_GOVERNANCE_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md) §2.

## Maturity level alignment

| DCAM / CMMI notion | Holistika L0–L5 | v1 verdict map |
|:---|:---|:---|
| Not present | L0 Absent | `gap` |
| Ad hoc | L1 Initial | weak `partial` |
| Managed | L2 Managed | `partial` |
| Defined / governed | **L3 Defined** | **`pass` — critical bar** |
| Measured | L4 Measured | outcome signal required for tier COMPLETE |
| Optimizing | L5 Optimizing | learning loop (AREA governance §6) |

## P6a verification snapshot (2026-06-13)

Command: `py scripts/validate_area_completeness.py --matrix`

| Signal | Result |
|:---|:---|
| 2-D grid live | **YES** — 16 components × L0–L5 |
| Deterministic heuristic | **YES** — repeatable matrix |
| Critical @ L3 | Data/Finance/Marketing/Operations/People **10/10** |
| Platform areas COMPLETE | Data **90%**, Finance **94%** |
| Org-wide all COMPLETE | **NO** — Legal/Research/Tech INCOMPLETE (expected; not P6a gate) |

**P6a gate:** Infonomics requires **model integrity**, not org-wide area closure. L0–L5 + critical-at-L3 on platform/stream areas satisfies Option D for P6b entry.

## Cross-references

- Research: `SRC-INF-EXT-004`, `SRC-INF-EXT-001` (Infonomics ledger)
- I94 roadmap: [`../../../planning/94-area-architecture-and-completeness-v2/master-roadmap.md`](../../../planning/94-area-architecture-and-completeness-v2/master-roadmap.md)
- P6b spec: [`implementation-spec-2026-06-13.md`](implementation-spec-2026-06-13.md)
