#!/usr/bin/env python3
"""Initiative 21 / P2 — redact pushed transcripts in delete-legal-transcripts/.

Forward-only redaction pass per decision D-CH-2: substitutes obvious private
names and personal paths in the *current tip* of the existing markdown
transcripts with the corresponding ``POI-*`` / ``GOI-*`` ``ref_id`` from
``GOI_POI_REGISTER.csv``. Does **not** rewrite git history.

Idempotent: running again on a redacted file is a no-op.

Usage::

    py scripts/redact_transcripts_p2.py --dry-run
    py scripts/redact_transcripts_p2.py --apply
    py scripts/redact_transcripts_p2.py --apply --report reports/p2-redaction-diff.md

This script is targeted at the named files; new transcripts must be redacted
at ingestion time per ``SOP-HLK_TRANSCRIPT_REDACTION_001.md``.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TRANSCRIPT_DIR = REPO_ROOT / "docs" / "references" / "hlk" / "business-intent" / "delete-legal-transcripts"


# Substitutions are applied in declaration order. Each tuple is
# (compiled-regex, replacement, human-readable label).
SUBS: list[tuple[re.Pattern[str], str, str]] = [
    (re.compile(r"Ayúdate\s+Pymes", flags=re.IGNORECASE), "GOI-ADV-ENTITY-2026", "adviser firm"),
    (re.compile(r"Ayudate\s+Pymes", flags=re.IGNORECASE), "GOI-ADV-ENTITY-2026", "adviser firm (no accent)"),
    (re.compile(r"\bCarmi\b"), "POI-LEG-ENISA-LEAD-2026", "ENISA-track adviser first name"),
    (re.compile(r"\bJorge\b"), "POI-ADV-INTAKE-LEAD-2026", "intake-stage adviser first name"),
    (re.compile(r"^source:\s*/Users/[^\n]*", flags=re.MULTILINE), "source: <off-repo per SOP-HLK_TRANSCRIPT_REDACTION_001>", "personal source path"),
]


REDACTION_HEADER = (
    "<!-- Initiative 21 / P2 redacted forward-only per SOP-HLK_TRANSCRIPT_REDACTION_001 -->\n"
    "<!-- Substitutions: ref_ids resolve in docs/references/hlk/compliance/GOI_POI_REGISTER.csv -->\n"
)


def _read(p: Path) -> tuple[str, str]:
    raw = p.read_bytes()
    for enc in ("utf-8-sig", "utf-16", "utf-16-le", "utf-16-be"):
        try:
            return raw.decode(enc), enc
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("utf-8", raw, 0, 1, "no candidate encoding decoded the file")


def _redact(text: str) -> tuple[str, list[tuple[str, int]]]:
    out = text
    counts: list[tuple[str, int]] = []
    for pat, repl, label in SUBS:
        new, n = pat.subn(repl, out)
        if n:
            counts.append((label, n))
        out = new
    if "Initiative 21 / P2 redacted forward-only" not in out:
        if out.startswith("---"):
            end = out.find("\n---", 4)
            if end != -1:
                end_nl = out.find("\n", end + 4)
                if end_nl != -1:
                    out = out[: end_nl + 1] + "\n" + REDACTION_HEADER + out[end_nl + 1 :]
                else:
                    out = out + "\n\n" + REDACTION_HEADER
            else:
                out = REDACTION_HEADER + out
        else:
            out = REDACTION_HEADER + out
    return out, counts


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (OSError, ValueError):
            pass
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Write redacted files (otherwise dry-run)")
    parser.add_argument("--report", type=Path, default=None, help="Write redaction report markdown")
    parser.add_argument("--dry-run", action="store_true", help="(default) print plan only")
    args = parser.parse_args()

    if not TRANSCRIPT_DIR.is_dir():
        print(f"error: missing {TRANSCRIPT_DIR}", file=sys.stderr)
        return 1

    rows: list[dict[str, object]] = []
    for name in sorted(p.name for p in TRANSCRIPT_DIR.iterdir()):
        if not name.endswith(".md") or name == "README.md":
            continue
        p = TRANSCRIPT_DIR / name
        try:
            text, enc = _read(p)
        except UnicodeDecodeError:
            rows.append({"name": name, "encoding": "binary", "skip": True, "counts": [], "bytes_in": p.stat().st_size, "bytes_out": p.stat().st_size})
            continue
        new_text, counts = _redact(text)
        rows.append(
            {
                "name": name,
                "encoding": enc,
                "skip": False,
                "counts": counts,
                "bytes_in": len(text.encode("utf-8")),
                "bytes_out": len(new_text.encode("utf-8")),
            }
        )
        if args.apply:
            p.write_text(new_text, encoding="utf-8", newline="\n")

    print("\n  Redaction plan (Initiative 21 / P2)")
    print("  " + "=" * 40)
    for r in rows:
        tag = "SKIP (binary)" if r["skip"] else r["encoding"]
        c = ", ".join(f"{lab}={n}" for lab, n in r["counts"]) if r["counts"] else "(no matches; idempotent / nothing to redact)"
        print(f"  - {r['name']}\n      encoding={tag}; bytes_in={r['bytes_in']}; bytes_out={r['bytes_out']}\n      {c}")
    print()
    print("  Dry-run; pass --apply to write." if not args.apply else "  Applied.")

    if args.report:
        lines = ["# Initiative 21 — P2 redaction diff", ""]
        lines.append(f"Generated: {Path(args.report).name}; mode={'apply' if args.apply else 'dry-run'}")
        lines.append("")
        lines.append("| File | encoding | bytes_in | bytes_out | substitutions |")
        lines.append("|:-----|:---------|---------:|----------:|:--------------|")
        for r in rows:
            tag = "binary" if r["skip"] else r["encoding"]
            c = "; ".join(f"{lab}={n}" for lab, n in r["counts"]) if r["counts"] else "—"
            lines.append(f"| `{r['name']}` | {tag} | {r['bytes_in']} | {r['bytes_out']} | {c} |")
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"  report: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
