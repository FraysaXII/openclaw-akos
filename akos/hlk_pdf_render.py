"""Shared HLK PDF + DOCX rendering helpers.

Extracted from ``scripts/export_adviser_handoff.py`` so both that script and
``scripts/compose_adviser_message.py`` (Initiative 24 P4) share one canonical
Markdown -> PDF / DOCX rendering chain. CSS styling, font selection, and
fallback ordering are unchanged from the original Initiative 22 P6 / D-IH-4
implementation.

Public functions:

- ``render_pdf(md_text, out_path, *, source_label="hlk_pdf_render") -> int``
  Renders Markdown to PDF using the WeasyPrint -> fpdf2 -> pandoc fallback
  chain. Returns 0 on success (including the soft-success path when only the
  markdown sidecar can be written). Returns non-zero only when an explicit
  renderer command (e.g. pandoc) fails its own subprocess.

- ``render_pdf_branded(md_text, out_path, *, profile="dossier", program_id=None,
  discipline=None, issue_date=None, source_label="hlk_pdf_render") -> int``
  Initiative 27 P1. Renders Markdown to a brand-aligned PDF using the live
  Holistika tokens captured in ``BRAND_VISUAL_PATTERNS.md`` (teal
  ``hsl(168 55% 38%)``, amber ``hsl(38 80% 50%)``, warm-slate dark hero band,
  cream-warm light body, Inter typography, 0.5rem radius). Adds a dark cover
  hero band with the Holistika monogram and a body styled per the print
  variant rules. Falls through the same WeasyPrint -> fpdf2 -> pandoc chain
  as ``render_pdf`` so it degrades gracefully on systems without WeasyPrint.

- ``render_docx(md_text, out_path, *, source_label="hlk_pdf_render") -> int``
  Renders Markdown to DOCX via pandoc. Soft-succeeds with the markdown
  sidecar when pandoc is unavailable.

- ``MD_EXTENSIONS`` — list of ``markdown`` library extensions used by both
  PDF and HTML pipelines.

Brand tokens (sourced from ``c:\\Users\\Shadow\\cd_shadow\\root_cd\\boilerplate``):
constants ``BRAND_TOKENS_LIGHT`` and ``BRAND_TOKENS_DARK`` mirror the HSL
values in ``BRAND_VISUAL_PATTERNS.md`` §1.1 / §1.2 so a single source-of-truth
update propagates here without code edits beyond the constant table.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

MD_EXTENSIONS: list[str] = ["tables", "fenced_code", "toc", "sane_lists", "attr_list"]


_TD_INLINE_TAGS_RE = re.compile(r"</?(?:code|a|em|strong|span|i|b)(?:\s[^>]*)?>", re.IGNORECASE)


def _flatten_td_inlines(html: str) -> str:
    """Strip nested inline tags inside ``<td>...</td>`` cells.

    fpdf2's ``write_html`` raises ``NotImplementedError: Unsupported nested
    HTML tags inside <td>`` when cells contain ``<code>``, ``<a>``, etc. The
    handoff Markdown is heavy on ``ref_id`` codes inside table cells; flatten
    those wrappers but keep the text so the PDF still shows the GOI/POI ids
    and links inline.
    """
    def _strip_in_td(match: "re.Match[str]") -> str:
        return _TD_INLINE_TAGS_RE.sub("", match.group(0))

    return re.sub(r"<td\b[^>]*>.*?</td>", _strip_in_td, html, flags=re.DOTALL | re.IGNORECASE)


_PDF_CSS = """
@page { size: A4; margin: 18mm 16mm 18mm 16mm; }
html { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; font-size: 10.5pt; line-height: 1.4; color: #1f1f1f; }
h1 { font-size: 20pt; margin-top: 0; }
h2 { font-size: 15pt; margin-top: 1.4em; border-bottom: 1px solid #d0d0d0; padding-bottom: 0.2em; }
h3 { font-size: 12pt; margin-top: 1.1em; }
code, pre { font-family: "Consolas", "Menlo", "Courier New", monospace; font-size: 9.5pt; }
code { background: #f4f4f6; padding: 1px 4px; border-radius: 3px; }
pre { background: #f4f4f6; padding: 8px 10px; border-radius: 4px; }
table { border-collapse: collapse; width: 100%; font-size: 9pt; margin: 0.6em 0 1em; page-break-inside: avoid; }
th, td { border: 1px solid #c8c8c8; padding: 5px 7px; vertical-align: top; }
th { background: #ececef; text-align: left; }
blockquote { border-left: 3px solid #888; padding: 6px 12px; color: #444; background: #fafafa; }
hr { border: none; border-top: 1px solid #c0c0c0; margin: 1em 0; }
a { color: #1a4dba; text-decoration: none; }
"""


# -- Initiative 27 P1: branded PDF renderer ------------------------------------
#
# Brand tokens mirror BRAND_VISUAL_PATTERNS.md §1.1 / §1.2. Keep these in sync
# with ``c:\\Users\\Shadow\\cd_shadow\\root_cd\\boilerplate\\app\\globals.css``.

BRAND_TOKENS_LIGHT: dict[str, str] = {
    "background": "hsl(40 20% 99%)",
    "foreground": "hsl(220 12% 18%)",
    "card": "hsl(40 15% 98%)",
    "muted_foreground": "hsl(220 8% 42%)",
    "border": "hsl(220 8% 88%)",
    "secondary": "hsl(220 8% 95%)",
    "accent_primary": "hsl(168 55% 38%)",
    "accent_secondary": "hsl(38 80% 50%)",
    "destructive": "hsl(0 75% 55%)",
}

BRAND_TOKENS_DARK: dict[str, str] = {
    "background": "hsl(220 16% 7%)",
    "foreground": "hsl(210 15% 90%)",
    "card": "hsl(220 14% 10%)",
    "accent_primary": "hsl(168 50% 44%)",
    "accent_secondary": "hsl(38 75% 55%)",
}


def _brand_pdf_css(*, profile: str = "dossier") -> str:
    """Return the brand-aligned CSS string used by ``render_pdf_branded``.

    Initiative 27 follow-up — visual upgrade per operator feedback (PDF "not
    appealing"). Inspired by modern proposal/dossier design patterns: oversized
    cover title with generous whitespace, numbered section indicators (CSS
    counters on body H1s), stat callouts (.stat-grid), pull-quote class for
    margin emphasis, capability cards with tag pills, friendly open-question
    callouts, cleaner page footer.

    Keep token references in sync with ``BRAND_TOKENS_LIGHT`` / ``BRAND_TOKENS_DARK``.
    """
    L = BRAND_TOKENS_LIGHT
    D = BRAND_TOKENS_DARK
    return (
        # ---- Page setup + footer string ------------------------------------
        "@page { size: A4; margin: 22mm 20mm 24mm 20mm; "
        "@bottom-center { content: string(footerline); font-family: Inter, 'Segoe UI', Arial, sans-serif; "
        "font-size: 8pt; color: " + L["muted_foreground"] + "; letter-spacing: 0.04em; } "
        "@bottom-right { content: counter(page) ' / ' counter(pages); font-family: Inter, 'Segoe UI', Arial, sans-serif; "
        "font-size: 8pt; color: " + L["muted_foreground"] + "; } }\n"
        "@page :first { margin: 0; @bottom-center { content: ''; } @bottom-right { content: ''; } }\n"

        # ---- Base typography -----------------------------------------------
        "html { font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, 'Helvetica Neue', Arial, sans-serif; "
        "font-size: 10.5pt; line-height: 1.65; color: " + L["foreground"] + "; background: " + L["background"] + "; "
        "counter-reset: section; }\n"
        "body { margin: 0; padding: 0; }\n"
        "p { margin: 0 0 0.85em 0; }\n"
        "strong { color: " + L["foreground"] + "; font-weight: 600; }\n"
        "em { color: " + L["foreground"] + "; }\n"

        # ---- Cover hero (clean, oversized title; metadata moved to footer band) -----
        ".cover-hero { min-height: 297mm; padding: 30mm 24mm 28mm 24mm; color: " + D["foreground"] + "; "
        "background: "
        "radial-gradient(ellipse 65% 55% at 28% 32%, hsla(168, 55%, 38%, 0.22) 0%, transparent 62%), "
        "radial-gradient(ellipse 85% 75% at 72% 65%, hsla(38, 80%, 50%, 0.14) 0%, transparent 72%), "
        "linear-gradient(155deg, " + D["background"] + " 0%, " + D["card"] + " 50%, hsl(220 12% 13%) 100%); "
        "page-break-after: always; position: relative; }\n"
        ".cover-hero .cover-eyebrow { font-size: 9pt; text-transform: uppercase; letter-spacing: 0.18em; color: " + D["accent_primary"] + "; "
        "font-weight: 600; margin: 0 0 8mm 0; opacity: 0.95; }\n"
        ".cover-hero .cover-monogram { width: 24mm; height: 24mm; margin-bottom: 60mm; opacity: 0.95; }\n"
        ".cover-hero h1 { font-size: 44pt; font-weight: 700; margin: 0 0 8mm 0; color: " + D["foreground"] + "; "
        "line-height: 1.05; letter-spacing: -0.025em; max-width: 130mm; }\n"
        ".cover-hero .cover-subtitle { font-size: 14pt; color: " + D["foreground"] + "; opacity: 0.78; "
        "margin: 0 0 0 0; font-weight: 400; max-width: 120mm; line-height: 1.4; }\n"
        ".cover-hero .cover-strip { position: absolute; left: 24mm; right: 24mm; bottom: 24mm; "
        "border-top: 1px solid hsla(168, 50%, 44%, 0.4); padding-top: 8mm; "
        "display: flex; justify-content: space-between; font-size: 9pt; "
        "color: " + D["foreground"] + "; opacity: 0.78; letter-spacing: 0.04em; }\n"
        ".cover-hero .cover-strip .strip-item .strip-label { display: block; font-size: 7.5pt; "
        "text-transform: uppercase; letter-spacing: 0.16em; color: " + D["accent_secondary"] + "; "
        "margin-bottom: 1.5mm; opacity: 0.9; }\n"
        ".cover-hero .cover-strip .strip-item .strip-value { font-weight: 600; color: " + D["foreground"] + "; opacity: 1; }\n"

        # ---- Body wrapper with horizontal margins ----------------------------
        ".dossier-body { max-width: 170mm; margin: 0 auto; padding: 0 0; }\n"
        ".footer-string { string-set: footerline content(); display: none; }\n"

        # ---- Section H1 with numbered counter --------------------------------
        # Body H1 acts as a section opener: "01 Pilar I — Mercantil"
        "main h1 { counter-increment: section; font-size: 26pt; font-weight: 700; "
        "margin: 8mm 0 4mm 0; color: " + L["foreground"] + "; letter-spacing: -0.018em; "
        "line-height: 1.15; page-break-before: auto; page-break-after: avoid; "
        "padding-top: 14mm; border-top: 1px solid " + L["border"] + "; position: relative; }\n"
        "main h1::before { content: counter(section, decimal-leading-zero); "
        "display: block; font-size: 11pt; font-weight: 600; color: " + L["accent_primary"] + "; "
        "letter-spacing: 0.18em; margin-bottom: 4mm; text-transform: uppercase; }\n"
        "main > h1:first-of-type { padding-top: 0; border-top: none; }\n"

        # H2 = sub-heading inside a pillar
        "h2 { font-size: 16pt; font-weight: 600; margin: 10mm 0 3mm 0; color: " + L["foreground"] + "; "
        "letter-spacing: -0.005em; page-break-after: avoid; line-height: 1.25; }\n"
        "h2::before { content: ''; display: block; width: 8mm; height: 2px; "
        "background: " + L["accent_primary"] + "; margin-bottom: 3mm; }\n"

        "h3 { font-size: 12pt; font-weight: 600; margin: 6mm 0 2mm 0; "
        "color: " + L["foreground"] + "; page-break-after: avoid; line-height: 1.3; }\n"
        "h4 { font-size: 9.5pt; font-weight: 600; margin: 5mm 0 1.5mm 0; "
        "color: " + L["accent_primary"] + "; text-transform: uppercase; "
        "letter-spacing: 0.12em; page-break-after: avoid; }\n"

        # ---- Code / monospace ------------------------------------------------
        "code, pre { font-family: 'Consolas', 'Menlo', 'Courier New', monospace; font-size: 9pt; }\n"
        "code { background: " + L["secondary"] + "; padding: 1px 5px; border-radius: 3px; "
        "color: " + L["foreground"] + "; }\n"
        "pre { background: " + L["card"] + "; padding: 10px 14px; border-radius: 4px; "
        "border: 1px solid " + L["border"] + "; line-height: 1.5; }\n"

        # ---- Tables: airier, more whitespace ---------------------------------
        "table { border-collapse: collapse; width: 100%; font-size: 9.5pt; "
        "margin: 5mm 0 6mm; page-break-inside: avoid; line-height: 1.5; }\n"
        "th, td { border-bottom: 1px solid " + L["border"] + "; padding: 8px 10px; "
        "vertical-align: top; text-align: left; }\n"
        "th { color: " + L["muted_foreground"] + "; font-size: 8.5pt; font-weight: 600; "
        "text-transform: uppercase; letter-spacing: 0.08em; "
        "border-bottom: 2px solid " + L["foreground"] + "; padding-bottom: 6px; }\n"
        "tr:last-child td { border-bottom: none; }\n"

        # ---- Friendly open-question callout (replaces TODO[OPERATOR]) -------
        "blockquote { border-left: 3px solid " + L["accent_primary"] + "; padding: 5mm 7mm; "
        "color: " + L["foreground"] + "; background: hsla(168, 55%, 38%, 0.05); "
        "margin: 5mm 0; border-radius: 0 4px 4px 0; line-height: 1.55; }\n"
        "blockquote p:last-child { margin-bottom: 0; }\n"
        "blockquote.callout-question { border-left: 4px solid " + L["accent_secondary"] + "; "
        "background: hsla(38, 80%, 50%, 0.07); padding: 6mm 8mm; margin: 6mm 0; }\n"
        "blockquote.callout-question .callout-label { display: block; font-size: 8.5pt; "
        "font-weight: 700; color: " + L["accent_secondary"] + "; "
        "text-transform: uppercase; letter-spacing: 0.14em; margin-bottom: 3mm; }\n"
        "blockquote.callout-risk { border-left-color: " + L["destructive"] + "; "
        "background: hsla(0, 75%, 55%, 0.05); }\n"
        # Legacy class kept for compatibility
        "blockquote.callout-operator { border-left: 4px solid " + L["accent_secondary"] + "; "
        "background: hsla(38, 80%, 50%, 0.07); padding: 6mm 8mm; margin: 6mm 0; }\n"

        # ---- Stat grid (oversized number + small caps label) ----------------
        ".stat-grid { display: flex; flex-wrap: wrap; gap: 0; margin: 6mm 0 8mm; "
        "border-top: 1px solid " + L["border"] + "; border-bottom: 1px solid " + L["border"] + "; "
        "padding: 4mm 0; page-break-inside: avoid; }\n"
        ".stat-grid .stat { flex: 1 1 0; min-width: 30mm; padding: 2mm 4mm; "
        "border-right: 1px solid " + L["border"] + "; }\n"
        ".stat-grid .stat:last-child { border-right: none; }\n"
        ".stat-grid .stat-num { display: block; font-size: 22pt; font-weight: 700; "
        "color: " + L["accent_primary"] + "; line-height: 1; letter-spacing: -0.02em; "
        "margin-bottom: 2mm; }\n"
        ".stat-grid .stat-label { display: block; font-size: 8pt; font-weight: 600; "
        "color: " + L["muted_foreground"] + "; text-transform: uppercase; letter-spacing: 0.1em; "
        "line-height: 1.3; }\n"

        # ---- Pull-quote / lead paragraph ------------------------------------
        ".lead { font-size: 13pt; line-height: 1.55; color: " + L["foreground"] + "; "
        "font-weight: 400; margin: 4mm 0 6mm; max-width: 150mm; }\n"
        ".pull-quote { font-size: 14pt; line-height: 1.45; color: " + L["accent_primary"] + "; "
        "font-style: italic; font-weight: 500; padding: 4mm 0 4mm 6mm; "
        "border-left: 3px solid " + L["accent_primary"] + "; margin: 6mm 0; }\n"

        # ---- Capability cards (Apéndice C) ----------------------------------
        ".capability-card { border: 1px solid " + L["border"] + "; border-radius: 6px; "
        "margin: 5mm 0 6mm; page-break-inside: avoid; overflow: hidden; "
        "background: " + L["background"] + "; }\n"
        ".capability-card .card-head { background: " + L["foreground"] + "; "
        "color: " + L["background"] + "; padding: 4mm 6mm; }\n"
        ".capability-card .card-head .card-eyebrow { font-size: 7.5pt; font-weight: 600; "
        "text-transform: uppercase; letter-spacing: 0.16em; "
        "color: " + L["accent_primary"] + "; margin-bottom: 1.5mm; display: block; }\n"
        ".capability-card .card-head .card-title { font-size: 13pt; font-weight: 600; "
        "color: " + L["background"] + "; margin: 0; line-height: 1.3; }\n"
        ".capability-card .card-tags { padding: 3mm 6mm 1mm; display: flex; flex-wrap: wrap; "
        "gap: 1.5mm; background: " + L["card"] + "; border-bottom: 1px solid " + L["border"] + "; }\n"
        ".capability-card .card-tags .tag { display: inline-block; font-size: 7.5pt; "
        "font-weight: 500; padding: 1mm 2.5mm; border-radius: 999px; "
        "background: hsla(168, 55%, 38%, 0.1); color: " + L["accent_primary"] + "; "
        "letter-spacing: 0.04em; margin-bottom: 1.5mm; }\n"
        ".capability-card .card-tags .tag.tag-amber { background: hsla(38, 80%, 50%, 0.12); "
        "color: " + L["accent_secondary"] + "; }\n"
        ".capability-card .card-body { padding: 5mm 6mm 4mm; line-height: 1.6; }\n"
        ".capability-card .card-body p:last-child { margin-bottom: 0; }\n"
        ".capability-card .card-foot { padding: 3mm 6mm 4mm; font-size: 8.5pt; "
        "color: " + L["muted_foreground"] + "; border-top: 1px solid " + L["border"] + "; "
        "background: " + L["card"] + "; }\n"

        # ---- Other primitives -----------------------------------------------
        "hr { border: none; border-top: 1px solid " + L["border"] + "; margin: 6mm 0; }\n"
        "a { color: " + L["accent_primary"] + "; text-decoration: none; "
        "border-bottom: 1px dotted " + L["accent_primary"] + "; }\n"
        "img { max-width: 100%; height: auto; }\n"
        "figure { margin: 5mm 0; page-break-inside: avoid; }\n"
        "figcaption { font-size: 8.5pt; color: " + L["muted_foreground"] + "; "
        "font-style: italic; margin-top: 1mm; }\n"
        ".source-cite { font-size: 8.5pt; color: " + L["muted_foreground"] + "; "
        "font-style: italic; margin-top: 1mm; }\n"

        # ---- Lists: airier ---------------------------------------------------
        "ul, ol { margin: 0 0 1em 0; padding-left: 4mm; }\n"
        "li { margin-bottom: 1.5mm; line-height: 1.55; }\n"
        "li::marker { color: " + L["accent_primary"] + "; }\n"
    )


# Initiative 27 follow-up: friendly open-question callouts.
# Per BRAND_JARGON_AUDIT.md §4.4 and §7: ``TODO[OPERATOR]`` must never reach the
# rendered output of an external deliverable. The render pipeline post-processes
# the HTML emitted by ``markdown`` to replace the operator-side label with a
# brand-friendly callout (Spanish or English depending on the language hint).
#
# The source Markdown still carries the ``TODO[OPERATOR]`` marker for operator
# grep/audit (see BRAND_JARGON_AUDIT §6 audit checklist); only the rendered
# HTML is transformed.

_TODO_OPERATOR_BLOCKQUOTE_RE = re.compile(
    # Match a <blockquote> whose first <p> contains <strong>TODO[OPERATOR]</strong>
    # followed by an em-dash / hyphen / colon. Captures the rest of the first
    # paragraph and the rest of the blockquote contents.
    r"<blockquote(?P<attrs>[^>]*)>\s*"
    r"<p>\s*<strong>\s*TODO\[OPERATOR\]\s*</strong>\s*"
    r"(?:[—\u2014\-:]+\s*)?"
    r"(?P<lead>.*?)</p>"
    r"(?P<rest>.*?)"
    r"</blockquote>",
    re.IGNORECASE | re.DOTALL,
)


def _friendly_callout_labels_html(html: str, *, language: str = "es") -> str:
    """Rewrite ``<blockquote>`` blocks that lead with ``<strong>TODO[OPERATOR]</strong>``.

    Replaces the operator-side label with an amber-tinted callout heading
    (``Pregunta abierta para tu confirmación`` in Spanish; ``Open question for
    your confirmation`` in English) and tags the blockquote with
    ``class="callout-question"`` so the brand CSS styles it.

    Args:
        html: HTML emitted by ``markdown.markdown(...)``.
        language: Language hint (``"es"`` or ``"en"``). Defaults to Spanish.

    Returns:
        HTML with all ``TODO[OPERATOR]`` blockquotes rewritten.
    """
    label = (
        "Pregunta abierta para tu confirmación"
        if language == "es"
        else "Open question for your confirmation"
    )

    def _rewrite(match: "re.Match[str]") -> str:
        existing_attrs = match.group("attrs") or ""
        lead = (match.group("lead") or "").strip()
        rest = (match.group("rest") or "").strip()
        # Inject class="callout-question" while preserving any existing attrs.
        if "class=" in existing_attrs.lower():
            attrs = re.sub(
                r'class\s*=\s*"([^"]*)"',
                r'class="\1 callout-question"',
                existing_attrs,
                count=1,
                flags=re.IGNORECASE,
            )
        else:
            attrs = existing_attrs + ' class="callout-question"'
        head = f'<span class="callout-label">{label}</span>'
        first_para = f"<p>{lead}</p>" if lead else ""
        return f"<blockquote{attrs}>{head}{first_para}{rest}</blockquote>"

    return _TODO_OPERATOR_BLOCKQUOTE_RE.sub(_rewrite, html)


def _build_cover_html(
    *,
    title: str,
    subtitle: str | None = None,
    program_id: str | None = None,
    discipline: str | None = None,
    issue_date: str | None = None,
    status_label: str | None = None,
    monogram_path: str | None = None,
    eyebrow: str | None = "Holística Research · Dossier",
) -> str:
    """Return the cover-page HTML fragment used by ``render_pdf_branded``.

    Initiative 27 follow-up — visual upgrade. Layout:

      [eyebrow caps]
      [monogram]

      ...generous whitespace...

      [oversized title]
      [subtitle, smaller]

      [bottom strip: program | date | discipline]
    """
    monogram_html = ""
    if monogram_path and Path(monogram_path).is_file():
        uri = Path(monogram_path).resolve().as_uri()
        monogram_html = f'<img class="cover-monogram" src="{uri}" alt="Holística Research" />'

    eyebrow_html = (
        f'<div class="cover-eyebrow">{eyebrow}</div>'
        if eyebrow
        else ""
    )
    subtitle_html = (
        f'<div class="cover-subtitle">{subtitle}</div>'
        if subtitle
        else ""
    )

    # Bottom strip — small, single-row, three columns max
    strip_items: list[str] = []
    if program_id:
        strip_items.append(
            f'<div class="strip-item"><span class="strip-label">Programa</span>'
            f'<span class="strip-value">{program_id}</span></div>'
        )
    if issue_date:
        strip_items.append(
            f'<div class="strip-item"><span class="strip-label">Fecha</span>'
            f'<span class="strip-value">{issue_date}</span></div>'
        )
    if discipline:
        strip_items.append(
            f'<div class="strip-item"><span class="strip-label">Disciplina</span>'
            f'<span class="strip-value">{discipline}</span></div>'
        )
    # Status label is intentionally dropped from the visual cover (kept in
    # frontmatter / footer string only) to reduce visual clutter per operator
    # feedback. If a future profile wants it back, gate behind the profile arg.
    _ = status_label
    strip_html = (
        f'<div class="cover-strip">{"".join(strip_items)}</div>'
        if strip_items
        else ""
    )

    return (
        '<section class="cover-hero">'
        f'{eyebrow_html}'
        f'{monogram_html}'
        f'<h1>{title}</h1>'
        f'{subtitle_html}'
        f'{strip_html}'
        "</section>"
    )


def render_pdf_branded(
    md_text: str,
    out_path: Path,
    *,
    profile: str = "dossier",
    title: str | None = None,
    subtitle: str | None = None,
    program_id: str | None = None,
    discipline: str | None = None,
    issue_date: str | None = None,
    status_label: str | None = None,
    monogram_path: str | None = None,
    source_label: str = "hlk_pdf_render_branded",
) -> int:
    """Render Markdown to a brand-aligned PDF (Initiative 27 P1).

    Uses the live Holistika brand tokens captured in
    ``docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VISUAL_PATTERNS.md``
    (teal / amber / warm-slate; Inter font; 0.5rem radius). Adds a dark hero
    band cover with the Holistika monogram and a body styled per the print
    variant rules. Falls through the same WeasyPrint -> fpdf2 -> pandoc chain
    as :func:`render_pdf` so it degrades gracefully.

    ``profile`` is reserved for future variants (e.g. ``"investor_pitch"``,
    ``"adviser_pack"``) — currently only ``"dossier"`` is implemented; other
    values fall back to the dossier styling with a warning.

    Args:
        md_text: Markdown source. Treated as the **body** content; the cover
            hero is generated from the metadata kwargs.
        out_path: Output PDF path. Parent directory is created if missing.
        profile: Visual profile name. Currently only ``"dossier"`` is honored.
        title: Cover title (e.g. ``"Dossier ENISA"``). If ``None``, the cover
            section is suppressed and the renderer falls back to plain
            ``render_pdf`` with the brand body CSS.
        subtitle: Cover subtitle (e.g. ``"Empresa Emergente — Certificación"``).
        program_id: Program reference id (cited in cover meta + page footer).
        discipline: Discipline label (e.g. ``"Asesoría Jurídica"``).
        issue_date: ISO date string used in the cover and the page footer.
        status_label: Free-text status label (e.g. ``"P1-Audit ready"``).
        monogram_path: Filesystem path to the Holistika monogram SVG/PNG used
            on the cover. If ``None`` or unreadable, the cover renders without
            it.
        source_label: Label used in stderr/stdout messages for traceability.

    Returns:
        ``0`` on success (including soft-success when the renderer chain falls
        back to writing only the markdown sidecar). Non-zero only when an
        explicit subprocess (e.g. pandoc) fails.
    """
    if profile != "dossier":
        print(
            f"warning: {source_label}: profile={profile!r} not implemented; "
            "falling back to dossier styling.",
            file=sys.stderr,
        )

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        import markdown as _md_lib  # type: ignore
    except ImportError:
        _md_lib = None

    if _md_lib is None:
        return render_pdf(md_text, out_path, source_label=source_label)

    body_html = _md_lib.markdown(md_text, extensions=MD_EXTENSIONS)

    # Detect language from the cover-side metadata or default to Spanish.
    # The language hint controls the friendly callout label (es/en).
    language_hint = "es"
    if subtitle and any(
        word in (subtitle or "").lower()
        for word in ("certification", "the ", "english", "operator brief")
    ):
        language_hint = "en"
    body_html = _friendly_callout_labels_html(body_html, language=language_hint)

    cover_html = ""
    if title:
        cover_html = _build_cover_html(
            title=title,
            subtitle=subtitle,
            program_id=program_id,
            discipline=discipline,
            issue_date=issue_date,
            status_label=status_label,
            monogram_path=monogram_path,
        )

    footer_parts = [p for p in (program_id, discipline, issue_date) if p]
    footer_text = " · ".join(footer_parts) if footer_parts else ""
    footer_div = f'<div class="footer-string">{footer_text}</div>' if footer_text else ""

    css = _brand_pdf_css(profile=profile)
    html_doc = (
        '<!DOCTYPE html><html><head><meta charset="utf-8">'
        f"<style>{css}</style></head><body>"
        f"{cover_html}"
        f"{footer_div}"
        f'<main class="dossier-body">{body_html}</main>'
        "</body></html>"
    )

    # Renderer 1: WeasyPrint (best CSS fidelity; honors the gradient cover).
    try:
        from weasyprint import HTML  # type: ignore
        try:
            HTML(string=html_doc, base_url=str(out_path.parent.resolve())).write_pdf(str(out_path))
            print(f"{source_label}: WeasyPrint wrote branded PDF -> {out_path}")
            return 0
        except Exception as exc:  # noqa: BLE001
            print(
                f"warning: {source_label}: WeasyPrint installed but rendering failed "
                f"({exc!r}); falling back to fpdf2 (gradient cover dropped).",
                file=sys.stderr,
            )
    except Exception:  # noqa: BLE001 — WeasyPrint not installed
        pass

    # Renderer 2: fpdf2 — drops the gradient cover but keeps the body palette.
    try:
        from fpdf import FPDF  # type: ignore
        try:
            pdf = FPDF(orientation="P", unit="mm", format="A4")
            pdf.set_auto_page_break(auto=True, margin=18)
            pdf.add_page()
            pdf.set_margins(left=16, top=18, right=16)

            family = "Helvetica"
            for fam, regular, bold, italic in _font_candidates():
                if Path(regular).is_file():
                    pdf.add_font(fam, "", regular)
                    if Path(bold).is_file():
                        pdf.add_font(fam, "B", bold)
                    if Path(italic).is_file():
                        pdf.add_font(fam, "I", italic)
                    family = fam
                    break
            pdf.set_font(family, size=10)

            # fpdf2 cover fallback: solid teal band with title (no gradient).
            if title:
                pdf.set_fill_color(43, 144, 119)  # teal hsl(168 55% 38%) approx
                pdf.rect(0, 0, 210, 80, "F")
                pdf.set_xy(16, 24)
                pdf.set_text_color(255, 255, 255)
                pdf.set_font(family, "B", 22)
                pdf.cell(0, 12, title, ln=1)
                if subtitle:
                    pdf.set_x(16)
                    pdf.set_font(family, "", 12)
                    pdf.cell(0, 8, subtitle, ln=1)
                pdf.ln(8)
                pdf.set_x(16)
                pdf.set_font(family, "", 10)
                meta_lines = []
                if program_id:
                    meta_lines.append(f"Programa: {program_id}")
                if discipline:
                    meta_lines.append(f"Disciplina: {discipline}")
                if status_label:
                    meta_lines.append(f"Estado: {status_label}")
                if issue_date:
                    meta_lines.append(f"Fecha: {issue_date}")
                for line in meta_lines:
                    pdf.set_x(16)
                    pdf.cell(0, 6, line, ln=1)
                pdf.set_text_color(31, 31, 31)
                pdf.ln(4)
                pdf.add_page()

            pdf.set_font(family, size=10)
            pdf.set_text_color(40, 45, 54)  # warm charcoal
            fpdf_html = _flatten_td_inlines(body_html)
            pdf.write_html(fpdf_html, ul_bullet_char="-", li_prefix_color=(98, 102, 111))
            pdf.output(str(out_path))
            print(f"{source_label}: fpdf2 wrote branded PDF (no gradient cover) -> {out_path}")
            return 0
        except Exception as exc:  # noqa: BLE001
            print(
                f"warning: {source_label}: fpdf2 installed but rendering failed "
                f"({exc!r}); falling back to pandoc.",
                file=sys.stderr,
            )
    except Exception as exc:  # noqa: BLE001
        print(f"warning: {source_label}: fpdf2 unavailable ({exc!r}); falling back to pandoc.", file=sys.stderr)

    # Renderer 3: pandoc (no gradient, no cover styling — just structure).
    pandoc = shutil.which("pandoc")
    md_tmp = out_path.with_suffix(".md")
    if not md_tmp.is_file():
        md_tmp.write_text(md_text, encoding="utf-8")
    if not pandoc:
        print(
            f"warning: {source_label}: no PDF renderer available; "
            f"wrote markdown only at {md_tmp}.",
            file=sys.stderr,
        )
        return 0  # soft-success
    cmd = [pandoc, str(md_tmp), "-o", str(out_path)]
    print(f"{source_label}: running:", " ".join(cmd))
    rc = subprocess.call(cmd)
    if rc != 0:
        print(f"error: {source_label}: pandoc returned {rc}", file=sys.stderr)
        return rc
    print(f"{source_label}: pandoc wrote PDF (unstyled) -> {out_path}")
    return 0


def _font_candidates() -> list[tuple[str, str, str, str]]:
    """Return Unicode-capable font candidates per platform.

    fpdf2's built-in fonts are Latin-1 only; Spanish accents and en-dashes
    require a Unicode TTF.
    """
    return [
        ("SegoeUI", "C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/segoeuii.ttf"),
        ("Arial", "C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/ariali.ttf"),
        ("DejaVuSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf"),
    ]


def render_pdf(md_text: str, out_path: Path, *, source_label: str = "hlk_pdf_render") -> int:
    """Render Markdown to PDF using WeasyPrint, fpdf2, or pandoc (in that order).

    Returns 0 on success, including the soft-success path when no renderer is
    available (a sibling ``.md`` is written next to ``out_path`` so callers
    still have the source). Returns non-zero only when an explicit subprocess
    fails (e.g. pandoc returns non-zero).
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        import markdown as _md_lib  # type: ignore
    except ImportError:
        _md_lib = None

    if _md_lib is not None:
        html_body = _md_lib.markdown(md_text, extensions=MD_EXTENSIONS)
        html_doc = (
            "<!DOCTYPE html><html><head><meta charset=\"utf-8\">"
            f"<style>{_PDF_CSS}</style></head><body>{html_body}</body></html>"
        )

        # Renderer 1: WeasyPrint (best CSS fidelity; needs native Cairo/Pango)
        try:
            from weasyprint import HTML  # type: ignore
            try:
                HTML(string=html_doc).write_pdf(str(out_path))
                print(f"{source_label}: WeasyPrint wrote PDF -> {out_path}")
                return 0
            except Exception as exc:  # noqa: BLE001
                print(
                    f"warning: WeasyPrint installed but rendering failed ({exc!r}); "
                    "falling back to fpdf2. On Windows install GTK3 runtime to enable WeasyPrint.",
                    file=sys.stderr,
                )
        except Exception:  # noqa: BLE001 — WeasyPrint not installed
            pass

        # Renderer 2: fpdf2 (pure-Python, zero native deps)
        try:
            from fpdf import FPDF  # type: ignore
            try:
                pdf = FPDF(orientation="P", unit="mm", format="A4")
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_page()
                pdf.set_margins(left=15, top=15, right=15)

                family = "Helvetica"
                for fam, regular, bold, italic in _font_candidates():
                    if Path(regular).is_file():
                        pdf.add_font(fam, "", regular)
                        if Path(bold).is_file():
                            pdf.add_font(fam, "B", bold)
                        if Path(italic).is_file():
                            pdf.add_font(fam, "I", italic)
                        family = fam
                        break
                pdf.set_font(family, size=10)

                fpdf_html = _flatten_td_inlines(html_body)
                pdf.write_html(fpdf_html, ul_bullet_char="-", li_prefix_color=(80, 80, 80))
                pdf.output(str(out_path))
                print(f"{source_label}: fpdf2 wrote PDF -> {out_path}")
                return 0
            except Exception as exc:  # noqa: BLE001
                print(
                    f"warning: fpdf2 installed but rendering failed ({exc!r}); falling back to pandoc.",
                    file=sys.stderr,
                )
        except Exception as exc:  # noqa: BLE001
            print(f"warning: fpdf2 unavailable ({exc!r}); falling back to pandoc.", file=sys.stderr)

    # Renderer 3: pandoc
    pandoc = shutil.which("pandoc")
    md_tmp = out_path.with_suffix(".md")
    if not md_tmp.is_file():
        md_tmp.write_text(md_text, encoding="utf-8")
    if not pandoc:
        print(
            f"warning: {source_label}: no PDF renderer available "
            "(markdown / WeasyPrint / fpdf2 / pandoc all missing); "
            f"wrote markdown only at {md_tmp}. To enable PDF, run "
            "`py -m pip install --only-binary=:all: -r requirements-export.txt` "
            "(installs fpdf2 for a pure-Python path), or install pandoc, or "
            "render DOCX via pandoc and convert to PDF in Word.",
            file=sys.stderr,
        )
        return 0  # soft-success
    cmd = [pandoc, str(md_tmp), "-o", str(out_path)]
    print(f"{source_label}: running:", " ".join(cmd))
    rc = subprocess.call(cmd)
    if rc != 0:
        print(f"error: {source_label}: pandoc returned {rc}", file=sys.stderr)
        return rc
    print(f"{source_label}: pandoc wrote PDF -> {out_path}")
    return 0


def render_docx(md_text: str, out_path: Path, *, source_label: str = "hlk_pdf_render") -> int:
    """Render Markdown to DOCX via pandoc (CLI on PATH, pypandoc, or
    pypandoc_binary which bundles pandoc in a pip wheel).

    Resolution order:
      1. ``pandoc`` on PATH (fastest; system install via Chocolatey / pandoc.org).
      2. ``pypandoc`` library — auto-finds pandoc if installed; can also use
         a bundled pandoc when ``pypandoc_binary`` is installed alongside.
    Soft-succeeds (returns 0 with the markdown sidecar written) when no
    pandoc backend is available.
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    md_tmp = out_path.with_suffix(".md")
    if not md_tmp.is_file():
        md_tmp.write_text(md_text, encoding="utf-8")

    extra_args = [
        "--from=markdown+pipe_tables+fenced_code_blocks+yaml_metadata_block",
        "--to=docx",
        "--standalone",
    ]

    # Backend 1: pandoc on PATH.
    pandoc = shutil.which("pandoc")
    if pandoc:
        cmd = [pandoc, str(md_tmp), "-o", str(out_path)] + extra_args
        print(f"{source_label}: running:", " ".join(cmd))
        rc = subprocess.call(cmd)
        if rc != 0:
            print(f"error: {source_label}: pandoc returned {rc}", file=sys.stderr)
            return rc
        print(f"{source_label}: pandoc wrote DOCX -> {out_path}")
        return 0

    # Backend 2: pypandoc (auto-finds pandoc; pairs with pypandoc_binary for a
    # zero-system-install path).
    try:
        import pypandoc  # type: ignore

        try:
            # pypandoc returns the output path string when outputfile is set.
            pypandoc.convert_text(
                md_text,
                "docx",
                format="md",
                outputfile=str(out_path),
                extra_args=["--standalone"],
            )
            print(f"{source_label}: pypandoc wrote DOCX -> {out_path}")
            return 0
        except Exception as exc:  # noqa: BLE001
            print(
                f"warning: {source_label}: pypandoc installed but rendering failed "
                f"({exc!r}); install pandoc on PATH (https://pandoc.org/installing.html) "
                "or `py -m pip install pypandoc_binary` to bundle pandoc.",
                file=sys.stderr,
            )
    except ImportError:
        pass

    print(
        f"warning: {source_label}: no DOCX backend available "
        "(pandoc / pypandoc / pypandoc_binary all missing). "
        f"Wrote markdown sidecar at {md_tmp}. Install via "
        "`py -m pip install pypandoc_binary` (zero-system install, ~70 MB) "
        "or `choco install pandoc` (Windows) / `brew install pandoc` (macOS). "
        "Or open the .md in Word/LibreOffice and Save As DOCX manually.",
        file=sys.stderr,
    )
    return 0  # soft-success
