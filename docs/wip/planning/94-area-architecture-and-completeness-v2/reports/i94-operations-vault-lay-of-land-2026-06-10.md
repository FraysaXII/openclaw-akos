---
parent_initiative: INIT-OPENCLAW_AKOS-94
authored: 2026-06-10
intellectual_kind: vault_inventory
feeds_phase: P4
linked_decisions:
  - D-IH-94-A
---

# Operations vault lay of the land (2026-06-10)

Full inventory sweep of `Admin/O5-1/Operations/` after P0–P3 + Research OPS-86-26.
**Operational lens only:** what exists to **execute** delivery, not what sister areas govern.

## Live scores

| Metric | Value |
|:---|:---|
| Area completeness | **93%**, crit@L3 **10/10 COMPLETE** |
| AREA-09 pairing | **12/53** process_list rows with `sop_path`/`runbook_path` |
| AREA-12 Quality Fabric | **partial** (1 discipline cited; §6 cross-check incomplete) |
| `--next` worklist | **empty** (critical tier closed) |

## Sub-area map

| Sub-area | Vault assets (md/yaml/csv) | Role | Delivery tag | Automation posture |
|:---|:---:|:---|:---|:---|
| **PMO** | ~28 | COO / PMO | project + program | **Strong** — WIP/inbox/cohesion renders, mirror trigger, area sweep |
| **RevOps** | ~12 | RevOps Manager | project (engagement spine) | **Medium** — scaffold, QBR, FINOPS bridge SOPs; CRM sync forward |
| **SMO** | ~3 | Service Manager | service | **Weak** — catalog + SLA canonical; `.gitkeep` only in folder root |
| **Engagement** | ~5 | PMO + RevOps | project (client) | **Medium** — discovery/design/proposal/estimation SOPs |
| **Root / canonicals** | ~4 | COO | cross-cutting | **Strong** — charter, delivery doctrine, process catalog YAML |

**Removed:** `IntelligenceOps/` (I94 P3 eviction → Research).

**Placement debt:** `PMO/canonicals/business-strategy/` (11 strategy canonicals) — register
only until I95 L6 inline-ratify.

## Executable catalog (T1 — 12 paired)

From `OPERATIONS_PROCESS_CATALOG.yaml` — all `lifecycle_status: active`:

| # | Process | Cadence | Runbook |
|:---:|:---|:---|:---|
| 1 | WIP dashboard render | Mon 07:00 | `render_wip_dashboard.py` |
| 2 | Operator inbox render | Daily 07:00 | `render_operator_inbox.py` |
| 3 | Cohesion index render | Quarterly | `render_operational_cohesion_index.py` |
| 4 | Initiative program anchors | event | `pmo_program_anchor_backfill.py` |
| 5 | External adviser router | on_demand | `export_adviser_handoff.py` |
| 6 | Engagement scaffold | event | `scaffold_engagement.py` |
| 7 | Mirror emit trigger | gated | `verify.py compliance_mirror_emit` |
| 8 | Area completeness sweep | event | `validate_area_completeness.py` |
| 9 | Initiative harmonisation | event | `validate_initiative_registry.py` |
| 10 | Vault promotion gate | gated | `validate_hlk.py` |
| 11 | RevOps QBR | quarterly | engagement template validators |
| 12 | Service catalog maintenance | weekly Mon | `validate_hlk.py` |

## process_list gap (AREA-09 cliff)

- **83** Operations-area rows in `process_list.csv`
- **12** paired (P3 tranche)
- **71** without vault `sop_path` pairing (includes legacy GTM rows, duplicate PMO dtp rows, RevOps TBI rows)

Priority unpaired clusters for T2 tranche:

1. Remaining PMO maintenance (`hol_opera_dtp_*`, initiative governance)
2. RevOps engagement lifecycle (`tbi_ops_dtp_revops_*`)
3. Engagement client delivery (`hol_ops_eng_*` / Think Big paths)
4. SMO service operations (currently 1 row `gtm_ws_service_catalog`)

## Cross-area touchpoints (execution triggers only)

| Sister area | Operations trigger | Canonical handoff target |
|:---|:---|:---|
| **Data** | Post-CSV tranche mirror emit | `SOP-OPS_MIRROR_EMIT_TRIGGER_001` → DataOps quality |
| **People/Compliance** | Vault promotion, process_list tranche | CSV gates + `SOP-META` |
| **Finance** | Engagement signed / QBR | `SOP-FINOPS_BRIDGE_001`, counterparty register |
| **Tech** | Pre-consumer-repo session | CICD baseline + fleet hygiene sweep |
| **Research** | Intelligence collection (evicted) | Research/Intelligence SOPs — not Operations |

## Gaps vs Data-area bar (I93 reference)

| Dimension | Data (I93 closed) | Operations (now) |
|:---|:---|:---|
| crit@L3 | 10/10 | 10/10 ✓ |
| Overall score | ~90% | 93% ✓ |
| Executable pairing depth | High (DataOps probes) | **12/53** — primary debt |
| Cross-area map | `cross-area-data-map` | **Missing** → P4 mint |
| Closure UAT | Signed | **Not minted** → P6 |

## Research backing (P4 wave)

- Source ledger: [`i94-operations-area-source-ledger-p4-wave-2026-06-10.csv`](i94-operations-area-source-ledger-p4-wave-2026-06-10.csv) — **308 internal + 120 external** (428 total); `validate_research_action.py` PASS.
