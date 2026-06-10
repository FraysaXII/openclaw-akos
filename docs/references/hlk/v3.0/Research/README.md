---
title: Research area — read this first (area-identity anchor)
language: en
intellectual_kind: area_identity_anchor
sharing_label: internal_only
audience: J-OP;J-AIC
authored: 2026-05-29
last_review: 2026-05-29
last_review_decision_id: D-IH-75-G
role_owner: Research Director (KM Officer steward; PMO/Founder interim)
status: active
---

# Research — area-identity anchor

> **Read this before touching anything "research."** This page exists because agents
> repeatedly forgot what the Research area *is* and where its pieces live — re-deriving
> it from scratch (expensively) or drifting into rogue folders. This is the cheap,
> reliable map so that does not recur. Paired with the scoped rule
> [`akos-research-area.mdc`](../../../../../.cursor/rules/akos-research-area.mdc), which loads
> this whenever a Research surface is touched.

## 1. What Research IS (the one-liner that prevents the drift)

Research is **Holistika's corporate-intelligence (CORPINT) operating system** across the
**full information lifecycle** — **acquire → process → store ⇄ recall → share**, guarded by
**protect** — over a *variety* of subjects, each with owners, topics, data models,
surfaces/channels/audiences, use-cases/projects/programs, and process-discovery→implementation.

The **organizing spine** of the area is that lifecycle, defined in
[`canonicals/RESEARCH_LIFECYCLE_DOCTRINE.md`](canonicals/RESEARCH_LIFECYCLE_DOCTRINE.md)
(founder-ratified logic change `D-IH-75-G`, 2026-05-29): the six lifecycle stages are the spine,
the four disciplines (§2) are the *crafts* that move information through it, and the points where
the lifecycle crosses into a sister area are first-class **cross-area joins** (§3). Read the
lifecycle doctrine first — it is the operating logic this whole map hangs on.

It is **NOT** a flat queue of research-actions. "Research Action"
([`RESEARCH_ACTION_DISCIPLINE.md`](Methodology/canonicals/RESEARCH_ACTION_DISCIPLINE.md), the
15th Quality-Fabric specialty) is **one discipline covering the ACQUIRE/PROCESS slice** — do
not mistake it for the whole area.

## 2. The four disciplines (the area's _crafts_ — they move information through the spine)

| Discipline | "Question" | Primary lifecycle stage | Index |
|:---|:---|:---|:---|
| **Methodology** | *how* we research | requirement + craft of all stages + RECALL | [`Methodology/README.md`](Methodology/README.md) |
| **Intelligence** | *what* we collect | ACQUIRE (HUMINT/OSINT) + classify | [`Intelligence/README.md`](Intelligence/README.md) |
| **Diagnosis** | *what's wrong* | PROCESS (the verdict layer) | [`Diagnosis/README.md`](Diagnosis/README.md) |
| **Validation** | *what's true* | PROCESS (the truth-gate) | [`Validation/README.md`](Validation/README.md) |

Each discipline index lists its sub-areas, capability rows, and SOPs. The full discipline ×
lifecycle map (who owns which stage) is the matrix in
[`canonicals/RESEARCH_LIFECYCLE_DOCTRINE.md`](canonicals/RESEARCH_LIFECYCLE_DOCTRINE.md) §4.
Area charter: [`canonicals/RESEARCH_AREA_CHARTER.md`](canonicals/RESEARCH_AREA_CHARTER.md).

## 3. The CORPINT lifecycle map (the spine — every stage now has an owner)

The previous draft of this map left three stages "thin — gap." The lifecycle doctrine
([`canonicals/RESEARCH_LIFECYCLE_DOCTRINE.md`](canonicals/RESEARCH_LIFECYCLE_DOCTRINE.md))
closed them: SHARE / RECALL / PROTECT are no longer homeless — they are **named cross-area joins**
(Research authors its side; a sister area owns the surface).

