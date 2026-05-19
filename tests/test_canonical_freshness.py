"""Tests for the canonical-enrichment freshness chassis + runbook (I86 Wave H Lane E).

Covers ``akos/canonical_freshness.py`` (Pydantic chassis) and exercises the
runbook ``scripts/validate_canonical_enrichment_freshness.py`` via the chassis
helpers directly. Honours the operator-ratified 3-tier defaults (3 / 30 / 90
days) and the boundary semantics codified in D-IH-86-AB (proposed).
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import pytest
from pydantic import ValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from akos.canonical_freshness import (  # noqa: E402
    CanonicalFreshnessRow,
    FreshnessAreaSummary,
    FreshnessThresholds,
    categorize,
    compute_days_since,
    parse_area_from_path,
    scan_canonical,
    summarize_by_area,
)

DEFAULT_THRESHOLDS = FreshnessThresholds()


# ---------------------------------------------------------------------------
# FreshnessThresholds (Pydantic validation)
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_thresholds_defaults_are_operator_ratified():
    """3 / 30 / 90 per operator ratify 2026-05-19 (D-IH-86-AB proposed)."""
    t = FreshnessThresholds()
    assert t.fresh_days == 3
    assert t.medium_days == 30
    assert t.long_term_days == 90


@pytest.mark.unit
def test_thresholds_reject_non_positive():
    with pytest.raises(ValidationError):
        FreshnessThresholds(fresh_days=0, medium_days=30, long_term_days=90)
    with pytest.raises(ValidationError):
        FreshnessThresholds(fresh_days=3, medium_days=-1, long_term_days=90)


@pytest.mark.unit
def test_thresholds_enforce_strict_ordering():
    # fresh < medium < long_term required
    with pytest.raises(ValidationError):
        FreshnessThresholds(fresh_days=30, medium_days=3, long_term_days=90)
    with pytest.raises(ValidationError):
        FreshnessThresholds(fresh_days=3, medium_days=90, long_term_days=30)
    with pytest.raises(ValidationError):
        FreshnessThresholds(fresh_days=3, medium_days=3, long_term_days=90)  # equal not allowed


@pytest.mark.unit
def test_thresholds_are_frozen():
    t = FreshnessThresholds()
    with pytest.raises(ValidationError):
        t.fresh_days = 10  # type: ignore[misc]


# ---------------------------------------------------------------------------
# categorize() — tier boundary semantics
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    ("days", "expected"),
    [
        (0, "fresh"),     # same-day review
        (1, "fresh"),
        (3, "fresh"),     # boundary: exactly fresh_days
        (4, "medium"),    # one past fresh
        (15, "medium"),
        (30, "medium"),   # boundary: exactly medium_days
        (31, "long_term"),
        (60, "long_term"),
        (90, "long_term"), # boundary: exactly long_term_days
        (91, "stale"),    # one past long_term
        (365, "stale"),
    ],
)
def test_categorize_at_default_boundaries(days: int, expected: str):
    assert categorize(days, DEFAULT_THRESHOLDS) == expected


@pytest.mark.unit
def test_categorize_missing_days_is_stale():
    assert categorize(None, DEFAULT_THRESHOLDS) == "stale"


@pytest.mark.unit
def test_categorize_respects_custom_thresholds():
    custom = FreshnessThresholds(fresh_days=7, medium_days=14, long_term_days=21)
    assert categorize(7, custom) == "fresh"
    assert categorize(8, custom) == "medium"
    assert categorize(14, custom) == "medium"
    assert categorize(15, custom) == "long_term"
    assert categorize(21, custom) == "long_term"
    assert categorize(22, custom) == "stale"


# ---------------------------------------------------------------------------
# compute_days_since() — date math, future-clamp, parse errors
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_compute_days_since_positive_delta():
    today = date(2026, 5, 19)
    assert compute_days_since("2026-05-15", today) == 4
    assert compute_days_since("2026-05-19", today) == 0  # same-day


@pytest.mark.unit
def test_compute_days_since_clamps_future_dates_to_zero():
    """Future review dates clamp to 0 so a typo'd 2099 never reads negative."""
    today = date(2026, 5, 19)
    assert compute_days_since("2099-01-01", today) == 0


@pytest.mark.unit
def test_compute_days_since_raises_on_bad_string():
    today = date(2026, 5, 19)
    with pytest.raises(ValueError):
        compute_days_since("not-a-date", today)
    with pytest.raises(ValueError):
        compute_days_since("2026/05/19", today)  # wrong format


# ---------------------------------------------------------------------------
# parse_area_from_path() — area parsing from real-shape paths
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    ("rel_path", "expected_area"),
    [
        ("docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/FOO.md", "People"),
        ("docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BAR.md", "Marketing"),
        ("docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/BAZ.md", "Envoy Tech Lab"),
        ("docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/QUX.md", "Tech"),
        ("docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/SUB/AREA.md", "Operations"),
        ("docs/references/hlk/v3.0/Admin/O5-1/Finance/Business Controller/canonicals/X.md", "Finance"),
        ("docs/references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/Y.md", "Research"),
        ("docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/Z.md", "People"),
    ],
)
def test_parse_area_from_real_shapes(tmp_path: Path, rel_path: str, expected_area: str):
    repo_root = tmp_path
    target = repo_root / rel_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("---\n---\n", encoding="utf-8")
    assert parse_area_from_path(target, repo_root) == expected_area


@pytest.mark.unit
def test_parse_area_returns_unknown_for_non_v30_paths(tmp_path: Path):
    target = tmp_path / "totally" / "unrelated" / "file.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("---\n---\n", encoding="utf-8")
    assert parse_area_from_path(target, tmp_path) == "unknown"


# ---------------------------------------------------------------------------
# scan_canonical() — frontmatter parsing, fallback, missing dates
# ---------------------------------------------------------------------------


