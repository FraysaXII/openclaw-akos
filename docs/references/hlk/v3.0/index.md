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

### Finding a document

- By role: navigate the folder tree below.
- By process: look up the `item_id` in [process_list.csv](../compliance/process_list.csv) and find its `role_owner`.
- By compliance classification: check [access_levels.md](../compliance/access_levels.md), [confidence_levels.md](../compliance/confidence_levels.md), or [source_taxonomy.md](../compliance/source_taxonomy.md).

### Platform compatibility

| Platform | How to use |
|----------|------------|
| Obsidian | Open `docs/references/hlk/v3.0/` as a vault |
| Google Drive | Sync this folder; structure maps 1:1 to Drive folders |
| SharePoint | Same folder mapping |
| Git / GitHub | Already versioned in the openclaw-akos repo |
| KiRBe | Ingest as a source; CSVs provide the graph structure |
| MADEIRA | Reads registry CSVs for structure, markdown tree for content |

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
  KiRBe/                         KiRBe platform documentation
  MADEIRA/                        MADEIRA platform documentation
  Showcases/                      Tech lab showcase materials
```

### Think Big (Entity: Think Big)

```
Think Big/
  Projects/                       Client and internal project documentation
  Clients/                        Client-specific materials
```

## Cross-references

| Baseline | Location |
|----------|----------|
| Organisation roles | [baseline_organisation.csv](../compliance/baseline_organisation.csv) (65 roles, 10 areas) |
| Process inventory | [process_list.csv](../compliance/process_list.csv) (317 items, 11 projects) |
| Access levels | [access_levels.md](../compliance/access_levels.md) (0-6) |
| Confidence levels | [confidence_levels.md](../compliance/confidence_levels.md) (Safe, Euclid, Keter) |
| Source taxonomy | [source_taxonomy.md](../compliance/source_taxonomy.md) (6 categories, 19 levels) |
| Precedence contract | [PRECEDENCE.md](../compliance/PRECEDENCE.md) |
| Meta-SOP | [SOP-META_PROCESS_MGMT_001.md](../compliance/SOP-META_PROCESS_MGMT_001.md) |
