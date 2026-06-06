---
language: en
status: active
canonical: true
role_owner: People Operations Manager (vault wayfinding) + Chief People Officer (interim — operator)
classification: way_of_working
intellectual_kind: vault_index
ssot: true
authored: 2026-03-31
last_review: 2026-05-15
last_review_initiative: I79 P5 (orphan-folder hygiene; full §Vault Structure rewrite per D-IH-79-K)
---

# Holistika Knowledge Vault v3.0

**Version**: 3.0
**Date**: 2026-03-31 (last full rewrite 2026-05-15 per I79 P5 cluster C)
**Status**: Active canonical vault
**Governance**: [Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md](Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md)
**Forward-layout decisions reflected here**: I22 (per-area `canonicals/` federation + `programs/` per-role), I63 (Envoy Tech Lab External Repos SOPs), I70 (Research promoted to top-level area; compliance/ master migrated to per-area-role homes), I72 (Marketing sub-area `canonicals/` charters), I79 (People manifesto + design pattern library + agentic doctrine + cross-area breakthrough SOP).

---

## Purpose

This is the active Holistika Knowledge Vault. It holds all canonical knowledge, SOPs, research outputs, project documents, and operational artifacts for the HLK ecosystem.

The folder structure mirrors the organisational hierarchy defined in [baseline_organisation.csv](Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv). Every document lives under the role that owns it. Per the **post-I22 forward-layout convention**, role-folder canonicals live under `<role>/canonicals/`; per-program casework lives under `<role>/programs/<program_id>/`; per-canonical dimension tables live under `<role>/canonicals/dimensions/`.

## How to use this vault

### Adding a document

1. Identify the **role owner** from [baseline_organisation.csv](Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv).
2. Navigate to that role's folder under `Admin/O5-1/<area>/<role>/canonicals/` (or top-level `Research/<discipline>/canonicals/` for the Research area, post-I70).
3. Write the document as markdown.
4. If it is a formal process, add a row to [process_list.csv](Admin/O5-1/People/Compliance/canonicals/process_list.csv).
5. If it is an SOP, follow the [SOP-META envelope](Admin/O5-1/People/Compliance/canonicals/SOP-META_PROCESS_MGMT_001.md). Per-`akos-executable-process-catalog.mdc` Rule 1, every executable SOP needs a paired runbook (Python script under `scripts/<purpose>.py`, YAML catalog entry, or external orchestrator workflow) with bidirectional cross-references.

### Promotion ladder for sensitive casework

Use a staged promotion path for founder-governance and other sensitive business casework:

1. Keep raw evidence and exploratory interpretation outside the canonical vault or in `docs/wip/`.
2. Promote stable, role-owned case decisions into `v3.0/`.
3. Formalize repeatable behavior as SOPs.
4. Register only the repeatable process layer in [process_list.csv](Admin/O5-1/People/Compliance/canonicals/process_list.csv).
5. Update [baseline_organisation.csv](Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv) only if ownership itself changes.

Current examples:

- [Founder incorporation knowledge index](Admin/O5-1/People/Legal/FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md)
- [External counsel handoff package](Admin/O5-1/People/Legal/EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md)
- [Founder governance document lifecycle](Admin/O5-1/People/Compliance/FOUNDER_GOVERNANCE_DOCUMENT_LIFECYCLE.md)

### Program-scoped casework (Initiative 22 P3 forward convention)

When a role-folder accumulates more than a handful of program-specific case docs, add a `programs/<program_id>/README.md` subfolder under the role to host new program-scoped material. This keeps role-folder roots from becoming flat dumps as additional programs (`PRJ-HOL-KIRBE-*`, `PRJ-HOL-CLIENT-*`, …) are added.

- **`<program_id>`** matches the canonical identifier in `process_list.csv` (e.g. `PRJ-HOL-FOUNDING-2026`).
- **Existing program-scoped docs at role-folder root stay in place** to avoid link breakage; each gains a `> **Program**` admonition pointing at the program README.
- **New program-scoped docs go directly into the program subfolder.**
- **Plane-scoped docs** (e.g. ADVOPS plane SOP, router) remain at the role-folder root because they are program-agnostic.

Current program subfolders:

**`PRJ-HOL-FOUNDING-2026`** (founder incorporation; ADVOPS plane):

- [`Admin/O5-1/People/Legal/programs/PRJ-HOL-FOUNDING-2026/README.md`](Admin/O5-1/People/Legal/programs/PRJ-HOL-FOUNDING-2026/README.md)
- [`Admin/O5-1/People/Compliance/programs/PRJ-HOL-FOUNDING-2026/README.md`](Admin/O5-1/People/Compliance/programs/PRJ-HOL-FOUNDING-2026/README.md)
- [`Admin/O5-1/Operations/PMO/programs/PRJ-HOL-FOUNDING-2026/README.md`](Admin/O5-1/Operations/PMO/programs/PRJ-HOL-FOUNDING-2026/README.md)

