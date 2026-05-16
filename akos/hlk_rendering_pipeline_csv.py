"""SSOT for `RENDERING_PIPELINE_REGISTRY.csv` (Initiative 77 P4.C).

Per `D-IH-77-I` (visual UAT rendering discipline + orphan-rendering-pipeline
governance discovery): every document-rendering pipeline in the repo
(Impeccable bridges, deck-HTML, dossier-PDF, Figma, PMO-hub, KM-diagrams,
touchpoint-kit messages, cover-emails, visual UAT renders, etc.) is catalogued
with status metadata + paired SOP + paired runbook per
`akos-executable-process-catalog.mdc` Rule 1 (SOP + executable runbook pairing)
+ Rule 2 (active / inactive / planned / experimental / deprecated metadata).

Canonical path:
    docs/references/hlk/v3.0/Envoy Tech Lab/canonicals/dimensions/RENDERING_PIPELINE_REGISTRY.csv

Owning area: Tech / System Owner (pipeline infrastructure)
Co-owning role: Brand Manager (brand-token consumption decisions)

Decision lineage:
- D-IH-77-G (I77 scope expansion to P4)
- D-IH-77-I (visual UAT rendering discipline + this registry)

Forward-charter targets: a future "rendering productization" initiative may
absorb this registry into the `@holistika/akos-render` library export
(analogous to the I74 brand-tooling productization pattern).
"""
from __future__ import annotations


RENDERING_PIPELINE_FIELDNAMES: tuple[str, ...] = (
    "pipeline_id",                   # ^[a-z0-9_]{3,80}$
    "name",                          # human-readable
    "trigger_type",                  # enum (cadence taxonomy per akos-executable-process-catalog Rule 3)
    "trigger_command",               # literal command or workflow that fires it
    "owning_area",                   # area slug (Tech, Marketing/Reach, Operations/PMO, etc.)
    "owning_role",                   # FK-by-convention to baseline_organisation.csv role_name
    "status",                        # enum (per Rule 2: active | inactive | planned | experimental | deprecated)
    "brand_tokens_consumed",         # yes | no — whether pipeline applies brand HSL palette + typography
    "input_paths",                   # semicolon-list of input file globs or paths
    "output_paths",                  # semicolon-list of output paths
    "sop_path",                      # paired SOP markdown path (or TODO[I-NN-...] marker)
    "runbook_path",                  # paired runbook script path (or TODO[I-NN-...] marker)
    "linked_processes",              # semicolon-list of process_list.csv item_ids (or empty for meta)
    "linked_decision_id",            # FK-by-convention to DECISION_REGISTER.csv
    "governance_class",              # governed | partial | orphan
    "added_at",                      # YYYY-MM-DD
    "last_review_at",                # YYYY-MM-DD
    "last_review_decision_id",       # FK-by-convention to DECISION_REGISTER.csv (e.g. cycle close)
    "methodology_version_at_review", # v3.0 / v3.1 / etc.
    "notes",
)


VALID_TRIGGER_TYPES: frozenset[str] = frozenset({
    "on_demand",        # operator (or agent on operator instruction) triggers ad-hoc
    "scheduled",        # fires on deterministic cron/cadence
    "event_triggered",  # fires when a specific event occurs (e.g. CSV change, deploy ping)
    "gated_operator",   # runs after explicit operator approval (AskQuestion ratification)
})


VALID_STATUSES: frozenset[str] = frozenset({
    "active",         # pipeline is wired up, tested, in production use
    "inactive",       # pipeline exists but not currently wired (e.g. dormant adapter)
    "planned",        # documented as future pipeline; no implementation yet
    "experimental",   # proof-of-concept; may promote to active or roll back
    "deprecated",     # phased out; replaced by successor
})


VALID_GOVERNANCE_CLASSES: frozenset[str] = frozenset({
    "governed",   # paired SOP + runbook exist + validator gates + tests cover
    "partial",    # script exists but no SOP OR no validator OR no tests
    "orphan",     # neither SOP nor runbook nor validator (manual operator-only workflow)
})


VALID_BRAND_TOKENS_CONSUMED: frozenset[str] = frozenset({"yes", "no"})


CANONICAL_PATH = (
    "docs/references/hlk/v3.0/Envoy Tech Lab/canonicals/dimensions/"
    "RENDERING_PIPELINE_REGISTRY.csv"
)
