"""Initiative 21 / P2 helper: introspect raw legal-transcript markdown.

This script is a one-shot helper used during P2 to inspect the existing
``docs/references/hlk/business-intent/delete-legal-transcripts/*.md`` files
on Windows where NFD-encoded filenames cause friction for editors.

Usage::

    py scripts/_redact_helper_p2.py preview <relative-path>
    py scripts/_redact_helper_p2.py preview-all
    py scripts/_redact_helper_p2.py rewrite <relative-path> <out-path>

This script is intentionally not wired into ``validate_hlk.py``; it can be
deleted after P2 completes.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TRANSCRIPT_DIR = REPO_ROOT / "docs" / "references" / "hlk" / "business-intent" / "delete-legal-transcripts"


def list_md() -> list[str]:
    out: list[str] = []
    for f in sorted(os.listdir(TRANSCRIPT_DIR)):
        if f.endswith(".md") and f != "README.md":
            out.append(f)
    return out


def _read(p: Path) -> tuple[str, str]:
    raw = p.read_bytes()
    for enc in ("utf-8-sig", "utf-16", "utf-16-le", "utf-16-be", "cp1252", "latin-1"):
        try:
            return raw.decode(enc), enc
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace"), "utf-8 (replace)"


def preview(name: str, limit: int = 80) -> None:
    p = TRANSCRIPT_DIR / name
    text, enc = _read(p)
    lines = text.splitlines()
    print(f"=== {name} :: encoding={enc} :: {len(lines)} lines :: {len(text)} chars ===")
    for ln in lines[:limit]:
        print(ln)


def preview_all(limit: int = 60) -> None:
    for n in list_md():
        preview(n, limit=limit)
        print()


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (OSError, ValueError):
            pass
    if len(sys.argv) < 2:
        print(__doc__)
        return 0
    cmd = sys.argv[1]
    if cmd == "list":
        for n in list_md():
            print(n)
        return 0
    if cmd == "preview":
        if len(sys.argv) < 3:
            print("usage: preview <name>")
            return 1
        preview(sys.argv[2])
        return 0
    if cmd == "preview-all":
        preview_all()
        return 0
    print("unknown command:", cmd)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
