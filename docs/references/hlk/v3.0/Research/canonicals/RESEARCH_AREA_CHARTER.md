---
language: en
status: active
canonical: true
role_owner: Research Director + KM Officer
classification: way_of_working
intellectual_kind: area_charter
ssot: true
authored: 2026-05-12
last_review: 2026-05-12
companion_to:
  - ../../Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md
  - ./Methodology/canonicals/METHODOLOGY_DISCIPLINE_CHARTER.md
  - ./Intelligence/canonicals/INTELLIGENCE_DISCIPLINE_CHARTER.md
  - ./Diagnosis/canonicals/DIAGNOSIS_DISCIPLINE_CHARTER.md
  - ./Validation/canonicals/VALIDATION_DISCIPLINE_CHARTER.md
---

# RESEARCH_AREA_CHARTER — Research as new top-level area (R2 design)

> Research promotes from `Admin/O5-1/Research/` sub-area to **`v3.0/Research/`** top-level area per **D-IH-70-S** (ratified 2026-05-12) + Conundrum 11. Four disciplines: **Methodology / Intelligence / Diagnosis / Validation** mirror the Brand sub-discipline ontology. Cross-cutting roles: Research Director + Research Analyst + KM Officer + Holistik Researcher. **Research owns Tier 1 of the 3-tier WIP topology** (`docs/wip/intelligence/`).

## 1. Why a top-level area

Pre-I70, Research was a sub-area under `Admin/O5-1/Research/` with scattered technique folders (Methodology Pillars, Research Techniques, HUMINT, OSINT, Deep Research, Intelligence Matrix). The structure read as a tools-shed — not a discipline. Three signals forced the promotion:

1. **Cross-area scope.** Research feeds Marketing (audience analysis), Operations (engagement intelligence), People (founder corpus + ethics research), Tech (technical due diligence on stack choices) — a sub-area buried under Admin/O5-1 mis-states its load-bearing role.
2. **WIP topology demands ownership.** `docs/wip/intelligence/` (Tier 1 per WORKSPACE_BLUEPRINT §17) is cross-area research staging; it needed an explicit top-level home to own it.
3. **MADEIRA productization vector.** Per D-IH-70-V forward-context, the agent-companion pattern (today's Cursor-agent operational pattern; tomorrow's MADEIRA L6 founder-companion) is itself a Research output — methodology + intelligence + diagnosis + validation are the four moves the agent makes alongside the operator.

## 2. Four disciplines (R2 design — mirrors Brand sub-discipline ontology)

| Discipline | One-sentence definition | Owns | Outputs |
|:---|:---|:---|:---|
| **Methodology** | The discipline of *how we research*. | Methodology Pillars, Research Techniques, Deep Research (technique craft) | RESEARCH_METHODOLOGY_DISCIPLINE.md (TBD); methodology-pillar canonicals; per-pillar SOPs |
| **Intelligence** | The discipline of *what we collect*. | HUMINT Techniques, OSINT Operations, Intelligence Matrix, IntelligenceOps SOPs (post P4.5 wave 3 migration) | INTELLIGENCE_DISCIPLINE_CHARTER.md (this commit, stub); per-source-type SOPs; intelligence-collection cadence |
| **Diagnosis** | The discipline of *what's wrong* (counterparty / system / engagement). | Engagement-as-org-diagnostic pattern (F-51); counterparty baseline reality assessment; system-health diagnosis | DIAGNOSIS_DISCIPLINE_CHARTER.md (this commit, stub); per-engagement diagnostic templates |
| **Validation** | The discipline of *what's true* (post-elicitation, post-analysis). | Source reliability grading; cross-source corroboration; evidence-confidence scoring | VALIDATION_DISCIPLINE_CHARTER.md (this commit, stub); confidence_levels.md (cross-link); validation gates |

These four disciplines mirror the Brand sub-discipline ontology (Brand: AV / Copywriter / Design / UX-Designer; Research: Methodology / Intelligence / Diagnosis / Validation). Each is a craft with its own techniques + SOPs + output formats.

## 3. Roles (cross-cutting across disciplines)

| Role | Discipline-coverage | Reports to | Notes |
|:---|:---|:---|:---|
| **Research Director** | All 4 disciplines (governance + cross-area orchestration) | Founder | New role; baseline_organisation.csv addition deferred to P8 §8.5 |
| **Research Analyst** | Methodology + Intelligence (primary); Diagnosis + Validation (secondary) | Research Director | Existing roles in baseline; expanded scope |
| **KM Officer** | Methodology + Validation (primary); curation across all 4 | Research Director | Owns Tier 1 WIP curation per blueprint §17 |
| **Holistik Researcher** | Discipline-specific per cohort (Trainee level access; expand on graduation) | Research Director / mentor | Per D-IH-70-M: role row + cohort tag; curriculum deferred to I73 |

## 4. Existing technique folders mapping (pre-migration view)

The existing `Admin/O5-1/Research/` sub-folders map to disciplines as follows. **Migration of these folders to `v3.0/Research/<discipline>/` is part of P4.5 Wave 3** (deferred to operator-driven migration session per session checkpoint). This charter authors at the new top-level NOW; folder migration follows.

