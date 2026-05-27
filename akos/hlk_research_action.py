"""Pydantic SSOT for Research Action source ledgers.

This module supports Wave R+4 C1.6 research-ops governance. It makes the
operator's research-action requirement executable: every source that can drive
strategic / tactical / operational decisions carries a topic cluster, source
taxonomy, format, Holistika reliability score, external perceived credibility
score, and control confidence.
"""
from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


SOURCE_LEDGER_FIELDNAMES: tuple[str, ...] = (
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

VALID_SOURCE_CATEGORIES: frozenset[str] = frozenset({
    "OSINT",
    "HUMINT",
    "SIGINT",
    "CORPINT",
    "MOTINT",
    "TBD",
})

VALID_SOURCE_LEVELS: frozenset[str] = frozenset({
    "1.1",
    "1.2",
    "1.3",
    "2.1",
    "2.2",
    "2.3",
    "3.1",
    "3.2",
    "3.3",
    "4.1",
    "4.2",
    "4.3",
    "5.1",
    "5.2",
    "5.3",
    "6.1",
    "6.2",
    "6.3",
})

VALID_SOURCE_FORMATS: frozenset[str] = frozenset({
    "article",
    "book",
    "dataset",
    "internal_canonical",
    "internal_transcript",
    "podcast",
    "report",
    "video_transcript",
    "webpage",
})

VALID_CONTROL_CONFIDENCE_LEVELS: frozenset[str] = frozenset({
    "Safe",
    "Euclid",
    "Keter",
})

DEFAULT_SOURCE_LEDGER_PATH = Path(
    "docs/wip/intelligence/research-grounded-wave-r-plus-4-2026-05-27/"
    "source-ledger.csv"
)


class ResearchSourceRow(BaseModel):
    """One source row in a research-action source ledger."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    source_id: str = Field(min_length=1, max_length=80)
    prong: str = Field(min_length=1, max_length=20)
    topic_cluster: str = Field(min_length=1, max_length=120)
    source_title_or_owner: str = Field(min_length=1, max_length=240)
    url: str = Field(min_length=1, max_length=500)
    format: Literal[
        "article",
        "book",
        "dataset",
        "internal_canonical",
        "internal_transcript",
        "podcast",
        "report",
        "video_transcript",
        "webpage",
    ]
    source_category: Literal["OSINT", "HUMINT", "SIGINT", "CORPINT", "MOTINT", "TBD"]
    source_level: Literal[
        "1.1",
        "1.2",
        "1.3",
        "2.1",
        "2.2",
        "2.3",
        "3.1",
        "3.2",
        "3.3",
        "4.1",
        "4.2",
        "4.3",
        "5.1",
        "5.2",
        "5.3",
        "6.1",
        "6.2",
        "6.3",
    ]
    holistika_reliability_score: int = Field(ge=1, le=5)
    external_perceived_credibility_score: int = Field(ge=1, le=5)
    control_confidence_level: Literal["Safe", "Euclid", "Keter"]
    decision_use: str = Field(min_length=1, max_length=240)
    notes: str = Field(default="", max_length=600)

    @field_validator("source_id")
    @classmethod
    def source_id_shape(cls, value: str) -> str:
        if not value.startswith("SRC-"):
            raise ValueError("source_id must start with SRC-")
        return value

    @field_validator("url")
    @classmethod
    def url_shape(cls, value: str) -> str:
        if not (
            value.startswith("https://")
            or value.startswith("http://")
            or value.startswith("docs/")
        ):
            raise ValueError("url must be http(s) or repo-relative docs/ path")
        return value


class ResearchSourceLedgerSummary(BaseModel):
    """Aggregate validation summary for a source ledger."""

    model_config = ConfigDict(extra="forbid")

    ledger_path: str
    source_count: int
    unique_source_ids: int
    topic_clusters: list[str]
    control_confidence_counts: dict[str, int]


def fixture_source_row() -> ResearchSourceRow:
    """Return one valid source row for validator self-tests."""

    return ResearchSourceRow(
        source_id="SRC-WR4-EF-01",
        prong="E;F",
        topic_cluster="agentic_context_and_pedagogy",
        source_title_or_owner="Nate B Jones video on agentic/context topics",
        url="https://www.youtube.com/watch?v=ogTLWGBc3cE",
        format="video_transcript",
        source_category="OSINT",
        source_level="2.1",
        holistika_reliability_score=4,
        external_perceived_credibility_score=4,
        control_confidence_level="Keter",
        decision_use="C3/C4 MADEIRA thesis and pedagogy",
        notes="Operator-named source; creator format needs corroboration.",
    )
