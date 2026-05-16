"""Paired runbook for SOP-RENDERING_PIPELINE_GOVERNANCE_001 (Initiative 77 P4.C).

Per `D-IH-77-I` (orphan-rendering-pipeline governance) + `akos-executable-
process-catalog.mdc` Rule 1 (SOP + executable runbook pairing): every governed
process needs a paired SOP (operator-facing) AND a paired runbook (agent-
facing).

This runbook reads ``RENDERING_PIPELINE_REGISTRY.csv`` and produces a filtered
view of the catalogued rendering pipelines, formatted for operator + agent
consumption.

Modes:
- default: print all active pipelines as markdown table
- ``--all``: include inactive + planned + experimental + deprecated
- ``--status <status>``: filter by status (active | inactive | planned |
  experimental | deprecated)
- ``--governance <class>``: filter by governance_class (governed | partial |
  orphan)
- ``--owning-area <area>``: filter by area (Tech | Marketing/Brand | etc.)
- ``--brand-tokens-only``: filter to pipelines that consume brand tokens
- ``--format md|json``: output format (default md)

Examples::

    py scripts/list_rendering_pipelines.py
    py scripts/list_rendering_pipelines.py --status active --brand-tokens-only
    py scripts/list_rendering_pipelines.py --governance orphan --format json
    py scripts/list_rendering_pipelines.py --owning-area Marketing/Brand

Exit codes:
    0  Filter succeeded (may return 0 rows)
    1  Invalid filter / unknown CSV schema
    2  IO / configuration error
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_rendering_pipeline_csv import (  # noqa: E402
    CANONICAL_PATH,
    RENDERING_PIPELINE_FIELDNAMES,
    VALID_GOVERNANCE_CLASSES,
    VALID_STATUSES,
)

REGISTRY_PATH = REPO_ROOT / CANONICAL_PATH


def _load_rows() -> list[dict[str, str]]:
    if not REGISTRY_PATH.exists():
        print(f"error: RENDERING_PIPELINE_REGISTRY.csv not found at {REGISTRY_PATH}", file=sys.stderr)
        sys.exit(2)
    with REGISTRY_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if tuple(reader.fieldnames or ()) != RENDERING_PIPELINE_FIELDNAMES:
            print(
                f"error: schema mismatch in RENDERING_PIPELINE_REGISTRY.csv "
                f"(header={reader.fieldnames!r}; expected={list(RENDERING_PIPELINE_FIELDNAMES)})",
                file=sys.stderr,
            )
            sys.exit(1)
        return list(reader)


def _filter_rows(
    rows: list[dict[str, str]],
    *,
    status: str | None,
    governance: str | None,
    owning_area: str | None,
    brand_tokens_only: bool,
    show_all: bool,
) -> list[dict[str, str]]:
    out = []
    for r in rows:
        if status and r.get("status") != status:
            continue
        if not show_all and not status and r.get("status") != "active":
            continue
        if governance and r.get("governance_class") != governance:
            continue
        if owning_area and r.get("owning_area") != owning_area:
            continue
        if brand_tokens_only and r.get("brand_tokens_consumed") != "yes":
            continue
        out.append(r)
    return out


def _render_md(rows: list[dict[str, str]]) -> str:
    if not rows:
        return "_(0 rows match the filter)_\n"
    cols = ["pipeline_id", "name", "status", "governance_class", "owning_area", "trigger_command", "brand_tokens_consumed"]
    header = "| " + " | ".join(cols) + " |"
    sep = "|" + "|".join(":---" for _ in cols) + "|"
    lines = [header, sep]
    for r in rows:
        row_cells = [r.get(c, "") for c in cols]
        lines.append("| " + " | ".join(row_cells) + " |")
    return "\n".join(lines) + "\n"


def _render_json(rows: list[dict[str, str]]) -> str:
    return json.dumps(rows, indent=2, ensure_ascii=False)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--all", action="store_true", dest="show_all",
                        help="Include all statuses (default: active only)")
    parser.add_argument("--status", default=None, choices=sorted(VALID_STATUSES) + [None],
                        help="Filter by exact status")
    parser.add_argument("--governance", default=None,
                        choices=sorted(VALID_GOVERNANCE_CLASSES) + [None],
                        help="Filter by governance_class")
    parser.add_argument("--owning-area", default=None,
                        help="Filter by owning_area (exact match)")
    parser.add_argument("--brand-tokens-only", action="store_true",
                        help="Filter to pipelines that consume brand tokens (brand_tokens_consumed=yes)")
    parser.add_argument("--format", default="md", choices=("md", "json"),
                        help="Output format (default md)")
    args = parser.parse_args(argv)

    rows = _load_rows()
    filtered = _filter_rows(
        rows,
        status=args.status,
        governance=args.governance,
        owning_area=args.owning_area,
        brand_tokens_only=args.brand_tokens_only,
        show_all=args.show_all,
    )

    if args.format == "md":
        sys.stdout.write(_render_md(filtered))
    else:
        sys.stdout.write(_render_json(filtered) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
