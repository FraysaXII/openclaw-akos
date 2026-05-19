"""Canonical-enrichment freshness audit chassis (I86 Wave H Lane E).

Operator-ratified 2026-05-19 via D-IH-86-AB (proposed; canonical row appended
by the cluster-burndown parent after Lane A + Lane C land). Codifies a 3-tier
staleness taxonomy for v3.0 area canonicals:

* ``fresh``      — reviewed within the short-term window (default 3 days; the
  operator's 2026-05-19 quote: "Option D but make it 3 days, because we're
  real fast today").
* ``medium``     — reviewed within the medium-term window (default 30 days).
* ``long_term``  — reviewed within the long-term window (default 90 days).
* ``stale``      — beyond ``long_term_days`` OR ``last_review_at:`` /
  ``last_review:`` frontmatter is missing.

This module is the Pydantic-typed *chassis* the executable runbook
``scripts/validate_canonical_enrichment_freshness.py`` and the paired SOP
``SOP-TECH_CANONICAL_FRESHNESS_AUDIT_001.md`` (mint pending; planned path
``docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-TECH_CANONICAL_FRESHNESS_AUDIT_001.md``)
both consume. Honouring ``akos-executable-process-catalog.mdc`` RULE 1: the
SOP is the operator-facing canonical, the runbook is the agent-facing
executable, and this chassis is the typed SSOT both bind to.

Honouring ``CONTRIBUTING.md`` §"Python Code Standards":
* Pydantic v2 models with explicit ``ConfigDict``.
* Type hints on every signature.
* No ``print()`` statements — diagnostic logging goes through ``akos.log``.
* Cross-platform ``pathlib.Path`` everywhere.
"""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

FreshnessTier = Literal["fresh", "medium", "long_term", "stale"]

CANONICAL_GLOB: str = "docs/references/hlk/v3.0/Admin/O5-1/**/canonicals/**/*.md"

V30_AREA_ROOT_PARTS: tuple[str, ...] = (
    "docs",
    "references",
    "hlk",
    "v3.0",
    "Admin",
    "O5-1",
)


class FreshnessThresholds(BaseModel):
    """Three-tier staleness threshold model.

    Operator-ratified defaults (2026-05-19): 3 / 30 / 90 days. Custom thresholds
    must satisfy ``fresh_days < medium_days < long_term_days``; a model-level
    validator rejects misordered tuples so misconfigured CI invocations FAIL
    loud rather than silently miscategorise rows.
    """

    model_config = ConfigDict(frozen=True)

    fresh_days: int = Field(
        default=3,
        ge=1,
        description="Short-term threshold: ≤ N days since last review counts as 'fresh'.",
    )
    medium_days: int = Field(
        default=30,
        ge=1,
        description="Medium-term threshold: > fresh_days and ≤ medium_days counts as 'medium'.",
    )
    long_term_days: int = Field(
        default=90,
        ge=1,
        description="Long-term threshold: > medium_days and ≤ long_term_days counts as 'long_term'; beyond is 'stale'.",
    )

    @model_validator(mode="after")
    def _check_ordering(self) -> "FreshnessThresholds":
        if not (self.fresh_days < self.medium_days < self.long_term_days):
            raise ValueError(
                "FreshnessThresholds must satisfy fresh_days < medium_days < long_term_days; "
                f"got fresh={self.fresh_days} medium={self.medium_days} long_term={self.long_term_days}."
            )
        return self


class CanonicalFreshnessRow(BaseModel):
    """One row in the freshness audit table — one canonical markdown surface.

    ``last_review_at`` retains the YYYY-MM-DD string when present in
    frontmatter (either under that key or the legacy ``last_review`` key);
    ``days_since_review`` is ``None`` when no review date could be parsed,
    and the row is then categorised as ``stale`` by the chassis.
    """

    model_config = ConfigDict(frozen=True, extra="ignore")

    path: str = Field(description="Repo-relative POSIX-style path to the canonical markdown surface.")
    area: str = Field(description="Area name parsed from path (People / Marketing / Tech / Operations / Envoy Tech Lab / Research / Finance / Admin).")
    intellectual_kind: Optional[str] = Field(
        default=None,
        description="Optional intellectual_kind frontmatter value (canon / sop / doctrine / ...) if present.",
    )
    last_review_at: Optional[str] = Field(
        default=None,
        description="YYYY-MM-DD review date sourced from `last_review_at:` or `last_review:` frontmatter, when present.",
    )
    days_since_review: Optional[int] = Field(
        default=None,
        description="Integer days from last_review_at to scan-date (clamped at 0 for future dates).",
    )
    tier: FreshnessTier = Field(description="Categorisation per FreshnessThresholds; 'stale' when no review date.")


class FreshnessAreaSummary(BaseModel):
    """Per-area aggregation of freshness rows for the audit summary table."""

    model_config = ConfigDict(frozen=True)

    area: str
    fresh: int = 0
    medium: int = 0
    long_term: int = 0
    stale: int = 0

    @property
    def total(self) -> int:
        return self.fresh + self.medium + self.long_term + self.stale


