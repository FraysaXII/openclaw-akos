# Holistika Knowledge Vault v3.0

**Version**: 3.0
**Date**: 2026-03-31
**Status**: Active canonical vault
**Governance**: [compliance/PRECEDENCE.md](../compliance/PRECEDENCE.md)

---

## Purpose

This is the active Holistika Knowledge Vault. It holds all canonical knowledge, SOPs, research outputs, project documents, and operational artifacts for the HLK ecosystem.

The folder structure mirrors the organisational hierarchy defined in [baseline_organisation.csv](../compliance/baseline_organisation.csv). Every document lives under the role that owns it.

## How to use this vault

### Adding a document

1. Identify the **role owner** from [baseline_organisation.csv](../compliance/baseline_organisation.csv).
2. Navigate to that role's folder under `Admin/O5-1/<area>/<role>/`.
3. Write the document as markdown.
4. If it is a formal process, add a row to [process_list.csv](../compliance/process_list.csv).
5. If it is an SOP, follow the [SOP-META envelope](../compliance/SOP-META_PROCESS_MGMT_001.md).

### Promotion ladder for sensitive casework

Use a staged promotion path for founder-governance and other sensitive business casework:

1. Keep raw evidence and exploratory interpretation outside the canonical vault or in `docs/wip/`.
2. Promote stable, role-owned case decisions into `v3.0/`.
3. Formalize repeatable behavior as SOPs.
4. Register only the repeatable process layer in [process_list.csv](../compliance/process_list.csv).
5. Update [baseline_organisation.csv](../compliance/baseline_organisation.csv) only if ownership itself changes.

Current examples:

- [Founder incorporation knowledge index](Admin/O5-1/People/Legal/FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md)
- [Founder governance document lifecycle](Admin/O5-1/People/Compliance/FOUNDER_GOVERNANCE_DOCUMENT_LIFECYCLE.md)

### Finding a document

- By role: navigate the folder tree below.
- By process: look up the `item_id` in [process_list.csv](../compliance/process_list.csv) and find its `role_owner`.
- By compliance classification: check [access_levels.md](../compliance/access_levels.md), [confidence_levels.md](../compliance/confidence_levels.md), or [source_taxonomy.md](../compliance/source_taxonomy.md).

### Knowledge management (Topic–Fact–Source, Output 1)

Holistika-wide KM is governed by [HLK_KM_TOPIC_FACT_SOURCE.md](../compliance/HLK_KM_TOPIC_FACT_SOURCE.md): **sources** (output types 0–4), **facts** (atomic, cited claims), **topics** (bundles and indexes), aligned to `artifact_role` and [PRECEDENCE.md](../compliance/PRECEDENCE.md).

| Need | Where |
|------|--------|
| Full contract (manifest fields, Obsidian tag vocabulary) | [HLK_KM_TOPIC_FACT_SOURCE.md](../compliance/HLK_KM_TOPIC_FACT_SOURCE.md) |
| Topic bundle template | [TOPIC_KNOWLEDGE_INDEX_TEMPLATE.md](Admin/O5-1/People/Compliance/TOPIC_KNOWLEDGE_INDEX_TEMPLATE.md) |
| Example visual manifest | [VISUAL_MANIFEST_EXAMPLE.manifest.md](Admin/O5-1/People/Compliance/VISUAL_MANIFEST_EXAMPLE.manifest.md) |
| PMO backlog index (Trello → topic_id; Trello not SSOT) | [RESEARCH_BACKLOG_TRELLO_REGISTRY.md](Admin/O5-1/Operations/PMO/RESEARCH_BACKLOG_TRELLO_REGISTRY.md) |
| Trello board JSON imports (primary + archive slices) | [imports/README.md](Admin/O5-1/Operations/PMO/imports/README.md) |
| WIP topic syntheses (interpretation layer) | [docs/wip/hlk-km/](../../../wip/hlk-km/) |
| Pilot Output 1 bundle (rasters + `*.manifest.md` + stubs) | [_assets/km-pilot/](_assets/km-pilot/) |
| Workspace roadmap / traceability | [master-roadmap.md](../../../wip/planning/hlk-km-knowledge-base/master-roadmap.md) |
| GitHub repository index (Holistika-tracked repos; GitHub is SSOT for code) | [Repositories/REPOSITORIES_REGISTRY.md](Envoy%20Tech%20Lab/Repositories/REPOSITORIES_REGISTRY.md) |

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
| MADEIRA | Reads registry CSVs for structure, markdown tree for content |

### Entity placement: Admin, Envoy Tech Lab, Think Big

- **Admin (`Admin/…`)** — Role-owned canonical knowledge: SOPs, internal programs (e.g. ENISA readiness), compliance, research methodology. Mirrors [baseline_organisation.csv](../compliance/baseline_organisation.csv).
- **Envoy Tech Lab** — **All GitHub repositories** Holistika tracks (platform, internal tools, client-delivery) are indexed in [Envoy Tech Lab/Repositories/](Envoy%20Tech%20Lab/Repositories/README.md). Vault markdown for KiRBe and MADEIRA continues under [Envoy Tech Lab/KiRBe/](Envoy%20Tech%20Lab/KiRBe/) and [Envoy Tech Lab/MADEIRA/](Envoy%20Tech%20Lab/MADEIRA/) unless a later migration consolidates paths. Default pattern: **registry pointer** to GitHub; submodules only when CI or pin requirements justify it (see Repositories README).
- **Think Big** — **Non-repository** client and program artifacts: commercials, SOWs, engagement memos, decks, and other deliverables that are not the Git root of a codebase. Link Think Big materials to repo rows and topic indexes in Envoy/PMO. See [Think Big/README.md](Think%20Big/README.md).

