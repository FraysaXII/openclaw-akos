"""Field contract for REPOSITORY_REGISTRY.csv (Initiative 59 P1.1 + I86 Wave H).

Canonical CSV lives under ``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPOSITORY_REGISTRY.csv``.
Mirrored to ``compliance.repository_registry_mirror`` on Supabase.

Repository = a tracked GitHub remote, with a class (platform / internal /
client-delivery / reference) and primary owner role. This dimension promotes the
existing markdown SSOT at ``docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/
REPOSITORIES_REGISTRY.md`` to a governed CSV (per **D-IH-59-C**), where the
markdown stays canonical for prose and the CSV becomes canonical for FK joins.

Sync between markdown and CSV is enforced by
``scripts/validate_repository_registry_md_csv_sync.py`` (CI-failing).

I86 Wave H schema extension (17 → 29 columns) per **D-IH-86-AC** (app-governance
scope) and **D-IH-86-AD** (12-column extension). Adds the orthogonal ``app_class``
axis (production / research / experiment / template / fork / archive /
uncategorized), the ``governance_status`` axis (governed / inventoried /
unmanaged / archived), and ten projection/observability columns to close the
92.7% unmanaged-repo gap surfaced by Lane F-GITHUB report
(``docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/
lane-f-app-governance-inventory-2026-05-19.md``). All 12 new columns are nullable
in the migration per backwards-compat posture (existing 7 rows continue to load);
the validator promotes ``app_class`` + ``governance_status`` to FAIL after the
Lane F-AUTHOR-2 backfill commit lands (I66 INFO→FAIL ramp pattern) via the
``--strict-app-class`` flag in ``scripts/validate_repository_registry.py``.

The existing ``class`` axis (platform / internal / client-delivery / reference)
stays unchanged — it encodes the AKOS-governance relationship; ``app_class``
encodes the artifact-purpose axis. The two axes are orthogonal and compound
(per Lane F report §5; mirrors the audience × format axes pattern in
``akos-external-render-discipline.mdc``).

FK uses:

- ``INITIATIVE_REGISTRY.csv`` ``repo_slug`` → REPOSITORY_REGISTRY.repo_slug.
- ``COMPONENT_SERVICE_MATRIX.csv`` ``repo_slug`` → REPOSITORY_REGISTRY.repo_slug.
- ``REPO_HEALTH_SNAPSHOT.csv`` ``repo_slug`` → REPOSITORY_REGISTRY.repo_slug.
- ``related_initiative_ids`` (I86 Wave H) → ``INITIATIVE_REGISTRY.csv`` ``initiative_id``.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

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
    "local_path",  # repo-relative path from ${REPO_ROOT}/.. for AKOS scripts to resolve consumer
    "last_review_at",                  # I71 P4 follow-up (D-IH-71-R) review-stamp (DATE; ISO YYYY-MM-DD)
    "last_review_by",                  # I71 P4 follow-up (D-IH-71-R) review-stamp (FK-by-convention to baseline_organisation.csv role_name)
    "last_review_decision_id",         # I71 P4 follow-up (D-IH-71-R) review-stamp (FK-by-convention to DECISION_REGISTER.csv decision_id; nullable)
    "methodology_version_at_review",   # I71 P4 follow-up (D-IH-71-R) review-stamp (LOGIC_CHANGE_LOG.md methodology version at review time; vMAJOR.MINOR per D-IH-71-D)
    # I86 Wave H schema extension (D-IH-86-AC + D-IH-86-AD) — 12 new columns; all nullable
    # in migration; validator promotes app_class + governance_status to FAIL after backfill.
    "app_class",                       # production | research | experiment | template | fork | archive | uncategorized
    "metadata_tags",                   # ;-list lowercase free-form tags (mirror of operator-driven categorisation)
    "github_topics",                   # ;-list mirror of repositoryTopics[].name from gh api (advisory only)
    "github_visibility",               # PUBLIC | PRIVATE | INTERNAL
    "primary_language",                # GH-reported primary language (e.g. TypeScript, Python, Markdown); empty for empty repos
    "created_at",                      # YYYY-MM-DD (mirrored from GH createdAt)
    "pushed_at",                       # YYYY-MM-DD (mirrored from GH pushedAt; drives staleness/archival sweep)
    "last_inventory_at",               # YYYY-MM-DD (when registry last ran a GH sweep for this row)
    "governance_status",               # governed | inventoried | unmanaged | archived
    "related_initiative_ids",          # ;-list FK to INITIATIVE_REGISTRY.csv initiative_id (e.g. I76;I86)
    "codeowners_present",              # true | false (parsed from .github/CODEOWNERS or repo root); empty when unknown
    "branch_protection_enabled",       # true | false (queried from GH API at inventory time); empty when unknown
)

VALID_REPO_CLASSES: frozenset[str] = frozenset({
    "platform", "internal", "client-delivery", "reference",
})

VALID_REPO_LIFECYCLE: frozenset[str] = frozenset({
    "active", "archived", "reference",
})

# I86 Wave H — three new enum frozensets per D-IH-86-AD.

VALID_APP_CLASS: frozenset[str] = frozenset({
    "production",     # the 4 currently-blessed: openclaw-akos, hlk-erp, boilerplate, kirbe
    "research",       # AKOS-internal R&D outputs (paper code, framework explorations)
    "experiment",     # throwaway / spike / POC — lowest-touch governance
    "template",       # boilerplate the operator forks for new projects (no governance contract)
    "fork",           # tracked upstream fork (no AKOS contract beyond inventory)
    "archive",        # retired (mirrors lifecycle_status=archived; flipped on GH isArchived=true)
    "uncategorized",  # awaiting operator classification (default for newly-discovered repos)
})

VALID_GOVERNANCE_STATUS: frozenset[str] = frozenset({
    "governed",      # full SOP + bless contract; CODEOWNERS + branch protection required
    "inventoried",   # classified + tagged, not yet blessed (default for backfilled rows)
    "unmanaged",     # in GitHub, NOT in registry (transient; should not persist after sweep)
    "archived",      # retired (mirrors app_class=archive)
})

VALID_GITHUB_VISIBILITY: frozenset[str] = frozenset({
    "PUBLIC",
    "PRIVATE",
    "INTERNAL",  # GitHub Enterprise visibility tier; recorded for future Enterprise org migration
})


_ISO_DATE_PATTERN = r"^\d{4}-\d{2}-\d{2}$"


class RepositoryRegistryRow(BaseModel):
    """Pydantic frozen BaseModel for one row of REPOSITORY_REGISTRY.csv.

    Per ``CONTRIBUTING.md`` §"Python Code Standards" and
    ``akos-holistika-operations.mdc`` §"New git-canonical compliance registers":
    frozen BaseModel + Literal enums for governed columns + slug regex on
    repo_slug + nullable annotations on every column that ships nullable in the
    canonical CSV.

    The 29 columns are SSOT per D-IH-59-C (initial 13 cols) + D-IH-63-A (3 cross-repo
    cols) + D-IH-71-R (4 review-stamp cols) + D-IH-86-AC/AD (12 app-governance cols).
    The first 17 columns are kept as permissive ``str`` with default empty string so
    the existing 7 canonical rows continue to round-trip cleanly; the 12 new
    columns ship nullable (``None`` accepted) per I86 Wave H backwards-compat posture.
    Validators promote ``app_class`` + ``governance_status`` to required after the
    Lane F-AUTHOR-2 backfill commit lands (``--strict-app-class`` flag in the
    paired validator script).
    """

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    # Existing 17 columns (kept permissive for backwards-compat with the 7 canonical
    # rows; the legacy validator script enforces the stricter row-level rules).
    repo_slug: str = Field(
        ...,
        pattern=r"^[a-z0-9][a-z0-9-]{1,80}$",
        min_length=2,
        max_length=81,
        description="Stable slug; PRIMARY KEY; matches ^[a-z0-9][a-z0-9-]{1,80}$",
    )
    github_url: str = Field(default="", max_length=512)
    class_: str = Field(default="", alias="class", max_length=64)
    primary_owner_role: str = Field(default="", max_length=128)
    topic_ids: str = Field(default="", max_length=2048)
    vault_doc_root: str = Field(default="", max_length=512)
    api_spec_pointer: str = Field(default="", max_length=512)
    api_topic_id: str = Field(default="", max_length=128)
    lifecycle_status: str = Field(default="", max_length=64)
    notes: str = Field(default="", max_length=4096)
    consumes_compliance_types: str = Field(default="", max_length=32)
    consumes_mirrors: str = Field(default="", max_length=1024)
    local_path: str = Field(default="", max_length=512)
    last_review_at: str = Field(default="", max_length=32)
    last_review_by: str = Field(default="", max_length=128)
    last_review_decision_id: str = Field(default="", max_length=64)
    methodology_version_at_review: str = Field(default="", max_length=16)

    # I86 Wave H — 12 new nullable columns per D-IH-86-AD.
    app_class: Literal[
        "production",
        "research",
        "experiment",
        "template",
        "fork",
        "archive",
        "uncategorized",
    ] | None = Field(
        default=None,
        description=(
            "Per D-IH-86-AD: artifact-purpose axis (orthogonal to class). "
            "Nullable in migration; promoted to required after Lane F-AUTHOR-2 backfill."
        ),
    )
    metadata_tags: str = Field(
        default="",
        max_length=1024,
        description="Per D-IH-86-AD: semicolon-list of operator-driven lowercase tags (mirror of github_topics).",
    )
    github_topics: str = Field(
        default="",
        max_length=1024,
        description="Per D-IH-86-AD: semicolon-list mirror of GH repositoryTopics[].name (advisory only per GOV.UK ADR-0017).",
    )
    github_visibility: Literal["PUBLIC", "PRIVATE", "INTERNAL"] | None = Field(
        default=None,
        description="Per D-IH-86-AD: cross-check vs GitHub API; flags drift when operator changes visibility outside the registry.",
    )
    primary_language: str | None = Field(
        default=None,
        max_length=64,
        description="Per D-IH-86-AD: GH-reported primary language (e.g., TypeScript, Python, Markdown); empty for empty repos.",
    )
    created_at: str | None = Field(
        default=None,
        pattern=_ISO_DATE_PATTERN,
        description="Per D-IH-86-AD: ISO date YYYY-MM-DD (mirrored from GH createdAt).",
    )
    pushed_at: str | None = Field(
        default=None,
        pattern=_ISO_DATE_PATTERN,
        description="Per D-IH-86-AD: ISO date YYYY-MM-DD (mirrored from GH pushedAt; drives staleness/archival sweep).",
    )
    last_inventory_at: str | None = Field(
        default=None,
        pattern=_ISO_DATE_PATTERN,
        description="Per D-IH-86-AD: ISO date YYYY-MM-DD (when registry last ran a GH sweep for this row).",
    )
    governance_status: Literal[
        "governed",
        "inventoried",
        "unmanaged",
        "archived",
    ] | None = Field(
        default=None,
        description=(
            "Per D-IH-86-AD: AKOS governance posture. "
            "Nullable in migration; promoted to required after Lane F-AUTHOR-2 backfill."
        ),
    )
    related_initiative_ids: str = Field(
        default="",
        max_length=512,
        description="Per D-IH-86-AD: semicolon-list FK to INITIATIVE_REGISTRY.csv initiative_id (e.g. I76;I86).",
    )
    codeowners_present: bool | None = Field(
        default=None,
        description="Per D-IH-86-AD: parsed from .github/CODEOWNERS or repo root; drift signal for governed repos.",
    )
    branch_protection_enabled: bool | None = Field(
        default=None,
        description="Per D-IH-86-AD: queried from GH API at inventory time; drift signal for governed repos.",
    )


CSV_PATH_RELATIVE: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/"
    "REPOSITORY_REGISTRY.csv"
)
