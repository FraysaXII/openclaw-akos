#!/usr/bin/env python3
"""Validate Sentry release-format across the consumer-repo fleet (I68 P4).

Asserts that each ``class=platform`` (or explicitly opted-in) consumer repo's
Sentry init code emits a release string matching the canonical
``<repo_slug>@<sha_short>`` template (D-IH-68-I; see
:mod:`akos.sentry_release`).

The check is **forward-compatible**:

- Default mode (no env var) only validates the canonical doc at
  ``docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/Repositories/SENTRY_DASHBOARD_HOLISTIKA.md``
  (presence of the canonical-format example block).
- ``AKOS_SENTRY_RELEASE_SCAN_CONSUMERS=1`` enables a per-consumer-repo scan
  that walks each repo's Sentry config files (``sentry.client.config.ts``,
  ``sentry.server.config.ts`` for Next.js; ``sentry_sdk.init(...)`` calls
  for Python FastAPI surfaces) looking for the ``release:`` field. This
  becomes default-strict in I68 P5 once sibling-repo carry-overs land.

Per ``akos-governance-remediation.mdc`` reuse-only rule: no parallel framework
introduced; uses ``akos.io.REPO_ROOT``, ``akos.log.setup_logging``, and the
canonical Pydantic models in ``akos.sentry_release``.

Usage::

    py scripts/validate_sentry_release_format.py
    py scripts/validate_sentry_release_format.py --json-log

Exit codes:
    0 -- canonical doc OK + (when scanning) all resolved consumer configs
         emit the canonical release format.
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
from akos.sentry_release import (
    RELEASE_TEMPLATE_CANONICAL,
    SentryReleaseFormatRule,
    parse_release_value,
)

logger = logging.getLogger("akos.sentry_release")

CANONICAL_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "Envoy Tech Lab"
    / "Repositories"
    / "SENTRY_DASHBOARD_HOLISTIKA.md"
)

REPOSITORY_REGISTRY_PATH = (
    REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "REPOSITORY_REGISTRY.csv"
)

# Repo classes that must carry a Sentry release-format. ``internal`` and
# ``client-delivery`` repos are exempt (per SOP-CICD_BASELINE_001 draft in P5).
SCANNED_CLASSES: frozenset[str] = frozenset({"platform", "reference"})

# Sentry config file globs we look in for the ``release:`` field.
# Next.js: sentry.client.config.{ts,js}, sentry.server.config.{ts,js},
#          sentry.edge.config.{ts,js}, next.config.{mjs,js,ts} (withSentryConfig).
# Python (FastAPI): any *.py with sentry_sdk.init( ... ) call.
NEXTJS_SENTRY_CONFIG_GLOBS: tuple[str, ...] = (
    "sentry.client.config.ts",
    "sentry.client.config.js",
    "sentry.server.config.ts",
    "sentry.server.config.js",
    "sentry.edge.config.ts",
    "sentry.edge.config.js",
)
NEXTJS_BUILD_CONFIG_GLOBS: tuple[str, ...] = ("next.config.mjs", "next.config.js", "next.config.ts")
PYTHON_SENTRY_INIT_GLOBS: tuple[str, ...] = ("**/main.py", "**/app.py", "**/sentry_init.py")

# release: "..." or release: '...' or release: `...` (template literal).
# Captures the literal string contents WITHOUT the surrounding quote chars.
_RELEASE_FIELD_RE = re.compile(
    r"release\s*[:=]\s*([\"'`])(?P<value>[^\"'`]+)\1",
    re.IGNORECASE,
)
# Python form: release=f"..." or release="..."; tolerates f-string prefix.
_PYTHON_RELEASE_FIELD_RE = re.compile(
    r"release\s*=\s*f?[\"']([^\"']+)[\"']",
    re.IGNORECASE,
)


def _validate_canonical_doc() -> list[str]:
    """Validate the AKOS canonical Sentry dashboard doc is present + carries
    the canonical release-format example.
    """
    errors: list[str] = []
    if not CANONICAL_DOC_PATH.is_file():
        errors.append(
            f"AKOS canonical Sentry dashboard doc not found at {CANONICAL_DOC_PATH}"
        )
        return errors
    text = CANONICAL_DOC_PATH.read_text(encoding="utf-8")
    if RELEASE_TEMPLATE_CANONICAL not in text:
        errors.append(
            f"{CANONICAL_DOC_PATH.relative_to(REPO_ROOT)}: "
            f"missing canonical release-format example {RELEASE_TEMPLATE_CANONICAL!r} "
            f"(per D-IH-68-I); the doc is the SSOT — operators should be able to copy "
            f"the format from it verbatim"
        )
    # Smoke-check the Pydantic rule still accepts the canonical template; any
    # future drift in the constant would surface here.
    try:
        SentryReleaseFormatRule(release_template=RELEASE_TEMPLATE_CANONICAL)
    except Exception as exc:  # noqa: BLE001 - surface validator-rule drift
        errors.append(
            f"akos.sentry_release.SentryReleaseFormatRule rejected the canonical "
            f"template {RELEASE_TEMPLATE_CANONICAL!r}: {exc!r}"
        )
    return errors


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


def _resolve_consumer_root(row: dict[str, str]) -> Path | None:
    """Resolve the consumer repo's local checkout root via ``local_path``."""
    local_path = (row.get("local_path") or "").strip()
    if not local_path:
        return None
    candidate = (REPO_ROOT.parent / local_path).resolve()
    if not candidate.is_dir():
        return None
    return candidate


