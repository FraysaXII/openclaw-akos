#!/usr/bin/env python3
"""Bless an external Holistika-tracked repository with the AKOS governance kit.

Idempotent scaffolder that copies (or refreshes) the standard governance and
CI/CD artifacts into a consuming repository, validated against the canonical
``REPOSITORY_REGISTRY.csv``. Replaces the historical hand-copy workflow with a
deterministic, sha256-stamped pipeline so drift is detectable.

What it writes (stack-aware):

- ``.cursor/rules/akos-mirror.mdc`` (verbatim copy of the AKOS template)
- ``.cursor/rules/.akos-mirror.sha256`` (drift marker)
- ``EXTERNAL_REPO_CONTRACT.md`` (rendered from the canonical template)
- ``CONTRIBUTING.md`` (root, rendered from the contributing template)
- ``.github/PULL_REQUEST_TEMPLATE.md`` (rendered)
- ``.gitattributes`` (eol=lf normalisation; preserved if exists)

When stack detection (Track E) is implemented, the script also writes:

- ``.github/workflows/ci.yml`` (when missing)
- ``.github/dependabot.yml``
- ``.github/CODEOWNERS``
- ``.github/dependabot-auto-merge.yml`` (Track K1)
- ``docs/runbooks/branch-protection.md``
- ``.github/ISSUE_TEMPLATE/{bug,feature,governance,config}.yml``
- ``LICENSE`` (proprietary marker by default)
- Sentry / Slack / Postman / SBOM / SAST templates (opt-in via ``--with``)

Behavior:

- ``--dry-run``: print planned actions; never write.
- Without ``--force``: refuses to overwrite hand-edited files (existing files
  whose sha256 differs from a previous bless stamp). Untouched-since-bless
  files are refreshed automatically on every run.
- ``--force``: overwrite all bless-managed files unconditionally.
- ``--auto-pr`` (Track K2): when sha256 drift is detected for the mirror rule,
  open a PR via ``gh`` against the consumer with the corrected file. Skipped
  gracefully when ``gh`` is unavailable.
- Repos with ``class=reference`` in ``REPOSITORY_REGISTRY.csv`` are skipped
  (per D-IH-32-N: light-touch reference-only).

Usage::

    py scripts/bless_external_repo.py \\
        --repo-path c:/Users/Shadow/cd_shadow/root_cd/hlk-erp \\
        --repo-slug hlk-erp \\
        --dry-run

    py scripts/bless_external_repo.py --repo-slug hlk-erp --auto-pr  # nightly drift mode

Cross-references:

- ``docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/EXTERNAL_REPO_CONTRACT_TEMPLATE.md``
- ``docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/_templates/`` (this script's input)
- ``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPOSITORY_REGISTRY.csv`` (slug FK)
- ``.cursor/rules/akos-mirror-template.mdc`` (mirror rule template)
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import logging
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT
from akos.log import setup_logging

logger = logging.getLogger("akos.bless")

REGISTRY_CSV = (
    REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "REPOSITORY_REGISTRY.csv"
)
MIRROR_TEMPLATE = REPO_ROOT / ".cursor" / "rules" / "akos-mirror-template.mdc"
TEMPLATES_DIR = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Envoy Tech Lab"
    / "Repositories"
    / "_templates"
)
CONTRACT_TEMPLATE = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Envoy Tech Lab"
    / "Repositories"
    / "EXTERNAL_REPO_CONTRACT_TEMPLATE.md"
)
PR_TEMPLATE = TEMPLATES_DIR / "PR_TEMPLATE.template.md"
CONTRIB_TEMPLATE = TEMPLATES_DIR / "CONTRIBUTING.template.md"

CI_TEMPLATES_DIR = TEMPLATES_DIR / "ci"

REFERENCE_CLASS = "reference"


@dataclass
class RepoMeta:
    """Resolved registry row for a slug (column-tolerant for I63 additions)."""

    slug: str
    github_url: str
    repo_class: str
    primary_owner_role: str
    vault_doc_root: str
    lifecycle_status: str
    consumes_compliance_types: bool = False
    consumes_mirrors: tuple[str, ...] = ()
    relative_path: str = ""


# ---------------------------------------------------------------------------
# Registry helpers
# ---------------------------------------------------------------------------


def load_registry(csv_path: Path = REGISTRY_CSV) -> dict[str, RepoMeta]:
    """Parse ``REPOSITORY_REGISTRY.csv`` into a slug -> RepoMeta map.

    Tolerant of the I63 columns (``consumes_compliance_types``,
    ``consumes_mirrors`` semicolon-separated, ``local_path``): if absent,
    defaults are used. Final canonical schema landed at I63 P4.
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"REPOSITORY_REGISTRY.csv not found at {csv_path}")
    out: dict[str, RepoMeta] = {}
    with csv_path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            slug = (row.get("repo_slug") or "").strip()
            if not slug:
                continue
            consumes = (row.get("consumes_compliance_types") or "no").strip().lower() == "yes"
            mirrors_raw = (row.get("consumes_mirrors") or "").strip()
            mirrors: tuple[str, ...] = (
                tuple(m.strip() for m in mirrors_raw.split(";") if m.strip())
                if mirrors_raw
                else ()
            )
            out[slug] = RepoMeta(
                slug=slug,
                github_url=(row.get("github_url") or "").strip(),
                repo_class=(row.get("class") or "").strip(),
                primary_owner_role=(row.get("primary_owner_role") or "").strip(),
                vault_doc_root=(row.get("vault_doc_root") or "").strip(),
                lifecycle_status=(row.get("lifecycle_status") or "").strip(),
                consumes_compliance_types=consumes,
                consumes_mirrors=mirrors,
                relative_path=(row.get("local_path") or "").strip(),
            )
    return out


