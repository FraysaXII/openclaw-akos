---
title: SOP — People Cross-Area Breakthrough Propagation
language: en
intellectual_kind: people-canonical-sop
sop_id: SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - People Operations Lead
last_review: 2026-05-15
last_review_by: People Operations Lead
ratifying_decisions:
  - D-IH-79-A
  - D-IH-79-I
status: active
register: internal
linked_canonicals:
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - PEOPLE_DESIGN_PATTERN_LIBRARY.md
  - PEOPLE_DESIGN_PATTERN_REGISTRY.csv
  - HOLISTIKA_AGENTIC_DOCTRINE.md
  - AGENTIC_FRAMEWORK_LANDSCAPE.md
linked_runbooks:
  - scripts/peopl_cross_area_breakthrough_announce.py
linked_processes:
  - tbi_peopl_dtp_cross_area_breakthrough_001
cadence: event_triggered
cadence_trigger: substantive update to PEOPLE_DESIGN_PATTERN_REGISTRY.csv or sibling-canonical revision
cadence_secondary: scheduled
cadence_secondary_schedule: quarterly
---

# SOP — People Cross-Area Breakthrough Propagation

## Purpose

Operationalise the cross-area mechanism that the People manifesto names. People is the discipline of disciplines: when People mints a new design pattern (or substantively revises an existing one), other areas — Marketing, Tech Lab, Research, Operations — should learn about it, decide whether to adopt it, and adopt it on their own terms. This SOP defines how that propagation happens: who announces, who decides, who supports.

Paired with the runbook [`scripts/peopl_cross_area_breakthrough_announce.py`](../../../../../../scripts/peopl_cross_area_breakthrough_announce.py) per [`akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1. Either People Operations Lead can run it via the SOP, or the runbook fires off-cadence after a registry edit. Both surfaces are SSOT for the same process.

## Scope

In scope:

- Propagation when [`PEOPLE_DESIGN_PATTERN_REGISTRY.csv`](../Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv) gains a new row (a new design pattern is minted).
- Propagation when an existing row is revised substantively (the pattern's `acceptance_criteria_human` or `acceptance_criteria_automation` shifts; the `consumer_areas` list expands or contracts; the `status` lifecycle changes).
- Propagation when [`HOLISTIKA_AGENTIC_DOCTRINE.md`](HOLISTIKA_AGENTIC_DOCTRINE.md) revises substantively — the Tech Lab landscape ([`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md)) is pinged so the framework rows stay coherent.
- Propagation when [`HOLISTIKA_ORGANISING_DOCTRINE.md`](HOLISTIKA_ORGANISING_DOCTRINE.md) revises substantively (the People manifesto itself shifts; every area is pinged).

Out of scope:

- Authoring of the consuming-area processes that adopt the pattern. People supports adoption; consuming areas author their own work per [`akos-people-discipline-of-disciplines.mdc`](../../../../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc) rule 1 (People is discipline-of-disciplines, not author of all processes).
- Marketing / Tech Lab / Research / Operations area-internal cadences. This SOP only governs the cross-area handoff; once a consuming area accepts a pattern, its adoption follows the area's own SOPs.

## Inputs

- [`PEOPLE_DESIGN_PATTERN_REGISTRY.csv`](../Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv) — the SSOT for pattern rows; the runbook reads here.
- [`PEOPLE_DESIGN_PATTERN_LIBRARY.md`](PEOPLE_DESIGN_PATTERN_LIBRARY.md) — human narrative companion; the announcement digest cites the relevant `#pattern-<slug>` anchor.
- The previous breakthrough digest under `docs/wip/planning/79-people-manifesto-and-pattern-library/reports/breakthroughs/<YYYY-MM>/` — establishes the "since last announcement" delta.
- The list of consuming areas per pattern row's `consumer_areas` cell (semicolon-separated tokens; `marketing;tech;research;operations;all`).

## Steps

### 1. Detect the trigger

Two trigger paths:

- **Event-triggered (primary)**: a registry edit lands. The author of the edit (typically People Operations Lead or Compliance Officer) flags whether the edit is substantive. New rows are always substantive; row revisions are substantive when they change `acceptance_criteria_*`, `consumer_areas`, `status`, or when the pattern's discipline-origin shifts.
- **Scheduled (secondary)**: quarterly catch-up. If the event-triggered path missed any edits over the quarter (e.g. the operator forgot to flag an edit as substantive), the quarterly run reconciles by reading every row revised since the last announcement.

### 2. Run the announcement digest

People Operations Lead runs the runbook:

```sh
py scripts/peopl_cross_area_breakthrough_announce.py --since <YYYY-MM-DD>
```

The runbook reads the registry CSV, filters rows last-revised after `--since`, groups by `consumer_areas`, and emits per-area Markdown digests under `docs/wip/planning/79-people-manifesto-and-pattern-library/reports/breakthroughs/<YYYY-MM>/<area>.md`. Each digest carries:

- Pattern ID + name + one-paragraph summary.
- The acceptance criteria for both human and automation paths.
- A link to the `#pattern-<slug>` anchor in [`PEOPLE_DESIGN_PATTERN_LIBRARY.md`](PEOPLE_DESIGN_PATTERN_LIBRARY.md).
- A link to the registry row's `canonical_artifact_path` (the upstream artefact that anchors the pattern).
- A short "what this means for your area" rendering authored by People Operations Lead at announcement time.

### 3. Per-area review and decision

