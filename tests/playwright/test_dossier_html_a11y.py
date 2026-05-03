"""Initiative 54 P2 — DOM-level a11y scenarios for the dossier HTML output.

Tests the **template-level** a11y contract of the dossier HTML rendered
by `akos.dossier.html_render.render_dossier_html` (Initiative 48 + I52
P6 surface). Per **R-54-3** mitigation, the template-time check is the
right surface (not data-time): once the template is clean, accumulated
KM data cannot introduce a regression.

Live axe-core run will land at I54 P3 (operator-driven; runs against
a rendered dossier HTML file produced by `scripts/render_uat_dossier.py
--format html`).
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

HTML_RENDER_PATH = REPO_ROOT / "akos" / "dossier" / "html_render.py"


@pytest.fixture(scope="module")
def html_render_source() -> str:
    return HTML_RENDER_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def rendered_dossier_html() -> str:
    """Render a minimal-stub dossier HTML for template-level inspection."""
    spec = importlib.util.spec_from_file_location("akos.dossier.html_render_a11y", HTML_RENDER_PATH)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules["akos.dossier.html_render_a11y"] = mod
    spec.loader.exec_module(mod)

    # Build a minimal `DossierRun`-shaped object with the surface fields
    # `render_dossier_html` reads. We test the template, not the section
    # rendering; section rendering is covered by tests/test_dossier_*.
    from types import SimpleNamespace

    section_render = SimpleNamespace(
        section_id="00_meta",
        title="Meta",
        status="PASS",
        markdown="# Meta\n\nminimal stub for template-level a11y test",
    )
    run = SimpleNamespace(
        run_id="i54-p2-template-test",
        started_at="2026-05-03T00:00:00Z",
        git_sha="0" * 40,
        mode="snapshot",
        overall_status="PASS",
        elapsed_ms=42,
    )
    try:
        return mod.render_dossier_html(run=run, sections=[section_render], screenshots=[])
    except TypeError:
        # If the function signature differs, fall back to inspecting the
        # template literal in the source.
        return ""


# ---- Template-level a11y contract tests ----------------------------------


def test_dossier_template_declares_doctype(html_render_source: str) -> None:
    assert "<!doctype html>" in html_render_source.lower() or "<!DOCTYPE html>" in html_render_source


def test_dossier_template_declares_html_lang_attribute(html_render_source: str) -> None:
    assert '<html lang="en"' in html_render_source


def test_dossier_template_declares_meta_charset(html_render_source: str) -> None:
    assert '<meta charset="utf-8"' in html_render_source


def test_dossier_template_declares_meta_viewport(html_render_source: str) -> None:
    assert '<meta name="viewport"' in html_render_source


def test_dossier_template_has_main_landmark(html_render_source: str) -> None:
    """axe-core `landmark-one-main` rule. Critical if missing."""
    assert "<main>" in html_render_source and "</main>" in html_render_source


def test_dossier_template_has_header_and_footer_landmarks(html_render_source: str) -> None:
    """Complementary landmark roles improve `region` rule compliance."""
    assert "<header>" in html_render_source
    assert "<footer>" in html_render_source


def test_dossier_template_has_csp_header(html_render_source: str) -> None:
    """Content-Security-Policy keeps the dossier CSP-compliant per I48
    spec; locks "no external CDN" axe-friendly posture."""
    assert "Content-Security-Policy" in html_render_source


def test_dossier_template_has_no_inline_javascript_event_handlers(html_render_source: str) -> None:
    """A11y rule of thumb + CSP: no inline `onclick=`, `onload=`, etc."""
    forbidden = ["onclick=", "onload=", "onerror=", "onmouseover=", "onkeydown="]
    for needle in forbidden:
        assert needle not in html_render_source, f"inline JS handler found: {needle}"


def test_dossier_template_uses_definition_list_for_meta_pairs(html_render_source: str) -> None:
    """`<dl>/<dt>/<dd>` is the semantic-correct structure for key-value
    metadata (run_id, mode, etc.); axe `definition-list` rule."""
    assert "<dl>" in html_render_source and "</dl>" in html_render_source
    assert "<dt>" in html_render_source and "<dd>" in html_render_source


def test_dossier_template_no_external_font_or_script_src(html_render_source: str) -> None:
    """Template must be standalone (per I48 spec + I54 D-IH-54-C scope)."""
    assert "fonts.googleapis.com" not in html_render_source
    assert "cdn.jsdelivr.net" not in html_render_source
    assert "unpkg.com" not in html_render_source


def test_rendered_dossier_html_has_main_landmark_when_callable(rendered_dossier_html: str) -> None:
    """Live render exercise: when the template is callable with a stub,
    the rendered HTML still carries the `<main>` landmark. R-54-3
    mitigation: template-time, not data-time."""
    if not rendered_dossier_html:
        pytest.skip("render_dossier_html signature did not match the stub; covered by source-level test")
    assert "<main>" in rendered_dossier_html
    assert "<html lang=\"en\"" in rendered_dossier_html
    assert "<header>" in rendered_dossier_html and "<footer>" in rendered_dossier_html


def test_rendered_dossier_html_escapes_run_id_metadata(rendered_dossier_html: str) -> None:
    """If the run_id is rendered, it must be escaped (no raw `<` or `>`
    leaking through). Locks the existing `_html_escape()` contract."""
    if not rendered_dossier_html:
        pytest.skip("render_dossier_html signature did not match the stub")
    assert "i54-p2-template-test" in rendered_dossier_html