# ---------------------------------------------------------------------------
# File-write helpers (idempotent, drift-aware)
# ---------------------------------------------------------------------------


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    if not path.is_file():
        return ""
    return sha256_text(path.read_text(encoding="utf-8"))


def render_template(template_text: str, repo: RepoMeta) -> str:
    """Substitute placeholders in a template with values from RepoMeta."""
    return (
        template_text.replace("{{REPO_SLUG}}", repo.slug)
        .replace("{{REPO_CLASS}}", repo.repo_class)
        .replace("{{PRIMARY_OWNER_ROLE}}", repo.primary_owner_role)
        .replace("{{VAULT_DOC_ROOT}}", repo.vault_doc_root or "(none)")
        .replace("{{GITHUB_URL}}", repo.github_url)
    )


def write_if_drift(
    dest: Path,
    rendered: str,
    *,
    dry_run: bool,
    force: bool,
    label: str,
    stamp_path: Path | None = None,
) -> str:
    """Write `rendered` to `dest` when content differs.

    Returns one of: "WROTE", "SKIPPED_UNCHANGED", "REFUSED_HAND_EDIT", "DRY_WROTE".

    When `stamp_path` is supplied, the previous bless sha256 is read from it and
    compared against the current on-disk sha256 to detect hand edits since the
    last bless run. Hand-edited files are refused unless `force=True`.
    """
    new_hash = sha256_text(rendered)
    if not dest.exists():
        if dry_run:
            logger.info("[dry-run] would create %s (%s)", dest, label)
            return "DRY_WROTE"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(rendered, encoding="utf-8")
        if stamp_path is not None:
            stamp_path.parent.mkdir(parents=True, exist_ok=True)
            stamp_path.write_text(new_hash + "\n", encoding="utf-8")
        logger.info("wrote %s (%s)", dest, label)
        return "WROTE"

    current_hash = sha256_file(dest)
    if current_hash == new_hash:
        logger.debug("up-to-date %s (%s)", dest, label)
        return "SKIPPED_UNCHANGED"

    if not force and stamp_path is not None and stamp_path.is_file():
        stamped = stamp_path.read_text(encoding="utf-8").strip()
        if stamped and stamped != current_hash:
            logger.warning(
                "%s has hand-edits since last bless (current=%s, stamped=%s); rerun with --force to overwrite",
                dest, current_hash[:12], stamped[:12],
            )
            return "REFUSED_HAND_EDIT"

    if dry_run:
        logger.info(
            "[dry-run] would update %s (current=%s -> new=%s, %s)",
            dest, current_hash[:12], new_hash[:12], label,
        )
        return "DRY_WROTE"

    dest.write_text(rendered, encoding="utf-8")
    if stamp_path is not None:
        stamp_path.parent.mkdir(parents=True, exist_ok=True)
        stamp_path.write_text(new_hash + "\n", encoding="utf-8")
    logger.info("updated %s (%s)", dest, label)
    return "WROTE"


# ---------------------------------------------------------------------------
# Stack detection (Track E)
# ---------------------------------------------------------------------------


