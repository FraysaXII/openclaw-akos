#!/usr/bin/env python3
"""Validate brand-jargon discipline on external public surfaces (I66 P2 / D-IH-66-J).

Reads the canonical forbidden-token registry from
``BRAND_JARGON_AUDIT.md`` §4.1 + ``BRAND_ABBREVIATIONS.md`` §2 and asserts that
no public-rendered DOM in sibling consumer repos contains those tokens. Token
list is parsed from canonical at run time, so the validator does **not** drift
from canon: edit the canonical and re-run.

Scope (per BRAND_JARGON_AUDIT.md §3 IN-scope rows):

- ``boilerplate/`` — public marketing site (``app/``, ``components/``,
  ``messages/`` — rendered DOM).
- ``hlk-erp/`` — operator surface; **public-route subset only**: only
  ``app/(public)/**``. Operator-only routes
  (``app/(operator)/**``, ``app/(authapp)/**``) are internal-register;
  internal short-forms allowed there per BRAND_ABBREVIATIONS §2.1.

Skipped (per BRAND_JARGON_AUDIT.md §3 OUT-of-scope rows):

- Internal SOPs + ``docs/`` + ``akos/`` + ``scripts/`` (AKOS itself: jargon allowed).
- Code comments, commit messages, PR bodies, CI workflows.
- Sibling repos that are absent (graceful skip).

Usage::

    py scripts/validate_brand_jargon.py
    py scripts/validate_brand_jargon.py --json-log
    py scripts/validate_brand_jargon.py --consumer-root C:/path/to/sibling

Exit codes::

    0 — no drift detected (or all consumer repos absent → graceful skip).
    1 — at least one forbidden token found in scanned surfaces.

Cross-references: BRAND_JARGON_AUDIT.md §4, BRAND_ABBREVIATIONS.md §2,
BRAND_BASELINE_REALITY_MATRIX.md §3 (internal-register tokens), I66 P2
master-roadmap §"P2 — Drift gates and rules".
"""

from __future__ import annotations

import argparse
import logging
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT
from akos.log import setup_logging

logger = logging.getLogger("akos.brand_jargon")

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
JARGON_AUDIT_PATH = CANON_DIR / "BRAND_JARGON_AUDIT.md"
ABBREVIATIONS_PATH = CANON_DIR / "BRAND_ABBREVIATIONS.md"

DEFAULT_CONSUMER_ROOTS = (
    REPO_ROOT.parent / "root_cd" / "boilerplate",
    REPO_ROOT.parent / "root_cd" / "hlk-erp",
)

SCANNED_SUBPATHS_BY_REPO = {
    "boilerplate": ("app", "components", "messages", "i18n/messages"),
    "hlk-erp": ("app/(public)",),
}

SCANNABLE_SUFFIXES = {".tsx", ".ts", ".jsx", ".js", ".mdx", ".md", ".json", ".html", ".css"}

EXCLUDED_DIRS = {"node_modules", ".next", ".turbo", "dist", "build", ".git", ".vercel"}

EXCLUDED_PATH_FRAGMENTS_BY_REPO = {
    "boilerplate": ("app/dashboard", "app/(authapp)", "app\\dashboard", "app\\(authapp)"),
    "hlk-erp": (),
}

CODE_LINE_PREFIXES = (
    "import ",
    "import{",
    "export {",
    "export *",
    "export type",
    "from \"",
    "from '",
    "require(",
    "@import ",
)


@dataclass(frozen=True)
class ForbiddenToken:
    """A single forbidden token with its canonical source row + context category."""

    token: str
    pattern: re.Pattern[str]
    category: str
    canonical_source: str


def _strip_md_inline(text: str) -> str:
    """Strip backticks + minimal markdown so token strings are comparable."""
    return text.replace("`", "").strip()


CANONICAL_ALLOWLIST = frozenset(
    s.lower()
    for s in (
        "Holistika",
        "Holistika R&S",
        "HLK Tech Lab",
        "Think Big",
        "MADEIRA",
        "MADEIRA Agent",
        "KiRBe",
        "ENVOY",
        "InfraMonitor",
        "Financial Analyst",
        "Holistika Research SL",
        "BRAND_ABBREVIATIONS.md",
        "BRAND_BASELINE_REALITY_MATRIX.md",
        "BRAND_ARCHITECTURE.md",
        "BRAND_JARGON_AUDIT.md",
    )
)

PLACEHOLDER_TOKENS = frozenset(
    {
        "…",
        "<anything>",
        "*",
        "<register>.csv",
        "topic_<anything>",
    }
)


