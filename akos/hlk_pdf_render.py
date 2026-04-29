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

    The CSS is a single Python string (not f-string) using ``.format()`` so
    that curly braces from CSS rules don't fight Python's f-string parser.
    Keep token references in sync with ``BRAND_TOKENS_LIGHT`` / ``BRAND_TOKENS_DARK``.
    """
    L = BRAND_TOKENS_LIGHT
    D = BRAND_TOKENS_DARK
    return (
        "@page { size: A4; margin: 18mm 16mm 22mm 16mm; @bottom-center { content: "
        "string(footerline); font-family: Inter, 'Segoe UI', Arial, sans-serif; "
        "font-size: 8.5pt; color: " + L["muted_foreground"] + "; } }\n"
        "@page :first { margin: 0; }\n"
        "html { font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, 'Helvetica Neue', Arial, sans-serif; font-size: 10.5pt; line-height: 1.5; color: " + L["foreground"] + "; background: " + L["background"] + "; }\n"
        "body { margin: 0; padding: 0; }\n"
        "p { margin: 0 0 0.75em 0; }\n"
        "strong { color: " + L["foreground"] + "; font-weight: 600; }\n"
        "em { color: " + L["foreground"] + "; }\n"
        ".cover-hero { min-height: 297mm; padding: 36mm 24mm 28mm 24mm; color: " + D["foreground"] + "; "
        "background: "
        "radial-gradient(ellipse 60% 50% at 30% 30%, hsla(168, 55%, 38%, 0.18) 0%, transparent 60%), "
        "radial-gradient(ellipse 80% 70% at 70% 60%, hsla(38, 80%, 50%, 0.12) 0%, transparent 70%), "
        "linear-gradient(160deg, " + D["background"] + " 0%, " + D["card"] + " 55%, hsl(220 12% 14%) 100%); "
        "page-break-after: always; }\n"
        ".cover-hero .cover-monogram { width: 28mm; height: 28mm; margin-bottom: 18mm; opacity: 0.95; }\n"
        ".cover-hero h1 { font-size: 28pt; font-weight: 700; margin: 0 0 6mm 0; color: " + D["foreground"] + "; line-height: 1.15; letter-spacing: -0.01em; }\n"
        ".cover-hero .cover-subtitle { font-size: 14pt; color: " + D["accent_primary"] + "; margin: 0 0 14mm 0; font-weight: 500; }\n"
        ".cover-hero .cover-rule { width: 32mm; height: 2px; background: " + D["accent_primary"] + "; margin: 0 0 10mm 0; }\n"
        ".cover-hero .cover-meta { font-size: 11pt; color: " + D["foreground"] + "; opacity: 0.85; margin: 0 0 1.6em 0; }\n"
        ".cover-hero .cover-meta .label { color: " + D["accent_secondary"] + "; font-weight: 600; margin-right: 6px; }\n"
        ".cover-hero .cover-foot { position: absolute; bottom: 28mm; left: 24mm; font-size: 10pt; color: " + D["foreground"] + "; opacity: 0.75; }\n"
        ".cover-hero .cover-foot strong { color: " + D["foreground"] + "; opacity: 1; }\n"
        "h1 { font-size: 20pt; font-weight: 700; margin: 0 0 0.5em 0; color: " + L["foreground"] + "; letter-spacing: -0.005em; page-break-after: avoid; }\n"
        "h2 { font-size: 15pt; font-weight: 600; margin: 1.6em 0 0.4em 0; color: " + L["accent_primary"] + "; border-bottom: 1px solid " + L["border"] + "; padding-bottom: 0.25em; page-break-after: avoid; }\n"
        "h3 { font-size: 12pt; font-weight: 600; margin: 1.2em 0 0.4em 0; color: " + L["foreground"] + "; page-break-after: avoid; }\n"
        "h4 { font-size: 10.5pt; font-weight: 600; margin: 1em 0 0.3em 0; color: " + L["muted_foreground"] + "; text-transform: uppercase; letter-spacing: 0.05em; page-break-after: avoid; }\n"
        "code, pre { font-family: 'Consolas', 'Menlo', 'Courier New', monospace; font-size: 9.5pt; }\n"
        "code { background: " + L["secondary"] + "; padding: 1px 4px; border-radius: 3px; color: " + L["foreground"] + "; }\n"
        "pre { background: " + L["secondary"] + "; padding: 10px 12px; border-radius: 4px; border: 1px solid " + L["border"] + "; }\n"
        "table { border-collapse: collapse; width: 100%; font-size: 9pt; margin: 0.8em 0 1.1em; page-break-inside: avoid; }\n"
        "th, td { border: 1px solid " + L["border"] + "; padding: 6px 8px; vertical-align: top; }\n"
        "th { background: " + L["secondary"] + "; color: " + L["foreground"] + "; text-align: left; font-weight: 600; }\n"
        "tr:nth-child(even) td { background: " + L["card"] + "; }\n"
        "blockquote { border-left: 3px solid " + L["accent_primary"] + "; padding: 8px 14px; color: " + L["foreground"] + "; background: hsla(168, 55%, 38%, 0.06); margin: 0.8em 0; border-radius: 0 4px 4px 0; }\n"
        "blockquote p:last-child { margin-bottom: 0; }\n"
        "blockquote.callout-operator { border-left-color: " + L["accent_secondary"] + "; background: hsla(38, 80%, 50%, 0.08); }\n"
        "blockquote.callout-risk { border-left-color: " + L["destructive"] + "; background: hsla(0, 75%, 55%, 0.05); }\n"
        "hr { border: none; border-top: 1px solid " + L["border"] + "; margin: 1.2em 0; }\n"
        "a { color: " + L["accent_primary"] + "; text-decoration: none; border-bottom: 1px dotted " + L["accent_primary"] + "; }\n"
        "img { max-width: 100%; height: auto; }\n"
        "figure { margin: 1em 0; page-break-inside: avoid; }\n"
        "figcaption { font-size: 8.5pt; color: " + L["muted_foreground"] + "; font-style: italic; margin-top: 0.3em; }\n"
        ".source-cite { font-size: 8.5pt; color: " + L["muted_foreground"] + "; font-style: italic; margin-top: 0.3em; }\n"
        ".footer-string { string-set: footerline content(); }\n"
    )


def _build_cover_html(
    *,
    title: str,
    subtitle: str | None = None,
    program_id: str | None = None,
    discipline: str | None = None,
    issue_date: str | None = None,
    status_label: str | None = None,
    monogram_path: str | None = None,
) -> str:
    """Return the cover-page HTML fragment used by ``render_pdf_branded``."""
    monogram_html = ""
    if monogram_path and Path(monogram_path).is_file():
        # WeasyPrint accepts file:// URLs reliably across platforms.
        uri = Path(monogram_path).resolve().as_uri()
        monogram_html = f'<img class="cover-monogram" src="{uri}" alt="Holistika Research" />'

    rows: list[str] = []
    if program_id:
        rows.append(f'<div class="cover-meta"><span class="label">Programa:</span> {program_id}</div>')
    if discipline:
        rows.append(f'<div class="cover-meta"><span class="label">Disciplina:</span> {discipline}</div>')
    if status_label:
        rows.append(f'<div class="cover-meta"><span class="label">Estado:</span> {status_label}</div>')
    if issue_date:
        rows.append(f'<div class="cover-meta"><span class="label">Fecha de emisión:</span> {issue_date}</div>')

    subtitle_html = f'<div class="cover-subtitle">{subtitle}</div>' if subtitle else ""
    foot_html = (
        '<div class="cover-foot">'
        '<strong>Holistika Research</strong> · holistikaresearch.com'
        '</div>'
    )

    return (
        '<section class="cover-hero">'
        f'{monogram_html}'
        f'<h1>{title}</h1>'
        f'{subtitle_html}'
        '<div class="cover-rule"></div>'
        + "".join(rows)
        + foot_html
        + "</section>"
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
        # No markdown lib at all — degrade to plain renderer.
        return render_pdf(md_text, out_path, source_label=source_label)

    body_html = _md_lib.markdown(md_text, extensions=MD_EXTENSIONS)

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
