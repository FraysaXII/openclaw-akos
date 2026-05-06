"""Field contract for INITIATIVE_REGISTRY.csv (Initiative 59 P1.2).

Canonical CSV lives under ``docs/references/hlk/compliance/INITIATIVE_REGISTRY.csv``.
Mirrored to ``compliance.initiative_registry_mirror`` on Supabase.

Central registry for every planning initiative across all Holistika-tracked
repositories (per **D-IH-59-A** governance promotion + **D-IH-59-B** two-layer
SSOT). Markdown ``master-roadmap.md`` files stay canonical for prose; this CSV
is canonical for governed metadata (status / FK joins / lifecycle).

Sync between master-roadmap.md frontmatter and CSV is enforced by
``scripts/validate_initiative_registry_frontmatter_sync.py`` (CI-failing).

PRIMARY KEY format: ``INIT-{REPO_SLUG_UPPER_NO_DASHES}-{NN}`` where ``REPO_SLUG``
is the row's ``repo_slug`` column upper-cased with dashes replaced by underscores
(e.g. ``openclaw-akos`` → ``OPENCLAW_AKOS``), and ``NN`` is the two-digit
initiative number prefix (e.g. ``58`` for ``58-cycle-2-multi-track-forward``).

FK targets:

- ``repo_slug`` → REPOSITORY_REGISTRY.repo_slug.
- ``cycle_id`` → CYCLE_REGISTER.cycle_id (nullable; empty if not part of a cycle).
- ``inception_decision_id`` → DECISION_REGISTER.decision_id (nullable for legacy
  initiatives without a recorded inception decision).
- ``closure_decision_id`` → DECISION_REGISTER.decision_id (nullable; populated
  when ``status='closed'``).
- ``superseded_by`` → INITIATIVE_REGISTRY.initiative_id (nullable; populated
  when ``status='archived'``).
- ``manifests_processes`` → semicolon-list FK to ``process_list.csv`` ``item_id``
  (nullable; **D-IH-59-G** receiver column for I60 mints).
"""

from __future__ import annotations

# Keep in sync with docs/references/hlk/compliance/INITIATIVE_REGISTRY.csv header row.
INITIATIVE_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "initiative_id",          # ^INIT-[A-Z0-9_]+-\d{2,3}$ ; PRIMARY KEY
    "repo_slug",              # FK to REPOSITORY_REGISTRY.repo_slug
    "folder_path",             # docs/wip/planning/<NN>-<slug>/ relative
    "title",                   # human-readable
    "status",                  # FK to akos.planning.status_taxonomy enum
    "cycle_id",                # FK to CYCLE_REGISTER.cycle_id (nullable)
    "owner_role",              # FK to baseline_organisation.csv role_name
    "inception_date",          # YYYY-MM-DD
    "last_review",             # YYYY-MM-DD
    "closed_at",               # YYYY-MM-DD (nullable; required when status=closed)
    "archived_at",             # YYYY-MM-DD (nullable; required when status=archived)
    "superseded_by",           # FK to INITIATIVE_REGISTRY.initiative_id (nullable)
    "continuous_rationale",    # free-form (nullable; required when status=continuous)
    "cadence",                 # weekly | monthly | quarterly | event_driven (nullable; required when status=program_line)
    "gated_on",                # free-form (nullable; required when status in {gated_external, gated_operator})
    "operator_action",         # free-form (nullable; required when status=gated_operator)
    "inception_decision_id",   # FK to DECISION_REGISTER.decision_id (nullable for legacy)
    "closure_decision_id",     # FK to DECISION_REGISTER.decision_id (nullable; required when status=closed)
    "manifests_processes",     # semicolon-list FK to process_list.csv item_id (nullable; D-IH-59-G)
    "linked_topic_ids",        # semicolon-list FK to TOPIC_REGISTRY.csv (nullable)
    "notes",
)

VALID_CADENCES: frozenset[str] = frozenset({
    "", "weekly", "monthly", "quarterly", "event_driven",
})