def _extract_tokens_from_jargon_audit(path: Path) -> list[ForbiddenToken]:
    """Parse BRAND_JARGON_AUDIT.md §4.1 / §4.2 for forbidden tokens.

    Only **first-of-bullet** backticked tokens are treated as forbidden — i.e.
    text matching ``^- `<TOKEN>` —`` (or with multiple comma-separated tokens
    before the dash). Tokens that appear inline later in a bullet's prose
    (often as canonical *replacements* or cross-references) are intentionally
    ignored. ``CANONICAL_ALLOWLIST`` further filters out tokens that are valid
    brand entities.
    """
    if not path.exists():
        raise FileNotFoundError(f"BRAND_JARGON_AUDIT.md not found at {path}")
    text = path.read_text(encoding="utf-8")

    tokens: list[ForbiddenToken] = []

    def _build_pattern(tok: str) -> re.Pattern[str]:
        if tok.endswith("-"):
            return re.compile(rf"\b{re.escape(tok)}\w+", re.IGNORECASE)
        if tok == "HLK":
            return re.compile(r"\bHLK\b(?!\s+Tech\s+Lab)")
        if "*" in tok:
            wild = re.escape(tok).replace(r"\*", r"\w*")
            return re.compile(rf"\b{wild}\b", re.IGNORECASE)
        return re.compile(rf"\b{re.escape(tok)}\b", re.IGNORECASE)

    def _harvest_section(section_re: str, category: str, canonical_source: str) -> None:
        section_match = re.search(section_re, text, re.DOTALL | re.MULTILINE)
        if not section_match:
            return
        body = section_match.group(1)
        bullet_re = re.compile(r"^\s*-\s+(?P<bullet>.+?)$", re.MULTILINE)
        em_dash_split = re.compile(r"\s+[—–]\s+")
        seen_tokens: set[str] = set()
        for match in bullet_re.finditer(body):
            bullet_text = match.group("bullet")
            if "`" not in bullet_text:
                continue
            head = em_dash_split.split(bullet_text, maxsplit=1)[0]
            for raw in re.findall(r"`([^`\n]+?)`", head):
                tok = _strip_md_inline(raw)
                if not tok or tok in PLACEHOLDER_TOKENS:
                    continue
                if tok.lower() in CANONICAL_ALLOWLIST:
                    continue
                if len(tok) < 2:
                    continue
                if tok in seen_tokens:
                    continue
                seen_tokens.add(tok)
                tokens.append(
                    ForbiddenToken(
                        token=tok,
                        pattern=_build_pattern(tok),
                        category=category,
                        canonical_source=canonical_source,
                    )
                )

    _harvest_section(
        r"^### 4\.1 .*?\n(.*?)(?=^### 4\.|^## 5\.|^## 8\.)",
        "codename",
        "BRAND_JARGON_AUDIT.md §4.1",
    )
    _harvest_section(
        r"^### 4\.2 .*?\n(.*?)(?=^### 4\.|^## 5\.|^## 8\.)",
        "stack_jargon",
        "BRAND_JARGON_AUDIT.md §4.2",
    )

    return tokens


def _extract_tokens_from_abbreviations(path: Path) -> list[ForbiddenToken]:
    """Parse BRAND_ABBREVIATIONS.md for short-forms forbidden in external prose.

    Conservatively returns only the standalone short-forms that were marked
    "Forbidden in all contexts" in §2.2-§2.6. ``HLK`` itself is covered by the
    ``BRAND_JARGON_AUDIT`` extractor (which knows the ``HLK Tech Lab`` exception).
    Single-letter / 2-letter forms like ``H``, ``MA``, ``KB``, ``EV``, ``TB``,
    ``TL``, ``HRS`` are too noisy to gate broadly; we limit them to JSON
    locale message files where they would be unambiguously brand-namespaced.
    """
    if not path.exists():
        return []
    forbidden: list[ForbiddenToken] = []
    for short_form in ("MA", "KB", "EV", "TB", "TL", "HRS"):
        forbidden.append(
            ForbiddenToken(
                token=short_form,
                pattern=re.compile(rf"\b{re.escape(short_form)}\b"),
                category="abbreviation_locale_only",
                canonical_source="BRAND_ABBREVIATIONS.md §2",
            )
        )
    return forbidden


