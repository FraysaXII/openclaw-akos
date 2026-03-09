#!/usr/bin/env python3
"""Resolve placeholder paths in ~/.mcporter/mcporter.json.

Replaces Linux placeholder paths (/opt/openclaw/workspace) with OS-correct
values derived from resolve_openclaw_home() and REPO_ROOT.  Idempotent:
re-running when paths are already resolved is a no-op.

Usage:
    py scripts/resolve-mcporter-paths.py
    py scripts/resolve-mcporter-paths.py --config PATH
    py scripts/resolve-mcporter-paths.py --dry-run
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import resolve_mcporter_paths, resolve_openclaw_home
from akos.log import setup_logging

logger = logging.getLogger("akos.resolve-mcporter")

DEFAULT_CONFIG = Path.home() / ".mcporter" / "mcporter.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve mcporter.json placeholder paths")
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help=f"Path to mcporter.json (default: {DEFAULT_CONFIG})",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    parser.add_argument("--json-log", action="store_true", help="JSON logging output")
    args = parser.parse_args()

    setup_logging(json_output=args.json_log)

    config_path: Path = args.config
    if not config_path.exists():
        logger.error("Config file not found: %s", config_path)
        logger.info(
            "Copy the example first: cp config/mcporter.json.example %s",
            config_path,
        )
        sys.exit(1)

    oc_home = resolve_openclaw_home()
    exports_dir = oc_home / "workspace" / "exports"
    if not exports_dir.exists():
        exports_dir.mkdir(parents=True, exist_ok=True)
        logger.info("Created exports directory: %s", exports_dir)

    raw = config_path.read_text(encoding="utf-8")
    resolved = resolve_mcporter_paths(raw)

    if raw == resolved:
        logger.info("No changes needed -- paths already resolved in %s", config_path)
        return

    if args.dry_run:
        logger.info("Dry run -- would update %s", config_path)
        for i, (old_line, new_line) in enumerate(
            zip(raw.splitlines(), resolved.splitlines()), 1
        ):
            if old_line != new_line:
                logger.info("  line %d: %s -> %s", i, old_line.strip(), new_line.strip())
        return

    config_path.write_text(resolved, encoding="utf-8")
    logger.info("Resolved placeholder paths in %s", config_path)


if __name__ == "__main__":
    main()
