"""Field contract for `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/TOPIC_REGISTRY.csv`.

Initiative 25 P2 (D-IH-12). Topics are first-class governed entities with
cross-topic edges (parent/depends/related/subsumes) projected from CSV into
Neo4j as typed relationships (`:DEPENDS_ON`, `:TOPIC_PARENT_OF`, `:RELATED_TO`,
`:TOPIC_SUBSUMES`, plus `:UNDER_PROGRAM` to the Initiative 23 PROGRAM_REGISTRY).

Schema:

- `topic_id` — unique identifier (snake_case prefix `topic_`).
- `title` — human-readable.
- `lifecycle_status` — `proposed | active | paused | closed | superseded`.
  (legacy `topic_class` retired at D-IH-95-H — superseded by the `subject_kind` facet below.)
- `primary_owner_role` — FK to `baseline_organisation.csv` `role_name`.
- `program_id` — FK to `PROGRAM_REGISTRY.csv` `program_id` OR `shared` for
  cross-program topics.
- `plane` — `advops | finops | mktops | techops | marops | devops | ops |
  shared` (some topics span planes).
- `parent_topic` — single optional parent topic_id.
- `related_topics` — semicolon-separated list of related topic_ids.
- `depends_on` — semicolon-separated list of upstream topic_ids.
- `subsumes` / `subsumed_by` — semicolon-separated lists of subsumed/subsuming
  topic_ids (typically used after a topic merge).
- `manifest_path` — path to the per-topic `*.manifest.md` under `_assets/`.
- `notes` — free-form.
"""

from __future__ import annotations

TOPIC_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "topic_id",
    "title",
    "lifecycle_status",
    "primary_owner_role",
    "program_id",
    "plane",
    "parent_topic",
    "related_topics",
    "depends_on",
    "subsumes",
    "subsumed_by",
    "manifest_path",
    "notes",    "last_review_at",                  # I71 P4 follow-up (D-IH-71-R) review-stamp (DATE; ISO YYYY-MM-DD)
    "last_review_by",                  # I71 P4 follow-up (D-IH-71-R) review-stamp (FK-by-convention to baseline_organisation.csv role_name)
    "last_review_decision_id",         # I71 P4 follow-up (D-IH-71-R) review-stamp (FK-by-convention to DECISION_REGISTER.csv decision_id; nullable)
    "methodology_version_at_review",   # I71 P4 follow-up (D-IH-71-R) review-stamp (LOGIC_CHANGE_LOG.md methodology version at review time; vMAJOR.MINOR per D-IH-71-D)
    "subject_kind",                    # D-IH-95-H L5 schema tranche — orthogonal facet (seeded from topic_class; topic_class retired in data tranche)
    "steward_role",                    # D-IH-95-H — vocabulary steward (KM Officer default; optional until seat activates)
    "working_area_path",               # D-IH-95-H — docs/wip/intelligence/<slug>/ corpus binding (occurrence); data tranche binds
    "knowledge_index_path",            # D-IH-95-H — TOPIC_KNOWLEDGE_INDEX path; data tranche binds
    "physical_model",                  # D-IH-95-H — keyed_in_place | physically_moved (governed-move authorization)
)
