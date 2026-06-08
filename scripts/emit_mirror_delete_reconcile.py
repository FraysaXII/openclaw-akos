#!/usr/bin/env python3
"""Append delete-reconciliation to an emitted mirror-upsert.sql (I95 / DB-01).

WHY
---
``sync_compliance_mirrors_from_csv.py`` emits UPSERTs only (``INSERT ... ON
CONFLICT DO UPDATE``). That keeps the mirror current for added/changed rows but
CANNOT shrink it: when rows are REMOVED from a canonical CSV (e.g. the BT-09
de-densification took CAPABILITY_REGISTRY 1,119 -> 93 and process_list 1,207 ->
496), the deleted rows orphan in the Supabase ``compliance.*_mirror`` tables.
A faithful mirror of a SSOT must delete what the SSOT deleted.

WHAT
----
This post-processor parses the emitted SQL, collects each mirror table's primary
key (from ``ON CONFLICT (<pk>)``) and the full set of PK values being upserted,
and appends — inside the same transaction, just before ``COMMIT;`` — one
``DELETE FROM compliance.<table> WHERE <pk> NOT IN (<current pk set>);`` per
table. The result is an idempotent FULL SYNC: after apply, each mirror equals
its CSV exactly (no orphans, no partial state — the apply is single-transaction).

SAFETY
------
* Two-plane doctrine: ``compliance.*_mirror`` is DERIVED (T2) from the git CSV
  SSOT (T1), so delete-not-in-CSV is correct, not data loss.
* Composite-PK tables (``ON CONFLICT (a, b)``) are SKIPPED (no simple NOT IN).
* Tables with zero emitted rows are SKIPPED (never emits ``WHERE pk NOT IN ()``
  which would be a syntax error / accidental full wipe).
* Opt-in: the emitter default stays upsert-only; the mirror-sync workflow opts
  in explicitly.

Usage::

    py scripts/emit_mirror_delete_reconcile.py --sql mirror-upsert.sql   # rewrites in place
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_INSERT_RE = re.compile(
    r"INSERT INTO compliance\.(?P<tbl>[a-z0-9_]+) \((?P<cols>.*?)\) VALUES \((?P<vals>.*)\) "
    r"ON CONFLICT \((?P<pk>[a-z0-9_, ]+)\) DO",
    re.IGNORECASE,
)


def split_sql_tuple(s: str) -> list[str]:
    """Split a top-level comma-separated SQL value list, respecting single-quoted
    strings (with '' escapes) and parentheses (e.g. ``now()``)."""
    out: list[str] = []
    cur: list[str] = []
    depth = 0
    in_q = False
    i = 0
    n = len(s)
    while i < n:
        ch = s[i]
        if in_q:
            cur.append(ch)
            if ch == "'":
                if i + 1 < n and s[i + 1] == "'":
                    cur.append("'")
                    i += 2
                    continue
                in_q = False
            i += 1
            continue
        if ch == "'":
            in_q = True
            cur.append(ch)
        elif ch == "(":
            depth += 1
            cur.append(ch)
        elif ch == ")":
            depth -= 1
            cur.append(ch)
        elif ch == "," and depth == 0:
            out.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
        i += 1
    if cur:
        out.append("".join(cur).strip())
    return out


def collect_pks(sql_text: str) -> dict[str, tuple[str, list[str]]]:
    """Return {table: (pk_column, [pk_value_literals])} for single-PK mirrors."""
    acc: dict[str, tuple[str, list[str]]] = {}
    skip_composite: set[str] = set()
    for line in sql_text.splitlines():
        m = _INSERT_RE.search(line)
        if not m:
            continue
        tbl = m.group("tbl")
        pk = m.group("pk").strip()
        if "," in pk:  # composite PK -> cannot do a simple NOT IN
            skip_composite.add(tbl)
            continue
        cols = [c.strip() for c in m.group("cols").split(",")]
        vals = split_sql_tuple(m.group("vals"))
        if pk not in cols or len(cols) != len(vals):
            continue
        pk_literal = vals[cols.index(pk)].strip()
        store = acc.setdefault(tbl, (pk, []))
        store[1].append(pk_literal)
    for tbl in skip_composite:
        acc.pop(tbl, None)
    return acc


def build_delete_block(pks: dict[str, tuple[str, list[str]]]) -> str:
    lines = [
        "",
        "-- ============================================================",
        "-- DELETE-RECONCILE (full-sync): drop mirror rows whose PK is no",
        "-- longer in the CSV SSOT. Same transaction as the upserts above.",
        "-- ============================================================",
    ]
    for tbl in sorted(pks):
        pk_col, values = pks[tbl]
        if not values:
            continue
        in_list = ", ".join(values)
        lines.append(
            f"DELETE FROM compliance.{tbl} WHERE {pk_col} NOT IN ({in_list});"
        )
    lines.append("")
    return "\n".join(lines)


def reconcile(sql_text: str) -> tuple[str, int]:
    pks = collect_pks(sql_text)
    if not pks:
        return sql_text, 0
    block = build_delete_block(pks)
    # Insert before the final COMMIT; (keep it inside the transaction).
    idx = sql_text.rfind("COMMIT;")
    if idx == -1:
        return sql_text + block + "\n", len(pks)
    return sql_text[:idx] + block + "\n" + sql_text[idx:], len(pks)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sql", type=Path, required=True, help="Emitted mirror-upsert.sql to augment in place.")
    args = ap.parse_args()
    text = args.sql.read_text(encoding="utf-8")
    out, n = reconcile(text)
    args.sql.write_text(out, encoding="utf-8")
    print(f"[delete-reconcile] appended NOT-IN DELETE for {n} mirror tables -> {args.sql}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