**`PRJ-HOL-KIR-2026`** (KiRBe SaaS platform — dual-natured product + KM ingestion source per D-IH-16; Initiative 23 P6, 2026-04-29):

- [`Admin/O5-1/Tech/System Owner/programs/PRJ-HOL-KIR-2026/README.md`](Admin/O5-1/Tech/System%20Owner/programs/PRJ-HOL-KIR-2026/README.md)
- [`Admin/O5-1/Data/Architecture/programs/PRJ-HOL-KIR-2026/README.md`](Admin/O5-1/Data/Architecture/programs/PRJ-HOL-KIR-2026/README.md)
- [`Admin/O5-1/Data/Governance/programs/PRJ-HOL-KIR-2026/README.md`](Admin/O5-1/Data/Governance/programs/PRJ-HOL-KIR-2026/README.md)
- [`Admin/O5-1/Finance/Business Controller/programs/PRJ-HOL-KIR-2026/README.md`](Admin/O5-1/Finance/Business%20Controller/programs/PRJ-HOL-KIR-2026/README.md)
- [`Admin/O5-1/People/programs/PRJ-HOL-KIR-2026/README.md`](Admin/O5-1/People/programs/PRJ-HOL-KIR-2026/README.md)
- [`Admin/O5-1/Operations/PMO/programs/PRJ-HOL-KIR-2026/README.md`](Admin/O5-1/Operations/PMO/programs/PRJ-HOL-KIR-2026/README.md)

Authoritative convention: [`compliance/README.md`](../compliance/README.md) (Initiative 22 P1).

### Finding a document

- By role: navigate the folder tree below.
- By process: look up the `item_id` in [process_list.csv](Admin/O5-1/People/Compliance/canonicals/process_list.csv) and find its `role_owner`. Every cadence-bound row carries a paired SOP path + runbook path (per `akos-executable-process-catalog.mdc`).
- By design pattern: look up the [`PEOPLE_DESIGN_PATTERN_REGISTRY.csv`](Admin/O5-1/People/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv) (post-I79 P2) — People-area patterns that other areas inherit when crafting their own processes.
- By compliance classification: check [access_levels.md](Admin/O5-1/People/Compliance/canonicals/access_levels.md), [confidence_levels.md](Admin/O5-1/People/Compliance/canonicals/confidence_levels.md), or [source_taxonomy.md](Admin/O5-1/People/Compliance/canonicals/source_taxonomy.md).

### Knowledge management (Topic–Fact–Source, Output 1)

Holistika-wide KM is governed by [HLK_KM_TOPIC_FACT_SOURCE.md](Admin/O5-1/People/Compliance/canonicals/HLK_KM_TOPIC_FACT_SOURCE.md): **sources** (output types 0–4), **facts** (atomic, cited claims), **topics** (bundles and indexes), aligned to `artifact_role` and [PRECEDENCE.md](Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md).

