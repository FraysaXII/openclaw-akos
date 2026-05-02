"""Initiative 48 P1 (extended in P5) tests — HTML render scaffold.

Coverage:
- BRAND_CSS_VARS derived from BRAND_TOKENS_LIGHT (single SSOT; E9)
- section_to_html_details emits <details> with id="section-NN"
- default_open=True emits ` open` attribute; False omits
- Section header includes "Section N — Name"
- Body content is HTML-escaped (R-48-3 XSS hygiene; D-IH-48-I)
- No <script> tag ever embedded (no JS framework per D-IH-48-I)
- Brand tokens re-exported for caller convenience
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.dossier.html_render import (
    BRAND_CSS_VARS,
    BRAND_TOKENS_DARK,
    BRAND_TOKENS_LIGHT,
    section_to_html_details,
)


# ---------------------------------------------------------------------------
# BRAND_CSS_VARS derivation (E9 single SSOT)
# ---------------------------------------------------------------------------

def test_brand_css_vars_root_block() -> None:
    """BRAND_CSS_VARS opens with :root { and closes with }."""
    assert BRAND_CSS_VARS.startswith(":root {")
    assert BRAND_CSS_VARS.rstrip().endswith("}")


def test_brand_css_vars_includes_all_light_tokens() -> None:
    """Every BRAND_TOKENS_LIGHT key appears as a CSS variable."""
    for key, val in BRAND_TOKENS_LIGHT.items():
        css_name = f"--c-{key.replace('_', '-')}"
        assert css_name in BRAND_CSS_VARS, f"missing CSS var {css_name}"
        assert val in BRAND_CSS_VARS, f"missing token value {val}"


def test_brand_css_vars_kebab_case_naming() -> None:
    """CSS variables use --c-kebab-case (not --c-snake_case)."""
    matches = re.findall(r"--c-[a-z0-9-]+:", BRAND_CSS_VARS)
    for m in matches:
        # No underscores in CSS variable names
        assert "_" not in m


def test_brand_tokens_light_dark_re_exported() -> None:
    """html_render re-exports tokens for caller convenience (single SSOT)."""
    from akos.hlk_pdf_render import BRAND_TOKENS_LIGHT as src_light
    from akos.hlk_pdf_render import BRAND_TOKENS_DARK as src_dark
    assert BRAND_TOKENS_LIGHT == src_light
    assert BRAND_TOKENS_DARK == src_dark


# ---------------------------------------------------------------------------
# section_to_html_details
# ---------------------------------------------------------------------------

def test_section_to_html_details_basic_shape() -> None:
    out = section_to_html_details(
        section_id=1, name="Executive summary",
        markdown_body="hello", default_open=True,
    )
    assert '<details' in out
    assert 'id="section-01"' in out
    assert ' open' in out
    assert 'Section 1' in out
    assert 'Executive summary' in out
    assert '</details>' in out


def test_section_id_zero_padded_to_2_digits() -> None:
    out = section_to_html_details(
        section_id=3, name="X", markdown_body="y", default_open=False,
    )
    assert 'id="section-03"' in out


def test_default_open_false_omits_open_attr() -> None:
    out = section_to_html_details(
        section_id=12, name="Appendix", markdown_body="x", default_open=False,
    )
    assert ' open' not in out
    assert 'id="section-12"' in out


def test_default_open_true_includes_open_attr() -> None:
    out = section_to_html_details(
        section_id=1, name="X", markdown_body="x", default_open=True,
    )
    # The substring " open" must appear within the <details> opening tag
    details_open = out[: out.index(">") + 1]
    assert " open" in details_open


# ---------------------------------------------------------------------------
# HTML escape (R-48-3 XSS hygiene)
# ---------------------------------------------------------------------------

def test_markdown_body_html_escaped() -> None:
    """R-48-3: any HTML-injection-attempt characters in body are escaped."""
    out = section_to_html_details(
        section_id=1, name="X",
        markdown_body='<script>alert("x")</script>',
        default_open=False,
    )
    assert "<script>" not in out
    assert "&lt;script&gt;" in out
    assert "&quot;" in out


def test_section_name_html_escaped() -> None:
    """Section name is also escaped."""
    out = section_to_html_details(
        section_id=1, name='<bad>',
        markdown_body="ok", default_open=False,
    )
    assert "&lt;bad&gt;" in out
    assert "<bad>" not in out


def test_no_script_tag_ever_embedded() -> None:
    """D-IH-48-I: NO JS framework. Even if body contains escaped scripts they survive as text."""
    out = section_to_html_details(
        section_id=1, name="X", markdown_body="javascript:void(0)",
        default_open=False,
    )
    assert "<script" not in out
    # The literal javascript: substring may appear inside escaped <pre>; that's fine
    # because there's no JS execution surface.
