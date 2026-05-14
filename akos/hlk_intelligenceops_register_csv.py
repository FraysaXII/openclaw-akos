"""Field contract for INTELLIGENCEOPS_REGISTER.csv (Initiative 72 P6).

Canonical CSV lives under
``docs/references/hlk/v3.0/Admin/O5-1/Research/Intelligence/canonicals/dimensions/``.

Mirrored to ``compliance.intelligenceops_register_mirror`` on Supabase per the
pattern established by Initiative 32 P2 (skill_registry_mirror) + Initiative 72
P2 (engagement_template_registry_mirror).

INTELLIGENCEOPS_REGISTER = sibling canonical to GOI_POI_REGISTER. While
GOI_POI_REGISTER captures the IDENTITY of allies/neutrals/enemies (named
individuals + organisations + their distance band + stance), the
INTELLIGENCEOPS_REGISTER captures the OPERATIONAL CONTRACT for systematic
intelligence collection against those identities — cadence + source type +
reliability grading + responsible role + output artifact.

Per `D-IH-72-H` the register is a SIBLING canonical (not a column-extension
on GOI_POI_REGISTER) — identity capture and intelligence-collection contract
have distinct lifecycles, distinct ownership, and distinct mirror tables.

Decision lineage:
- `D-IH-72-A` (P0 charter)
- `D-IH-72-H` (sibling registry, not GOI_POI col-extension)
- `D-IH-72-I` (regulator-relationship roadmap = generic SOP + ENISA worked example)
- `D-IH-72-J` (media-counterparty-onboarding = Storytelling charter cross-link + register row)
- `D-IH-72-K` (recruiter onboarding = register row + I73 People Operations onboarding SOP)
- `D-IH-72-Q` (cadence taxonomy = on_demand|scheduled|event_triggered|gated_operator)
- `D-IH-70-AC` (forward-charter from I70 P8.5 GOI/POI hunt: 4 enum classes
  ratified including competitor_intelligence_target + recruiter — these
  classes seed INTELLIGENCEOPS_REGISTER target_class enum)
"""

from __future__ import annotations

# Keep in sync with the canonical CSV header row at
# docs/references/hlk/v3.0/Admin/O5-1/Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv
INTELLIGENCEOPS_REGISTER_FIELDNAMES: tuple[str, ...] = (
    "register_id",                     # ^IO-[A-Z0-9-]{4,80}$ — stable identifier
    "target_id",                       # FK-by-convention to GOI_POI_REGISTER.csv ref_id; TODO[OPERATOR-...] markers
                                       # allowed when GOI row not yet minted (gated by SOP authoring cycle)
    "target_class",                    # enum competitor_intelligence_target | regulator | media | recruiter
    "cadence",                         # enum on_demand | scheduled | event_triggered | gated_operator (per D-IH-72-Q)
    "source_type",                     # enum HUMINT | OSINT | TECHINT | hybrid (per HUMINT FM 2-22.3 source typology)
    "reliability",                     # enum A | B | C | D | E (HUMINT FM 2-22.3 source-reliability rating)
    "output_artifact",                 # path or template-pattern; where the collection output lands
    "responsible_role",                # FK to baseline_organisation.csv role_name
    "lifecycle_status",                # enum active | scaffold | deprecated
    "intro_decision_id",               # FK to DECISION_REGISTER.csv decision_id; chartering decision
    "linked_sop_path",                 # path to operator-facing SOP (per akos-executable-process-catalog.mdc Rule 1)
    "linked_runbook_path",             # path to executable runbook (per akos-executable-process-catalog.mdc Rule 1)
    "notes",
    "last_review_at",                  # I71 P4 follow-up (D-IH-71-R) review-stamp (DATE; ISO YYYY-MM-DD)
    "last_review_by",                  # I71 P4 follow-up (D-IH-71-R) review-stamp (FK-by-convention to baseline_organisation.csv role_name)
    "last_review_decision_id",         # I71 P4 follow-up (D-IH-71-R) review-stamp (FK-by-convention to DECISION_REGISTER.csv decision_id; nullable)
    "methodology_version_at_review",   # I71 P4 follow-up (D-IH-71-R) review-stamp (LOGIC_CHANGE_LOG.md methodology version at review time; vMAJOR.MINOR per D-IH-71-D)
)


VALID_TARGET_CLASSES: frozenset[str] = frozenset({
    "competitor_intelligence_target",
    "regulator",
    "media",
    "recruiter",
})


# Per D-IH-72-Q cadence taxonomy.
VALID_CADENCES: frozenset[str] = frozenset({
    "on_demand",
    "scheduled",
    "event_triggered",
    "gated_operator",
})


# Per HUMINT FM 2-22.3 (US Army Field Manual on Human Intelligence) source typology.
# Distinct from the FM 2-22.3 reliability rating below.
VALID_SOURCE_TYPES: frozenset[str] = frozenset({
    "HUMINT",   # human intelligence (interviews, conversations, briefings)
    "OSINT",    # open-source intelligence (public web, registries, journalism)
    "TECHINT",  # technical intelligence (code analysis, infra signals, telemetry)
    "hybrid",   # multi-source synthesis
})


# HUMINT FM 2-22.3 §B-2 source-reliability rating scale.
VALID_RELIABILITY_GRADES: frozenset[str] = frozenset({
    "A",  # completely reliable
    "B",  # usually reliable
    "C",  # fairly reliable
    "D",  # not usually reliable
    "E",  # unreliable
})


VALID_LIFECYCLE_STATUSES: frozenset[str] = frozenset({
    "active",       # contract is live; collection happens per cadence
    "scaffold",     # contract authored but collection not yet running (TODO target_id common)
    "deprecated",   # contract retired; historical record only
})
