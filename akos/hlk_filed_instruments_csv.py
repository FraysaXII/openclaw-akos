"""Field contract for FILED_INSTRUMENTS.csv (Initiative 21 / P5 + I81 P2 T3).

Canonical CSV lives under
docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/advops/FILED_INSTRUMENTS.csv.
Mirrored to compliance.filed_instruments_mirror on Supabase.

Replaces the markdown register ``FOUNDER_FILED_INSTRUMENT_REGISTER.md`` as
the SSOT for legal instruments and registral artifacts. The vault markdown
becomes a derived human view filtered by program/discipline.

Naming lineage: created at I21 as FOUNDER_FILED_INSTRUMENTS.csv +
hlk_founder_filed_instruments_csv.py; renamed at I81 P2 T3 (D-IH-81-S
under D-IH-81-G umbrella, 2026-05-23) to drop the FOUNDER_ prefix now
that the folder context (advops/) already implies the founder-level
scope. The deprecation shim
``akos/hlk_founder_filed_instruments_csv.py`` re-exports
``FOUNDER_FILED_INSTRUMENTS_FIELDNAMES`` as an alias for
``FILED_INSTRUMENTS_FIELDNAMES`` for one initiative cycle (removal at
I81 P9 closure).
"""

from __future__ import annotations

# Keep in sync with docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/advops/FILED_INSTRUMENTS.csv header row.
FILED_INSTRUMENTS_FIELDNAMES: tuple[str, ...] = (
    "instrument_id",
    "discipline_id",
    "program_id",
    "instrument_type",
    "jurisdiction",
    "status",
    "effective_or_filing_date",
    "storage_location",
    "vault_link",
    "primary_owner_role",
    "counterparty_goi_ref_id",
    "supersedes_instrument_id",
    "notes",
    "last_review_at",                  # I71 P4 follow-up (D-IH-71-R) review-stamp (DATE; ISO YYYY-MM-DD)
    "last_review_by",                  # I71 P4 follow-up (D-IH-71-R) review-stamp (FK-by-convention to baseline_organisation.csv role_name)
    "last_review_decision_id",         # I71 P4 follow-up (D-IH-71-R) review-stamp (FK-by-convention to DECISION_REGISTER.csv decision_id; nullable)
    "methodology_version_at_review",   # I71 P4 follow-up (D-IH-71-R) review-stamp (LOGIC_CHANGE_LOG.md methodology version at review time; vMAJOR.MINOR per D-IH-71-D)
)
