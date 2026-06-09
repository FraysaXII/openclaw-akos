---
authored: 2026-06-10
tranche: I95-T3
parent_initiative: INIT-OPENCLAW_AKOS-95
linked_initiative: INIT-OPENCLAW_AKOS-91
decision_ids:
  - D-IH-91-A
  - D-IH-95-L
---

# P0 research — I91 store-coverage matrix v1 (I95 Tranche 3)

Planner-quality evidence packet before I91 P1–P2 execution.

## Internal evidence sweep

| Source | Finding | Tranche implication |
|:---|:---|:---|
| [`91-enterprise-graph-store-coverage/master-roadmap.md`](../../91-enterprise-graph-store-coverage/master-roadmap.md) | P1 blocked on `NEO4J_*` at 2026-06-01; P2 matrix under `reports/store-coverage-matrix-<date>.md` | Unblock P1 using I95 F6 harness; mint matrix v1 today |
| [`store-inventory-2026-06-01.md`](../../91-enterprise-graph-store-coverage/reports/store-inventory-2026-06-01.md) | Seven store classes + five enterprise surfaces (S-OPS..S-SIB) | Matrix rows/columns inherit P0 skeleton — no schema fork |
| [`p1-neo4j-preflight-blocked-2026-06-01.md`](../../91-enterprise-graph-store-coverage/reports/p1-neo4j-preflight-blocked-2026-06-01.md) | BLOCKED-ENV superseded by I95 F6 | Mint new PASS report; do not delete blocker (audit trail) |
| [`i95-neo4j-cq-uat-2026-06-09.md`](i95-neo4j-cq-uat-2026-06-09.md) | Instance `6c0d76bf`; dual-emit + CQ PASS | Probe username = instance id (post-restore Free tier) |
| [`i91-i93-cross-initiative-regression-2026-06-04.md`](../../93-data-area-foundation-and-governance/reports/i91-i93-cross-initiative-regression-2026-06-04.md) | I93 owns DATA-FAM CAP rows; I91 owns matrix v1 | Matrix cites I93 cross-area map; no CAP re-mint |
| [`cross-area-data-map-2026-06-04.md`](../../93-data-area-foundation-and-governance/reports/cross-area-data-map-2026-06-04.md) | 7 DATA-FAM families + probe profiles | Optional matrix appendix row per family (consume-only) |
| [`akos/hlk_neo4j.py`](../../../../akos/hlk_neo4j.py) | Dry-run parity via `assert_graph_registry_parity`; live sync via `sync_csv_graph` | P1 smoke = probe + `--dry-run` (no write required for v1) |
| [`i95-initiative-cluster-map.md`](../i95-initiative-cluster-map.md) | Burndown rank 2 = I91 P1–P2 | Promote to DONE after matrix + probe evidence |
| Tranche 2 (`cfb8b18`) | INDEX_INTEGRITY Wave N DONE | Out of scope |

## Novelty test (applied-research RULE 2)

Store-coverage matrix v1 is a **refinement** of I91 P0 inventory + I93 cross-area map precedent. No novel doctrine framing — **external citation optional**.

## External research (light touch — store federation precedent)

- **Neo4j Graph Data Science / Aura ops docs** — graph store as read projection over git SSOT aligns with federated metadata pattern (CSV authoritative; Neo4j derived). Supports S-GOV/S-KM graph rows without claiming Neo4j is SSOT.
- **DAMA-DMBOK 2.0 Data Architecture** — multi-store coverage map is standard metadata inventory practice; I93 DATA-FAM families already encode producer/consumer roles.

## Disposition plan

| Decision point | Outcome | Rationale |
|:---|:---|:---|
| P1 live sync vs dry-run only | **dry-run + probe** (recommended) | Roadmap P1 gate satisfied; live sync is P3 regression scope |
| Matrix location | **I91 `reports/`** | I91 charter §5 closure criteria; I95 cites via cluster map |
| Canonical CSV promotion | **defer** | v1 report-class; promotion needs operator CSV gate |
| AskQuestion fork | **none** | Evidence pre-digested; F6 cleared blocker |

## Tranche 3 scope boundary

**In:** Probe PASS evidence, sync dry-run, matrix v1, I91 roadmap update, cluster map rank 2 DONE, PMO/files-modified/CHANGELOG.

**Out:** I91 P3 graph explorer regression, I92 ERP handoff, canonical CSV mint, live `sync_hlk_neo4j.py` write (unless operator requests).
