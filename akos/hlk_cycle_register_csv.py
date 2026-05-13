"""Field contract for CYCLE_REGISTER.csv (Initiative 59 P1.4).

Canonical CSV lives under ``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/CYCLE_REGISTER.csv``.
Mirrored to ``compliance.cycle_register_mirror`` on Supabase.

Formalizes coordinating cycles like Initiatives 57, 58, 59. Cycles differ
structurally from regular initiatives: they coordinate multiple sub-initiatives
via FK joins (e.g., I58 coordinated I28/I29/I30/I31). This dimension makes the
relationship queryable.

PRIMARY KEY format: ``CYC-{NN}`` where ``NN`` is the cycle number (typically
matches the coordinating initiative's number).

FK targets:

- ``coordinating_initiative_id`` → INITIATIVE_REGISTRY.initiative_id.
- ``coordinated_initiative_ids`` → semicolon-list FK to INITIATIVE_REGISTRY
  (sub-initiatives driven to closure within the cycle).
"""

from __future__ import annotations

# Keep in sync with docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/CYCLE_REGISTER.csv header row.
CYCLE_REGISTER_FIELDNAMES: tuple[str, ...] = (
    "cycle_id",                       # ^CYC-\d{1,3}$ ; PRIMARY KEY
    "title",                          # human-readable
    "coordinating_initiative_id",     # FK to INITIATIVE_REGISTRY.initiative_id
    "coordinated_initiative_ids",     # semicolon-list FK to INITIATIVE_REGISTRY
    "status",                         # active | closed | archived
    "started_at",                     # YYYY-MM-DD
    "closed_at",                      # YYYY-MM-DD (nullable; required when status=closed)
    "scope_summary",                  # one-paragraph summary
    "verification_matrix_count",       # int (>=0); number of checks at P10 closure
    "operator_approval_gates_count",   # int (>=0); G-NN-* gate count
    "linked_topic_ids",               # semicolon-list FK to TOPIC_REGISTRY.csv (nullable)
    "notes",
)

VALID_CYCLE_STATUSES: frozenset[str] = frozenset({
    "active", "closed", "archived",
})
