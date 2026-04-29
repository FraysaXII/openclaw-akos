# Program — `PRJ-HOL-KIR-2026` (People / Compliance chain)

**Owner role**: Compliance (CPO chain)  
**Program registry**: [`PROGRAM_REGISTRY.csv`](../../../../../../../compliance/dimensions/PROGRAM_REGISTRY.csv) → `PRJ-HOL-KIR-2026`.  
**Scope**: All Compliance casework specifically scoped to KiRBe (DPIA, privacy, regulated-data handling).

This folder is the **program-scoped landing point** for Compliance casework on Holistika's KiRBe SaaS platform. Created **2026-04-29** as a cascade of `operator-answers-wave2.yaml` Section 4 `kirbe_duality.has_paying_customers_today: true` per **D-IH-16** — when KiRBe has paying customers, Compliance is no longer on-demand; it is **required**. Until 2026-04-29 the founder-incorporation program (`PRJ-HOL-FOUNDING-2026`) was the only Compliance-scoped program; KiRBe joins as the second.

> **Process-list anchors** — Compliance Methodology workstream `hol_peopl_ws_1`; GOI/POI register maintenance `hol_peopl_dtp_303`; transcript redaction `hol_peopl_dtp_304`. These are cross-program; KiRBe-specific compliance casework adds new `process_list.csv` rows under `hol_peopl_*` as it surfaces (e.g. KiRBe DPIA, KiRBe data-subject access workflows, KiRBe regulator notifications).

## Casework scope (incoming)

- **DPIA / privacy impact assessment** for KiRBe ingestion sources and end-user data flows.
- **Data subject access requests (DSAR)** — KiRBe-specific runbook, joined to GOI/POI register entries for affected counterparties.
- **Regulator notifications** when KiRBe handles regulated data (financial, health, ENS).
- **Adviser engagement** when KiRBe-specific compliance questions surface — uses ADVOPS plane (Initiative 21) with `discipline_id=startup_certification` or new disciplines as needed.
- **Annual privacy review** with the Brand Manager (cross-program; D-IH-17 cadence).

## Cross-references

- Tech KiRBe folder: [`Admin/O5-1/Tech/System Owner/programs/PRJ-HOL-KIR-2026/`](../../../../Tech/System%20Owner/programs/PRJ-HOL-KIR-2026/README.md)
- Legal KiRBe folder (sister; created in the same cascade): [`Admin/O5-1/People/Legal/programs/PRJ-HOL-KIR-2026/`](../../Legal/programs/PRJ-HOL-KIR-2026/README.md)
- Data Governance KiRBe folder (DQ + lineage): [`Admin/O5-1/Data/Governance/programs/PRJ-HOL-KIR-2026/`](../../../../Data/Governance/programs/PRJ-HOL-KIR-2026/README.md)
- PMO KiRBe folder: [`Admin/O5-1/Operations/PMO/programs/PRJ-HOL-KIR-2026/`](../../../../Operations/PMO/programs/PRJ-HOL-KIR-2026/README.md)
- GOI/POI maintenance SOP: [`SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md`](../../SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md)
- Transcript redaction SOP: [`SOP-HLK_TRANSCRIPT_REDACTION_001.md`](../../SOP-HLK_TRANSCRIPT_REDACTION_001.md)
- Initiative 23 master roadmap: [`docs/wip/planning/23-hlk-program-registry-and-program-2/master-roadmap.md`](../../../../../../../../wip/planning/23-hlk-program-registry-and-program-2/master-roadmap.md)
- D-IH-16 (KiRBe duality + on-demand → required cascade): see Initiative 23 [`decision-log.md`](../../../../../../../../wip/planning/23-hlk-program-registry-and-program-2/decision-log.md).
