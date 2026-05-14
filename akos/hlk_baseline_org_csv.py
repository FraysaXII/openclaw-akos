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
# Columns 16-17 (sub_area + status) were added by I70 P8 §8.14 (operator
# ratification 2026-05-13, D-IH-70-Z) as part of the v3.1 methodology
# versioning rework: sub_area enables hierarchical encoding within an area
# (e.g. Marketing/Reach, People/Compliance, Operations/SMO); status enables
# soft-state tracking (active / deprecated / pending) without hard-removing
# rows when an org-design refinement is in flight.
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
    "sub_area",
    "status",    "last_review_at",                  # I71 P4 follow-up (D-IH-71-R) review-stamp (DATE; ISO YYYY-MM-DD)
    "last_review_by",                  # I71 P4 follow-up (D-IH-71-R) review-stamp (FK-by-convention to baseline_organisation.csv role_name)
    "last_review_decision_id",         # I71 P4 follow-up (D-IH-71-R) review-stamp (FK-by-convention to DECISION_REGISTER.csv decision_id; nullable)
    "methodology_version_at_review",   # I71 P4 follow-up (D-IH-71-R) review-stamp (LOGIC_CHANGE_LOG.md methodology version at review time; vMAJOR.MINOR per D-IH-71-D)

)
