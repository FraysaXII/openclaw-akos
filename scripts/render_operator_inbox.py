#!/usr/bin/env python3
"""Operator Action Inbox auto-renderer (Initiative 59 P4).

Reads ``docs/references/hlk/compliance/OPS_REGISTER.csv`` and emits a single
ranked, FK-joined operator-readable surface at
``docs/wip/planning/OPERATOR_INBOX.md``. The CSV is the SSOT; this surface is
the one place the operator looks to know "what genuinely needs me right now".

Filter
======

Inbox rows are those with ``status='open'`` AND ``owner_class IN ('operator',
'mixed')`` per **D-IH-59-A** governance promotion + the I59 plan §P4. ``rice_score``
ranks the table descending; rows missing a numeric RICE land at the bottom in
their natural order so they remain visible.

Joins
=====

- ``originating_initiative_id`` joins ``INITIATIVE_REGISTRY.csv`` for the
  initiative title.
- ``owner_role`` joins ``baseline_organisation.csv`` for the role's
  human-readable label (falls back to the role_name as-is when the FK is the
  default ``PMO`` or any unknown role).

Determinism
===========

Stable sort + canonical column set ⇒ sha256 stable across runs. ``--check-only``
re-renders to a temp buffer and exits 1 if the on-disk file is out of date.
This mirrors the ``render_wip_dashboard.py`` pattern so the same release-gate
hook can wrap both surfaces.

Usage
=====

::

    py scripts/render_operator_inbox.py             # render and write
    py scripts/render_operator_inbox.py --check-only # report drift; exit 1 if stale
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT

PLANNING_DIR = REPO_ROOT / "docs" / "wip" / "planning"
HLK_COMPLIANCE = REPO_ROOT / "docs" / "references" / "hlk" / "compliance"
OPS_REGISTER_CSV = HLK_COMPLIANCE / "OPS_REGISTER.csv"
INITIATIVE_REGISTRY_CSV = HLK_COMPLIANCE / "INITIATIVE_REGISTRY.csv"
ORG_CSV = HLK_COMPLIANCE / "baseline_organisation.csv"
INBOX_PATH = PLANNING_DIR / "OPERATOR_INBOX.md"

INBOX_OWNER_CLASSES: frozenset[str] = frozenset({"operator", "mixed"})


def _load_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _initiative_title_lookup() -> dict[str, str]:
    rows = _load_csv(INITIATIVE_REGISTRY_CSV)
    return {(r.get("initiative_id") or "").strip(): (r.get("title") or "").strip() for r in rows}


def _role_label_lookup() -> dict[str, str]:
    rows = _load_csv(ORG_CSV)
    out: dict[str, str] = {}
    for r in rows:
        role = (r.get("role_name") or "").strip()
        label = (r.get("display_name") or r.get("role_name") or "").strip()
        if role:
            out[role] = label
    return out


def _format_rice(value: str) -> tuple[str, float]:
    """Return ``(display, sort_key)`` — sort_key is negative so DESC sort works."""
    raw = (value or "").strip()
    if not raw:
        return "—", 0.0
    try:
        f = float(raw)
        return f"{f:g}", -f
    except ValueError:
        return raw, 0.0


def _row_for_inbox(
    ops_row: dict[str, str],
    titles: dict[str, str],
    role_labels: dict[str, str],
) -> tuple[float, str, list[str]]:
    """Return ``(sort_key_primary, sort_key_tiebreak, rendered_cells)``.

    Tie-break key is the ``ops_action_id`` so equal-RICE rows stay stable.
    """
    ops_id = (ops_row.get("ops_action_id") or "").strip()
    init_id = (ops_row.get("originating_initiative_id") or "").strip()
    init_title = titles.get(init_id, "")
    initiative_display = f"{init_id}" if not init_title else f"{init_id} — {init_title}"
    owner_class = (ops_row.get("owner_class") or "").strip()
    owner_role = (ops_row.get("owner_role") or "").strip()
    owner_label = role_labels.get(owner_role, owner_role)
    owner_display = owner_class if not owner_label else f"{owner_class} ({owner_label})"
    rice_display, rice_sort = _format_rice(ops_row.get("rice_score") or "")
    rice_impact = (ops_row.get("rice_impact") or "").strip()
    if rice_impact and rice_display == "—":
        rice_display = f"impact={rice_impact}"
    title = (ops_row.get("title") or "").strip() or "(seed; needs operator triage)"
    notes = (ops_row.get("notes") or "").strip()
    cells = [
        f"`{ops_id}`",
        initiative_display,
        owner_display,
        rice_display,
        title,
        notes,
    ]
    return rice_sort, ops_id, cells


def _render_block() -> tuple[str, int]:
    """Return ``(rendered_block, row_count)`` (excludes the BEGIN/END markers)."""
    ops_rows = _load_csv(OPS_REGISTER_CSV)
    titles = _initiative_title_lookup()
    role_labels = _role_label_lookup()
    candidates: list[tuple[float, str, list[str]]] = []
    for r in ops_rows:
        if (r.get("status") or "").strip() != "open":
            continue
        if (r.get("owner_class") or "").strip() not in INBOX_OWNER_CLASSES:
            continue
        candidates.append(_row_for_inbox(r, titles, role_labels))
    candidates.sort(key=lambda t: (t[0], t[1]))

    headers = ["OPS ID", "Initiative", "Owner", "RICE", "What", "Notes"]
    lines: list[str] = []
    if not candidates:
        lines.append("_No open operator/mixed actions._")
        return "\n".join(lines), 0
    lines.append(f"_Rows: {len(candidates)} (open · operator/mixed · ranked by RICE desc)._")
    lines.append("")
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    for _, _, cells in candidates:
        safe = [(c or "").replace("|", "\\|") for c in cells]
        lines.append("| " + " | ".join(safe) + " |")
    return "\n".join(lines), len(candidates)


BEGIN_MARKER = "<!-- BEGIN AUTO -->"
END_MARKER = "<!-- END AUTO -->"

PREAMBLE = """\
---
language: en
status: continuous
continuous_rationale: Auto-rendered Operator Action Inbox (I59 P4) — re-renders from OPS_REGISTER.csv on every status flip; never hand-edit between markers.
---

