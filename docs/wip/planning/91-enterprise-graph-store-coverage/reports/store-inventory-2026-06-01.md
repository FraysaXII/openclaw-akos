---
intellectual_kind: phase_report
sharing_label: internal_only
initiative_id: INIT-OPENCLAW_AKOS-91
authored: 2026-06-01
language: en
linked_decisions:
  - D-IH-91-A
phase: P0
---

# I91 P0 — Enterprise store inventory (skeleton)

> **Purpose:** Name the stores I91 will map in the coverage matrix (P2). **Not** a full coverage verdict yet — only inventory + primary SSOT path.

## Store classes

| Store class | SSOT / entry path | Typical consumers | I07 / I91 touch |
|:---|:---|:---|:---|
| Git canonical CSVs | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/` (+ `dimensions/`) | `validate_hlk.py`, mirrors, ERP panels | Graph projection via sync |
| Supabase `compliance.*_mirror` | Migrations + `scripts/sync_compliance_mirrors_from_csv.py` | ERP, ops dashboards, FDW joins | P1 mirror emit parity |
| Neo4j graph | `scripts/sync_hlk_neo4j.py` | Explorer, `hlk_graph_mcp_server.py` | **P1 blocked** until `NEO4J_*` |
| Vault markdown | `docs/references/hlk/v3.0/` tree | Operators, KM, render pipelines | `validate_hlk_vault_links.py` |
| Planning WIP | `docs/wip/planning/<NN-slug>/` | Initiatives, UAT, cluster coordinator | Index only (not graph SSOT) |
| Sibling repos | `REPOSITORY_REGISTRY.csv` → `hlk-erp`, `kirbe-platform`, `boilerplate` | Deployed surfaces, blessed mirrors | Drift gate (`check_external_repo_contract.py`) |
| Intelligence WIP | `docs/wip/intelligence/` | Research actions, radar | Out of graph SSOT; cross-ref only |

## Enterprise surfaces (coverage matrix rows — TBD in P2)

| Surface ID | Description | Stores to verify in P2 |
|:---|:---|:---|
| S-OPS | Operator dashboards / ERP operator plane | Mirrors + ERP routes + graph |
| S-GOV | Compliance registers (process, role, decision, initiative) | Canonical CSV + mirror + graph |
| S-KM | Topic / program / manifest Output-1 | `TOPIC_REGISTRY` + `_assets/` + graph |
| S-EXT | External render (deck, dossier, PDF) | Vault assets + render trail validators |
| S-SIB | Sibling-repo runtime | `REPOSITORY_REGISTRY` + health snapshot |

## Verification (P0)

```powershell
py scripts/validate_hlk.py
py scripts/validate_hlk_vault_links.py
```

## Next

- P1: [`p1-neo4j-preflight-blocked-2026-06-01.md`](p1-neo4j-preflight-blocked-2026-06-01.md)
- P2: `store-coverage-matrix-2026-06-01.md` (fills S-* rows with PASS / partial / gap)
