---
title: Research area — read this first (area-identity anchor)
language: en
intellectual_kind: area_identity_anchor
sharing_label: internal_only
audience: J-OP;J-AIC
authored: 2026-05-29
last_review: 2026-05-29
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
**full information lifecycle** — **acquire → share → process → store → recall → protect** —
over a *variety* of subjects, each with owners, topics, data models, surfaces/channels/
audiences, use-cases/projects/programs, and process-discovery→implementation.

It is **NOT** a flat queue of research-actions. "Research Action"
([`RESEARCH_ACTION_DISCIPLINE.md`](Methodology/canonicals/RESEARCH_ACTION_DISCIPLINE.md), the
15th Quality-Fabric specialty) is **one discipline covering the ACQUIRE/PROCESS slice** — do
not mistake it for the whole area.

## 2. The four disciplines (the area's spine)

| Discipline | "Question" | Home |
|:---|:---|:---|
| **Methodology** | *how* we research | [`Methodology/canonicals/`](Methodology/canonicals/) (METHODOLOGY + RESEARCH_ACTION + Research Radar when minted) |
| **Intelligence** | *what* we collect | [`Intelligence/canonicals/`](Intelligence/canonicals/) (INTELLIGENCE charter + GOI/POI stance; IntelligenceOps register/SOPs) |
| **Diagnosis** | *what's wrong* | [`Diagnosis/canonicals/`](Diagnosis/canonicals/) |
| **Validation** | *what's true* | [`Validation/canonicals/`](Validation/canonicals/) |

Area charter: [`canonicals/RESEARCH_AREA_CHARTER.md`](canonicals/RESEARCH_AREA_CHARTER.md).

## 3. The CORPINT lifecycle map (and where it's thin)

| Stage | Built? | Primary homes |
|:---|:---|:---|
| **ACQUIRE** (intake/collection) | strong | Research Action; IntelligenceOps; source ledgers; substrate audit; Trello backlog |
| **PROCESS** (synthesize/validate) | moderate | Research Action govern; Validation; Diagnosis; synthesis prongs |
| **STORE** (KB/KiRBe) | moderate | KM Topic–Fact–Source + TOPIC_REGISTRY; KiRBe (I83); Neo4j |
| **SHARE / OUTAKE** (dissemination) | **THIN — gap** | external-render + brand dual-register + audience/channel registries (sister-area; **no Research-owned outake doctrine yet**) |
| **RECALL** (retrieval/search) | **THIN — gap** | derived-recall principle; Neo4j/MCP; **no governed recall discipline** |
| **PROTECT** (counter-intelligence) | **THIN — gap** | access levels + confidence + GOI/POI stance + redaction; **no counter-intelligence doctrine** |

The three thin stages (**OUTAKE, RECALL, PROTECT**) are the named forward work — see the
[Wave R+5 plan](../../../../wip/planning/86-initiative-cluster-execution-coordinator/tranches/wave-r-plus-5-research-radar-and-governance-integrity.md).

## 4. Where things live (the homes I kept getting wrong)

- **Canonical (SSOT):** `docs/references/hlk/v3.0/Research/<discipline>/canonicals/`. New
  research disciplines (e.g. Research Radar) land here as **Methodology siblings**.
- **Tier-1 WIP (Research-owned, cross-area):** [`docs/wip/intelligence/`](../../../../wip/intelligence/README.md)
  — this is **correct by design** (`D-IH-70-O` + [blueprint](../Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §17).
  **Do NOT move/rename it** without a deliberate topology decision superseding `D-IH-70-O`.
- **Operational / legacy:** `docs/references/hlk/v3.0/Admin/O5-1/Research/` (technique folders +
  some IntelligenceOps SOPs) — **mid-migration** into the top-level tree (P4.5).
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