## Governance

- **Canonical baselines** live in [compliance/](../compliance/) (shared between v2.7 and v3.0).
- **Historical reference** lives in [Research & Logic/](../Research%20%26%20Logic/) (v2.7, read-only).
- **Active knowledge** lives here in `v3.0/` (edit here).
- See [PRECEDENCE.md](../compliance/PRECEDENCE.md) for the full precedence contract.

## Vault Structure

### Admin (Entity: Holistika)

```
Admin/
  O5-1/                          Chief Business Officer
    Research/                    Holistik Researcher (area head)
      HUMINT Techniques/         Human intelligence collection
      Intelligence Matrix/       Intel classification and fact management
      Methodology Pillars/       Process Eng, Business Eng, Foresight
      Deep Research/             Multi-source synthesis and assessment
      Research Techniques/       HxPESTAL, 6Ws, analogies, briefs
      OSINT Operations/          Web intel, social media, publications
    People/                      CPO
      Compliance/                Policy and methodology enforcement
      Organisation/              Personnel and resource governance
      Talent/                    People development
        Ethics & Learning/       Knowledge center and education
        Corporate Marketing/     Corporate voice in people strategy
      Legal/                     Legal counsel and specialists
    Operations/                  COO
      PMO/                       Project management office
      SMO/                       Service management office
    Finance/                     CFO
      Business Controller/       Strategic financial analysis
        Pricing/
        Taxes/
      Financial Controller/      Financial statement accountability
        Front Office/            O2C and PTP
    Marketing/                   CMO
      Brand/                     Brand identity and creative direction
        AV/
        Copywriter/
        Design/
        UX Designer/
      Growth/                    Growth strategy and acquisition
      Social/                    Social media management
        Community Manager/
        Paid Media Manager/
    Data/                        CDO
      Architecture/              Data structure and architecture
      Science/                   Data science and analytics
      Governance/                Data governance and quality
    Tech/                        CTO
      DevOPS/                    Infrastructure and delivery
        Front-End/
        Back-End/
      System Owner/              Platform and infrastructure ownership
        Domain Specialist/
      AI Engineer/               AI systems and agent orchestration
      Tech Lead/                 Technical leadership
  AI/                            AI governance chain
    Susana Madeira/              AI persona with admin privileges
    AIC/                         AI agent execution role
```

### Envoy Tech Lab (Entity: HLK Tech Lab / Envoy Tech)

```
Envoy Tech Lab/
  Repositories/                   Canonical index of Holistika-tracked GitHub repos
    README.md                     Policy: pointer-first, submodule criteria
    REPOSITORIES_REGISTRY.md      Table: slug, URL, class, owner role, topic_ids
    platform/                     Optional stubs for platform-class repos
    internal/                     Optional stubs for internal tooling repos
    client-delivery/              Optional stubs for client-delivery repos
  KiRBe/                          KiRBe platform documentation (vault-authored)
  MADEIRA/                        MADEIRA platform documentation (vault-authored)
  Showcases/                      Tech lab showcase materials
```

### Think Big (Entity: Think Big)

```
Think Big/
  README.md                       Scope: non-repo artifacts; link to Envoy registry for code
  Projects/                       Client and internal project documentation (non-repo)
  Clients/                        Client-specific materials (non-repo)
```

## Cross-references

| Baseline | Location |
|----------|----------|
| Organisation roles | [baseline_organisation.csv](../compliance/baseline_organisation.csv) (65 roles, 10 areas) |
| Process inventory | [process_list.csv](../compliance/process_list.csv) (324 items, 11 projects) |
| Access levels | [access_levels.md](../compliance/access_levels.md) (0-6) |
| Confidence levels | [confidence_levels.md](../compliance/confidence_levels.md) (Safe, Euclid, Keter) |
| Source taxonomy | [source_taxonomy.md](../compliance/source_taxonomy.md) (6 categories, 19 levels) |
| Precedence contract | [PRECEDENCE.md](../compliance/PRECEDENCE.md) |
| Meta-SOP | [SOP-META_PROCESS_MGMT_001.md](../compliance/SOP-META_PROCESS_MGMT_001.md) |
| KM contract (Topic / Fact / Source, Output 1) | [HLK_KM_TOPIC_FACT_SOURCE.md](../compliance/HLK_KM_TOPIC_FACT_SOURCE.md) |
| GitHub repository index (Holistika-tracked) | [Envoy Tech Lab/Repositories/REPOSITORIES_REGISTRY.md](Envoy%20Tech%20Lab/Repositories/REPOSITORIES_REGISTRY.md) |
