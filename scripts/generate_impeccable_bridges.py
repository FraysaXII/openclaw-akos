#!/usr/bin/env python3
"""Generate Impeccable bridge coverage report from brand canonicals (I77 P2).

Sibling to ``scripts/validate_impeccable_bridge_drift.py`` (drift gate; FAIL
or WARN-based). This generator focuses on **operator-facing reporting** —
emit a per-bridge coverage breakdown so the operator (or future Brand
Manager) can decide which canonicals to cross-reference next.

Per C-77-1 default (fenced-regenerable-sections; resolved at P2 inline-ratify
gate D-IH-77-G), this tool ships ``--check`` mode in P2. The ``--write``
mode is **forward-charter** — operator approval required before any bridge
file is auto-written (the bridges carry operator-authored narrative outside
of pure cross-references; auto-write must preserve that prose via fence
markers ``<!-- impeccable-bridge-generator:start -->`` /
``<!-- impeccable-bridge-generator:end -->``).

Modes::

    --check (default)  Non-mutating; prints coverage report to stdout.
                       Same as ``validate_impeccable_bridge_drift.py`` but
                       emits a markdown table instead of one-warning-per-miss.
    --write            Reserved for forward-charter; currently raises NotImplemented.
                       Will regenerate fenced sections after D-IH-77-G ratification.

Usage::

    py scripts/generate_impeccable_bridges.py
    py scripts/generate_impeccable_bridges.py --check
    py scripts/generate_impeccable_bridges.py --workspace-root /path/to/repo
    py scripts/generate_impeccable_bridges.py --output /tmp/coverage.md

Exit codes::

    0 — coverage check ran successfully (drift not enforced at this layer;
        the validator script enforces drift).
    1 — registry file missing OR bridge file missing OR --write invoked
        before D-IH-77-G ratification.

Cross-references:
  ``akos/impeccable_bridge.py`` -- Pydantic chassis.
  ``scripts/validate_impeccable_bridge_drift.py`` -- sibling drift gate.
  ``docs/wip/planning/77-impeccable-brand-bridge-refresh/master-roadmap.md`` §"Strand B".
  D-IH-77-C -- generator + drift gate scope.
  C-77-1 -- generator overwrite mode (default: fenced-regenerable; resolved at
    P2 D-IH-77-G).
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.impeccable_bridge import (  # noqa: E402
    CANONICAL_REGISTRY_PATH,
    compute_coverage,
    parse_all_bridge_files,
    parse_canonical_inventory,
    render_coverage_section_markdown,
)
from akos.io import REPO_ROOT  # noqa: E402
from akos.log import setup_logging  # noqa: E402

logger = logging.getLogger("akos.impeccable_bridge_generator")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Generate Impeccable bridge coverage report (I77 P2; --check mode "
            "ships at P2; --write mode reserved for D-IH-77-G ratification)."
        )
    )
    parser.add_argument(
        "--workspace-root",
        type=Path,
        default=REPO_ROOT,
        help="Workspace root to scan (default: AKOS repo root).",
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--check",
        action="store_true",
        default=True,
        help="Non-mutating coverage report (default).",
    )
    mode_group.add_argument(
        "--write",
        action="store_true",
        help=(
            "Reserved for forward-charter; currently raises NotImplementedError. "
            "Will regenerate fenced sections inside bridges after D-IH-77-G "
            "operator ratification per C-77-1 default."
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Write the markdown report to this file instead of stdout.",
    )
    args = parser.parse_args(argv)
    setup_logging()

    if args.write:
        logger.error(
            "--write mode reserved for forward-charter; awaiting D-IH-77-G "
            "(generator overwrite mode ratification per C-77-1) at I77 P2 "
            "inline-ratify gate. Use --check for the read-only report."
        )
        return 1

    registry_path = args.workspace_root / CANONICAL_REGISTRY_PATH
    if not registry_path.exists():
        logger.error(
            "CANONICAL_REGISTRY.csv not found at %s; cannot generate coverage report",
            registry_path,
        )
        return 1

    canonicals = parse_canonical_inventory(registry_path)
    if not canonicals:
        logger.warning(
            "No brand canonicals found in CANONICAL_REGISTRY.csv. "
            "Empty coverage report. Run I77 P1 + add brand canonicals to the registry."
        )
        return 0

    bridges = parse_all_bridge_files(args.workspace_root)
    missing_bridges = [b.bridge_name for b in bridges if not b.exists]
    if missing_bridges:
        logger.error(
            "Bridge file(s) missing from workspace root: %s. Run I77 P1.",
            ", ".join(missing_bridges),
        )
        return 1

    report = compute_coverage(bridges, canonicals, strictness="soft")
    markdown = render_coverage_section_markdown(report, canonicals)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown, encoding="utf-8")
        logger.info("Coverage report written to %s", args.output)
    else:
        sys.stdout.write(markdown + "\n")

    logger.info(
        "Generated coverage report -- %d/%d brand canonicals cited by >= 1 bridge",
        report.canonical_count - len(report.missing_canonicals),
        report.canonical_count,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
