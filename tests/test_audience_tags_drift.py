"""Tests for ``scripts/validate_audience_tags.py`` (I85 P2 / D-IH-85-A/B/D).

Mirrors the I85 P1 validator-test discipline: structural sanity + canonical
example PASS + targeted unit tests for parser + J-OP exclusion rule.
"""
from __future__ import annotations

import sys
import textwrap
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import validate_audience_tags as drift  # noqa: E402


@pytest.mark.brand
def test_canonical_scan_passes() -> None:
    """Repo scan PASS at this commit — only BASELINE_REALITY.md has audience: frontmatter."""
    assert drift.validate() == 0


@pytest.mark.brand
def test_extract_frontmatter_audience_single() -> None:
    """Single-string ``audience: J-IN`` parses to ['J-IN']."""
    text = "---\naudience: J-IN\nstatus: active\n---\n\n# Body\n"
    assert drift._extract_frontmatter_audience(text) == ["J-IN"]


@pytest.mark.brand
def test_extract_frontmatter_audience_list_inline() -> None:
    """List ``audience: [J-IN, J-CU]`` parses to ['J-IN', 'J-CU']."""
    text = "---\naudience: [J-IN, J-CU, J-PT]\n---\n\n# Body\n"
    assert drift._extract_frontmatter_audience(text) == ["J-IN", "J-CU", "J-PT"]


@pytest.mark.brand
def test_extract_frontmatter_no_audience_field() -> None:
    """Frontmatter without ``audience:`` returns None."""
    text = "---\nstatus: active\nlast_review: 2026-05-16\n---\n\n# Body\n"
    assert drift._extract_frontmatter_audience(text) is None


@pytest.mark.brand
def test_extract_frontmatter_no_frontmatter() -> None:
    """Body-only file (no frontmatter) returns None."""
    text = "# Body only\n\nSome content.\n"
    assert drift._extract_frontmatter_audience(text) is None


@pytest.mark.brand
def test_valid_codes_loaded_from_registry() -> None:
    """``_load_valid_audience_codes`` returns the 8 seeded codes."""
    valid_codes, register_sides = drift._load_valid_audience_codes()
    expected = {"J-IN", "J-CU", "J-PT", "J-ENISA", "J-AD", "J-RC", "J-CO", "J-OP"}
    assert expected.issubset(valid_codes)
    assert register_sides["J-OP"] == "internal"
    assert register_sides["J-IN"] == "external"


@pytest.mark.brand
def test_unknown_audience_code_fails_validation(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Synthetic markdown with unknown J-* code triggers FAIL."""
    fake_file = tmp_path / "fake-surface.md"
    fake_file.write_text(
        textwrap.dedent(
            """\
            ---
            audience: [J-INVALID]
            ---

            # Body
            """
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(drift, "_iter_target_files", lambda: [fake_file])
    monkeypatch.setattr(drift, "REPO_ROOT", tmp_path)

    assert drift.validate() == 1


@pytest.mark.brand
def test_j_op_composed_with_external_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """J-OP cannot be composed with any other audience (D-IH-85-D)."""
    fake_file = tmp_path / "operator-mixed.md"
    fake_file.write_text(
        textwrap.dedent(
            """\
            ---
            audience: [J-OP, J-IN]
            ---

            # Body
            """
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(drift, "_iter_target_files", lambda: [fake_file])
    monkeypatch.setattr(drift, "REPO_ROOT", tmp_path)

    assert drift.validate() == 1


@pytest.mark.brand
def test_j_op_alone_passes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """J-OP alone is valid (operator-only file like BASELINE_REALITY.md)."""
    fake_file = tmp_path / "operator-only.md"
    fake_file.write_text(
        textwrap.dedent(
            """\
            ---
            audience: [J-OP]
            ---

            # Body
            """
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(drift, "_iter_target_files", lambda: [fake_file])
    monkeypatch.setattr(drift, "REPO_ROOT", tmp_path)

    assert drift.validate() == 0


@pytest.mark.brand
def test_multi_audience_external_list_passes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Three-audience external list passes."""
    fake_file = tmp_path / "services.md"
    fake_file.write_text(
        textwrap.dedent(
            """\
            ---
            audience: [J-CU, J-PT, J-IN]
            ---

            # Body
            """
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(drift, "_iter_target_files", lambda: [fake_file])
    monkeypatch.setattr(drift, "REPO_ROOT", tmp_path)

    assert drift.validate() == 0
