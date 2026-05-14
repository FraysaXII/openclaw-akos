"""Field contract for `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PROGRAM_REGISTRY.csv`.

Initiative 23 P1 (D-IH-8): the Program Registry is a separate canonical CSV
under the new `compliance/dimensions/` subfolder per the Initiative 22 forward
layout convention. Programs are the primary axis for Wave-2 (`<plane> ×
<program_id> × <topic_id>`) and reference back to `process_list.csv` projects
via `process_item_id` when one exists.

Schema (D-IH-8 + D-IH-9):

- `program_id` — canonical PRJ-HOL-style identifier (e.g. `PRJ-HOL-FOUNDING-2026`,
  `PRJ-HOL-KIRBE-2026`). Stable across `process_list.csv` reorganizations and
  used as the path component under `_assets/<plane>/<program_id>/<topic_id>/`
  and `v3.0/<role>/programs/<program_id>/`.
- `process_item_id` — FK to `process_list.csv` `item_id` of `item_granularity =
  project` row when one exists. Empty for casework-only programs (e.g.
  PRJ-HOL-FOUNDING-2026 has no project granularity row).
- `program_name` — human-readable name.
- `program_code` — 3-letter unique short handle (`^[A-Z]{3}$`); used in graph
  node properties (`Program.program_code`) and short slugs.
- `lifecycle_status` — `proposed | active | paused | closed | superseded`.
- `parent_program_id` — single optional parent (sub-program relationship).
- `consumes_program_ids` — semicolon-separated list of upstream programs whose
  outputs this program depends on. Validator enforces DAG (cycle detection).
- `produces_for_program_ids` — semicolon-separated list of downstream programs
  this program feeds. Conventionally the inverse of `consumes_program_ids`.
- `subsumes_program_ids` — semicolon-separated list of programs this program
  subsumes (e.g. after a merge); referenced programs typically have
  `lifecycle_status = superseded`.
- `primary_owner_role` — FK to `baseline_organisation.csv` `role_name`.
- `default_plane` — `advops | finops | mktops | techops | marops | devops | ops`.
- `start_date` — ISO date or `unknown`.
- `target_close_date` — ISO date or `open` (foundational/ongoing).
- `risk_class` — `low | medium | high | critical`.
- `notes` — free-form; agent-defaulted cells per D-IH-23-A annotated inline.

The Postgres mirror at `compliance.program_registry_mirror` stores the same
columns as TEXT (DAMA-pure projection); Neo4j projects typed relationships
from the semicolon-list columns per D-IH-9 / D-IH-18.
"""

from __future__ import annotations

PROGRAM_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "program_id",
    "process_item_id",
    "program_name",
    "program_code",
    "lifecycle_status",
    "parent_program_id",
    "consumes_program_ids",
    "produces_for_program_ids",
    "subsumes_program_ids",
    "primary_owner_role",
    "default_plane",
    "start_date",
    "target_close_date",
    "risk_class",
    "notes",    "last_review_at",                  # I71 P4 follow-up (D-IH-71-R) review-stamp (DATE; ISO YYYY-MM-DD)
    "last_review_by",                  # I71 P4 follow-up (D-IH-71-R) review-stamp (FK-by-convention to baseline_organisation.csv role_name)
    "last_review_decision_id",         # I71 P4 follow-up (D-IH-71-R) review-stamp (FK-by-convention to DECISION_REGISTER.csv decision_id; nullable)
    "methodology_version_at_review",   # I71 P4 follow-up (D-IH-71-R) review-stamp (LOGIC_CHANGE_LOG.md methodology version at review time; vMAJOR.MINOR per D-IH-71-D)

)
