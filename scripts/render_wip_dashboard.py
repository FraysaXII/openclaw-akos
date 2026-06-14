#!/usr/bin/env python3
"""WIP dashboard auto-renderer (Initiative 32 P10 + Initiative 59 P2 section split).

Paired SOP: docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/SOP-PMO_WIP_DASHBOARD_RENDER_001.md
Catalog: docs/references/hlk/v3.0/Admin/O5-1/Operations/canonicals/OPERATIONS_PROCESS_CATALOG.yaml (pmo_wip_dashboard_render)

Reads each ``docs/wip/planning/<NN>-*/master-roadmap.md`` and extracts:
- the initiative number (from folder prefix)
- the title (first H1)
- the status — preferring ``status:`` from frontmatter (validated against the
  ``akos.planning.status_taxonomy.InitiativeStatus`` SSOT enum); else falling
  back to the legacy ``**Status:**`` line in the body; else ``unknown``
- the date (from frontmatter ``last_review`` or ``Date:`` line)
- the program_id / plane (from frontmatter)

I59 P2 split: rows are **grouped into status taxonomy sections**
(Closed / Archived / Active / Continuous / Program Lines / Gated (external) /
Gated (operator) / Unknown) per ``DASHBOARD_SECTION_ORDER``. Within each section
rows stay sorted by initiative number ascending. Legacy frontmatter values that
do not match the taxonomy land in the **Unknown** section without crashing —
they get normalised in P3 (status audit + tag).

Emits a deterministic block between ``<!-- BEGIN AUTO -->`` and ``<!-- END AUTO -->``
markers in ``docs/wip/planning/WIP_DASHBOARD.md``. Hand-written content above and
below the markers is preserved.

Determinism: stable sort + stable section order ⇒ sha256 stable across runs.

Usage::

    py scripts/render_wip_dashboard.py             # render and write
    py scripts/render_wip_dashboard.py --check-only # report what would change; exit 1 if drift
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT
from akos.planning.carryover_posture import (
    INDEX_DASHBOARD_POSTURES,
    POSTURE_PLAIN_LABELS,
)
from akos.planning.status_taxonomy import (
    DASHBOARD_SECTION_ORDER,
    DASHBOARD_SECTION_TITLES,
    VALID_INITIATIVE_STATUSES,
    InitiativeStatus,
)

PLANNING_DIR = REPO_ROOT / "docs" / "wip" / "planning"
DASHBOARD_PATH = PLANNING_DIR / "WIP_DASHBOARD.md"
CARRYOVER_INDEX_PATH = PLANNING_DIR / "_trackers" / "carryover-posture-index.md"
INITIATIVE_DIR_RE = re.compile(r"^(\d{2}[a-z]?)-(.+)$")
H1_RE = re.compile(r"^#\s+(.+?)$", re.MULTILINE)
STATUS_RE = re.compile(r"\*\*?Status:?\*?\*?\s*(.+?)$", re.MULTILINE | re.IGNORECASE)
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
LAST_REVIEW_RE = re.compile(r"^last_review\s*:\s*([^\s]+)\s*$", re.MULTILINE)
FRONTMATTER_STATUS_RE = re.compile(r"^status\s*:\s*([^\s#]+)\s*$", re.MULTILINE)
DATE_RE = re.compile(r"\*\*?Date:?\*?\*?\s*(\d{4}-\d{2}-\d{2})", re.MULTILINE | re.IGNORECASE)

BEGIN_MARKER = "<!-- BEGIN AUTO -->"
END_MARKER = "<!-- END AUTO -->"
CARRYOVER_BEGIN_MARKER = "<!-- BEGIN CARRYOVER AUTO -->"
CARRYOVER_END_MARKER = "<!-- END CARRYOVER AUTO -->"

CARRYOVER_INDEX_ROW_RE = re.compile(
    r"^\|\s*(CO-\d+-\d+)\s*\|\s*([a-z_]+)\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*`?([^|`]+)`?\s*\|"
)

UNKNOWN_BUCKET = "unknown"


def _classify_status(frontmatter_status: str | None, body_status_raw: str | None) -> tuple[str, str]:
    """Classify a master-roadmap row into a taxonomy bucket.

    Returns ``(taxonomy_bucket, display_status)`` where ``taxonomy_bucket`` is
    one of ``DASHBOARD_SECTION_ORDER`` plus ``unknown``, and ``display_status``
    is the human-readable status text shown in the rendered table.

    Resolution order:
    1. Frontmatter ``status:`` — if it matches ``VALID_INITIATIVE_STATUSES``,
       use it as both bucket and display.
    2. Frontmatter ``status:`` — if non-empty but not a taxonomy value, bucket
       is ``unknown`` (legacy drift expected; P3 mass audit normalises).
    3. Legacy body ``**Status:**`` line — bucket is ``unknown``, display is
       the trimmed body string.
    4. No status anywhere — bucket and display both ``unknown``.
    """
    if frontmatter_status:
        normalised = frontmatter_status.strip().lower()
        if normalised in VALID_INITIATIVE_STATUSES:
            return normalised, normalised
        return UNKNOWN_BUCKET, frontmatter_status.strip()
    if body_status_raw:
        return UNKNOWN_BUCKET, body_status_raw
    return UNKNOWN_BUCKET, "unknown"


def _read_initiative(folder: Path) -> dict[str, str] | None:
    m = INITIATIVE_DIR_RE.match(folder.name)
    if not m:
        return None
    seq = m.group(1)
    slug = m.group(2)
    roadmap = folder / "master-roadmap.md"
    if not roadmap.is_file():
        bucket, display = _classify_status(None, None)
        return {
            "seq": seq, "slug": slug, "title": "(no master-roadmap.md)",
            "status": display, "bucket": bucket, "date": "—", "folder": folder.name,
        }
    text = roadmap.read_text(encoding="utf-8")
    fm_match = FRONTMATTER_RE.match(text)
    body = text[fm_match.end():] if fm_match else text
    fm_block = fm_match.group(1) if fm_match else ""

    h1 = H1_RE.search(body)
    title = h1.group(1).strip() if h1 else slug

    fm_status_match = FRONTMATTER_STATUS_RE.search(fm_block)
    fm_status = fm_status_match.group(1).strip() if fm_status_match else None

    body_status_match = STATUS_RE.search(body)
    body_status: str | None
    if body_status_match:
        body_status = body_status_match.group(1).strip().rstrip(".")
        body_status = re.sub(r"\s+", " ", body_status)
        if len(body_status) > 80:
            body_status = body_status[:77] + "..."
    else:
        body_status = None

    bucket, display = _classify_status(fm_status, body_status)

    date = "—"
    lr = LAST_REVIEW_RE.search(fm_block)
    if lr:
        date = lr.group(1)
    else:
        d = DATE_RE.search(body)
        if d:
            date = d.group(1)

    return {
        "seq": seq, "slug": slug, "title": title,
        "status": display, "bucket": bucket, "date": date, "folder": folder.name,
    }


def _scan_initiatives() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for p in sorted(PLANNING_DIR.iterdir()):
        if not p.is_dir() or p.name.startswith(".") or p.name == "00-ad-hoc-proposals":
            continue
        row = _read_initiative(p)
        if row is not None:
            rows.append(row)
    rows.sort(key=lambda r: r["seq"])
    return rows


def _render_table(rows: list[dict[str, str]]) -> str:
    """Render a single flat table (legacy single-section output).

    Retained for callers that want the un-grouped variant. The dashboard
    output uses :func:`_render_grouped_table` instead since I59 P2.
    """
    lines = [
        "| Seq | Folder | Status | Last review | Title |",
        "|:---:|:-------|:-------|:-----------:|:------|",
    ]
    for r in rows:
        title = r["title"]
        if len(title) > 90:
            title = title[:87] + "..."
        lines.append(
            f"| **{r['seq']}** | [`{r['folder']}/`]({r['folder']}/) | "
            f"{r['status']} | {r['date']} | {title} |"
        )
    return "\n".join(lines) + "\n"


def _render_grouped_table(rows: list[dict[str, str]]) -> str:
    """Render rows grouped into status taxonomy sections (I59 P2).

    Section order is fixed by ``DASHBOARD_SECTION_ORDER`` so the rendered
    block is deterministic regardless of folder traversal order. Empty
    sections still emit their header (with a "_(none)_" placeholder row)
    so operators see at-a-glance which buckets are empty.
    """
    bucket_order = list(DASHBOARD_SECTION_ORDER) + [UNKNOWN_BUCKET]
    bucket_titles: dict[str, str] = {**DASHBOARD_SECTION_TITLES, UNKNOWN_BUCKET: "Unknown / unclassified"}
    grouped: dict[str, list[dict[str, str]]] = {b: [] for b in bucket_order}
    for r in rows:
        b = r.get("bucket", UNKNOWN_BUCKET)
        if b not in grouped:
            grouped[UNKNOWN_BUCKET].append(r)
        else:
            grouped[b].append(r)
    out: list[str] = []
    for bucket in bucket_order:
        title = bucket_titles[bucket]
        bucket_rows = grouped[bucket]
        out.append(f"### {title} ({len(bucket_rows)})\n")
        if not bucket_rows:
            out.append("_(none)_\n")
            continue
        out.append("| Seq | Folder | Status | Last review | Title |")
        out.append("|:---:|:-------|:-------|:-----------:|:------|")
        for r in bucket_rows:
            row_title = r["title"]
            if len(row_title) > 90:
                row_title = row_title[:87] + "..."
            out.append(
                f"| **{r['seq']}** | [`{r['folder']}/`]({r['folder']}/) | "
                f"{r['status']} | {r['date']} | {row_title} |"
            )
        out.append("")
    return "\n".join(out) + "\n"


def _parse_carryover_index_rows() -> list[dict[str, str]]:
    if not CARRYOVER_INDEX_PATH.is_file():
        return []
    text = CARRYOVER_INDEX_PATH.read_text(encoding="utf-8")
    rows: list[dict[str, str]] = []
    in_table = False
    for line in text.splitlines():
        if "index_id | posture | item_id" in line and "discoverability_path" in line:
            in_table = True
            continue
        if in_table:
            if not line.startswith("|"):
                if rows:
                    break
                continue
            if ":---" in line:
                continue
            m = CARRYOVER_INDEX_ROW_RE.match(line.strip())
            if not m:
                continue
            posture = m.group(2).strip()
            if posture not in INDEX_DASHBOARD_POSTURES:
                continue
            rows.append(
                {
                    "index_id": m.group(1).strip(),
                    "posture": posture,
                    "item_id": m.group(3).strip(),
                    "target": m.group(4).strip(),
                    "activation_trigger": m.group(5).strip(),
                    "next_review": m.group(6).strip(),
                    "owner": m.group(7).strip(),
                    "discoverability_path": m.group(8).strip().strip("`"),
                }
            )
    return rows


def _render_carryover_section() -> str:
    rows = _parse_carryover_index_rows()
    if not rows:
        return "_(no scheduled carryover rows in index)_\n"
    lines = [
        "| Index | Posture | Item | Target | Activation trigger | Next review | Owner |",
        "|:---:|:---|:---|:---|:---|:---|:---|",
    ]
    for r in rows:
        label = POSTURE_PLAIN_LABELS.get(r["posture"], r["posture"])
        lines.append(
            f"| **{r['index_id']}** | {label} | {r['item_id']} | {r['target']} | "
            f"{r['activation_trigger']} | {r['next_review']} | {r['owner']} |"
        )
    lines.append("")
    lines.append(
        f"Full index: [`carryover-posture-index.md`](_trackers/carryover-posture-index.md) "
        f"— **scheduled ≠ dropped**."
    )
    return "\n".join(lines) + "\n"


def _splice_carryover_into_dashboard(carryover: str, text: str) -> str:
    if CARRYOVER_BEGIN_MARKER in text and CARRYOVER_END_MARKER in text:
        pre, _, rest = text.partition(CARRYOVER_BEGIN_MARKER)
        _, _, post = rest.partition(CARRYOVER_END_MARKER)
        return f"{pre}{CARRYOVER_BEGIN_MARKER}\n{carryover}{CARRYOVER_END_MARKER}{post}"
    insert = (
        f"\n\n## Scheduled carryover (cross-initiative)\n\n"
        f"{CARRYOVER_BEGIN_MARKER}\n{carryover}{CARRYOVER_END_MARKER}\n"
    )
    if END_MARKER in text:
        idx = text.index(END_MARKER) + len(END_MARKER)
        return text[:idx] + insert + text[idx:]
    return text + insert


def _splice_into_dashboard(table: str) -> str:
    """Splice the rendered table between BEGIN AUTO and END AUTO markers.

    Creates the dashboard with default scaffold if absent. Preserves hand-written
    content above and below the markers.
    """
    if not DASHBOARD_PATH.is_file():
        scaffold = (
            "---\nlanguage: en\nstatus: active\nintellectual_kind: dashboard\n"
            "role_owner: PMO\narea: Operations / PMO\nentity: Holistika Research\n"
            "authority: PMO\n---\n\n"
            "# WIP Dashboard — initiative state at a glance\n\n"
            "Auto-rendered from each initiative's `master-roadmap.md` frontmatter + body. "
            "Hand-written content above / below the markers is preserved across re-renders. "
            "Run `py scripts/render_wip_dashboard.py` after any initiative change.\n\n"
            "## Initiatives\n\n"
            f"{BEGIN_MARKER}\n{table}{END_MARKER}\n\n"
            "## Re-render contract\n\n"
            "- Renderer: [`scripts/render_wip_dashboard.py`](../../../scripts/render_wip_dashboard.py)\n"
            "- Verify profile: `wip_dashboard_render_smoke`\n"
            "- Determinism gate: sha256 stable across two consecutive runs\n"
        )
        return scaffold
    text = DASHBOARD_PATH.read_text(encoding="utf-8")
    if BEGIN_MARKER not in text or END_MARKER not in text:
        # Defensive: append a fresh markered block at end-of-file.
        return text + f"\n\n## Initiatives (auto-rendered)\n\n{BEGIN_MARKER}\n{table}{END_MARKER}\n"
    pre, _, rest = text.partition(BEGIN_MARKER)
    _, _, post = rest.partition(END_MARKER)
    return f"{pre}{BEGIN_MARKER}\n{table}{END_MARKER}{post}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Render WIP dashboard from initiative master-roadmaps")
    parser.add_argument("--check-only", action="store_true", help="Report drift; exit 1 if dashboard would change")
    args = parser.parse_args()

    rows = _scan_initiatives()
    table = _render_grouped_table(rows)
    carryover = _render_carryover_section()
    new_text = _splice_into_dashboard(table)
    new_text = _splice_carryover_into_dashboard(carryover, new_text)

    existing = DASHBOARD_PATH.read_text(encoding="utf-8") if DASHBOARD_PATH.is_file() else ""
    new_hash = hashlib.sha256(new_text.encode("utf-8")).hexdigest()
    old_hash = hashlib.sha256(existing.encode("utf-8")).hexdigest() if existing else ""

    print(f"\n  WIP dashboard renderer (Initiative 32 P10)")
    print(f"  initiatives scanned: {len(rows)}")
    print(f"  new sha256:          {new_hash[:16]}...")
    print(f"  existing sha256:     {old_hash[:16] + '...' if old_hash else '(no existing dashboard)'}")

    if args.check_only:
        if new_hash != old_hash:
            print(f"  DRIFT: dashboard would change. Run without --check-only to update.")
            return 1
        print(f"  PASS: dashboard up to date.")
        return 0

    DASHBOARD_PATH.write_text(new_text, encoding="utf-8")
    print(f"  wrote {DASHBOARD_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
