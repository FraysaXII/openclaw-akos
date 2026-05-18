"""Pydantic chassis for INITIATIVE_REGISTRY -> PROGRAM_REGISTRY anchor parsing (I86 P1).

Per D-IH-86-H (ratified Round 2 of I86 master-roadmap) initiatives with
``status in {active, continuous, program_line}`` may carry a free-text
``Program anchors: PRJ-HOL-<CODE>-<YEAR>; PRJ-HOL-<CODE>-<YEAR>`` prefix in
their ``notes`` column. The prefix is a foreign-key carrier into
``PROGRAM_REGISTRY.csv`` until the column-promotion phase (I86 P2 / D-IH-86-J)
lands a first-class ``program_anchors`` semicolon-list column on
[`INITIATIVE_REGISTRY.csv`](../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv).

This module exposes the parse contract so the validator
([`scripts/validate_initiative_program_anchors.py`](../scripts/validate_initiative_program_anchors.py))
and runbook
([`scripts/pmo_program_anchor_backfill.py`](../scripts/pmo_program_anchor_backfill.py))
share one Pydantic-grounded shape.

Per [`CONTRIBUTING.md`](../CONTRIBUTING.md) "Python Code Standards":
Pydantic models replace hand-written ``assert`` chains; type hints on every
signature; no ``print()`` (use ``akos.log.setup_logging``).
"""

from __future__ import annotations

import re
from typing import Iterable

from pydantic import BaseModel, Field, field_validator

ANCHOR_PREFIX: str = "Program anchors:"
PROGRAM_ID_PATTERN: re.Pattern[str] = re.compile(r"^PRJ-HOL-[A-Z]+-\d{4}$")
ANCHOR_LINE_PATTERN: re.Pattern[str] = re.compile(
    r"Program anchors:\s*(?P<list>[^.]+?)(?:\.|$)",
    re.IGNORECASE,
)


class InitiativeProgramAnchorParse(BaseModel):
    """Result of parsing an ``INITIATIVE_REGISTRY.csv`` ``notes`` cell.

    Attributes:
        initiative_id: Row primary key (e.g. ``INIT-OPENCLAW_AKOS-01``).
        notes_raw: Original ``notes`` cell content (may be empty).
        has_prefix: True when the ``Program anchors:`` prefix is present.
        anchors: Parsed ``PRJ-HOL-*-YYYY`` ids from the prefix (de-duplicated; order preserved).
        unknown_anchors: Anchors whose id is not present in the supplied program registry.
        malformed_tokens: Tokens that look anchor-shaped but fail the id regex.
    """

    initiative_id: str = Field(..., min_length=1)
    notes_raw: str = Field(default="")
    has_prefix: bool = Field(default=False)
    anchors: list[str] = Field(default_factory=list)
    unknown_anchors: list[str] = Field(default_factory=list)
    malformed_tokens: list[str] = Field(default_factory=list)

    @field_validator("anchors", "unknown_anchors", "malformed_tokens")
    @classmethod
    def _strip_empty(cls, value: list[str]) -> list[str]:
        return [v.strip() for v in value if v and v.strip()]


def _split_semi(value: str) -> list[str]:
    return [s.strip() for s in (value or "").split(";") if s.strip()]


def parse_anchor_prefix(notes: str) -> tuple[bool, list[str], list[str]]:
    """Extract anchor ids from the ``Program anchors:`` prefix of a notes cell.

    Returns ``(has_prefix, well_formed_ids, malformed_tokens)``.

    Pattern: ``Program anchors: <id>; <id>; <id>.`` where the terminating ``.`` or
    end-of-string closes the list. Subsequent prose in ``notes`` is preserved by
    callers; this parser does not consume beyond the period.
    """
    if not notes:
        return False, [], []
    match = ANCHOR_LINE_PATTERN.search(notes)
    if not match:
        return False, [], []
    tokens = _split_semi(match.group("list"))
    well_formed: list[str] = []
    malformed: list[str] = []
    seen: set[str] = set()
    for token in tokens:
        if PROGRAM_ID_PATTERN.match(token):
            if token not in seen:
                seen.add(token)
                well_formed.append(token)
        else:
            malformed.append(token)
    return True, well_formed, malformed


def parse_initiative_row(
    initiative_id: str,
    notes: str,
    known_program_ids: Iterable[str],
) -> InitiativeProgramAnchorParse:
    """Build an ``InitiativeProgramAnchorParse`` for one INITIATIVE_REGISTRY row.

    ``known_program_ids`` is the FK target set (typically the ``program_id``
    column of ``PROGRAM_REGISTRY.csv``). Anchors not in that set are surfaced
    via ``unknown_anchors`` so the validator can fail-loud on typos.
    """
    program_set = {p.strip() for p in known_program_ids if p and p.strip()}
    has_prefix, well_formed, malformed = parse_anchor_prefix(notes)
    unknown = [a for a in well_formed if a not in program_set] if program_set else []
    return InitiativeProgramAnchorParse(
        initiative_id=initiative_id,
        notes_raw=notes or "",
        has_prefix=has_prefix,
        anchors=well_formed,
        unknown_anchors=unknown,
        malformed_tokens=malformed,
    )


__all__ = [
    "ANCHOR_PREFIX",
    "PROGRAM_ID_PATTERN",
    "ANCHOR_LINE_PATTERN",
    "InitiativeProgramAnchorParse",
    "parse_anchor_prefix",
    "parse_initiative_row",
]
