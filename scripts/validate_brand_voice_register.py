#!/usr/bin/env python3
"""Validate per-locale voice register on consumer i18n message files (I66 P2 / D-IH-66-J).

Reads forbidden patterns from ``BRAND_FRENCH_PATTERNS.md`` §5
(anglicisms + performative-French) and ``BRAND_SPANISH_PATTERNS.md``
§13 + §"Patterns to refuse" (anglicism stuffing + performative-Spanish +
vague-time language). Asserts that no per-locale i18n message file
(``boilerplate/messages/{en,es,fr}.json`` and any ``hlk-erp/messages/*``
mirror) contains those patterns.

This is a **register validator** distinct from ``validate_brand_jargon.py``:

- ``validate_brand_jargon.py`` is locale-agnostic and forbids internal
  codenames + stack jargon + abbreviations from rendered DOM (any locale).
- ``validate_brand_voice_register.py`` is **locale-aware** and forbids
  patterns that read native-speaker-bad in a given locale (FR anglicisms,
  ES performative humility, etc.).

Skipped (graceful) when consumer repos are absent. Token lists are parsed
from canonical at run time so the validator does not drift.

Usage::

    py scripts/validate_brand_voice_register.py
    py scripts/validate_brand_voice_register.py --json-log
    py scripts/validate_brand_voice_register.py --consumer-root C:/path/to/sibling

Exit codes::

    0 — no register drift, or no consumer repos present (graceful skip).
    1 — at least one forbidden pattern found in a per-locale message file.

Cross-references: BRAND_FRENCH_PATTERNS.md §5, BRAND_SPANISH_PATTERNS.md §13,
BRAND_VOICE_FOUNDATION.md, I66 P2 master-roadmap.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT
from akos.log import setup_logging

logger = logging.getLogger("akos.brand_voice_register")

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
FRENCH_PATTERNS_PATH = CANON_DIR / "BRAND_FRENCH_PATTERNS.md"
SPANISH_PATTERNS_PATH = CANON_DIR / "BRAND_SPANISH_PATTERNS.md"

DEFAULT_CONSUMER_ROOTS = (
    REPO_ROOT.parent / "root_cd" / "boilerplate",
    REPO_ROOT.parent / "root_cd" / "hlk-erp",
)

MESSAGE_RELATIVE_PATHS = ("messages", "i18n/messages")


@dataclass(frozen=True)
class RegisterRule:
    locale: str
    token: str
    pattern: re.Pattern[str]
    rationale: str
    canonical_source: str


def _extract_french_anglicisms(path: Path) -> list[RegisterRule]:
    """Parse the §5.1 anglicism table from BRAND_FRENCH_PATTERNS.md.

    Table format::

        | `de-risquer` | `réduire le risque` |

    We extract the left column (anglicism) and build a word-boundary regex.
    """
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")

    rules: list[RegisterRule] = []
    section = re.search(
        r"### 5\.1 Anglicisms.*?\n(.*?)(?=^### 5\.|^## 6\.)",
        text,
        re.DOTALL | re.MULTILINE,
    )
    if not section:
        return rules

    for row_match in re.finditer(
        r"^\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|", section.group(1), re.MULTILINE
    ):
        anglicism = row_match.group(1).strip()
        replacement = row_match.group(2).strip()
        if not anglicism:
            continue
        rules.append(
            RegisterRule(
                locale="fr",
                token=anglicism,
                pattern=re.compile(rf"\b{re.escape(anglicism)}\b", re.IGNORECASE),
                rationale=f"FR anglicism — replace with '{replacement}'",
                canonical_source="BRAND_FRENCH_PATTERNS.md §5.1",
            )
        )
    return rules


def _french_performative_patterns(path: Path) -> list[RegisterRule]:
    """A small allow-list of FR performative-language tokens to forbid in messages.

    We do not parse the §5.2 free-form prose — building patterns from prose is
    too fragile. Instead we hard-code high-confidence performative tokens that
    BRAND_FRENCH_PATTERNS.md §5.2 explicitly names. The canonical source is
    cited so an operator-driven update flow keeps both in sync.
    """
    if not path.exists():
        return []
    return [
        RegisterRule(
            locale="fr",
            token=token,
            pattern=re.compile(rf"\b{re.escape(token)}\b", re.IGNORECASE),
            rationale="FR performative — see BRAND_FRENCH_PATTERNS.md §5.2",
            canonical_source="BRAND_FRENCH_PATTERNS.md §5.2",
        )
        for token in (
            "Je serais honoré",
            "infiniment pour le temps",
            "Je me permets de me tourner",
            "dans les meilleurs délais",
        )
    ]


def _spanish_register_rules(path: Path) -> list[RegisterRule]:
    """Hand-curated forbidden patterns for ES locale per BRAND_SPANISH_PATTERNS.md.

    The §13 "Boilerplate ES copy alignment" section explicitly lists tokens
    the validator must flag. We materialize them as compiled regexes here.
    """
    if not path.exists():
        return []
    return [
        RegisterRule(
            locale="es",
            token=token,
            pattern=pattern,
            rationale=rationale,
            canonical_source="BRAND_SPANISH_PATTERNS.md §13",
        )
        for token, pattern, rationale in (
            (
                "humildemente",
                re.compile(r"\bhumildemente\b", re.IGNORECASE),
                "ES performative humility",
            ),
            (
                "seríamos honrados",
                re.compile(r"\bser[ií]amos\s+honrados\b", re.IGNORECASE),
                "ES performative humility",
            ),
            (
                "a la mayor brevedad posible",
                re.compile(r"\ba\s+la\s+mayor\s+brevedad\s+posible\b", re.IGNORECASE),
                "ES vague-time language",
            ),
            (
                "Estimados Sres.",
                re.compile(r"\bEstimados\s+Sres\.?", re.IGNORECASE),
                "ES bureaucratic over-formal in marketing copy",
            ),
            (
                "pricing",
                re.compile(r"\bpricing\b", re.IGNORECASE),
                "ES anglicism — use 'precio' or 'tarifa'",
            ),
            (
                "engagement",
                re.compile(r"\bengagement\b", re.IGNORECASE),
                "ES anglicism — use 'mision' (consulting) or 'interaccion' (marketing)",
            ),
            (
                "mindset",
                re.compile(r"\bmindset\b", re.IGNORECASE),
                "ES anglicism — use 'mentalidad' or 'enfoque'",
            ),
            (
                "growth",
                re.compile(r"\bgrowth\b", re.IGNORECASE),
                "ES anglicism — use 'crecimiento'",
            ),
            (
                "framework",
                re.compile(r"\bframework\b", re.IGNORECASE),
                "ES anglicism — use 'marco metodologico' or 'marco'",
            ),
        )
    ]


def _load_rules() -> list[RegisterRule]:
    return [
        *_extract_french_anglicisms(FRENCH_PATTERNS_PATH),
        *_french_performative_patterns(FRENCH_PATTERNS_PATH),
        *_spanish_register_rules(SPANISH_PATTERNS_PATH),
    ]


@dataclass
class RegisterHit:
    file: Path
    locale: str
    json_path: str
    rule: RegisterRule
    snippet: str


def _walk_json_keys(value: object, path_parts: list[str]) -> Iterable[tuple[str, str]]:
    """Yield (json-pointer-like-path, string-value) for every leaf string."""
    if isinstance(value, dict):
        for k, v in value.items():
            yield from _walk_json_keys(v, [*path_parts, str(k)])
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from _walk_json_keys(v, [*path_parts, str(i)])
    elif isinstance(value, str):
        yield (".".join(path_parts), value)


def _file_locale(path: Path) -> str | None:
    stem = path.stem.lower()
    if stem in {"en", "es", "fr", "en-us", "es-es", "fr-fr"}:
        return stem.split("-", 1)[0]
    return None


def _scan_message_file(path: Path, rules: list[RegisterRule]) -> list[RegisterHit]:
    locale = _file_locale(path)
    if locale is None:
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning("Skipping unreadable message file %s: %s", path, exc)
        return []

    relevant_rules = [r for r in rules if r.locale == locale]
    if not relevant_rules:
        return []

    hits: list[RegisterHit] = []
    for json_path, leaf in _walk_json_keys(data, []):
        for rule in relevant_rules:
            if rule.pattern.search(leaf):
                hits.append(
                    RegisterHit(
                        file=path,
                        locale=locale,
                        json_path=json_path,
                        rule=rule,
                        snippet=leaf[:140],
                    )
                )
    return hits


def _resolve_consumer_roots(extra: list[Path]) -> list[tuple[str, Path]]:
    out: list[tuple[str, Path]] = []
    seen: set[Path] = set()
    for root in (*extra, *DEFAULT_CONSUMER_ROOTS):
        if not root.exists():
            continue
        resolved = root.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        out.append((root.name, resolved))
    return out


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate per-locale voice register (I66 P2)")
    parser.add_argument("--json-log", action="store_true")
    parser.add_argument(
        "--consumer-root",
        action="append",
        default=[],
        help="Extra consumer-repo root to scan (repeatable)",
    )
    parser.add_argument("--strict-empty", action="store_true")
    args = parser.parse_args(list(argv) if argv is not None else None)
    setup_logging(json_output=args.json_log)

    rules = _load_rules()
    if not rules:
        logger.error(
            "No register rules parsed from canonical (BRAND_FRENCH_PATTERNS.md / "
            "BRAND_SPANISH_PATTERNS.md). Refusing to PASS."
        )
        return 1

    consumer_roots = _resolve_consumer_roots([Path(p) for p in args.consumer_root])
    if not consumer_roots:
        msg = "No consumer repos found at default sibling paths. Skipping voice-register scan."
        if args.strict_empty:
            logger.error("%s", msg)
            return 1
        logger.info("%s", msg)
        return 0

    all_hits: list[RegisterHit] = []
    files_scanned = 0
    for repo_name, repo_root in consumer_roots:
        for messages_subpath in MESSAGE_RELATIVE_PATHS:
            messages_dir = repo_root / messages_subpath
            if not messages_dir.exists():
                continue
            for path in messages_dir.rglob("*.json"):
                files_scanned += 1
                all_hits.extend(_scan_message_file(path, rules))

    if all_hits:
        for hit in all_hits[:200]:
            try:
                rel = hit.file.relative_to(REPO_ROOT.parent)
            except ValueError:
                rel = hit.file
            logger.error(
                "%s [%s] %s: %r — %s (canonical: %s)",
                rel,
                hit.locale,
                hit.json_path,
                hit.rule.token,
                hit.rule.rationale,
                hit.rule.canonical_source,
            )
        if len(all_hits) > 200:
            logger.error("... and %d more hits suppressed", len(all_hits) - 200)
        logger.error(
            "BRAND_VOICE_REGISTER: %d forbidden register pattern(s) across %d file(s)",
            len(all_hits),
            len({h.file for h in all_hits}),
        )
        return 1

    logger.info(
        "BRAND_VOICE_REGISTER OK — %d message file(s) scanned across %d consumer repo(s); "
        "0 register-pattern violations",
        files_scanned,
        len(consumer_roots),
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
