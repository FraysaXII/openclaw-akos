#!/usr/bin/env python3
"""Validate the dual-register contract for BRAND_BASELINE_REALITY_MATRIX.md (I66 P2).

The dual-register contract (per BRAND_BASELINE_REALITY_MATRIX.md §3 + D-IH-66-M)
is asymmetric:

- **Internal register** (HUMINT-grounded vocabulary: counterparty, elicitation,
  reliability grading, intelligence collection, intelligence report, approach
  techniques, baseline reality assessment) is allowed in operator-private
  surfaces — internal SOPs, agent transcripts, AKOS-vault internal docs,
  ``docs/wip/intelligence/`` working space, decks' ``.counterparty-brief.md``
  companions, deck ``.objections.md`` companions.
- **External register** is the canonical for any rendered surface served to a
  non-cleared audience: ``boilerplate/`` rendered DOM, deck **slide bodies**
  (not their companions), public ``hlk-erp/app/(public)/`` routes, press,
  email signatures, and any artefact under ``_assets/advops/`` whose
  ``intellectual_kind`` is *not* a counterparty-brief.

This validator asserts:

1. Internal-register tokens **never** appear in deck slide bodies under
   ``docs/references/hlk/v3.0/_assets/advops/**/deck/*.yaml`` (deck companion
   files ``*.objections.md`` and ``*.counterparty-brief.md`` are intentionally
   exempt — they carry the internal register).
2. Internal-register tokens never appear in
   ``docs/references/hlk/v3.0/_assets/advops/**/dossier_*.md`` rendered prose
   (dossiers are external deliverables — same rule as decks).
3. Sibling ``boilerplate/`` rendered DOM under ``app/`` and ``messages/``
   never contains internal-register tokens. Skip gracefully if the sibling
   is absent.

The internal-register token list is parsed from
BRAND_BASELINE_REALITY_MATRIX.md §3 ("Translation rules") at run time, so the
validator does not drift from canon: edit the canonical and re-run.

Per the I76 P3 Lane 3 refactor (2026-05-19): the scan helpers
(``InternalToken``, ``BaselineHit``, ``scan_text``, ``load_canonical_tokens``)
moved from this script into :mod:`akos.brand_baseline_reality` so the same
scanner powers ``scripts/madeira_personality_check.py`` (Madeira's per-output
self-policing call surface). This script is now a thin CLI shim around the
shared module — argv + exit codes + log output are unchanged.

Usage::

    py scripts/validate_brand_baseline_reality_drift.py
    py scripts/validate_brand_baseline_reality_drift.py --json-log

Exit codes::

    0 — no internal-register leakage detected.
    1 — at least one internal-register token found in an external-register surface.

Cross-references: BRAND_BASELINE_REALITY_MATRIX.md §3, BRAND_JARGON_AUDIT.md §4.1,
.cursor/rules/akos-brand-baseline-reality.mdc (P2), I66 P2 master-roadmap.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.brand_baseline_reality import (
    BaselineHit,
    InternalToken,
    MATRIX_PATH,
    load_canonical_tokens,
    scan_text,
)
from akos.brand_baseline_reality import (
    _build_token_patterns,
    _extract_internal_tokens_from_matrix,
)
from akos.io import REPO_ROOT
from akos.log import setup_logging

__all__ = [
    "BaselineHit",
    "InternalToken",
    "MATRIX_PATH",
    "load_canonical_tokens",
    "scan_text",
    "_build_token_patterns",
    "_extract_internal_tokens_from_matrix",
    "_scan_text",
    "main",
]

logger = logging.getLogger("akos.brand_baseline_reality")

ADVOPS_DIR = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "_assets" / "advops"

DEFAULT_CONSUMER_ROOTS = (REPO_ROOT.parent / "root_cd" / "boilerplate",)

EXEMPT_FILE_SUFFIXES = (".objections.md", ".counterparty-brief.md")


def _is_exempt(path: Path) -> bool:
    name = path.name.lower()
    return any(name.endswith(suf) for suf in EXEMPT_FILE_SUFFIXES)


def _scan_path(path: Path, tokens: list[InternalToken]) -> list[BaselineHit]:
    """Read ``path`` and scan it via ``akos.brand_baseline_reality.scan_text``.

    Honours the validator-local exemption rule (``EXEMPT_FILE_SUFFIXES``) and
    the markdown / mermaid frontmatter strip rule.
    """
    if _is_exempt(path):
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    strip_frontmatter = path.suffix.lower() in {".md", ".mmd"}
    return scan_text(
        text,
        tokens=tokens,
        strip_frontmatter=strip_frontmatter,
        file=path,
    )


_scan_text = _scan_path


def _scan_advops_decks_and_dossiers(tokens: list[InternalToken]) -> list[BaselineHit]:
    if not ADVOPS_DIR.exists():
        return []
    hits: list[BaselineHit] = []
    # I86 P3 (D-IH-86-L) extension: the adviser-surface glob set widens P2's deck+dossier
    # scope to include founder-filed instrument prose, adviser handoff exports, and any
    # markdown under _assets/advops/**/founder-filed/. These are operator-authored prose
    # destined for adviser review; they must not carry the internal-register `PRJ-HOL-*`
    # program-anchor ids. Companion files (*.objections.md / *.counterparty-brief.md) remain
    # exempt via EXEMPT_FILE_SUFFIXES because they intentionally carry the internal register.
    for pattern in (
        "**/deck/*.yaml",
        "**/dossier_*.md",
        "**/deck_slides.yaml",
        "**/founder-filed/**/*.md",
        "**/adviser-handoff/*.md",
    ):
        for path in ADVOPS_DIR.glob(pattern):
            if path.is_file():
                hits.extend(_scan_path(path, tokens))
    return hits


def _scan_boilerplate(consumer_roots: list[Path], tokens: list[InternalToken]) -> list[BaselineHit]:
    hits: list[BaselineHit] = []
    for root in consumer_roots:
        for sub in ("app", "messages", "i18n/messages", "components"):
            base = root / sub
            if not base.exists():
                continue
            for path in base.rglob("*"):
                if not path.is_file():
                    continue
                if path.suffix.lower() not in {".tsx", ".ts", ".jsx", ".js", ".mdx", ".md", ".json", ".html"}:
                    continue
                if any(part in {"node_modules", ".next", ".turbo", "dist"} for part in path.parts):
                    continue
                hits.extend(_scan_path(path, tokens))
    return hits


def _resolve_consumer_roots(extra: list[Path]) -> list[Path]:
    out: list[Path] = []
    seen: set[Path] = set()
    for root in (*extra, *DEFAULT_CONSUMER_ROOTS):
        if not root.exists():
            continue
        resolved = root.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        out.append(resolved)
    return out


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate baseline-reality dual-register contract (I66 P2)")
    parser.add_argument("--json-log", action="store_true")
    parser.add_argument("--consumer-root", action="append", default=[])
    parser.add_argument("--skip-consumer", action="store_true", help="Only scan AKOS-internal advops surfaces")
    args = parser.parse_args(list(argv) if argv is not None else None)
    setup_logging(json_output=args.json_log)

    tokens = load_canonical_tokens(MATRIX_PATH)
    if not tokens:
        logger.error("Could not extract internal-register token list. Refusing to PASS.")
        return 1

    all_hits: list[BaselineHit] = _scan_advops_decks_and_dossiers(tokens)

    if not args.skip_consumer:
        consumer_roots = _resolve_consumer_roots([Path(p) for p in args.consumer_root])
        if consumer_roots:
            all_hits.extend(_scan_boilerplate(consumer_roots, tokens))
        else:
            logger.info("No consumer repos found; scanning AKOS-internal advops surfaces only")

    if all_hits:
        for hit in all_hits[:200]:
            try:
                rel = hit.file.relative_to(REPO_ROOT.parent) if hit.file else Path("<in-memory>")
            except ValueError:
                rel = hit.file if hit.file else Path("<in-memory>")
            logger.error(
                "%s:%d  internal-register token %r leaked into external surface: %s",
                rel,
                hit.line,
                hit.token.token,
                hit.snippet,
            )
        if len(all_hits) > 200:
            logger.error("... and %d more hits suppressed", len(all_hits) - 200)
        logger.error(
            "BRAND_BASELINE_REALITY: %d internal-register leakage(s) across %d file(s)",
            len(all_hits),
            len({h.file for h in all_hits if h.file is not None}),
        )
        return 1

    logger.info(
        "BRAND_BASELINE_REALITY OK — dual-register contract holds; %d internal token(s) checked",
        len(tokens),
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
