"""Initiative 28 P6 — assert deck SSOT contains zero forbidden tokens.

Closes the I28 P6 verification matrix entry "tests/test_deck_jargon.py" (per
[`28-investor-style-company-dossier/master-roadmap.md`](../docs/wip/planning/28-investor-style-company-dossier/master-roadmap.md)
§8). Reuses ``scripts/lint_brand_voice_offline.py`` (the canonical
``BRAND_JARGON_AUDIT.md`` §4 token list shipped in I49 P12) so the deck never
drifts from the brand-canonical forbidden-tokens contract.

The Spanish narrative SSOT mirror is also asserted clean, since I28 D-IH-28-1
treats `deck_story_es.md` and `deck_slides.yaml` as a single content surface
that must be jargon-free in source.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LINTER_PATH = REPO_ROOT / "scripts" / "lint_brand_voice_offline.py"

DECK_SSOT_DIR = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "_assets" / "advops" / "PRJ-HOL-FOUNDING-2026" / "enisa_company_dossier"

DECK_SSOT_FILES = (
    DECK_SSOT_DIR / "deck_slides.yaml",
    DECK_SSOT_DIR / "deck_story_es.md",
    DECK_SSOT_DIR / "cover_email_company_dossier_es.md",
)


def _load_linter():
    """Import ``scripts/lint_brand_voice_offline.py`` for in-process scanning."""
    spec = importlib.util.spec_from_file_location("lint_brand_voice_offline", LINTER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["lint_brand_voice_offline"] = module
    spec.loader.exec_module(module)
    return module


def test_deck_ssot_dir_present():
    """Sanity: the I28 deck SSOT folder must exist (P0/P1 deliverable)."""
    assert DECK_SSOT_DIR.is_dir(), f"deck SSOT dir missing: {DECK_SSOT_DIR}"


def test_deck_ssot_files_present():
    """All three deck SSOT files must be present (P1 narrative + P1 yaml + P5 cover email)."""
    for path in DECK_SSOT_FILES:
        assert path.is_file(), f"deck SSOT file missing: {path}"


def test_deck_ssot_passes_brand_jargon_audit():
    """Run BRAND_JARGON_AUDIT §4 forbidden-token scan against every deck SSOT file."""
    linter = _load_linter()
    compiled = linter._compile()
    violations: list[str] = []
    for path in DECK_SSOT_FILES:
        if not path.is_file():
            continue
        for v in linter.lint_file(path, compiled=compiled):
            violations.append(v.to_line())
    assert not violations, "BRAND_JARGON_AUDIT §4 violations in deck SSOT:\n" + "\n".join(violations)
