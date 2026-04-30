#!/usr/bin/env python3
"""Export the Holística company-dossier HTML preview to a deck-grade PDF.

Initiative 28 P5. Reads the rendered HTML at
``docs/presentations/holistika-company-dossier/index.html`` (built by
``scripts/build_company_deck.py``) and renders it to a 14-slide PDF using
WeasyPrint at the deck-native 1440 × 810 px page size.

Default output:
    artifacts/exports/holistika-company-dossier-enisa-2026-04-30.pdf

Usage::

    py scripts/export_company_deck_pdf.py
    py scripts/export_company_deck_pdf.py --out path/to/file.pdf

The script captures sha256 hashes for the source HTML and the rendered PDF
into a JSON manifest next to the PDF for the closure trail.

Why not Figma? The Figma REST API export path requires a personal access
token which is not connected here; the Figma deck remains the visual SSOT
(see ``figma-link.md``) but the deterministic, governed PDF is rendered
from the HTML preview which uses identical brand tokens and copy.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HTML_SOURCE = REPO_ROOT / "docs" / "presentations" / "holistika-company-dossier" / "index.html"
DEFAULT_OUT_DIR = REPO_ROOT / "artifacts" / "exports"
DEFAULT_OUT_NAME = "holistika-company-dossier-enisa-{date}.pdf"


def _sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument(
        "--source",
        type=Path,
        default=HTML_SOURCE,
        help=f"HTML source (default: {HTML_SOURCE.relative_to(REPO_ROOT)}).",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help=(
            f"Output PDF path. Defaults to "
            f"{(DEFAULT_OUT_DIR / DEFAULT_OUT_NAME).relative_to(REPO_ROOT)} "
            "with today's UTC date."
        ),
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="Optional JSON manifest path with sha256 hashes for the closure trail.",
    )
    args = parser.parse_args(argv)

    source: Path = args.source
    if not source.is_file():
        sys.stderr.write(
            f"export_company_deck_pdf: source HTML not found at "
            f"{source}. Run `py scripts/build_company_deck.py` first.\n"
        )
        return 1

    today = _dt.datetime.now(_dt.UTC).date().isoformat()
    if args.out is None:
        out_path = DEFAULT_OUT_DIR / DEFAULT_OUT_NAME.format(date=today)
    else:
        out_path = args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        from weasyprint import HTML, CSS  # type: ignore
    except ImportError:
        sys.stderr.write(
            "export_company_deck_pdf: WeasyPrint is required. "
            "Install via `py -m pip install --only-binary=:all: -r requirements-export.txt`.\n"
        )
        return 2

    html_bytes = source.read_bytes()
    html_sha = _sha256_bytes(html_bytes)

    # Override the default print @page rule to guarantee 1440x810 frame size
    # regardless of operator browser print settings. The HTML container uses a
    # flex column for the on-screen deck; we flatten it for print so every
    # `.slide` becomes a top-level block that respects page breaks.
    extra_css = CSS(
        string=(
            "@page { size: 1440px 810px; margin: 0; }"
            "html, body { background: white; margin: 0; padding: 0; }"
            ".deck-container { display: block !important; padding: 0 !important; gap: 0 !important; }"
            ".deck-header { display: none !important; }"
            ".slide {"
            "  display: block !important;"
            "  box-shadow: none !important;"
            "  border-radius: 0 !important;"
            "  margin: 0 !important;"
            "  width: 1440px !important;"
            "  height: 810px !important;"
            "  page-break-after: always !important;"
            "  page-break-inside: avoid !important;"
            "  break-after: page !important;"
            "  position: relative !important;"
            "  overflow: hidden !important;"
            "}"
            ".slide:last-child { page-break-after: auto !important; break-after: auto !important; }"
        )
    )

    base_url = source.parent.resolve().as_uri()
    HTML(filename=str(source), base_url=base_url).write_pdf(
        str(out_path), stylesheets=[extra_css]
    )

    pdf_bytes = out_path.read_bytes()
    pdf_sha = _sha256_bytes(pdf_bytes)

    manifest = {
        "initiative": "i28-investor-style-company-dossier",
        "generated_utc": _dt.datetime.now(_dt.UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "source_html": str(source.relative_to(REPO_ROOT)).replace("\\", "/"),
        "source_html_sha256": html_sha,
        "rendered_pdf": str(out_path).replace("\\", "/"),
        "rendered_pdf_sha256": pdf_sha,
        "rendered_pdf_bytes": len(pdf_bytes),
    }

    if args.manifest is not None:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
        print(f"export_company_deck_pdf: manifest -> {args.manifest}")
    else:
        # Always print a one-line summary even without --manifest.
        print(json.dumps(manifest, indent=2, sort_keys=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
