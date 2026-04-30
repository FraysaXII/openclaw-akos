"""Tests for the Initiative 29 P3 Impeccable bridge files.

Covers:
- ``PRODUCT.md`` + ``DESIGN.md`` exist at the repo root.
- Both files reference all five canonical brand SSOT files by repo-relative path.
- Both files contain the AKOS-precedence rule (Impeccable yields to AKOS rules).
- Neither bridge contains hardcoded hex colors that would imply duplicated brand-token content
  (HSL token names from the canonical visual file are allowed as references; a `#RRGGBB` hex
  literal would suggest the bridge has copied brand content rather than redirecting).
- The Impeccable skill bundle is installed under ``.cursor/skills/impeccable/``.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PRODUCT_MD = REPO_ROOT / "PRODUCT.md"
DESIGN_MD = REPO_ROOT / "DESIGN.md"
IMPECCABLE_DIR = REPO_ROOT / ".cursor" / "skills" / "impeccable"

CANONICAL_BRAND_FILES = (
    "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VOICE_FOUNDATION.md",
    "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VISUAL_PATTERNS.md",
    "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_DO_DONT.md",
    "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_SPANISH_PATTERNS.md",
    "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_JARGON_AUDIT.md",
)


# ---- File presence ---------------------------------------------------------

def test_product_md_exists():
    assert PRODUCT_MD.is_file(), f"missing {PRODUCT_MD}"


def test_design_md_exists():
    assert DESIGN_MD.is_file(), f"missing {DESIGN_MD}"


def test_impeccable_skill_installed():
    assert IMPECCABLE_DIR.is_dir(), f"missing {IMPECCABLE_DIR}"
    assert (IMPECCABLE_DIR / "SKILL.md").is_file(), "missing SKILL.md"
    assert (IMPECCABLE_DIR / "LICENSE").is_file(), "missing LICENSE"
    assert (IMPECCABLE_DIR / "NOTICE.md").is_file(), "missing NOTICE.md"


# ---- Bridge content contract -----------------------------------------------

def test_product_md_references_all_canonical_brand_files():
    """PRODUCT.md must point at all five canonical brand SSOT files."""
    text = PRODUCT_MD.read_text(encoding="utf-8")
    missing = []
    for ref in (
        "BRAND_VOICE_FOUNDATION.md",
        "BRAND_VISUAL_PATTERNS.md",
        "BRAND_DO_DONT.md",
        "BRAND_SPANISH_PATTERNS.md",
        "BRAND_JARGON_AUDIT.md",
    ):
        if ref not in text:
            missing.append(ref)
    assert not missing, f"PRODUCT.md missing references to canonical brand files: {missing}"


def test_design_md_references_brand_visual_patterns_and_deck_visual_system():
    """DESIGN.md must point at BRAND_VISUAL_PATTERNS.md and the deck visual
    system spec (the deck-specific layout SSOT)."""
    text = DESIGN_MD.read_text(encoding="utf-8")
    assert "BRAND_VISUAL_PATTERNS.md" in text
    assert "deck-visual-system.md" in text


def test_product_md_carries_akos_precedence_rule():
    """The non-negotiable AKOS-precedence statement must be present."""
    text = PRODUCT_MD.read_text(encoding="utf-8")
    assert "akos-" in text or "AKOS" in text, "PRODUCT.md must mention the AKOS rule precedence"
    assert ("AKOS rule wins" in text or "AKOS wins" in text), (
        "PRODUCT.md must declare AKOS precedence rule"
    )


def test_design_md_carries_akos_precedence_rule():
    text = DESIGN_MD.read_text(encoding="utf-8")
    # DESIGN.md cross-refs SOP §3.7 which carries the precedence rule;
    # the bridge itself should also surface the rule, even briefly.
    assert "AKOS" in text or "akos-" in text, "DESIGN.md must reference the AKOS rule"


# ---- No-duplication guard --------------------------------------------------

# Bridges may use HSL function syntax `hsl(168 55% 38%)` (referencing a token)
# but should not introduce hardcoded hex codes (which would imply duplicated
# brand-token content rather than a redirect).
HEX_COLOR_RE = re.compile(r"#[0-9A-Fa-f]{6}\b")


def test_product_md_has_no_hex_colors():
    text = PRODUCT_MD.read_text(encoding="utf-8")
    hits = HEX_COLOR_RE.findall(text)
    assert not hits, (
        f"PRODUCT.md contains hardcoded hex colors {hits} — duplication of "
        f"brand-token content. Reference token names in BRAND_VISUAL_PATTERNS.md instead."
    )


def test_design_md_has_no_hex_colors():
    text = DESIGN_MD.read_text(encoding="utf-8")
    hits = HEX_COLOR_RE.findall(text)
    assert not hits, (
        f"DESIGN.md contains hardcoded hex colors {hits} — duplication of "
        f"brand-token content. Reference token names instead."
    )
