from __future__ import annotations

import csv
from pathlib import Path

import pytest

from akos.evidence_class_gate import (
    acim_has_evidence_proof,
    is_url_hash_padding,
    normalize_url_for_dedupe,
)
from akos.hlk_research_action import SOURCE_LEDGER_FIELDNAMES, fixture_source_row
from scripts.validate_research_action import validate_source_ledger


def _write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=SOURCE_LEDGER_FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


@pytest.mark.hlk
def test_evidence_gate_hash_padding_helper() -> None:
    assert is_url_hash_padding("https://vercel.com/docs/foo#12")
    assert not is_url_hash_padding("https://vercel.com/docs/foo")
    assert normalize_url_for_dedupe("https://x.com/a#1") == "https://x.com/a"


@pytest.mark.hlk
def test_acim_evidence_proof_from_tool_catalog_ref() -> None:
    assert acim_has_evidence_proof(
        notes="",
        realisation_refs="",
        tool_catalog_ref="scripts/validate_component_module_registry.py",
    )


@pytest.mark.hlk
def test_validate_source_ledger_rejects_hash_padding(tmp_path: Path) -> None:
    ledger = tmp_path / "source-ledger.csv"
    row = fixture_source_row().model_dump()
    row["format"] = "webpage"
    row["url"] = "https://vercel.com/docs/deployments/troubleshoot#1"
    _write_rows(ledger, [row])

    ok, messages, summary = validate_source_ledger(ledger)

    assert ok is False
    assert summary is None
    assert any("RA-EC-01" in message for message in messages)
