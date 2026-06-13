#!/usr/bin/env python3
"""Validate Research Action source ledgers.

Default mode validates the Wave R+4 C1/C1.5 source ledger. ``--self-test``
checks the Pydantic SSOT and synthetic fixtures only.
"""
from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_research_action import (  # noqa: E402
    DEFAULT_SOURCE_LEDGER_PATH,
    SOURCE_LEDGER_FIELDNAMES,
    ResearchSourceLedgerSummary,
    ResearchSourceRow,
    fixture_source_row,
)
from akos.research_ledger_ops import BASELINE_PRONG_IDS, normalize_prong  # noqa: E402


def _resolve_path(path_value: str | None) -> Path:
    raw = Path(path_value) if path_value else DEFAULT_SOURCE_LEDGER_PATH
    return raw if raw.is_absolute() else REPO_ROOT / raw


def validate_source_ledger(path: Path) -> tuple[bool, list[str], ResearchSourceLedgerSummary | None]:
    """Validate a source ledger CSV and return (ok, messages, summary)."""

    messages: list[str] = []
    if not path.is_file():
        return False, [f"source ledger not found: {path}"], None

    rows: list[ResearchSourceRow] = []
    seen: set[str] = set()
    with path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        if tuple(reader.fieldnames or ()) != SOURCE_LEDGER_FIELDNAMES:
            messages.append(
                f"header mismatch: got={reader.fieldnames!r} "
                f"expected={list(SOURCE_LEDGER_FIELDNAMES)!r}"
            )
            return False, messages, None
        for line_no, raw_row in enumerate(reader, start=2):
            try:
                row = ResearchSourceRow.model_validate(raw_row)
            except Exception as exc:
                messages.append(f"L{line_no}: {exc}")
                continue
            normalized_prong = normalize_prong(row.prong)
            if normalized_prong not in BASELINE_PRONG_IDS:
                messages.append(
                    f"L{line_no}: prong {row.prong!r} is not a baseline consumer ID "
                    f"(expected BL-* per RESEARCH_PRONG_LATTICE_DISCIPLINE.md; "
                    f"got {normalized_prong!r} after normalize)"
                )
            elif normalized_prong != row.prong.strip():
                messages.append(
                    f"L{line_no}: prong {row.prong!r} should be {normalized_prong!r} "
                    "(charter alias or typo — use baseline BL-* in the ledger CSV)"
                )
            if row.source_id in seen:
                messages.append(f"L{line_no}: duplicate source_id {row.source_id}")
            seen.add(row.source_id)
            rows.append(row)

    if messages:
        return False, messages, None

    counts = Counter(row.control_confidence_level for row in rows)
    summary = ResearchSourceLedgerSummary(
        ledger_path=path.relative_to(REPO_ROOT).as_posix()
        if path.is_relative_to(REPO_ROOT)
        else str(path),
        source_count=len(rows),
        unique_source_ids=len(seen),
        topic_clusters=sorted({row.topic_cluster for row in rows}),
        control_confidence_counts=dict(sorted(counts.items())),
    )
    return True, messages, summary


def self_test() -> int:
    """Run lightweight fixture checks."""

    row = fixture_source_row()
    summary = ResearchSourceLedgerSummary(
        ledger_path=DEFAULT_SOURCE_LEDGER_PATH.as_posix(),
        source_count=1,
        unique_source_ids=1,
        topic_clusters=[row.topic_cluster],
        control_confidence_counts={row.control_confidence_level: 1},
    )
    if summary.source_count != 1:
        print("FAIL: ResearchSourceLedgerSummary fixture failed")
        return 1
    print("PASS: research-action self-test")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--source-ledger", help="Path to source-ledger.csv")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    path = _resolve_path(args.source_ledger)
    ok, messages, summary = validate_source_ledger(path)
    if not ok:
        print("FAIL: research-action source ledger validation")
        for message in messages:
            print(f"  - {message}")
        return 1

    assert summary is not None
    print(
        "PASS: research-action source ledger "
        f"({summary.source_count} rows; topics={len(summary.topic_clusters)}; "
        f"control_confidence={summary.control_confidence_counts})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