| Need | Where |
|------|--------|
| Full contract (manifest fields, Obsidian tag vocabulary) | [HLK_KM_TOPIC_FACT_SOURCE.md](Admin/O5-1/People/Compliance/canonicals/HLK_KM_TOPIC_FACT_SOURCE.md) |
| Topic bundle template | [TOPIC_KNOWLEDGE_INDEX_TEMPLATE.md](Admin/O5-1/People/Compliance/canonicals/TOPIC_KNOWLEDGE_INDEX_TEMPLATE.md) |
| Example visual manifest | [VISUAL_MANIFEST_EXAMPLE.manifest.md](Admin/O5-1/People/Compliance/canonicals/VISUAL_MANIFEST_EXAMPLE.manifest.md) |
| PMO backlog index (Trello → topic_id; Trello not SSOT) | [RESEARCH_BACKLOG_TRELLO_REGISTRY.md](Admin/O5-1/Operations/PMO/canonicals/RESEARCH_BACKLOG_TRELLO_REGISTRY.md) |
| Trello board JSON imports (primary + archive slices) | [imports/README.md](Admin/O5-1/Operations/PMO/imports/README.md) |
| `process_list.csv` maintenance (columns, parent ids, duplicate names, paired SOP+runbook) | [SOP-PMO_PROCESS_LIST_CSV_MAINTENANCE_001.md](Admin/O5-1/Operations/PMO/canonicals/SOP-PMO_PROCESS_LIST_CSV_MAINTENANCE_001.md) |
| FINOPS counterparty register (`finops/FINOPS_COUNTERPARTY_REGISTER.csv`; no amounts in git; moved to `finops/` subdirectory 2026-05-23 per I81 P2 T1 / D-IH-81-Q) | [SOP-HLK_FINOPS_COUNTERPARTY_REGISTER_MAINTENANCE_001.md](Admin/O5-1/Finance/Business%20Controller/canonicals/SOP-HLK_FINOPS_COUNTERPARTY_REGISTER_MAINTENANCE_001.md) |
| GOI/POI register (`GOI_POI_REGISTER.csv`; obfuscated knowledge dimension, raw mapping off-repo) | [SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md](Admin/O5-1/People/Compliance/canonicals/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md) |
| Adviser-call transcript redaction policy (forward-only) | [SOP-HLK_TRANSCRIPT_REDACTION_001.md](Admin/O5-1/People/Compliance/canonicals/SOP-HLK_TRANSCRIPT_REDACTION_001.md) |
| External Adviser Engagement (ADVOPS) plane SOP | [SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md](Admin/O5-1/Operations/PMO/canonicals/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md) |
| External Adviser router (Legal / Fiscal / IP / Banking / Certification / Notary) | [EXTERNAL_ADVISER_ROUTER.md](Admin/O5-1/Operations/PMO/canonicals/EXTERNAL_ADVISER_ROUTER.md) |
| Topic-Fact-Source manifest for ADVOPS plane | [topic_external_adviser_handoff.manifest.md](_assets/advops/2026-holistika-incorporation/adviser_handoff/topic_external_adviser_handoff.manifest.md) |
| `_assets/` directory contract (forward layout) | [_assets/README.md](_assets/README.md) |
| WIP topic syntheses (interpretation layer) | [docs/wip/intelligence/](../../../wip/intelligence/) (Trello stubs per topic; archived `hlk-km/` at [docs/wip/_archived/hlk-km-pre-2026-05-12/](../../../wip/_archived/hlk-km-pre-2026-05-12/)) |
| Pilot Output 1 bundle (rasters + `*.manifest.md` + stubs) | [_assets/km-pilot/](_assets/km-pilot/) |
| Workspace roadmap / traceability | [master-roadmap.md](../../../wip/planning/03-hlk-km-knowledge-base/master-roadmap.md) |
| GitHub repository index (Holistika-tracked repos; GitHub is SSOT for code) | [Repositories/REPOSITORIES_REGISTRY.md](Envoy%20Tech%20Lab/Repositories/REPOSITORIES_REGISTRY.md) |
| MADEIRA verdict and dossier cadence (`env_tech_dtp_madeira_verdict`) | [SOP-MADEIRA_VERDICT_AND_CADENCE_001.md](Admin/O5-1/Tech/System%20Owner/canonicals/SOP-MADEIRA_VERDICT_AND_CADENCE_001.md) |
| MADEIRA incident response (`env_tech_dtp_madeira_incident`) | [SOP-MADEIRA_INCIDENT_RESPONSE_001.md](Admin/O5-1/Tech/System%20Owner/canonicals/SOP-MADEIRA_INCIDENT_RESPONSE_001.md) |
| MADEIRA scenario lifecycle and telemetry (`env_tech_dtp_madeira_lifecycle`, `env_tech_dtp_madeira_telemetry`) | [SOP-MADEIRA_SCENARIO_LIFECYCLE_001.md](Admin/O5-1/Tech/System%20Owner/canonicals/SOP-MADEIRA_SCENARIO_LIFECYCLE_001.md) |
| MADEIRA quarterly UX review — control plane (`env_tech_dtp_madeira_uxreview`) | [SOP-MADEIRA_UX_REVIEW_001.md](Admin/O5-1/Tech/System%20Owner/canonicals/SOP-MADEIRA_UX_REVIEW_001.md) |
| **People manifesto (discipline-of-disciplines)** | [HOLISTIKA_PEOPLE_MANIFESTO.md](Admin/O5-1/People/canonicals/HOLISTIKA_PEOPLE_MANIFESTO.md) (I79 P1) |
| **People design pattern registry (cross-area inheritance)** | [PEOPLE_DESIGN_PATTERN_REGISTRY.csv](Admin/O5-1/People/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv) (I79 P2) |
| **People agentic doctrine (jargon-free)** | [HOLISTIKA_AGENTIC_DOCTRINE.md](Admin/O5-1/People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md) (I79 P3a) |
| **Tech Lab agentic framework landscape (jargon-heavy)** | [AGENTIC_FRAMEWORK_LANDSCAPE.md](Admin/O5-1/Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) (I79 P3b) |
| **Ethical agentic boundaries (red-lines)** | [ETHICAL_AGENTIC_BOUNDARIES.md](Admin/O5-1/People/Ethics/canonicals/ETHICAL_AGENTIC_BOUNDARIES.md) (I79 P3a) |
| **Cross-area breakthrough propagation (when People mints a new pattern)** | [SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md](Admin/O5-1/People/canonicals/SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md) (I79 P4) |
| **Research area charter (top-level area, post-I70)** | [RESEARCH_AREA_CHARTER.md](Research/canonicals/RESEARCH_AREA_CHARTER.md) |

