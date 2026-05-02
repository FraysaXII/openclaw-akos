"""Initiative 48 P5 — markdown -> HTML with brand CSS (full render).

Standalone HTML output: NO JavaScript / NO external CDN / NO remote fonts
(D-IH-48-I; R-48-3 mitigation). Brand CSS variables derived from the same
BRAND_TOKENS_LIGHT/DARK constants used by `akos.hlk_pdf_render.render_pdf_branded`
(E9 single-source brand tokens; drift caught by existing test
`tests/test_render_dossier.py::test_brand_tokens_light_match_pattern_doc`).

Public API:
- ``render_dossier_html(run) -> str`` (P5 end-to-end)
- ``section_to_html_details(section_id, name, markdown_body, default_open, markdown_lib) -> str``
- ``BRAND_CSS_VARS`` derived constant
- ``DOSSIER_HTML_CSS`` full stylesheet block

P5 uses the existing `markdown` library (already in repo deps via I22 P6
PDF chain) for proper markdown -> HTML conversion (tables, code blocks,
nested lists, inline SVG passthrough). NO new dependency added.
"""

from __future__ import annotations

from typing import Any

# Reuse brand tokens from akos.hlk_pdf_render to avoid duplication (E9).
from akos.hlk_pdf_render import BRAND_TOKENS_DARK, BRAND_TOKENS_LIGHT, MD_EXTENSIONS

try:
    import markdown as _md_lib  # type: ignore
except ImportError:  # pragma: no cover (markdown is in repo deps)
    _md_lib = None


def _brand_css_var_block(prefix: str = "--c-") -> str:
    """Render :root { --c-token: value; ... } CSS block from BRAND_TOKENS_LIGHT.

    Single SSOT: the Python tokens (already drift-checked vs BRAND_VISUAL_PATTERNS.md).
    """
    rules = []
    for key, val in BRAND_TOKENS_LIGHT.items():
        rules.append(f"  {prefix}{key.replace('_', '-')}: {val};")
    return ":root {\n" + "\n".join(rules) + "\n}"


BRAND_CSS_VARS = _brand_css_var_block()

# P5 full stylesheet: brand CSS variables + Inter typography + collapsible
# <details> + sparkline-friendly inline SVG support + table styling +
# dark-mode media query (CSS-only; no JS toggle).
DOSSIER_HTML_CSS = f"""
{BRAND_CSS_VARS}

* {{ box-sizing: border-box; }}
html {{ font-size: 16px; }}
body {{
  font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  background: var(--c-background); color: var(--c-foreground);
  max-width: 960px; margin: 2rem auto; padding: 0 1.25rem; line-height: 1.65;
}}
h1, h2, h3, h4 {{ color: var(--c-foreground); margin-top: 1.5em; line-height: 1.3; }}
h1 {{
  color: var(--c-accent-primary); font-size: 2.25rem; font-weight: 700;
  border-bottom: 2px solid var(--c-accent-primary); padding-bottom: 0.5rem;
  margin-top: 0;
}}
h2 {{ font-size: 1.5rem; font-weight: 600; }}
h3 {{ font-size: 1.15rem; font-weight: 600; color: var(--c-muted-foreground); }}

a {{ color: var(--c-accent-primary); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}

code {{ font-family: 'Fira Code', 'Cascadia Code', Consolas, 'Courier New', monospace;
  background: var(--c-secondary); padding: 0.1rem 0.35rem; border-radius: 0.25rem;
  font-size: 0.9em; }}
pre code {{ background: none; padding: 0; }}
pre {{ background: var(--c-secondary); padding: 0.75rem 1rem; border-radius: 0.5rem;
  border: 1px solid var(--c-border); overflow-x: auto; }}

table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: 0.95em; }}
th, td {{ border: 1px solid var(--c-border); padding: 0.45rem 0.7rem; text-align: left; }}
th {{ background: var(--c-secondary); font-weight: 600; }}
tr:nth-child(2n) td {{ background: rgba(0, 0, 0, 0.015); }}

blockquote {{ border-left: 4px solid var(--c-accent-secondary); margin: 1rem 0;
  padding: 0.5rem 1rem; background: var(--c-card); color: var(--c-muted-foreground); }}

ul, ol {{ padding-left: 1.5rem; }}
li {{ margin: 0.3rem 0; }}

details.dossier-section {{
  background: var(--c-card); border: 1px solid var(--c-border);
  border-radius: 0.5rem; padding: 1rem 1.25rem; margin: 1rem 0;
}}
details.dossier-section > summary {{
  cursor: pointer; font-size: 1.1rem; font-weight: 500;
  color: var(--c-foreground); list-style: none; padding: 0.25rem 0;
}}
details.dossier-section > summary::-webkit-details-marker {{ display: none; }}
details.dossier-section > summary::before {{
  content: '\\25B8'; display: inline-block; margin-right: 0.5rem;
  color: var(--c-accent-primary); transition: transform 0.15s;
}}
details.dossier-section[open] > summary::before {{ transform: rotate(90deg); }}
details.dossier-section > summary > strong {{ color: var(--c-accent-primary); }}
details.dossier-section[open] {{ border-color: var(--c-accent-primary); }}

.dossier-section-body {{ margin-top: 0.75rem; padding-top: 0.75rem;
  border-top: 1px solid var(--c-border); }}
.dossier-section-body > h2 {{ display: none; }}  /* Section H2 already in <summary> */

header {{ background: linear-gradient(135deg, var(--c-card) 0%, var(--c-secondary) 100%);
  border: 1px solid var(--c-border); border-radius: 0.5rem;
  padding: 1.5rem; margin-bottom: 1.5rem; }}
header dl {{ display: grid; grid-template-columns: max-content 1fr;
  gap: 0.4rem 1.5rem; margin: 0; }}
header dt {{ color: var(--c-muted-foreground); font-weight: 500; }}
header dd {{ margin: 0; }}

footer {{ margin-top: 3rem; padding-top: 1.5rem;
  border-top: 1px solid var(--c-border);
  color: var(--c-muted-foreground); font-size: 0.85rem; text-align: center; }}

svg {{ max-width: 100%; height: auto; }}

@media (prefers-color-scheme: dark) {{
  :root {{ --c-background: hsl(220 16% 7%); --c-foreground: hsl(210 15% 90%);
    --c-card: hsl(220 14% 10%); --c-secondary: hsl(220 8% 15%);
    --c-border: hsl(220 8% 20%); --c-muted-foreground: hsl(220 8% 60%); }}
}}

@media print {{
  details.dossier-section {{ break-inside: avoid; }}
  details {{ open: ''; }}
}}
"""


