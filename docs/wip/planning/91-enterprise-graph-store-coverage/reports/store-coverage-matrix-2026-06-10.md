---
intellectual_kind: coverage_matrix
sharing_label: internal_only
initiative_id: INIT-OPENCLAW_AKOS-91
version: v1
authored: 2026-06-10
language: en
linked_decisions:
  - D-IH-91-A
  - D-IH-95-L
linked_initiatives:
  - INIT-OPENCLAW_AKOS-93
  - INIT-OPENCLAW_AKOS-95
phase: P2
status: active
---

# I91 store-coverage matrix v1 (2026-06-10)

Operator-maintainable map of **which Holistika stores cover which enterprise surfaces**. SSOT for I91 P2; consumed by I92 ERP reassess and I93 P3 data-architecture canonical (consume-only — no DATA-FAM CAP re-mint per [`i91-i93-cross-initiative-regression-2026-06-04.md`](../../93-data-area-foundation-and-governance/reports/i91-i93-cross-initiative-regression-2026-06-04.md)).

**Predecessor:** [`store-inventory-2026-06-01.md`](store-inventory-2026-06-01.md) (P0 skeleton). **P1 gate:** [`p1-neo4j-preflight-pass-2026-06-10.md`](p1-neo4j-preflight-pass-2026-06-10.md).

## Coverage legend

| Code | Meaning |
|:---|:---|
| **PASS** | Store actively covers surface; validators or probe green |
| **PARTIAL** | Store exists; known gap or operator follow-up |
| **GAP** | Surface needs store; not wired |
| **N/A** | Surface out of scope for that store class |
| **INDEX** | Planning/index only — not graph SSOT |

## Store classes (columns)

| Store ID | SSOT path | Class |
|:---|:---|:---|
| **ST-GIT** | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/` (+ `dimensions/`, plane subdirs) | Git canonical CSV |
| **ST-MIR** | `compliance.*_mirror` via `scripts/sync_compliance_mirrors_from_csv.py` | Supabase mirror |
| **ST-GRAPH** | Neo4j via `scripts/sync_hlk_neo4j.py` (instance `6c0d76bf`) | Graph projection |
| **ST-VAULT** | `docs/references/hlk/v3.0/` markdown tree | Vault markdown |
| **ST-PLAN** | `docs/wip/planning/<NN-slug>/` | Planning WIP |
| **ST-SIB** | `REPOSITORY_REGISTRY.csv` → consumer repos | Sibling repos |
| **ST-INTEL** | `docs/wip/intelligence/` | Intelligence WIP |

## Surface × store matrix (v1)

| Surface | Description | ST-GIT | ST-MIR | ST-GRAPH | ST-VAULT | ST-PLAN | ST-SIB | ST-INTEL |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **S-OPS** | Operator dashboards / ERP operator plane | PASS | PARTIAL | PARTIAL | PASS | INDEX | PARTIAL | INDEX |
| **S-GOV** | Compliance registers (process, role, decision, initiative) | PASS | PASS | PASS | PASS | INDEX | N/A | N/A |
| **S-KM** | Topic / program / manifest Output-1 | PASS | PARTIAL | PASS | PASS | N/A | N/A | PARTIAL |
| **S-EXT** | External render (deck, dossier, PDF) | PARTIAL | N/A | N/A | PASS | N/A | PARTIAL | N/A |
| **S-SIB** | Sibling-repo runtime + deploy health | PARTIAL | N/A | N/A | PASS | N/A | PARTIAL | N/A |

### Row notes (plain language)

- **S-OPS / ST-MIR PARTIAL** — prod mirrors applied (GOV wave); **OPS-95-2** engagement_model_id backfill still open on 7 engagements.
- **S-OPS / ST-GRAPH PARTIAL** — probe + dry-run PASS; live dual-emit exercised at I95 F6; ERP panel joins not yet wired (I92 scope).
- **S-KM / ST-MIR PARTIAL** — `TOPIC_REGISTRY` + KM manifests in git; not all topic rows mirrored to Postgres.
- **S-EXT / ST-GIT PARTIAL** — render trail validators cover subset; full channel registry coupling is Quality Fabric scope.
- **S-SIB** — `REPOSITORY_REGISTRY` PASS in git; deploy-class verification per-repo is I68 discipline (PARTIAL fleet-wide).

## DATA-FAM family appendix (I93 consume-only)

Seven umbrella families from [`cross-area-data-map-2026-06-04.md`](../../93-data-area-foundation-and-governance/reports/cross-area-data-map-2026-06-04.md). I91 **does not** own CAP row mint — maps which stores each family touches.

| DATA-FAM family | Primary stores | Coverage v1 |
|:---|:---|:---:|
| DATA-FAM-COMPLIANCE-MIRROR | ST-GIT + ST-MIR | PASS |
| DATA-FAM-CANONICAL-CSV | ST-GIT + ST-VAULT | PASS |
| DATA-FAM-ENGAGEMENT-FACT | ST-GIT + ST-MIR + ST-PLAN | PARTIAL |
| DATA-FAM-TELEMETRY-OBS | ST-SIB + ST-GIT (`COMPONENT_SERVICE_MATRIX`) | PARTIAL |
| DATA-FAM-GTM-CRM | ST-MIR (`holistika_ops`) + ST-GIT | PARTIAL |
| DATA-FAM-KM-TOPIC | ST-GIT + ST-VAULT + ST-GRAPH | PASS |
| DATA-FAM-AIC-RUNTIME | ST-GIT + ST-SIB + config SSOT | PARTIAL |

## Verification commands (reproducible)

```powershell
py scripts/neo4j_connectivity_probe.py
py scripts/sync_hlk_neo4j.py --dry-run
py scripts/validate_hlk.py
py scripts/validate_hlk_vault_links.py
py scripts/verify.py pre_commit_fast
```

| Command | 2026-06-10 | Notes |
|:---|:---:|:---|
| `neo4j_connectivity_probe.py` | PASS (exit 0) | Instance `6c0d76bf` |
| `sync_hlk_neo4j.py --dry-run` | PASS (exit 0) | Parity only |
| `validate_hlk.py` | *(run at commit)* | Umbrella |
| `validate_hlk_vault_links.py` | *(run at commit)* | Vault cross-links |

## Forward work (not v1)

| Item | Owner | Trigger |
|:---|:---|:---|
| I91 P3 graph explorer / MCP regression | I91 | Matrix v1 + I07 baseline compare |
| I92 ERP panel data-source joins | I92 | Cites matrix rows for S-OPS |
| Canonical CSV promotion | Operator gate | If matrix graduates from report → `techops/` or `dimensions/` |
| Live sync cadence | Operator | Scheduled dual-emit post P3 |

## Cross-references

- I91 roadmap: [`../master-roadmap.md`](../master-roadmap.md)
- I95 cluster map: [`../../95-canonical-articulation-model/i95-initiative-cluster-map.md`](../../95-canonical-articulation-model/i95-initiative-cluster-map.md)
- Component inventory: [`techops/COMPONENT_SERVICE_MATRIX.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/techops/COMPONENT_SERVICE_MATRIX.csv)