def _scan_for_release_strings(
    repo_root: Path, *, repo_slug: str
) -> list[tuple[Path, str]]:
    """Walk a consumer repo's Sentry config files extracting release values.

    Returns a list of (file_path, raw_release_value) tuples.
    """
    hits: list[tuple[Path, str]] = []
    for config_name in NEXTJS_SENTRY_CONFIG_GLOBS:
        config_path = repo_root / config_name
        if not config_path.is_file():
            continue
        text = config_path.read_text(encoding="utf-8", errors="replace")
        for match in _RELEASE_FIELD_RE.finditer(text):
            hits.append((config_path, match.group("value")))
    for build_config_name in NEXTJS_BUILD_CONFIG_GLOBS:
        config_path = repo_root / build_config_name
        if not config_path.is_file():
            continue
        text = config_path.read_text(encoding="utf-8", errors="replace")
        for match in _RELEASE_FIELD_RE.finditer(text):
            hits.append((config_path, match.group("value")))
    for python_glob in PYTHON_SENTRY_INIT_GLOBS:
        for py_path in repo_root.glob(python_glob):
            if not py_path.is_file():
                continue
            text = py_path.read_text(encoding="utf-8", errors="replace")
            if "sentry_sdk.init" not in text and "Sentry.init" not in text:
                continue
            for match in _PYTHON_RELEASE_FIELD_RE.finditer(text):
                hits.append((py_path, match.group(1)))
    return hits


