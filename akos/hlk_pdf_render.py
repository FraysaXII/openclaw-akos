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

- ``render_docx(md_text, out_path, *, source_label="hlk_pdf_render") -> int``
  Renders Markdown to DOCX via pandoc. Soft-succeeds with the markdown
  sidecar when pandoc is unavailable.

- ``MD_EXTENSIONS`` — list of ``markdown`` library extensions used by both
  PDF and HTML pipelines.
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