def section_to_html_details(
    *,
    section_id: int,
    name: str,
    markdown_body: str,
    default_open: bool,
    use_markdown_lib: bool = True,
) -> str:
    """Wrap a section's markdown body in a brand-styled <details> element.

    P5: when ``use_markdown_lib=True`` (default) AND the markdown library is
    available, convert markdown_body via the same MD_EXTENSIONS that the PDF
    chain uses (tables, fenced_code, sane_lists, attr_list, toc). Inline SVG
    (sparklines from akos.dossier.sparkline) passes through unchanged.

    P1 fallback: when ``use_markdown_lib=False`` OR markdown lib unavailable,
    body is wrapped in <pre> + HTML-escaped (no markdown rendering).
    """
    open_attr = " open" if default_open else ""
    safe_name = _html_escape(name)
    body_html = _render_section_body(markdown_body, use_markdown_lib=use_markdown_lib)
    return (
        f'<details id="section-{section_id:02d}"{open_attr} class="dossier-section">\n'
        f'  <summary><strong>Section {section_id}</strong> &mdash; {safe_name}</summary>\n'
        f'  <div class="dossier-section-body">\n'
        f'{body_html}\n'
        f'  </div>\n'
        f'</details>'
    )


def _render_section_body(markdown_body: str, *, use_markdown_lib: bool = True) -> str:
    """Convert a section's markdown body to HTML.

    P5: prefers markdown library (with MD_EXTENSIONS) for proper rendering;
    falls back to escaped <pre> when library unavailable or use_markdown_lib=False.
    Inline SVG fragments embedded in the markdown (sparklines) pass through
    unchanged because the markdown library treats them as raw HTML.
    """
    if use_markdown_lib and _md_lib is not None:
        # Strip the section header line ("## Section N — Name") since the
        # <summary> already shows it; otherwise it duplicates inside the body.
        body_text = _strip_section_header(markdown_body)
        html = _md_lib.markdown(body_text, extensions=MD_EXTENSIONS)
        return html
    # Fallback: P1-style escaped <pre>
    return f'    <pre>{_html_escape(markdown_body)}</pre>'


def _strip_section_header(markdown_body: str) -> str:
    """Remove the leading `## Section N — Name` line (already in <summary>)."""
    lines = markdown_body.splitlines()
    if lines and lines[0].startswith("## Section "):
        # Skip header + blank line that usually follows
        idx = 1
        while idx < len(lines) and not lines[idx].strip():
            idx += 1
        return "\n".join(lines[idx:])
    return markdown_body


def render_dossier_html(run: Any) -> str:
    """Render the full dossier as a standalone HTML document (P5 end-to-end).

    Per D-IH-48-I + R-48-3: NO JS / NO external CDN / NO remote fonts.
    Standalone-file invariant: the operator can email this HTML to anyone
    without security review (no XSS surface; no third-party assets).

    Brand CSS variables derived from BRAND_TOKENS_LIGHT (single SSOT; E9).
    Per-section <details> default-open per the dossier-section-spec.md state.
    """
    # Defer import to avoid circular dep at module load
    from akos.dossier.sections import SECTION_CLASSES

    body_parts = []
    for r in sorted(run.section_results, key=lambda x: x.section_id):
        cls = next((c for c in SECTION_CLASSES if c.section_id == r.section_id), None)
        default_open = cls.default_open_html if cls else False
        body_parts.append(section_to_html_details(
            section_id=r.section_id, name=r.name,
            markdown_body=r.markdown, default_open=default_open,
        ))
    body = "\n".join(body_parts)

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'self' 'unsafe-inline'">
<title>AKOS Operator UAT Dossier &mdash; {_html_escape(run.run_id)}</title>
<style>
{DOSSIER_HTML_CSS}
</style>
</head>
<body>
<header>
<h1>AKOS Operator UAT Dossier</h1>
<dl>
<dt>run_id</dt><dd><code>{_html_escape(run.run_id)}</code></dd>
<dt>started_at</dt><dd>{_html_escape(run.started_at)}</dd>
<dt>git_sha</dt><dd><code>{_html_escape(run.git_sha)}</code></dd>
<dt>mode</dt><dd><strong>{_html_escape(run.mode)}</strong></dd>
<dt>overall_status</dt><dd><strong>{_html_escape(run.overall_status)}</strong></dd>
<dt>elapsed_ms</dt><dd>{run.elapsed_ms}</dd>
</dl>
</header>
<main>
{body}
</main>
<footer>
Generated by <code>py scripts/render_uat_dossier.py --mode {_html_escape(run.mode)}</code>
&nbsp;&middot;&nbsp; Initiative 48 &nbsp;&middot;&nbsp; Standalone (no JS / no CDN / no external fonts)
</footer>
</body>
</html>
"""


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
    "DOSSIER_HTML_CSS",
    "render_dossier_html",
    "section_to_html_details",
]