**Binary visuals (Output 1):** store under `v3.0/_assets/<topic_id>/` with a sidecar `*.manifest.md` and a short companion markdown stub for search. Do not use `.cursor/` or other tool-local paths for canonical assets.

**Obsidian:** use the controlled tag prefixes documented in the KM contract; do not invent new root tags without updating that document.

### Platform compatibility

| Platform | How to use |
|----------|------------|
| Obsidian | Open `docs/references/hlk/v3.0/` as a vault |
| Google Drive | Sync this folder; structure maps 1:1 to Drive folders |
| SharePoint | Same folder mapping |
| Git / GitHub | This monorepo plus any repos listed in the Envoy **repository registry** (code SSOT remains on GitHub) |
| KiRBe | Ingest as a source; CSVs provide the graph structure |
| Neo4j (optional) | Mirrored read index: run `py scripts/sync_hlk_neo4j.py` after CSV changes; credentials in `~/.openclaw/.env` (`NEO4J_*`); see `PRECEDENCE.md` mirrored row |
| MADEIRA | Reads registry CSVs for structure, markdown tree for content |

### Entity placement: Admin, Envoy Tech Lab, Research, Think Big

> **Five top-level entities** in `v3.0/`: `Admin/` (role-owned canonicals + AI governance chain), `Envoy Tech Lab/` (platform docs + Repositories registry), `Research/` (top-level area, promoted from Admin/O5-1/Research per D-IH-70-S), `Think Big/` (non-repo engagement artefacts), `_assets/` (KM Output-1 binaries with manifests).

- **Admin (`Admin/…`)** — Role-owned canonical knowledge under `Admin/O5-1/<area>/<role>/canonicals/`: SOPs, internal programs (e.g. ENISA readiness), compliance, research methodology. Mirrors [baseline_organisation.csv](Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv). Also hosts the AI governance chain at `Admin/AI/` (Susana Madeira persona + AIC role-class — both currently RESERVED).
- **Envoy Tech Lab** (top-level) — **All GitHub repositories** Holistika tracks (platform, internal tools, client-delivery) are indexed in [Envoy Tech Lab/Repositories/](Envoy%20Tech%20Lab/Repositories/README.md). Vault markdown for KiRBe and MADEIRA continues under [Envoy Tech Lab/KiRBe/](Envoy%20Tech%20Lab/KiRBe/) and [Envoy Tech Lab/MADEIRA/](Envoy%20Tech%20Lab/MADEIRA/). Default pattern: **registry pointer** to GitHub; submodules only when CI or pin requirements justify it (see Repositories README). Distinct from `Admin/O5-1/Envoy Tech Lab/` which hosts the area-role canonicals (Cross Repo SOPs, External Repos SOPs, MADEIRA-AKOS migration manifests, the agentic framework landscape).
- **Research** (top-level, post-I70) — Area charter + 4 discipline charters (Methodology, Intelligence, Diagnosis, Validation) under `Research/<discipline>/canonicals/`. Promoted from `Admin/O5-1/Research/` per **D-IH-70-S** (2026-05-12, Initiative 70). The legacy `Admin/O5-1/Research/` tools-shed (HUMINT Techniques, OSINT Operations, Methodology Pillars, Research Techniques, Intelligence Matrix, Deep Research) remains as historical technique archive under `Admin/O5-1/Research/`; new canonical discipline work happens at top-level `Research/`.
- **Think Big** — **Non-repository** client and adviser engagement artifacts: commercials, SOWs, engagement memos, decks, and other deliverables that are not the Git root of a codebase. Two-root model (`Clients/` outbound, `Advisers/` inbound) per D-W13-I. Link Think Big materials to repo rows and topic indexes in Envoy/PMO. See [Think Big/README.md](Think%20Big/README.md).
- **`_assets/`** — KM Output-1 binary visuals with paired `*.manifest.md` and Markdown stub files. Forward layout `_assets/<plane>/<program_id>/<topic_id>/` per I22 P3 convention. See [_assets/README.md](_assets/README.md).

## Governance

- **Canonical baselines** live per-area-role under `Admin/O5-1/<area>/<role>/canonicals/` (post-I70 P4.5 federation; the legacy aggregator `docs/references/hlk/compliance/` was migrated 2026-05-12 + tombstone removed 2026-05-15 per I79 P5).
- **Path-mapping registry** for the federation: [`Admin/O5-1/People/Compliance/canonicals/CANONICAL_REGISTRY.csv`](Admin/O5-1/People/Compliance/canonicals/CANONICAL_REGISTRY.csv).
- **Historical reference** lives in [Research & Logic/](../Research%20%26%20Logic/) (v2.7, read-only — 1 300+ files; not linted by validators).
- **Active knowledge** lives here in `v3.0/` (edit here).
- See [PRECEDENCE.md](Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md) for the full precedence contract.

