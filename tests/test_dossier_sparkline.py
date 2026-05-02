"""Initiative 48 P1 + P7 tests — sparkline SVG generator.

Coverage:
- INSUFFICIENT_DATA_PLACEHOLDER returned when len(values) < 2
- Valid SVG XML emitted when len(values) >= 2
- Deterministic across 2 runs with same input (sha256 stable)
- Brand stroke color matches BRAND_TOKENS_LIGHT.accent_primary (single SSOT; E9)
- Flat-line input (vmin == vmax) renders without ZeroDivisionError
- Polyline points count matches input length
- ARIA label present for accessibility
- Endpoint dots toggleable
- XML escape on label (XSS hygiene; R-48-3)
"""

from __future__ import annotations

import hashlib
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.dossier.sparkline import (
    INSUFFICIENT_DATA_PLACEHOLDER,
    SPARKLINE_AXIS_COLOR,
    SPARKLINE_STROKE_COLOR,
    render_sparkline_svg,
)


# ---------------------------------------------------------------------------
# INSUFFICIENT-DATA placeholder
# ---------------------------------------------------------------------------

def test_insufficient_data_placeholder_for_zero_values() -> None:
    out = render_sparkline_svg([])
    assert out == INSUFFICIENT_DATA_PLACEHOLDER


def test_insufficient_data_placeholder_for_one_value() -> None:
    out = render_sparkline_svg([42])
    assert out == INSUFFICIENT_DATA_PLACEHOLDER


def test_insufficient_data_placeholder_text() -> None:
    """Placeholder text must explain the 2-point minimum."""
    assert ">=2" in INSUFFICIENT_DATA_PLACEHOLDER
    assert "INSUFFICIENT-DATA" in INSUFFICIENT_DATA_PLACEHOLDER


# ---------------------------------------------------------------------------
# Valid SVG emission
# ---------------------------------------------------------------------------

def test_two_value_input_emits_svg() -> None:
    out = render_sparkline_svg([1.0, 2.0], label="test")
    assert out.startswith("<svg")
    assert out.endswith("</svg>")


def test_emitted_svg_is_valid_xml() -> None:
    """Sparkline SVG must parse as XML (no malformed tags / unescaped chars)."""
    out = render_sparkline_svg([1, 2, 3, 4, 5], label="parses-cleanly")
    root = ET.fromstring(out)
    assert root.tag.endswith("svg")


def test_polyline_points_count_matches_input() -> None:
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    out = render_sparkline_svg(values, label="ten")
    m = re.search(r'<polyline points="([^"]+)"', out)
    assert m
    points = m.group(1).split()
    assert len(points) == len(values)


def test_aria_label_present_for_accessibility() -> None:
    out = render_sparkline_svg([1, 2, 3], label="my-metric")
    assert 'role="img"' in out
    assert 'aria-label="my-metric"' in out


def test_title_element_includes_first_last_n() -> None:
    out = render_sparkline_svg([1.0, 2.0, 3.0], label="trend")
    assert "<title>" in out
    assert "first=1" in out
    assert "last=3" in out
    assert "n=3" in out


def test_endpoint_dots_emitted_by_default() -> None:
    out = render_sparkline_svg([1, 2, 3])
    # Two <circle> elements (start + end)
    assert out.count("<circle") == 2


def test_endpoint_dots_can_be_disabled() -> None:
    out = render_sparkline_svg([1, 2, 3], show_endpoints=False)
    assert "<circle" not in out


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------

def test_sparkline_deterministic_across_two_runs() -> None:
    out1 = render_sparkline_svg([1.0, 2.0, 3.0, 2.5, 4.0], label="repro")
    out2 = render_sparkline_svg([1.0, 2.0, 3.0, 2.5, 4.0], label="repro")
    assert out1 == out2
    assert hashlib.sha256(out1.encode()).hexdigest() == hashlib.sha256(out2.encode()).hexdigest()


# ---------------------------------------------------------------------------
# Brand token reuse (E9 single-source brand tokens)
# ---------------------------------------------------------------------------

def test_default_stroke_color_is_brand_accent_primary() -> None:
    """SPARKLINE_STROKE_COLOR matches BRAND_TOKENS_LIGHT.accent_primary."""
    from akos.hlk_pdf_render import BRAND_TOKENS_LIGHT
    assert SPARKLINE_STROKE_COLOR == BRAND_TOKENS_LIGHT["accent_primary"]


def test_default_axis_color_is_brand_border() -> None:
    from akos.hlk_pdf_render import BRAND_TOKENS_LIGHT
    assert SPARKLINE_AXIS_COLOR == BRAND_TOKENS_LIGHT["border"]


def test_caller_can_override_stroke_color() -> None:
    out = render_sparkline_svg([1, 2, 3], stroke_color="hsl(0 100% 50%)")
    assert "hsl(0 100% 50%)" in out


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_flat_line_input_does_not_crash() -> None:
    """vmin == vmax: must render without ZeroDivisionError; flat at mid-line."""
    out = render_sparkline_svg([5.0, 5.0, 5.0], label="flat")
    assert out.startswith("<svg")


def test_negative_values_render() -> None:
    out = render_sparkline_svg([-3.0, -1.0, -2.0])
    assert out.startswith("<svg")


def test_xml_escape_on_label_xss_hygiene() -> None:
    """R-48-3: label with HTML-injection-attempt characters must be escaped."""
    out = render_sparkline_svg([1, 2], label='<script>alert("x")</script>')
    assert "<script>" not in out
    assert "&lt;script&gt;" in out


def test_width_height_propagate_to_svg_attrs() -> None:
    out = render_sparkline_svg([1, 2, 3], width=300, height=80)
    assert 'width="300"' in out
    assert 'height="80"' in out
    assert 'viewBox="0 0 300 80"' in out
