#!/usr/bin/env python3
"""Verify governance posture of every non-reference Holistika-tracked repo.

Reads ``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPOSITORY_REGISTRY.csv`` and the
latest ``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPO_HEALTH_SNAPSHOT.csv`` row per
slug, then enforces:

1. ``has_external_repo_contract`` is ``true`` for every non-reference repo.
2. ``has_akos_mirror_rule`` is ``true`` for repos with a ``.cursor/rules/``
   directory (boilerplate exempt per D-IH-32-N).
3. The local copy of ``EXTERNAL_REPO_CONTRACT.md`` (when reachable) declares
   ``last_review:`` within the last ``--freshness-days`` (default 90).
4. The local copy of ``.cursor/rules/akos-mirror.mdc`` (when reachable) is
   sha256-identical to the canonical AKOS template
   ``.cursor/rules/akos-mirror-template.mdc``.

Usage::

    py scripts/check_external_repo_contract.py
    py scripts/check_external_repo_contract.py --freshness-days 60
    py scripts/check_external_repo_contract.py --json-log

Exit codes:
    0 -- all checks pass.
    1 -- one or more checks fail.

Wired into ``scripts/release-gate.py`` via ``run_external_repo_contract_check()``.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import logging
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT
from akos.log import setup_logging

logger = logging.getLogger("akos.repo-contract")

REGISTRY_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "REPOSITORY_REGISTRY.csv"
SNAPSHOT_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "REPO_HEALTH_SNAPSHOT.csv"
MIRROR_TEMPLATE = REPO_ROOT / ".cursor" / "rules" / "akos-mirror-template.mdc"

DEFAULT_FRESHNESS_DAYS = 90

# Re-uses the same path map convention as snapshot_external_repos.py.
DEFAULT_REPO_PATHS: dict[str, Path] = {
    "boilerplate": Path(r"c:\Users\Shadow\cd_shadow\root_cd\boilerplate"),
    "hlk-erp": Path(r"c:\Users\Shadow\cd_shadow\root_cd\hlk-erp"),
    "kirbe-platform": Path(r"c:\Users\Shadow\cd_shadow\root_cd\kirbe"),
}

LAST_REVIEW_RE = re.compile(r"^last_review:\s*(\d{4}-\d{2}-\d{2})\s*$", re.MULTILINE)


def _resolve_repo_paths() -> dict[str, Path]:
    override = os.environ.get("AKOS_EXTERNAL_REPO_ROOTS")
    if override:
        try:
            import json
            data = json.loads(override)
            return {k: Path(v) for k, v in data.items()}
        except Exception:
            pass
    return DEFAULT_REPO_PATHS


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _load_registry() -> list[dict[str, str]]:
    with REGISTRY_CSV.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _load_latest_snapshot() -> dict[str, dict[str, str]]:
    if not SNAPSHOT_CSV.is_file():
        return {}
    out: dict[str, dict[str, str]] = {}
    with SNAPSHOT_CSV.open("r", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            slug = row.get("repo_slug", "").strip()
            if slug:
                out[slug] = row
    return out


def _last_review_age_days(contract_path: Path) -> int | None:
    if not contract_path.is_file():
        return None
    try:
        text = contract_path.read_text(encoding="utf-8")
    except Exception:
        return None
    m = LAST_REVIEW_RE.search(text)
    if not m:
        return None
    try:
        last_review = datetime.strptime(m.group(1), "%Y-%m-%d").date()
    except ValueError:
        return None
    return (date.today() - last_review).days


def _check_one(
    row: dict[str, str],
    snapshot_row: dict[str, str] | None,
    repo_path: Path | None,
    freshness_days: int,
) -> list[str]:
    """Return a list of error strings for one repo (empty list = OK)."""
    errors: list[str] = []
    slug = row["repo_slug"]
    repo_class = (row.get("class") or "").strip().lower()

    if repo_class == "reference":
        return []

    if snapshot_row is None:
        errors.append(f"{slug}: no row in REPO_HEALTH_SNAPSHOT.csv (run snapshot_external_repos.py)")
        return errors

    if (snapshot_row.get("has_external_repo_contract") or "").lower() != "true":
        errors.append(f"{slug}: missing EXTERNAL_REPO_CONTRACT.md (snapshot reports false)")

    has_mirror = (snapshot_row.get("has_akos_mirror_rule") or "").lower() == "true"
    has_rules_dir = repo_path is not None and (repo_path / ".cursor" / "rules").is_dir()
    if has_rules_dir and not has_mirror:
        errors.append(f"{slug}: .cursor/rules/akos-mirror.mdc missing")

    if repo_path is not None and repo_path.is_dir():
        contract_path = repo_path / "EXTERNAL_REPO_CONTRACT.md"
        age = _last_review_age_days(contract_path)
        if age is None:
            if contract_path.is_file():
                errors.append(f"{slug}: EXTERNAL_REPO_CONTRACT.md missing or invalid last_review:")
        elif age > freshness_days:
            errors.append(
                f"{slug}: EXTERNAL_REPO_CONTRACT.md last_review is {age} days old "
                f"(freshness_days={freshness_days})"
            )

        mirror_path = repo_path / ".cursor" / "rules" / "akos-mirror.mdc"
        if mirror_path.is_file() and MIRROR_TEMPLATE.is_file():
            consumer_hash = _sha256_text(mirror_path.read_text(encoding="utf-8"))
            template_hash = _sha256_text(MIRROR_TEMPLATE.read_text(encoding="utf-8"))
            if consumer_hash != template_hash:
                errors.append(
                    f"{slug}: .cursor/rules/akos-mirror.mdc sha256 drifted from AKOS template "
                    f"(consumer={consumer_hash[:12]}, template={template_hash[:12]})"
                )

    return errors


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check governance posture of external Holistika repos")
    parser.add_argument("--freshness-days", type=int, default=DEFAULT_FRESHNESS_DAYS,
                        help="Maximum age in days for EXTERNAL_REPO_CONTRACT.md last_review (default 90)")
    parser.add_argument("--json-log", action="store_true")
    args = parser.parse_args(list(argv) if argv is not None else None)
    setup_logging(json_output=args.json_log)

    if not REGISTRY_CSV.is_file():
        logger.error("REPOSITORY_REGISTRY.csv not found at %s", REGISTRY_CSV)
        return 1

    registry_rows = _load_registry()
    snapshot = _load_latest_snapshot()
    repo_paths = _resolve_repo_paths()

    akos_repo_url = "https://github.com/FraysaXII/openclaw-akos"

    all_errors: list[str] = []
    checked = 0
    skipped = 0
    for row in registry_rows:
        slug = (row.get("repo_slug") or "").strip()
        if not slug:
            continue
        repo_class = (row.get("class") or "").strip().lower()
        github_url = (row.get("github_url") or "").strip()
        if repo_class == "reference":
            continue
        # Skip AKOS-internal slugs (the canonical AKOS repo + its monorepo aliases).
        if github_url == akos_repo_url:
            skipped += 1
            continue
        # Skip slugs without any local path mapping or snapshot row (placeholders).
        if slug not in repo_paths and slug not in snapshot:
            logger.info("skipping %s (no local path or snapshot row; treat as placeholder)", slug)
            skipped += 1
            continue
        repo_path = repo_paths.get(slug)
        errors = _check_one(row, snapshot.get(slug), repo_path, args.freshness_days)
        if errors:
            for e in errors:
                logger.error(e)
            all_errors.extend(errors)
        checked += 1

    if all_errors:
        logger.error(
            "external repo contract: %d issue(s) across %d repo(s) (%d skipped)",
            len(all_errors), checked, skipped,
        )
        return 1

    logger.info(
        "external repo contract: OK -- %d repo(s) validated, %d skipped (AKOS-internal / placeholder)",
        checked, skipped,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
