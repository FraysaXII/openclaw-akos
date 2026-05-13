#!/usr/bin/env python3
"""Notify consumer repos when an AKOS canonical CSV changes.

Triggered (typically) from a GitHub Actions workflow on AKOS that watches
``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/*.csv``. For every row in
``REPOSITORY_REGISTRY.csv`` whose ``consumes_mirrors`` includes a changed
mirror, this script:

1. Posts a structured Slack notification (when ``SLACK_OPS_WEBHOOK`` is set).
2. Optionally opens a tracking issue in the consumer repo via ``gh`` CLI
   (``--open-issue``).

Designed to be safe to re-run: issue creation is idempotent (checks for an
existing open issue with the canonical title before creating).

Usage::

    py scripts/notify_consumers_of_canonical_change.py --changed PERSONA_REGISTRY,SKILL_REGISTRY
    py scripts/notify_consumers_of_canonical_change.py --changed PERSONA_REGISTRY --open-issue
    py scripts/notify_consumers_of_canonical_change.py --changed PERSONA_REGISTRY --dry-run
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.log import setup_logging
from scripts.bless_external_repo import REFERENCE_CLASS, load_registry

logger = logging.getLogger("akos.notify_consumers")


def _post_slack(text: str, *, dry_run: bool) -> bool:
    if dry_run:
        logger.info("[dry-run] would post Slack:\n%s", text)
        return True
    url = os.environ.get("SLACK_OPS_WEBHOOK")
    if not url:
        logger.warning("SLACK_OPS_WEBHOOK not set; skipping Slack post")
        return False
    payload = json.dumps({"text": text}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return 200 <= resp.status < 300
    except Exception as exc:
        logger.warning("slack post failed: %s", exc)
        return False


def _open_consumer_issue(repo_url: str, slug: str, mirrors: list[str], *, dry_run: bool) -> str:
    title = f"chore(akos): regenerate types for canonical mirror change ({', '.join(mirrors)})"
    if dry_run:
        logger.info("[dry-run] would open issue in %s: %s", repo_url, title)
        return "DRY_WROTE"
    if shutil.which("gh") is None:
        return "SKIPPED_NO_GH"
    repo_arg = repo_url.replace("https://github.com/", "")
    try:
        existing = subprocess.run(
            ["gh", "issue", "list", "--repo", repo_arg, "--search", title, "--state", "open", "--json", "number"],
            capture_output=True, text=True, timeout=30, check=False,
        )
        if existing.returncode == 0 and existing.stdout.strip() not in ("[]", ""):
            return "EXISTS"
    except Exception:
        return "FAILED"
    body = (
        "AKOS canonical mirror(s) changed:\n\n"
        + "\n".join(f"- `{m}`" for m in mirrors)
        + "\n\n"
        "Run `py scripts/regen_consumer_types.py --repo-slug "
        + slug
        + "` against AKOS, or wait for the nightly auto-PR.\n\n"
        "Source: https://github.com/FraysaXII/openclaw-akos/tree/main/docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/\n"
    )
    try:
        result = subprocess.run(
            ["gh", "issue", "create", "--repo", repo_arg, "--title", title, "--body", body, "--label", "akos-linked,governance"],
            capture_output=True, text=True, timeout=60, check=False,
        )
        return "OPENED" if result.returncode == 0 else "FAILED"
    except Exception:
        return "FAILED"


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Notify consumers of AKOS canonical CSV changes")
    parser.add_argument("--changed", required=True,
                        help="Comma-separated list of changed mirror names (no .csv suffix)")
    parser.add_argument("--open-issue", action="store_true",
                        help="Also open a tracking issue in each affected consumer repo via gh")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json-log", action="store_true")
    args = parser.parse_args(list(argv) if argv is not None else None)
    setup_logging(json_output=args.json_log)

    changed = [c.strip() for c in args.changed.split(",") if c.strip()]
    if not changed:
        logger.error("--changed must list at least one mirror name")
        return 2

    registry = load_registry()
    affected: list[tuple[str, list[str]]] = []
    for slug, meta in sorted(registry.items()):
        if meta.repo_class.lower() == REFERENCE_CLASS:
            continue
        if "openclaw-akos" in meta.github_url:
            continue
        if not meta.consumes_compliance_types:
            continue
        intersect = sorted(set(meta.consumes_mirrors) & set(changed))
        if intersect:
            affected.append((slug, intersect))

    if not affected:
        logger.info("no consumers declared %s as a consumed mirror; nothing to notify", changed)
        return 0

    summary_lines = [f"*AKOS canonical mirror change* — {', '.join(f'`{c}`' for c in changed)}"]
    for slug, intersect in affected:
        summary_lines.append(f"• `{slug}` consumes: {', '.join(intersect)}")
    summary = "\n".join(summary_lines)
    _post_slack(summary, dry_run=args.dry_run)

    if args.open_issue:
        for slug, intersect in affected:
            meta = registry[slug]
            outcome = _open_consumer_issue(meta.github_url, slug, intersect, dry_run=args.dry_run)
            print(f"  [{outcome:>14}] {slug} ({', '.join(intersect)})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
