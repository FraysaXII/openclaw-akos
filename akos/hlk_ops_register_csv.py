"""Field contract for OPS_REGISTER.csv (Initiative 59 P1.3).

Canonical CSV lives under ``docs/references/hlk/compliance/OPS_REGISTER.csv``.
Mirrored to ``compliance.ops_register_mirror`` on Supabase.

Formalizes ``OPS-XX-Y`` action items previously scattered across per-initiative
``master-roadmap.md`` "Forwarded residuals" sections + ``CHANGELOG.md`` entries
+ ad-hoc agent summaries. ``docs/wip/planning/OPERATOR_INBOX.md`` is auto-rendered
from this CSV (``status=open AND owner_class IN (operator, mixed) ORDER BY
rice_score DESC``) per Initiative 59 P4.

PRIMARY KEY format: ``OPS-{NN}-{Y}[.{x}]`` where ``NN`` is the originating
initiative number, ``Y`` is the integer sequence within that initiative, and
``.x`` is an optional sub-action suffix (e.g. ``OPS-54-1.c``).

FK targets:

- ``originating_initiative_id`` → INITIATIVE_REGISTRY.initiative_id.
- ``forwarded_to_initiative_id`` → INITIATIVE_REGISTRY.initiative_id (nullable).
- ``gate_id`` → free-form gate identifier (e.g. G-58-1; nullable).
- ``linked_decision_ids`` → semicolon-list FK to DECISION_REGISTER.decision_id
  (nullable).
"""

from __future__ import annotations

# Keep in sync with docs/references/hlk/compliance/OPS_REGISTER.csv header row.
OPS_REGISTER_FIELDNAMES: tuple[str, ...] = (
    "ops_action_id",                # ^OPS-\d{1,3}-\d+(\.[a-z0-9]+)?$ ; PRIMARY KEY
    "title",                        # human-readable
    "originating_initiative_id",    # FK to INITIATIVE_REGISTRY.initiative_id
    "forwarded_to_initiative_id",   # FK to INITIATIVE_REGISTRY.initiative_id (nullable)
    "owner_class",                  # operator | engineering | mixed
    "owner_role",                   # FK to baseline_organisation.csv role_name
    "status",                       # open | in_progress | closed | cancelled | superseded
    "rice_reach",                   # int (0..100); RICE methodology
    "rice_impact",                  # 0.25 | 0.5 | 1 | 2 | 3
    "rice_confidence_pct",          # int (0..100)
    "rice_effort_person_weeks",     # float (>= 0.1)
    "rice_score",                   # float; reach * impact * confidence / effort
    "gate_id",                      # free-form gate id (nullable)
    "linked_decision_ids",          # semicolon-list FK to DECISION_REGISTER (nullable)
    "summary",                      # short summary (1-2 sentences)
    "operator_runbook_path",        # path to operator-side runbook (nullable)
    "evidence_path",                 # path to evidence/closure report (nullable)
    "opened_at",                    # YYYY-MM-DD
    "closed_at",                    # YYYY-MM-DD (nullable; required when status=closed)
    "notes",
)

VALID_OPS_OWNER_CLASSES: frozenset[str] = frozenset({
    "operator", "engineering", "mixed",
})

VALID_OPS_STATUSES: frozenset[str] = frozenset({
    "open", "in_progress", "closed", "cancelled", "superseded",
})

VALID_RICE_IMPACTS: frozenset[str] = frozenset({
    "0.25", "0.5", "1", "2", "3",
})
