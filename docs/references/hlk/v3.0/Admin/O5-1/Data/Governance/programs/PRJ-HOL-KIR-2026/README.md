# Program — `PRJ-HOL-KIR-2026` (Data / Governance chain)

**Owner role**: Data Governance Lead (CDO chain)  
**Program registry**: [`PROGRAM_REGISTRY.csv`](../../../../../../../compliance/dimensions/PROGRAM_REGISTRY.csv) → `PRJ-HOL-KIR-2026`.  
**Scope**: All Data-Governance-chain casework specifically scoped to KiRBe ingestion data quality, lineage, and masterdata.

This folder is the **program-scoped landing point** for Data Governance casework on KiRBe's ingestion plane. KiRBe is BOTH a SaaS product AND a vault KM ingestion source per `v3.0/index.md` ("Ingest as a source") — Data Governance owns the ingestion DQ and lineage discipline that makes that ingestion trustworthy.

> **Process-list anchors** — `thi_data_dtp_274 KiRBe Ingestion Data Quality Monitoring` (Data Governance Lead + Data Steward) and `thi_data_dtp_275 Formal Data Lineage` (CDO chain). Both are required for KiRBe to be a reliable KM source.

## Casework scope (incoming)

- KiRBe ingestion DQ rule definitions and monitoring dashboards.
- Lineage capture from KiRBe input sources → intermediate parsers/embeddings → vector store → answer surfaces.
- Drift detection and operator alerting when DQ falls below thresholds.

## Cross-references

- Tech KiRBe folder: [`Admin/O5-1/Tech/System Owner/programs/PRJ-HOL-KIR-2026/`](../../../../Tech/System%20Owner/programs/PRJ-HOL-KIR-2026/README.md)
- Data Architecture KiRBe folder (graph navigation): [`Admin/O5-1/Data/Architecture/programs/PRJ-HOL-KIR-2026/`](../../Architecture/programs/PRJ-HOL-KIR-2026/README.md)
- Initiative 23 master roadmap: [`docs/wip/planning/23-hlk-program-registry-and-program-2/master-roadmap.md`](../../../../../../../../wip/planning/23-hlk-program-registry-and-program-2/master-roadmap.md)