def detect_stack(repo_path: Path) -> dict[str, bool]:
    """Detect which CI/CD templates apply to a repo based on filesystem signals."""
    pkg_json = (repo_path / "package.json").is_file()
    pyproject = (repo_path / "pyproject.toml").is_file()
    requirements = (repo_path / "requirements.txt").is_file()
    has_supabase = (repo_path / "supabase" / "migrations").is_dir()
    has_workflows = (repo_path / ".github" / "workflows").is_dir()
    return {
        "is_node": pkg_json,
        "is_python": pyproject or requirements,
        "has_supabase_migrations": has_supabase,
        "has_workflows": has_workflows,
    }


# ---------------------------------------------------------------------------
# Auto-PR (Track K2): nightly drift fix via gh CLI
# ---------------------------------------------------------------------------


def open_drift_pr(repo_meta: RepoMeta, repo_path: Path, *, dry_run: bool) -> str:
    """Open a PR in the consumer to realign akos-mirror.mdc to the AKOS template.

    Returns one of: "OPENED", "EXISTS", "SKIPPED_NO_GH", "SKIPPED_DRY_RUN", "FAILED".
    """
    if dry_run:
        logger.info("[dry-run] would open drift-realign PR in %s", repo_meta.github_url)
        return "SKIPPED_DRY_RUN"

    if shutil.which("gh") is None:
        logger.warning("gh CLI not available; skipping auto-PR for %s", repo_meta.slug)
        return "SKIPPED_NO_GH"

    title = f"chore(governance): realign .cursor/rules/akos-mirror.mdc to AKOS template"
    repo_arg = repo_meta.github_url.replace("https://github.com/", "")
    try:
        existing = subprocess.run(
            ["gh", "pr", "list", "--repo", repo_arg, "--search", title, "--state", "open", "--json", "number"],
            capture_output=True, text=True, timeout=30, cwd=repo_path, check=False,
        )
        if existing.returncode == 0 and existing.stdout.strip() not in ("[]", ""):
            logger.info("drift PR already open for %s", repo_meta.slug)
            return "EXISTS"
    except Exception as exc:
        logger.warning("could not query existing PRs for %s: %s", repo_meta.slug, exc)

    body = (
        "Automated drift realignment from AKOS canonical template.\n\n"
        "The AKOS-side `.cursor/rules/akos-mirror-template.mdc` has been updated; this PR "
        "syncs the local copy to keep governance guardrails aligned.\n\n"
        "Source: https://github.com/FraysaXII/openclaw-akos/blob/main/.cursor/rules/akos-mirror-template.mdc\n"
    )

    try:
        result = subprocess.run(
            ["gh", "pr", "create", "--repo", repo_arg, "--title", title, "--body", body, "--base", "main"],
            capture_output=True, text=True, timeout=60, cwd=repo_path, check=False,
        )
        if result.returncode == 0:
            logger.info("opened drift PR for %s", repo_meta.slug)
            return "OPENED"
        logger.error("gh pr create failed for %s: %s", repo_meta.slug, result.stderr.strip())
        return "FAILED"
    except Exception as exc:
        logger.error("auto-PR error for %s: %s", repo_meta.slug, exc)
        return "FAILED"


# ---------------------------------------------------------------------------
# Bless orchestrator
# ---------------------------------------------------------------------------


def _resolve_repo_path(repo: RepoMeta, override: Path | None) -> Path | None:
    if override is not None:
        return override
    if repo.relative_path:
        candidate = (REPO_ROOT.parent / repo.relative_path).resolve()
        if candidate.is_dir():
            return candidate
    return None