def _validate_release_value(
    raw_value: str, *, expected_repo_slug: str, source_path: Path
) -> list[str]:
    """Validate a single extracted release value matches the canonical shape."""
    errors: list[str] = []
    rel = source_path.relative_to(REPO_ROOT.parent) if source_path.is_relative_to(REPO_ROOT.parent) else source_path
    # Allow Sentry-template-string forms that contain literal placeholders
    # the runtime substitutes (e.g. ``boilerplate@${process.env.GIT_SHA}``);
    # the validator only enforces the prefix shape.
    bare = raw_value.split("@", 1)[0] if "@" in raw_value else raw_value
    has_at = "@" in raw_value
    if not has_at:
        errors.append(
            f"{rel}: release {raw_value!r} missing '@<sha>' suffix; "
            f"canonical is '{RELEASE_TEMPLATE_CANONICAL}' per D-IH-68-I"
        )
        return errors
    if bare != expected_repo_slug:
        errors.append(
            f"{rel}: release prefix {bare!r} does not match REPOSITORY_REGISTRY "
            f"repo_slug {expected_repo_slug!r}; rename per D-IH-68-I"
        )
    parsed = parse_release_value(raw_value)
    # Tolerate template-literal SHA forms: only fail when the SHA portion is
    # neither a real short-SHA nor a known templating placeholder.
    if parsed is None:
        sha_part = raw_value.split("@", 1)[1] if has_at else ""
        sha_part_stripped = sha_part.strip()
        # Known templating placeholders we accept (Vercel/Render env-var
        # interpolation, Next.js process.env reads, Python f-string slices).
        is_template = any(
            tok in sha_part_stripped
            for tok in (
                "${",
                "{{",
                "process.env",
                "os.environ",
                "RENDER_GIT_COMMIT",
                "VERCEL_GIT_COMMIT_SHA",
            )
        )
        if not is_template:
            errors.append(
                f"{rel}: release SHA portion {sha_part!r} is neither a 7-12 char hex "
                f"short-SHA nor a recognised templating placeholder "
                f"({', '.join(['${', '{{', 'process.env', 'os.environ', 'RENDER_GIT_COMMIT', 'VERCEL_GIT_COMMIT_SHA'])})"
            )
    return errors


def _scan_consumer_repos() -> list[str]:
    """Scan each in-scope consumer repo for Sentry release-format drift."""
    errors: list[str] = []
    rows = _load_repository_rows()
    scanned = 0
    skipped = 0
    no_release = 0
    for row in rows:
        repo_class = (row.get("class") or "").strip().lower()
        repo_slug = (row.get("repo_slug") or "").strip()
        if repo_class not in SCANNED_CLASSES:
            continue
        repo_root = _resolve_consumer_root(row)
        if repo_root is None:
            logger.info(
                "consumer-repo scan: %s (class=%s) has no resolvable local_path; skipping",
                repo_slug,
                repo_class,
            )
            skipped += 1
            continue
        hits = _scan_for_release_strings(repo_root, repo_slug=repo_slug)
        if not hits:
            logger.warning(
                "consumer-repo scan: %s (class=%s) has no Sentry release: ... field "
                "in any of the canonical config files; will be flagged as drift "
                "once I68 P5 sibling-repo carry-overs land. Skipping for now.",
                repo_slug,
                repo_class,
            )
            no_release += 1
            continue
        for source_path, raw_value in hits:
            errors.extend(
                _validate_release_value(
                    raw_value, expected_repo_slug=repo_slug, source_path=source_path
                )
            )
        scanned += 1
    logger.info(
        "Consumer-repo scan complete: %d scanned (release fields validated), "
        "%d skipped (no local checkout), %d skipped (no release: field — pre-carry-over state)",
        scanned,
        skipped,
        no_release,
    )
    return errors


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate Sentry release-format across consumer-repo fleet (I68 P4)"
    )
    parser.add_argument("--json-log", action="store_true", help="JSON logging output")
    args = parser.parse_args(list(argv) if argv is not None else None)
    setup_logging(json_output=args.json_log)

    all_errors: list[str] = []
    doc_errors = _validate_canonical_doc()
    all_errors.extend(doc_errors)
    if not doc_errors:
        logger.info(
            "Canonical Sentry dashboard doc OK at %s (carries canonical release-format example)",
            CANONICAL_DOC_PATH.relative_to(REPO_ROOT),
        )

    if os.environ.get("AKOS_SENTRY_RELEASE_SCAN_CONSUMERS") == "1":
        consumer_errors = _scan_consumer_repos()
        all_errors.extend(consumer_errors)
    else:
        logger.info(
            "Consumer-repo scan SKIPPED (default soft mode); "
            "set AKOS_SENTRY_RELEASE_SCAN_CONSUMERS=1 to enable. "
            "Will become default-strict in I68 P5 once sibling-repo carry-overs land."
        )

    if all_errors:
        for err in all_errors:
            logger.error(err)
        logger.error(
            "Sentry release-format validation: %d error(s)", len(all_errors)
        )
        return 1

    logger.info("Sentry release-format validation OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
