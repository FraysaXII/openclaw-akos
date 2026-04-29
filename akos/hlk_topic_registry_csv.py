"""Field contract for `docs/references/hlk/compliance/dimensions/TOPIC_REGISTRY.csv`.

Initiative 25 P2 (D-IH-12). Topics are first-class governed entities with
cross-topic edges (parent/depends/related/subsumes) projected from CSV into
Neo4j as typed relationships (`:DEPENDS_ON`, `:TOPIC_PARENT_OF`, `:RELATED_TO`,
`:TOPIC_SUBSUMES`, plus `:UNDER_PROGRAM` to the Initiative 23 PROGRAM_REGISTRY).

Schema:

- `topic_id` — unique identifier (snake_case prefix `topic_`).
- `title` — human-readable.
- `topic_class` — `process_map | architecture | wireframe | methodology_map |
  manifesto | evidence_pack | brand_asset | other`.
- `lifecycle_status` — `proposed | active | paused | closed | superseded`.
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
    "topic_class",
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
    "notes",
)
