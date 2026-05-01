"""Initiative 31 P1 — Tests for the language-frontmatter validator + audience exception."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOP_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Marketing" / "Brand" / "SOP-HLK_LOCALISATION_001.md"  # I32 P7 (D-IH-32-E) relocation
BRAND_FR_STUB = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Marketing" / "Brand" / "BRAND_FRENCH_PATTERNS.md"
VALIDATOR = REPO_ROOT / "scripts" / "validate_hlk_language_frontmatter.py"
MADEIRA_MD = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Operations" / "PMO" / "business-strategy" / "MADEIRA_PLATFORM.md"
GOVERNANCE_MOAT_MD = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Operations" / "PMO" / "business-strategy" / "GOVERNANCE_MOAT.md"


def _read_lang(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^language:\s*(\w+)\s*$", text, re.MULTILINE)
    return m.group(1) if m else None


def test_localisation_sop_exists_and_is_english():
    assert SOP_PATH.is_file(), f"missing {SOP_PATH}"
    assert _read_lang(SOP_PATH) == "en"


def test_brand_french_patterns_stub_exists():
    assert BRAND_FR_STUB.is_file(), f"missing {BRAND_FR_STUB}"
    text = BRAND_FR_STUB.read_text(encoding="utf-8")
    assert "status: stub" in text, "BRAND_FRENCH_PATTERNS.md must declare status: stub until first FR deliverable lands"
    assert _read_lang(BRAND_FR_STUB) == "en", "the stub itself is authored in EN (it codifies FR rules in EN)"


def test_validator_script_passes_on_canonical_surfaces():
    proc = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=str(REPO_ROOT),
        capture_output=True, text=True, timeout=60,
    )
    assert proc.returncode == 0, (
        f"validate_hlk_language_frontmatter rc={proc.returncode}\n"
        f"stdout={proc.stdout}\nstderr={proc.stderr}"
    )
    assert "PASS" in proc.stdout


def test_audience_canonical_exception_madeira_is_es():
    """D-IH-31-E: MADEIRA_PLATFORM.md is the textbook audience-canonical exception
    (Spanish content that feeds Spanish slides exclusively). Must stay `es`.
    """
    assert MADEIRA_MD.is_file()
    assert _read_lang(MADEIRA_MD) == "es", (
        "MADEIRA_PLATFORM.md must declare language: es per D-IH-31-E"
    )


def test_audience_canonical_exception_governance_moat_is_es():
    """D-IH-31-E: GOVERNANCE_MOAT.md is the second audience-canonical exception."""
    assert GOVERNANCE_MOAT_MD.is_file()
    assert _read_lang(GOVERNANCE_MOAT_MD) == "es", (
        "GOVERNANCE_MOAT.md must declare language: es per D-IH-31-E"
    )


def test_outbound_brief_fr_variant_declares_derived_from():
    """The FR template is the first exercise of the locale-derivation pipeline:
    it must declare derived_from and language: fr."""
    fr_path = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Operations" / "PMO" / "sourcing-briefs" / "TEMPLATE_OUTBOUND_BRIEF_fr.md"
    assert fr_path.is_file()
    text = fr_path.read_text(encoding="utf-8")
    assert "language: fr" in text
    assert "derived_from:" in text


def test_outbound_brief_en_canonical_declares_derived_locales():
    en_path = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Operations" / "PMO" / "sourcing-briefs" / "TEMPLATE_OUTBOUND_BRIEF_en.md"
    assert en_path.is_file()
    text = en_path.read_text(encoding="utf-8")
    assert "language: en" in text
    assert "derived_locales:" in text
