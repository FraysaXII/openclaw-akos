#!/usr/bin/env python3
"""Validate the canonical Holistika SUBDOMAINS_REGISTRY.md.

Parses the markdown table under "Registry table" and enforces:

1. Every row has the required columns populated (no empty cells where required).
2. ``state`` value is in {active, reserved, archived}.
3. ``data_mode`` value is in {live, demo, none}.
4. ``auth`` value is in {required, none}.
5. ``brand_register`` value is in {internal, external}.
6. No duplicate (subdomain, apex) tuples.
7. ``state == 'active'`` rows have a non-empty ``vercel_project`` and a
   non-empty ``linked_initiative``.

Usage:
    py scripts/validate_subdomains_registry.py
    py scripts/validate_subdomains_registry.py --json-log

Exit codes:
    0 -- registry is valid.
    1 -- registry has errors (printed to stderr).
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT
from akos.log import setup_logging

logger = logging.getLogger("akos.subdomains")

REGISTRY_PATH = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "Envoy Tech Lab"
    / "Repositories"
    / "SUBDOMAINS_REGISTRY.md"
)

REQUIRED_COLUMNS = (
    "subdomain",
    "apex",
    "state",
    "data_mode",
    "auth",
    "brand_register",
    "vercel_project",
    "repo",
    "linked_initiative",
    "notes",
)

ALLOWED = {
    "state": {"active", "reserved", "archived"},
    "data_mode": {"live", "demo", "none"},
    "auth": {"required", "none"},
    "brand_register": {"internal", "external"},
}

TABLE_HEADER_RE = re.compile(r"^\|\s*subdomain\s*\|", re.IGNORECASE)


def _strip_md_code(cell: str) -> str:
    """Strip wrapping backticks and basic markdown link syntax for value comparison."""
    s = cell.strip()
    if s.startswith("`") and s.endswith("`"):
        s = s[1:-1]
    return s.strip()


def _parse_registry(path: Path) -> tuple[list[str], list[list[str]]]:
    """Parse the registry markdown file and return (header, rows)."""
    if not path.exists():
        raise FileNotFoundError(f"SUBDOMAINS_REGISTRY.md not found at {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    header: list[str] = []
    rows: list[list[str]] = []
    in_table = False
    for line in lines:
        stripped = line.strip()
        if not in_table:
            if TABLE_HEADER_RE.match(stripped):
                header = [c.strip().lower() for c in stripped.strip("|").split("|")]
                in_table = True
                continue
        else:
            if not stripped.startswith("|"):
                break
            if re.match(r"^\|[\s\-:|]+$", stripped):
                continue
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if len(cells) >= len(REQUIRED_COLUMNS) - 1 and cells[0]:
                rows.append(cells)
    return header, rows


def _validate_row(idx: int, header: list[str], cells: list[str]) -> list[str]:
    """Return a list of human-readable error strings for one row (empty list = OK)."""
    errors: list[str] = []
    if len(cells) < len(REQUIRED_COLUMNS):
        return [f"Row {idx}: expected {len(REQUIRED_COLUMNS)} columns, got {len(cells)}"]

    by_col = dict(zip(header, cells))

    for col in REQUIRED_COLUMNS:
        if col not in by_col:
            errors.append(f"Row {idx}: missing column '{col}' (header mismatch)")

    if errors:
        return errors

    state = _strip_md_code(by_col["state"]).lower()
    if state not in ALLOWED["state"]:
        errors.append(
            f"Row {idx} ({by_col['subdomain']}): state '{state}' not in {sorted(ALLOWED['state'])}"
        )

    data_mode = _strip_md_code(by_col["data_mode"]).lower()
    if data_mode not in ALLOWED["data_mode"]:
        errors.append(
            f"Row {idx} ({by_col['subdomain']}): data_mode '{data_mode}' not in {sorted(ALLOWED['data_mode'])}"
        )

    auth = _strip_md_code(by_col["auth"]).lower()
    if auth not in ALLOWED["auth"]:
        errors.append(
            f"Row {idx} ({by_col['subdomain']}): auth '{auth}' not in {sorted(ALLOWED['auth'])}"
        )

    brand_register = _strip_md_code(by_col["brand_register"]).lower()
    if brand_register not in ALLOWED["brand_register"]:
        errors.append(
            f"Row {idx} ({by_col['subdomain']}): brand_register '{brand_register}' not in {sorted(ALLOWED['brand_register'])}"
        )

    if state == "active":
        if not _strip_md_code(by_col["vercel_project"]) or _strip_md_code(by_col["vercel_project"]) in {"_(none yet)_", "_(future)_"}:
            errors.append(
                f"Row {idx} ({by_col['subdomain']}): active rows require a non-empty vercel_project"
            )
        if not _strip_md_code(by_col["linked_initiative"]):
            errors.append(
                f"Row {idx} ({by_col['subdomain']}): active rows require a linked_initiative"
            )

    return errors


def _validate_uniqueness(header: list[str], rows: list[list[str]]) -> list[str]:
    """Return a list of error strings for duplicate (subdomain, apex) pairs."""
    seen: dict[tuple[str, str], int] = {}
    errors: list[str] = []
    for idx, cells in enumerate(rows, start=1):
        if len(cells) < 2:
            continue
        by_col = dict(zip(header, cells))
        key = (
            _strip_md_code(by_col.get("subdomain", "")).lower(),
            _strip_md_code(by_col.get("apex", "")).lower(),
        )
        if not key[0]:
            continue
        if key in seen:
            errors.append(
                f"Row {idx}: duplicate (subdomain={key[0]}, apex={key[1]}) -- previous row {seen[key]}"
            )
        else:
            seen[key] = idx
    return errors


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Holistika SUBDOMAINS_REGISTRY.md")
    parser.add_argument("--json-log", action="store_true", help="JSON logging output")
    args = parser.parse_args(list(argv) if argv is not None else None)
    setup_logging(json_output=args.json_log)

    try:
        header, rows = _parse_registry(REGISTRY_PATH)
    except FileNotFoundError as exc:
        logger.error("%s", exc)
        return 1

    if not header:
        logger.error("Could not find a 'subdomain' table header in %s", REGISTRY_PATH)
        return 1
    if not rows:
        logger.error("No data rows found in %s", REGISTRY_PATH)
        return 1

    all_errors: list[str] = []
    for idx, cells in enumerate(rows, start=1):
        all_errors.extend(_validate_row(idx, header, cells))
    all_errors.extend(_validate_uniqueness(header, rows))

    if all_errors:
        for err in all_errors:
            logger.error(err)
        logger.error("SUBDOMAINS_REGISTRY.md: %d error(s)", len(all_errors))
        return 1

    logger.info("SUBDOMAINS_REGISTRY.md OK -- %d row(s) validated", len(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
