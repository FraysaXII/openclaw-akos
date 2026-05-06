"""Initiative 59 P5 — tests for scripts/check_active_initiative_freshness.py."""

from __future__ import annotations

import csv
from datetime import date, timedelta
from pathlib import Path

import pytest

import importlib.util, sys

REPO_ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "freshness_under_test",
    REPO_ROOT / "scripts" / "check_active_initiative_freshness.py",
)
assert _spec is not None and _spec.loader is not None
_mod = importlib.util.module_from_spec(_spec)
sys.modules["freshness_under_test"] = _mod
_spec.loader.exec_module(_mod)


def _seed_csv(tmp_path: Path, rows: list[dict[str, str]]) -> Path:
    csv_path = tmp_path / "INITIATIVE_REGISTRY.csv"
    fieldnames = list(rows[0].keys()) if rows else ["initiative_id", "status", "last_review", "title", "folder_path"]
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return csv_path


def test_all_fresh(tmp_path: Path) -> None:
    today = date(2026, 5, 6)
    rows = [
        {"initiative_id": "INIT-X-03", "status": "active", "last_review": "2026-05-01", "title": "A", "folder_path": "docs/wip/planning/03-a/"},
        {"initiative_id": "INIT-X-08", "status": "active", "last_review": "2026-04-30", "title": "B", "folder_path": "docs/wip/planning/08-b/"},
    ]
    csv_path = _seed_csv(tmp_path, rows)
    stale, fresh = _mod.check_freshness(14, csv_path=csv_path, today=today)
    assert len(stale) == 0
    assert len(fresh) == 2


def test_stale_flagged(tmp_path: Path) -> None:
    today = date(2026, 5, 6)
    rows = [
        {"initiative_id": "INIT-X-03", "status": "active", "last_review": "2026-04-01", "title": "A", "folder_path": "docs/wip/planning/03-a/"},
        {"initiative_id": "INIT-X-08", "status": "active", "last_review": "2026-05-01", "title": "B", "folder_path": "docs/wip/planning/08-b/"},
    ]
    csv_path = _seed_csv(tmp_path, rows)
    stale, fresh = _mod.check_freshness(14, csv_path=csv_path, today=today)
    assert len(stale) == 1
    assert stale[0]["initiative_id"] == "INIT-X-03"
    assert stale[0]["days_since"] == 35
    assert len(fresh) == 1


def test_non_active_excluded(tmp_path: Path) -> None:
    today = date(2026, 5, 6)
    rows = [
        {"initiative_id": "INIT-X-01", "status": "closed", "last_review": "2026-01-01", "title": "Old", "folder_path": ""},
        {"initiative_id": "INIT-X-02", "status": "continuous", "last_review": "2026-01-01", "title": "Loop", "folder_path": ""},
        {"initiative_id": "INIT-X-03", "status": "active", "last_review": "2026-05-06", "title": "A", "folder_path": ""},
    ]
    csv_path = _seed_csv(tmp_path, rows)
    stale, fresh = _mod.check_freshness(14, csv_path=csv_path, today=today)
    assert len(stale) == 0
    assert len(fresh) == 1
    assert fresh[0]["initiative_id"] == "INIT-X-03"


def test_missing_last_review_is_stale(tmp_path: Path) -> None:
    today = date(2026, 5, 6)
    rows = [
        {"initiative_id": "INIT-X-99", "status": "active", "last_review": "", "title": "Unreviewed", "folder_path": "docs/wip/planning/99-no-reports/"},
    ]
    csv_path = _seed_csv(tmp_path, rows)
    stale, fresh = _mod.check_freshness(14, csv_path=csv_path, today=today)
    assert len(stale) == 1
    assert stale[0]["days_since"] is None


def test_missing_csv_returns_empty(tmp_path: Path) -> None:
    csv_path = tmp_path / "nonexistent.csv"
    stale, fresh = _mod.check_freshness(14, csv_path=csv_path, today=date(2026, 5, 6))
    assert stale == [] and fresh == []


def test_custom_threshold(tmp_path: Path) -> None:
    today = date(2026, 5, 6)
    rows = [
        {"initiative_id": "INIT-X-03", "status": "active", "last_review": "2026-04-20", "title": "A", "folder_path": ""},
    ]
    csv_path = _seed_csv(tmp_path, rows)
    stale_7, _ = _mod.check_freshness(7, csv_path=csv_path, today=today)
    stale_30, _ = _mod.check_freshness(30, csv_path=csv_path, today=today)
    assert len(stale_7) == 1
    assert len(stale_30) == 0
