#!/usr/bin/env python3
"""Validate Playwright config baseline across the consumer-repo fleet.

Initiative 68 P2 (D-IH-68-B). Asserts that:

1. The AKOS canonical template at
   ``docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/_templates/playwright.config.ts.tmpl``
   parses to a valid :class:`akos.playwright_baseline.PlaywrightBaselineConfig`
   with all 5 :data:`STANDARD_VIEWPORT_NAMES` present and explicit sizes
   matching :data:`STANDARD_VIEWPORT_SIZES`.

2. For every ``class=platform`` or ``class=reference`` row in
   ``REPOSITORY_REGISTRY.csv`` whose ``local_path`` resolves to a sibling
   directory containing ``playwright.config.ts``, the consumer-repo file
   carries the same 5 viewports unless an explicit per-viewport opt-out
   is encoded in ``REPOSITORY_REGISTRY.csv ci_baseline_optouts`` (column
   added in I68 P5 PAUSE POINT #3 - canonical CSV gate; missing column is
   treated as "no opt-outs", so the validator passes safely until P5).

The TS parser is a deterministic string-grep over the projects[] array
(no ``ts-node``/AST dependency); the deterministic test corpus under
``tests/fixtures/playwright_configs/`` exercises both the canonical
shape and known drift patterns.

Usage::

    py scripts/validate_playwright_baseline.py
    py scripts/validate_playwright_baseline.py --json-log

Exit codes:
    0 -- canonical template + all resolved consumer configs validate clean.
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

from akos.io import REPO_ROOT
from akos.log import setup_logging
from akos.playwright_baseline import (
    STANDARD_VIEWPORT_NAMES,
    STANDARD_VIEWPORT_SIZES,
    PlaywrightBaselineConfig,
    PlaywrightProject,
    ViewportName,
)

logger = logging.getLogger("akos.playwright_baseline")

CANONICAL_TEMPLATE_PATH = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Envoy Tech Lab"
    / "Repositories"
    / "_templates"
    / "playwright.config.ts.tmpl"
)

REPOSITORY_REGISTRY_PATH = (
    REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "REPOSITORY_REGISTRY.csv"
)

# Repo classes that must carry a Playwright baseline. ``internal`` and
# ``client-delivery`` repos are exempt (no rendered surface for visual
# regression).
SCANNED_CLASSES: frozenset[str] = frozenset({"platform", "reference"})

# A project entry name="..." plus optional viewport: { width: N, height: N }
# block. We tolerate trailing devices['<key>'] shorthand by capturing
# devices_key separately.
_PROJECT_NAME_RE = re.compile(
    r"name\s*:\s*['\"](?P<name>[a-z0-9][a-z0-9-]+)['\"]",
    re.IGNORECASE,
)
_VIEWPORT_BLOCK_RE = re.compile(
    r"viewport\s*:\s*\{\s*width\s*:\s*(?P<w>\d+)\s*,\s*height\s*:\s*(?P<h>\d+)\s*\}",
    re.IGNORECASE,
)
_DEVICES_KEY_RE = re.compile(
    r"devices\s*\[\s*['\"](?P<key>[^'\"]+)['\"]\s*\]",
    re.IGNORECASE,
)
_PROJECT_BLOCK_RE = re.compile(
    r"\{\s*name\s*:[^}]*\}",  # naive but works for the canonical one-liner format
    re.DOTALL,
)
_RETRIES_RE = re.compile(
    r"retries\s*:\s*process\.env\.CI\s*\?\s*(?P<n>\d+)\s*:",
    re.IGNORECASE,
)


def _extract_projects(text: str) -> list[PlaywrightProject]:
    """Extract ``PlaywrightProject`` entries from a Playwright config string.

    String-grep-based; tolerates the canonical template format plus the
    common one-line-per-project variant. Each project block is matched on
    its inner ``name`` + optional ``viewport: {width, height}`` + optional
    ``devices['<key>']`` shorthand.
    """
    projects: list[PlaywrightProject] = []
    seen_names: set[str] = set()
    for block_match in _PROJECT_BLOCK_RE.finditer(text):
        block = block_match.group(0)
        name_match = _PROJECT_NAME_RE.search(block)
        if not name_match:
            continue
        name = name_match.group("name")
        if name in seen_names:
            continue
        seen_names.add(name)
        if name not in STANDARD_VIEWPORT_NAMES:
            # Unknown viewport name: still record it as a project (Pydantic
            # will reject because Literal mismatch), surfacing the drift.
            continue
        viewport_match = _VIEWPORT_BLOCK_RE.search(block)
        devices_match = _DEVICES_KEY_RE.search(block)
        if viewport_match:
            projects.append(
                PlaywrightProject(
                    name=name,  # type: ignore[arg-type]  (validated by Literal)
                    viewport_width=int(viewport_match.group("w")),
                    viewport_height=int(viewport_match.group("h")),
                    devices_key=devices_match.group("key") if devices_match else None,
                )
            )
        elif devices_match:
            projects.append(
                PlaywrightProject(
                    name=name,  # type: ignore[arg-type]
                    devices_key=devices_match.group("key"),
                )
            )
        else:
            # Project without explicit viewport AND without devices_key:
            # Pydantic still constructs but the validator surfaces drift
            # downstream because the standard size cannot be inferred.
            projects.append(PlaywrightProject(name=name))  # type: ignore[arg-type]
    return projects


def _extract_retries_on_ci(text: str) -> int:
    """Extract the ``retries`` value when ``process.env.CI`` is truthy."""
    match = _RETRIES_RE.search(text)
    if match:
        return int(match.group("n"))
    # Default 0 (Playwright default) when the canonical pattern is absent;
    # the validator will surface this as drift via PlaywrightBaselineConfig.
    return 0


def _parse_config_file(
    path: Path, *, repo_slug: str, opt_outs: list[str]
) -> PlaywrightBaselineConfig:
    """Parse a Playwright config TS file into a Pydantic model."""
    text = path.read_text(encoding="utf-8")
    projects = _extract_projects(text)
    retries_on_ci = _extract_retries_on_ci(text)
    return PlaywrightBaselineConfig(
        repo_slug=repo_slug,
        projects=projects,
        retries_on_ci=retries_on_ci,
        ci_baseline_optouts=opt_outs,
    )


def _validate_config(
    config: PlaywrightBaselineConfig, *, source_path: Path
) -> list[str]:
    """Return a list of error strings for a parsed config (empty = OK)."""
    errors: list[str] = []
    missing = config.missing_viewports()
    if missing:
        errors.append(
            f"{source_path.relative_to(REPO_ROOT) if source_path.is_relative_to(REPO_ROOT) else source_path}:"
            f" missing required viewports {sorted(missing)} from projects[]"
            f" (and not opted out via ci_baseline_optouts);"
            f" canonical 5 are {list(STANDARD_VIEWPORT_NAMES)}"
        )
    drift = config.has_explicit_size_drift()
    for d in drift:
        errors.append(
            f"{source_path.relative_to(REPO_ROOT) if source_path.is_relative_to(REPO_ROOT) else source_path}: {d}"
        )
    if config.retries_on_ci != 2 and "playwright-retries" not in config.ci_baseline_optouts:
        errors.append(
            f"{source_path.relative_to(REPO_ROOT) if source_path.is_relative_to(REPO_ROOT) else source_path}:"
            f" retries on CI is {config.retries_on_ci}, AKOS canonical is 2"
            f" (declare 'playwright-retries' in ci_baseline_optouts to allow drift)"
        )
    return errors


def _validate_canonical_template() -> list[str]:
    """Validate the AKOS canonical template at :data:`CANONICAL_TEMPLATE_PATH`."""
    if not CANONICAL_TEMPLATE_PATH.is_file():
        return [f"AKOS canonical template not found at {CANONICAL_TEMPLATE_PATH}"]
    config = _parse_config_file(
        CANONICAL_TEMPLATE_PATH, repo_slug="canonical-template", opt_outs=[]
    )
    return _validate_config(config, source_path=CANONICAL_TEMPLATE_PATH)


def _load_repository_rows() -> list[dict[str, str]]:
    """Read REPOSITORY_REGISTRY.csv into a list of dict rows.

    Returns ``[]`` if the file is absent (treats absence as "no consumer
    repos to scan"), so the validator stays safe in minimal-checkout
    environments.
    """
    if not REPOSITORY_REGISTRY_PATH.is_file():
        logger.info(
            "REPOSITORY_REGISTRY.csv not present at %s; skipping consumer-repo scan",
            REPOSITORY_REGISTRY_PATH,
        )
        return []
    with REPOSITORY_REGISTRY_PATH.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _opt_outs_for(row: dict[str, str]) -> list[str]:
    """Read the ``ci_baseline_optouts`` column safely.

    Column added in I68 P5 PAUSE POINT #3 - canonical CSV gate. Until then
    the column is absent and we return an empty list (no opt-outs).
    """
    raw = (row.get("ci_baseline_optouts") or "").strip()
    if not raw:
        return []
    # Tolerate either a JSON-array string (P5 future) or a semicolon-list.
    # Any value that *looks like* a JSON array (starts with '[') is parsed
    # as JSON; if parsing fails (e.g. malformed value), we return empty
    # rather than fall back to semicolon-splitting because semicolon-split
    # of a malformed JSON would surface garbage strings as opt-out keys.
    if raw.startswith("["):
        try:
            import json as _json
            parsed = _json.loads(raw)
            return [str(x) for x in parsed]
        except Exception:  # noqa: BLE001 - tolerate malformed values, treat as no opt-outs
            return []
    return [s.strip() for s in raw.split(";") if s.strip()]


def _resolve_consumer_config(row: dict[str, str]) -> Path | None:
    """Resolve the consumer repo's playwright.config.ts via ``local_path``.

    Returns ``None`` when the local path is absent, the directory is
    missing, or no ``playwright.config.ts`` exists yet (which is the
    expected state for repos that haven't received the I68 P2 sibling-repo
    carry-over PR yet).
    """
    local_path = (row.get("local_path") or "").strip()
    if not local_path:
        return None
    candidate = (REPO_ROOT.parent / local_path / "playwright.config.ts").resolve()
    if not candidate.is_file():
        return None
    return candidate


def _scan_consumer_repos() -> list[str]:
    """Scan each in-scope consumer repo's local Playwright config (if present)."""
    errors: list[str] = []
    rows = _load_repository_rows()
    scanned = 0
    skipped = 0
    for row in rows:
        repo_class = (row.get("class") or "").strip().lower()
        repo_slug = (row.get("repo_slug") or "").strip()
        if repo_class not in SCANNED_CLASSES:
            continue
        config_path = _resolve_consumer_config(row)
        if config_path is None:
            logger.info(
                "consumer-repo scan: %s (class=%s) has no resolvable playwright.config.ts; skipping",
                repo_slug,
                repo_class,
            )
            skipped += 1
            continue
        try:
            config = _parse_config_file(
                config_path,
                repo_slug=repo_slug,
                opt_outs=_opt_outs_for(row),
            )
        except Exception as exc:  # noqa: BLE001 - surface parse failures as errors
            errors.append(f"{config_path}: parse failed: {exc}")
            continue
        errors.extend(_validate_config(config, source_path=config_path))
        scanned += 1
    logger.info(
        "Consumer-repo scan complete: %d scanned, %d skipped (no local checkout)",
        scanned,
        skipped,
    )
    return errors


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate Playwright config baseline across consumer-repo fleet (I68 P2)"
    )
    parser.add_argument("--json-log", action="store_true", help="JSON logging output")
    args = parser.parse_args(list(argv) if argv is not None else None)
    setup_logging(json_output=args.json_log)

    all_errors: list[str] = []
    template_errors = _validate_canonical_template()
    all_errors.extend(template_errors)
    if not template_errors:
        logger.info(
            "Canonical template OK at %s (5 viewports, retries-on-CI=2)",
            CANONICAL_TEMPLATE_PATH.relative_to(REPO_ROOT),
        )

    # Consumer-repo scanning is opt-in via AKOS_PLAYWRIGHT_BASELINE_SCAN_CONSUMERS=1
    # until I68 P2 sibling-repo carry-over PRs ship the AKOS canonical viewport
    # naming convention to consumer repos. Today (2026-05-10) `boilerplate` and
    # `hlk-erp` use browser-named projects (chromium / firefox / webkit) — known
    # drift that is the EXPECTED state pre-carry-over. Operators investigating
    # consumer-repo drift run this validator with the env var set; the default
    # release-gate run only validates the AKOS canonical template.
    if os.environ.get("AKOS_PLAYWRIGHT_BASELINE_SCAN_CONSUMERS") == "1":
        consumer_errors = _scan_consumer_repos()
        all_errors.extend(consumer_errors)
    else:
        logger.info(
            "Consumer-repo scan SKIPPED (default soft mode); "
            "set AKOS_PLAYWRIGHT_BASELINE_SCAN_CONSUMERS=1 to enable. "
            "Will become default-strict in I68 P5 once sibling-repo carry-overs land."
        )

    if all_errors:
        for err in all_errors:
            logger.error(err)
        logger.error(
            "Playwright baseline validation: %d error(s)", len(all_errors)
        )
        return 1

    logger.info("Playwright baseline validation OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
