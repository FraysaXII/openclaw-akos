---
title: Methodology discipline — index (how we research)
language: en
intellectual_kind: discipline_index
sharing_label: internal_only
audience: J-OP;J-AIC
role_owner: KM Officer + Research Analyst
status: active
authored: 2026-05-29
last_review: 2026-05-29
last_review_decision_id: D-IH-75-G
---

# Methodology — discipline index

> **The discipline of _how_ we research.** Methodology sets the requirement that opens every
> research action, owns the craft of every lifecycle stage, and owns the **RECALL** discipline
> (how we retrieve what we know). Constitution: [`canonicals/METHODOLOGY_DISCIPLINE_CHARTER.md`](canonicals/METHODOLOGY_DISCIPLINE_CHARTER.md).
> Area spine: [`../canonicals/RESEARCH_LIFECYCLE_DOCTRINE.md`](../canonicals/RESEARCH_LIFECYCLE_DOCTRINE.md).

## Lifecycle ownership

Methodology is the cross-stage craft: **+ requirement** at ACQUIRE, **+ craft** at PROCESS, **+
packaging** at SHARE, and **`++` primary** at RECALL (the derived-recall principle). It is the
discipline that makes the other three repeatable.

## Sub-areas (the three crafts of method)

| Sub-area | What lives here | Index |
|:---|:---|:---|
| **Pillars** | The foundational research moves applied across every engagement. | [`Pillars/README.md`](Pillars/README.md) |
| **Techniques** | The concrete per-pillar moves (the toolbox). | [`Techniques/README.md`](Techniques/README.md) |
| **Deep-Research** | The long-cycle investigation apparatus + research-material pipeline. | [`Deep-Research/README.md`](Deep-Research/README.md) |

These three sub-areas are **realized** (this build) — they index the real capability rows in
[`CAPABILITY_REGISTRY.csv`](../../Admin/O5-1/People/Compliance/canonicals/dimensions/CAPABILITY_REGISTRY.csv)
(filter `area = Research`, roles Lead Researcher + Holistik Researcher). They replace the empty
`Admin/O5-1/Research/Methodology Pillars/` + `Research Techniques/` + `Deep Research/` husks
(deleted per `D-IH-75-G`; the husks held no content — the content was always in the registry).

## Active doctrines + SOPs (the method canon)

| Artefact | What it governs | Path (migration pending per §below) |
|:---|:---|:---|
| Research Action discipline | The 8-stage ingest->govern loop (ACQUIRE->PROCESS). | [`canonicals/RESEARCH_ACTION_DISCIPLINE.md`](canonicals/RESEARCH_ACTION_DISCIPLINE.md) |
| Research Radar discipline | The freshness/time axis before govern. | [`canonicals/RESEARCH_RADAR_DISCIPLINE.md`](canonicals/RESEARCH_RADAR_DISCIPLINE.md) |
| Research Action SOP | AC-HUMAN walkthrough of the 8 stages. | `../../Admin/O5-1/Research/Methodology/canonicals/SOP-RESEARCH_ACTION_001.md` |
| Research Radar SOP | The sweep cadence. | `../../Admin/O5-1/Research/Methodology/canonicals/SOP-RESEARCH_RADAR_001.md` |
| Substrate landscape doctrine | The technical-substrate audit doctrine. | `../../Admin/O5-1/Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md` |
| Substrate audit cadence SOP | Per-substrate audit cadence. | `../../Admin/O5-1/Research/Methodology/canonicals/SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md` |

**Migration note.** The SOPs + substrate doctrine still physically live under the legacy
`Admin/O5-1/Research/Methodology/canonicals/` path. Their move into this tree is a separate,
gated mechanical follow-up (it ripples into cursor-rule globs + PRECEDENCE rows + validator
references, so it is not bundled into this area-logic build). See the
[migration proposal](../../../../../wip/intelligence/legacy-research-admin-migration-proposal-2026-05-29.md).

## Cross-references

- Area anchor: [`../README.md`](../README.md) · Lifecycle spine: [`../canonicals/RESEARCH_LIFECYCLE_DOCTRINE.md`](../canonicals/RESEARCH_LIFECYCLE_DOCTRINE.md).
- Sister disciplines: [Intelligence](../Intelligence/README.md) · [Diagnosis](../Diagnosis/README.md) · [Validation](../Validation/README.md).
- Initiative: [I75 Research area governance](../../../../../wip/planning/75-research-area-governance/master-roadmap.md) P1 (Methodology SOP buildout).
