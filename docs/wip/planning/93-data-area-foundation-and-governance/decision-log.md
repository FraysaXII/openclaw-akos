---
intellectual_kind: decision_log
parent_initiative: INIT-OPENCLAW_AKOS-93
status: ratified
language: en
authored: 2026-06-04
last_review: 2026-06-04
ratified_at: 2026-06-04
ratified_by: Operator (GATE #1 — ratify-dispatch)
---

# I93 — Decision log (RATIFIED at GATE #1, 2026-06-04)

> **GATE #1 CLEARED** — operator ratified D-IH-93-A..H (2026-06-04, "ratify and dispatch").
> Composer is now authorized to mint `INITIATIVE_REGISTRY.csv` (`INIT-OPENCLAW_AKOS-93`) +
> `DECISION_REGISTER.csv` (D-IH-93-A..H) rows and begin P0 canonical writes. Plain-language
> summaries lead; codes travel alongside (per `akos-operator-communication.mdc`).
> Plain-language summaries lead; codes travel alongside (per `akos-operator-communication.mdc`).

| ID | Question / trigger | Options considered | Decision | Rationale |
|:---|:---|:---|:---|:---|
| **D-IH-93-A** | Should the DATA build-out be its own initiative? | (a) fold into I91; (b) new initiative | **New initiative I93**, Full scope, CDO+CPO+PMO co-owned | I91 is graph+store-coverage (infra slice). The DATA *area* (org + DAMA doctrine + People meta-process + harmonization) is broader and People-led; warrants its own initiative consuming I91. |
| **D-IH-93-B** | How to make "create an area" governable? | (a) ad-hoc per area; (b) People-governed meta-process | **Meta-process**: `pattern_area_buildout` + `SOP-PEOPLE_AREA_GOVERNANCE_001` + `compose_AREA` Quality-Fabric specialty + `validate_area_completeness.py` | Operator: "create a People governed process out of this area creation… this way our process will be governable." People = discipline-of-disciplines (RULE 1): mints the pattern; areas author their own canonicals. 14-component bar = countable governance. |
| **D-IH-93-C** | Where do DATA canonicals live; what about DataOps? | (a) keep DataOps in People; (b) move it | **Create `Data/{Governance,Architecture,Science}/canonicals/` + `DATA_AREA_CHARTER.md`; MOVE DataOps doctrine (People→Data) + SOP (Tech→Data)** | Operator chose "folders + charter AND move." Re-homes the data-quality discipline to the area it governs; System Owner + DevOPS stay co-owners (execution remains Tech). |
| **D-IH-93-D** | Which DAMA doctrines to mint | subset vs all | **All 8**: governance policy; data-contract standard + registry; semantic/metrics layer; data architecture (three-tier); lineage SOP; MDM golden-record SOP; privacy/retention policy; BI/warehouse governance (or explicit "not now") | Operator selected all. Closes the absent DAMA areas (contracts, semantic layer, BI, data products) + partials (architecture, lineage, security, MDM). |
| **D-IH-93-E** | Which harmonization/hygiene fixes | subset vs all | **All 4**: component data-contract population; engagement ID reconciliation + Websitz/Rushly GOI rows; USE_CASE_ARCHIVE backfill (5 POCs); transcript-backfill tracker + high-value promotion | Operator selected all. Makes "DATA serves each component" real; fixes the engagement join schism; records real use cases; closes the transcript backfill gap. |
| **D-IH-93-F** | DATA-FAM + cross-area engineering | row-by-row vs family-level | **7 DATA-FAM umbrella families** (CAP+CONF+process) + cross-area map (115 classified, 35 unmapped → area batches); coordinate with I91 | Family-level avoids 400+ one-off CAP mints; matches `data-area-capability-coverage-2026-06-04.md`. Federated/data-mesh model: DATA sets standards, areas own products. |
| **D-IH-93-G** | Order vs the 4 P4 items | P4-first / commit-then-design / design-first | **Design-first**; Tier-0 P3e commit + OPS-90-9 + I86 UAT run as Composer packets in parallel; I91 P1 DATA-FAM folds into I93 P6 | Operator: "go for option C… do more research still… heavy lifting now so Composer executes it all." |
| **D-IH-93-H** | DataOps-move ripple contract | in-place vs aliased move | **`git mv` with one-cycle deprecation aliases + full ripple checklist** (Quality-Fabric §6 path, all linked refs, cursor-rule globs, CANONICAL_REGISTRY/PRECEDENCE/KNOWLEDGE_PAIRING rows) | Same shape as OPS-86-26 legacy-SSOT migration; prevents broken links while the move lands. |
| **BI/warehouse governance** *(ratified P5 as `D-IH-93-I`; **amended P5b**)* | BI/warehouse governance now? | not-now → full pack | **Full Postgres-native doctrine** — see amended `D-IH-93-I` | Research proved warehouse = Supabase T2; SUEZ pain = missing adapters/contracts. |

## Per-phase research & quality bar (operationalises existing decisions — no new ID)

Operator instruction 2026-06-04: *"how do we ensure these have such quality-bar
(research for each)."* The answer is the **§9.0 invariant bar** in the master roadmap —
every phase P2–P8 produces its own research packet (`reports/research-p<N>-<date>.md`),
an evidence-base section in each minted canonical, and a tranche charter that passes the
synthesis-before-tranche check **before** Composer executes.

This is **not a new minted decision** — it operationalises three already-ratified things:

- **Design-first sequencing** (`D-IH-93-G` — thinking-seat heavy lift before Composer), now
  applied **once per phase**, not once for the whole initiative.
- **Applied-research discipline** (the rulebook requiring internal precedent + external
  grounding on any canonical/rule/skill mint — `akos-applied-research-discipline.mdc`).
- **Synthesis-before-tranche** (the pre-commit scope/atomicity/reversibility review —
  `akos-synthesis-before-tranche.mdc`).

No `DECISION_REGISTER.csv` row is minted for the bar itself; it lives in the plan SSOT
(`master-roadmap.md` §9.0) per `akos-planning-traceability.mdc`.

## P2b inline-ratify (2026-06-04 — operationalises D-IH-93-D catalog posture)

| Gate | Decision |
|:---|:---|
| Catalog SSOT | **Option A** — repo-native; git CSV authoritative |
| DAMA-tool interop | **A++** — three-layer stack (§7); **accelerate L3 ODCS export to P3** (not P8) |
| Governed-claim bar | **Strict + forward-declared** (§9) — no gap-theatre on "governed" language |
| P2b commit | Full pack including posture §7–§9 |

Recorded in initiative decision log only (no new `D-IH-93-*` ID — extends existing eight-DAMA charter `D-IH-93-D`).

## P5b BI/integration full pack (2026-06-04)

| Gate | Decision |
|:---|:---|
| Doctrine scope | **Full pack (Option A)** — amend `D-IH-93-I`; mint governance + registries + matrix tranche |
| SUEZ unblock | **Stream B alternative** — Supabase Edge + ERP panel when client PA blocked |
| Warehouse posture | **Supabase Postgres T2** — no Snowflake primary build |

Minted: `DATA_BI_GOVERNANCE.md`, `DATA_INTEGRATION_PLANE.md`, `BI_CONSUMER_REGISTRY.csv`, `RPA_ADAPTER_REGISTRY.csv`, engagement scaffold + SUEZ Stream B SOPs, `bi_integration_readiness_check.py`, COMPONENT_SERVICE_MATRIX tranche (~10 adds + Power Platform dedupe tags).

Supersedes P5 not-now row in §P5 BI gate below for doctrine scope only; P5 MDM/privacy mint unchanged.

## P5 BI gate + MDM/privacy mint (2026-06-04)

| Gate | Decision |
|:---|:---|
| BI / warehouse governance | **Amended at P5b** — was explicit not-now; now full pack under amended `D-IH-93-I` |
| MDM golden record | `SOP-DATA_MASTERDATA_GOLDEN_RECORD_001.md` pairs `thi_data_dtp_32` + `mdm_golden_record_check.py` |
| Privacy / retention | `DATA_PRIVACY_RETENTION_POLICY.md` — five-tier classification + retention schedule IDs for P7 matrix |

Rationale for not-now: roadmap non-goal (no warehouse build in I93); semantic layer + metrics registry cover current BI-adjacent needs; P7 component matrix uses privacy enum without warehouse charter.

Supersedes decision-log row 30 placeholder (BI ID now allocated as `D-IH-93-I` at P5 ratification).

## Ratification gate

GATE #1 (operator): approve D-IH-93-A..H (+ BI decision deferred to P5) and authorize:
1. `INITIATIVE_REGISTRY.csv` += `INIT-OPENCLAW_AKOS-93` row.
2. `DECISION_REGISTER.csv` += D-IH-93-A..H rows.
3. P0 canonical-CSV writes (PEOPLE_DESIGN_PATTERN_REGISTRY + process_list).

All three are canonical-CSV writes — Composer executes after operator approval.

## Cross-references

- Master roadmap: [`master-roadmap.md`](master-roadmap.md)
- Evidence: [`reports/research-synthesis-2026-06-04.md`](reports/research-synthesis-2026-06-04.md)
