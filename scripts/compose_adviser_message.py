#!/usr/bin/env python3
"""Compose a draft adviser message fusing the four-layer methodology.

Initiative 24 P4 (D-IH-10). Reads canonical CSVs and produces a draft message
the operator finalises and sends. The composer **never** writes a real
recipient email or sends — those are operator actions at SMTP time. Per
``SOP-HLK_COMMUNICATION_METHODOLOGY_001.md`` the four layers are:

    Layer 1 — Brand foundation  (voice charter, archetype, register matrix)
    Layer 2 — Concept           (canonical CSV facts)
    Layer 3 — Use-case          (recipient + lens + sharing label + discipline)
    Layer 4 — Eloquence         (voice register / language / pronoun)

Voice register precedence (highest first): recipient profile -> discipline
default -> brand foundation default -> global default. The brand foundation
files at ``v3.0/Admin/O5-1/Marketing/Brand/`` are the authoritative voice
source per D-IH-17. While they are scaffold-staged
(``status: scaffold-awaiting-discovery``) the composer refuses to resolve
brand-foundation tokens unless ``--allow-scaffold-tokens`` is set explicitly
for dry-run.

Usage::

    py scripts/compose_adviser_message.py \
        --recipient POI-LEG-ENISA-LEAD-2026 \
        --discipline LEG \
        --program-id PRJ-HOL-FOUNDING-2026 \
        --evidence artifacts/exports/handoff-PRJ-HOL-FOUNDING-2026-2026-04-29.md \
        --out artifacts/exports/draft-LEG-2026-04-29.md \
        --format md

    py scripts/compose_adviser_message.py --recipient POI-LEG-ENISA-LEAD-2026 \
        --discipline LEG --program-id PRJ-HOL-FOUNDING-2026 --dry-run

Exit codes:
    0   — draft written (or dry-run) successfully
    1   — refusal (sentinels remain, brand foundation not ready, restricted leak, …)
    2   — usage error (missing CSV, unknown ref_id, …)

SOC: never inlines a real recipient email; only the GOI/POI ref_id leaves
the script. Operator inlines the address at SMTP step from the off-repo
identity store.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_adviser_disciplines_csv import (  # noqa: E402
    ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES,
)
from akos.hlk_goipoi_csv import GOIPOI_REGISTER_FIELDNAMES  # noqa: E402

HLK_COMPLIANCE = REPO_ROOT / "docs" / "references" / "hlk" / "compliance"
GOIPOI_CSV = HLK_COMPLIANCE / "GOI_POI_REGISTER.csv"
DISCIPLINES_CSV = HLK_COMPLIANCE / "ADVISER_ENGAGEMENT_DISCIPLINES.csv"
PROGRAM_REGISTRY_CSV = HLK_COMPLIANCE / "dimensions" / "PROGRAM_REGISTRY.csv"
BRAND_DIR = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "Marketing"
    / "Brand"
)
BRAND_VOICE = BRAND_DIR / "BRAND_VOICE_FOUNDATION.md"

GLOBAL_DEFAULT_REGISTER = "peer_consulting"
GLOBAL_DEFAULT_LANGUAGE = "bilingual"
SCAFFOLD_FRONTMATTER_RE = re.compile(r"^\s*status:\s*scaffold-awaiting-discovery", re.MULTILINE)


def _read_csv(path: Path, fieldnames: tuple[str, ...]) -> list[dict[str, str]]:
    if not path.is_file():
        sys.stderr.write(f"compose_adviser_message: missing {path}\n")
        raise SystemExit(2)
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if list(reader.fieldnames or []) != list(fieldnames):
            sys.stderr.write(
                f"compose_adviser_message: header drift in {path.name}\n"
                f"  expected: {list(fieldnames)}\n  got:      {reader.fieldnames}\n"
            )
            raise SystemExit(2)
        return [dict(r) for r in reader]


def load_goipoi() -> dict[str, dict[str, str]]:
    rows = _read_csv(GOIPOI_CSV, GOIPOI_REGISTER_FIELDNAMES)
    return {row["ref_id"].strip(): row for row in rows if row.get("ref_id")}


def load_disciplines() -> dict[str, dict[str, str]]:
    rows = _read_csv(DISCIPLINES_CSV, ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES)
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        did = (row.get("discipline_id") or "").strip()
        code = (row.get("discipline_code") or "").strip()
        if did:
            out[did] = row
        if code:
            out[code] = row
    return out


def load_programs() -> dict[str, dict[str, str]]:
    if not PROGRAM_REGISTRY_CSV.is_file():
        return {}
    with PROGRAM_REGISTRY_CSV.open(encoding="utf-8", newline="") as fh:
        return {row["program_id"].strip(): row for row in csv.DictReader(fh) if row.get("program_id")}


def brand_foundation_status() -> tuple[bool, str]:
    """Return (ready, status_text). ready=False means scaffold-staged."""
    if not BRAND_VOICE.is_file():
        return False, "absent"
    text = BRAND_VOICE.read_text(encoding="utf-8")
    if SCAFFOLD_FRONTMATTER_RE.search(text):
        return False, "scaffold-awaiting-discovery"
    return True, "active"


def resolve_voice_register(
    recipient: dict[str, str], discipline: dict[str, str] | None, brand_ready: bool
) -> tuple[str, str]:
    """Return (voice_register, source) per Layer 4 precedence.

    Source values: 'recipient', 'discipline', 'brand', 'global'.
    """
    rec_register = (recipient.get("voice_register") or "").strip()
    if rec_register:
        return rec_register, "recipient"
    disc_default = ""
    if discipline is not None:
        disc_default = (discipline.get("default_voice_register") or discipline.get("default_register") or "").strip()
    if disc_default:
        return disc_default, "discipline"
    if brand_ready:
        # Scaffold MD: read voice charter / archetype later when scaffolder writes it.
        return "peer_consulting", "brand"
    return GLOBAL_DEFAULT_REGISTER, "global"


def resolve_language(recipient: dict[str, str]) -> str:
    return (recipient.get("language_preference") or "").strip() or GLOBAL_DEFAULT_LANGUAGE


def resolve_pronoun(recipient: dict[str, str]) -> str:
    return (recipient.get("pronoun_register") or "").strip()


def resolve_sharing_label(recipient: dict[str, str]) -> str:
    sens = (recipient.get("sensitivity") or "").strip()
    if sens == "restricted":
        return "internal_only"
    if sens == "confidential":
        return "counsel_and_named_counterparty"
    if sens == "public":
        return "counsel_ok"
    return "counsel_ok"


def render_md(
    *,
    recipient: dict[str, str],
    discipline: dict[str, str],
    program: dict[str, str] | None,
    voice_register: str,
    voice_source: str,
    language: str,
    pronoun: str,
    sharing_label: str,
    evidence_path: Path | None,
) -> str:
    lines: list[str] = []
    lines.append("---")
    lines.append(f"composer: scripts/compose_adviser_message.py")
    lines.append(f"recipient_ref_id: {recipient['ref_id']}")
    lines.append(f"discipline_id: {discipline.get('discipline_id', '')}")
    lines.append(f"discipline_code: {discipline.get('discipline_code', '')}")
    if program:
        lines.append(f"program_id: {program['program_id']}")
        lines.append(f"program_code: {program.get('program_code', '')}")
    lines.append(f"voice_register: {voice_register}  # source: {voice_source}")
    lines.append(f"language_preference: {language}")
    if pronoun:
        lines.append(f"pronoun_register: {pronoun}")
    lines.append(f"sharing_label: {sharing_label}")
    lines.append(f"sensitivity: {recipient.get('sensitivity', '')}")
    lines.append("status: draft")
    lines.append("---")
    lines.append("")
    lines.append("# Draft adviser message (operator-finalised; never sent by composer)")
    lines.append("")
    lines.append("> **Recipient ref_id**: `" + recipient["ref_id"] + "`. Operator inlines the real email at SMTP step from the off-repo identity store. The composer never writes a real address into git artifacts.")
    lines.append("")
    lines.append("## Layer 1 — Brand voice")
    lines.append("")
    lines.append(f"- **Voice register**: `{voice_register}` (resolved from {voice_source})")
    lines.append(f"- **Language**: `{language}`")
    if pronoun:
        lines.append(f"- **Pronoun register**: `{pronoun}`")
    lines.append("")
    lines.append("Brand foundation: see [`BRAND_VOICE_FOUNDATION.md`](../../docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VOICE_FOUNDATION.md). The eloquence layer below operates **inside** the brand voice envelope — it does not override it.")
    lines.append("")
    lines.append("## Layer 2 — Concept (canonical facts)")
    lines.append("")
    if program:
        lines.append(f"- **Program**: `{program['program_id']}` — {program.get('program_name', '')}")
    lines.append(f"- **Discipline**: `{discipline.get('discipline_code', '')}` — {discipline.get('discipline_name', '')}")
    lines.append(f"- **Lens**: `{recipient.get('lens', '')}`")
    lines.append("")
    if evidence_path is not None and evidence_path.is_file():
        lines.append(f"Evidence bundle attached: [`{evidence_path.name}`]({evidence_path.as_posix()}). Cite individual facts by their `Q-…` / `INST-…` ids inside the message body.")
    else:
        lines.append("Operator: paste evidence inline from `ADVISER_OPEN_QUESTIONS.csv` and `FOUNDER_FILED_INSTRUMENTS.csv`. Cite by `Q-…` / `INST-…` id.")
    lines.append("")
    lines.append("## Layer 3 — Use-case")
    lines.append("")
    lines.append(f"- **Sharing label**: `{sharing_label}` (sensitivity `{recipient.get('sensitivity', '')}`)")
    lines.append(f"- **Recipient lens**: `{recipient.get('lens', '')}`")
    lines.append(f"- **Recipient class**: `{recipient.get('class', '')}`")
    lines.append("")
    lines.append("## Layer 4 — Eloquence (operator fills in)")
    lines.append("")
    lines.append("> **TODO operator** — write the actual message body in the voice register above. Keep the four-layer locked: every claim cites a CSV row id; tone matches `voice_register` × `pronoun_register`; no `restricted`-sensitivity rows are referenced unless the message is `internal_only`.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Pre-flight checklist (G-24-3 if this is the real adviser send)")
    lines.append("")
    lines.append("- [ ] Real recipient email resolved off-repo and inlined manually at SMTP step.")
    lines.append("- [ ] Sharing-label gate honoured (no `restricted` rows in body).")
    lines.append("- [ ] Discipline-lens match.")
    lines.append("- [ ] Brand voice match per `BRAND_REGISTER_MATRIX.md`.")
    lines.append("- [ ] Archive copy committed under `artifacts/exports/email-<program>-<discipline>-<DATE>.md` (gitignored under `artifacts/exports/` per Initiative 21 hygiene; commit the redacted version only when post-send).")
    lines.append("- [ ] SMTP `Sent` timestamp captured into the UAT report at send time.")
    lines.append("- [ ] Founder sign-off recorded in `operator-answers-wave2.yaml` Section 5.")
    lines.append("")
    return "\n".join(lines) + "\n"


def render_text(md_body: str) -> str:
    """Plain-text variant for paste-into-Gmail. Strips Mermaid blocks and
    most markdown markup; preserves bullets and headings as text."""
    # Strip mermaid code fences entirely.
    md_body = re.sub(r"```mermaid[\s\S]*?```", "", md_body)
    # Strip frontmatter
    md_body = re.sub(r"^---[\s\S]*?\n---\n", "", md_body, count=1)
    # Demote markdown headings to plain underlined-style.
    md_body = re.sub(r"^#+\s+(.*)$", r"\1", md_body, flags=re.MULTILINE)
    # Strip bold/italic markers but keep text.
    md_body = re.sub(r"\*\*(.*?)\*\*", r"\1", md_body)
    md_body = re.sub(r"\*(.*?)\*", r"\1", md_body)
    md_body = re.sub(r"`([^`]*)`", r"\1", md_body)
    # Convert markdown links to "text (url)".
    md_body = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", md_body)
    # Convert blockquote markers.
    md_body = re.sub(r"^>\s*", "", md_body, flags=re.MULTILINE)
    return md_body


def render_html(md_body: str) -> str:
    """Minimal HTML wrapping; relies on operator pasting into a HTML editor.

    Not a full markdown-to-HTML converter — keeps things safe and readable.
    For richer rendering, operator runs `markdown` package or pandoc on the
    output `.md`. This is a structural envelope for `--format html`.
    """
    body_html = (
        md_body.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return (
        "<!doctype html>\n<html><head><meta charset=\"utf-8\"><title>Adviser draft</title>\n"
        "<style>body{font-family:system-ui,Segoe UI,sans-serif;max-width:780px;margin:2rem auto;line-height:1.5;color:#222} pre{white-space:pre-wrap}</style>\n"
        "</head><body>\n<pre>" + body_html + "</pre>\n</body></html>\n"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--recipient", required=True, help="GOI/POI ref_id (e.g. POI-LEG-ENISA-LEAD-2026)")
    parser.add_argument("--discipline", required=True, help="Discipline code (LEG/FIS/IPT/BNK/CRT/NOT) or discipline_id")
    parser.add_argument("--program-id", default="", help="PRJ-HOL-style program_id (optional)")
    parser.add_argument("--evidence", type=Path, default=None, help="Optional path to evidence handoff bundle")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output path (defaults to stdout for --dry-run; required otherwise)",
    )
    parser.add_argument(
        "--format",
        choices=("md", "html", "text"),
        default="md",
        help="Output format",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print to stdout instead of writing")
    parser.add_argument(
        "--allow-scaffold-tokens",
        action="store_true",
        help="Allow brand foundation in scaffold-awaiting-discovery state (dry-run only)",
    )
    args = parser.parse_args(argv)

    goipoi = load_goipoi()
    recipient = goipoi.get(args.recipient.strip())
    if recipient is None:
        sys.stderr.write(f"compose_adviser_message: unknown recipient ref_id {args.recipient!r}\n")
        return 2

    if (recipient.get("sensitivity") or "").strip() == "restricted":
        sys.stderr.write(
            f"compose_adviser_message: REFUSED — recipient {args.recipient!r} is sensitivity=restricted; "
            "composer never produces drafts that cross plane boundaries.\n"
        )
        return 1

    disciplines = load_disciplines()
    discipline = disciplines.get(args.discipline.strip()) or disciplines.get(args.discipline.strip().upper())
    if discipline is None:
        sys.stderr.write(
            f"compose_adviser_message: unknown discipline {args.discipline!r}; "
            f"valid codes: {sorted(set(d.get('discipline_code', '') for d in disciplines.values() if d.get('discipline_code')))}\n"
        )
        return 2

    programs = load_programs()
    program: dict[str, str] | None = None
    if args.program_id:
        program = programs.get(args.program_id.strip())
        if program is None:
            sys.stderr.write(
                f"compose_adviser_message: unknown program_id {args.program_id!r} "
                "(not in PROGRAM_REGISTRY.csv)\n"
            )
            return 2

    brand_ready, brand_status = brand_foundation_status()
    if not brand_ready and not args.allow_scaffold_tokens:
        sys.stderr.write(
            f"compose_adviser_message: BRAND_FOUNDATION_NOT_READY (status: {brand_status})\n"
            f"  {BRAND_VOICE.relative_to(REPO_ROOT)} is scaffold-awaiting-discovery.\n"
            "  Operator fills operator-answers-wave2.yaml Section 2 then runs:\n"
            "    py scripts/wave2_backfill.py --section brand_voice\n"
            "  to flip the brand foundation MDs to status: active.\n"
            "  For dry-run preview before that, pass --allow-scaffold-tokens.\n"
        )
        return 1

    voice_register, voice_source = resolve_voice_register(recipient, discipline, brand_ready)
    language = resolve_language(recipient)
    pronoun = resolve_pronoun(recipient)
    sharing_label = resolve_sharing_label(recipient)

    md_body = render_md(
        recipient=recipient,
        discipline=discipline,
        program=program,
        voice_register=voice_register,
        voice_source=voice_source,
        language=language,
        pronoun=pronoun,
        sharing_label=sharing_label,
        evidence_path=args.evidence,
    )

    if args.format == "md":
        body = md_body
    elif args.format == "text":
        body = render_text(md_body)
    elif args.format == "html":
        body = render_html(md_body)
    else:
        sys.stderr.write(f"compose_adviser_message: unsupported format {args.format!r}\n")
        return 2

    if args.dry_run or args.out is None:
        sys.stdout.write(body)
        return 0

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(body, encoding="utf-8")
    print(f"compose_adviser_message: wrote {args.out.relative_to(REPO_ROOT) if args.out.is_relative_to(REPO_ROOT) else args.out} ({len(body)} chars; format={args.format})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
