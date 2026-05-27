from __future__ import annotations

import pytest
from pydantic import ValidationError

from akos.hlk_research_action import (
    SOURCE_LEDGER_FIELDNAMES,
    VALID_CONTROL_CONFIDENCE_LEVELS,
    VALID_SOURCE_CATEGORIES,
    VALID_SOURCE_FORMATS,
    ResearchSourceLedgerSummary,
    ResearchSourceRow,
    fixture_source_row,
)


@pytest.mark.hlk
def test_source_ledger_fieldnames_include_scores() -> None:
    assert SOURCE_LEDGER_FIELDNAMES == (
        "source_id",
        "prong",
        "topic_cluster",
        "source_title_or_owner",
        "url",
        "format",
        "source_category",
        "source_level",
        "holistika_reliability_score",
        "external_perceived_credibility_score",
        "control_confidence_level",
        "decision_use",
        "notes",
    )


@pytest.mark.hlk
def test_fixture_source_row_is_valid() -> None:
    row = fixture_source_row()
    assert row.source_id == "SRC-WR4-EF-01"
    assert row.format in VALID_SOURCE_FORMATS
    assert row.source_category in VALID_SOURCE_CATEGORIES
    assert row.control_confidence_level in VALID_CONTROL_CONFIDENCE_LEVELS


@pytest.mark.hlk
def test_source_scores_are_bounded() -> None:
    data = fixture_source_row().model_dump()
    data["holistika_reliability_score"] = 6
    with pytest.raises(ValidationError):
        ResearchSourceRow.model_validate(data)

    data = fixture_source_row().model_dump()
    data["external_perceived_credibility_score"] = 0
    with pytest.raises(ValidationError):
        ResearchSourceRow.model_validate(data)


@pytest.mark.hlk
def test_source_id_requires_prefix() -> None:
    data = fixture_source_row().model_dump()
    data["source_id"] = "WR4-EF-01"
    with pytest.raises(ValidationError):
        ResearchSourceRow.model_validate(data)


@pytest.mark.hlk
def test_summary_round_trip() -> None:
    row = fixture_source_row()
    summary = ResearchSourceLedgerSummary(
        ledger_path="docs/wip/intelligence/example/source-ledger.csv",
        source_count=1,
        unique_source_ids=1,
        topic_clusters=[row.topic_cluster],
        control_confidence_counts={row.control_confidence_level: 1},
    )
    assert summary.control_confidence_counts == {"Keter": 1}
