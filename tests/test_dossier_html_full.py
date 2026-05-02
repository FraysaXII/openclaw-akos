"""Initiative 48 P5 tests — standalone HTML mode end-to-end (full render).

Coverage:
- render_dossier_html(run) returns a complete <!doctype html>...</html> doc
- DOSSIER_HTML_CSS includes brand CSS variables + Inter typography + dark-mode media query
- markdown library is invoked for section bodies (tables / code / lists render as HTML)
- Section header strip: ## Section N — Name removed from body (already in <summary>)
- Standalone-file invariant: no external CDN / no <script> / no remote font URL
- CSP meta tag present
- Dark-mode media query present (CSS-only; no JS toggle)
- Print styles present (avoid section break-inside)
- Inline SVG sparkline passes through markdown library unchanged
- All 12 sections present in output (default_open varies per section)
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.dossier.html_render import (
    BRAND_CSS_VARS,
    DOSSIER_HTML_CSS,
    _render_section_body,
    _strip_section_header,
    render_dossier_html,
    section_to_html_details,
)
from akos.dossier.run import DossierRun, DossierSectionResult


# ---------------------------------------------------------------------------
# DOSSIER_HTML_CSS contents
# ---------------------------------------------------------------------------

def test_dossier_html_css_includes_brand_vars() -> None:
    assert "--c-accent-primary" in DOSSIER_HTML_CSS
    assert "--c-foreground" in DOSSIER_HTML_CSS
    assert "--c-background" in DOSSIER_HTML_CSS


def test_dossier_html_css_includes_inter_typography() -> None:
    assert "Inter" in DOSSIER_HTML_CSS


def test_dossier_html_css_has_dark_mode_media_query() -> None:
    """CSS-only dark mode (no JS toggle)."""
    assert "prefers-color-scheme: dark" in DOSSIER_HTML_CSS


def test_dossier_html_css_has_print_styles() -> None:
    """Print stylesheet ensures break-inside: avoid for sections."""
    assert "@media print" in DOSSIER_HTML_CSS
    assert "break-inside: avoid" in DOSSIER_HTML_CSS


def test_dossier_html_css_styles_collapsible_details() -> None:
    """details.dossier-section is the styling hook."""
    assert "details.dossier-section" in DOSSIER_HTML_CSS


def test_dossier_html_css_overrides_section_h2_to_hide() -> None:
    """Section H2 inside <details> body is hidden because it's already in <summary>."""
    assert ".dossier-section-body > h2" in DOSSIER_HTML_CSS
    assert "display: none" in DOSSIER_HTML_CSS


# ---------------------------------------------------------------------------
# _strip_section_header
# ---------------------------------------------------------------------------

def test_strip_section_header_removes_h2_and_blank() -> None:
    body = "## Section 1 — Executive summary\n\nbody text\n"
    out = _strip_section_header(body)
    assert "## Section 1" not in out
    assert "body text" in out


def test_strip_section_header_no_op_when_no_header() -> None:
    body = "just body text\nno header\n"
    out = _strip_section_header(body)
    assert out == body


# ---------------------------------------------------------------------------
# _render_section_body
# ---------------------------------------------------------------------------

def test_render_section_body_uses_markdown_lib_for_lists() -> None:
    body = "## Section 1 — Test\n\n- item 1\n- item 2\n"
    out = _render_section_body(body, use_markdown_lib=True)
    assert "<ul>" in out
    assert "<li>item 1</li>" in out


def test_render_section_body_renders_tables() -> None:
    body = "## Section 2 — T\n\n| a | b |\n|:--|:--|\n| 1 | 2 |\n"
    out = _render_section_body(body, use_markdown_lib=True)
    assert "<table>" in out
    assert "<th" in out


def test_render_section_body_passes_through_inline_svg() -> None:
    """Sparklines (inline SVG) embedded in markdown must pass through unchanged."""
    body = "## Section 11 — Trend\n\n<svg><polyline points='0,0 1,1'/></svg>\n"
    out = _render_section_body(body, use_markdown_lib=True)
    assert "<svg>" in out
    assert "<polyline" in out


