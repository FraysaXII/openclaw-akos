"""Initiative 48 P1 (extended in P5) — markdown -> HTML with brand CSS.

Standalone HTML output: NO JavaScript / NO external CDN / NO remote fonts
(D-IH-48-I; R-48-3 mitigation). Brand CSS variables derived from the same
BRAND_TOKENS_LIGHT/DARK constants used by `akos.hlk_pdf_render.render_pdf_branded`
(E9 single-source brand tokens; drift caught by existing test
`tests/test_render_dossier.py::test_brand_tokens_light_match_pattern_doc`).

Public API (P1):
- ``section_to_html_details(section_id, name, markdown_body, default_open) -> str``
- ``BRAND_CSS_VARS`` derived constant

P5 will extend with full ``render_dossier_html(dossier_run) -> str`` end-to-end
function that wraps everything in ``<html><head><style>...</style></head><body>``.
"""

from __future__ import annotations

# Reuse brand tokens from akos.hlk_pdf_render to avoid duplication (E9).
# Importing here is safe (no circular dep; render_pdf_branded does not import
# anything from akos.dossier).
from akos.hlk_pdf_render import BRAND_TOKENS_DARK, BRAND_TOKENS_LIGHT


def _brand_css_var_block(prefix: str = "--c-") -> str:
    """Render :root { --c-token: value; ... } CSS block from BRAND_TOKENS_LIGHT.

    Single SSOT: the Python tokens (already drift-checked vs BRAND_VISUAL_PATTERNS.md).
    """
    rules = []
    for key, val in BRAND_TOKENS_LIGHT.items():
        rules.append(f"  {prefix}{key.replace('_', '-')}: {val};")
    return ":root {\n" + "\n".join(rules) + "\n}"


BRAND_CSS_VARS = _brand_css_var_block()


def section_to_html_details(
    *,
    section_id: int,
    name: str,
    markdown_body: str,
    default_open: bool,
) -> str:
    """Wrap a section's markdown body in a brand-styled <details> element.

    P1 minimal: body is rendered verbatim inside <pre> (no markdown->HTML
    conversion yet). P5 will replace with proper markdown library invocation.

    Default-open vs collapsed per the section's class attribute (D-IH-48-I +
    dossier-section-spec.md per-section default state).
    """
    open_attr = " open" if default_open else ""
    safe_name = _html_escape(name)
    safe_body = _html_escape(markdown_body)
    return (
        f'<details id="section-{section_id:02d}"{open_attr} class="dossier-section">\n'
        f'  <summary><strong>Section {section_id}</strong> &mdash; {safe_name}</summary>\n'
        f'  <div class="dossier-section-body">\n'
        f'    <pre>{safe_body}</pre>\n'
        f'  </div>\n'
        f'</details>'
    )


def _html_escape(text: str) -> str:
    """Minimal HTML escape (no JS framework; CSP-compatible)."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


__all__ = [
    "BRAND_CSS_VARS",
    "BRAND_TOKENS_LIGHT",
    "BRAND_TOKENS_DARK",
    "section_to_html_details",
]
