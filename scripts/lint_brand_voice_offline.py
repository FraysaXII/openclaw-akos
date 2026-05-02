#!/usr/bin/env python3
"""Initiative 49 P12 — offline brand-voice fast-lint.

Pure regex / token-list scan for forbidden tokens defined in
``docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_JARGON_AUDIT.md``
section 4 (internal codenames, stack jargon, methodology shorthand,
operator-side process tokens). Designed to run in seconds during pre_commit
when LLM-judge cost is undesirable.

Scope: external-facing artefacts only — public README sections, deployed web
pages, deck slides, generated dossiers, cover emails. Internal SOPs,
implementation notes, code comments are intentionally out of scope.

Usage::

    py scripts/lint_brand_voice_offline.py <path> [<path> ...]
    py scripts/lint_brand_voice_offline.py --scan-defaults

Exit codes:
- ``0`` no violations
- ``1`` violations found (printed line-by-line)
- ``2`` invocation error
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

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.log import setup_logging

logger = logging.getLogger("scripts.lint_brand_voice_offline")


# §4.1 internal codenames — exact-token bans (case-insensitive on word boundary).
INTERNAL_CODENAMES: tuple[str, ...] = (
    r"\bAKOS\b",
    r"\btopic_[A-Za-z0-9_]+",
    r"\bplane\b",
    r"\bADVOPS\b",
    r"\bTECHOPS\b",
    r"\bFINOPS\b",
    r"\bMKTOPS\b",
    r"\bGOI\b",
    r"\bPOI\b",
    r"\bref_id\b",
    r"\bGOI-[A-Z0-9]+",
    r"\bPOI-[A-Z0-9]+",
    r"\bprogram_id\b",
    r"\bPRJ-HOL-[A-Z0-9-]+",
    r"\brepo_slug\b",
    r"\bholistika_ops\.[A-Za-z0-9_]+",
    r"\bkirbe\.[A-Za-z0-9_]+",
    r"\bcompliance\.[A-Za-z0-9_]+",
    r"\bprocess_list\.csv\b",
    r"\bbaseline_organisation\.csv\b",
)

# §4.2 stack / framework jargon (case-sensitive when capitalised).
STACK_JARGON: tuple[str, ...] = (
    r"\bRBAC\b",
    r"\bRLS\b",
    r"\bpgvector\b",
    r"\bRRF\b",
    r"\bCohere reranking\b",
    r"\bLogfire\b",
    r"\bBullMQ\b",
    r"\bRedis\b",
    r"\bMux\b",
    r"\bCloudflare R2\b",
    r"\bJWT\b",
    r"\bOAuth2\b",
    r"\bnext-intl\b",
    r"\bPydantic\b",
    r"\bshadcn\b",
    r"\bPolaris\b",
    r"\bLiquid\b",
    r"\bMermaid\b",
    r"\bWeasyPrint\b",
    r"\bpandoc\b",
    r"\bmmdc\b",
)

# §4.3 methodology shorthand.
METHODOLOGY_SHORTHAND: tuple[str, ...] = (
    r"\b4-layer methodology\b",
    r"\bAKOS Strict\b",
    r"\bStrict mode\b",
    r"\bTopic-Fact-Source\b",
    r"\bderived view\b",
)

# §4.4 operator-side process tokens — must never reach rendered output.
OPERATOR_TOKENS: tuple[str, ...] = (
    r"TODO\[OPERATOR(?:[-A-Za-z0-9]*)\]",
    r"\[OPERATOR\]",
    r"<OPERATOR_CONFIRM>",
    r"\{:\s*\.callout-operator\s*\}",
)

CATEGORY_PATTERNS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("internal_codename_§4.1", INTERNAL_CODENAMES),
    ("stack_jargon_§4.2", STACK_JARGON),
    ("methodology_shorthand_§4.3", METHODOLOGY_SHORTHAND),
    ("operator_token_§4.4", OPERATOR_TOKENS),
)


@dataclass(frozen=True)
class Violation:
    path: Path
    line_number: int
    category: str
    pattern: str
    snippet: str

    def to_line(self) -> str:
        return f"{self.path}:{self.line_number}: [{self.category}] {self.pattern} -> {self.snippet}"


def _compile() -> list[tuple[str, str, re.Pattern[str]]]:
    out: list[tuple[str, str, re.Pattern[str]]] = []
    for category, patterns in CATEGORY_PATTERNS:
        for pat in patterns:
            out.append((category, pat, re.compile(pat)))
    return out


def _frontmatter_end_line(lines: list[str]) -> int:
    """Return 1-based line number where YAML frontmatter ends; 0 if no frontmatter.

    Per BRAND_JARGON_AUDIT §4 the forbidden tokens MAY appear inside
    machine-readable provenance metadata (frontmatter / footer source lines);
    we skip frontmatter blocks while scanning external prose.
    """
    if not lines or lines[0].strip() != "---":
        return 0
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return idx + 1
    return 0


_BACKTICK_RE = re.compile(r"`[^`]*`")
_YAML_PATH_FIELD_RE = re.compile(r"^\s*[A-Za-z0-9_]+_source\s*:\s*", re.IGNORECASE)
_YAML_COMMENT_RE = re.compile(r"^\s*#")
_HTML_COMMENT_RE = re.compile(r"^\s*<!--")


def _strip_backticks(line: str) -> str:
    """Remove inline backtick-wrapped substrings; per BRAND_JARGON_AUDIT §4 the
    forbidden tokens MAY appear inside code references / paths quoted by an
    operator. The lint targets external-prose leakage, not quoted code paths.
    """
    return _BACKTICK_RE.sub(" ", line)


def lint_text(text: str, path: Path, *, compiled=None, skip_frontmatter: bool = True) -> list[Violation]:
    compiled = compiled or _compile()
    lines = text.splitlines()
    fm_end = _frontmatter_end_line(lines) if skip_frontmatter else 0
    violations: list[Violation] = []
    for ln, line in enumerate(lines, start=1):
        if ln <= fm_end:
            continue
        stripped = line.rstrip()
        if _YAML_COMMENT_RE.match(stripped) or _HTML_COMMENT_RE.match(stripped):
            continue
        if _YAML_PATH_FIELD_RE.match(stripped):
            continue
        scan_target = _strip_backticks(stripped)
        for category, pat, regex in compiled:
            for match in regex.finditer(scan_target):
                violations.append(Violation(
                    path=path,
                    line_number=ln,
                    category=category,
                    pattern=pat,
                    snippet=stripped[max(0, match.start() - 20): match.end() + 20].strip(),
                ))
    return violations


def lint_file(path: Path, *, compiled=None) -> list[Violation]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        logger.warning("could not read %s: %s", path, exc)
        return []
    return lint_text(text, path, compiled=compiled)


def lint_paths(paths: Iterable[Path]) -> list[Violation]:
    compiled = _compile()
    out: list[Violation] = []
    for path in paths:
        if path.is_dir():
            for sub in path.rglob("*.md"):
                out.extend(lint_file(sub, compiled=compiled))
        elif path.is_file():
            out.extend(lint_file(path, compiled=compiled))
    return out


def default_targets() -> list[Path]:
    """External-facing artefacts only — see BRAND_JARGON_AUDIT §3 scope table.

    README.md, internal SOPs, and ``static/madeira_control.html`` are explicitly
    out of scope (internal architecture docs / runbooks per §3). Defaults only
    scan deck story body + deck slides body (frontmatter skipped automatically).
    """
    candidates = [
        REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "_assets" / "advops" / "PRJ-HOL-FOUNDING-2026" / "enisa_company_dossier" / "deck_story_es.md",
        REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "_assets" / "advops" / "PRJ-HOL-FOUNDING-2026" / "enisa_company_dossier" / "deck_slides.yaml",
    ]
    return [p for p in candidates if p.exists()]


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("paths", nargs="*", type=Path,
                    help="Files or directories to lint (default uses --scan-defaults)")
    ap.add_argument("--scan-defaults", action="store_true",
                    help="Lint default external-facing artefacts (README, control plane HTML, deck story/slides)")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--json", action="store_true",
                    help="Emit JSON list of violations on stdout instead of printable lines")
    return ap.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    setup_logging(json_output=False)
    targets: list[Path] = list(args.paths or [])
    if args.scan_defaults or not targets:
        targets.extend(default_targets())
    if not targets:
        sys.stderr.write("FAIL: no paths given and --scan-defaults found nothing\n")
        return 2

    violations = lint_paths(targets)
    if args.json:
        import json as _json
        payload = [
            {"path": str(v.path), "line": v.line_number, "category": v.category,
             "pattern": v.pattern, "snippet": v.snippet}
            for v in violations
        ]
        sys.stdout.write(_json.dumps({"violation_count": len(violations), "violations": payload},
                                     indent=2, sort_keys=True))
        sys.stdout.write("\n")
        return 0 if not violations else 1

    if violations:
        if not args.quiet:
            sys.stderr.write(
                f"  brand voice fast-lint: {len(violations)} violation(s)\n"
                f"  ============================================\n"
            )
        for v in violations:
            sys.stderr.write(v.to_line() + "\n")
        if not args.quiet:
            sys.stderr.write(
                "  Reference: BRAND_JARGON_AUDIT.md §4 (forbidden tokens for external prose).\n"
            )
        return 1

    if not args.quiet:
        sys.stdout.write(
            f"  brand voice fast-lint: PASS\n"
            f"  ============================\n"
            f"  files scanned (incl. md tree): {len(targets)}\n"
            f"  no §4 forbidden tokens found.\n"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