## Vault Structure

> **Reading guide.** This section mirrors the actual on-disk layout as of 2026-05-15 (post-I70 / post-I22 / post-I79). Every per-role folder hosts a `canonicals/` subfolder for SSOT documents and an optional `programs/<program_id>/` subfolder for per-program casework. Per-canonical dimension tables (CSV registries) live at `<role>/canonicals/dimensions/`. Empty role-leaf folders are **intentional scaffolding** that mirror `baseline_organisation.csv`; they are not orphans.

### Top-level layout (v3.0/)

```
v3.0/
  index.md                         (this file — vault wayfinding SSOT)
  Admin/                           Role-owned canonicals + AI governance chain
  Envoy Tech Lab/                  Top-level platform docs + Repositories registry
  Research/                        Top-level Research area (post-I70 promotion)
  Think Big/                       Non-repository engagement artifacts (Clients + Advisers)
  _assets/                         KM Output-1 binary visuals with manifests
```

### Admin (Entity: Holistika)

```
Admin/
  O5-1/                              Chief Business Officer
    Data/                            CDO
      Architecture/                  Data structure and architecture
        canonicals/                  (none yet — area scaffolding)
        programs/<program_id>/       Per-program casework (e.g. PRJ-HOL-KIR-2026)
      Governance/                    Data governance and quality
        canonicals/                  (none yet)
        programs/<program_id>/
      Science/                       Data science and analytics
    Envoy Tech Lab/                  CTO-Lab area (distinct from top-level Envoy Tech Lab/)
      canonicals/                    AGENTIC_FRAMEWORK_LANDSCAPE (I79 P3b) + …
      Cross Repo/                    Cross-repo schema-propagation SOP (I63)
      External Repos/                External-repo bless + drift-remediation SOPs (I63)
      MADEIRA-AKOS/                  MADEIRA-on-AKOS migration manifests (I02)
        historical-AIC/
        library/
        migration-manifests/
        wip/
      Repositories/                  External-repo bless template + SOP-TECH_AGENTIC_INFRA_001 (I79 P3b)
    Finance/                         CFO
      Business Controller/           Strategic financial analysis
        canonicals/                  FINOPS_COUNTERPARTY register SOP + Pricing/Taxes scaffolding
        Pricing/                     (RESERVED scaffolding — baseline role)
        Taxes/                       (RESERVED scaffolding — baseline role)
        programs/<program_id>/
      Financial Controller/          Financial statement accountability
        Front Office/                (RESERVED scaffolding — O2C / PTP)
    Marketing/                       CMO (post-I72 sub-area canonicals federation)
      canonicals/                    Cross-sub-area marketing SSOTs
      Brand/                         Brand identity + creative direction
        canonicals/                  BRAND_VISION + BRAND_DO_DONT + BRAND_JARGON_AUDIT + BRAND_BASELINE_REALITY_MATRIX + …
        AV/                          Audio-visual sub-discipline (BRAND_AV_CHARTER)
          canonicals/
        Copywriter/                  Copywriting sub-discipline (BRAND_COPYWRITING_DISCIPLINE)
          canonicals/
        Design/                      Design sub-discipline (BRAND_DESIGN_CHARTER)
          canonicals/
        UX Designer/                 UX sub-discipline (BRAND_UX_DESIGNER_CHARTER + BRAND_GANTT_DISCIPLINE)
          canonicals/
      Experimentation/               Experimentation sub-area (I72 P1)
        canonicals/                  Sub-area charter + ATTRIBUTION_ADAPTER_REGISTRY (post-I72 P9)
      Growth/                        (legacy slot; SOPs migrated to Reach/ per D-IH-72-Z)
      Reach/                         Reach sub-area — top-of-funnel + outbound + inbound (post-I72 P9 owner of CRM/EMAIL/COMMUNICATION/SCHEDULING adapters)
        canonicals/                  Sub-area charter + GTM SOPs migrated from Growth/
      Resonance/                     Resonance sub-area (I72 P1)
        canonicals/                  Sub-area charter
        Account Management/          Nested sub-area (I72 P1 R7)
          canonicals/                ACCOUNT_MANAGEMENT_CHARTER
      Social/                        Social media management
        Community Manager/           (RESERVED scaffolding)
        Paid Media Manager/          (RESERVED scaffolding)
      Storytelling/                  Storytelling sub-area (I72 P1)
        canonicals/                  Sub-area charter
    Operations/                      COO
      Engagement/                    Engagement sub-area
        canonicals/                  Engagement template registry + …
      IntelligenceOps/               Intelligence-ops sub-area (I66 P3)
        canonicals/                  CORPINT methodology SOPs (operator-private)
      PMO/                           Project management office
        canonicals/                  9 SOPs incl. SOP-PMO_PROCESS_LIST_CSV_MAINTENANCE_001 + KB_HUMAN_READABILITY_CHARTER + WORKSPACE_BLUEPRINT_HOLISTIKA + INITIATIVE_REGISTRY/OPS_REGISTER/DECISION_REGISTER + business-strategy/ (I29/I30 strategy SSOT)
        imports/                     Trello board JSON imports
        sourcing-briefs/             Outbound sourcing brief templates (en/es/fr)
        programs/<program_id>/       Per-program casework (PRJ-HOL-FOUNDING-2026, PRJ-HOL-KIR-2026)
      RevOps/                        Revenue operations sub-area (I72 P8/P9)
        canonicals/                  REVOPS_PROCESS_CATALOG + REVOPS/BILLING adapter registries + 3 RevOps SOPs + 2 ERP panel routes
      SMO/                           Service management office
        canonicals/                  SMO charter + CONTRACT_ADAPTER_REGISTRY
    People/                          CPO (discipline-of-disciplines per I79 manifesto)
      canonicals/                    HOLISTIKA_PEOPLE_MANIFESTO (I79 P1) + HOLISTIKA_AGENTIC_DOCTRINE (I79 P3a) + SOP-PEOPLE_AGENTIC_OPERATIONS_001 (I79 P3a) + SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001 (I79 P4) + dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv (I79 P2)
      Compliance/                    Policy and methodology enforcement
        canonicals/                  PRECEDENCE + access_levels + confidence_levels + source_taxonomy + SOP-META_PROCESS_MGMT_001 + HLK_KM_TOPIC_FACT_SOURCE + SOPs + dimensions/ (TOPIC_REGISTRY, GOI_POI_REGISTER, FINOPS_COUNTERPARTY_REGISTER, PERSONA_REGISTRY, SKILL_REGISTRY, INITIATIVE_REGISTRY, OPS_REGISTER, DECISION_REGISTER, PROCESS_LIST, BASELINE_ORGANISATION, COMPONENT_SERVICE_MATRIX, …)
        programs/<program_id>/
      Ethics/                        Ethical posture + red-lines
        canonicals/                  ETHICS_CHARTER + ETHICAL_AGENTIC_BOUNDARIES (I79 P3a)
      Learning/                      Learning + curriculum (I73)
        canonicals/                  Learning charter + curriculum SOPs (I73)
      Legal/                         Legal counsel + specialists
        canonicals/                  Legal SOPs + counsel handoff package + open-questions register + filed-instruments register
        _templates/                  Reusable legal templates
        programs/<program_id>/       Per-program casework (PRJ-HOL-FOUNDING-2026, PRJ-HOL-KIR-2026)
      Organisation/                  Personnel + resource governance (RESERVED scaffolding — baseline role)
      People Operations/             People-Operations Lead (post-I73)
        canonicals/                  ENGAGEMENT_MODEL_REGISTRY + recruiting SOPs (I73)
      Talent/                        People development
        Corporate Marketing/         (RESERVED scaffolding — baseline role)
        Ethics & Learning/           (RESERVED scaffolding — baseline role)
      programs/<program_id>/         Per-program casework (PRJ-HOL-KIR-2026)
    Research/                        Holistik Researcher (legacy tools-shed; CHARTERS now at top-level Research/)
      HUMINT Techniques/             Human intelligence collection
      Intelligence/                  Intel sub-discipline
        canonicals/                  GOI/POI doctrine + INTELLIGENCE_DISCIPLINE_CHARTER + …
      Intelligence Matrix/           Intel classification and fact management
      Methodology Pillars/           Process Eng, Business Eng, Foresight
      Deep Research/                 Multi-source synthesis and assessment
      Research Techniques/           HxPESTAL, 6Ws, analogies, briefs
      OSINT Operations/              Web intel, social media, publications
    Tech/                            CTO
      AI Engineer/                   AI systems + agent orchestration (RESERVED scaffolding — baseline role)
      DevOPS/                        Infrastructure + delivery
        Front-End/                   (RESERVED scaffolding)
        Back-End/                    (RESERVED scaffolding)
      System Owner/                  Platform + infrastructure ownership
        canonicals/                  4 MADEIRA SOPs + COMPONENT_SERVICE_MATRIX governance + …
        Domain Specialist/           Sub-role
        programs/<program_id>/       Per-program casework (PRJ-HOL-KIR-2026)
      Tech Lead/                     Technical leadership (RESERVED scaffolding — baseline role)
  AI/                                AI governance chain
    Susana Madeira/                  Named Holistika AI persona — RESERVED.md (I79 P5 cluster B)
    AIC/                             AI-in-Charge role-class — RESERVED.md (I79 P5 cluster B)
```

