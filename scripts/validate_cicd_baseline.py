#!/usr/bin/env python3
"""Validate CICD baseline across the consumer-repo fleet (I68 P5 / D-IH-68-D).

Asserts that:

1. The AKOS canonical SOP at
   ``docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/SOP-CICD_BASELINE_001.md``
   is present + carries a ``status:`` of ``review`` or ``active`` + a known
   ``version:`` (per :data:`akos.cicd_baseline.KNOWN_SOP_VERSIONS`).
2. The AKOS canonical workflow template at
   ``docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/_templates/github-workflows/ci-baseline.yml.tmpl``
   is present and parseable as YAML (smoke-check; we don't enforce specific
   job names because the template evolves).
3. The AKOS canonical Render YAML stub at
   ``docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/_templates/render/render-baseline.yaml.tmpl``
   is present.
4. (Opt-in via ``AKOS_CICD_BASELINE_SCAN_CONSUMERS=1``) Every ``class=platform``
   or ``class=reference`` row in ``REPOSITORY_REGISTRY.csv`` constructs a valid
   :class:`akos.cicd_baseline.CICDBaselineRow`. This becomes default-strict
   in I68 P8 closure once sibling-repo carry-overs land.

Forward-compatible: tolerates absence of ``ci_baseline_version``,
``build_time_target_seconds``, ``ci_baseline_optouts`` columns until the
canonical CSV gate (I68 P5 PAUSE POINT #3) ships them.

Usage::

    py scripts/validate_cicd_baseline.py
    py scripts/validate_cicd_baseline.py --json-log

Exit codes:
    0 -- canonical SOP + templates OK + (when scanning) every row constructs
         a valid baseline model.
    1 -- one or more validation errors (printed to stderr).
"""

from __future__ import annotations

import argparse
import csv
import logging
import os
import re
import sys
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.cicd_baseline import (
    KNOWN_SOP_VERSIONS,
    CICDBaselineRow,
)
from akos.io import REPO_ROOT
from akos.log import setup_logging

logger = logging.getLogger("akos.cicd_baseline")

CANONICAL_SOP_PATH = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "Tech"
    / "System Owner"
    / "SOP-CICD_BASELINE_001.md"
)
CANONICAL_GHA_TEMPLATE_PATH = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Envoy Tech Lab"
    / "Repositories"
    / "_templates"
    / "github-workflows"
    / "ci-baseline.yml.tmpl"
)
CANONICAL_RENDER_STUB_PATH = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Envoy Tech Lab"
    / "Repositories"
    / "_templates"
    / "render"
    / "render-baseline.yaml.tmpl"
)

REPOSITORY_REGISTRY_PATH = (
    REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "REPOSITORY_REGISTRY.csv"
)

SCANNED_CLASSES: frozenset[str] = frozenset({"platform", "reference"})

# YAML frontmatter `status:` + `version:` extraction (deterministic; no PyYAML
# dependency for this lightweight smoke-check).
_FRONTMATTER_STATUS_RE = re.compile(r"^status:\s*([a-z_-]+)\s*$", re.MULTILINE | re.IGNORECASE)
_FRONTMATTER_VERSION_RE = re.compile(r"^version:\s*(v[0-9]+\.[0-9]+\.[0-9]+)\s*$", re.MULTILINE | re.IGNORECASE)


def _validate_canonical_sop() -> list[str]:
    """Validate the canonical SOP-CICD_BASELINE_001.md is present + has known status + version."""
    errors: list[str] = []
    if not CANONICAL_SOP_PATH.is_file():
        errors.append(f"AKOS canonical SOP not found at {CANONICAL_SOP_PATH}")
        return errors
    text = CANONICAL_SOP_PATH.read_text(encoding="utf-8")
    rel = CANONICAL_SOP_PATH.relative_to(REPO_ROOT)
    status_match = _FRONTMATTER_STATUS_RE.search(text)
    if status_match is None:
        errors.append(f"{rel}: missing `status:` frontmatter field")
    else:
        status = status_match.group(1).lower()
        if status not in {"review", "active"}:
            errors.append(
                f"{rel}: status {status!r} must be 'review' (during I68 P5) or 'active' "
                f"(after I68 P8 closure)"
            )
    version_match = _FRONTMATTER_VERSION_RE.search(text)
    if version_match is None:
        errors.append(f"{rel}: missing `version:` frontmatter field")
    else:
        version = version_match.group(1)
        if version not in KNOWN_SOP_VERSIONS:
            errors.append(
                f"{rel}: version {version!r} not in known set "
                f"{sorted(KNOWN_SOP_VERSIONS)} — bump akos.cicd_baseline.KNOWN_SOP_VERSIONS first"
            )
    return errors


