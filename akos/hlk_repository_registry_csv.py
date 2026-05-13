"""Field contract for REPOSITORY_REGISTRY.csv (Initiative 59 P1.1).

Canonical CSV lives under ``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPOSITORY_REGISTRY.csv``.
Mirrored to ``compliance.repository_registry_mirror`` on Supabase.

Repository = a tracked GitHub remote, with a class (platform / internal /
client-delivery / reference) and primary owner role. This dimension promotes the
existing markdown SSOT at ``docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/
REPOSITORIES_REGISTRY.md`` to a governed CSV (per **D-IH-59-C**), where the
markdown stays canonical for prose and the CSV becomes canonical for FK joins.

Sync between markdown and CSV is enforced by
``scripts/validate_repository_registry_md_csv_sync.py`` (CI-failing).

FK uses:

- ``INITIATIVE_REGISTRY.csv`` ``repo_slug`` → REPOSITORY_REGISTRY.repo_slug.
- ``COMPONENT_SERVICE_MATRIX.csv`` ``repo_slug`` → REPOSITORY_REGISTRY.repo_slug.
- ``REPO_HEALTH_SNAPSHOT.csv`` ``repo_slug`` → REPOSITORY_REGISTRY.repo_slug.
"""

from __future__ import annotations

# Keep in sync with docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPOSITORY_REGISTRY.csv header row.
REPOSITORY_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "repo_slug",            # ^[a-z0-9][a-z0-9-]{1,80}$ ; PRIMARY KEY
    "github_url",           # canonical https URL
    "class",                # platform | internal | client-delivery | reference
    "primary_owner_role",   # FK to baseline_organisation.csv role_name
    "topic_ids",            # semicolon-list FK to TOPIC_REGISTRY.csv
    "vault_doc_root",       # path under v3.0/Envoy Tech Lab/ or empty
    "api_spec_pointer",     # repo-relative path or "—"
    "api_topic_id",         # FK to TOPIC_REGISTRY.csv or "—"
    "lifecycle_status",     # active | archived | reference
    "notes",                # free-form
    # Initiative 63 P4 — cross-repo governance columns:
    "consumes_compliance_types",  # yes | no — drives scripts/regen_consumer_types.py
    "consumes_mirrors",           # ;-list of mirror names without .csv (e.g. PERSONA_REGISTRY;SKILL_REGISTRY)
    "local_path",                 # repo-relative path from ${REPO_ROOT}/.. for AKOS scripts to resolve consumer
)

VALID_REPO_CLASSES: frozenset[str] = frozenset({
    "platform", "internal", "client-delivery", "reference",
})

VALID_REPO_LIFECYCLE: frozenset[str] = frozenset({
    "active", "archived", "reference",
})