### Envoy Tech Lab (top-level — Entity: HLK Tech Lab)

```
Envoy Tech Lab/
  KiRBe/                             KiRBe platform documentation (vault-authored)
  MADEIRA/                           MADEIRA platform documentation (vault-authored)
  Neo4j/                             Neo4j strategy + agent-memory ADR
  Repositories/                      Canonical index of Holistika-tracked GitHub repos
    README.md                        Policy: pointer-first, submodule criteria
    REPOSITORIES_REGISTRY.md         Table: slug, URL, class, owner role, topic_ids
    EXTERNAL_REPO_CONTRACT_TEMPLATE.md
    _templates/                      Bless-pattern templates (CI workflows, issue templates, render config, …)
      ci/                            CI workflow templates (26 files)
      github-workflows/
      issue/                         Issue templates (3 files)
      render/                        Render deployment templates
    platform/                        Optional stubs for platform-class repos
    internal/                        Optional stubs for internal tooling repos
    client-delivery/                 Optional stubs for client-delivery repos
  Showcases/                         Tech lab showcase materials
```

### Research (top-level — Entity: Holistika; promoted post-I70 D-IH-70-S)

```
Research/
  canonicals/                        RESEARCH_AREA_CHARTER (top-level area charter)
  Methodology/                       Methodology discipline
    canonicals/                      METHODOLOGY_DISCIPLINE_CHARTER
  Intelligence/                      Intelligence discipline
    canonicals/                      INTELLIGENCE_DISCIPLINE_CHARTER + GOI_POI_STANCE_DOCTRINE
  Diagnosis/                         Diagnosis discipline
    canonicals/                      DIAGNOSIS_DISCIPLINE_CHARTER
  Validation/                        Validation discipline
    canonicals/                      VALIDATION_DISCIPLINE_CHARTER
```

