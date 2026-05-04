#!/usr/bin/env python3
"""Split the monolithic ``artifacts/sql/compliance_mirror_upsert.sql`` into
per-table batches sized for MCP ``execute_sql`` calls (operator SQL gate).

Usage::

    py scripts/split_compliance_mirror_upsert.py
    py scripts/split_compliance_mirror_upsert.py --skip-tables goipoi_register_mirror
    py scripts/split_compliance_mirror_upsert.py --max-bytes 40000

Emits one ``.sql`` file per (table, chunk) under
``artifacts/sql/mirror-batches/<YYYYMMDD>/<NN>-<table>-<chunk>.sql`` and a
``manifest.json`` summarising statement counts + byte sizes per batch.

The intent is operator review then table-by-table apply via MCP
``execute_sql``. Each chunk wraps its INSERTs in a fresh ``BEGIN; ... COMMIT;``
so failures roll back at the batch level.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = ROOT / "artifacts" / "sql" / "compliance_mirror_upsert.sql"

TABLE_MARKER = re.compile(r"^--\s*compliance\.(\w+)\s+upserts[^\n]*\n", re.MULTILINE)


def split_by_table(body: str) -> dict[str, list[str]]:
    """Return {table_name: [insert_stmt, …]}.

    Each insert is a single SQL statement ending in ``;``.
    Comments and BEGIN/COMMIT framing in the source are dropped here; the
    caller decides chunking + framing.
    """
    sections: dict[str, list[str]] = {}
    matches = list(TABLE_MARKER.finditer(body))
    for i, m in enumerate(matches):
        table = m.group(1)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        chunk = body[start:end]
        statements = [
            s.strip() + ";"
            for s in chunk.split(";\n")
            if s.strip() and "INSERT INTO" in s and "ON CONFLICT" in s
        ]
        sections.setdefault(table, []).extend(statements)
    return sections


def chunk_statements(stmts: list[str], max_bytes: int) -> list[list[str]]:
    """Greedy chunking by byte budget."""
    out: list[list[str]] = []
    cur: list[str] = []
    cur_size = 0
    framing_overhead = len("BEGIN;\n") + len("\nCOMMIT;\n")
    for s in stmts:
        sz = len(s) + 1
        if cur and cur_size + sz + framing_overhead > max_bytes:
            out.append(cur)
            cur = []
            cur_size = 0
        cur.append(s)
        cur_size += sz
    if cur:
        out.append(cur)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=str(DEFAULT_INPUT))
    ap.add_argument("--max-bytes", type=int, default=40_000,
                    help="max bytes per batch (default 40 KB; safe for MCP execute_sql)")
    ap.add_argument("--skip-tables", nargs="*", default=[],
                    help="tables to skip (e.g. already-in-sync mirrors like goipoi_register_mirror)")
    ap.add_argument("--out-dir", default=None)
    args = ap.parse_args()

    src = Path(args.input)
    if not src.exists():
        print(f"ERROR: input not found: {src}", file=sys.stderr)
        return 2
    body = src.read_text(encoding="utf-8")
    sections = split_by_table(body)
    if not sections:
        print("ERROR: no '-- compliance.<table>_mirror upserts' markers found", file=sys.stderr)
        return 2

    today = dt.date.today().strftime("%Y%m%d")
    out_dir = Path(args.out_dir) if args.out_dir else ROOT / "artifacts" / "sql" / "mirror-batches" / today
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest: list[dict] = []
    table_idx = 0
    for table, stmts in sections.items():
        if table in args.skip_tables:
            print(f"  SKIP   {table:<40} ({len(stmts)} stmts)")
            manifest.append({"table": table, "skipped": True, "stmt_count": len(stmts)})
            continue
        chunks = chunk_statements(stmts, args.max_bytes)
        table_idx += 1
        for ci, chunk in enumerate(chunks, start=1):
            sql = "BEGIN;\n" + "\n".join(chunk) + "\nCOMMIT;\n"
            fname = f"{table_idx:02d}-{table}-chunk{ci:02d}.sql"
            (out_dir / fname).write_text(sql, encoding="utf-8")
            manifest.append({
                "file": fname,
                "table": table,
                "chunk_index": ci,
                "stmt_count": len(chunk),
                "byte_size": len(sql),
            })
            print(f"  WROTE  {fname:<60} stmts={len(chunk):>4} size={len(sql):>7} bytes")
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\nmanifest: {out_dir / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
