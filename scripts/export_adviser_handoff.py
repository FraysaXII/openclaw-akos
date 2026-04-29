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
# Bootstrap: import `akos.*` when this script is invoked directly.
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

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


# Initiative 24 follow-up (2026-04-29): the PDF rendering chain (WeasyPrint
# -> fpdf2 -> pandoc) now lives in `akos/hlk_pdf_render.py` so both this
# script and `scripts/compose_adviser_message.py` share one canonical path.
# The local _render_pdf wrapper preserves the existing call site and label.
from akos.hlk_pdf_render import render_pdf as _render_pdf_shared  # noqa: E402
from akos.hlk_pdf_render import render_pdf_branded as _render_pdf_branded_shared  # noqa: E402


def _render_pdf(md_text: str, out_path: "Path") -> int:
    """Initiative 22 P6 (D-IH-4) PDF render: thin wrapper over the shared helper."""
    return _render_pdf_shared(md_text, out_path, source_label="export_adviser_handoff")


def _render_pdf_branded(
    md_text: str,
    out_path: "Path",
    *,
    program_id: str,
    discipline_label: str,
    issue_date: str,
) -> int:
    """Initiative 27 P1 branded variant: thin wrapper over render_pdf_branded.

    Adds the dossier appendix cover (dark hero band + program/discipline strip)
    so the appendix PDF visually pairs with the dossier PDF when stapled or
    sent together.
    """
    monogram = REPO_ROOT.parent / "root_cd" / "boilerplate" / "public" / "holistika-short-100x100.svg"
    return _render_pdf_branded_shared(
        md_text,
        out_path,
        profile="dossier",
        title="Apéndice — Cuestionario asesores",
        subtitle="Fact-pattern, instrumentos, preguntas abiertas",
        program_id=program_id,
        discipline=discipline_label,
        issue_date=issue_date,
        status_label="Anexo al dossier ENISA",
        monogram_path=str(monogram) if monogram.is_file() else None,
        source_label="export_adviser_handoff_branded",
    )


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
        choices=("md", "pdf", "html", "text"),
        default="md",
        help="Output format. md primary; pdf via WeasyPrint/fpdf2/pandoc; html (Initiative 24 P5) wraps the md body in a single-file HTML envelope; text (Initiative 24 P5) emits a paste-into-Gmail plain-text body that strips Mermaid blocks and most markup.",
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
    parser.add_argument(
        "--profile",
        choices=("default", "dossier"),
        default="default",
        help=(
            "Visual profile for --format pdf. 'dossier' adds the brand-aligned "
            "cover hero band + body styling per BRAND_VISUAL_PATTERNS.md "
            "(Initiative 27 P1) so the appendix pairs visually with the ENISA "
            "dossier. 'default' keeps the legacy generic styling."
        ),
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
    elif args.format == "html":
        out_path.write_text(_render_html(md), encoding="utf-8")
    elif args.format == "text":
        out_path.write_text(_render_text(md), encoding="utf-8")
    else:
        md_tmp = out_path.with_suffix(".md")
        md_tmp.write_text(md, encoding="utf-8")
        if args.profile == "dossier":
            issue_date_iso = generated_iso.split("T", 1)[0]
            disc_label = (
                ", ".join(discipline_codes.get(d, d) for d in selected)
                if selected
                else "Asesores"
            )
            rc = _render_pdf_branded(
                md,
                out_path,
                program_id=args.program_id,
                discipline_label=disc_label,
                issue_date=issue_date_iso,
            )
        else:
            rc = _render_pdf(md, out_path)
        if rc != 0:
            return rc

    sha = hashlib.sha256(md.encode("utf-8")).hexdigest()[:16]
    print(
        f"export_adviser_handoff: wrote {out_path} "
        f"({len(md.encode('utf-8'))} bytes, md_sha256_prefix={sha})"
    )
    return 0


def _render_html(md_body: str) -> str:
    """Initiative 24 P5: minimal single-file HTML wrapper around the MD body.

    Goal: paste-into-email-client friendly, not a full markdown→HTML
    converter. We escape the body and wrap in a styled `<pre>` so structure
    survives. For richer rendering operators run `markdown` library or
    pandoc on the .md output instead.
    """
    body_html = (
        md_body.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return (
        "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">\n"
        "<title>Adviser handoff</title>\n"
        "<style>body{font-family:system-ui,Segoe UI,sans-serif;max-width:780px;margin:2rem auto;line-height:1.5;color:#222}"
        " pre{white-space:pre-wrap;font-family:ui-monospace,Consolas,monospace;font-size:14px}</style>\n"
        "</head><body>\n<pre>" + body_html + "</pre>\n</body></html>\n"
    )


def _render_text(md_body: str) -> str:
    """Initiative 24 P5: plain-text body for paste-into-Gmail.

    Strips Mermaid code blocks (which would render as raw text in plain
    email and confuse readers), demotes markdown headings, removes bold/
    italic markers, converts ``[text](url)`` to ``text (url)``, and
    flattens blockquote prefixes. Preserves bullets, numbered lists, and
    overall structure as visible text.
    """
    import re as _re

    text = _re.sub(r"```mermaid[\s\S]*?```", "", md_body)
    text = _re.sub(r"^---[\s\S]*?\n---\n", "", text, count=1)
    text = _re.sub(r"^#+\s+(.*)$", r"\1", text, flags=_re.MULTILINE)
    text = _re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = _re.sub(r"\*(.*?)\*", r"\1", text)
    text = _re.sub(r"`([^`]*)`", r"\1", text)
    text = _re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", text)
    text = _re.sub(r"^>\s*", "", text, flags=_re.MULTILINE)
    return text


if __name__ == "__main__":
    sys.exit(main())
