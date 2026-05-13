"""Field contract for baseline_organisation.csv (canonical organisational baseline).

Canonical CSV lives under docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv.
Mirrored to compliance.baseline_organisation_mirror on Supabase.

Authored in the 2026-05-11 release-gate hygiene pass to close a long-running
drift between the CSV header (15 columns since the Initiative 18 / I12 P12 era)
and the hardcoded tuple in scripts/sync_compliance_mirrors_from_csv.py
(12 columns ending at ``components_used``). The drift caused
``test_sync_compliance_mirrors_from_csv.py`` to silently fail until P13.4 made
it visible. SSOT extraction makes every downstream consumer (sync script,
validator, drift gate) import a single fieldnames tuple from this module,
matching the akos/hlk_<csv>_csv.py pattern used by every other dimension CSV.
"""

from __future__ import annotations

# Keep in sync with docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv header row.
#
# Columns 1-12 are the original Initiative 11 / Phase 1 canonical baseline.
# Columns 13-15 (the role_hourly_*_eur trio) were added by a later finance /
# pricing initiative (rate bands per role for SOP-ENG_ESTIMATION_DISCIPLINE_001
# and downstream proposal-tarification rendering) and remained un-mirrored
# until the 2026-05-11 hygiene pass added them to the mirror DDL.
BASELINE_ORGANISATION_FIELDNAMES: tuple[str, ...] = (
    "org_uuid",
    "role_name",
    "role_description",
    "role_full_description",
    "access_level",
    "reports_to",
    "area",
    "entity",
    "org_id",
    "sop_url",
    "responsible_processes",
    "components_used",
    "role_hourly_min_eur",
    "role_hourly_par_eur",
    "role_hourly_max_eur",
)
