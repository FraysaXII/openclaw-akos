"""Field contract for FOUNDER_FILED_INSTRUMENTS.csv (Initiative 21 / P5).

Canonical CSV lives under docs/references/hlk/compliance/.
Mirrored to compliance.founder_filed_instruments_mirror on Supabase.

Replaces the markdown register ``FOUNDER_FILED_INSTRUMENT_REGISTER.md`` as
the SSOT for legal instruments and registral artifacts. The vault markdown
becomes a derived human view filtered by program/discipline.
"""

from __future__ import annotations

# Keep in sync with docs/references/hlk/compliance/FOUNDER_FILED_INSTRUMENTS.csv header row.
FOUNDER_FILED_INSTRUMENTS_FIELDNAMES: tuple[str, ...] = (
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
)
