"""Field contract for ADVISER_OPEN_QUESTIONS.csv (Initiative 21 / P4).

Canonical CSV lives under docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/.
Mirrored to compliance.adviser_open_questions_mirror on Supabase.

Replaces the markdown queue ``FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md`` as
the SSOT for adviser-facing questions and actions across all disciplines and
programs. The vault markdown becomes a derived human view per discipline.
"""

from __future__ import annotations

# Keep in sync with docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/ADVISER_OPEN_QUESTIONS.csv header row.
ADVISER_OPEN_QUESTIONS_FIELDNAMES: tuple[str, ...] = (
    "question_id",
    "discipline_id",
    "program_id",
    "question_or_action",
    "owner_role",
    "target_date",
    "status",
    "poi_ref_id",
    "goi_ref_id",
    "evidence_pointer",
    "notes",
)
