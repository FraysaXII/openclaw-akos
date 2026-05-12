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
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT
from akos.log import setup_logging

logger = logging.getLogger("akos.brand_baseline_reality")

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
    / "canonicals"
)
MATRIX_PATH = CANON_DIR / "BRAND_BASELINE_REALITY_MATRIX.md"

ADVOPS_DIR = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "_assets" / "advops"

DEFAULT_CONSUMER_ROOTS = (REPO_ROOT.parent / "root_cd" / "boilerplate",)

EXEMPT_FILE_SUFFIXES = (".objections.md", ".counterparty-brief.md")

DEFAULT_INTERNAL_TOKENS = (
    "counterparty",
    "elicitation",
    "reliability grading",
    "intelligence collection",
    "intelligence report",
    "approach techniques",
    "baseline reality assessment",
)


@dataclass(frozen=True)
class InternalToken:
    token: str
    pattern: re.Pattern[str]


def _build_token_patterns(tokens: Iterable[str]) -> list[InternalToken]:
    return [
        InternalToken(token=t, pattern=re.compile(rf"\b{re.escape(t)}\b", re.IGNORECASE))
        for t in tokens
    ]


def _extract_internal_tokens_from_matrix(path: Path) -> list[InternalToken]:
    """Best-effort parse of BRAND_BASELINE_REALITY_MATRIX.md §3 for the internal
    token list. Falls back to ``DEFAULT_INTERNAL_TOKENS`` if the section can't
    be located (so the validator never silently weakens)."""
    if not path.exists():
        return _build_token_patterns(DEFAULT_INTERNAL_TOKENS)
    text = path.read_text(encoding="utf-8")

    section = re.search(
        r"^## 3\.\s*Translation rules.*?\n(.*?)(?=^## 4\.|^## 5\.)",
        text,
        re.DOTALL | re.MULTILINE,
    )
    if not section:
        return _build_token_patterns(DEFAULT_INTERNAL_TOKENS)

    extracted: set[str] = set()
    for match in re.finditer(r"^\|\s*Internal[^|]*\|\s*([^|]+)\|", section.group(1), re.MULTILINE):
        cell = match.group(1).strip()
        for raw in re.findall(r"`([^`]+)`", cell):
            tok = raw.strip().strip(",")
            if tok and len(tok) >= 4 and tok.lower() not in {"internal", "external"}:
                extracted.add(tok)

    if not extracted:
        return _build_token_patterns(DEFAULT_INTERNAL_TOKENS)

    merged = sorted(extracted | set(DEFAULT_INTERNAL_TOKENS), key=lambda s: (-len(s), s))
    return _build_token_patterns(merged)


@dataclass
class BaselineHit:
    file: Path
    line: int
    token: InternalToken
    snippet: str


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _is_exempt(path: Path) -> bool:
    name = path.name.lower()
    return any(name.endswith(suf) for suf in EXEMPT_FILE_SUFFIXES)


def _scan_text(path: Path, tokens: list[InternalToken]) -> list[BaselineHit]:
    if _is_exempt(path):
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []

    hits: list[BaselineHit] = []
    for tok in tokens:
        for match in tok.pattern.finditer(text):
            ln = _line_number(text, match.start())
            line_start = text.rfind("\n", 0, match.start()) + 1
            line_end = text.find("\n", match.end())
            if line_end < 0:
                line_end = len(text)
            hits.append(
                BaselineHit(
                    file=path,
                    line=ln,
                    token=tok,
                    snippet=text[line_start:line_end].strip()[:140],
                )
            )
    return hits


def _scan_advops_decks_and_dossiers(tokens: list[InternalToken]) -> list[BaselineHit]:
    if not ADVOPS_DIR.exists():
        return []
    hits: list[BaselineHit] = []
    for pattern in ("**/deck/*.yaml", "**/dossier_*.md", "**/deck_slides.yaml"):
        for path in ADVOPS_DIR.glob(pattern):
            if path.is_file():
                hits.extend(_scan_text(path, tokens))
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
                hits.extend(_scan_text(path, tokens))
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

    tokens = _extract_internal_tokens_from_matrix(MATRIX_PATH)
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
                rel = hit.file.relative_to(REPO_ROOT.parent)
            except ValueError:
                rel = hit.file
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
            len({h.file for h in all_hits}),
        )
        return 1

    logger.info(
        "BRAND_BASELINE_REALITY OK — dual-register contract holds; %d internal token(s) checked",
        len(tokens),
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
