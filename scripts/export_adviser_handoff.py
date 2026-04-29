#!/usr/bin/env python3
"""Export an emailable adviser handoff bundle for one or all disciplines.

Initiative 21 / P7 deliverable. Reads the canonical compliance CSVs (SSOTs):

- docs/references/hlk/compliance/ADVISER_ENGAGEMENT_DISCIPLINES.csv
- docs/references/hlk/compliance/GOI_POI_REGISTER.csv
- docs/references/hlk/compliance/ADVISER_OPEN_QUESTIONS.csv
- docs/references/hlk/compliance/FOUNDER_FILED_INSTRUMENTS.csv

…and writes a stable-ordered Markdown handoff (Cover -> Sharing legend -> Fact
pattern -> Filed instruments -> Open questions -> Exhibit list with relative links).

Markdown is the primary deliverable; PDF (via `pandoc`) is opt-in via `--format pdf`
(falls back to printing the resolved pandoc command if pandoc is unavailable).

Usage examples:

  py scripts/export_adviser_handoff.py --discipline all --format md \\
      --out artifacts/exports/handoff-smoke.md
  py scripts/export_adviser_handoff.py --discipline legal --program-id PRJ-HOL-FOUNDING-2026 \\
      --out artifacts/exports/legal-handoff-2026-04.md

Sensitivity gate: rows with `sensitivity == restricted` (in GOI/POI) are
filtered from the per-section text unless `--include-restricted` is passed.
The script never resolves real names (off-repo); it always emits ref_ids only.
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import hashlib
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HLK_COMPLIANCE = REPO_ROOT / "docs" / "references" / "hlk" / "compliance"
DISCIPLINES_CSV = HLK_COMPLIANCE / "ADVISER_ENGAGEMENT_DISCIPLINES.csv"
GOIPOI_CSV = HLK_COMPLIANCE / "GOI_POI_REGISTER.csv"
QUESTIONS_CSV = HLK_COMPLIANCE / "ADVISER_OPEN_QUESTIONS.csv"
INSTRUMENTS_CSV = HLK_COMPLIANCE / "FOUNDER_FILED_INSTRUMENTS.csv"


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = [dict(r) for r in reader]
    return fieldnames, rows


def _md_table(headers: list[str], rows: list[list[str]]) -> str:
    if not rows:
        return "_(no rows)_\n"
    head = "| " + " | ".join(headers) + " |"
    sep = "|" + "|".join(":---" for _ in headers) + "|"
    body = "\n".join("| " + " | ".join((c or "—") for c in row) + " |" for row in rows)
    return f"{head}\n{sep}\n{body}\n"


def _section_cover(*, program_id: str, disciplines: list[str], generated_iso: str, source_sha: str) -> str:
    return (
        "# External Adviser Handoff Package (export)\n\n"
        f"**Program**: `{program_id}`  \n"
        f"**Disciplines**: {', '.join(disciplines)}  \n"
        f"**Generated (UTC)**: {generated_iso}  \n"
        f"**Source git sha**: `{source_sha}`  \n"
        "**Owner plane**: External Adviser Engagement (ADVOPS) — PMO  \n"
        "**Naming posture**: GOI/POI ref_ids only; private parties never resolved in this artifact.\n\n"
    )


def _section_sharing_legend() -> str:
    return (
        "## Binding ladder & sharing legend\n\n"
        "Sensitivity bands map to sharing labels per `docs/references/hlk/compliance/PRECEDENCE.md` "
        "and Initiative 21 decision **D-CH-7**:\n\n"
        "| Sensitivity | Sharing label | Notes |\n"
        "|:---|:---|:---|\n"
        "| `public` | `counsel_ok` (free) | Public authorities (e.g. AEAT, ENISA, OEPM) and public-entity GOIs |\n"
        "| `internal` | `counsel_ok` | Internal-use rows; counsel and named counterparty may see |\n"
        "| `confidential` | `counsel_and_named_counterparty` | Limit forwarding; bank/desk-level details |\n"
        "| `restricted` | `internal_only` | Excluded from this export by default (use `--include-restricted` to include) |\n\n"
        "All ref_ids resolve via `docs/references/hlk/compliance/GOI_POI_REGISTER.csv`. "
        "Real names of private entities and persons are kept off-repo per "
        "`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md`.\n\n"
    )


def _section_fact_pattern(goipoi: list[dict[str, str]], program_id: str) -> str:
    rows = sorted(
        (r for r in goipoi if (r.get("program_id") or "").strip() == program_id),
        key=lambda r: (r.get("entity_kind", ""), r.get("ref_id", "")),
    )
    body_rows = [
        [
            r.get("ref_id", ""),
            r.get("entity_kind", ""),
            r.get("class", ""),
            r.get("display_name", ""),
            r.get("lens", ""),
            r.get("sensitivity", ""),
            r.get("role_owner", ""),
        ]
        for r in rows
    ]
    return (
        "## Fact pattern (GOI/POI ref_ids)\n\n"
        "Display names are obfuscated for private entities. See the canonical fact-pattern document "
        "[`FOUNDER_FACT_PATTERN_RELATED_ENTITIES.md`]"
        "(../../docs/references/hlk/v3.0/Admin/O5-1/People/Legal/FOUNDER_FACT_PATTERN_RELATED_ENTITIES.md).\n\n"
        + _md_table(
            ["ref_id", "entity_kind", "class", "display_name", "lens", "sensitivity", "role_owner"],
            body_rows,
        )
        + "\n"
    )


def _section_filed_instruments(
    instruments: list[dict[str, str]], program_id: str, discipline_codes: dict[str, str]
) -> str:
    rows = sorted(
        (r for r in instruments if (r.get("program_id") or "").strip() == program_id),
        key=lambda r: (r.get("discipline_id", ""), r.get("status", ""), r.get("instrument_id", "")),
    )
    body_rows = [
        [
            r.get("instrument_id", ""),
            r.get("discipline_id", ""),
            r.get("instrument_type", ""),
            r.get("jurisdiction", ""),
            r.get("status", ""),
            r.get("effective_or_filing_date", ""),
            r.get("storage_location", ""),
            r.get("primary_owner_role", ""),
            r.get("counterparty_goi_ref_id", ""),
        ]
        for r in rows
    ]
    return (
        "## Filed instruments\n\n"
        "Per-discipline filings (drafts → signed → filed → superseded). SSOT: "
        "`docs/references/hlk/compliance/FOUNDER_FILED_INSTRUMENTS.csv`.\n\n"
        + _md_table(
            [
                "instrument_id",
                "discipline_id",
                "instrument_type",
                "jurisdiction",
                "status",
                "effective_or_filing_date",
                "storage_location",
                "primary_owner_role",
                "counterparty_goi_ref_id",
            ],
            body_rows,
        )
        + "\n"
    )


def _section_open_questions(
    questions: list[dict[str, str]],
    program_id: str,
    disciplines: list[str],
    discipline_codes: dict[str, str],
) -> str:
    out = ["## Open questions and actions\n"]
    out.append(
        "Grouped by discipline. SSOT: `docs/references/hlk/compliance/ADVISER_OPEN_QUESTIONS.csv` "
        "(see also derived view `FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md`).\n\n"
    )
    for d in disciplines:
        rows = [
            r
            for r in questions
            if (r.get("program_id") or "").strip() == program_id
            and (r.get("discipline_id") or "").strip() == d
        ]
        rows.sort(key=lambda r: r.get("question_id", ""))
        out.append(f"### {discipline_codes.get(d, d.upper())} — `discipline_id = {d}`\n\n")
        body_rows = [
            [
                r.get("question_id", ""),
                r.get("question_or_action", ""),
                r.get("owner_role", ""),
                r.get("target_date", ""),
                r.get("status", ""),
                r.get("poi_ref_id", "") or r.get("goi_ref_id", ""),
                r.get("evidence_pointer", ""),
            ]
            for r in rows
        ]
        out.append(
            _md_table(
                ["question_id", "question_or_action", "owner_role", "target_date", "status", "stakeholder", "evidence"],
                body_rows,
            )
        )
        out.append("\n")
    return "".join(out)


def _section_exhibits(
    questions: list[dict[str, str]],
    instruments: list[dict[str, str]],
    program_id: str,
    disciplines: list[str],
) -> str:
    rels: set[str] = set()
    for r in questions:
        if (r.get("program_id") or "").strip() != program_id:
            continue
        if (r.get("discipline_id") or "").strip() not in disciplines:
            continue
        ev = (r.get("evidence_pointer") or "").strip()
        if ev:
            for piece in ev.split(";"):
                p = piece.strip()
                if p:
                    rels.add(p)
    for r in instruments:
        if (r.get("program_id") or "").strip() != program_id:
            continue
        if (r.get("discipline_id") or "").strip() not in disciplines:
            continue
        vl = (r.get("vault_link") or "").strip()
        if vl:
            rels.add(vl)
    rows = sorted(rels)
    body_rows = [[p, ("present" if (REPO_ROOT / p).exists() else "missing")] for p in rows]
    return (
        "## Exhibit list (relative paths)\n\n"
        "Cross-references from open questions and filed instruments. Operator validates before sending.\n\n"
        + _md_table(["relative_path", "presence"], body_rows)
        + "\n"
    )


_TD_INLINE_TAGS_RE = re.compile(r"</?(?:code|a|em|strong|span|i|b)(?:\s[^>]*)?>", re.IGNORECASE)


def _flatten_td_inlines(html: str) -> str:
    """Strip nested inline tags inside `<td>...</td>` cells.

    fpdf2's `write_html` raises `NotImplementedError: Unsupported nested HTML tags
    inside <td>` when cells contain `<code>`, `<a>`, etc. The handoff Markdown
    is heavy on `ref_id` codes inside table cells; flatten those wrappers but
    keep the text so the PDF still shows the GOI/POI ids and links inline.
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


def _render_pdf(md_text: str, out_path: "Path") -> int:
    """Render Markdown to PDF using WeasyPrint, fpdf2, or pandoc.

    Initiative 22 P6 (D-IH-4): try renderers in this order:
      1. WeasyPrint   — best CSS fidelity; requires native Cairo/Pango (Windows: GTK3 runtime).
      2. fpdf2        — pure-Python, zero native deps; default fallback on Windows.
      3. pandoc       — external binary fallback.
    If none are available, write markdown only and return 0 (soft success — the
    smoke profile SKIPs the PDF lane gracefully).
    """
    try:
        import markdown as _md_lib  # type: ignore
    except ImportError:
        _md_lib = None

    if _md_lib is not None:
        html_body = _md_lib.markdown(
            md_text, extensions=["tables", "fenced_code", "toc", "sane_lists", "attr_list"]
        )
        html_doc = (
            "<!DOCTYPE html><html><head><meta charset=\"utf-8\">"
            f"<style>{_PDF_CSS}</style></head><body>{html_body}</body></html>"
        )

        # Renderer 1: WeasyPrint (best CSS fidelity; needs native Cairo/Pango)
        try:
            from weasyprint import HTML  # type: ignore
            try:
                HTML(string=html_doc).write_pdf(str(out_path))
                print(f"export_adviser_handoff: WeasyPrint wrote PDF -> {out_path}")
                return 0
            except Exception as exc:
                print(
                    f"warning: WeasyPrint installed but rendering failed ({exc!r}); "
                    "falling back to fpdf2. On Windows install GTK3 runtime to enable WeasyPrint.",
                    file=sys.stderr,
                )
        except Exception:
            pass

        # Renderer 2: fpdf2 (pure-Python, zero native deps)
        try:
            from fpdf import FPDF  # type: ignore
            try:
                pdf = FPDF(orientation="P", unit="mm", format="A4")
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_page()
                pdf.set_margins(left=15, top=15, right=15)

                # fpdf2's built-in fonts are Latin-1 only. Register a Unicode TTF
                # so GOI/POI ref_ids, en-dashes, and Spanish glyphs render correctly.
                font_candidates = [
                    ("SegoeUI", "C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/segoeuii.ttf"),
                    ("Arial", "C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/ariali.ttf"),
                    ("DejaVuSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf"),
                ]
                family = "Helvetica"
                for fam, regular, bold, italic in font_candidates:
                    if Path(regular).is_file():
                        pdf.add_font(fam, "", regular)
                        if Path(bold).is_file():
                            pdf.add_font(fam, "B", bold)
                        if Path(italic).is_file():
                            pdf.add_font(fam, "I", italic)
                        family = fam
                        break
                pdf.set_font(family, size=10)

                # fpdf2's write_html cannot render nested inline tags inside <td>.
                # Flatten <code>, <a>, <em>, <strong>, <span> inside table cells so
                # the table layout still works; raw text content is preserved.
                fpdf_html = _flatten_td_inlines(html_body)
                pdf.write_html(fpdf_html, ul_bullet_char="-", li_prefix_color=(80, 80, 80))
                pdf.output(str(out_path))
                print(f"export_adviser_handoff: fpdf2 wrote PDF -> {out_path}")
                return 0
            except Exception as exc:
                print(
                    f"warning: fpdf2 installed but rendering failed ({exc!r}); falling back to pandoc.",
                    file=sys.stderr,
                )
        except Exception as exc:
            print(f"warning: fpdf2 unavailable ({exc!r}); falling back to pandoc.", file=sys.stderr)

    # Renderer 3: pandoc
    pandoc = shutil.which("pandoc")
    md_tmp = out_path.with_suffix(".md")
    if not md_tmp.is_file():
        md_tmp.write_text(md_text, encoding="utf-8")
    if not pandoc:
        print(
            "warning: no PDF renderer available (markdown / WeasyPrint / fpdf2 / pandoc all missing); "
            f"wrote markdown only at {md_tmp}. To enable PDF, run "
            "`py -m pip install --only-binary=:all: -r requirements-export.txt` "
            "(installs fpdf2 for a pure-Python path).",
            file=sys.stderr,
        )
        # Soft-success: caller still has the markdown source; profile gates can SKIP.
        return 0
    cmd = [pandoc, str(md_tmp), "-o", str(out_path)]
    print("running:", " ".join(cmd))
    rc = subprocess.call(cmd)
    if rc != 0:
        print("error: pandoc returned", rc, file=sys.stderr)
        return rc
    print(f"export_adviser_handoff: pandoc wrote PDF -> {out_path}")
    return 0


def _git_sha() -> str:
    try:
        sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=str(REPO_ROOT), stderr=subprocess.DEVNULL
        ).decode().strip()
        return sha or "unknown"
    except Exception:
        return "unknown"


def build_markdown(
    *,
    program_id: str,
    selected_disciplines: list[str],
    discipline_codes: dict[str, str],
    goipoi: list[dict[str, str]],
    questions: list[dict[str, str]],
    instruments: list[dict[str, str]],
    include_restricted: bool,
    generated_iso: str,
    source_sha: str,
) -> str:
    if not include_restricted:
        goipoi = [r for r in goipoi if (r.get("sensitivity") or "").strip() != "restricted"]

    parts: list[str] = []
    parts.append(_section_cover(
        program_id=program_id,
        disciplines=selected_disciplines,
        generated_iso=generated_iso,
        source_sha=source_sha,
    ))
    parts.append(_section_sharing_legend())
    parts.append(_section_fact_pattern(goipoi, program_id))
    parts.append(_section_filed_instruments(instruments, program_id, discipline_codes))
    parts.append(_section_open_questions(questions, program_id, selected_disciplines, discipline_codes))
    parts.append(_section_exhibits(questions, instruments, program_id, selected_disciplines))
    parts.append(
        "## Provenance\n\n"
        f"- Generator: `scripts/export_adviser_handoff.py` (Initiative 21 / P7).\n"
        f"- Source git sha: `{source_sha}`.\n"
        f"- Generated (UTC): {generated_iso}.\n"
        "- SSOTs: `ADVISER_ENGAGEMENT_DISCIPLINES.csv`, `GOI_POI_REGISTER.csv`, "
        "`ADVISER_OPEN_QUESTIONS.csv`, `FOUNDER_FILED_INSTRUMENTS.csv`.\n"
        "- Plane SOP: "
        "[`SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md`]"
        "(../../docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md).\n"
    )
    return "\n".join(parts)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument(
        "--discipline",
        required=True,
        help="Discipline id (e.g. legal, fiscal, ip, banking, certification, notary) or 'all'.",
    )
    parser.add_argument(
        "--program-id",
        default="PRJ-HOL-FOUNDING-2026",
        help="Program id to filter on (default: PRJ-HOL-FOUNDING-2026).",
    )
    parser.add_argument(
        "--format",
        choices=("md", "pdf"),
        default="md",
        help="Output format (md primary; pdf via pandoc).",
    )
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Output file path.",
    )
    parser.add_argument(
        "--include-restricted",
        action="store_true",
        help="Include rows with sensitivity=restricted (default: excluded).",
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Smoke-mode: write to a temp markdown and exit 0 if rendering succeeded.",
    )
    args = parser.parse_args(argv)

    for p in (DISCIPLINES_CSV, GOIPOI_CSV, QUESTIONS_CSV, INSTRUMENTS_CSV):
        if not p.is_file():
            print(f"error: missing canonical CSV {p}", file=sys.stderr)
            return 2

    _, disc_rows = _read_csv(DISCIPLINES_CSV)
    discipline_codes = {r["discipline_id"]: r.get("discipline_code", "") for r in disc_rows}
    valid = list(discipline_codes.keys())

    if args.discipline == "all":
        selected = list(valid)
    elif args.discipline in valid:
        selected = [args.discipline]
    else:
        print(
            f"error: unknown discipline '{args.discipline}'. valid: {', '.join(valid)} or 'all'.",
            file=sys.stderr,
        )
        return 2

    _, goipoi = _read_csv(GOIPOI_CSV)
    _, questions = _read_csv(QUESTIONS_CSV)
    _, instruments = _read_csv(INSTRUMENTS_CSV)

    generated_iso = _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    source_sha = _git_sha()

    md = build_markdown(
        program_id=args.program_id,
        selected_disciplines=selected,
        discipline_codes=discipline_codes,
        goipoi=goipoi,
        questions=questions,
        instruments=instruments,
        include_restricted=args.include_restricted,
        generated_iso=generated_iso,
        source_sha=source_sha,
    )

    out_path: Path = args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if args.format == "md":
        out_path.write_text(md, encoding="utf-8")
    else:
        md_tmp = out_path.with_suffix(".md")
        md_tmp.write_text(md, encoding="utf-8")
        rc = _render_pdf(md, out_path)
        if rc != 0:
            return rc

    sha = hashlib.sha256(md.encode("utf-8")).hexdigest()[:16]
    print(
        f"export_adviser_handoff: wrote {out_path} "
        f"({len(md.encode('utf-8'))} bytes, md_sha256_prefix={sha})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
