#!/usr/bin/env python3
"""Detect registry rows in REPOSITORY_REGISTRY.csv that haven't been blessed yet.

A row is considered un-blessed when:

- ``class != reference``
- ``github_url`` is not the AKOS repo itself
- A local path is resolvable (via the ``local_path`` column or ``--repo-path-map``),
  AND the consumer is missing ``EXTERNAL_REPO_CONTRACT.md`` or
  ``.cursor/rules/akos-mirror.mdc``.

When local paths are NOT resolvable, the row is reported as ``UNREACHABLE`` so
operators can decide whether to add a `local_path` value or accept it as a placeholder.

This is a NUDGE check: it surfaces work to be done but does not fail
release-gate by default. ``--strict`` flips it to a hard fail.

Usage::

    py scripts/detect_unblessed_registry_rows.py
    py scripts/detect_unblessed_registry_rows.py --strict
    py scripts/detect_unblessed_registry_rows.py --json-log
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT
from akos.log import setup_logging
from scripts.bless_external_repo import REFERENCE_CLASS, RepoMeta, load_registry

logger = logging.getLogger("akos.detect_unblessed")


def _resolve_repo_path(meta: RepoMeta, override_map: dict[str, Path]) -> Path | None:
    if meta.slug in override_map:
        return override_map[meta.slug]
    if meta.relative_path:
        cand = (REPO_ROOT.parent / meta.relative_path).resolve()
        if cand.is_dir():
            return cand
    return None


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Detect un-blessed external repos")
    parser.add_argument("--strict", action="store_true", help="Exit 1 when un-blessed rows found")
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
    needs_bless: list[str] = []
    unreachable: list[str] = []
    blessed: list[str] = []

    for slug, meta in sorted(registry.items()):
        if meta.repo_class.lower() == REFERENCE_CLASS:
            continue
        if "openclaw-akos" in meta.github_url:
            continue
        repo_path = _resolve_repo_path(meta, overrides)
        if repo_path is None:
            unreachable.append(slug)
            continue
        contract = repo_path / "EXTERNAL_REPO_CONTRACT.md"
        mirror = repo_path / ".cursor" / "rules" / "akos-mirror.mdc"
        if not contract.is_file() or not mirror.is_file():
            needs_bless.append(slug)
        else:
            blessed.append(slug)

    print()
    print("=" * 56)
    print("  REPOSITORY_REGISTRY bless status")
    print("=" * 56)
    for slug in blessed:
        print(f"  [    BLESSED] {slug}")
    for slug in needs_bless:
        print(f"  [NEEDS_BLESS] {slug}  -> py scripts/bless_external_repo.py --repo-slug {slug}")
    for slug in unreachable:
        print(f"  [UNREACHABLE] {slug}  -> add `local_path` column value or pass --repo-path-map")
    print()

    if args.strict and needs_bless:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
