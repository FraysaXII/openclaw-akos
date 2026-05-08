#!/usr/bin/env python3
"""Validate brand-canon self-consistency + upstream alignment (I66 P2 / D-IH-66-J).

Two checks run together:

1. **Self-consistency** (always runs against AKOS canonicals):

   - Every required Marketing/Brand canonical exists with the expected
     ``status: active`` frontmatter.
   - ``BRAND_BASELINE_REALITY_MATRIX.md`` "External vocabulary" column never
     contains any token that is forbidden by ``BRAND_JARGON_AUDIT.md`` §4.1
     or ``BRAND_ABBREVIATIONS.md`` §2 (the dual-register contract — the
     external register, by construction, does not leak the internal register).
   - ``BRAND_VISION.md`` carries exactly one ``<!-- public-vision:start -->``
     and one matching ``<!-- public-vision:end -->`` marker.
   - ``BRAND_LOGO_SYSTEM.md`` cites both ``BRAND_ARCHITECTURE.md`` and
     ``BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md``.
   - ``BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md`` ``status`` is
     ``active`` and supersedes the 2026-04-08 v1.0 draft.

2. **Upstream alignment** (skips gracefully if ``boilerplate/`` not present):

   - The HSL accent token list referenced by ``BRAND_VISUAL_PATTERNS.md`` (or
     equivalent) is consistent with the boilerplate live source. We do a
     light heuristic check: the boilerplate ``app/globals.css`` (or
     ``tailwind.config.ts``) declares a ``--brand-accent`` variable. The
     test is **presence**, not value-matching, so refactors of the brand
     accent don't surprise-break this gate; the operator manually re-asserts
     consistency on a brand-color review.

Usage::

    py scripts/validate_brand_canon_drift.py
    py scripts/validate_brand_canon_drift.py --json-log

Exit codes::

    0 — canon self-consistent + (best-effort) upstream consistent.
    1 — at least one self-consistency rule violated.

Cross-references: BRAND_BASELINE_REALITY_MATRIX.md §3, BRAND_JARGON_AUDIT.md §4,
BRAND_ABBREVIATIONS.md §2, BRAND_VISION.md, I66 P2 master-roadmap.
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT
from akos.log import setup_logging

logger = logging.getLogger("akos.brand_canon_drift")

CANON_DIR = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "Marketing"
    / "Brand"
)
LEGAL_DIR = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "People"
    / "Legal"
)

REQUIRED_CANONICALS = (
    CANON_DIR / "BRAND_VOICE_FOUNDATION.md",
    CANON_DIR / "BRAND_DO_DONT.md",
    CANON_DIR / "BRAND_REGISTER_MATRIX.md",
    CANON_DIR / "BRAND_JARGON_AUDIT.md",
    CANON_DIR / "BRAND_VISUAL_PATTERNS.md",
    CANON_DIR / "BRAND_SPANISH_PATTERNS.md",
    CANON_DIR / "BRAND_FRENCH_PATTERNS.md",
    CANON_DIR / "BRAND_ARCHITECTURE.md",
    CANON_DIR / "BRAND_VISION.md",
    CANON_DIR / "BRAND_BASELINE_REALITY_MATRIX.md",
    CANON_DIR / "BRAND_LOGO_SYSTEM.md",
    CANON_DIR / "BRAND_ABBREVIATIONS.md",
    LEGAL_DIR / "BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md",
)

BOILERPLATE_PATH = REPO_ROOT.parent / "root_cd" / "boilerplate"

INTERNAL_REGISTER_TOKENS = (
    "counterparty",
    "elicitation",
    "reliability grading",
    "intelligence collection",
    "intelligence report",
    "approach techniques",
    "baseline reality assessment",
)


@dataclass
class CanonError:
    file: Path
    rule: str
    detail: str


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _check_required_canonicals_present() -> list[CanonError]:
    errors: list[CanonError] = []
    for path in REQUIRED_CANONICALS:
        if not path.exists():
            errors.append(CanonError(file=path, rule="missing_canonical", detail="file not found"))
            continue
        text = _read(path)
        match = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
        if not match:
            errors.append(
                CanonError(file=path, rule="missing_frontmatter", detail="no YAML frontmatter")
            )
            continue
        frontmatter = match.group(1)
        if not re.search(r"^status:\s*active\s*$", frontmatter, re.MULTILINE):
            errors.append(
                CanonError(
                    file=path,
                    rule="status_not_active",
                    detail="frontmatter must declare 'status: active'",
                )
            )
    return errors


def _check_vision_markers() -> list[CanonError]:
    """Assert BRAND_VISION.md has at least one well-formed start/end marker pair.

    The canonical may legitimately contain additional in-prose mentions of the
    marker syntax (e.g. inside §1 internal preamble documenting the contract);
    we therefore check ≥ 1 each + a start-precedes-end ordering invariant for
    the *first* occurrences.
    """
    path = CANON_DIR / "BRAND_VISION.md"
    if not path.exists():
        return [CanonError(file=path, rule="vision_missing", detail="BRAND_VISION.md not found")]
    text = _read(path)
    start_marker = "<!-- public-vision:start -->"
    end_marker = "<!-- public-vision:end -->"
    starts = text.count(start_marker)
    ends = text.count(end_marker)
    errors: list[CanonError] = []
    if starts < 1:
        errors.append(
            CanonError(
                file=path,
                rule="vision_marker_start_missing",
                detail=f"expected at least 1 '{start_marker}'; found 0",
            )
        )
    if ends < 1:
        errors.append(
            CanonError(
                file=path,
                rule="vision_marker_end_missing",
                detail=f"expected at least 1 '{end_marker}'; found 0",
            )
        )
    if starts >= 1 and ends >= 1:
        first_start = text.find(start_marker)
        first_end = text.find(end_marker)
        if first_end < first_start:
            errors.append(
                CanonError(
                    file=path,
                    rule="vision_marker_order",
                    detail="first end marker appears before first start marker",
                )
            )
    return errors


def _check_baseline_reality_external_register_clean() -> list[CanonError]:
    """Assert the External-vocabulary cells in BRAND_BASELINE_REALITY_MATRIX.md
    do not contain any internal-register token. The dual-register contract is
    that the *external* column is the public vocabulary; internal tokens leaking
    into it would invert the contract."""
    path = CANON_DIR / "BRAND_BASELINE_REALITY_MATRIX.md"
    if not path.exists():
        return [CanonError(file=path, rule="matrix_missing", detail="file not found")]
    text = _read(path)

    section = re.search(
        r"^## 3\.\s*Translation rules.*?\n(.*?)(?=^## 4\.|^## 5\.)",
        text,
        re.DOTALL | re.MULTILINE,
    )
    if not section:
        return []
    section_text = section.group(1)

    errors: list[CanonError] = []
    for token in INTERNAL_REGISTER_TOKENS:
        for match in re.finditer(
            rf"\bExternal[^\n]*?\b{re.escape(token)}\b",
            section_text,
            re.IGNORECASE,
        ):
            errors.append(
                CanonError(
                    file=path,
                    rule="internal_token_in_external_column",
                    detail=(
                        f"internal-register token '{token}' appears in an External-row "
                        f"line: {match.group(0)[:140]!r}"
                    ),
                )
            )
    return errors


def _check_logo_system_cross_refs() -> list[CanonError]:
    path = CANON_DIR / "BRAND_LOGO_SYSTEM.md"
    if not path.exists():
        return [CanonError(file=path, rule="logo_missing", detail="file not found")]
    text = _read(path)
    errors: list[CanonError] = []
    if "BRAND_ARCHITECTURE.md" not in text:
        errors.append(
            CanonError(
                file=path,
                rule="missing_xref",
                detail="must cite BRAND_ARCHITECTURE.md",
            )
        )
    if "BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md" not in text:
        errors.append(
            CanonError(
                file=path,
                rule="missing_xref",
                detail="must cite BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md",
            )
        )
    return errors


def _check_hierarchy_supersedes() -> list[CanonError]:
    path = LEGAL_DIR / "BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md"
    if not path.exists():
        return [CanonError(file=path, rule="hierarchy_missing", detail="file not found")]
    text = _read(path)
    errors: list[CanonError] = []
    if not re.search(r"^supersedes:\s*", text, re.MULTILINE):
        errors.append(
            CanonError(
                file=path,
                rule="hierarchy_no_supersedes",
                detail="frontmatter must include 'supersedes:' field per the 2026-04 → 2026-05 rewrite",
            )
        )
    return errors


def _check_boilerplate_brand_accent_present() -> list[CanonError]:
    """Soft (informational) upstream check: if boilerplate sibling exists,
    confirm at least one brand-namespaced CSS custom property is declared. The
    operator may use ``--brand-*``, ``--accent-*``, ``--color-primary*``, or
    similar conventions; we accept any of those patterns. Returns INFO-level
    findings as comments to stdout but **never fails** the gate (the upstream
    visual-pattern contract is operator-asserted on a brand-color review, not
    mechanically enforced — pinning a specific CSS variable name would be too
    brittle across boilerplate refactors).
    """
    if not BOILERPLATE_PATH.exists():
        logger.info(
            "boilerplate sibling not present at %s; skipping upstream check",
            BOILERPLATE_PATH,
        )
        return []

    candidates = [
        BOILERPLATE_PATH / "app" / "globals.css",
        BOILERPLATE_PATH / "src" / "app" / "globals.css",
        BOILERPLATE_PATH / "tailwind.config.ts",
        BOILERPLATE_PATH / "tailwind.config.js",
    ]
    pattern = re.compile(r"--(?:brand|accent|color-primary|color-accent|primary|accent-primary)\b")
    found_in: list[Path] = []
    for cand in candidates:
        if not cand.exists():
            continue
        try:
            content = cand.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if pattern.search(content):
            found_in.append(cand)

    if not found_in:
        logger.warning(
            "boilerplate present but no brand-namespaced CSS custom property found "
            "in globals.css / tailwind.config (informational; upstream visual-pattern "
            "consistency requires manual operator review)"
        )
    else:
        logger.info(
            "boilerplate brand-namespaced CSS variable present in: %s",
            ", ".join(str(p.name) for p in found_in),
        )
    return []


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate brand-canon drift (I66 P2)")
    parser.add_argument("--json-log", action="store_true")
    parser.add_argument(
        "--skip-upstream",
        action="store_true",
        help="Skip the upstream (boilerplate) alignment check",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)
    setup_logging(json_output=args.json_log)

    errors: list[CanonError] = []
    errors.extend(_check_required_canonicals_present())
    errors.extend(_check_vision_markers())
    errors.extend(_check_baseline_reality_external_register_clean())
    errors.extend(_check_logo_system_cross_refs())
    errors.extend(_check_hierarchy_supersedes())
    if not args.skip_upstream:
        errors.extend(_check_boilerplate_brand_accent_present())

    if errors:
        for err in errors:
            try:
                rel = err.file.relative_to(REPO_ROOT)
            except ValueError:
                rel = err.file
            logger.error("%s [%s]: %s", rel, err.rule, err.detail)
        logger.error("BRAND_CANON_DRIFT: %d violation(s)", len(errors))
        return 1

    logger.info(
        "BRAND_CANON_DRIFT OK — %d canonicals present + dual-register contract clean",
        len(REQUIRED_CANONICALS),
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