def bless_repo(
    *,
    repo_meta: RepoMeta,
    repo_path: Path,
    dry_run: bool = False,
    force: bool = False,
    auto_pr: bool = False,
    with_features: Iterable[str] = (),
) -> dict[str, str]:
    """Apply governance + CI/CD artifacts to one consumer repo.

    Returns a dict of {label: outcome} for caller-side reporting.
    """
    results: dict[str, str] = {}

    if repo_meta.repo_class.lower() == REFERENCE_CLASS:
        logger.info("skipping %s: class=reference (D-IH-32-N light-touch)", repo_meta.slug)
        results["overall"] = "SKIPPED_REFERENCE"
        return results

    if not repo_path.is_dir():
        logger.error("repo path %s is not a directory; nothing to bless", repo_path)
        results["overall"] = "FAILED_NO_PATH"
        return results

    # 1. Cursor mirror rule (verbatim, sha-stamped).
    mirror_dest = repo_path / ".cursor" / "rules" / "akos-mirror.mdc"
    stamp_dest = repo_path / ".cursor" / "rules" / ".akos-mirror.sha256"
    mirror_text = MIRROR_TEMPLATE.read_text(encoding="utf-8")
    drift_before = mirror_dest.is_file() and sha256_file(mirror_dest) != sha256_text(mirror_text)
    results["akos-mirror.mdc"] = write_if_drift(
        mirror_dest, mirror_text, dry_run=dry_run, force=force, label="cursor mirror rule",
        stamp_path=stamp_dest,
    )

    # 2. EXTERNAL_REPO_CONTRACT.md
    contract_dest = repo_path / "EXTERNAL_REPO_CONTRACT.md"
    contract_text = render_template(
        CONTRACT_TEMPLATE.read_text(encoding="utf-8"), repo_meta
    )
    contract_stamp = repo_path / ".github" / ".akos-bless" / "external_repo_contract.sha256"
    results["EXTERNAL_REPO_CONTRACT.md"] = write_if_drift(
        contract_dest, contract_text, dry_run=dry_run, force=force, label="contract",
        stamp_path=contract_stamp,
    )

    # 3. Root CONTRIBUTING.md (if missing or force).
    contrib_dest = repo_path / "CONTRIBUTING.md"
    contrib_text = render_template(CONTRIB_TEMPLATE.read_text(encoding="utf-8"), repo_meta)
    contrib_stamp = repo_path / ".github" / ".akos-bless" / "contributing.sha256"
    results["CONTRIBUTING.md"] = write_if_drift(
        contrib_dest, contrib_text, dry_run=dry_run, force=force, label="contributing",
        stamp_path=contrib_stamp,
    )

    # 4. .github/PULL_REQUEST_TEMPLATE.md
    pr_dest = repo_path / ".github" / "PULL_REQUEST_TEMPLATE.md"
    pr_text = render_template(PR_TEMPLATE.read_text(encoding="utf-8"), repo_meta)
    pr_stamp = repo_path / ".github" / ".akos-bless" / "pull_request_template.sha256"
    results["PULL_REQUEST_TEMPLATE.md"] = write_if_drift(
        pr_dest, pr_text, dry_run=dry_run, force=force, label="PR template", stamp_path=pr_stamp,
    )

    # 5. .gitattributes (only when missing — never overwrite without --force).
    gitattr_dest = repo_path / ".gitattributes"
    if not gitattr_dest.exists() or force:
        gitattr_template = CI_TEMPLATES_DIR / "gitattributes.template"
        if gitattr_template.is_file():
            gitattr_text = gitattr_template.read_text(encoding="utf-8")
            results[".gitattributes"] = write_if_drift(
                gitattr_dest, gitattr_text, dry_run=dry_run, force=True, label=".gitattributes",
            )
        else:
            results[".gitattributes"] = "SKIPPED_NO_TEMPLATE"
    else:
        results[".gitattributes"] = "SKIPPED_PRESENT"

    # 6. Stack-aware CI/CD templates (Track E).
    stack = detect_stack(repo_path)
    results["_stack"] = (
        f"node={stack['is_node']} python={stack['is_python']} "
        f"supabase={stack['has_supabase_migrations']} workflows={stack['has_workflows']}"
    )

    ci_artifacts: list[tuple[str, Path, Path]] = []  # (label, template_path, dest_path)
    if (CI_TEMPLATES_DIR / "ci.yml.template").is_file():
        ci_artifacts.append(("ci.yml", CI_TEMPLATES_DIR / "ci.yml.template", repo_path / ".github" / "workflows" / "ci.yml"))
    if (CI_TEMPLATES_DIR / "dependabot.yml.template").is_file():
        ci_artifacts.append(("dependabot.yml", CI_TEMPLATES_DIR / "dependabot.yml.template", repo_path / ".github" / "dependabot.yml"))
    if (CI_TEMPLATES_DIR / "CODEOWNERS.template").is_file():
        ci_artifacts.append(("CODEOWNERS", CI_TEMPLATES_DIR / "CODEOWNERS.template", repo_path / ".github" / "CODEOWNERS"))
    if (CI_TEMPLATES_DIR / "branch-protection-runbook.template.md").is_file():
        ci_artifacts.append((
            "branch-protection.md",
            CI_TEMPLATES_DIR / "branch-protection-runbook.template.md",
            repo_path / "docs" / "runbooks" / "branch-protection.md",
        ))
    if (CI_TEMPLATES_DIR / "dependabot-auto-merge.yml.template").is_file() and stack["is_node"]:
        ci_artifacts.append((
            "dependabot-auto-merge.yml",
            CI_TEMPLATES_DIR / "dependabot-auto-merge.yml.template",
            repo_path / ".github" / "workflows" / "dependabot-auto-merge.yml",
        ))
    # Stack-aware Node-only artefacts
    if stack["is_node"]:
        if (CI_TEMPLATES_DIR / "lint-staged.config.template.json").is_file():
            ci_artifacts.append((
                "lint-staged.config.json",
                CI_TEMPLATES_DIR / "lint-staged.config.template.json",
                repo_path / ".lintstagedrc.json",
            ))
        if (CI_TEMPLATES_DIR / "commitlint.config.template.cjs").is_file():
            ci_artifacts.append((
                "commitlint.config.cjs",
                CI_TEMPLATES_DIR / "commitlint.config.template.cjs",
                repo_path / "commitlint.config.cjs",
            ))
        if (CI_TEMPLATES_DIR / "husky-pre-commit.template.sh").is_file():
            ci_artifacts.append((
                "husky-pre-commit",
                CI_TEMPLATES_DIR / "husky-pre-commit.template.sh",
                repo_path / ".husky" / "pre-commit",
            ))
    # Stack-aware Supabase artefact
    if stack["has_supabase_migrations"]:
        if (CI_TEMPLATES_DIR / "supabase-migration-lint.yml.template").is_file():
            ci_artifacts.append((
                "supabase-migration-lint.yml",
                CI_TEMPLATES_DIR / "supabase-migration-lint.yml.template",
                repo_path / ".github" / "workflows" / "supabase-migration-lint.yml",
            ))
    # Opt-in pipeline extensions via --with
    if "semgrep" in with_features and (CI_TEMPLATES_DIR / "sast-semgrep.yml.template").is_file():
        ci_artifacts.append((
            "sast.yml",
            CI_TEMPLATES_DIR / "sast-semgrep.yml.template",
            repo_path / ".github" / "workflows" / "sast.yml",
        ))
    if "sbom" in with_features and (CI_TEMPLATES_DIR / "sbom.yml.template").is_file():
        ci_artifacts.append((
            "sbom.yml",
            CI_TEMPLATES_DIR / "sbom.yml.template",
            repo_path / ".github" / "workflows" / "sbom.yml",
        ))
    if "codecov" in with_features:
        if (CI_TEMPLATES_DIR / "codecov.yml.template").is_file():
            ci_artifacts.append((
                "codecov.yml",
                CI_TEMPLATES_DIR / "codecov.yml.template",
                repo_path / "codecov.yml",
            ))
        if (CI_TEMPLATES_DIR / "codecov-workflow.yml.template").is_file():
            ci_artifacts.append((
                "codecov-workflow.yml",
                CI_TEMPLATES_DIR / "codecov-workflow.yml.template",
                repo_path / ".github" / "workflows" / "codecov.yml",
            ))
    if "semantic-release" in with_features:
        if (CI_TEMPLATES_DIR / "semantic-release.config.template.json").is_file():
            ci_artifacts.append((
                "release.config.json",
                CI_TEMPLATES_DIR / "semantic-release.config.template.json",
                repo_path / "release.config.json",
            ))
        if (CI_TEMPLATES_DIR / "semantic-release-workflow.yml.template").is_file():
            ci_artifacts.append((
                "release.yml",
                CI_TEMPLATES_DIR / "semantic-release-workflow.yml.template",
                repo_path / ".github" / "workflows" / "release.yml",
            ))

    for label, src, dest in ci_artifacts:
        if dest.exists() and not force:
            results[label] = "SKIPPED_PRESENT"
            continue
        rendered = render_template(src.read_text(encoding="utf-8"), repo_meta)
        stamp = repo_path / ".github" / ".akos-bless" / f"{label}.sha256"
        results[label] = write_if_drift(
            dest, rendered, dry_run=dry_run, force=force, label=label, stamp_path=stamp,
        )

    # 7. Issue templates (Track I) — directory-level idempotency.
    # Templates live in _templates/issue/{bug,feature,governance}.yml.template; rendered into
    # <repo>/.github/ISSUE_TEMPLATE/{bug,feature,governance}.yml.
    issue_templates_dir = TEMPLATES_DIR / "issue"
    if issue_templates_dir.is_dir():
        for src in sorted(issue_templates_dir.iterdir()):
            if not src.is_file() or not src.name.endswith(".template"):
                continue
            dest_name = src.name.replace(".yml.template", ".yml")
            dest = repo_path / ".github" / "ISSUE_TEMPLATE" / dest_name
            if dest.exists() and not force:
                results[f"ISSUE_TEMPLATE/{dest_name}"] = "SKIPPED_PRESENT"
                continue
            rendered = render_template(src.read_text(encoding="utf-8"), repo_meta)
            stamp = repo_path / ".github" / ".akos-bless" / f"issue_{dest_name}.sha256"
            results[f"ISSUE_TEMPLATE/{dest_name}"] = write_if_drift(
                dest, rendered, dry_run=dry_run, force=force, label=f"issue:{dest_name}", stamp_path=stamp,
            )

    # 8. LICENSE (Track I) — only when missing; never overwrite without --force.
    # LICENSE.template lives at _templates/LICENSE.template (root of templates dir).
    license_template = TEMPLATES_DIR / "LICENSE.template"
    license_dest = repo_path / "LICENSE"
    if license_template.is_file():
        if license_dest.exists() and not force:
            results["LICENSE"] = "SKIPPED_PRESENT"
        else:
            results["LICENSE"] = write_if_drift(
                license_dest, render_template(license_template.read_text(encoding="utf-8"), repo_meta),
                dry_run=dry_run, force=force, label="LICENSE",
            )

    # 9. Sentry templates (Track H) — opt-in; only render when --with sentry.
    if "sentry" in with_features:
        for client_kind in ("client", "server", "edge"):
            src = CI_TEMPLATES_DIR / f"sentry.{client_kind}.config.template.ts"
            if not src.is_file():
                continue
            dest = repo_path / f"sentry.{client_kind}.config.ts"
            if dest.exists() and not force:
                results[f"sentry.{client_kind}.config.ts"] = "SKIPPED_PRESENT"
                continue
            results[f"sentry.{client_kind}.config.ts"] = write_if_drift(
                dest, render_template(src.read_text(encoding="utf-8"), repo_meta),
                dry_run=dry_run, force=force, label=f"sentry-{client_kind}",
            )

    # 10. Slack monitoring templates (Track H) — opt-in.
    if "slack" in with_features:
        slack_lib = CI_TEMPLATES_DIR / "lib_monitoring_slack.template.ts"
        if slack_lib.is_file():
            dest = repo_path / "lib" / "monitoring" / "slack.ts"
            if dest.exists() and not force:
                results["lib/monitoring/slack.ts"] = "SKIPPED_PRESENT"
            else:
                results["lib/monitoring/slack.ts"] = write_if_drift(
                    dest, render_template(slack_lib.read_text(encoding="utf-8"), repo_meta),
                    dry_run=dry_run, force=force, label="slack-lib",
                )
        verdict_route = CI_TEMPLATES_DIR / "verdict_flip_route.template.ts"
        if verdict_route.is_file() and stack["is_node"]:
            dest = repo_path / "app" / "api" / "monitoring" / "verdict-flip" / "route.ts"
            if dest.exists() and not force:
                results["app/api/monitoring/verdict-flip/route.ts"] = "SKIPPED_PRESENT"
            else:
                results["app/api/monitoring/verdict-flip/route.ts"] = write_if_drift(
                    dest, render_template(verdict_route.read_text(encoding="utf-8"), repo_meta),
                    dry_run=dry_run, force=force, label="verdict-flip-route",
                )

    # 10b. Browser smoke (Track H) — opt-in via `browser-smoke` feature flag.
    if "browser-smoke" in with_features:
        smoke_template = CI_TEMPLATES_DIR / "browser-smoke.template.ts"
        if smoke_template.is_file() and stack["is_node"]:
            dest = repo_path / "scripts" / "browser-smoke.ts"
            if dest.exists() and not force:
                results["scripts/browser-smoke.ts"] = "SKIPPED_PRESENT"
            else:
                results["scripts/browser-smoke.ts"] = write_if_drift(
                    dest, render_template(smoke_template.read_text(encoding="utf-8"), repo_meta),
                    dry_run=dry_run, force=force, label="browser-smoke",
                )

    # 11. Postman (Track J) — opt-in via `postman` feature flag.
    if "postman" in with_features:
        coll_template = CI_TEMPLATES_DIR / "postman_collection.template.json"
        readme_template = CI_TEMPLATES_DIR / "postman_README.template.md"
        newman_template = CI_TEMPLATES_DIR / "newman.yml.template"
        if coll_template.is_file():
            dest = repo_path / "postman" / f"{repo_meta.slug}.postman_collection.json"
            if dest.exists() and not force:
                results["postman/collection"] = "SKIPPED_PRESENT"
            else:
                results["postman/collection"] = write_if_drift(
                    dest, render_template(coll_template.read_text(encoding="utf-8"), repo_meta),
                    dry_run=dry_run, force=force, label="postman-coll",
                )
        if readme_template.is_file():
            dest = repo_path / "postman" / "README.md"
            if dest.exists() and not force:
                results["postman/README"] = "SKIPPED_PRESENT"
            else:
                results["postman/README"] = write_if_drift(
                    dest, render_template(readme_template.read_text(encoding="utf-8"), repo_meta),
                    dry_run=dry_run, force=force, label="postman-readme",
                )
        if newman_template.is_file():
            dest = repo_path / ".github" / "workflows" / "newman.yml"
            if dest.exists() and not force:
                results["newman.yml"] = "SKIPPED_PRESENT"
            else:
                results["newman.yml"] = write_if_drift(
                    dest, render_template(newman_template.read_text(encoding="utf-8"), repo_meta),
                    dry_run=dry_run, force=force, label="newman",
                )

    # 12. Auto-PR for drift detection (Track K2).
    if auto_pr and drift_before and not dry_run:
        results["auto_pr"] = open_drift_pr(repo_meta, repo_path, dry_run=dry_run)

    results["overall"] = "OK"
    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bless an external Holistika-tracked repository")
    parser.add_argument("--repo-slug", required=True, help="Slug from REPOSITORY_REGISTRY.csv")
    parser.add_argument("--repo-path", help="Absolute or repo-relative path to the consumer's working tree")
    parser.add_argument("--dry-run", action="store_true", help="Print planned actions; never write")
    parser.add_argument("--force", action="store_true", help="Overwrite hand-edited bless-managed files")
    parser.add_argument("--auto-pr", action="store_true", help="Open a gh PR when drift detected (nightly mode)")
    parser.add_argument(
        "--with",
        dest="with_features",
        action="append",
        default=[],
        help=(
            "Opt-in templates: sentry / slack / postman / sbom / semgrep / "
            "codecov / semantic-release / browser-smoke / supabase-lint"
        ),
    )
    parser.add_argument("--json-log", action="store_true")
    args = parser.parse_args(list(argv) if argv is not None else None)

    setup_logging(json_output=args.json_log)

    try:
        registry = load_registry()
    except FileNotFoundError as exc:
        logger.error("%s", exc)
        return 1

    repo_meta = registry.get(args.repo_slug)
    if repo_meta is None:
        logger.error("slug '%s' not found in REPOSITORY_REGISTRY.csv (known: %s)",
                     args.repo_slug, sorted(registry))
        return 2

    override_path = Path(args.repo_path).resolve() if args.repo_path else None
    repo_path = _resolve_repo_path(repo_meta, override_path)
    if repo_path is None:
        logger.error(
            "could not resolve a working tree for '%s'; pass --repo-path or set the path "
            "column in REPOSITORY_REGISTRY.csv (I63)", args.repo_slug,
        )
        return 3

    logger.info("blessing %s at %s (class=%s, dry_run=%s, force=%s, auto_pr=%s)",
                repo_meta.slug, repo_path, repo_meta.repo_class, args.dry_run, args.force, args.auto_pr)

    results = bless_repo(
        repo_meta=repo_meta,
        repo_path=repo_path,
        dry_run=args.dry_run,
        force=args.force,
        auto_pr=args.auto_pr,
        with_features=tuple(args.with_features),
    )

    print()
    print("=" * 56)
    print(f"  bless: {repo_meta.slug}")
    print("=" * 56)
    for label, outcome in results.items():
        if label.startswith("_"):
            continue
        print(f"  [{outcome:>22}] {label}")
    print()

    overall = results.get("overall", "FAILED")
    if overall in {"OK", "SKIPPED_REFERENCE"}:
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