| Stage | Owner | Cross-area join |
|:---|:---|:---|
| **ACQUIRE** (collection) | Research/Intelligence (HUMINT/OSINT) `++` | Operations feeds the engagement-trigger need |
| **PROCESS** (analyse/validate) | Research/Diagnosis + Validation `++` | — |
| **STORE** (durable memory) | Research authors; **Tech owns the store** | KM Topic–Fact–Source; Neo4j; KiRBe (I83) |
| **RECALL** (retrieval) | Research/Methodology owns the recall *discipline* | **Tech** owns the retrieval *infra* (Neo4j/MCP/search) |
| **SHARE / OUTAKE** (dissemination) | Research authors the internal-register product | **Marketing/Brand** (dual-register) + **External-Render** deliver |
| **PROTECT** (counter-intelligence) | Research/Intelligence (source protection + GOI/POI) | **People/Ethics** (red lines) + **People/Compliance** (access/confidence/redaction) |

The genuinely new claim is **PROTECT** as a first-class stage with a cross-area ownership triad
(`D-IH-75-H`); a full Counter-Intelligence discipline mint is forward-chartered (co-ratified by
People/Ethics + Compliance). Remaining forward work is tracked in the
[Wave R+5 plan](../../../../wip/planning/86-initiative-cluster-execution-coordinator/tranches/wave-r-plus-5-research-radar-and-governance-integrity.md)
+ [I75 P1–P4](../../../../wip/planning/75-research-area-governance/master-roadmap.md).

## 4. Where things live (the homes I kept getting wrong)

- **Canonical (SSOT):** `docs/references/hlk/v3.0/Research/<discipline>/canonicals/`. New
  research disciplines (e.g. Research Radar) land here as **Methodology siblings**.
- **Discipline indexes + technique sub-areas:** each discipline has a `README.md` index, and
  Methodology + Intelligence carry **realized** technique sub-folders
  (`Methodology/{Pillars,Techniques,Deep-Research}/` + `Intelligence/{HUMINT,OSINT,Matrix}/`),
  each indexing real capability rows. These replaced the empty `Admin/` technique husks per
  `D-IH-75-G` (the husks held no content — the content was always in the capability registry).
- **Tier-1 WIP (Research-owned, cross-area):** [`docs/wip/intelligence/`](../../../../wip/intelligence/README.md)
  — this is **correct by design** (`D-IH-70-O` + [blueprint](../Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §17).
  **Do NOT move/rename it** without a deliberate topology decision superseding `D-IH-70-O`.
- **Executable SSOT (post OPS-86-26, 2026-06-10):** Intelligence + Methodology **SOPs**, substrate
  doctrine, entity rationale, and `INTELLIGENCEOPS_REGISTER.csv` live under this top-level tree.
  Legacy `Admin/O5-1/Research/` is **empty/removed** after the migration bundle.
- **Topic SSOT:** `…/People/Compliance/canonicals/dimensions/TOPIC_REGISTRY.csv`; Trello backlog
  index at `…/Operations/PMO/RESEARCH_BACKLOG_TRELLO_REGISTRY.md` (Trello = evidence, not SSOT).

## 5. Do / Don't (the anti-amnesia rules)

- **DO** treat Research as the CORPINT lifecycle (§3), with owners + topics, not a research-action queue.
- **DO** put new research-discipline canonicals under `v3.0/Research/<discipline>/canonicals/`.
- **DON'T** invent a new generic `docs/wip/<name>/` home for research WIP — `docs/wip/intelligence/` is it.
- **DON'T** physically move `docs/wip/intelligence/` (it contradicts the ratified topology).
- **DON'T** mistake Research Action (intake) for the whole area.

## 6. Cross-references

- Area charter: [`RESEARCH_AREA_CHARTER.md`](canonicals/RESEARCH_AREA_CHARTER.md).
- Scoped rule (loads this anchor on Research surfaces): [`akos-research-area.mdc`](../../../../../.cursor/rules/akos-research-area.mdc).
- Research Radar (freshness / time axis): [`charter`](../../../../wip/intelligence/research-radar-2026-05-29/charter-2026-05-29.md) + [`regression`](../../../../wip/intelligence/research-radar-2026-05-29/regression-2026-05-29.md).
- Harmonization plan: [`Wave R+5`](../../../../wip/planning/86-initiative-cluster-execution-coordinator/tranches/wave-r-plus-5-research-radar-and-governance-integrity.md).
- Tier-1 WIP home: [`docs/wip/intelligence/README.md`](../../../../wip/intelligence/README.md).
- Area-governance initiative: [`I75`](../../../../wip/planning/75-research-area-governance/master-roadmap.md).
