#!/usr/bin/env python3
"""Validate P6 deck companion completeness and public/private register split."""

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

logger = logging.getLogger("akos.dossier_companion_drift")

DECK_DIR = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "_assets" / "advops" / "shared" / "decks"
INTERNAL_TOKENS = (
    "counterparty",
    "elicitation",
    "reliability grading",
    "intelligence collection",
    "intelligence report",
    "approach techniques",
    "baseline reality assessment",
)


@dataclass(frozen=True)
class CompanionError:
    file: Path
    rule: str
    detail: str


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _frontmatter(text: str) -> str:
    match = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    return match.group(1) if match else ""


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _scan_public_deck_for_internal_tokens(path: Path) -> list[CompanionError]:
    text = _read(path)
    body = re.sub(r"^---\s*\n.*?\n---\s*", "", text, count=1, flags=re.DOTALL)
    errors: list[CompanionError] = []
    for token in INTERNAL_TOKENS:
        for match in re.finditer(rf"\b{re.escape(token)}\b", body, re.IGNORECASE):
            errors.append(
                CompanionError(
                    path,
                    "internal_token_in_public_deck",
                    f"token {token!r} at body line {_line_number(body, match.start())}",
                )
            )
    return errors


def _check_companion(path: Path, expected_kind: str) -> list[CompanionError]:
    if not path.exists():
        return [CompanionError(path, "missing_companion", "required companion file not found")]
    text = _read(path)
    fm = _frontmatter(text)
    errors: list[CompanionError] = []
    if "access_level: 5" not in fm:
        errors.append(CompanionError(path, "companion_access_level", "companion must be access_level: 5"))
    if "operator_private" not in fm:
        errors.append(CompanionError(path, "companion_classification", "companion must be operator_private"))
    if f"artifact_kind: {expected_kind}" not in fm:
        errors.append(
            CompanionError(path, "companion_kind", f"expected artifact_kind: {expected_kind}")
        )
    return errors


def check_dossier_companions(deck_dir: Path = DECK_DIR) -> list[CompanionError]:
    if not deck_dir.exists():
        return [CompanionError(deck_dir, "deck_dir_missing", "P6 deck directory not found")]

    errors: list[CompanionError] = []
    decks = sorted(deck_dir.glob("*.deck.md"))
    if not decks:
        return [CompanionError(deck_dir, "no_decks", "no *.deck.md files found")]

    for deck in decks:
        stem = deck.name.removesuffix(".deck.md")
        objections = deck.with_name(f"{stem}.objections.md")
        brief = deck.with_name(f"{stem}.counterparty-brief.md")
        errors.extend(_scan_public_deck_for_internal_tokens(deck))
        errors.extend(_check_companion(objections, "deck_objection_companion"))
        errors.extend(_check_companion(brief, "deck_counterparty_brief"))
    return errors


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate P6 deck companion drift")
    parser.add_argument("--json-log", action="store_true")
    args = parser.parse_args(list(argv) if argv is not None else None)
    setup_logging(json_output=args.json_log)

    errors = check_dossier_companions()
    if errors:
        for err in errors:
            logger.error("%s: %s (%s)", err.rule, err.detail, err.file)
        return 1
    logger.info("DOSSIER_COMPANION_DRIFT OK - %s deck(s) have valid companions", len(list(DECK_DIR.glob("*.deck.md"))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
