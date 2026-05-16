#!/usr/bin/env python3
"""Validate Impeccable bridge drift against the brand-canonical inventory (I77 P2).

Drift contract (per I77 master-roadmap §"Strand B" + D-IH-77-C):

- Every active brand canonical under
  ``docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/`` (filtered
  via ``CANONICAL_REGISTRY.csv`` ``owning_area=Marketing`` + ``owning_role=Brand``
  + non-SOP + status=active) MUST appear as a cross-reference in **at least
  one** workspace-root bridge file (PRODUCT.md / DESIGN.md / BASELINE_REALITY.md).

- Strictness ladder per D-IH-77-C: **soft-30d-then-strict** (default;
  matches ``validate_cicd_baseline.py`` precedent). The env override
  ``AKOS_IMPECCABLE_BRIDGE_DRIFT_STRICT=1`` flips soft → strict. The
  release-gate row is **INFO** until I77 P3 closure (per master-roadmap
  §"Drift gate"), then flips to **FAIL**.

Bridges that don't exist at workspace root fail loud regardless of mode
(all 3 are expected post-I77 P1).

Usage::

    py scripts/validate_impeccable_bridge_drift.py
    py scripts/validate_impeccable_bridge_drift.py --strict
    py scripts/validate_impeccable_bridge_drift.py --workspace-root /path/to/repo

Exit codes::

    0 — no drift OR soft mode (per-canonical warnings logged but non-failing).
    1 — strict mode AND drift detected (missing canonical) OR a bridge file
        is missing from workspace root.

Cross-references:
  ``akos/impeccable_bridge.py`` — Pydantic chassis + parsers + coverage.
  ``scripts/generate_impeccable_bridges.py`` — sibling tool (coverage reporter).
  ``docs/wip/planning/77-impeccable-brand-bridge-refresh/master-roadmap.md`` §"Strand B".
  D-IH-77-C — Strand B posture (soft-30d-then-strict; Pydantic chassis).
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.impeccable_bridge import (  # noqa: E402
    CANONICAL_REGISTRY_PATH,
    compute_coverage,
    parse_all_bridge_files,
    parse_canonical_inventory,
)
from akos.io import REPO_ROOT  # noqa: E402
from akos.log import setup_logging  # noqa: E402

logger = logging.getLogger("akos.impeccable_bridge_drift")

ENV_STRICT = "AKOS_IMPECCABLE_BRIDGE_DRIFT_STRICT"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate Impeccable bridge drift against brand-canonical inventory "
            "(I77 P2; D-IH-77-C soft-30d-then-strict default)."
        )
    )
    parser.add_argument(
        "--workspace-root",
        type=Path,
        default=REPO_ROOT,
        help="Workspace root to scan (default: AKOS repo root).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help=(
            "Force strict mode (FAIL on any drift). Default: soft "
            "(WARN per missing canonical; exit 0 unless a bridge file is missing). "
            f"Env override: {ENV_STRICT}=1 also forces strict."
        ),
    )
    args = parser.parse_args(argv)
    setup_logging()

    strict_mode = args.strict or os.environ.get(ENV_STRICT) == "1"
    strictness = "strict" if strict_mode else "soft"

    registry_path = args.workspace_root / CANONICAL_REGISTRY_PATH
    if not registry_path.exists():
        logger.error(
            "CANONICAL_REGISTRY.csv not found at %s; cannot run drift gate",
            registry_path,
        )
        return 1

    canonicals = parse_canonical_inventory(registry_path)
    if not canonicals:
        logger.warning(
            "No brand canonicals found in CANONICAL_REGISTRY.csv (empty filter result). "
            "Skipping drift gate as graceful no-op."
        )
        return 0

    bridges = parse_all_bridge_files(args.workspace_root)
    missing_bridges = [b.bridge_name for b in bridges if not b.exists]
    if missing_bridges:
        logger.error(
            "Bridge file(s) missing from workspace root: %s. "
            "Run I77 P1 to author them.",
            ", ".join(missing_bridges),
        )
        return 1

    for bridge in bridges:
        if not bridge.has_akos_precedence_rule:
            logger.warning(
                "Bridge %s lacks the non-negotiable 'AKOS precedence rule' section "
                "(per SOP-HLK_TOOLING_STANDARDS_001.md §3.7).",
                bridge.bridge_name,
            )

    report = compute_coverage(bridges, canonicals, strictness=strictness)

    logger.info(
        "Coverage: %d/%d brand canonicals cited by >= 1 bridge (%.1f%%); strictness=%s",
        report.canonical_count - len(report.missing_canonicals),
        report.canonical_count,
        report.coverage_ratio * 100,
        strictness,
    )

    if not report.has_drift:
        logger.info(
            "BRIDGE drift OK -- all %d brand canonicals cited by >= 1 bridge",
            report.canonical_count,
        )
        return 0

    canonicals_by_id = {c.canonical_id: c for c in canonicals}
    for canonical_id in report.missing_canonicals:
        canonical = canonicals_by_id.get(canonical_id)
        if not canonical:
            continue
        log_fn = logger.error if strict_mode else logger.warning
        log_fn(
            "DRIFT -- canonical '%s' (%s) not cited by any bridge "
            "(PRODUCT.md / DESIGN.md / BASELINE_REALITY.md). "
            "Add a cross-reference link.",
            canonical.canonical_id,
            canonical.filename,
        )

    if strict_mode:
        logger.error(
            "BRIDGE drift FAIL -- %d brand canonical(s) missing from all bridges "
            "(strict mode; --strict or %s=1)",
            len(report.missing_canonicals),
            ENV_STRICT,
        )
        return 1

    logger.warning(
        "BRIDGE drift SOFT-WARN -- %d brand canonical(s) missing from all bridges. "
        "Exit 0 (soft-30d-then-strict per D-IH-77-C). "
        "Promote to strict with --strict or %s=1.",
        len(report.missing_canonicals),
        ENV_STRICT,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