def _is_inside_excluded_dir(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    return any(part in EXCLUDED_DIRS for part in rel.parts)


def _is_inside_repo_excluded_path(path: Path, root: Path, repo_name: str) -> bool:
    fragments = EXCLUDED_PATH_FRAGMENTS_BY_REPO.get(repo_name, ())
    if not fragments:
        return False
    rel_str = str(path.relative_to(root))
    return any(frag in rel_str for frag in fragments)


def _file_is_scannable(path: Path) -> bool:
    return path.suffix.lower() in SCANNABLE_SUFFIXES


def _walk_subpath(root: Path, subpath: str, repo_name: str) -> Iterable[Path]:
    base = root / subpath
    if not base.exists():
        return ()
    return (
        p
        for p in base.rglob("*")
        if p.is_file()
        and _file_is_scannable(p)
        and not _is_inside_excluded_dir(p, root)
        and not _is_inside_repo_excluded_path(p, root, repo_name)
    )


def _is_code_only_line(line: str, suffix: str) -> bool:
    """Return True for lines that are TypeScript/JS imports / exports / comments
    — code, not rendered DOM. We do this so library identifiers like
    ``next-intl`` or ``shadcn`` (which are forbidden in *prose* per
    BRAND_JARGON_AUDIT.md §4.2, but **must** appear as module specifiers in
    source) don't false-positive, and so that ``// Basic rate limiting (use
    Redis ...)`` developer comments don't fail the gate either.
    """
    if suffix.lower() not in {".tsx", ".ts", ".jsx", ".js"}:
        return False
    stripped = line.lstrip()
    if stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*"):
        return True
    return any(stripped.startswith(prefix) for prefix in CODE_LINE_PREFIXES)


@dataclass
class JargonHit:
    file: Path
    line: int
    column: int
    token: ForbiddenToken
    snippet: str


def _line_and_column(text: str, offset: int) -> tuple[int, int]:
    line = text.count("\n", 0, offset) + 1
    last_nl = text.rfind("\n", 0, offset)
    col = offset - (last_nl + 1) + 1
    return line, col


def _scan_file(path: Path, tokens: list[ForbiddenToken]) -> list[JargonHit]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []

    hits: list[JargonHit] = []
    is_locale_json = path.suffix.lower() == ".json" and "messages" in path.parts
    suffix = path.suffix

    for tok in tokens:
        if tok.category == "abbreviation_locale_only" and not is_locale_json:
            continue
        for match in tok.pattern.finditer(text):
            ln, col = _line_and_column(text, match.start())
            line_start = text.rfind("\n", 0, match.start()) + 1
            line_end = text.find("\n", match.end())
            if line_end < 0:
                line_end = len(text)
            line_text = text[line_start:line_end]
            if _is_code_only_line(line_text, suffix):
                continue
            snippet = line_text.strip()[:140]
            hits.append(JargonHit(file=path, line=ln, column=col, token=tok, snippet=snippet))
    return hits


def _resolve_consumer_roots(extra_roots: list[Path]) -> list[tuple[str, Path]]:
    candidates: list[tuple[str, Path]] = []
    seen: set[Path] = set()
    for root in (*extra_roots, *DEFAULT_CONSUMER_ROOTS):
        if not root.exists():
            continue
        resolved = root.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        candidates.append((root.name, resolved))
    return candidates


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate brand-jargon discipline (I66 P2)")
    parser.add_argument("--json-log", action="store_true", help="JSON logging output")
    parser.add_argument(
        "--consumer-root",
        action="append",
        default=[],
        help="Extra consumer-repo root to scan (repeatable)",
    )
    parser.add_argument(
        "--strict-empty",
        action="store_true",
        help="Fail (exit 1) if no consumer repos are found instead of skipping gracefully",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)
    setup_logging(json_output=args.json_log)

    try:
        tokens = _extract_tokens_from_jargon_audit(JARGON_AUDIT_PATH)
    except FileNotFoundError as exc:
        logger.error("%s", exc)
        return 1
    tokens.extend(_extract_tokens_from_abbreviations(ABBREVIATIONS_PATH))

    if not tokens:
        logger.error(
            "No forbidden tokens parsed from canonical (BRAND_JARGON_AUDIT.md / "
            "BRAND_ABBREVIATIONS.md). Refusing to PASS — canonical may be malformed."
        )
        return 1

    extra_roots = [Path(p) for p in args.consumer_root]
    consumer_roots = _resolve_consumer_roots(extra_roots)

    if not consumer_roots:
        msg = (
            "No consumer repos found at default sibling paths "
            f"({', '.join(str(p) for p in DEFAULT_CONSUMER_ROOTS)}). "
            "Skipping brand-jargon scan."
        )
        if args.strict_empty:
            logger.error("%s", msg)
            return 1
        logger.info("%s", msg)
        return 0

    all_hits: list[JargonHit] = []
    files_scanned = 0
    for repo_name, repo_root in consumer_roots:
        subpaths = SCANNED_SUBPATHS_BY_REPO.get(repo_name, ("app", "components"))
        logger.info(
            "Scanning %s (%s) for %d forbidden tokens ...",
            repo_name,
            ", ".join(subpaths),
            len(tokens),
        )
        for subpath in subpaths:
            for path in _walk_subpath(repo_root, subpath, repo_name):
                files_scanned += 1
                all_hits.extend(_scan_file(path, tokens))

    if all_hits:
        for hit in all_hits[:200]:
            try:
                rel = hit.file.relative_to(REPO_ROOT.parent)
            except ValueError:
                rel = hit.file
            logger.error(
                "%s:%d:%d  [%s] %r — %s (canonical: %s)",
                rel,
                hit.line,
                hit.column,
                hit.token.category,
                hit.token.token,
                hit.snippet,
                hit.token.canonical_source,
            )
        if len(all_hits) > 200:
            logger.error("... and %d more hits suppressed", len(all_hits) - 200)
        logger.error(
            "BRAND_JARGON_AUDIT: %d forbidden token(s) across %d file(s)",
            len(all_hits),
            len({h.file for h in all_hits}),
        )
        return 1

    logger.info(
        "BRAND_JARGON_AUDIT OK — %d files scanned across %d consumer repo(s); "
        "0 forbidden tokens",
        files_scanned,
        len(consumer_roots),
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