def test_render_section_body_fallback_when_lib_disabled() -> None:
    body = "## Section X — Y\n\nbody\n"
    out = _render_section_body(body, use_markdown_lib=False)
    assert "<pre>" in out


# ---------------------------------------------------------------------------
# section_to_html_details with markdown lib
# ---------------------------------------------------------------------------

def test_section_to_html_details_default_uses_markdown_lib() -> None:
    out = section_to_html_details(
        section_id=1, name="X",
        markdown_body="## Section 1 — X\n\n- a\n- b\n",
        default_open=True,
    )
    assert "<ul>" in out
    assert "<li>a</li>" in out


def test_section_to_html_details_strips_duplicate_section_header() -> None:
    """Body's '## Section N — Name' is removed (already in <summary>)."""
    out = section_to_html_details(
        section_id=3, name="X",
        markdown_body="## Section 3 — X\n\nbody\n",
        default_open=False,
    )
    # Body should not contain a duplicate H2 header
    body_part = out.split("dossier-section-body")[1]
    assert "<h2>Section 3" not in body_part


# ---------------------------------------------------------------------------
# render_dossier_html end-to-end (P5 entry point)
# ---------------------------------------------------------------------------

def _build_test_run() -> DossierRun:
    run = DossierRun(run_id="test-html-run", git_sha="abc123")
    for sid in range(1, 13):
        run.add(DossierSectionResult(
            section_id=sid, name=f"Test Section {sid}",
            status="PASS",
            markdown=f"## Section {sid} — Test Section {sid}\n\n- item {sid}\n",
        ))
    return run


def test_render_dossier_html_returns_full_doctype() -> None:
    run = _build_test_run()
    out = render_dossier_html(run)
    assert out.startswith("<!doctype html>")
    assert "</html>" in out


def test_render_dossier_html_includes_run_id_in_title_and_header() -> None:
    run = _build_test_run()
    out = render_dossier_html(run)
    assert "test-html-run" in out


def test_render_dossier_html_no_external_references() -> None:
    """R-48-3 + D-IH-48-I: standalone-file invariant. No CDN / JS / external fonts."""
    run = _build_test_run()
    out = render_dossier_html(run)
    for forbidden in ("<script", "https://cdn.", "https://fonts.googleapis",
                      '<link rel="stylesheet"', "src=\"http"):
        assert forbidden not in out, f"standalone-file invariant violated: {forbidden!r} in HTML"


def test_render_dossier_html_includes_csp_meta() -> None:
    """CSP guard limits XSS damage even if internal markdown slips."""
    run = _build_test_run()
    out = render_dossier_html(run)
    assert "Content-Security-Policy" in out
    assert "default-src 'self' 'unsafe-inline'" in out


def test_render_dossier_html_includes_all_12_sections() -> None:
    run = _build_test_run()
    out = render_dossier_html(run)
    for sid in range(1, 13):
        assert f"id=\"section-{sid:02d}\"" in out


def test_render_dossier_html_includes_brand_css() -> None:
    run = _build_test_run()
    out = render_dossier_html(run)
    assert "--c-accent-primary" in out
    assert "Inter" in out
    assert "@media (prefers-color-scheme: dark)" in out


def test_render_dossier_html_includes_footer() -> None:
    run = _build_test_run()
    out = render_dossier_html(run)
    assert "<footer>" in out
    assert "Initiative 48" in out


# ---------------------------------------------------------------------------
# Cumulative HTML size sanity
# ---------------------------------------------------------------------------

def test_render_dossier_html_size_reasonable() -> None:
    """HTML output should be reasonable size (5KB-200KB for typical 12-section dossier)."""
    run = _build_test_run()
    out = render_dossier_html(run)
    assert 5000 < len(out) < 200000, f"unexpected HTML size: {len(out)} chars"
