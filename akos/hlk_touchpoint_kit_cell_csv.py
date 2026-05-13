"""Field contract for TOUCHPOINT_KIT_CELL_REGISTRY.csv (Initiative 32 P3).

Canonical CSV lives under ``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/``.
Mirrored to ``compliance.touchpoint_kit_cell_mirror`` on Supabase.

A touchpoint-kit cell = one (persona × channel × language) template file under
``docs/references/hlk/v3.0/_assets/touchpoint-kit/<persona_id>/<channel_id>/intro_message_<lang>.md``.
The cell registry makes the touchpoint-kit queryable from runtime: today the
kit is filesystem-only and a runtime cannot answer "show me all (persona ×
channel × language) cells that exist". With this CSV, the answer is a SELECT.

The keystone validator invariant is the **FS-vs-CSV drift detector**: the
validator scans the touchpoint-kit folder, derives the expected cell set from
the filesystem, and asserts the CSV mirrors it 1:1 (no phantom rows, no
missing rows). Per the I32 P3 plan, a planted-phantom test is the regression
guard.

The 8-cells framing from Initiative 31 P4 (discovery-taxonomy.md) is preserved
as: rows grouped by ``(persona_id, channel_id)`` yield 8 distinct combinations
across the 15 file rows.
"""

from __future__ import annotations

# Keep in sync with docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/TOUCHPOINT_KIT_CELL_REGISTRY.csv header row.
TOUCHPOINT_KIT_CELL_FIELDNAMES: tuple[str, ...] = (
    "cell_id",                    # ^CELL-[A-Z0-9-]{4,80}-(EN|ES|FR)$
    "persona_id",                 # FK to PERSONA_REGISTRY.csv
    "channel_id",                 # FK to CHANNEL_TOUCHPOINT_REGISTRY.csv
    "language",                   # en | es | fr (FK to ALLOWED_LANGUAGES)
    "topic_ids",                  # semicolon-list FK to TOPIC_REGISTRY.csv (axis 6)
    "template_path",              # repo-relative; must exist on disk (FS-drift check)
    "distance_variants_in_file",  # semicolon-list of N1; N2; N3; N4
    "lifecycle_status",           # active | deprecated | scaffold
    "last_review",                # YYYY-MM-DD
    "notes",
)

ALLOWED_LANGUAGES: frozenset[str] = frozenset({"en", "es", "fr"})
VALID_LIFECYCLE_STATUSES: frozenset[str] = frozenset({"active", "deprecated", "scaffold"})
VALID_DISTANCE_BANDS: frozenset[str] = frozenset({"N1", "N2", "N3", "N4"})

# Touchpoint-kit root (relative to REPO_ROOT) — used by the validator's FS-drift scan.
TOUCHPOINT_KIT_ROOT: str = "docs/references/hlk/v3.0/_assets/touchpoint-kit"
