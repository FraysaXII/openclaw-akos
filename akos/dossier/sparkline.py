"""Initiative 48 P1 (extended in P7) — inline SVG sparkline generator.

Deterministic SVG generator for trend lines per Section 11 of dossier-section-spec.md.
NO JavaScript / external CDN / Vega dependency (R-48-3 mitigation; D-IH-48-I).

Public API:
- ``render_sparkline_svg(values, *, label, width, height, ...) -> str``
- ``INSUFFICIENT_DATA_PLACEHOLDER`` constant (when <2 data points)

Output: ``<svg>...</svg>`` string suitable for inline embedding in markdown
(GitHub-flavoured markdown supports inline SVG) AND inline HTML
(no <img src=> reference; no XSS surface).

Determinism: same input -> same SVG bytes (sorted attributes, fixed precision).
"""

from __future__ import annotations

from typing import Sequence

INSUFFICIENT_DATA_PLACEHOLDER = (
    "> _INSUFFICIENT-DATA: sparkline requires >=2 data points; emit on next run._"
)

# Brand tokens reused from akos.hlk_pdf_render.BRAND_TOKENS_LIGHT (HSL strings).
# Inlined here to avoid circular import; sync-safe because brand drift test
# (tests/test_render_dossier.py::test_brand_tokens_light_match_pattern_doc)
# enforces source-of-truth alignment with BRAND_VISUAL_PATTERNS.md.
SPARKLINE_STROKE_COLOR = "hsl(168 55% 38%)"  # accent_primary (teal)
SPARKLINE_AXIS_COLOR = "hsl(220 8% 88%)"      # border (light grey)
SPARKLINE_TEXT_COLOR = "hsl(220 8% 42%)"      # muted_foreground


def render_sparkline_svg(
    values: Sequence[float | int],
    *,
    label: str = "",
    width: int = 180,
    height: int = 40,
    stroke_color: str | None = None,
    axis_color: str | None = None,
    show_endpoints: bool = True,
) -> str:
    """Render a deterministic inline SVG sparkline.

    When ``len(values) < 2`` returns ``INSUFFICIENT_DATA_PLACEHOLDER``.

    Otherwise emits a fixed-width SVG line chart with:
    - bottom axis line
    - polyline through all data points (normalized to height-aware viewport)
    - optional endpoint dots (start + end) when ``show_endpoints=True``
    - optional ``<title>`` element with label + first/last values for accessibility
    """
    if len(values) < 2:
        return INSUFFICIENT_DATA_PLACEHOLDER

    stroke = stroke_color or SPARKLINE_STROKE_COLOR
    axis = axis_color or SPARKLINE_AXIS_COLOR

    floats = [float(v) for v in values]
    vmin = min(floats)
    vmax = max(floats)
    span = vmax - vmin
    if span == 0.0:
        # Flat line: render at vertical mid-line.
        normalized = [0.5] * len(floats)
    else:
        normalized = [(v - vmin) / span for v in floats]

    # Padding inside viewport
    pad_x = 4
    pad_y = 4
    inner_w = width - 2 * pad_x
    inner_h = height - 2 * pad_y

    n = len(floats)
    # Compute x,y for each point
    points: list[tuple[float, float]] = []
    for i, n_val in enumerate(normalized):
        x = pad_x + (i / (n - 1)) * inner_w
        # Invert y so high values appear at top
        y = pad_y + (1.0 - n_val) * inner_h
        points.append((round(x, 2), round(y, 2)))

    polyline_pts = " ".join(f"{x},{y}" for x, y in points)

    title_text = ""
    if label:
        title_text = (
            f"<title>{_xml_escape(label)} (first={_fmt(floats[0])}, "
            f"last={_fmt(floats[-1])}, n={n})</title>"
        )

    endpoints = ""
    if show_endpoints:
        x0, y0 = points[0]
        x1, y1 = points[-1]
        endpoints = (
            f'<circle cx="{x0}" cy="{y0}" r="2" fill="{stroke}"/>'
            f'<circle cx="{x1}" cy="{y1}" r="2.5" fill="{stroke}"/>'
        )

    axis_y = height - pad_y
    axis_line = (
        f'<line x1="{pad_x}" y1="{axis_y}" x2="{width - pad_x}" y2="{axis_y}" '
        f'stroke="{axis}" stroke-width="0.5"/>'
    )

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" '
        f'aria-label="{_xml_escape(label or "sparkline")}">'
        f'{title_text}'
        f'{axis_line}'
        f'<polyline points="{polyline_pts}" fill="none" '
        f'stroke="{stroke}" stroke-width="1.5" stroke-linecap="round" '
        f'stroke-linejoin="round"/>'
        f'{endpoints}'
        f'</svg>'
    )
    return svg


def _xml_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _fmt(value: float) -> str:
    """Format a float for sparkline title text. Trim trailing zeros for readability."""
    if value == int(value):
        return str(int(value))
    return f"{value:.3f}".rstrip("0").rstrip(".")
