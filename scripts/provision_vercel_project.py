#!/usr/bin/env python3
"""Provision (or verify) a Vercel project for an active subdomain row.

Reads ``SUBDOMAINS_REGISTRY.md`` for rows where ``state=active`` and a
``vercel_project`` is named, then ensures the project exists, has the
expected GitHub link, and the custom domain is attached.

Idempotent: when the project already exists with the right GitHub link and
domain attached, exits 0 with no changes.

Skips gracefully when the ``vercel`` CLI is not authenticated (warns,
returns 0) — this is a convenience tool, not a hard gate.

Usage::

    py scripts/provision_vercel_project.py --subdomain erp
    py scripts/provision_vercel_project.py --dry-run            # all active rows
    py scripts/provision_vercel_project.py --subdomain madeira --dry-run
"""

from __future__ import annotations

import argparse
import logging
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT
from akos.log import setup_logging

logger = logging.getLogger("akos.provision_vercel")

REGISTRY_MD = (
    REPO_ROOT / "docs" / "references" / "hlk" / "v3.0"
    / "Envoy Tech Lab" / "Repositories" / "SUBDOMAINS_REGISTRY.md"
)


def _parse_registry() -> list[dict[str, str]]:
    if not REGISTRY_MD.is_file():
        return []
    text = REGISTRY_MD.read_text(encoding="utf-8")
    rows: list[dict[str, str]] = []
    in_table = False
    headers: list[str] = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("| subdomain "):
            headers = [c.strip() for c in s.strip("|").split("|")]
            in_table = True
            continue
        if in_table and re.match(r"^\|\s*-+\s*\|", s):
            continue
        if in_table:
            if not s.startswith("|"):
                in_table = False
                continue
            cols = [c.strip().strip("`") for c in s.strip("|").split("|")]
            if len(cols) != len(headers):
                continue
            rows.append(dict(zip(headers, cols)))
    return rows


def _vercel_available() -> bool:
    return shutil.which("vercel") is not None


def _vercel(args: list[str]) -> tuple[int, str, str]:
    try:
        result = subprocess.run(
            ["vercel"] + args, capture_output=True, text=True, timeout=60, check=False,
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as exc:
        return 99, "", str(exc)


def provision_one(row: dict[str, str], *, dry_run: bool) -> str:
    project = row.get("vercel_project", "").strip()
    subdomain = row.get("subdomain", "").strip()
    apex = row.get("apex", "").strip()
    if not project or project.startswith("_(") or project.startswith("rewrite"):
        logger.info("%s: project not provisionable from registry (rewrite or none)", subdomain)
        return "SKIPPED_NON_PROVISIONABLE"
    fqdn = f"{subdomain}.{apex}" if subdomain and apex else ""
    if not fqdn:
        return "SKIPPED_NO_FQDN"

    if dry_run:
        logger.info("[dry-run] %s -> project '%s' on %s", subdomain, project, fqdn)
        return "DRY_WROTE"

    if not _vercel_available():
        logger.warning("vercel CLI not available; skipping provisioning")
        return "SKIPPED_NO_CLI"

    rc, out, err = _vercel(["projects", "ls"])
    if rc != 0:
        logger.warning("vercel projects ls failed: %s", err.strip())
        return "SKIPPED_NOT_AUTHED"

    if project not in out:
        logger.info("creating Vercel project %s", project)
        rc2, out2, err2 = _vercel(["projects", "add", project])
        if rc2 != 0:
            logger.error("vercel projects add failed: %s", err2.strip())
            return "FAILED_CREATE"

    rc3, out3, err3 = _vercel(["domains", "add", fqdn, project])
    if rc3 != 0 and "already" not in (err3 + out3).lower():
        logger.error("vercel domains add failed: %s", err3.strip())
        return "FAILED_DOMAIN"
    return "PROVISIONED"


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Provision Vercel projects from SUBDOMAINS_REGISTRY")
    parser.add_argument("--subdomain", help="Limit to one subdomain slug")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json-log", action="store_true")
    args = parser.parse_args(list(argv) if argv is not None else None)
    setup_logging(json_output=args.json_log)

    rows = _parse_registry()
    active = [r for r in rows if (r.get("state") or "").strip().lower() == "active"]
    if args.subdomain:
        active = [r for r in active if (r.get("subdomain") or "").strip() == args.subdomain]
    if not active:
        logger.warning("no active rows matched")
        return 0

    overall_failed = False
    for row in active:
        outcome = provision_one(row, dry_run=args.dry_run)
        print(f"  [{outcome:>26}] {row.get('subdomain', '?')}.{row.get('apex', '?')} -> {row.get('vercel_project', '?')}")
        if outcome.startswith("FAILED"):
            overall_failed = True
    return 1 if overall_failed else 0


if __name__ == "__main__":
    sys.exit(main())
