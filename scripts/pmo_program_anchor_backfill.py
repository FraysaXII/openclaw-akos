#!/usr/bin/env python3
"""PMO runbook — backfill Program anchors prefix on INITIATIVE_REGISTRY notes (I86 P1).

Paired runbook for [`SOP-PMO_INITIATIVE_PROGRAM_ANCHORS_001.md`](../docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/SOP-PMO_INITIATIVE_PROGRAM_ANCHORS_001.md)
per [`akos-executable-process-catalog.mdc`](../.cursor/rules/akos-executable-process-catalog.mdc)
RULE 1 (every executable process needs a paired human-readable SOP).

Stage A semantics (D-IH-86-H + D-IH-86-J):

- The runbook lists ``status in {active, continuous, program_line}`` rows in
  `INITIATIVE_REGISTRY.csv` that lack a ``Program anchors:`` prefix on
  ``notes``, alongside an operator-proposed ``proposals.csv`` of
  ``initiative_id -> anchors``.
- ``--coverage-report`` writes a per-persona table at
  ``docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/coverage-by-persona-<DATE>.md``.
- ``--apply`` consumes a confirmed ``proposals.csv`` and rewrites ``notes`` to
  prepend the canonical prefix (idempotent — re-running on already-prefixed rows
  is a no-op). ``--apply`` MUST be operator-approved (canonical-CSV gate).
- ``--legacy-notes-parser`` (Stage A only) sources truth from the ``notes``
  prefix. The Stage B successor in I86 P2 will source truth from the new
  first-class ``program_anchors`` column and emit WARN on rows still carrying
  the prefix.

Per [`CONTRIBUTING.md`](../CONTRIBUTING.md) "Python Code Standards":
Pydantic chassis at ``akos/hlk_initiative_program_anchors.py``; type hints;
``akos.log.setup_logging`` for structured output; ``pathlib.Path``; tests in
``tests/test_pmo_program_anchor_backfill.py``.

Usage::

    py scripts/pmo_program_anchor_backfill.py --list-unanchored
    py scripts/pmo_program_anchor_backfill.py --coverage-report
    py scripts/pmo_program_anchor_backfill.py --apply proposals.csv --dry-run
    py scripts/pmo_program_anchor_backfill.py --apply proposals.csv

``proposals.csv`` schema::

    initiative_id,anchors
    INIT-OPENCLAW_AKOS-03,PRJ-HOL-PGF-2026;PRJ-HOL-DAT-2026

Exit codes::

    0 - clean run (or dry-run preview).
    1 - parse error in proposals.csv (unknown anchor; malformed token; FK miss).
    2 - INITIATIVE_REGISTRY.csv or PROGRAM_REGISTRY.csv missing.
"""

from __future__ import annotations

import argparse
import csv
import logging
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_initiative_program_anchors import (  # noqa: E402
    ANCHOR_PREFIX,
    PROGRAM_ID_PATTERN,
    parse_anchor_prefix,
)
from akos.io import REPO_ROOT  # noqa: E402
from akos.log import setup_logging  # noqa: E402

logger = logging.getLogger("akos.pmo_program_anchor_backfill")

INITIATIVE_CSV: Path = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "People"
    / "Compliance"
    / "canonicals"
    / "INITIATIVE_REGISTRY.csv"
)
PROGRAM_CSV: Path = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "People"
    / "Compliance"
    / "canonicals"
    / "dimensions"
    / "PROGRAM_REGISTRY.csv"
)
ANCHORED_STATUSES: frozenset[str] = frozenset({"active", "continuous", "program_line"})


@dataclass
class UnanchoredRow:
    initiative_id: str
    title: str
    status: str
    owner_role: str


def _load_initiative_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    return fieldnames, rows