Each consuming-area role-owner (Marketing → Brand Manager; Tech Lab → System Owner; Research → Holistik Researcher; Operations → PMO) reads the digest for their area within one week of receipt. The decision per pattern is one of:

- **Adopt now** — the pattern fits a current or imminent need; the area authors a process row referencing the pattern via `process_list.csv` 8th column `inherited_pattern_id` (P6 deliverable).
- **Adopt later** — the pattern is relevant but the area is not ready; the decision is recorded with an expected adoption window.
- **Decline** — the pattern is not relevant for the area; the decision is recorded so the same digest does not re-circulate.

Decisions land in the area's own decision log, and the digest carries a back-link section listing each area's response.

### 4. Tech Lab pingback for agentic doctrine revisions

When the trigger is a substantive revision to [`HOLISTIKA_AGENTIC_DOCTRINE.md`](HOLISTIKA_AGENTIC_DOCTRINE.md), the runbook explicitly pings the Tech Lab landscape (`AGENTIC_FRAMEWORK_LANDSCAPE.md`) and SOP (`SOP-TECH_AGENTIC_INFRA_001.md`). System Owner reads the People-side change within one week and assesses whether the framework rows, the integration postures, or the knowledge base infrastructure dimensions need to revise to stay coherent. The cross-area breakthrough log records the Tech Lab assessment outcome (revise / no-action / scheduled-revise-at-next-quarterly).

This pingback is the structural defence against the People doctrine + Tech Lab landscape + Ethics anchor triangle going out of sync.

### 5. People support during adoption

After a consuming area decides **adopt now**, People supports the adoption:

- Office-hours session with the role-owner authoring the consuming process row.
- Review of the consuming process row before commit (does the adoption respect the pattern's spirit, not just the letter).
- Knowledge-test bank update for any agent in the consuming area whose scope intersects the new pattern (per [`SOP-PEOPLE_AGENTIC_OPERATIONS_001.md`](SOP-PEOPLE_AGENTIC_OPERATIONS_001.md) §2 test scope).
- Cross-canonical link: the pattern row's `canonical_artifact_path` is updated if the adoption surfaces a new canonical artefact worth registering.

### 6. Quarterly reconciliation

Once per quarter, People Operations Lead runs the runbook in `--reconcile` mode:

```sh
py scripts/peopl_cross_area_breakthrough_announce.py --reconcile --quarter <YYYY-Q>
```

This emits a quarterly summary digest under `reports/breakthroughs/<YYYY-Q>/quarterly-reconciliation.md` covering:

- All patterns minted or revised during the quarter.
- All consuming-area decisions recorded during the quarter.
- Patterns with no decision recorded (the role-owner is pinged).
- Patterns adopted across multiple areas (a candidate for promotion to a higher-tier pattern class).

## Outputs

- Per-area Markdown digests under `docs/wip/planning/79-people-manifesto-and-pattern-library/reports/breakthroughs/<YYYY-MM>/<area>.md`.
- Quarterly reconciliation summary under `reports/breakthroughs/<YYYY-Q>/quarterly-reconciliation.md`.
- Decision records in each consuming area's own decision log.
- Updates to pattern rows when adoption surfaces canonical artefact paths.

## Failure modes

- **Substantive edit not flagged.** Mitigation: quarterly reconciliation catches missed events; pattern row's `last_review` ISO date is the canonical evidence of revision.
- **Consuming area never responds to a digest.** Mitigation: quarterly reconciliation surfaces patterns with no decision recorded; People Operations Lead pings the role-owner directly.
- **Pattern adopted differently across two areas.** Mitigation: People runs an alignment session before either area commits; pattern row may be split into sibling rows if the divergence is structural.
- **Tech Lab pingback skipped after agentic doctrine revision.** Mitigation: the runbook special-cases doctrine-revision triggers; the audit step in [`SOP-TECH_AGENTIC_INFRA_001.md`](../../Envoy%20Tech%20Lab/canonicals/SOP-TECH_AGENTIC_INFRA_001.md) §1 confirms the ping landed.

## Cross-references

- [`HOLISTIKA_ORGANISING_DOCTRINE.md`](HOLISTIKA_ORGANISING_DOCTRINE.md) — the People manifesto framing People-as-discipline-of-disciplines (the why for this SOP).
- [`PEOPLE_DESIGN_PATTERN_LIBRARY.md`](PEOPLE_DESIGN_PATTERN_LIBRARY.md) — narrative companion to the registry; digests cite anchors here.
- [`PEOPLE_DESIGN_PATTERN_REGISTRY.csv`](../Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv) — registry SSOT; the runbook reads this file.
- [`HOLISTIKA_AGENTIC_DOCTRINE.md`](HOLISTIKA_AGENTIC_DOCTRINE.md) — substantive revision triggers Tech Lab pingback.
- [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) — Tech Lab landscape that receives the pingback.
- [`SOP-PEOPLE_AGENTIC_OPERATIONS_001.md`](SOP-PEOPLE_AGENTIC_OPERATIONS_001.md) — knowledge-test cadence the digest informs.
- [`scripts/peopl_cross_area_breakthrough_announce.py`](../../../../../../scripts/peopl_cross_area_breakthrough_announce.py) — paired runbook.
- [`akos-people-discipline-of-disciplines.mdc`](../../../../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc) — Cursor rule the SOP operationalises.
- [`PRECEDENCE.md`](../Compliance/canonicals/PRECEDENCE.md) — registers this SOP.
