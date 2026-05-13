#!/usr/bin/env python3
"""Apply the AKOS estimation discipline to a per-engagement ``scope.yaml``.

Reads:
  * ``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv`` — role × hourly-rate triangle.
  * ``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/COUNTRY_WORK_CALENDAR.csv`` — country calendar.
  * ``<scope.yaml>`` — operator-supplied scope (engagement slug, counterparty label, country, packages).

Writes:
  * ``<output_dir>/commercial-schedule.md`` — math table + totals + Mermaid Gantt.

Usage::

    py scripts/estimate_engagement.py \
        --scope docs/wip/intelligence/2026-05-10-suez-webuy-procure-to-pay/scope.yaml \
        --out docs/wip/intelligence/2026-05-10-suez-webuy-procure-to-pay/commercial-schedule.md

Cross-references:
  * SOP-ENG_ESTIMATION_DISCIPLINE_001 — canonical body.
  * akos/engagement_estimation.py — math + Gantt rendering.
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.engagement_estimation import (
    EngagementScope,
    WorkPackage,
    estimate_engagement,
    load_calendar,
    load_role_rates,
    render_commercial_schedule_markdown,
)
from akos.io import REPO_ROOT
from akos.log import setup_logging

logger = logging.getLogger("akos.estimate_engagement")

ROLES_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "baseline_organisation.csv"
CALENDAR_CSV = (
    REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "COUNTRY_WORK_CALENDAR.csv"
)


def _load_yaml(path: Path) -> dict:
    """Minimal YAML loader using PyYAML if available, else a tiny fallback.

    ``scope.yaml`` is small and structured; the fallback parser handles the
    schema produced by ``estimation-template.md`` without taking PyYAML as a
    hard dependency at import time.
    """
    try:
        import yaml  # type: ignore[import-not-found]

        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except ImportError:
        return _tiny_yaml_load(path.read_text(encoding="utf-8"))


def _tiny_yaml_load(text: str) -> dict:
    """Tiny YAML subset: top-level scalars, lists of dicts, nested dicts."""
    import re

    lines = [ln for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith("#")]
    root: dict = {}
    stack: list[tuple[int, object]] = [(-1, root)]
    list_marker = re.compile(r"^(\s*)- (.*)$")
    kv = re.compile(r"^(\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$")
    for raw in lines:
        if m := list_marker.match(raw):
            indent = len(m.group(1))
            body = m.group(2)
            while stack and stack[-1][0] >= indent:
                stack.pop()
            parent = stack[-1][1]
            if not isinstance(parent, list):
                raise ValueError(f"unexpected list item under non-list at: {raw!r}")
            new: dict = {}
            parent.append(new)
            if ":" in body:
                kk, _, vv = body.partition(":")
                if vv.strip():
                    new[kk.strip()] = _coerce_scalar(vv.strip())
                else:
                    stack.append((indent, new))
                    stack.append((indent + 2, new))
            else:
                stack.append((indent, new))
            continue
        if m := kv.match(raw):
            indent = len(m.group(1))
            key = m.group(2)
            val = m.group(3).strip()
            while stack and stack[-1][0] >= indent:
                stack.pop()
            parent = stack[-1][1]
            if not isinstance(parent, dict):
                raise ValueError(f"unexpected key under non-dict at: {raw!r}")
            if val == "":
                child: object
                child = []
                if _peek_is_dict_block(text, raw):
                    child = {}
                parent[key] = child
                stack.append((indent, child))
            else:
                parent[key] = _coerce_scalar(val)
    return root


def _peek_is_dict_block(text: str, anchor: str) -> bool:
    """Heuristic: if the next non-empty indented line begins with ``key:`` not ``-``,
    the parent is a dict block.
    """
    lines = text.splitlines()
    try:
        idx = lines.index(anchor)
    except ValueError:
        return False
    indent = len(anchor) - len(anchor.lstrip())
    for nxt in lines[idx + 1 :]:
        s = nxt.lstrip()
        if not s or s.startswith("#"):
            continue
        nxt_indent = len(nxt) - len(s)
        if nxt_indent <= indent:
            return False
        return not s.startswith("- ")
    return False


def _coerce_scalar(value: str):
    if value.startswith(("'", '"')) and value.endswith(value[0]):
        return value[1:-1]
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.lower() == "null":
        return None
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def _scope_from_dict(data: dict) -> EngagementScope:
    raw_packages = data.get("packages") or []
    packages = [
        WorkPackage(
            package_id=p["package_id"],
            method_id=p["method_id"],
            label=p.get("label"),
            role_mix_override=p.get("role_mix_override"),
            multiplier_ids=list(p.get("multiplier_ids") or []),
        )
        for p in raw_packages
    ]
    start = data.get("start_date")
    if isinstance(start, str):
        start = date.fromisoformat(start)
    return EngagementScope(
        engagement_slug=data["engagement_slug"],
        counterparty_label=data["counterparty_label"],
        country_code=data["country_code"],
        start_date=start,
        packages=packages,
        notes=data.get("notes", "") or "",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--scope", required=True, help="path to scope.yaml")
    parser.add_argument("--out", required=True, help="path to write commercial-schedule.md")
    parser.add_argument("--json-log", action="store_true")
    args = parser.parse_args(argv)
    setup_logging(json_output=args.json_log)

    scope_path = Path(args.scope)
    out_path = Path(args.out)
    if not scope_path.exists():
        logger.error("scope file not found: %s", scope_path)
        return 1

    rates = load_role_rates(ROLES_CSV)
    calendars = load_calendar(CALENDAR_CSV)
    scope_dict = _load_yaml(scope_path)
    scope = _scope_from_dict(scope_dict)
    estimate = estimate_engagement(scope, rates, calendars)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_commercial_schedule_markdown(estimate), encoding="utf-8")
    logger.info("wrote: %s", out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