| Existing folder | Target discipline | Target path |
|:---|:---|:---|
| `Admin/O5-1/Research/Methodology Pillars/` | Methodology | `v3.0/Research/Methodology/Pillars/` |
| `Admin/O5-1/Research/Research Techniques/` | Methodology | `v3.0/Research/Methodology/Techniques/` |
| `Admin/O5-1/Research/Deep Research/` | Methodology + Validation (split on technique vs assessment) | `v3.0/Research/Methodology/Deep-Research/` (technique side) + cross-link from `Validation/` |
| `Admin/O5-1/Research/HUMINT Techniques/` | Intelligence | `v3.0/Research/Intelligence/HUMINT/` |
| `Admin/O5-1/Research/OSINT Operations/` | Intelligence | `v3.0/Research/Intelligence/OSINT/` |
| `Admin/O5-1/Research/Intelligence Matrix/` | Intelligence | `v3.0/Research/Intelligence/Matrix/` |
| `Admin/O5-1/Research/RESEARCH_VS_TECH_LAB_ENTITY_RATIONALE_2026-04.md` | Methodology (architectural rationale) | `v3.0/Research/canonicals/RESEARCH_VS_TECH_LAB_ENTITY_RATIONALE_2026-04.md` |
| `Admin/O5-1/Operations/IntelligenceOps/SOP-IO_*` (4 SOPs) | Intelligence | `v3.0/Research/Intelligence/canonicals/SOP-IO_*` (per D-IH-70-W ratification) |

**Diagnosis** has no pre-existing folder content; it's a new discipline created by P4.7 (formalizing the engagement-as-org-diagnostic pattern that has been implicit in P13's I12 SUEZ engagement work).

## 5. Tier 1 WIP ownership (per blueprint §17)

Research owns `docs/wip/intelligence/` as Tier 1 (cross-area research staging). Concretely:

- **Curation**: KM Officer reviews Tier 1 contents weekly; flags overdue WIP per timeboxing rules (SOP-WIP_LIFECYCLE_001 reserved for I71).
- **Promotion gate**: Tier 1 → canonical promotion (per blueprint §13 4-step ladder) is approved by Research Director (with founder consultation for cross-area-impact promotions).
- **Engagement WIP**: per-engagement intelligence folders (e.g., `2026-05-10-suez-webuy-procure-to-pay/`) are Tier 1 by default; promote to canonical at engagement-completion only.

## 6. Cross-area boundaries (single-ownership preserved)

To prevent dilution with existing areas:

- **Marketing/Brand sub-disciplines** (Brand/AV/Copywriter/Design/UX-Designer) own brand-prose research, voice register, anti-AI-tone tics. Research/Intelligence collects audience-analysis source material; Marketing/Brand authors the prose register on top.
- **Operations/PMO** owns initiative orchestration (Tier 2 WIP; planning packets). Research/Methodology authors how-to-do-research; PMO orchestrates when-and-where research lands.
- **People/Compliance** owns identity / behavior / authorization compliance; Research/Validation cross-supports with reliability grading + source confidence.
- **Tech/System Owner** owns architectural decisions; Research/Intelligence supports tech due diligence.

**Authoring vs consuming rule** (mirrors P2.5 D-IH-70-X Storytelling/Resonance pattern): Research AUTHORS investigative artifacts (intelligence reports, methodology pillars, diagnostic templates, validation rubrics); other areas CONSUME those artifacts as inputs to their own work. Single-ownership preserved by separating verbs.

## 7. UAT acceptance criteria

- All 4 discipline charter stubs exist at `v3.0/Research/<discipline>/canonicals/<DISCIPLINE>_CHARTER.md`.
- This `RESEARCH_AREA_CHARTER.md` exists at `v3.0/Research/canonicals/`.
- `docs/wip/intelligence/` has a top-level README declaring Research ownership (forward note; ships with this commit).
- Cross-links from `Admin/O5-1/Research/` sub-folders forward-link to the new home (P4.5 wave 3 will execute the actual move).
- `baseline_organisation.csv` Research Director role addition deferred to P8 §8.5 (People restructure tranche).

## 8. Cross-references

- [`../../Admin/O5-1/People/canonicals/RESEARCH_HEAD_DISCIPLINE.md`](../../Admin/O5-1/People/canonicals/RESEARCH_HEAD_DISCIPLINE.md) — Research-Head meta-discipline of research-first canonical authoring (I86 Wave H Lane D; People canonical per `D-IH-86-RH-A`).
- **D-IH-70-S** — Research as new top-level area: see [`docs/wip/planning/70-holistika-os-self-governance/reports/p3-topology-decisions-pause-record.md`](../../../../wip/planning/70-holistika-os-self-governance/reports/p3-topology-decisions-pause-record.md) §3.
- **D-IH-70-W** — IntelligenceOps placement under Research/Intelligence (sub-decision of D-IH-70-B from P2.5 audit).
- **WORKSPACE_BLUEPRINT_HOLISTIKA** §17 (3-tier WIP topology) — Research owns Tier 1.
- **CLASSIFICATION_LATTICE** — Research outputs span all 5 classes (fact / way_of_working / active_research_radar / selling_point / reference_only).
- **HLK_ERP_ARCHITECTURE** §4 — per-area panel inventory reserves `/operator/research/<discipline>/` panels (status: reserved P10.5).
- **Brand sub-discipline ontology** (P5 forward-link) — mirrors this 4-discipline structure.
- **Existing technique folders** — see §4 mapping table above; migration deferred to P4.5 wave 3.
