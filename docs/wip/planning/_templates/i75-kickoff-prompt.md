---
language: en
status: active
authored: 2026-05-13
last_review: 2026-05-13
target_initiative: I75 (candidate)
target_phase: Discovery → Plan-Author → P0 charter
classification: fact
ssot: false
---

# I75 kickoff — Discovery + Plan-Author + P0 charter (Research area governance)

> **Copy everything below the `--- BEGIN PROMPT ---` line into a fresh Cursor chat.**
>
> **Hold gate**: do not run until I71 + I72 + I73 P0 charters have shipped + Research Director hire (or founder commitment to take the role) is decided.

## --- BEGIN PROMPT ---

```
Goal: Drive INIT-OPENCLAW_AKOS-75 (Research area governance) from "candidate" to "active P0 charter
shipped on main", in the same inline-AskQuestion style as the I70 transcript.

Read first (in this order; do not skip):
- .cursor/rules/akos-inline-ratification.mdc
- .cursor/rules/akos-planning-traceability.mdc
- .cursor/rules/akos-governance-remediation.mdc
- docs/wip/planning/_candidates/i75-research-area-governance.md (lift)
- docs/wip/planning/_templates/initiative-planning-prompts.md (generic prompt trio)

Internal canonicals to read (Research is a deep area; budget reading time):
- docs/references/hlk/v3.0/Research/canonicals/RESEARCH_AREA_CHARTER.md
- docs/references/hlk/v3.0/Research/Methodology/canonicals/METHODOLOGY_DISCIPLINE_CHARTER.md
- docs/references/hlk/v3.0/Research/Intelligence/canonicals/INTELLIGENCE_DISCIPLINE_CHARTER.md
- docs/references/hlk/v3.0/Research/Diagnosis/canonicals/DIAGNOSIS_DISCIPLINE_CHARTER.md
- docs/references/hlk/v3.0/Research/Validation/canonicals/VALIDATION_DISCIPLINE_CHARTER.md
- docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/FOUNDER_METHODOLOGY_VERSIONING.md
- docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/LOGIC_CHANGE_LOG.md
- docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/FOUNDER_CORPUS_INVENTORY.md
- docs/wip/intelligence/README.md (Tier 1 WIP topology; Research owns)
- DECISION_REGISTER.csv rows: D-IH-70-S (Research as new top-level), D-IH-70-W (IntelligenceOps
  placement under Research/Intelligence).

External research targets (cite at least 4 with URLs):
- Intelligence-discipline canon (HUMINT / OSINT public materials; e.g. CIA Tradecraft Primer,
  Bellingcat OSINT handbook, Open Source Centre).
- Methodology-pillar approaches in consultancy / academia (e.g. McKinsey 7S, BCG growth-share,
  Deloitte's strategy frameworks; for academic — design science research methodology).
- Source-reliability grading systems (Admiralty Code, NATO STANAG 2511; intelligence-community
  standard vocabularies).
- Validation gates in research (peer review, replication crisis literature, Stanford / MIT
  research reproducibility programs).

Step 1 — Discovery (per generic Prompt 1):
- Surface every architectural conundrum (C-75-1 through C-75-5).
- C-75-1 (Methodology pillar count: 6 vs 8 vs operator-driven) is pre-charter architectural.
  Founder must enumerate stable pillars before the agent can scope P1.
- C-75-2 (Intelligence vs Compliance overlap on OSINT / regulatory boundary) is pre-charter.
- One AskQuestion batch: confirm PROMOTE next-step.

Step 2 — Plan-Author (per generic Prompt 2):
- Author .cursor/plans/i75-research-area-governance_<8hex>.plan.md
- Author docs/wip/planning/75-research-area-governance/master-roadmap.md
- Author docs/wip/planning/75-research-area-governance/reports/p0-charter-<date>.md
- git mv the candidate.

Step 3 — Mint registry rows (one atomic commit):
- DECISION_REGISTER.csv: D-IH-75-A (Methodology pillar SOPs), D-IH-75-B (Intelligence per-source
  SOPs + Intelligence Matrix), D-IH-75-C (Diagnosis + Validation rubrics), D-IH-75-D (KM Officer
  curriculum cross-coordinated with D-IH-73-A), D-IH-75-E (Research Director activation),
  D-IH-75-F (per-engagement intelligence cadence), plus charter row.
- INITIATIVE_REGISTRY.csv: row INIT-OPENCLAW_AKOS-75 with status=active.
- OPS_REGISTER.csv: rows OPS-75-1 through OPS-75-6, status=open.

Step 4 — Cross-link surfaces:
- WORKSPACE_BLUEPRINT_HOLISTIKA.md section 17 (3-tier WIP topology; Research owns Tier 1).
- WORKSPACE_BLUEPRINT_HOLISTIKA.md section 13 (WIP-to-canonical promotion; Validation gate consumer).
- I73 cross-link: KM Officer curriculum (I75 P4) and Holistik Researcher curriculum (I73 P1)
  must reference each other. If I73 P1 has shipped, lift its content into I75 P4 inputs.
- I72 cross-link: per-engagement intelligence cadence (I75 P6) and engagement-template promotion
  machine (I72 P3) must reference each other.
- CHANGELOG.md [Unreleased] / Added: charter entry.

Verification (same suite as I72/I73/I74):
- validate_decision_register, validate_initiative_registry, validate_ops_register, validate_hlk,
  validate_master_roadmap_frontmatter, validate_hlk_vault_links, render_operator_inbox.

Commit message:
"i75 p0 inline charter + registries + workspace cross-links (research area governance)"

DECISION DISCIPLINE (binding):
- C-75-1 pillar count: NEVER ship the Methodology charter without the founder enumerating stable
  pillars. The founder is the SSOT for the methodology pillars; the agent must NOT invent them.
- C-75-5 Validation gate veto authority: pre-charter ratify; default = co-sign with PMO; founder
  breaks ties.

OPERATOR NOTES (paste your latest thoughts here):
[paste-here]
```

## --- END PROMPT ---

## Initiative-specific guidance

- I75 is the **deepest** of the candidate set in terms of SOP authoring volume — ~6-8 Methodology pillars × multi-page SOPs + Intelligence per-source-type + Diagnosis templates + Validation rubrics. Budget P1–P3 generously; consider per-discipline phase splits in the master-roadmap.
- **The KM Officer / Holistik Researcher boundary** (C-75-4) cross-coordinates with I73 C-73-1 (cohort size). Best practice: ratify both at the same `AskQuestion` batch when I73 + I75 are both in P0.
- **IntelligenceOps SOPs** are already migrated under `Research/Intelligence/canonicals/` per `D-IH-70-W` (I70 P4.5 wave 3). Verify they're there before P2 scopes per-source-type SOPs; the agent must not duplicate.

## After P0 ships

P1 (Methodology pillar SOPs) is per-pillar work; budget one phase commit per pillar OR one phase commit for all pillars depending on operator preference. Ratify at P1 inline-ratify gate.