# Operator Action Inbox

> **SSOT** is `docs/references/hlk/compliance/OPS_REGISTER.csv`. This file is
> auto-rendered by `scripts/render_operator_inbox.py` on every change to that
> CSV. Filter: `status='open'` AND `owner_class IN ('operator', 'mixed')`,
> ordered by `rice_score DESC`.
>
> Re-render: `py scripts/render_operator_inbox.py`. Determinism gate runs in
> release-gate.

"""

POSTAMBLE = """

## Reading guide

- **OPS ID** is the canonical primary key in `OPS_REGISTER.csv`.
- **Initiative** is the originating initiative (linked via
  `originating_initiative_id`).
- **Owner** is `owner_class` followed by the labelled `owner_role`.
- **RICE** is the persisted `rice_score` (numeric). `impact=N` indicates a
  partial RICE (`rice_impact` set, full score not yet computed).
- **What** is the row's `title`; **Notes** is the row's `notes` field.

## How rows enter and leave this inbox

- **Enter:** a coding cycle mints a new row in `OPS_REGISTER.csv` with
  `status='open'` and `owner_class='operator'` or `'mixed'`. The next inbox
  re-render picks it up.
- **Leave:** the operator (or a follow-up cycle) flips the row's `status` to
  `closed` (or `forwarded`/`superseded`) in `OPS_REGISTER.csv`. The next inbox
  re-render drops it.
- Closed history lives in `OPS_REGISTER.csv` itself; the `closed_at` /
  `linked_decision_ids` fields preserve the audit trail without polluting this
  active surface.

## Cross-references

- Status taxonomy SSOT: `akos/planning/status_taxonomy.py`
- Initiative governance lifecycle SOP:
  `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-INITIATIVE_GOVERNANCE_001.md`
- Process harmonisation SOP (forward-looking):
  `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-INITIATIVE_PROCESS_HARMONISATION_001.md`
- I59 master roadmap (this surface's parent):
  `docs/wip/planning/59-hlk-governance-clean-slate/master-roadmap.md`
"""


def _render_full() -> tuple[str, int]:
    block, count = _render_block()
    body = (
        PREAMBLE
        + BEGIN_MARKER
        + "\n\n"
        + block
        + "\n\n"
        + END_MARKER
        + POSTAMBLE
    )
    if not body.endswith("\n"):
        body = body + "\n"
    return body, count


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Render to memory and exit 1 if the on-disk file would change.",
    )
    args = parser.parse_args()

    new_body, count = _render_full()
    new_sha = _sha256(new_body)
    existing = INBOX_PATH.read_text(encoding="utf-8") if INBOX_PATH.is_file() else ""
    existing_sha = _sha256(existing)

    print()
    print("  Operator Action Inbox renderer (I59 P4)")
    print("  " + "=" * 40)
    print(f"  rows in inbox:      {count}")
    print(f"  new sha256:         {new_sha[:16]}...")
    print(f"  existing sha256:    {existing_sha[:16]}...")

    if args.check_only:
        if new_sha == existing_sha:
            print("  PASS: operator inbox up to date.")
            return 0
        print("  FAIL: operator inbox is stale; re-run without --check-only.")
        return 1

    if new_sha == existing_sha:
        print("  No changes.")
        return 0
    INBOX_PATH.write_text(new_body, encoding="utf-8")
    print(f"  wrote {INBOX_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
