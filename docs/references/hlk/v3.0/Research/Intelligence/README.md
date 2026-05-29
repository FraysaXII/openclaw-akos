---
title: Intelligence discipline — index (what we collect)
language: en
intellectual_kind: discipline_index
sharing_label: internal_only
audience: J-OP;J-AIC
role_owner: Research Analyst + KM Officer
status: active
authored: 2026-05-29
last_review: 2026-05-29
last_review_decision_id: D-IH-75-G
---

# Intelligence — discipline index

> **The discipline of _what_ we collect.** Intelligence owns **ACQUIRE** (human + open-source
> collection), begins **PROCESS** (classification into the matrix), and holds the Research side of
> **PROTECT** (source protection + GOI/POI stance). Constitution:
> [`canonicals/INTELLIGENCE_DISCIPLINE_CHARTER.md`](canonicals/INTELLIGENCE_DISCIPLINE_CHARTER.md).
> Area spine: [`../canonicals/RESEARCH_LIFECYCLE_DOCTRINE.md`](../canonicals/RESEARCH_LIFECYCLE_DOCTRINE.md).

## Lifecycle ownership

**`++` primary at ACQUIRE** (HUMINT + OSINT) + **+ classify** at PROCESS + **+ source protection**
at PROTECT. Source categories are governed by
[`source_taxonomy.md`](../../Admin/O5-1/People/Compliance/canonicals/source_taxonomy.md)
(OSINT / HUMINT / SIGINT / CORPINT / MOTINT).

## Sub-areas (the collection crafts)

| Sub-area | Source category | Index |
|:---|:---|:---|
| **HUMINT** | Human Intelligence — elicitation from human sources. | [`HUMINT/README.md`](HUMINT/README.md) |
| **OSINT** | Open Source Intelligence — public-source investigation. | [`OSINT/README.md`](OSINT/README.md) |
| **Matrix** | The Intelligence Matrix — classify, score, and place collected intel. | [`Matrix/README.md`](Matrix/README.md) |

**Realized** (this build) — each indexes real capability rows in
[`CAPABILITY_REGISTRY.csv`](../../Admin/O5-1/People/Compliance/canonicals/dimensions/CAPABILITY_REGISTRY.csv)
(roles HUMINT Specialist / OSINT Analyst / Intelligence Analyst). They replace the empty
`Admin/O5-1/Research/HUMINT Techniques/` + `OSINT Operations/` + `Intelligence Matrix/` husks
(deleted per `D-IH-75-G`).

## Active SOPs + register (the intelligence canon)

| Artefact | What it governs | Path (migration pending) |
|:---|:---|:---|
| IntelligenceOps register | The live "Intelligence Matrix" — collection contracts vs named targets, with per-target freshness. | `../../Admin/O5-1/Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv` |
| Elicitation SOP | HUMINT elicitation discipline. | `../../Admin/O5-1/Research/Intelligence/canonicals/SOP-IO_ELICITATION_DISCIPLINE_001.md` |
| Intelligence report SOP | Per-engagement report authoring (a SHARE product). | `../../Admin/O5-1/Research/Intelligence/canonicals/SOP-IO_INTELLIGENCE_REPORT_001.md` |
| Regulator relationship SOP | Regulator-facing collection + relationship. | `../../Admin/O5-1/Research/Intelligence/canonicals/SOP-REGULATOR_RELATIONSHIP_001.md` |
| Research engagement trigger SOP | When an engagement triggers a collection cycle. | `../../Admin/O5-1/Research/Intelligence/canonicals/SOP-RESEARCH_ENGAGEMENT_TRIGGER_001.md` |
| GOI/POI stance doctrine | Who we watch / who may watch us (PROTECT). | [`canonicals/GOI_POI_STANCE_DOCTRINE.md`](canonicals/GOI_POI_STANCE_DOCTRINE.md) |

**Migration note.** The IntelligenceOps register is an **SSOT CSV**; relocating it changes a
canonical path and must update PRECEDENCE + validators + Pydantic FIELDNAMES + the Supabase mirror
emit in one commit. That move is a separate gated follow-up, not part of this area-logic build. See
the [migration proposal](../../../../../wip/intelligence/legacy-research-admin-migration-proposal-2026-05-29.md).

## Cross-references

- Area anchor: [`../README.md`](../README.md) · Lifecycle spine: [`../canonicals/RESEARCH_LIFECYCLE_DOCTRINE.md`](../canonicals/RESEARCH_LIFECYCLE_DOCTRINE.md).
- PROTECT join: People/Ethics (red lines) + People/Compliance (access + confidence + redaction) — see lifecycle doctrine §6.3.
- Sister disciplines: [Methodology](../Methodology/README.md) · [Diagnosis](../Diagnosis/README.md) · [Validation](../Validation/README.md).
- Initiative: [I75 Research area governance](../../../../../wip/planning/75-research-area-governance/master-roadmap.md) P2 (Intelligence SOP buildout).
