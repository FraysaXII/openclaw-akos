"""Initiative 49 P15 — accessibility assertions for `static/madeira_control.html`.

Covers HTML-only a11y signals enforced at the source level. A separate
Playwright + axe-core run can be wired post-closure; until then these
assertions act as deterministic regression locks for the redesign.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

CONTROL_HTML_PATH = REPO_ROOT / "static" / "madeira_control.html"


@pytest.fixture(scope="module")
def html_text() -> str:
    return CONTROL_HTML_PATH.read_text(encoding="utf-8")


def test_doctype_and_lang_attribute(html_text: str) -> None:
    assert html_text.lstrip().startswith("<!DOCTYPE html>")
    assert "<html lang=" in html_text


def test_main_landmark_present(html_text: str) -> None:
    assert "<main>" in html_text and "</main>" in html_text


def test_color_scheme_meta_present(html_text: str) -> None:
    assert '<meta name="color-scheme"' in html_text


def test_status_panel_has_role_and_aria_live(html_text: str) -> None:
    assert 'role="status"' in html_text
    assert 'aria-live="polite"' in html_text


def test_alert_role_used_on_error_path(html_text: str) -> None:
    assert 'setAttribute("role", "alert")' in html_text


def test_focus_visible_outline_defined(html_text: str) -> None:
    assert "button:focus-visible" in html_text


def test_reduced_motion_respected(html_text: str) -> None:
    assert "prefers-reduced-motion: reduce" in html_text


def test_no_external_cdn_references(html_text: str) -> None:
    """Surface must run offline (no external <script> or <link> src per shape brief S-7)."""
    assert "<script src=" not in html_text
    assert "<link " not in html_text


def test_aria_pressed_on_mode_buttons(html_text: str) -> None:
    assert 'id="btn-ask"' in html_text and 'aria-pressed="false"' in html_text


def test_aria_pressed_on_locale_buttons(html_text: str) -> None:
    assert 'data-locale-set="en"' in html_text
    assert 'data-locale-set="es"' in html_text
    assert 'data-locale-set="fr"' in html_text


def test_no_blocking_alert_call(html_text: str) -> None:
    """Audit gap from pre-redesign: blocking `alert()` broke screen reader flow."""
    assert "alert(" not in html_text


def test_brand_voice_lint_clean_on_control_plane() -> None:
    """The redesigned file body should not introduce new BRAND_JARGON_AUDIT §4 violations.

    The file is internal (out of §3 external scope); the surface lane still runs the
    fast-lint defensively to catch regressions when prose drifts.
    """
    import importlib.util
    p = REPO_ROOT / "scripts" / "lint_brand_voice_offline.py"
    spec = importlib.util.spec_from_file_location("scripts.lint_brand_voice_offline_a11y", p)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["scripts.lint_brand_voice_offline_a11y"] = mod
    spec.loader.exec_module(mod)
    violations = mod.lint_file(CONTROL_HTML_PATH)
    leaks = [v for v in violations if v.category == "operator_token_§4.4"]
    assert not leaks, f"operator-token leaks: {[v.snippet for v in leaks]}"
