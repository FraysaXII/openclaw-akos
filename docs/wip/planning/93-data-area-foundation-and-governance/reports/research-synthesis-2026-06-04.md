---
intellectual_kind: research_synthesis
parent_initiative: INIT-OPENCLAW_AKOS-93
status: research-synthesis
audience: J-OP
role_owner: PMO + CDO + CPO
language: en
authored: 2026-06-04
last_review: 2026-06-04
ratifying_research:
  - DAMA-DMBOK 2.0 (2024 maintenance revision) + DMBOK 3.0 (2025 evergreen, AI/agentic)
  - Open Data Contract Standard (ODCS) v3.1.0 — Linux Foundation Bitol project
  - Semantic/metrics layer governance (define-once-use-everywhere; MCP/AI-readiness; 2026)
internal_evidence_sweeps: 7
---

# I93 — DATA Area Foundation: research synthesis (2026-06-04)

> Evidence base for the I93 master-roadmap. Consolidates **7 internal evidence
> sweeps** (engagements, transcripts, v2.7 vault + GTM, DAMA coverage, cross-area
> org/process, area-governance pattern, cross-area data engineering) + **3 external
> research sweeps** (data contracts, semantic layer, DAMA operating model). Per
> `akos-applied-research-discipline.mdc` RULE 1 (internal precedent) + RULE 2
> (external grounding). Operator AskQuestion ratification 2026-06-04: **Full scope (C)**
> + People-governed area-creation meta-process + move DataOps into Data + all 8 DAMA
> doctrines + all 4 harmonization fixes.

## 0. The load-bearing finding

**DATA is the only top-level area in `Admin/O5-1/` with no `canonicals/` folder.**
The Chief Data Officer chain exists and is mostly active in `baseline_organisation.csv`
(CDO → Data Architect / Lead Data Scientist / Data Governance Lead → Data Steward /
Data Engineer / Database Owner), but it owns **zero** canonical doctrine. The data
quality rulebook (`DATAOPS_DISCIPLINE.md`) lives under **People**; its checklist
(`SOP-TECH_DATAOPS_QUALITY_001.md`) under **Tech**; and the Data area is **invisible
in `CANONICAL_REGISTRY.csv`** (zero Data-area rows). Operator vision: *data supports
everything; governance is the key; DAMA is the driver.* This initiative builds the
DATA area as a real, governed, DAMA-aligned area — and mints the **People meta-process**
that makes "create + harmonize an area" a repeatable, countable discipline.

## 1. Evidence matrix

