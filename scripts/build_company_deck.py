#!/usr/bin/env python3
"""Build the Holística company-dossier HTML preview deck.

Initiative 28 P3. Reads the slide structured data at
``docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck_slides.yaml``
and emits a self-contained HTML preview at
``docs/presentations/holistika-company-dossier/index.html``.

Design constraints:

- **Pure Python + PyYAML.** No npm / no React build tool. Keeps the workflow
  governed inside the repo and reproducible offline.
- **Self-contained output.** The emitted HTML inlines the deck stylesheet
  (``docs/presentations/holistika-company-dossier/styles.css``) so the deck
  is portable as a single file (operator can email it, drop it in a Drive,
  or print to PDF without needing the asset bundle).
- **Markdown SSOT wins for content.** The YAML is the single source of slide
  copy; the HTML is derived and re-emitted on every build.
- **Print-ready.** Each slide is a 1440×810 frame with ``page-break-after``
  rules so Chrome's "Save as PDF" produces a clean 14-page deck.
- **No imagery dependencies.** The cover monogram is rendered as text
  inside a small bordered tile to avoid pulling raster assets across folders.

Usage::

    py scripts/build_company_deck.py
    py scripts/build_company_deck.py --check-only   # validate YAML schema, do not write

Exit codes:
    0  HTML written (or validation passed in check-only mode)
    1  YAML schema violation (missing required fields, wrong slide count, etc.)
    2  IO / configuration error
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import html
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SLIDES_YAML = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "_assets"
    / "advops"
    / "PRJ-HOL-FOUNDING-2026"
    / "enisa_company_dossier"
    / "deck_slides.yaml"
)
OUT_DIR = REPO_ROOT / "docs" / "presentations" / "holistika-company-dossier"
OUT_HTML = OUT_DIR / "index.html"
STYLES_CSS = OUT_DIR / "styles.css"

REQUIRED_LAYOUTS = {
    "cover_hero",
    "section_opener",
    "solution_three_lines",
    "method_three_columns",
    "capability_grid",
    "product_spotlight",
    "market_icp",
    "business_model_today_tomorrow",
    "moat_pillars",
    "roadmap_three_phases",
    "enisa_fit_use_of_funds",
    "ask_signature",
}
EXPECTED_SLIDE_COUNT_RANGE = (12, 16)


# ----------------------------------------------------------------------------
# Schema validation
# ----------------------------------------------------------------------------


def _fail(msg: str) -> None:
    sys.stderr.write(f"build_company_deck: {msg}\n")
    raise SystemExit(1)


def validate_deck(data: dict[str, Any]) -> None:
    if "document" not in data:
        _fail("missing top-level 'document' key in deck_slides.yaml")
    if "slides" not in data or not isinstance(data["slides"], list):
        _fail("missing top-level 'slides' list")
    slides = data["slides"]
    n = len(slides)
    if not (EXPECTED_SLIDE_COUNT_RANGE[0] <= n <= EXPECTED_SLIDE_COUNT_RANGE[1]):
        _fail(
            f"slide count {n} outside expected range "
            f"{EXPECTED_SLIDE_COUNT_RANGE[0]}-{EXPECTED_SLIDE_COUNT_RANGE[1]}"
        )
    seen_ids: set[str] = set()
    for i, slide in enumerate(slides, start=1):
        for required in ("id", "layout"):
            if required not in slide:
                _fail(f"slide #{i} missing '{required}'")
        sid = slide["id"]
        if sid in seen_ids:
            _fail(f"duplicate slide id {sid!r}")
        seen_ids.add(sid)
        layout = slide["layout"]
        if layout not in REQUIRED_LAYOUTS:
            _fail(
                f"slide {sid!r}: unknown layout {layout!r} "
                f"(known: {sorted(REQUIRED_LAYOUTS)})"
            )
    # Forbidden tokens in any slide copy (jargon audit + TODO leak check)
    forbidden = (
        "TODO[OPERATOR]",
        "AKOS Strict",
        "ADVOPS",
        "TECHOPS",
        "FINOPS",
        "topic_",
        "ref_id",
        "GOI-",
        "POI-",
        "RBAC",
        "RLS",
        "pgvector",
        "Logfire",
        "Cohere",
        "BullMQ",
        "Cloudflare R2",
        "FastAPI",
        "Pydantic",
        "Polaris",
    )
    flat_text = json.dumps(slides, ensure_ascii=False)
    leaks = [tok for tok in forbidden if tok in flat_text]
    if leaks:
        _fail(
            "slide copy contains forbidden tokens (BRAND_JARGON_AUDIT.md §4): "
            f"{leaks}. External deck copy must stay jargon-free."
        )


# ----------------------------------------------------------------------------
# HTML helpers
# ----------------------------------------------------------------------------


def esc(s: str | None) -> str:
    return html.escape(s, quote=True) if s else ""


def _inline_paragraph(text: str | None) -> str:
    """Render a multi-paragraph string into <p> blocks."""
    if not text:
        return ""
    parts = [p.strip() for p in text.split("\n\n") if p.strip()]
    return "".join(f'<p class="body-paragraph">{esc(p)}</p>' for p in parts)


def _slide_footer(slide_index: int, total: int, doc_title: str) -> str:
    return (
        '<div class="slide-footer">'
        f"<span>{esc(doc_title)}</span>"
        f"<span>{slide_index} / {total}</span>"
        "</div>"
    )


# ----------------------------------------------------------------------------
# Layout renderers
# ----------------------------------------------------------------------------


def render_cover_hero(slide: dict[str, Any], idx: int, total: int, doc: dict[str, Any]) -> str:
    eyebrow = esc(slide.get("eyebrow"))
    title = esc(slide.get("title"))
    subtitle = esc(slide.get("subtitle"))
    footer = slide.get("footer", {}) or {}
    org = esc(footer.get("org") or "Holística Research")
    url = esc(footer.get("url") or "holistikaresearch.com")
    date = esc(footer.get("date") or _dt.datetime.now(_dt.UTC).strftime("%Y"))
    return (
        '<section class="slide slide-dark slide-cover">'
        '<div class="cover-grid"></div>'
        '<div class="slide-inner">'
        '<div class="brand-monogram">H</div>'
        f'<div class="cover-eyebrow">{eyebrow}</div>'
        f'<h1 class="cover-title">{title}</h1>'
        f'<p class="cover-subtitle">{subtitle}</p>'
        "</div>"
        '<div class="cover-strip">'
        f"<span>{org}</span>"
        f"<span>{url}</span>"
        f"<span>{date}</span>"
        "</div>"
        "</section>"
    )


def render_section_opener(slide: dict[str, Any], idx: int, total: int, doc: dict[str, Any]) -> str:
    number = esc(slide.get("section_number"))
    label = esc(slide.get("section_label"))
    headline = esc(slide.get("headline"))
    body = esc(slide.get("body"))
    return (
        '<section class="slide slide-dark slide-section">'
        '<div class="slide-inner">'
        f'<div class="section-number">{number}</div>'
        f'<div class="section-label">{label}</div>'
        f'<h1 class="section-headline">{headline}</h1>'
        f'<p class="section-body">{body}</p>'
        "</div>"
        "</section>"
    )


def render_solution_three_lines(slide: dict[str, Any], idx: int, total: int, doc: dict[str, Any]) -> str:
    eyebrow = esc(slide.get("eyebrow"))
    headline = esc(slide.get("headline"))
    cards = []
    for line in slide.get("lines", []):
        cards.append(
            '<div class="solution-card">'
            f'<h3 class="solution-title">{esc(line.get("title"))}</h3>'
            f'<p class="solution-body">{esc(line.get("body"))}</p>'
            "</div>"
        )
    return (
        '<section class="slide slide-light slide-body">'
        '<div class="slide-inner">'
        f'<div class="eyebrow">{eyebrow}</div>'
        f'<h1 class="body-headline">{headline}</h1>'
        f'<div class="solution-grid">{"".join(cards)}</div>'
        "</div>"
        + _slide_footer(idx, total, doc["title"])
        + "</section>"
    )


def render_method_three_columns(slide: dict[str, Any], idx: int, total: int, doc: dict[str, Any]) -> str:
    eyebrow = esc(slide.get("eyebrow"))
    headline = esc(slide.get("headline"))
    stripes = []
    cols = slide.get("columns", [])
    for i, col in enumerate(cols):
        amber_cls = " amber" if i == len(cols) - 1 else ""
        stripes.append(
            f'<div class="method-stripe{amber_cls}">'
            f'<div class="method-tag">{esc(col.get("tag"))}</div>'
            "<div>"
            f'<h3 class="method-stripe-title">{esc(col.get("title"))}</h3>'
            f'<p class="method-stripe-body">{esc(col.get("body"))}</p>'
            "</div>"
            "</div>"
        )
    return (
        '<section class="slide slide-light slide-body">'
        '<div class="slide-inner">'
        f'<div class="eyebrow">{eyebrow}</div>'
        f'<h1 class="body-headline">{headline}</h1>'
        f'<div class="method-stripes">{"".join(stripes)}</div>'
        "</div>"
        + _slide_footer(idx, total, doc["title"])
        + "</section>"
    )


def render_capability_grid(slide: dict[str, Any], idx: int, total: int, doc: dict[str, Any]) -> str:
    eyebrow = esc(slide.get("eyebrow"))
    headline = esc(slide.get("headline"))
    stat_grid_html = ""
    if slide.get("stat_grid"):
        stat_blocks = []
        for stat in slide["stat_grid"]:
            stat_blocks.append(
                '<div class="stat-block">'
                f'<div class="stat-num">{esc(str(stat.get("num")))}</div>'
                f'<div class="stat-label">{esc(stat.get("label"))}</div>'
                "</div>"
            )
        stat_grid_html = f'<div class="stat-grid">{"".join(stat_blocks)}</div>'
    cards = []
    for card in slide.get("cards", []):
        tag_html_parts = []
        tag_list = card.get("tags") or []
        for j, tg in enumerate(tag_list):
            cls = "tag-amber" if j == len(tag_list) - 1 else "tag"
            tag_html_parts.append(f'<span class="{cls}">{esc(tg)}</span>')
        cards.append(
            '<article class="capability-card">'
            '<div class="card-head">'
            f'<div class="card-order">{esc(card.get("order"))}</div>'
            f'<div class="card-category">{esc(card.get("category"))}</div>'
            f'<h3 class="card-title">{esc(card.get("title"))}</h3>'
            "</div>"
            f'<div class="card-body">{esc(card.get("outcome"))}</div>'
            f'<div class="card-tags">{"".join(tag_html_parts)}</div>'
            f'<div class="card-foot">{esc(card.get("footer"))}</div>'
            "</article>"
        )
    return (
        '<section class="slide slide-light slide-body">'
        '<div class="slide-inner">'
        f'<div class="eyebrow">{eyebrow}</div>'
        f'<h1 class="body-headline">{headline}</h1>'
        f"{stat_grid_html}"
        f'<div class="capability-grid">{"".join(cards)}</div>'
        "</div>"
        + _slide_footer(idx, total, doc["title"])
        + "</section>"
    )


def render_product_spotlight(slide: dict[str, Any], idx: int, total: int, doc: dict[str, Any]) -> str:
    eyebrow = esc(slide.get("eyebrow"))
    headline = esc(slide.get("headline"))
    body = _inline_paragraph(slide.get("body"))
    points = slide.get("proof_points") or []
    points_html = "".join(f'<div class="spotlight-point">{esc(p)}</div>' for p in points)
    why = esc(slide.get("why_it_matters"))
    return (
        '<section class="slide slide-light slide-body">'
        '<div class="slide-inner">'
        f'<div class="eyebrow">{eyebrow}</div>'
        f'<h1 class="body-headline">{headline}</h1>'
        '<div class="spotlight-grid">'
        f"<div>{body}<div class=\"pull-quote\">{why}</div></div>"
        f'<div class="spotlight-points">{points_html}</div>'
        "</div>"
        "</div>"
        + _slide_footer(idx, total, doc["title"])
        + "</section>"
    )


def render_market_icp(slide: dict[str, Any], idx: int, total: int, doc: dict[str, Any]) -> str:
    eyebrow = esc(slide.get("eyebrow"))
    headline = esc(slide.get("headline"))
    cards = []
    for icp in slide.get("icps", []):
        cards.append(
            '<div class="icp-card">'
            f'<h3 class="icp-title">{esc(icp.get("title"))}</h3>'
            f'<p class="icp-body">{esc(icp.get("body"))}</p>'
            f'<span class="icp-signal">{esc(icp.get("signal"))}</span>'
            "</div>"
        )
    return (
        '<section class="slide slide-light slide-body">'
        '<div class="slide-inner">'
        f'<div class="eyebrow">{eyebrow}</div>'
        f'<h1 class="body-headline">{headline}</h1>'
        f'<div class="icp-grid">{"".join(cards)}</div>'
        "</div>"
        + _slide_footer(idx, total, doc["title"])
        + "</section>"
    )


def render_business_model(slide: dict[str, Any], idx: int, total: int, doc: dict[str, Any]) -> str:
    eyebrow = esc(slide.get("eyebrow"))
    headline = esc(slide.get("headline"))
    rows = []
    for key, css_class in (
        ("today", ""),
        ("bridge", " amber"),
        ("tomorrow", ""),
    ):
        block = slide.get(key) or {}
        rows.append(
            f'<div class="bm-row{css_class}">'
            f'<div><span class="bm-tag">{esc(block.get("tag"))}</span></div>'
            "<div>"
            f'<h3 class="bm-title">{esc(block.get("title"))}</h3>'
            f'<p class="bm-body">{esc(block.get("body"))}</p>'
            "</div>"
            "</div>"
        )
    return (
        '<section class="slide slide-light slide-body">'
        '<div class="slide-inner">'
        f'<div class="eyebrow">{eyebrow}</div>'
        f'<h1 class="body-headline">{headline}</h1>'
        f'<div class="bm-stack">{"".join(rows)}</div>'
        "</div>"
        + _slide_footer(idx, total, doc["title"])
        + "</section>"
    )


def render_moat_pillars(slide: dict[str, Any], idx: int, total: int, doc: dict[str, Any]) -> str:
    eyebrow = esc(slide.get("eyebrow"))
    headline = esc(slide.get("headline"))
    cards = []
    for pillar in slide.get("pillars", []):
        cards.append(
            '<div class="moat-card">'
            f'<h3 class="moat-title">{esc(pillar.get("title"))}</h3>'
            f'<p class="moat-body">{esc(pillar.get("body"))}</p>'
            "</div>"
        )
    return (
        '<section class="slide slide-light slide-body">'
        '<div class="slide-inner">'
        f'<div class="eyebrow">{eyebrow}</div>'
        f'<h1 class="body-headline">{headline}</h1>'
        f'<div class="moat-grid">{"".join(cards)}</div>'
        "</div>"
        + _slide_footer(idx, total, doc["title"])
        + "</section>"
    )


def render_roadmap(slide: dict[str, Any], idx: int, total: int, doc: dict[str, Any]) -> str:
    eyebrow = esc(slide.get("eyebrow"))
    headline = esc(slide.get("headline"))
    windows = []
    for phase in slide.get("phases", []):
        deliverables = "".join(
            f"<li>{esc(d)}</li>" for d in (phase.get("deliverables") or [])
        )
        windows.append(
            '<div class="roadmap-window">'
            f'<span class="roadmap-window-window">{esc(phase.get("window"))}</span>'
            f'<h3 class="roadmap-window-title">{esc(phase.get("title"))}</h3>'
            f'<ul class="roadmap-window-deliverables">{deliverables}</ul>'
            "</div>"
        )
    return (
        '<section class="slide slide-light slide-body">'
        '<div class="slide-inner">'
        f'<div class="eyebrow">{eyebrow}</div>'
        f'<h1 class="body-headline">{headline}</h1>'
        '<div class="roadmap-track">'
        f'<div class="roadmap-grid">{"".join(windows)}</div>'
        "</div>"
        "</div>"
        + _slide_footer(idx, total, doc["title"])
        + "</section>"
    )


def render_enisa_fit(slide: dict[str, Any], idx: int, total: int, doc: dict[str, Any]) -> str:
    eyebrow = esc(slide.get("eyebrow"))
    headline = esc(slide.get("headline"))
    fit_cards = []
    for fp in slide.get("fit_points", []):
        fit_cards.append(
            '<div class="fit-card">'
            f'<h3 class="fit-title">{esc(fp.get("title"))}</h3>'
            f'<p class="fit-body">{esc(fp.get("body"))}</p>'
            "</div>"
        )
    use_of_funds = slide.get("use_of_funds") or {}
    funds_lines = "".join(
        f"<li>{esc(line)}</li>" for line in (use_of_funds.get("lines") or [])
    )
    return (
        '<section class="slide slide-light slide-body">'
        '<div class="slide-inner">'
        f'<div class="eyebrow">{eyebrow}</div>'
        f'<h1 class="body-headline">{headline}</h1>'
        f'<div class="enisa-fit">{"".join(fit_cards)}</div>'
        '<div class="use-of-funds">'
        f'<div class="use-of-funds-title">{esc(use_of_funds.get("title"))}</div>'
        f"<ul>{funds_lines}</ul>"
        "</div>"
        "</div>"
        + _slide_footer(idx, total, doc["title"])
        + "</section>"
    )


def render_ask_signature(slide: dict[str, Any], idx: int, total: int, doc: dict[str, Any]) -> str:
    eyebrow = esc(slide.get("eyebrow"))
    headline = esc(slide.get("headline"))
    asks_html = ""
    for i, line in enumerate(slide.get("ask_lines") or [], start=1):
        asks_html += (
            '<div class="ask-line">'
            f'<span class="ask-arrow">→</span>'
            f"<span>{esc(line)}</span>"
            "</div>"
        )
    closing = esc(slide.get("closing"))
    signature = esc(slide.get("signature"))
    contact_hint = esc(slide.get("contact_hint"))
    return (
        '<section class="slide slide-light slide-body">'
        '<div class="slide-inner">'
        f'<div class="eyebrow">{eyebrow}</div>'
        f'<h1 class="body-headline">{headline}</h1>'
        f'<div class="ask-lines">{asks_html}</div>'
        '<div class="ask-signature">'
        f'<span class="closing">{closing}</span>'
        f'<span class="signature">{signature}</span>'
        f'<span class="contact-hint">{contact_hint}</span>'
        "</div>"
        "</div>"
        + _slide_footer(idx, total, doc["title"])
        + "</section>"
    )


LAYOUT_RENDERERS = {
    "cover_hero": render_cover_hero,
    "section_opener": render_section_opener,
    "solution_three_lines": render_solution_three_lines,
    "method_three_columns": render_method_three_columns,
    "capability_grid": render_capability_grid,
    "product_spotlight": render_product_spotlight,
    "market_icp": render_market_icp,
    "business_model_today_tomorrow": render_business_model,
    "moat_pillars": render_moat_pillars,
    "roadmap_three_phases": render_roadmap,
    "enisa_fit_use_of_funds": render_enisa_fit,
    "ask_signature": render_ask_signature,
}


# ----------------------------------------------------------------------------
# Document assembly
# ----------------------------------------------------------------------------


def render_document(data: dict[str, Any], css: str, source_sha: str) -> str:
    document = data["document"]
    slides = data["slides"]
    n = len(slides)
    body_parts: list[str] = []
    for i, slide in enumerate(slides, start=1):
        renderer = LAYOUT_RENDERERS[slide["layout"]]
        body_parts.append(renderer(slide, i, n, document))
    body_html = "".join(body_parts)
    title = esc(document.get("title", "Holística Research — Dossier"))
    lang = esc(document.get("language", "es"))
    today = _dt.datetime.now(_dt.UTC).date().isoformat()
    header = (
        '<div class="deck-header">'
        f'<span>HOLÍSTICA · DOSSIER · {today}</span>'
        f'<span>SHA <strong>{source_sha[:12]}</strong></span>'
        "</div>"
    )
    return (
        f'<!DOCTYPE html><html lang="{lang}"><head>'
        '<meta charset="utf-8" />'
        '<meta name="viewport" content="width=1480" />'
        f"<title>{title}</title>"
        f"<style>{css}</style>"
        "</head>"
        '<body><main class="deck-container">'
        f"{header}"
        f"{body_html}"
        "</main></body></html>"
    )


# ----------------------------------------------------------------------------
# Entry
# ----------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Validate YAML schema and exit; do not write HTML.",
    )
    args = parser.parse_args(argv)

    if not SLIDES_YAML.is_file():
        sys.stderr.write(f"build_company_deck: missing {SLIDES_YAML}\n")
        return 2
    if not STYLES_CSS.is_file():
        sys.stderr.write(f"build_company_deck: missing {STYLES_CSS}\n")
        return 2

    try:
        import yaml  # type: ignore
    except ImportError:
        sys.stderr.write(
            "build_company_deck: pyyaml is required (py -m pip install pyyaml).\n"
        )
        return 2

    raw = SLIDES_YAML.read_text(encoding="utf-8")
    data = yaml.safe_load(raw)
    validate_deck(data)

    if args.check_only:
        print(
            f"build_company_deck: schema OK — {len(data['slides'])} slides, "
            f"layouts {sorted({s['layout'] for s in data['slides']})}"
        )
        return 0

    css = STYLES_CSS.read_text(encoding="utf-8")
    source_sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    html_doc = render_document(data, css, source_sha)
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(html_doc, encoding="utf-8")
    out_sha = hashlib.sha256(html_doc.encode("utf-8")).hexdigest()
    print(
        f"build_company_deck: wrote {OUT_HTML.relative_to(REPO_ROOT)} "
        f"(slides={len(data['slides'])}, "
        f"yaml_sha256={source_sha[:16]}..., html_sha256={out_sha[:16]}...)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
