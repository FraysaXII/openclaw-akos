"""Reusable brand-baseline-reality (BBR) scanner per I76 P3 Lane 3 refactor.

Lifts the previously-private scan helpers from
``scripts/validate_brand_baseline_reality_drift.py`` into a real ``akos.*``
module so other surfaces (most importantly the I76 P3 personality-check
runbook ``scripts/madeira_personality_check.py`` that Madeira self-polices
every output through) can call the same scanner without reaching into a
private ``_underscore`` symbol of a sibling script.

Public API:

- :class:`InternalToken` — frozen dataclass pairing a token literal with the
  compiled regex used to find it.
- :class:`BaselineHit` — a single internal-register hit (line + token + snippet
  + optional source ``Path``).
- :data:`DEFAULT_INTERNAL_TOKENS` — fallback token literal list per
  ``BRAND_BASELINE_REALITY_MATRIX.md`` §3 (used when the canonical matrix file
  is unparseable so the validator never silently weakens).
- :func:`load_canonical_tokens` — best-effort parse of the matrix's §3
  translation rules table; falls back to ``DEFAULT_INTERNAL_TOKENS`` on
  parse failure.
- :func:`scan_text` — scan a string for internal-register tokens; returns
  a list of :class:`BaselineHit`. Supports an in-memory `tokens` override,
  a `strip_frontmatter` flag (per D-IH-89-H operator-metadata exemption),
  and an optional `file` argument to populate the hit's ``file`` attribute
  for downstream reporting.

The validator (``scripts/validate_brand_baseline_reality_drift.py``) is
refactored to a thin shim that imports these helpers; its CLI behaviour
(argv + exit codes + log output) is unchanged.

Cross-references: ``BRAND_BASELINE_REALITY_MATRIX.md`` §3,
``BRAND_JARGON_AUDIT.md`` §4.1, ``.cursor/rules/akos-brand-baseline-reality.mdc``.
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from akos.io import REPO_ROOT

LOG = logging.getLogger("akos.brand_baseline_reality")


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
"""The active brand canonicals directory (per BRAND_VISION canonicals housing)."""

MATRIX_PATH: Path = CANON_DIR / "BRAND_BASELINE_REALITY_MATRIX.md"
"""Default path to the canonical translation-rules matrix."""


DEFAULT_INTERNAL_TOKENS: tuple[str, ...] = (
    "counterparty",
    "elicitation",
    "reliability grading",
    "intelligence collection",
    "intelligence report",
    "approach techniques",
    "baseline reality assessment",
    "PRJ-HOL-",
)
"""Fallback internal-register token list used when the canonical matrix is
unparseable. Mirrors BRAND_BASELINE_REALITY_MATRIX.md §3 row keys + the
PRJ-HOL- engagement-id prefix per D-IH-89-E."""


_FRONTMATTER_RE = re.compile(r"^---\s*\n.*?\n---\s*\n", re.DOTALL)


@dataclass(frozen=True)
class InternalToken:
    """One internal-register token plus its case-insensitive word-boundary regex."""

    token: str
    pattern: re.Pattern[str]


@dataclass
class BaselineHit:
    """One occurrence of an internal-register token in scanned text.

    ``file`` is ``None`` for in-memory scans (e.g. when Madeira's personality
    runbook scans a draft that has not yet been written to disk); the
    validator populates it from the path under scan.
    """

    line: int
    token: InternalToken
    snippet: str
    file: Path | None = field(default=None)


def _build_token_patterns(tokens: Iterable[str]) -> list[InternalToken]:
    """Compile each token literal into a case-insensitive word-boundary regex."""
    return [
        InternalToken(token=t, pattern=re.compile(rf"\b{re.escape(t)}\b", re.IGNORECASE))
        for t in tokens
    ]


def _extract_internal_tokens_from_matrix(path: Path) -> list[InternalToken]:
    """Best-effort parse of BRAND_BASELINE_REALITY_MATRIX.md §3 internal column.

    Falls back to ``DEFAULT_INTERNAL_TOKENS`` if the section can't be located,
    which keeps the validator from silently weakening when the matrix is
    rewritten in a way the regex doesn't recognise.
    """
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
    for match in re.finditer(
        r"^\|\s*Internal[^|]*\|\s*([^|]+)\|", section.group(1), re.MULTILINE
    ):
        cell = match.group(1).strip()
        for raw in re.findall(r"`([^`]+)`", cell):
            tok = raw.strip().strip(",")
            if tok and len(tok) >= 4 and tok.lower() not in {"internal", "external"}:
                extracted.add(tok)

    if not extracted:
        return _build_token_patterns(DEFAULT_INTERNAL_TOKENS)

    merged = sorted(extracted | set(DEFAULT_INTERNAL_TOKENS), key=lambda s: (-len(s), s))
    return _build_token_patterns(merged)


def load_canonical_tokens(matrix_path: Path | None = None) -> list[InternalToken]:
    """Public API: load the internal-register token list from canon.

    When ``matrix_path`` is omitted, uses ``MATRIX_PATH``. Returns the
    fallback ``DEFAULT_INTERNAL_TOKENS`` list if the matrix is missing or
    its §3 table is unparseable.
    """
    return _extract_internal_tokens_from_matrix(matrix_path or MATRIX_PATH)


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _strip_frontmatter_for_scan(text: str) -> str:
    """Replace the YAML frontmatter region with whitespace before scanning.

    Frontmatter is operator metadata (``program_id``, ``plane``, ``sources``,
    ``role_owner``, etc.) -- never rendered to the external reader. Per
    ``D-IH-89-H`` (2026-05-18) operator metadata may carry internal tokens
    (e.g. ``program_id: PRJ-HOL-FOUNDING-2026``) without violating BBR; only
    the body prose that ships to advisers / regulators must hold the
    external register.

    Replaces the frontmatter span with whitespace (rather than removing) so
    line numbers in error reports still match the original file.
    """
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return text
    span = match.group(0)
    blanked = re.sub(r"[^\n]", " ", span)
    return blanked + text[len(span):]


def scan_text(
    text: str,
    *,
    tokens: list[InternalToken] | None = None,
    strip_frontmatter: bool = False,
    file: Path | None = None,
) -> list[BaselineHit]:
    """Scan ``text`` for internal-register tokens and return per-line hits.

    Args:
        text: The body to scan.
        tokens: Optional override token list; when ``None`` the canonical
            matrix is parsed (with fallback to ``DEFAULT_INTERNAL_TOKENS``).
            Pass a custom list to scan against a non-canonical token set
            (e.g. for testing).
        strip_frontmatter: When True and the text starts with a YAML
            frontmatter block, that span is blanked (line numbers preserved)
            before scanning. Set to True for markdown-shaped surfaces.
        file: Optional source ``Path`` to populate on each emitted hit; the
            scanner does not read the path -- the caller passes the text
            directly. When ``None``, hits emit with ``file=None`` (the
            in-memory call shape used by ``scripts/madeira_personality_check.py``).
    """
    token_list = tokens if tokens is not None else load_canonical_tokens()
    body = _strip_frontmatter_for_scan(text) if strip_frontmatter else text

    hits: list[BaselineHit] = []
    for tok in token_list:
        for match in tok.pattern.finditer(body):
            ln = _line_number(body, match.start())
            line_start = body.rfind("\n", 0, match.start()) + 1
            line_end = body.find("\n", match.end())
            if line_end < 0:
                line_end = len(body)
            hits.append(
                BaselineHit(
                    line=ln,
                    token=tok,
                    snippet=body[line_start:line_end].strip()[:140],
                    file=file,
                )
            )
    return hits


__all__ = [
    "BaselineHit",
    "CANON_DIR",
    "DEFAULT_INTERNAL_TOKENS",
    "InternalToken",
    "MATRIX_PATH",
    "load_canonical_tokens",
    "scan_text",
]
