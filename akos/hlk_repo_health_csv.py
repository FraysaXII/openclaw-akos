"""Field contract for REPO_HEALTH_SNAPSHOT.csv (Initiative 32 P7 / v0.2 P8).

Canonical CSV lives under ``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/``.
Mirrored to ``compliance.repo_health_snapshot_mirror`` on Supabase (operational
mirror; same posture as ``finops.registered_fact``).

D-IH-32-L: cross-repo extraction is **pull-based**. AKOS reads external repo
state (``boilerplate``, ``hlk-erp``, ``kirbe``) into this CSV via
``scripts/snapshot_external_repos.py``. KiRBe and ERP push nothing to AKOS
authoring surfaces. Snapshot cadence: weekly (cron) + on-demand.

Each row captures a snapshot of one external repo's HLK doctrine compliance:
EXTERNAL_REPO_CONTRACT.md presence, akos-mirror.mdc cursor rule presence,
language-frontmatter compliance percentage, brand-jargon violation count.
Drift detection over time: a 4-consecutive-week regression on any external
repo triggers Initiative 42 (cross-repo CI integration).
"""

from __future__ import annotations

# Keep in sync with docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPO_HEALTH_SNAPSHOT.csv header row.
REPO_HEALTH_SNAPSHOT_FIELDNAMES: tuple[str, ...] = (
    "repo_slug",                              # FK to REPOSITORIES_REGISTRY.md
    "snapshot_date",                          # YYYY-MM-DD
    "commit_sha_at_snapshot",                 # short SHA or 'unknown' if not a git clone
    "cursor_rule_count",                      # int — rules under .cursor/rules/
    "has_external_repo_contract",             # true | false
    "has_akos_mirror_rule",                   # true | false (.cursor/rules/akos-mirror.mdc presence)
    "language_frontmatter_compliance_pct",    # float in [0.0, 100.0]; only on .md files
    "brand_jargon_violations",                # int (informational; per BRAND_JARGON_AUDIT.md §4)
    "embedded_obsidian_snapshot_present",     # true | false (boilerplate-specific)
    # CI/CD posture columns (Track G — bless pattern):
    "ci_workflow_present",                    # true | false (.github/workflows/ci.yml exists)
    "dependabot_present",                     # true | false (.github/dependabot.yml exists)
    "codeowners_present",                     # true | false (.github/CODEOWNERS exists)
    "license_present",                        # true | false (LICENSE | LICENSE.md | LICENSE.txt at root)
    "akos_mirror_sha256_match",               # true | false (sha256 vs AKOS template; '' when N/A)
    "secret_rotation_oldest_age_days",        # int days (0 if no runbook); -1 when unknown
    "notes",
)
