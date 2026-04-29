#!/usr/bin/env python3
"""Render the brand-aligned ENISA dossier PDF (Initiative 27 P4).

Thin wrapper around ``akos.hlk_pdf_render.render_pdf_branded`` that:

1. Reads the canonical dossier markdown for a given program / language;
2. Strips the YAML frontmatter (the renderer does not display it);
3. Resolves the cover metadata (program, discipline, issue date, monogram);
4. Emits a brand-aligned PDF with the dark hero band cover + light body styling
   per ``BRAND_VISUAL_PATTERNS.md``;
5. Captures sha256 hashes of the source markdown and the rendered PDF for the
   Initiative 24 G-24-3 closure trail.

Usage::

    py scripts/render_dossier.py \\
        --program PRJ-HOL-FOUNDING-2026 \\
        --language es \\
        --out artifacts/exports/dossier-enisa-PRJ-HOL-FOUNDING-2026-2026-04-29.pdf

When ``--out`` is omitted, defaults to::

    artifacts/exports/dossier-enisa-<program>-<ISO-DATE>.pdf

Soft-success behaviour matches ``render_pdf_branded``: when no PDF renderer is
available, a markdown sidecar is written next to ``--out`` and the script
returns 0. The sha256 manifest still lands so the operator has trace data.

Exit codes:
    0 — PDF written (or soft-success markdown sidecar)
    1 — refusal (dossier missing / frontmatter unreadable)
    2 — usage error
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_pdf_render import render_pdf_branded  # noqa: E402

DEFAULT_PROGRAM = "PRJ-HOL-FOUNDING-2026"
DEFAULT_LANGUAGE = "es"
DEFAULT_PLANE = "advops"
DEFAULT_TOPIC_DIR = "enisa_evidence"

DOSSIER_TITLE_BY_LANGUAGE: dict[str, str] = {
    "es": "Dossier ENISA",
    "en": "ENISA Dossier",
}

DOSSIER_SUBTITLE_BY_LANGUAGE: dict[str, str] = {
    "es": "Empresa Emergente — Certificación",
    "en": "Empresa Emergente — Certification",
}

STATUS_BY_LANGUAGE: dict[str, str] = {
    "es": "P1-Audit ready",
    "en": "P1-Audit ready",
}

DISCIPLINE_BY_LANGUAGE: dict[str, str] = {
    "es": "Asesoría Jurídica + Certificación",
    "en": "Legal Counsel + Certification",
}

BOILERPLATE_LOGO_PATH = (
    REPO_ROOT.parent / "root_cd" / "boilerplate" / "public" / "holistika-short-100x100.svg"
)


def resolve_dossier_md(*, program: str, language: str) -> Path:
    """Return the canonical dossier markdown path for a given program + language."""
    return (
        REPO_ROOT
        / "docs"
        / "references"
        / "hlk"
        / "v3.0"
        / "_assets"
        / DEFAULT_PLANE
        / program
        / DEFAULT_TOPIC_DIR
        / f"dossier_{language}.md"
    )


def strip_frontmatter(md: str) -> str:
    """Remove the leading ``---\\n…\\n---\\n`` YAML block; the body of the
    dossier is what we render to PDF."""
    return re.sub(r"^---\s*\n.*?\n---\s*\n", "", md, count=1, flags=re.DOTALL)


def _sha256_of_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha256_of_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument(
        "--program",
        default=DEFAULT_PROGRAM,
        help=f"Program id (default: {DEFAULT_PROGRAM}).",
    )
    parser.add_argument(
        "--language",
        default=DEFAULT_LANGUAGE,
        choices=list(DOSSIER_TITLE_BY_LANGUAGE.keys()),
        help=f"Dossier language (default: {DEFAULT_LANGUAGE}).",
    )
    parser.add_argument(
        "--profile",
        default="dossier",
        choices=("dossier",),
        help="Visual profile for render_pdf_branded (default: dossier).",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output PDF path. Defaults to artifacts/exports/dossier-enisa-<program>-<ISO-DATE>.pdf.",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="Optional path to write a JSON manifest with sha256 hashes for the closure trail.",
    )
    parser.add_argument(
        "--issue-date",
        default=None,
        help="ISO date stamped on the cover and footer (default: today UTC).",
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Smoke-mode: only verify that the markdown source parses and the cover metadata resolves; no PDF written.",
    )
    args = parser.parse_args(argv)

    md_path = resolve_dossier_md(program=args.program, language=args.language)
    if not md_path.is_file():
        sys.stderr.write(
            f"render_dossier: REFUSED — dossier markdown not found at "
            f"{md_path.relative_to(REPO_ROOT)}.\n"
            f"  Authored at Initiative 27 P2 only for program={DEFAULT_PROGRAM} language={DEFAULT_LANGUAGE}.\n"
            f"  Add a sibling dossier_<language>.md under the same folder for additional languages.\n"
        )
        return 1

    md_text = md_path.read_text(encoding="utf-8")
    body = strip_frontmatter(md_text)
    if not body.strip():
        sys.stderr.write(
            f"render_dossier: REFUSED — dossier body is empty after frontmatter strip "
            f"({md_path.relative_to(REPO_ROOT)}).\n"
        )
        return 1

    issue_date = args.issue_date or _dt.datetime.now(_dt.UTC).date().isoformat()
    out_path: Path
    if args.out is not None:
        out_path = args.out
    else:
        out_path = REPO_ROOT / "artifacts" / "exports" / f"dossier-enisa-{args.program}-{issue_date}.pdf"

    monogram_path = str(BOILERPLATE_LOGO_PATH) if BOILERPLATE_LOGO_PATH.is_file() else None

    if args.smoke:
        print(
            f"render_dossier: smoke OK — dossier={md_path.relative_to(REPO_ROOT)} "
            f"body_chars={len(body)} cover_title={DOSSIER_TITLE_BY_LANGUAGE[args.language]!r} "
            f"program={args.program} issue_date={issue_date} "
            f"monogram={'present' if monogram_path else 'absent'}"
        )
        return 0

    out_path.parent.mkdir(parents=True, exist_ok=True)
    md_sidecar = out_path.with_suffix(".md")
    if not md_sidecar.is_file() or md_sidecar.read_text(encoding="utf-8") != md_text:
        md_sidecar.write_text(md_text, encoding="utf-8")

    rc = render_pdf_branded(
        body,
        out_path,
        profile=args.profile,
        title=DOSSIER_TITLE_BY_LANGUAGE[args.language],
        subtitle=DOSSIER_SUBTITLE_BY_LANGUAGE[args.language],
        program_id=args.program,
        discipline=DISCIPLINE_BY_LANGUAGE[args.language],
        issue_date=issue_date,
        status_label=STATUS_BY_LANGUAGE[args.language],
        monogram_path=monogram_path,
        source_label="render_dossier",
    )

    md_sha = _sha256_of_text(md_text)
    pdf_sha = _sha256_of_path(out_path) if out_path.is_file() else None

    manifest_data = {
        "program_id": args.program,
        "language": args.language,
        "profile": args.profile,
        "issue_date": issue_date,
        "source_md": str(md_path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "source_md_sha256": md_sha,
        "rendered_pdf": str(out_path).replace("\\", "/"),
        "rendered_pdf_sha256": pdf_sha,
        "monogram_path": monogram_path,
        "renderer_rc": rc,
    }

    if args.manifest is not None:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(json.dumps(manifest_data, indent=2, sort_keys=True), encoding="utf-8")
        print(f"render_dossier: manifest -> {args.manifest}")

    print(
        f"render_dossier: program={args.program} language={args.language} "
        f"md_sha256={md_sha[:16]}... "
        f"pdf_sha256={(pdf_sha[:16] + '...') if pdf_sha else 'absent (soft-success md sidecar only)'}"
    )
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
