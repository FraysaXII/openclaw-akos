"""Field contract for GOI_POI_REGISTER.csv (Initiative 21).

Canonical CSV lives under docs/references/hlk/compliance/.
Mirrored to compliance.goipoi_register_mirror on Supabase.

GOI = Group of Interest (organisation / entity).
POI = Person of Interest (role-as-position; a real human reference).

Operating rule: documents reference ``ref_id`` only. Real human and private
organisation names are kept off-repo. Public entities (``is_public_entity = true``)
may use a real name as ``display_name``; private entities must use an obfuscated
display label safe for public repository visibility.
"""

from __future__ import annotations

# Keep in sync with docs/references/hlk/compliance/GOI_POI_REGISTER.csv header row.
GOIPOI_REGISTER_FIELDNAMES: tuple[str, ...] = (
    "ref_id",
    "entity_kind",
    "class",
    "is_public_entity",
    "display_name",
    "lens",
    "sensitivity",
    "program_id",
    "role_owner",
    "process_item_id",
    "primary_link",
    "notes",
)
