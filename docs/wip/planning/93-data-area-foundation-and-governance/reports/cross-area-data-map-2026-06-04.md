---
audience: J-OP
last_review: 2026-06-04
linked_decisions:
  - D-IH-93-F
  - D-IH-90-AA
status: research-synthesis
parent_initiative: INIT-OPENCLAW_AKOS-93
feeds_phase: P6
---

# Cross-area DATA-FAM producer/consumer map (2026-06-04)

Governance audit for I93 P6 (seven DATA-FAM umbrella capabilities + cross-area process
engineering). Heuristic classification of **115** explicit data producer/consumer processes
from ~442 executable `process_list` rows; **35** remain unmapped for area-batch assignment.

**Role codes:** `P` = produce · `C` = consume · `PC` = both

## Summary counts by family and area

| DATA-FAM family | Total | Tech | Ops | Finance | People | Research | MKT | Legal |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| DATA-FAM-COMPLIANCE-MIRROR | 12 | 1 | 2 | 3 | 4 | 1 | 0 | 1 |
| DATA-FAM-CANONICAL-CSV | 44 | 4 | 19 | 0 | 3 | 1 | 4 | 0 |
| DATA-FAM-ENGAGEMENT-FACT | 18 | 0 | 7 | 0 | 9 | 1 | 4 | 0 |
| DATA-FAM-TELEMETRY-OBS | 8 | 5 | 0 | 0 | 0 | 1 | 0 | 0 |
| DATA-FAM-GTM-CRM | 5 | 0 | 0 | 2 | 0 | 1 | 2 | 0 |
| DATA-FAM-KM-TOPIC | 7 | 6 | 0 | 0 | 1 | 0 | 0 | 0 |
| DATA-FAM-AIC-RUNTIME | 5 | 3 | 1 | 0 | 1 | 0 | 0 | 0 |
| **UNMAPPED** | 35 | 6 | 5 | 1 | 7 | 9 | 11 | 3 |

## Load-bearing processes (mint anchors)

| item_id | Family | Role | Notes |
|:---|:---|:---|:---|
| `env_tech_dtp_dataops_quality_001` | COMPLIANCE-MIRROR | P | DataOps umbrella; probe sweep entry point |
| `hol_peopl_dtp_index_integrity_001` | CANONICAL-CSV | PC | Baseline index integrity sweep |
| `hol_peopl_dtp_inter_wave_regression_001` | CANONICAL-CSV | PC | Inter-wave regression sweep |
| `thi_finan_dtp_303` / `hol_peopl_dtp_303` / `thi_legal_dtp_304` | COMPLIANCE-MIRROR | P | Register maintenance trio |
| `tbi_ops_dtp_revops_crm_sync_001` | ENGAGEMENT-FACT | PC | RevOps CRM adapter sync |
| `env_tech_dtp_techops_reliability_001` | TELEMETRY-OBS | P | TechOps reliability cadence |
| `env_tech_dtp_268` / `env_tech_dtp_269` | KM-TOPIC | PC/P | Neo4j GraphRAG + agent context |

## Formal `area=Data` processes (6 executable)

| item_id | item_name | Suggested DATA-FAM |
|:---|:---|:---|
| `thi_data_dtp_32` | Enterprise MasterData | CANONICAL-CSV + ENGAGEMENT-FACT |
| `thi_data_dtp_274` | KiRBe Ingestion Data Quality Monitoring | TELEMETRY-OBS + COMPLIANCE-MIRROR |
| `thi_data_dtp_275` | Formal Data Lineage | KM-TOPIC + COMPLIANCE-MIRROR |
| `SOP-ETL_MACROECON_INGESTION_001` | Macroeconomic ETL Ingestion | COMPLIANCE-MIRROR |
| `thi_data_dtp_77` | Data Modeling | CANONICAL-CSV |
| `thi_data_dtp_34` | RPA | ENGAGEMENT-FACT |

## OPS-86-15 mirror gap (Supabase DDL)

| CSV | Mirror DDL in repo? | Emit in sync script? | Pydantic SSOT |
|:---|:---:|:---:|:---:|
| `AIC_REGISTRY.csv` | No | No | Yes |
| `AUDIENCE_REGISTRY.csv` | No (doc ahead of code) | No | Yes |
| `CAPABILITY_REGISTRY.csv` | No | No | Yes |
| `CAPABILITY_CONFIDENCE_REGISTRY.csv` | No | No | Yes |
| `COUNTRY_WORK_CALENDAR.csv` | **Yes** (I93 P6) | **Yes** | No (OPS-86-18; CSV-only emit) |
| `CHANNEL_TOUCHPOINT_REGISTRY.csv` | **Yes** | **Yes** | Yes |

**Status (2026-06-04 P6):** OPS-86-15 five-CSV gap **closed in repo** via migration
`20260604120000_i93_p6_ops8615_mirror_gap_closure.sql` + `sync_compliance_mirrors_from_csv.py
--ops8615-gap-mirrors-only`. Operator still applies DDL to Supabase + runs emit SQL.

## DATA-FAM → DataOps probe profiles (P6 extension)

| DATA-FAM | Probe cluster |
|:---|:---|
| COMPLIANCE-MIRROR | DATA-01, DATA-02, DATA-03 |
| CANONICAL-CSV | DATA-01, DATA-05, DATA-07 + `validate_hlk.py` |
| ENGAGEMENT-FACT | DATA-01, DATA-07 + engagement validators |
| TELEMETRY-OBS | DATA-04, DATA-07 + techops/eval harness |
| GTM-CRM | DATA-03, DATA-04 + FINOPS/GTM SOPs |
| KM-TOPIC | DATA-06 + `validate_hlk_km_manifests.py` |
| AIC-RUNTIME | DATA-06, DATA-07 + MADEIRA persistence checks |

**Implementation:** add `DATA_FAM_PROBE_PROFILES` + `--data-fam` flag to
`scripts/dataops_quality_check.py`; first live probe = mirror parity (OPS-86-15 closure).

## P6 mint checklist

1. Operator-approved CSV tranche: `process_list` → `CAPABILITY_REGISTRY` → `CAPABILITY_CONFIDENCE_REGISTRY`.
2. Seven umbrella rows: `CAP-HOL-DATA-FAM-*-001` + matching `CONF-*` seeds + `hol_data_dtp_datafam_*` process rows.
3. Coordinate with I91 store-coverage scope — I93 owns family CAP rows; I91 owns graph projection.
4. Area batches for 35 unmapped: Tech → Ops → Research → People → MKT → Finance → Legal.

## Cross-refs

- I90 synthesis: `docs/wip/planning/90-routing-and-wiring/reports/data-area-capability-coverage-2026-06-04.md`
- I93 roadmap P6: `docs/wip/planning/93-data-area-foundation-and-governance/master-roadmap.md`
- Schemas: `akos/hlk_capability_registry_csv.py`, `akos/hlk_capability_confidence_csv.py`, `akos/hlk_process_csv.py`
