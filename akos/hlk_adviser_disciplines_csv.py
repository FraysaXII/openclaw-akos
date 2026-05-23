"""Field contract for ADVISER_ENGAGEMENT_DISCIPLINES.csv (Initiative 21).

Canonical CSV lives under docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/.
Mirrored to compliance.adviser_engagement_disciplines_mirror on Supabase.

Defines the small lookup of external-adviser engagement **disciplines** (legal,
fiscal, IP, banking, certification, notary, …) used by the ADVOPS plane
(workstream ``hol_opera_ws_5``). Adviser open questions and filed instruments
reference rows here by ``discipline_id`` to drive per-discipline routing in
``EXTERNAL_ADVISER_ROUTER.md`` and the counsel handoff package.
"""

from __future__ import annotations

# Keep in sync with docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/advops/ADVISER_ENGAGEMENT_DISCIPLINES.csv header row.
# (Moved to advops/ at I81 P2 T2 — D-IH-81-R under D-IH-81-G umbrella, 2026-05-23.)
ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES: tuple[str, ...] = (
    "discipline_id",
    "discipline_code",
    "display_name",
    "canonical_role",
    "default_process_item_id",
    "default_program_id",
    "description",
    "notes",    "last_review_at",                  # I71 P4 follow-up (D-IH-71-R) review-stamp (DATE; ISO YYYY-MM-DD)
    "last_review_by",                  # I71 P4 follow-up (D-IH-71-R) review-stamp (FK-by-convention to baseline_organisation.csv role_name)
    "last_review_decision_id",         # I71 P4 follow-up (D-IH-71-R) review-stamp (FK-by-convention to DECISION_REGISTER.csv decision_id; nullable)
    "methodology_version_at_review",   # I71 P4 follow-up (D-IH-71-R) review-stamp (LOGIC_CHANGE_LOG.md methodology version at review time; vMAJOR.MINOR per D-IH-71-D)

)
