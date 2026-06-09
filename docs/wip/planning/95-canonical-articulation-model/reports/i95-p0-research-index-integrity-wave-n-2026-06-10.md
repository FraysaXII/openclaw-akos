---
authored: 2026-06-10
tranche: I95-T2
parent_initiative: INIT-OPENCLAW_AKOS-95
wave: N
decision_ids:
  - D-IH-86-CD
  - D-IH-86-CF
---

# P0 research — INDEX_INTEGRITY Wave N (I95 Tranche 2)

Planner-quality evidence packet before index backfill edits.

## Internal evidence sweep

| Source | Finding | Tranche implication |
|:---|:---|:---|
| [`INDEX_INTEGRITY_DISCIPLINE.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/INDEX_INTEGRITY_DISCIPLINE.md) | 8-dimension probe set IDX-01..08; specialty mint complete (Wave N P3) | Tranche = N.4 backfill, not re-mint |
| [`akos/hlk_index_integrity.py`](../../../../akos/hlk_index_integrity.py) + [`scripts/baseline_index_sweep.py`](../../../../scripts/baseline_index_sweep.py) | Mechanical layer shipped; sweep at `wave_close` | Run sweep first; fix deterministic paths |
| Pre-edit sweep (`index-sweep-2026-06-10-tranche2-wave-n.md`) | fresh=3, drift=1 (IDX-04), gap=3 (IDX-02/06/08), skip=1 (IDX-03) | Target: clear IDX-04 + gaps; IDX-03 skip OK (no Wave marker in recent commits) |
| [`INITIATIVE_REGISTRY.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv) | I78/I85/I87 **closed**; I90–I95 **active** (I93 closed) | README §70–87 table + §Closing list drift |
| [`INITIATIVE_DEPENDENCIES.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_DEPENDENCIES.md) | `last_generated: 2026-05-29`; no I90–I95 section | Primary Tranche 2 deliverable |
| [`i95-initiative-cluster-map.md`](../i95-initiative-cluster-map.md) | Interim SSOT for I86–I95 edges | Promote edges into INITIATIVE_DEPENDENCIES |
| [`HOLISTIKA_QUALITY_FABRIC.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md) §6 | Missing `INTENT_RANKED_REGRESSION_DISCIPLINE.md` (IDX-08) | Append §6 row + frontmatter link |
| [`PRECEDENCE.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md) | Missing BUILDOUT_BACKLOG + CANONICAL_GOVERNANCE_REGISTRY (IDX-02) | Append canonical rows (I95 L2 + P95-GOV-1 lineage) |
| [`docs/ARCHITECTURE.md`](../../../../ARCHITECTURE.md) HLK Dimension Registries | Missing BUILDOUT_BACKLOG (IDX-06) | Append to dimension list |
| Tranche 1 (`1f509f2`) | L3 tranche-5 DONE — out of scope | Do not redo |

## Novelty test (applied-research RULE 2)

INDEX_INTEGRITY specialty is **refinement** of Wave M INTER_WAVE_REGRESSION mint pattern (D-IH-86-CD). No novel framing in this tranche — **external citation optional**.

## External research (light touch — refinement only)

- **Keep a Changelog** (keepachangelog.com) — `[Unreleased]` working-line discipline already codified in repo CHANGELOG policy; supports IDX-03 hygiene without new doctrine.
- **World Quality Report 2024** (cited in planning-traceability UAT bar) — structured index freshness reduces post-release defect rate; operationalises why IDX sweeps gate wave-close.

## Disposition plan (5-option enum preview)

| Finding | Recommended disposition | Rationale |
|:---|:---|:---|
| IDX-04 INITIATIVE_DEPENDENCIES stale | **deterministic-fix-now** | Cluster map provides edge SSOT; prose refresh is mechanical |
| IDX-01/07 README I78 active | **deterministic-fix-now** | Registry says closed |
| IDX-02 PRECEDENCE 2 CSVs | **deterministic-fix-now** | Row templates exist; I95/P95-GOV lineage known |
| IDX-06 ARCHITECTURE BUILDOUT_BACKLOG | **deterministic-fix-now** | Single CSV append to list |
| IDX-08 QF §6 INTENT_RANKED | **deterministic-fix-now** | Canonical exists at active; compose pattern mirrors INTER_WAVE_REGRESSION |
| IDX-03 CHANGELOG Wave marker | **defer-OPS** | No Wave-X in recent commit messages; skip probe correct |

## Tranche 2 scope boundary

**In:** README + INITIATIVE_DEPENDENCIES + PRECEDENCE/ARCHITECTURE/QF gap fixes + sweep report + cluster map/PMO/files-modified updates.

**Out:** N.5 60-finding triage, N.6 mega-ratify, WIP_DASHBOARD re-render, process_list mint, INITIATIVE_REGISTRY edits.