def _load_program_ids(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        return {
            (row.get("program_id") or "").strip()
            for row in csv.DictReader(fh)
            if (row.get("program_id") or "").strip()
        }


def _list_unanchored(rows: list[dict[str, str]]) -> list[UnanchoredRow]:
    out: list[UnanchoredRow] = []
    for row in rows:
        status = (row.get("status") or "").strip()
        if status not in ANCHORED_STATUSES:
            continue
        notes = row.get("notes") or ""
        has_prefix, _ids, _malformed = parse_anchor_prefix(notes)
        if has_prefix:
            continue
        out.append(
            UnanchoredRow(
                initiative_id=(row.get("initiative_id") or "").strip(),
                title=(row.get("title") or "").strip(),
                status=status,
                owner_role=(row.get("owner_role") or "").strip(),
            )
        )
    return out


def _format_anchors_prefix(anchors: list[str]) -> str:
    return f"{ANCHOR_PREFIX} {'; '.join(anchors)}."


def _load_proposals(path: Path, known_ids: set[str]) -> tuple[dict[str, list[str]], list[str]]:
    if not path.is_file():
        return {}, [f"proposals file not found: {path}"]
    out: dict[str, list[str]] = {}
    errors: list[str] = []
    with path.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            iid = (row.get("initiative_id") or "").strip()
            raw_anchors = (row.get("anchors") or "").strip()
            if not iid:
                continue
            tokens = [t.strip() for t in raw_anchors.split(";") if t.strip()]
            for tok in tokens:
                if not PROGRAM_ID_PATTERN.match(tok):
                    errors.append(f"{iid}: malformed anchor {tok!r}")
                elif known_ids and tok not in known_ids:
                    errors.append(f"{iid}: anchor {tok!r} not in PROGRAM_REGISTRY.csv")
            if tokens:
                out[iid] = tokens
    return out, errors


def _apply_proposals(
    rows: list[dict[str, str]],
    proposals: dict[str, list[str]],
    today: str,
    decision_id: str,
    methodology_version: str,
) -> tuple[int, list[str]]:
    applied = 0
    skipped: list[str] = []
    for row in rows:
        iid = (row.get("initiative_id") or "").strip()
        if iid not in proposals:
            continue
        notes = (row.get("notes") or "").strip()
        has_prefix, _ids, _malformed = parse_anchor_prefix(notes)
        if has_prefix:
            skipped.append(f"{iid}: already carries prefix; skip")
            continue
        prefix = _format_anchors_prefix(proposals[iid])
        row["notes"] = f"{prefix} {notes}".strip()
        row["last_review_at"] = today
        row["last_review_by"] = (row.get("last_review_by") or "PMO").strip() or "PMO"
        row["last_review_decision_id"] = decision_id
        row["methodology_version_at_review"] = methodology_version
        applied += 1
    return applied, skipped


def _write_initiative_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _coverage_report(
    rows: list[dict[str, str]], output_path: Path, today: str
) -> None:
    """Emit a per-persona coverage matrix at output_path."""
    by_persona: dict[str, list[tuple[str, str, bool]]] = {
        "PMO": [],
        "Brand & Narrative Manager": [],
        "System Owner": [],
        "DevOPS": [],
        "Holistik Researcher": [],
        "People Operations Lead": [],
    }
    unmapped: list[tuple[str, str, bool, str]] = []
    for row in rows:
        status = (row.get("status") or "").strip()
        if status not in ANCHORED_STATUSES:
            continue
        iid = (row.get("initiative_id") or "").strip()
        title = (row.get("title") or "").strip()[:60]
        owner = (row.get("owner_role") or "").strip()
        has_prefix, _ids, _malformed = parse_anchor_prefix(row.get("notes") or "")
        bucket = by_persona.get(owner)
        if bucket is None:
            unmapped.append((iid, title, has_prefix, owner))
            continue
        bucket.append((iid, title, has_prefix))

    lines: list[str] = [
        "---",
        "language: en",
        "classification: planning_report",
        "initiative: INIT-OPENCLAW_AKOS-86",
        f"authored: {today}",
        "role_owner: PMO",
        "---",
        "",
        "# Initiative -> Program coverage by persona (Stage A baseline)",
        "",
        "Generated by `scripts/pmo_program_anchor_backfill.py --coverage-report`.",
        "",
        "Status legend: `[x]` anchors present in `notes`; `[ ]` unanchored.",
        "",
    ]
    for persona in sorted(by_persona):
        bucket = by_persona[persona]
        if not bucket:
            continue
        lines.append(f"## {persona}")
        lines.append("")
        for iid, title, has_prefix in sorted(bucket):
            mark = "x" if has_prefix else " "
            lines.append(f"- [{mark}] `{iid}` — {title}")
        lines.append("")
    if unmapped:
        lines.append("## Unmapped owner_role")
        lines.append("")
        for iid, title, has_prefix, owner in unmapped:
            mark = "x" if has_prefix else " "
            lines.append(f"- [{mark}] `{iid}` ({owner}) — {title}")
        lines.append("")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--list-unanchored", action="store_true", help="Print rows missing the anchors prefix.")
    parser.add_argument(
        "--coverage-report",
        action="store_true",
        help="Emit reports/coverage-by-persona-<DATE>.md.",
    )
    parser.add_argument(
        "--apply",
        type=str,
        default=None,
        help="Path to proposals.csv to consume (apply unless --dry-run).",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show diff but do not write CSV.")
    parser.add_argument("--today", type=str, default="2026-05-17", help="ISO date stamp.")
    parser.add_argument("--decision-id", type=str, default="D-IH-86-H", help="Decision id stamp.")
    parser.add_argument("--version", type=str, default="v3.1", help="Methodology version stamp.")
    parser.add_argument("--json-log", action="store_true", help="Structured JSON output.")
    parser.add_argument(
        "--legacy-notes-parser",
        action="store_true",
        help="Stage A flag (no-op until Stage B switches default to column-read).",
    )
    args = parser.parse_args(argv)

    setup_logging(json_output=args.json_log)

    if not INITIATIVE_CSV.is_file():
        logger.error(
            "INITIATIVE_REGISTRY missing",
            extra={"agent_role": "runbook", "tool_name": "pmo_program_anchor_backfill"},
        )
        return 2

    fieldnames, rows = _load_initiative_rows(INITIATIVE_CSV)
    program_ids = _load_program_ids(PROGRAM_CSV)

    if args.list_unanchored:
        unanchored = _list_unanchored(rows)
        if not args.json_log:
            print(f"\n  Unanchored active-class INITIATIVE rows: {len(unanchored)}")
            for u in unanchored:
                print(f"    - {u.initiative_id:30s} ({u.status:14s}) owner={u.owner_role}: {u.title}")
        return 0

    if args.coverage_report:
        report_path = (
            REPO_ROOT
            / "docs"
            / "wip"
            / "planning"
            / "86-initiative-cluster-execution-coordinator"
            / "reports"
            / f"coverage-by-persona-{args.today}.md"
        )
        _coverage_report(rows, report_path, args.today)
        if not args.json_log:
            print(f"  wrote: {report_path.relative_to(REPO_ROOT).as_posix()}")
        return 0

    if args.apply:
        proposals, errors = _load_proposals(Path(args.apply), program_ids)
        if errors:
            for err in errors:
                logger.error(err, extra={"agent_role": "runbook"})
                if not args.json_log:
                    print(f"  FAIL: {err}")
            return 1
        applied, skipped = _apply_proposals(
            rows,
            proposals,
            today=args.today,
            decision_id=args.decision_id,
            methodology_version=args.version,
        )
        if not args.json_log:
            print(f"\n  Proposals consumed: {len(proposals)}")
            print(f"  Rows updated:       {applied}")
            print(f"  Rows skipped:       {len(skipped)}")
            for skip in skipped:
                print(f"    - {skip}")
        if args.dry_run:
            if not args.json_log:
                print("  DRY-RUN: no file written")
            return 0
        _write_initiative_csv(INITIATIVE_CSV, fieldnames, rows)
        if not args.json_log:
            print(f"  wrote: {INITIATIVE_CSV.relative_to(REPO_ROOT).as_posix()}")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
