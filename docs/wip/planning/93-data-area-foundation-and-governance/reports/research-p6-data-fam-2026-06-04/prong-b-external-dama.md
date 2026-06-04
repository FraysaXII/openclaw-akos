---
intellectual_kind: research_prong_synthesis
parent_pack: research-p6-data-fam-2026-06-04
prong: B
authored: 2026-06-04
---

# Prong B — External DAMA / data-product framing

## Alignment

| External concept | Holistika P6 binding |
|:---|:---|
| DAMA data architecture (federated) | DATA sets standards; areas own domain products |
| Data mesh — domain data products | Seven DATA-FAM umbrellas = named products |
| Purview / ODCS data products | L3 projection via existing `export_data_contract_odcs.py` |
| DataOps monitoring | `dataops_quality_check.py --data-fam <FAMILY>` |

## What we are NOT doing in P6

- Full data mesh decentralization (no per-area autonomous infra teams)
- Snowflake/BigQuery warehouse selection (decided P5b — Postgres T2)
- Purview deployment (posture remains repo-native SSOT per P2b Option A)

## Recommended probe philosophy

**Family-level probes** answer: "Is this data product healthy?" not "Is every process row perfect?"

First live probe = **COMPLIANCE-MIRROR mirror parity** because:
- Mechanical (DDL + emit path exists for CHANNEL)
- Closes documented OPS-86-15 gap
- Unblocks wave-close DataOps credibility