### Think Big (Entity: Think Big)

Two physical roots per the [Workspace Blueprint](Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md): `Clients/` for **outbound** engagements where Holistika provides (customer, partner, product, and internal-capacity via the reserved `internal-` slug prefix); `Advisers/` for **inbound** engagements where Holistika is the customer of external advisers. `Projects/` was retired per D-W13-I (P13.5, 2026-05-11) — everything at Think Big is a project-shaped engagement under one of the two roots.

```
Think Big/
  README.md                          Scope: non-repo artifacts; two-root model; link to Envoy registry for code
  Clients/                           Outbound engagements (types 1 / 2 / 3 / 5); slug pattern <YYYY>-<slug>/ or <YYYY>-internal-<slug>/
    _engagement-template/            Literal copy-target for new outbound engagements (P13.3)
      00-internal/                   Operator-private notes
      01-operator-pack/              Operator working artefacts
      02-customer-pack/              Customer-facing deliverables
      _archive/                      Engagement archive
      _exports/                      Final exports
      _external_marks/               External brand-mark inventory
    2026-asesoria-hosteleria/        Live engagement
    2026-efa-collab/                 Live engagement
    2026-internal-service-management-ssot/  Internal-capacity engagement (per the 'internal-' prefix)
    2026-shadowgpu-inbound/          Live engagement
    2026-suez-webuy/                 Live engagement (largest archive)
    2026-websitz-rushly/             Live engagement
  Advisers/                          Inbound engagements (type 4); slug pattern <YYYY>-<slug>/
    _engagement-template/            Literal copy-target for new inbound engagements (P13.3)
      00-internal/                   Operator-private notes
      01-our-pack/                   Our prep artefacts
      02-adviser-pack/               Materials shared with adviser
      _archive/
      _exports/
    2026-holistika-incorporation/    Live adviser engagement (founder incorporation)
```

### `_assets/` (KM Output-1 binary visuals)

```
_assets/
  README.md                          Forward-layout contract
  _meta/                             Cross-asset graph + metadata (topic_graph.{mmd,svg,png})
  advops/                            ADVOPS plane assets
    PRJ-HOL-FOUNDING-2026/           Per-program assets (founder incorporation; ENISA evidence; adviser handoff)
      adviser_handoff/               Adviser-handoff topic with manifest
      enisa_company_dossier/         ENISA company dossier topic
      enisa_evidence/                ENISA evidence topic
    shared/                          Cross-program shared assets
      decks/                         Investor / sales / advisor / partner / recruiter decks + counterparty briefs + objections briefs
      email-signatures/
      engagement/
      onboarding/
      press-kit/
      proposals/
      sequences/                     Outbound sequence templates
      2026-suez-webuy/               Engagement-specific shared assets
  km-pilot/                          Pilot Output-1 bundle (rasters + manifests + stubs; 25 files)
  operations/
    shared/engagement/estimation/    Engagement estimation template
  pmo/                               PMO-plane SOP manifests (SOP-INITIATIVE_GOVERNANCE_001 + …)
  techops/                           TECHOPS-plane SOP manifests + topic assets
    PRJ-HOL-KIR-2026/                Per-program (KiRBe billing-plane routing topic + raster + manifest)
  touchpoint-kit/                    Per-persona × per-channel intro message templates (en/es)
    PERSONA-ADVISOR-REFERRAL/CHAN-EMAIL-INBOUND/
    PERSONA-CUSTOMER-KIRBE-PROSPECT/CHAN-WEB-FORM/
    PERSONA-IDEA-PROPOSER/CHAN-DIRECT-DM/
    PERSONA-INVESTOR-COLD/CHAN-LINKEDIN-DM/
    PERSONA-INVESTOR-WARM/CHAN-EMAIL-INBOUND/
    PERSONA-PARTNER-JOINT-EQUITY/CHAN-EMAIL-INBOUND/
    PERSONA-TALENT-INBOUND/CHAN-WEB-FORM/
    PERSONA-VENDOR-OUTBOUND/CHAN-DIRECT-DM/
```