def _write_canonical(
    repo_root: Path,
    rel_path: str,
    frontmatter_body: str = "",
) -> Path:
    target = repo_root / rel_path
    target.parent.mkdir(parents=True, exist_ok=True)
    text = "---\n" + frontmatter_body.strip("\n") + "\n---\n\n# heading\n\nbody.\n"
    target.write_text(text, encoding="utf-8")
    return target


@pytest.mark.unit
def test_scan_canonical_prefers_last_review_at_over_last_review(tmp_path: Path):
    target = _write_canonical(
        tmp_path,
        "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/X.md",
        "last_review_at: 2026-05-19\nlast_review: 2020-01-01\n",
    )
    row = scan_canonical(target, tmp_path, date(2026, 5, 19), DEFAULT_THRESHOLDS)
    assert row.last_review_at == "2026-05-19"
    assert row.days_since_review == 0
    assert row.tier == "fresh"


@pytest.mark.unit
def test_scan_canonical_falls_back_to_last_review(tmp_path: Path):
    target = _write_canonical(
        tmp_path,
        "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/Y.md",
        "last_review: 2026-04-15\n",
    )
    row = scan_canonical(target, tmp_path, date(2026, 5, 19), DEFAULT_THRESHOLDS)
    assert row.last_review_at == "2026-04-15"
    assert row.days_since_review == 34
    assert row.tier == "long_term"
    assert row.area == "Marketing"


@pytest.mark.unit
def test_scan_canonical_missing_review_is_stale(tmp_path: Path):
    target = _write_canonical(
        tmp_path,
        "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/Z.md",
        "status: active\n",
    )
    row = scan_canonical(target, tmp_path, date(2026, 5, 19), DEFAULT_THRESHOLDS)
    assert row.last_review_at is None
    assert row.days_since_review is None
    assert row.tier == "stale"
    assert row.area == "Tech"


@pytest.mark.unit
def test_scan_canonical_bad_date_string_is_stale(tmp_path: Path):
    target = _write_canonical(
        tmp_path,
        "docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/BAD.md",
        "last_review_at: not-a-date\n",
    )
    row = scan_canonical(target, tmp_path, date(2026, 5, 19), DEFAULT_THRESHOLDS)
    assert row.last_review_at is None  # bad date wiped
    assert row.tier == "stale"


@pytest.mark.unit
def test_scan_canonical_extracts_intellectual_kind(tmp_path: Path):
    target = _write_canonical(
        tmp_path,
        "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/IK.md",
        "intellectual_kind: doctrine\nlast_review: 2026-05-18\n",
    )
    row = scan_canonical(target, tmp_path, date(2026, 5, 19), DEFAULT_THRESHOLDS)
    assert row.intellectual_kind == "doctrine"


# ---------------------------------------------------------------------------
# Integration: synthesised tmpdir with 4 fake canonicals (one per tier)
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_integration_four_tier_synthesis(tmp_path: Path):
    today = date(2026, 5, 19)
    fixtures = [
        ("People",          "2026-05-18", "fresh"),       # 1 day ago
        ("Marketing",       "2026-05-10", "medium"),      # 9 days ago
        ("Tech",            "2026-04-01", "long_term"),   # 48 days ago
        ("Envoy Tech Lab",  "2025-12-01", "stale"),       # 169 days ago
    ]
    paths = []
    for area, last_review, _expected in fixtures:
        rel = f"docs/references/hlk/v3.0/Admin/O5-1/{area}/canonicals/F-{area.replace(' ', '_')}.md"
        paths.append(
            _write_canonical(tmp_path, rel, f"last_review_at: {last_review}\n")
        )
    # one extra surface with no review date -> stale
    _write_canonical(
        tmp_path,
        "docs/references/hlk/v3.0/Admin/O5-1/Research/canonicals/F-Research.md",
        "status: active\n",
    )

    rows = [scan_canonical(p, tmp_path, today, DEFAULT_THRESHOLDS) for p in paths]
    research_path = tmp_path / "docs/references/hlk/v3.0/Admin/O5-1/Research/canonicals/F-Research.md"
    rows.append(scan_canonical(research_path, tmp_path, today, DEFAULT_THRESHOLDS))

    tiers_by_area = {row.area: row.tier for row in rows}
    assert tiers_by_area["People"] == "fresh"
    assert tiers_by_area["Marketing"] == "medium"
    assert tiers_by_area["Tech"] == "long_term"
    assert tiers_by_area["Envoy Tech Lab"] == "stale"
    assert tiers_by_area["Research"] == "stale"

    summaries = summarize_by_area(rows)
    summary_by_area = {s.area: s for s in summaries}
    assert summary_by_area["People"].fresh == 1
    assert summary_by_area["Marketing"].medium == 1
    assert summary_by_area["Tech"].long_term == 1
    assert summary_by_area["Envoy Tech Lab"].stale == 1
    assert summary_by_area["Research"].stale == 1
    assert sum(s.total for s in summaries) == 5


# ---------------------------------------------------------------------------
# CanonicalFreshnessRow — Pydantic SSOT shape contract
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_canonical_row_is_frozen():
    row = CanonicalFreshnessRow(path="a.md", area="People", tier="fresh")
    with pytest.raises(ValidationError):
        row.area = "Marketing"  # type: ignore[misc]


@pytest.mark.unit
def test_canonical_row_tier_must_be_enum_value():
    with pytest.raises(ValidationError):
        CanonicalFreshnessRow(path="a.md", area="People", tier="ancient")  # type: ignore[arg-type]


@pytest.mark.unit
def test_summary_total_property():
    s = FreshnessAreaSummary(area="People", fresh=12, medium=8, long_term=3, stale=1)
    assert s.total == 24
