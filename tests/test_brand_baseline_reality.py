"""Tests for akos/brand_baseline_reality.py per I76 P3 Lane 3 refactor.

The new module lifts the BBR scan helpers out of
``scripts/validate_brand_baseline_reality_drift.py`` so other surfaces
(notably ``scripts/madeira_personality_check.py``) can call the same
scanner without reaching into a private ``_underscore`` symbol.

These tests lock the public API:

- ``scan_text("clean text")`` returns an empty list.
- ``scan_text("counterparty leaked")`` returns one hit with the canonical
  token attached.
- ``scan_text(text, tokens=[custom])`` accepts a custom token list.
- ``scan_text(text, strip_frontmatter=True)`` blanks the YAML frontmatter
  region before scanning while preserving line-number fidelity.
- ``load_canonical_tokens()`` falls back to ``DEFAULT_INTERNAL_TOKENS``
  when the matrix file is missing or unparseable.
- ``BaselineHit.file`` is ``None`` for in-memory ``scan_text`` calls.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from akos.brand_baseline_reality import (
    BaselineHit,
    DEFAULT_INTERNAL_TOKENS,
    InternalToken,
    load_canonical_tokens,
    scan_text,
)


pytestmark = pytest.mark.brand


# ---------------------------------------------------------------------------
# Empty / clean cases
# ---------------------------------------------------------------------------


def test_scan_clean_text_returns_empty_list() -> None:
    """Text with no internal-register tokens emits zero hits."""
    assert scan_text("This is perfectly fine external prose.") == []


def test_scan_empty_string_returns_empty_list() -> None:
    assert scan_text("") == []


def test_scan_no_double_quotes_no_hits() -> None:
    assert scan_text("Plain words about research and clients.") == []


# ---------------------------------------------------------------------------
# Single-token leak detection
# ---------------------------------------------------------------------------


def test_scan_detects_single_internal_token() -> None:
    hits = scan_text("The counterparty was difficult to elicit from.")
    tokens_found = {hit.token.token for hit in hits}
    assert "counterparty" in tokens_found


def test_scan_returns_hit_with_line_number() -> None:
    body = "Line one is fine.\nThe counterparty leaked here.\nLine three is fine."
    hits = scan_text(body)
    assert hits
    counterparty_hits = [h for h in hits if h.token.token == "counterparty"]
    assert counterparty_hits
    assert counterparty_hits[0].line == 2


def test_scan_returns_hit_with_snippet() -> None:
    body = "We started with elicitation of the audience baseline."
    hits = scan_text(body)
    assert hits
    elicitation_hits = [h for h in hits if h.token.token == "elicitation"]
    assert elicitation_hits
    assert "elicitation" in elicitation_hits[0].snippet


def test_scan_case_insensitive_match() -> None:
    """Internal tokens match case-insensitively via word-boundary regex."""
    hits = scan_text("Counterparty profiling was incomplete.")
    assert any(h.token.token == "counterparty" for h in hits)


def test_scan_word_boundary_does_not_partial_match() -> None:
    """The regex uses word boundaries; substrings inside other words don't trigger."""
    hits = scan_text("Encounterparty is not a real word.")
    assert not any(h.token.token == "counterparty" for h in hits)


# ---------------------------------------------------------------------------
# Multi-token detection
# ---------------------------------------------------------------------------


def test_scan_detects_multiple_distinct_tokens() -> None:
    body = "We did intelligence collection then reliability grading."
    hits = scan_text(body)
    tokens_found = {h.token.token for h in hits}
    assert "intelligence collection" in tokens_found
    assert "reliability grading" in tokens_found


def test_scan_detects_prj_hol_prefix() -> None:
    body = "Engagement PRJ-HOL-FOUNDING-2026 progresses well."
    hits = scan_text(body)
    assert any(h.token.token == "PRJ-HOL-" for h in hits)


# ---------------------------------------------------------------------------
# Custom token list override
# ---------------------------------------------------------------------------


def test_scan_with_custom_token_list_works() -> None:
    """Caller can pass a custom token list (e.g. for personality-check tuning)."""
    import re

    custom = [
        InternalToken(
            token="forbidden_word",
            pattern=re.compile(r"\bforbidden_word\b", re.IGNORECASE),
        )
    ]
    hits = scan_text("This contains forbidden_word inline.", tokens=custom)
    assert len(hits) == 1
    assert hits[0].token.token == "forbidden_word"


def test_scan_with_empty_token_list_returns_no_hits() -> None:
    hits = scan_text("counterparty word here", tokens=[])
    assert hits == []


