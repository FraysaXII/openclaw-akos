#!/usr/bin/env python3
"""Surface upcoming/overdue secret rotations across all blessed external repos.

Reads ``docs/runbooks/secrets-rotation.md`` from every consumer repo with a
resolvable local path (via the ``path`` column in ``REPOSITORY_REGISTRY.csv``
or via ``--repo-path-map``) and emits:

- A markdown summary to stdout (always).
- A Slack ops notification if ``SLACK_OPS_WEBHOOK`` is set in the environment.
- Exit code ``1`` if any secret is overdue (default >90 days) and ``--strict``
  is passed; otherwise always exits ``0`` (this is a notifier, not a gate).

Designed to run daily via cron / GitHub Actions schedule from AKOS.

Reuses ``check_external_repo_ci_posture.check_secret_rotation`` to keep the
parsing rules in one place (SSOT, no duplicated logic).

Usage::

    py scripts/secret_rotation_reminders.py
    py scripts/secret_rotation_reminders.py --strict --json-log
    py scripts/secret_rotation_reminders.py --warn-days 60 --fail-days 90
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import urllib.request
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT
from akos.log import setup_logging
from scripts.bless_external_repo import load_registry, REFERENCE_CLASS
from scripts.check_external_repo_ci_posture import check_secret_rotation

logger = logging.getLogger("akos.secret_rotation_reminders")


def _resolve_repo_path(slug: str, relative_path: str, override_map: dict[str, Path]) -> Path | None:
    if slug in override_map:
        return override_map[slug]
    if relative_path:
        candidate = (REPO_ROOT.parent / relative_path).resolve()
        if candidate.is_dir():
            return candidate
    return None


def _post_slack(text: str) -> bool:
    url = os.environ.get("SLACK_OPS_WEBHOOK")
    if not url:
        return False
    payload = json.dumps({"text": text}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return 200 <= resp.status < 300
    except Exception as exc:
        logger.warning("slack post failed: %s", exc)
        return False


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Daily secret-rotation reminder across blessed repos")
    parser.add_argument("--warn-days", type=int, default=75)
    parser.add_argument("--fail-days", type=int, default=90)
    parser.add_argument("--strict", action="store_true", help="Exit 1 when any secret is overdue")
    parser.add_argument(
        "--repo-path-map",
        action="append",
        default=[],
        help="Per-repo path override, e.g. hlk-erp=C:/abs/path. Repeatable.",
    )
    parser.add_argument("--json-log", action="store_true")
    args = parser.parse_args(list(argv) if argv is not None else None)
    setup_logging(json_output=args.json_log)

    overrides: dict[str, Path] = {}
    for entry in args.repo_path_map:
        if "=" not in entry:
            continue
        slug, path_str = entry.split("=", 1)
        overrides[slug.strip()] = Path(path_str.strip()).resolve()

    registry = load_registry()
    overdue_lines: list[str] = []
    warn_lines: list[str] = []
    pass_lines: list[str] = []
    skipped_lines: list[str] = []

    for slug, meta in sorted(registry.items()):
        if meta.repo_class.lower() == REFERENCE_CLASS:
            continue
        if "openclaw-akos" in meta.github_url:
            continue
        repo_path = _resolve_repo_path(slug, meta.relative_path, overrides)
        if repo_path is None:
            skipped_lines.append(f"- `{slug}` — no resolvable local path")
            continue
        result = check_secret_rotation(repo_path, warn_days=args.warn_days, fail_days=args.fail_days)
        line = f"- `{slug}` — {result.level}: {result.message}"
        if result.level == "FAIL":
            overdue_lines.append(line)
        elif result.level == "WARN":
            warn_lines.append(line)
        elif result.level == "PASS":
            pass_lines.append(line)
        else:
            skipped_lines.append(line)

    summary_parts = ["# Secret rotation reminders\n"]
    if overdue_lines:
        summary_parts.append(f"\n## Overdue (>{args.fail_days}d) — action required\n")
        summary_parts.extend(overdue_lines)
    if warn_lines:
        summary_parts.append(f"\n## Approaching ({args.warn_days}-{args.fail_days}d)\n")
        summary_parts.extend(warn_lines)
    if pass_lines:
        summary_parts.append("\n## Healthy\n")
        summary_parts.extend(pass_lines)
    if skipped_lines:
        summary_parts.append("\n## Skipped\n")
        summary_parts.extend(skipped_lines)
    summary = "\n".join(summary_parts) + "\n"
    print(summary)

    if overdue_lines or warn_lines:
        slack_text = (
            f"*Secret rotation reminders* — "
            f"{len(overdue_lines)} overdue, {len(warn_lines)} approaching\n"
            + "\n".join(overdue_lines + warn_lines)
        )
        _post_slack(slack_text)

    if args.strict and overdue_lines:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
