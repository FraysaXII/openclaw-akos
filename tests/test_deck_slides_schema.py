"""Initiative 28 P6 — assert deck_slides.yaml has 12-14 slides with required fields.

Closes the I28 P6 verification matrix entry "tests/test_deck_slides_schema.py"
(per [`28-investor-style-company-dossier/master-roadmap.md`](../docs/wip/planning/28-investor-style-company-dossier/master-roadmap.md)
§8). Locks the slide-count band declared in I28 §2 (12-14 slides) and the
required field shape for each slide (``id``, ``layout``).

The deck currently ships **14 slides** (`page_count: 14`); the test allows
12-14 to leave room for future trim/expand without re-spec'ing the contract.
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
DECK_SLIDES_PATH = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "_assets"
    / "advops"
    / "2026-holistika-incorporation"
    / "enisa_company_dossier"
    / "deck_slides.yaml"
)

REQUIRED_TOP_KEYS = ("document", "slides")
REQUIRED_DOCUMENT_KEYS = ("title", "language", "audience", "tone", "format", "page_count")
REQUIRED_SLIDE_KEYS = ("id", "layout")

SLIDE_COUNT_MIN = 12
SLIDE_COUNT_MAX = 14


@pytest.fixture(scope="module")
def deck() -> dict:
    """Parse ``deck_slides.yaml`` once per test module."""
    yaml = pytest.importorskip("yaml")
    text = DECK_SLIDES_PATH.read_text(encoding="utf-8")
    return yaml.safe_load(text)


def test_deck_slides_yaml_present():
    assert DECK_SLIDES_PATH.is_file(), f"deck_slides.yaml missing: {DECK_SLIDES_PATH}"


def test_top_level_shape(deck):
    for key in REQUIRED_TOP_KEYS:
        assert key in deck, f"deck_slides.yaml missing top-level key: {key}"


def test_document_shape(deck):
    document = deck["document"]
    for key in REQUIRED_DOCUMENT_KEYS:
        assert key in document, f"deck.document missing required key: {key}"


def test_slide_count_in_band(deck):
    """Slide count is between 12 and 14 inclusive (per I28 §2 deck spec)."""
    slides = deck["slides"]
    n = len(slides)
    assert SLIDE_COUNT_MIN <= n <= SLIDE_COUNT_MAX, (
        f"slide count {n} outside expected band [{SLIDE_COUNT_MIN}, {SLIDE_COUNT_MAX}]"
    )


def test_page_count_matches_actual_slides(deck):
    declared = deck["document"]["page_count"]
    actual = len(deck["slides"])
    assert declared == actual, (
        f"document.page_count={declared} disagrees with actual slide count={actual}"
    )


def test_each_slide_has_required_keys(deck):
    """Every slide must have an ``id`` and a ``layout`` so the renderer can dispatch."""
    missing: list[str] = []
    for idx, slide in enumerate(deck["slides"]):
        for key in REQUIRED_SLIDE_KEYS:
            if key not in slide:
                missing.append(f"slides[{idx}] missing {key} (slide id={slide.get('id')!r})")
    assert not missing, "\n".join(missing)


def test_slide_ids_are_unique(deck):
    """No duplicate slide ``id`` values (the renderer uses them as anchor keys)."""
    ids = [slide.get("id") for slide in deck["slides"]]
    assert len(ids) == len(set(ids)), f"duplicate slide ids: {ids}"


def test_slide_ids_are_kebab_with_two_digit_prefix(deck):
    """Slide ids follow the ``NN-name`` convention (e.g. ``01-cover``, ``14-ask``)."""
    import re

    pat = re.compile(r"^\d{2}-[a-z][a-z0-9-]*[a-z0-9]$")
    bad = [s["id"] for s in deck["slides"] if not pat.match(s["id"])]
    assert not bad, f"slides with non-kebab ids: {bad}"


def test_audience_includes_three_personas(deck):
    """I28 D-IH-28-1: audience = ENISA adviser + certifier-style + investor-like."""
    audience = deck["document"]["audience"]
    assert "enisa_adviser" in audience
    assert any("certif" in a for a in audience), f"missing certifier-style audience in {audience}"
    assert any("investor" in a for a in audience), f"missing investor-like audience in {audience}"


def test_language_is_spanish(deck):
    """Per D-IH-28-2 the canonical narrative SSOT is Spanish (``es``)."""
    assert deck["document"]["language"] == "es"
