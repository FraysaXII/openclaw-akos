#!/usr/bin/env python3
"""Configure GitHub branch protection on ``main`` for blessed external repos.

Idempotent: when the desired protection already matches, exits 0 with no
changes. Uses ``gh`` CLI (which the operator already has installed for the
nightly drift workflow). Skips gracefully when ``gh`` is unavailable.

What it sets on ``main``:

- Required reviews >= 1, dismiss-stale on update.
- Required status checks: ``lint``, ``typecheck``, ``audit``, ``unit``, ``build``
  (a subset is satisfied when CI uses compound names like ``lint-typecheck``).
- Required conversation resolution.
- Block force-push and branch deletion.

The required status check names are derived from the AKOS canonical CI
template; if a consumer adds extra jobs, those become *additional* gates, not
substitutes.

Usage::

    py scripts/configure_branch_protection.py --repo-slug hlk-erp
    py scripts/configure_branch_protection.py --repo-slug hlk-erp --dry-run
    py scripts/configure_branch_protection.py            # all blessed non-reference repos
"""

from __future__ import annotations

import argparse
import json
import logging
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.log import setup_logging
from scripts.bless_external_repo import load_registry, REFERENCE_CLASS

logger = logging.getLogger("akos.branch_protection")

REQUIRED_CONTEXTS_DEFAULT = ["lint", "typecheck", "audit", "unit", "build"]


def _gh_available() -> bool:
    return shutil.which("gh") is not None


def _repo_arg_from_url(url: str) -> str | None:
    if "github.com/" not in url:
        return None
    return url.split("github.com/", 1)[1].rstrip("/")


def _get_current_protection(repo_arg: str) -> dict | None:
    try:
        result = subprocess.run(
            ["gh", "api", f"repos/{repo_arg}/branches/main/protection"],
            capture_output=True, text=True, timeout=30, check=False,
        )
        if result.returncode != 0:
            return None
        return json.loads(result.stdout)
    except Exception as exc:
        logger.warning("gh api fetch failed for %s: %s", repo_arg, exc)
        return None


def _desired_payload(required_contexts: list[str]) -> dict:
    return {
        "required_status_checks": {
            "strict": True,
            "contexts": required_contexts,
        },
        "enforce_admins": False,
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": True,
            "require_code_owner_reviews": False,
            "required_approving_review_count": 1,
            "require_last_push_approval": False,
        },
        "restrictions": None,
        "required_linear_history": False,
        "allow_force_pushes": False,
        "allow_deletions": False,
        "required_conversation_resolution": True,
        "lock_branch": False,
        "allow_fork_syncing": True,
    }


def _matches(current: dict | None, desired: dict) -> bool:
    if not current:
        return False
    cur_pr = (current.get("required_pull_request_reviews") or {})
    if cur_pr.get("required_approving_review_count", 0) < desired["required_pull_request_reviews"]["required_approving_review_count"]:
        return False
    if not cur_pr.get("dismiss_stale_reviews", False):
        return False
    cur_sc = (current.get("required_status_checks") or {})
    if not cur_sc.get("strict", False):
        return False
    cur_contexts = set(cur_sc.get("contexts") or [])
    if not set(desired["required_status_checks"]["contexts"]).issubset(cur_contexts):
        return False
    if (current.get("allow_force_pushes") or {}).get("enabled"):
        return False
    if (current.get("allow_deletions") or {}).get("enabled"):
        return False
    if not (current.get("required_conversation_resolution") or {}).get("enabled"):
        return False
    return True


def configure_one(repo_arg: str, *, dry_run: bool, required_contexts: list[str]) -> str:
    desired = _desired_payload(required_contexts)
    current = _get_current_protection(repo_arg)
    if _matches(current, desired):
        logger.info("%s: branch protection already aligned", repo_arg)
        return "ALIGNED"
    if dry_run:
        logger.info("[dry-run] %s: would PUT branch protection", repo_arg)
        return "DRY_WROTE"
    payload_path = Path("/tmp/akos_branch_protection.json")
    try:
        payload_path.write_text(json.dumps(desired), encoding="utf-8")
    except OSError:
        # Windows fallback
        payload_path = Path.home() / "akos_branch_protection.json"
        payload_path.write_text(json.dumps(desired), encoding="utf-8")
    try:
        result = subprocess.run(
            [
                "gh", "api", "--method", "PUT",
                f"repos/{repo_arg}/branches/main/protection",
                "--input", str(payload_path),
                "-H", "Accept: application/vnd.github+json",
            ],
            capture_output=True, text=True, timeout=60, check=False,
        )
        if result.returncode == 0:
            logger.info("%s: branch protection updated", repo_arg)
            return "UPDATED"
        logger.error("%s: PUT failed: %s", repo_arg, result.stderr.strip())
        return "FAILED"
    except Exception as exc:
        logger.error("%s: PUT exception %s", repo_arg, exc)
        return "FAILED"
    finally:
        try:
            payload_path.unlink(missing_ok=True)
        except Exception:
            pass


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Configure branch protection on main")
    parser.add_argument("--repo-slug")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--contexts", action="append", default=[],
                        help="Override required status check contexts (repeatable)")
    parser.add_argument("--json-log", action="store_true")
    args = parser.parse_args(list(argv) if argv is not None else None)
    setup_logging(json_output=args.json_log)

    if not _gh_available():
        logger.warning("gh CLI not available; skipping branch-protection configuration")
        return 0

    contexts = args.contexts or list(REQUIRED_CONTEXTS_DEFAULT)
    registry = load_registry()
    if args.repo_slug:
        slugs = [args.repo_slug]
    else:
        slugs = [
            s for s, m in registry.items()
            if m.repo_class.lower() != REFERENCE_CLASS
            and "openclaw-akos" not in m.github_url
        ]

    overall_failed = False
    for slug in slugs:
        meta = registry.get(slug)
        if meta is None:
            logger.warning("unknown slug %s", slug)
            continue
        repo_arg = _repo_arg_from_url(meta.github_url)
        if repo_arg is None:
            logger.warning("%s: cannot derive owner/repo from %s", slug, meta.github_url)
            continue
        outcome = configure_one(repo_arg, dry_run=args.dry_run, required_contexts=contexts)
        print(f"  [{outcome:>10}] {slug} ({repo_arg})")
        if outcome == "FAILED":
            overall_failed = True

    return 1 if overall_failed else 0


if __name__ == "__main__":
    sys.exit(main())
