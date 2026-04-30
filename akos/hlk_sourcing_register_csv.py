"""Field contract for SOURCING_REGISTER.csv (Initiative 31 P5.2).

Canonical CSV lives under ``docs/references/hlk/compliance/dimensions/``.
Mirrored to ``compliance.sourcing_register_mirror`` on Supabase.

Records every external professional Holistika has engaged or considered
engaging (designers, developers, marketers, translators, advisors, etc).
Each row carries:

- ``distance_band_at_first_contact`` — how the vendor first arrived
  (cold ``N4`` via Upwork or referred ``N2`` via a known advisor).
- ``current_distance_band`` — often migrates over time as the relationship
  matures (``N4`` cold becomes ``N1`` repeat-hire, captured as a costly
  signal of relationship quality).

Operating rule: real names kept off-repo per redaction discipline; only
``vendor_id`` is the stable handle. Operator-managed identity mapping lives
in the off-repo redaction sheet alongside GOI/POI mappings.
"""

from __future__ import annotations

# Keep in sync with docs/references/hlk/compliance/dimensions/SOURCING_REGISTER.csv header row.
SOURCING_REGISTER_FIELDNAMES: tuple[str, ...] = (
    "vendor_id",
    "discipline",
    "engagement_type",
    "languages_supported",
    "timezone_band",
    "hourly_rate_band",
    "quality_band",
    "distance_band_at_first_contact",
    "current_distance_band",
    "last_engagement_date",
    "linked_topic_ids",
    "notes",
)
