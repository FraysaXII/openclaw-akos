"""Field contract for ADVISER_ENGAGEMENT_DISCIPLINES.csv (Initiative 21).

Canonical CSV lives under docs/references/hlk/compliance/.
Mirrored to compliance.adviser_engagement_disciplines_mirror on Supabase.

Defines the small lookup of external-adviser engagement **disciplines** (legal,
fiscal, IP, banking, certification, notary, …) used by the ADVOPS plane
(workstream ``hol_opera_ws_5``). Adviser open questions and filed instruments
reference rows here by ``discipline_id`` to drive per-discipline routing in
``EXTERNAL_ADVISER_ROUTER.md`` and the counsel handoff package.
"""

from __future__ import annotations

# Keep in sync with docs/references/hlk/compliance/ADVISER_ENGAGEMENT_DISCIPLINES.csv header row.
ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES: tuple[str, ...] = (
    "discipline_id",
    "discipline_code",
    "display_name",
    "canonical_role",
    "default_process_item_id",
    "default_program_id",
    "description",
    "notes",
)