| ID | Observation | Source sweep | Impact |
|:---|:---|:---|:---|
| E1 | `Data/` area has only 2 KiRBe program READMEs; no `canonicals/` | DAMA + org sweeps | No area doctrine; CDO chain owns nothing written |
| E2 | No `DATA_AREA_CHARTER.md` (RevOps, Research, 4 Marketing sub-areas all have charters) | area-gov sweep | Area identity undefined |
| E3 | DataOps doctrine under `People/canonicals/`, SOP under `Tech/System Owner/canonicals/` | scaffolding read | Orphaned from the area it governs |
| E4 | `CANONICAL_REGISTRY.csv` has 0 Data-area rows | direct read | Data invisible in metadata SSOT |
| E5 | 8-role CDO chain exists (5 active, 2 planned, Database Owner area=Tech) | org sweep | Org plane real; doctrine plane empty |
| E6 | Only 6 formal `area=Data` executable processes vs ~442 repo-wide | cross-area sweep | DATA plane is cross-cutting, not a column |
| E7 | `COMPONENT_SERVICE_MATRIX.csv` (97 rows): `data_classification`=internal for all; `legal_hold`+`retention_policy_ref` blank | DAMA sweep + direct read | "DATA serves each component" declared, not real |
| E8 | DAMA areas absent: Warehousing/BI, data contracts, semantic/metrics layer, data products, data mesh; lineage + metadata partial | DAMA sweep | Classic DAMA depth missing |
| E9 | DataOps probes `DATA-01..07` all stubbed `skip` in `dataops_quality_check.py` | cross-area sweep | Discipline active but unenforced |
| E10 | 6 engagements (SUEZ flagship w/ named data products); engagement ID schism `eng_2026_*` vs `ENG-*`; Websitz/Rushly GOI rows missing | engagements sweep | Engagement data plane needs hygiene |
| E11 | USE_CASE_ARCHIVE has 1 internal row; 5 real POC narratives not appended | engagements sweep | Capability realisations untracked |
| E12 | ~27 distinct transcripts; ~8 backfilled, ~10 partial, ~9-12 orphaned; no backfill tracker; not in Topic-Fact-Source | transcripts sweep | Transcription outran canonical backfill (operator's instinct confirmed) |
| E13 | OPS-86-15 mirror gap = 5 CSVs (AIC, AUDIENCE doc-ahead, CAPABILITY, CAPABILITY_CONFIDENCE, COUNTRY_WORK_CALENDAR); CHANNEL already mirrored | cross-area sweep | Mirror plane incomplete |
| E14 | No single "create an area" SOP; area build-out is a composed pipeline | area-gov sweep | Meta-process is the gap to mint |
| E15 | v2.7 "Research & Logic" is a sparse git mirror (~1,300 files documented, not on disk); has CDO subtree + KiRBe Supabase taxonomy + GTM | v2.7 sweep | Historical DATA lineage exists; not carried forward |

## 2. DATA org plane (baseline_organisation.csv — CDO chain)

| Role | Reports to | Entity | Status |
|:---|:---|:---|:---|
| CDO (Chief Data Officer) | O5-1 | Think Big | active |
| Data Architect | CDO | Think Big | active |
| Lead Data Scientist | CDO | Think Big | planned |
| Business Analyst (front-end of Data Gov) | Lead Data Scientist | Think Big | planned |
| Data Engineer (back-end of Data Gov) | Lead Data Scientist | Think Big | active |
| Data Governance Lead | CDO | HLK Tech Lab | active |
| Data Steward | Data Governance Lead | HLK Tech Lab | active |
| Database Owner (area=Tech; dotted line) | Data Governance Lead | HLK Tech Lab | active |

Gaps: split entity (CDO=Think Big vs Data Gov Lead=HLK Tech Lab); Database Owner sits
in Tech; Lead Data Scientist + Business Analyst planned with no process rows.

## 3. DATA process plane (area=Data, 14 rows; 6 executable)

`thi_data_prj_1` (HLK Data Governance) → `thi_data_ws_1` (Data Management) +
`thi_data_ws_2` (MasterData/Architecture). Executable processes: `thi_data_dtp_32`
(Enterprise MasterData), `thi_data_dtp_34` (RPA), `thi_data_dtp_77` (Data Modeling),
`thi_data_dtp_274` (KiRBe Ingestion DQ), `thi_data_dtp_275` (Formal Data Lineage),
`SOP-ETL_MACROECON_INGESTION_001`. Tasks: `_31` Query/KPI/Reporting Catalog, `_33`
Datamarts, `_76` SQL functions, `_78` Column Types, `_72` Make.

## 4. Cross-area data process map (115 of ~442 classified by DATA-FAM family)

| DATA-FAM family | Total | Tech | Ops | Fin | People | Research | MKT | Legal |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| DATA-FAM-CANONICAL-CSV | 44 | 4 | 19 | 0 | 3 | 1 | 4 | 0 |
| DATA-FAM-ENGAGEMENT-FACT | 18 | 0 | 7 | 0 | 9 | 1 | 4 | 0 |
| DATA-FAM-COMPLIANCE-MIRROR | 12 | 1 | 2 | 3 | 4 | 0 | 1 | 1 |
| DATA-FAM-TELEMETRY-OBS | 8 | 5 | 0 | 0 | 0 | 1 | 0 | 0 |
| DATA-FAM-KM-TOPIC | 7 | 6 | 0 | 0 | 1 | 0 | 0 | 0 |
| DATA-FAM-GTM-CRM | 5 | 0 | 0 | 2 | 0 | 1 | 2 | 0 |
| DATA-FAM-AIC-RUNTIME | 5 | 3 | 1 | 0 | 1 | 0 | 0 | 0 |
| UNMAPPED (manual in P6 batches) | 35 | 6 | 5 | 1 | 7 | 9 | 11 | 3 |

The 7 families come from `data-area-capability-coverage-2026-06-04.md`. Family→probe
clusters: COMPLIANCE-MIRROR→DATA-01/02/03; CANONICAL-CSV→DATA-01/05/07; ENGAGEMENT-FACT→
DATA-01/07; TELEMETRY-OBS→DATA-04/07; GTM-CRM→DATA-03/04; KM-TOPIC→DATA-06; AIC-RUNTIME→
DATA-06/07.

## 5. DAMA-DMBOK coverage (11 areas + adjacencies)

| DAMA area | Status | Gap to close in I93 |
|:---|:---|:---|
| 1 Data Governance | partial→strong spine | Area charter + governance-policy canonical (P2) |
| 2 Data Architecture | partial | Three-tier canonical CSV↔Supabase↔Neo4j (P3) |
| 3 Data Modeling & Design | partial | Register-centric; enterprise model deferred |
| 4 Data Storage & Operations | partial→strong | DataOps probes wiring (P6) |
| 5 Data Security | partial | Privacy/retention/legal-hold policy (P5) |
| 6 Data Integration & Interop | partial | Data-contract standard (P2) |
| 7 Document & Content Mgmt | partial | KM Topic-Fact-Source (exists; transcripts P7) |
| 8 Reference & Master Data | partial→strong | MDM/golden-record SOP (P5) |
| 9 Data Warehousing & BI | **absent** | BI/warehouse governance OR explicit "not now" decision (P5) |
| 10 Metadata | partial→strong | Consumes I91 store-coverage + CANONICAL_REGISTRY ext |
| 11 Data Quality | partial→active | DataOps live probes (P6) |
| A Data contracts | **absent** | DATA_CONTRACT_REGISTRY + ODCS-aligned standard (P2) |
| B Semantic/metrics layer | **absent** | METRICS_REGISTRY + semantic-layer canonical (P4) |
| C Data products | **absent** | DATA-FAM families as data products (P6) |
| E Data lineage | partial | Lineage SOP + automation (P4; consumes I91 graph) |
| F DataOps | partial→active | Move into Data area + wire probes (P1/P6) |

## 6. Registry schemas (verbatim, for mint packets)

**`CAPABILITY_REGISTRY.csv`** (17 cols): `capability_id, capability_name, bearer_class,
area, role_owner, originating_process_ids, substrate_id, skill_ids, lifecycle_status,
i81_verdict, i81_gap_summary, external_register_summary, last_review_at, last_review_by,
last_review_decision_id, methodology_version_at_review, notes` — Pydantic
`akos/hlk_capability_registry_csv.py::CAPABILITY_REGISTRY_FIELDNAMES`.

**`CAPABILITY_CONFIDENCE_REGISTRY.csv`** (16 cols): `confidence_id, capability_id,
substrate_score, repeatability_score, quality_score, translatability_score,
auditability_score, aggregate_confidence, rating_method, rated_at, rated_by, notes,
last_review_at, last_review_by, last_review_decision_id, methodology_version_at_review`
— Pydantic `akos/hlk_capability_confidence_csv.py::CAPABILITY_CONFIDENCE_FIELDNAMES`.
`confidence_id = CONF-<capability_id>-<YYYYMMDD>`; aggregate = mean of 5 scores (validator-enforced).

**`process_list.csv`** (33 cols): `type, orientation, entity, area, role_parent_1,
role_owner, item_parent_2, item_parent_2_id, item_parent_1, item_parent_1_id, item_name,
item_id, item_granularity, time_hours_par, time_hours_min, time_hours_max, description,
instructions, addundum_extras, confidence, count_name, frequency, quality, last_review_at,
last_review_by, last_review_decision_id, methodology_version_at_review, m3_sub_area,
engagement_template_id, persona_id, cadence_type, min_rev_value_eur, par_rev_value_eur,
max_rev_value_eur, inherited_pattern_id` — Pydantic `akos/hlk_process_csv.py::PROCESS_LIST_FIELDNAMES`.

## 7. DataOps probe structure (DATA-01..07)

`akos/hlk_dataops_quality.py`: `VALID_DATAOPS_DIMENSION_CODES` (7), `VALID_DATA_SURFACES`
(`canonical_csv, mirror_table, fdw_projection, manifest_md, pydantic_ssot,
observability_evidence`), `DATAOPS_FINDING_FIELDNAMES`, `DATAOPS_SWEEP_FIELDNAMES`.
`scripts/dataops_quality_check.py::PROBE_REGISTRY` keyed by `DATA-0N` → all currently
`skip`. I93 P6 extends with `DATA_FAM_PROBE_PROFILES` + `--data-fam` flag + incremental
live probes (mirror parity first → closes OPS-86-15 evidence).

## 8. Area-completeness bar (14 components — the harmonization SSOT)

From the area-governance sweep. A fully-governed area satisfies: (1) parent redesign,
(2) area charter, (3) discipline/sub-area charters, (4) process_list rows, (5)
baseline_organisation roles, (6) CAPABILITY + CONFIDENCE rows, (7) CANONICAL_REGISTRY +
PRECEDENCE entries, (8) dimension/adapter registries, (9) paired SOP+runbook, (10)
Supabase mirrors, (11) cursor rule + skill, (12) Quality Fabric harmonization, (13) area
README/index, (14) `inherited_pattern_id` on processes. Today: Marketing/Brand + RevOps
score highest; **Data scores lowest**. This 14-component bar becomes `compose_AREA`
(new Quality Fabric specialty) + `scripts/validate_area_completeness.py` (countable
governance) — the mechanism that makes "harmonize the quality of our areas" real.

## 9. External grounding (applied-research RULE 2)

- **Data contracts** → Open Data Contract Standard (ODCS v3.1.0, Linux Foundation Bitol),
  the 2026 industry standard (supersedes the older Data Contract Specification).
  Components: schema, semantics, SLAs, quality rules, ownership, versioning/change-mgmt.
  Best practice: contracts-as-code in Git + CI validation + start lean (5 critical
  constraints) + semantic versioning + warn-first-fail-later. **Maps directly onto the
  AKOS two-plane model** (CSV SSOT + mirror) and the existing drift-gate pattern.
- **Semantic / metrics layer** → governed "define once, use everywhere"; metrics layer =
  subset (measure defs). DAMA-aligned governance: split business vs technical ownership;
  RBAC/RLS on metric defs; AI-readiness via MCP. Version-controlled metrics-as-code.
- **DAMA-DMBOK** → governance-at-center "DAMA Wheel"; 2024 revision renames "program"→
  "function", integrates AI governance, defines Data Owner as a *business person
  accountable for a domain*; DMBOK 3.0 (2025) targets AI/agentic. Operating model for
  decentralised orgs = **federated / data mesh**: global standards (contracts, quality,
  metadata) + domain ownership. **This is the I93 model**: DATA area sets global
  standards; each area owns its domain data products (cross-area engineering).

## 10. Cross-references

- Operator AskQuestion ratification 2026-06-04 (Full/C + People meta-process + DataOps
  move + 8 DAMA doctrines + 4 hygiene fixes).
- `docs/wip/planning/90-routing-and-wiring/reports/data-area-capability-coverage-2026-06-04.md` (7 DATA-FAM families).
- `docs/wip/planning/91-enterprise-graph-store-coverage/master-roadmap.md` (graph + store-coverage; I93 consumes).
- `docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/DATAOPS_DISCIPLINE.md`, `HOLISTIKA_QUALITY_FABRIC.md`, `PEOPLE_DESIGN_PATTERN_LIBRARY.md`.
- `.cursor/rules/akos-holistika-operations.mdc` (two-plane), `akos-people-discipline-of-disciplines.mdc` (pattern mint).
