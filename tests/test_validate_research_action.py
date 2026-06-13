from __future__ import annotations

import csv
from pathlib import Path

import pytest

from akos.hlk_research_action import SOURCE_LEDGER_FIELDNAMES, fixture_source_row
from scripts.validate_research_action import validate_source_ledger


def _write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=SOURCE_LEDGER_FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


@pytest.mark.hlk
def test_validate_source_ledger_accepts_valid_fixture(tmp_path: Path) -> None:
    ledger = tmp_path / "source-ledger.csv"
    _write_rows(ledger, [fixture_source_row().model_dump()])

    ok, messages, summary = validate_source_ledger(ledger)

    assert ok is True
    assert messages == []
    assert summary is not None
    assert summary.source_count == 1
    assert summary.control_confidence_counts == {"Keter": 1}


@pytest.mark.hlk
def test_validate_source_ledger_rejects_bad_header(tmp_path: Path) -> None:
    ledger = tmp_path / "source-ledger.csv"
    ledger.write_text("source_id,url\nSRC-X,https://example.com\n", encoding="utf-8")

    ok, messages, summary = validate_source_ledger(ledger)

    assert ok is False
    assert summary is None
    assert "header mismatch" in messages[0]


@pytest.mark.hlk
def test_validate_source_ledger_rejects_invalid_prong(tmp_path: Path) -> None:
    ledger = tmp_path / "source-ledger.csv"
    row = fixture_source_row().model_dump()
    row["prong"] = "B"
    _write_rows(ledger, [row])

    ok, messages, summary = validate_source_ledger(ledger)

    assert ok is False
    assert summary is None
    assert any("not a baseline consumer ID" in message for message in messages)


@pytest.mark.hlk
def test_validate_source_ledger_rejects_charter_alias_prong(tmp_path: Path) -> None:
    ledger = tmp_path / "source-ledger.csv"
    row = fixture_source_row().model_dump()
    row["prong"] = "P1-TECH"
    _write_rows(ledger, [row])

    ok, messages, summary = validate_source_ledger(ledger)

    assert ok is False
    assert summary is None
    assert any("should be 'BL-TECH'" in message for message in messages)


@pytest.mark.hlk
def test_validate_source_ledger_rejects_duplicate_ids(tmp_path: Path) -> None:
    ledger = tmp_path / "source-ledger.csv"
    row = fixture_source_row().model_dump()
    _write_rows(ledger, [row, row])

    ok, messages, summary = validate_source_ledger(ledger)

    assert ok is False
    assert summary is None
    assert any("duplicate source_id" in message for message in messages)