## Cross-references

| Baseline | Location |
|----------|----------|
| Organisation roles | [baseline_organisation.csv](Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv) (65+ roles, 10 areas) |
| Process inventory | [process_list.csv](Admin/O5-1/People/Compliance/canonicals/process_list.csv) (paired SOP+runbook contract per `akos-executable-process-catalog.mdc`; `inherited_pattern_id` FK column post-I79 P6) |
| Component / service inventory (CTO SSOT) | [COMPONENT_SERVICE_MATRIX.csv](Admin/O5-1/People/Compliance/canonicals/techops/COMPONENT_SERVICE_MATRIX.csv) (relocated 2026-05-22 per **D-IH-81-G-T5**) |
| Access levels | [access_levels.md](Admin/O5-1/People/Compliance/canonicals/access_levels.md) (0-6) |
| Confidence levels | [confidence_levels.md](Admin/O5-1/People/Compliance/canonicals/confidence_levels.md) (Safe, Euclid, Keter) |
| Source taxonomy | [source_taxonomy.md](Admin/O5-1/People/Compliance/canonicals/source_taxonomy.md) (6 categories, 19 levels) |
| Precedence contract | [PRECEDENCE.md](Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md) |
| Canonical-asset path-mapping registry (post-I70 federation) | [CANONICAL_REGISTRY.csv](Admin/O5-1/People/Compliance/canonicals/CANONICAL_REGISTRY.csv) |
| Meta-SOP | [SOP-META_PROCESS_MGMT_001.md](Admin/O5-1/People/Compliance/canonicals/SOP-META_PROCESS_MGMT_001.md) |
| KM contract (Topic / Fact / Source, Output 1) | [HLK_KM_TOPIC_FACT_SOURCE.md](Admin/O5-1/People/Compliance/canonicals/HLK_KM_TOPIC_FACT_SOURCE.md) |
| GitHub repository index (Holistika-tracked) | [Envoy Tech Lab/Repositories/REPOSITORIES_REGISTRY.md](Envoy%20Tech%20Lab/Repositories/REPOSITORIES_REGISTRY.md) |
| Initiative registry (live + closed) | [INITIATIVE_REGISTRY.csv](Admin/O5-1/People/Compliance/canonicals/dimensions/INITIATIVE_REGISTRY.csv) |
| Decision register (D-IH-NN-X) | [DECISION_REGISTER.csv](Admin/O5-1/People/Compliance/canonicals/dimensions/DECISION_REGISTER.csv) |
| Operations register (OPS-NN-X) | [OPS_REGISTER.csv](Admin/O5-1/People/Compliance/canonicals/dimensions/OPS_REGISTER.csv) |
| Topic registry (KM Output-1) | [TOPIC_REGISTRY.csv](Admin/O5-1/People/Compliance/canonicals/dimensions/TOPIC_REGISTRY.csv) |
| GOI/POI register (knowledge dimension; raw mapping off-repo) | [GOI_POI_REGISTER.csv](Admin/O5-1/People/Compliance/canonicals/dimensions/GOI_POI_REGISTER.csv) |
| Persona registry | [PERSONA_REGISTRY.csv](Admin/O5-1/People/Compliance/canonicals/dimensions/PERSONA_REGISTRY.csv) |
| Skill registry | [SKILL_REGISTRY.csv](Admin/O5-1/People/Compliance/canonicals/dimensions/SKILL_REGISTRY.csv) |
| **People manifesto + design pattern library + agentic doctrine + breakthrough SOP (I79)** | [`Admin/O5-1/People/canonicals/`](Admin/O5-1/People/canonicals/) |
| **Tech Lab agentic framework landscape (I79 P3b)** | [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](Admin/O5-1/Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) |
| **Research area top-level charter (post-I70)** | [`RESEARCH_AREA_CHARTER.md`](Research/canonicals/RESEARCH_AREA_CHARTER.md) |