def parse_area_from_path(p: Path, repo_root: Path) -> str:
    """Return the area name embedded in a v3.0 canonical path.

    Example mappings::

        docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/foo.md          -> "People"
        docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/foo.md -> "Marketing"
        docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/foo.md  -> "Envoy Tech Lab"
        docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/foo  -> "Tech"

    Paths that do not contain ``Admin/O5-1`` (e.g. external mirrors) return
    the literal string ``"unknown"`` so downstream tables can flag them rather
    than crashing on a missing path segment.
    """
    try:
        rel = p.resolve().relative_to(repo_root.resolve())
    except ValueError:
        rel = p
    parts = rel.parts
    for idx, segment in enumerate(parts):
        if segment == "O5-1" and idx + 1 < len(parts):
            return parts[idx + 1]
    return "unknown"


def compute_days_since(last_review_at: str, today: date) -> int:
    """Return days from ``last_review_at`` (YYYY-MM-DD) to ``today``.

    Future review dates clamp to 0 (no negative days) so a typo'd 2099 date
    surfaces as ``fresh`` rather than as a negative-tier surprise. Raises
    ``ValueError`` for unparseable date strings so the runbook can record
    the bad row and continue scanning.
    """
    parsed = datetime.strptime(last_review_at.strip(), "%Y-%m-%d").date()
    delta = (today - parsed).days
    return max(delta, 0)


def categorize(days_since: Optional[int], thresholds: FreshnessThresholds) -> FreshnessTier:
    """Categorise a row into one of the four tiers.

    Missing ``days_since`` (i.e. no parseable review date) always maps to
    ``stale``; the absence of a review date is the strongest possible
    enrichment-cadence signal.
    """
    if days_since is None:
        return "stale"
    if days_since <= thresholds.fresh_days:
        return "fresh"
    if days_since <= thresholds.medium_days:
        return "medium"
    if days_since <= thresholds.long_term_days:
        return "long_term"
    return "stale"


_FRONTMATTER_FENCE = "---"


def _parse_frontmatter(text: str) -> dict[str, str]:
    """Minimal YAML-frontmatter parser: top-level ``key: value`` only.

    Deliberately small: this chassis only needs flat ``key: value`` rows for
    ``last_review_at``, ``last_review``, and ``intellectual_kind``. Nested
    mappings, lists, and multi-line scalars are tolerated (we skip them).
    Returns ``{}`` when no frontmatter block is found.
    """
    stripped = text.lstrip("\ufeff")
    if not stripped.startswith(_FRONTMATTER_FENCE):
        return {}
    lines = stripped.splitlines()
    if not lines or lines[0].strip() != _FRONTMATTER_FENCE:
        return {}
    out: dict[str, str] = {}
    for raw in lines[1:]:
        if raw.strip() == _FRONTMATTER_FENCE:
            break
        if not raw or raw.lstrip() != raw:
            continue
        if ":" not in raw:
            continue
        key, _, value = raw.partition(":")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and value:
            out[key] = value
    return out


def _extract_review_date(frontmatter: dict[str, str]) -> Optional[str]:
    """Prefer ``last_review_at:``; fall back to legacy ``last_review:``."""
    for key in ("last_review_at", "last_review"):
        value = frontmatter.get(key)
        if value:
            return value.strip()
    return None


def scan_canonical(
    path: Path,
    repo_root: Path,
    today: date,
    thresholds: FreshnessThresholds,
) -> CanonicalFreshnessRow:
    """Scan a single canonical markdown file and return its freshness row.

    Reads the file with ``utf-8`` + ``errors='replace'`` so a stray byte does
    not crash a 150+-file scan; the runbook surfaces per-file failures via
    logger.warning rather than aborting.
    """
    text = path.read_text(encoding="utf-8", errors="replace")
    frontmatter = _parse_frontmatter(text)
    review_str = _extract_review_date(frontmatter)
    days_since: Optional[int]
    if review_str is None:
        days_since = None
    else:
        try:
            days_since = compute_days_since(review_str, today)
        except ValueError:
            days_since = None
            review_str = None
    try:
        rel_posix = path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        rel_posix = path.as_posix()
    return CanonicalFreshnessRow(
        path=rel_posix,
        area=parse_area_from_path(path, repo_root),
        intellectual_kind=frontmatter.get("intellectual_kind"),
        last_review_at=review_str,
        days_since_review=days_since,
        tier=categorize(days_since, thresholds),
    )


def summarize_by_area(rows: list[CanonicalFreshnessRow]) -> list[FreshnessAreaSummary]:
    """Aggregate rows into per-area summary records, sorted by area name."""
    buckets: dict[str, dict[str, int]] = {}
    for row in rows:
        bucket = buckets.setdefault(
            row.area,
            {"fresh": 0, "medium": 0, "long_term": 0, "stale": 0},
        )
        bucket[row.tier] += 1
    return [
        FreshnessAreaSummary(
            area=area,
            fresh=counts["fresh"],
            medium=counts["medium"],
            long_term=counts["long_term"],
            stale=counts["stale"],
        )
        for area, counts in sorted(buckets.items())
    ]
