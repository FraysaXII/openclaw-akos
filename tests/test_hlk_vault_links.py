"""Tests for akos.hlk_vault_links."""

from __future__ import annotations

from akos.hlk_vault_links import resolve_markdown_target, validate_vault_internal_links
from akos.io import REPO_ROOT


def test_resolve_markdown_target_relative():
    src = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "index.md"
    target = "../compliance/PRECEDENCE.md"
    got = resolve_markdown_target(src, target, REPO_ROOT)
    assert got is not None
    assert got.name == "PRECEDENCE.md"


def test_validate_vault_internal_links_passes():
    errors = validate_vault_internal_links(REPO_ROOT)
    assert errors == [], errors


def test_resolve_skips_http():
    src = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "index.md"
    assert resolve_markdown_target(src, "https://example.com/a.md", REPO_ROOT) is None
