#!/usr/bin/env python3
"""Two-plane mirror-contract parity guard (I95 D-IH-95-* / DataOps DATA-08).

WHY THIS EXISTS
---------------
The HLK runs a two-plane data architecture:

  * Plane 1 (T1) — git CSV SSOT, validated by Pydantic models in ``akos/`` via
    ``scripts/validate_hlk.py`` (CSV <-> Python contract).
  * Plane 2 (T2) — the Supabase ``compliance.*_mirror`` tables, whose schema
    (column types + CHECK constraints) is hand-written in ``supabase/migrations/``.

``validate_hlk`` proves CSV <-> Pydantic. NOTHING proved Pydantic/CSV <-> the
mirror DDL. So when a Pydantic enum grew (e.g. ``pattern_class`` gained
``area_governance`` at I93) without a matching ``ALTER ... CHECK`` migration, the
two planes drifted *silently* until the mirror-sync ``psql`` apply blew up
mid-stream with a cryptic ``violates check constraint`` (I95, 2026-06-08).

This guard closes that gap: it parses the emitted ``mirror-upsert.sql`` (the exact
payload that will be applied) and checks every value destined for an enum-
constrained column against the LIVE ``CHECK`` constraint set, reporting EVERY
drift at once (no whack-a-mole) BEFORE the apply runs.

Run modes
---------
* CI / operator (live truth)::

      py scripts/validate_mirror_enum_parity.py --emit            # emits + introspects live + checks

  Live introspection uses ``SUPABASE_DB_URL`` (preferred) or ``SUPABASE_PASSWORD``
  (pooler, same contract as ``.github/workflows/supabase-mirror-sync.yml``).

* Offline / test (snapshot)::

      py scripts/validate_mirror_enum_parity.py --emit-sql mirror.sql --constraints-json snap.json

Exit code 0 = parity OK; 1 = drift found (prints the exact ALTER to reconcile);
2 = could not introspect (no DB creds and no snapshot) -> SKIP (advisory).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SYNC_SCRIPT = REPO_ROOT / "scripts" / "sync_compliance_mirrors_from_csv.py"

# --- constraint def parsing -------------------------------------------------

_ANY_ARRAY_RE = re.compile(r"\(([a-z_][a-z0-9_]*) = ANY \(ARRAY\[(.*?)\]\)\)", re.DOTALL)
_ARRAY_VALUE_RE = re.compile(r"'((?:[^']|'')*)'::text")

# A def is compound/relational (NOT a plain single-column enum) if it joins
# conditions with AND, compares to another column/date, or carries more than one
# ANY-array. Such CHECKs (e.g. goipoi bridge_required_when_not_n1, collaborator
# overlay/methodology pairing, rate-override expiry consistency) must be SKIPPED:
# their embedded ARRAY is a conditional BRANCH, not the column's allowed set, so
# treating it as an enum produces false positives.
_COMPOUND_MARKERS = (" AND ", "<>", ">=", "<=", " < ", " > ", "CURRENT_DATE")


def parse_check_def(def_str: str) -> tuple[str, set[str]] | tuple[None, None]:
    """Extract (column, allowed_values) from a PURE single-column enum CHECK.

    Accepts ``CHECK ((col = ANY (ARRAY[...])))`` and the nullable variants
    (``(col IS NULL) OR (col = ''::text) OR (col = ANY (ARRAY[...]))``). Returns
    (None, None) for compound/relational CHECKs which are not plain enums.
    """
    if def_str.count("= ANY (ARRAY") != 1:
        return None, None
    if any(mark in def_str for mark in _COMPOUND_MARKERS):
        return None, None
    m = _ANY_ARRAY_RE.search(def_str)
    if not m:
        return None, None
    col = m.group(1)
    vals = {v.replace("''", "'") for v in _ARRAY_VALUE_RE.findall(m.group(2))}
    return col, vals


def load_constraints(rows: list[dict]) -> dict[str, dict[str, set[str]]]:
    """rows: [{'tbl':..., 'conname':..., 'def':...}] -> {table: {col: allowed}}.

    If a column carries multiple PURE enum CHECKs they are AND-ed, so the
    effective allowed set is their intersection.
    """
    out: dict[str, dict[str, set[str]]] = {}
    for r in rows:
        col, allowed = parse_check_def(r.get("def", ""))
        if not col:
            continue
        tbl = out.setdefault(r["tbl"], {})
        tbl[col] = (tbl[col] & allowed) if col in tbl else allowed
    return out


# --- emitted SQL parsing ----------------------------------------------------

_INSERT_RE = re.compile(
    r"INSERT INTO compliance\.(?P<tbl>[a-z0-9_]+) \((?P<cols>.*?)\) VALUES \((?P<vals>.*)\) ON CONFLICT",
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


def literal_token(v: str) -> str | None:
    """Return the string-literal token for a value, or None if it is not a plain
    quoted string (numbers, ``now()``, ``DATE '...'`` are not enum tokens)."""
    v = v.strip()
    if v.startswith("DATE "):
        return None
    if len(v) >= 2 and v[0] == "'" and v[-1] == "'":
        return v[1:-1].replace("''", "'")
    return None


def check_emit(emit_path: Path, constraints: dict[str, dict[str, set[str]]]) -> dict[str, dict[str, set[str]]]:
    """Return {table: {col: set(offending_values)}} for enum CHECK violations."""
    drifts: dict[str, dict[str, set[str]]] = {}
    with emit_path.open(encoding="utf-8") as fh:
        for line in fh:
            m = _INSERT_RE.search(line)
            if not m:
                continue
            tbl = m.group("tbl")
            tbl_constraints = constraints.get(tbl)
            if not tbl_constraints:
                continue
            cols = [c.strip() for c in m.group("cols").split(",")]
            vals = split_sql_tuple(m.group("vals"))
            if len(cols) != len(vals):
                continue  # defensive: skip rows we cannot align
            for col, allowed in tbl_constraints.items():
                if col not in cols:
                    continue
                tok = literal_token(vals[cols.index(col)])
                if tok is None or tok == "":
                    continue  # NULL/empty handled by nullable CHECKs
                if tok not in allowed:
                    drifts.setdefault(tbl, {}).setdefault(col, set()).add(tok)
    return drifts


# --- live introspection -----------------------------------------------------

_CONSTRAINTS_QUERY = (
    "select coalesce(json_agg(json_build_object('tbl', t.relname, 'conname', "
    "c.conname, 'def', pg_get_constraintdef(c.oid))), '[]') "
    "from pg_constraint c join pg_class t on t.oid=c.conrelid "
    "join pg_namespace n on n.oid=t.relnamespace "
    "where n.nspname='compliance' and c.contype='c' "
    "and pg_get_constraintdef(c.oid) ilike '%= ANY (ARRAY%';"
)


def introspect_live() -> list[dict] | None:
    """Fetch enum CHECK constraints via psql using the same secret contract as
    the mirror-sync workflow. Returns None if no creds / psql unavailable."""
    db_url = os.environ.get("SUPABASE_DB_URL", "")
    pwd = os.environ.get("SUPABASE_PASSWORD", "")
    ref = os.environ.get("SUPABASE_PROJECT_REF", "swrmqpelgoblaquequzb")
    host = os.environ.get("SUPABASE_POOLER_HOST", "aws-0-eu-central-1.pooler.supabase.com")
    base = ["psql", "-tAX", "-c", _CONSTRAINTS_QUERY]
    env = dict(os.environ)
    if db_url.startswith(("postgres://", "postgresql://")):
        cmd = ["psql", db_url, "-tAX", "-c", _CONSTRAINTS_QUERY]
    elif pwd:
        env["PGPASSWORD"] = pwd
        cmd = base[:1] + ["-h", host, "-p", "5432", "-U", f"postgres.{ref}", "-d", "postgres"] + base[1:]
    else:
        return None
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=60)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if res.returncode != 0:
        sys.stderr.write(res.stderr)
        return None
    return json.loads(res.stdout.strip() or "[]")


def emit_sql(out_path: Path) -> None:
    subprocess.run(
        [sys.executable, str(SYNC_SCRIPT), "--output", str(out_path), "--git-sha", "parity-preflight"],
        check=True,
        cwd=str(REPO_ROOT),
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--emit", action="store_true", help="Emit a fresh mirror SQL to a temp file and check it.")
    ap.add_argument("--emit-sql", type=Path, help="Path to an existing emitted mirror-upsert.sql.")
    ap.add_argument("--constraints-json", type=Path, help="Snapshot of enum CHECK constraints (offline mode).")
    args = ap.parse_args()

    # 1) constraints (live, else snapshot)
    if args.constraints_json:
        rows = json.loads(args.constraints_json.read_text(encoding="utf-8"))
    else:
        rows = introspect_live()
        if rows is None:
            print("[mirror-enum-parity] SKIP: no DB creds (SUPABASE_DB_URL/PASSWORD) and no --constraints-json.")
            return 2
    constraints = load_constraints(rows)
    print(f"[mirror-enum-parity] loaded {sum(len(c) for c in constraints.values())} enum CHECK columns across {len(constraints)} mirror tables.")

    # 2) emitted SQL (fresh, else provided)
    tmp = None
    if args.emit_sql:
        emit_path = args.emit_sql
    else:
        tmp = Path(tempfile.mkstemp(suffix="_mirror_parity.sql")[1])
        emit_sql(tmp)
        emit_path = tmp

    try:
        drifts = check_emit(emit_path, constraints)
    finally:
        if tmp and tmp.exists():
            tmp.unlink()

    if not drifts:
        print("[mirror-enum-parity] OK: every emitted enum value satisfies its live mirror CHECK constraint.")
        return 0

    print("\n[mirror-enum-parity] DRIFT FOUND — emitted CSV values rejected by the live mirror CHECK:\n")
    for tbl in sorted(drifts):
        for col, vals in sorted(drifts[tbl].items()):
            current = sorted(constraints[tbl][col])
            need = sorted(set(current) | set(vals))
            print(f"  compliance.{tbl}.{col}: missing {sorted(vals)}")
            print(f"    -> ALTER TABLE compliance.{tbl} DROP CONSTRAINT IF EXISTS <constraint>;")
            quoted = ",".join(f"'{v}'" for v in need)
            print(f"       ADD CONSTRAINT <constraint> CHECK ({col} IN ({quoted}));\n")
    print("Fix: add a migration extending the CHECK constraint(s) above to match the Pydantic SSOT, then re-run.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