def test_scan_with_custom_tokens_does_not_use_canonical() -> None:
    """When tokens= is passed, canonical tokens are NOT also scanned."""
    import re

    custom = [
        InternalToken(token="otherword", pattern=re.compile(r"\botherword\b", re.IGNORECASE))
    ]
    hits = scan_text("counterparty mentioned but otherword too.", tokens=custom)
    tokens_found = {h.token.token for h in hits}
    assert "counterparty" not in tokens_found
    assert "otherword" in tokens_found


# ---------------------------------------------------------------------------
# Frontmatter stripping
# ---------------------------------------------------------------------------


def test_scan_strip_frontmatter_blanks_metadata_block() -> None:
    """With strip_frontmatter=True, internal tokens in YAML metadata don't leak."""
    body = """---
program_id: PRJ-HOL-FOUNDING-2026
counterparty_role: investor
---

This is the body prose. It is clean.
"""
    hits = scan_text(body, strip_frontmatter=True)
    assert hits == []


def test_scan_strip_frontmatter_preserves_line_numbers() -> None:
    """Frontmatter is blanked, not deleted -- body line numbers stay correct."""
    body = """---
program_id: PRJ-HOL-FOUNDING-2026
---

Line 5 is fine.
The counterparty appears here at line 6.
"""
    hits = scan_text(body, strip_frontmatter=True)
    counterparty_hits = [h for h in hits if h.token.token == "counterparty"]
    assert counterparty_hits
    assert counterparty_hits[0].line == 6


def test_scan_without_strip_frontmatter_catches_metadata_leak() -> None:
    """Default scan_text (strip_frontmatter=False) DOES see frontmatter tokens."""
    body = """---
program_id: PRJ-HOL-FOUNDING-2026
---

Body is clean.
"""
    hits = scan_text(body, strip_frontmatter=False)
    assert any(h.token.token == "PRJ-HOL-" for h in hits)


def test_scan_strip_frontmatter_no_match_when_no_frontmatter() -> None:
    """If text has no frontmatter, strip_frontmatter is a no-op."""
    body = "Just body prose with counterparty leaking."
    hits = scan_text(body, strip_frontmatter=True)
    assert any(h.token.token == "counterparty" for h in hits)


# ---------------------------------------------------------------------------
# load_canonical_tokens() + fallback behaviour
# ---------------------------------------------------------------------------


def test_load_canonical_tokens_returns_list_of_internal_tokens() -> None:
    tokens = load_canonical_tokens()
    assert tokens
    for tok in tokens:
        assert isinstance(tok, InternalToken)


def test_load_canonical_tokens_fallback_to_default_when_matrix_missing(tmp_path: Path) -> None:
    """When the matrix path doesn't exist, fall back to DEFAULT_INTERNAL_TOKENS."""
    fake = tmp_path / "does-not-exist.md"
    tokens = load_canonical_tokens(matrix_path=fake)
    token_strings = {t.token for t in tokens}
    for default_tok in DEFAULT_INTERNAL_TOKENS:
        assert default_tok in token_strings


def test_load_canonical_tokens_fallback_when_section_unparseable(tmp_path: Path) -> None:
    """Matrix exists but lacks the §3 table -- fall back."""
    weird = tmp_path / "weird.md"
    weird.write_text("# Header\n\nNo translation rules section here.\n", encoding="utf-8")
    tokens = load_canonical_tokens(matrix_path=weird)
    token_strings = {t.token for t in tokens}
    for default_tok in DEFAULT_INTERNAL_TOKENS:
        assert default_tok in token_strings


def test_default_internal_tokens_includes_humint_vocabulary() -> None:
    """Sanity check: the fallback list mirrors the matrix §3 documented set."""
    expected = {
        "counterparty",
        "elicitation",
        "reliability grading",
        "intelligence collection",
        "intelligence report",
        "approach techniques",
        "baseline reality assessment",
        "PRJ-HOL-",
    }
    assert set(DEFAULT_INTERNAL_TOKENS) == expected


# ---------------------------------------------------------------------------
# BaselineHit shape
# ---------------------------------------------------------------------------


def test_baseline_hit_file_is_none_for_in_memory_scan() -> None:
    """Calling scan_text without file= produces hits with file=None."""
    hits = scan_text("counterparty leaked")
    assert hits
    assert all(h.file is None for h in hits)


def test_baseline_hit_file_populated_when_path_passed() -> None:
    fake_path = Path("/tmp/example.md")
    hits = scan_text("counterparty leaked here", file=fake_path)
    assert hits
    assert all(h.file == fake_path for h in hits)


def test_baseline_hit_carries_full_token_object() -> None:
    """BaselineHit.token is an InternalToken (with both .token and .pattern)."""
    hits = scan_text("counterparty leaked")
    assert hits
    hit = hits[0]
    assert isinstance(hit.token, InternalToken)
    assert hit.token.token == "counterparty"
    assert hit.token.pattern is not None