def _validate_canonical_templates() -> list[str]:
    """Validate the canonical GHA workflow template + Render YAML stub are present."""
    errors: list[str] = []
    if not CANONICAL_GHA_TEMPLATE_PATH.is_file():
        errors.append(
            f"AKOS canonical GitHub Actions workflow template not found at "
            f"{CANONICAL_GHA_TEMPLATE_PATH}"
        )
    if not CANONICAL_RENDER_STUB_PATH.is_file():
        errors.append(
            f"AKOS canonical Render YAML stub not found at {CANONICAL_RENDER_STUB_PATH}"
        )
    return errors


def _load_repository_rows() -> list[dict[str, str]]:
    """Read REPOSITORY_REGISTRY.csv into a list of dict rows."""
    if not REPOSITORY_REGISTRY_PATH.is_file():
        logger.info(
            "REPOSITORY_REGISTRY.csv not present at %s; skipping consumer-repo scan",
            REPOSITORY_REGISTRY_PATH,
        )
        return []
    with REPOSITORY_REGISTRY_PATH.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _scan_consumer_repos() -> list[str]:
    """Scan each in-scope consumer-repo row for CICD-baseline metadata validity."""
    errors: list[str] = []
    rows = _load_repository_rows()
    scanned = 0
    skipped = 0
    for row in rows:
        repo_class = (row.get("class") or "").strip().lower()
        repo_slug = (row.get("repo_slug") or "").strip()
        if repo_class not in SCANNED_CLASSES:
            continue
        try:
            CICDBaselineRow.from_registry_row(row)
        except Exception as exc:  # noqa: BLE001 - surface model construction failures
            errors.append(
                f"REPOSITORY_REGISTRY.csv repo_slug={repo_slug}: "
                f"CICDBaselineRow validation failed: {exc!r}"
            )
            continue
        scanned += 1
    skipped = len(rows) - scanned - sum(
        1 for r in rows if (r.get("class") or "").strip().lower() not in SCANNED_CLASSES
    )
    logger.info(
        "Consumer-repo CICD-baseline scan complete: %d rows validated, %d skipped (out-of-scope class)",
        scanned,
        len(rows) - scanned,
    )
    return errors


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate CICD baseline across consumer-repo fleet (I68 P5)"
    )
    parser.add_argument("--json-log", action="store_true", help="JSON logging output")
    args = parser.parse_args(list(argv) if argv is not None else None)
    setup_logging(json_output=args.json_log)

    all_errors: list[str] = []

    sop_errors = _validate_canonical_sop()
    all_errors.extend(sop_errors)
    if not sop_errors:
        logger.info(
            "Canonical SOP-CICD_BASELINE_001.md OK at %s",
            CANONICAL_SOP_PATH.relative_to(REPO_ROOT),
        )

    template_errors = _validate_canonical_templates()
    all_errors.extend(template_errors)
    if not template_errors:
        logger.info(
            "Canonical GHA workflow template + Render YAML stub OK at %s + %s",
            CANONICAL_GHA_TEMPLATE_PATH.relative_to(REPO_ROOT),
            CANONICAL_RENDER_STUB_PATH.relative_to(REPO_ROOT),
        )

    if os.environ.get("AKOS_CICD_BASELINE_SCAN_CONSUMERS") == "1":
        consumer_errors = _scan_consumer_repos()
        all_errors.extend(consumer_errors)
    else:
        logger.info(
            "Consumer-repo scan SKIPPED (default soft mode); "
            "set AKOS_CICD_BASELINE_SCAN_CONSUMERS=1 to enable. "
            "Will become default-strict in I68 P8 closure once REPOSITORY_REGISTRY.csv "
            "ci_baseline_version + build_time_target_seconds + ci_baseline_optouts columns "
            "ship via I68 P5 PAUSE POINT #3 — canonical CSV gate."
        )

    if all_errors:
        for err in all_errors:
            logger.error(err)
        logger.error(
            "CICD baseline validation: %d error(s)", len(all_errors)
        )
        return 1

    logger.info("CICD baseline validation OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
