"""SSOT for ``AUDIENCE_REGISTRY.csv`` (Initiative 85 P1).

Per D-IH-85-A (narrow FK index pattern; CSV is the FK source-of-truth for
``audience: [J-*]`` frontmatter on advops + touchpoint-kit + bridge surfaces;
``BRAND_BASELINE_REALITY_MATRIX.md`` remains SSOT for deep audience content —
bridge framing, objection patterns, first-doubt triggers, voice deltas).

Per D-IH-85-B (multi-audience encoding = YAML list ``audience: [J-IN, J-AD]``;
FK-resolvable; no parser ambiguity vs comma-string).

Canonical path:
    docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv

Owning area: Marketing / Brand (audience-tag canon governance)
Co-owning role: System Owner (validator + drift gate infrastructure)

Mirrored to ``compliance.audience_registry_mirror`` on Supabase via
``sync_compliance_mirrors_from_csv.py`` after I85 P1 lands.

Decision lineage:
- D-IH-85-A through D-IH-85-E (I85 P0 charter; agent_inline_default per
  I86 inline-ratify pre-pass batch on 2026-05-16).

The ``register_side`` column encodes the dual-register contract from
``.cursor/rules/akos-brand-baseline-reality.mdc`` — which audience-class
consumes the internal CORPINT register (operator + cleared collaborators +
agents) vs the external translated-capability register vs the hybrid posture
(internal vocabulary tolerated post-NDA).
"""
from __future__ import annotations


AUDIENCE_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "audience_code",                  # ^J-[A-Z]{2,8}$
    "name",                           # human-readable
    "register_side",                  # enum internal | external | hybrid (per akos-brand-baseline-reality.mdc)
    "intent_summary",                 # 1-sentence intent + ask
    "typical_surfaces",               # semicolon-list of surface glob paths
    "bridge_anchor",                  # anchor link into BRAND_BASELINE_REALITY_MATRIX.md
    "status",                         # enum active | inactive | planned | experimental | deprecated
    "added_at",                       # YYYY-MM-DD
    "last_review_at",                 # YYYY-MM-DD (I71 D-IH-71-R review-stamp)
    "last_review_by",                 # FK-by-convention to baseline_organisation.csv role_name
    "last_review_decision_id",        # FK-by-convention to DECISION_REGISTER decision_id
    "methodology_version_at_review",  # vMAJOR.MINOR per D-IH-71-D
    "linked_decision_id",             # FK-by-convention to DECISION_REGISTER decision_id (lineage)
    "notes",
)


VALID_REGISTER_SIDES: frozenset[str] = frozenset({
    "internal",   # consumes the CORPINT register; operator + cleared collaborators + agents (J-OP)
    "external",   # consumes the translated-capability register only (J-IN, J-CU, J-PT, J-ENISA, J-RC)
    "hybrid",     # external until cleared / NDA-signed; internal vocabulary tolerated post-clearance (J-AD, J-CO)
})


VALID_STATUSES: frozenset[str] = frozenset({
    "active",         # in production use; advops + touchpoint-kit surfaces may target this audience
    "inactive",       # legitimate audience class but no active surfaces target it right now
    "planned",        # documented future audience; no implementation yet
    "experimental",   # proof-of-concept; may promote to active or roll back
    "deprecated",     # phased out; replaced by successor code
})


CANONICAL_PATH = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/"
    "dimensions/AUDIENCE_REGISTRY.csv"
)
