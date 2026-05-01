#!/usr/bin/env python3
"""Initiative 32 P10 — WIP dashboard auto-renderer.

Reads each ``docs/wip/planning/<NN>-*/master-roadmap.md`` and extracts:
- the initiative number (from folder prefix)
- the title (first H1)
- the status (from ``Status:`` line if present, else "open")
- the date (from frontmatter ``last_review`` or ``Date:`` line)
- the program_id / plane (from frontmatter)

Emits a deterministic table between ``<!-- BEGIN AUTO -->`` and ``<!-- END AUTO -->``
markers in ``docs/wip/planning/WIP_DASHBOARD.md``. Hand-written content above and
below the markers is preserved.

Determinism: the table is sorted by initiative number ascending; sha256 stable
across two consecutive runs.

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

PLANNING_DIR = REPO_ROOT / "docs" / "wip" / "planning"
DASHBOARD_PATH = PLANNING_DIR / "WIP_DASHBOARD.md"
INITIATIVE_DIR_RE = re.compile(r"^(\d{2}[a-z]?)-(.+)$")
H1_RE = re.compile(r"^#\s+(.+?)$", re.MULTILINE)
STATUS_RE = re.compile(r"\*\*?Status:?\*?\*?\s*(.+?)$", re.MULTILINE | re.IGNORECASE)
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
LAST_REVIEW_RE = re.compile(r"^last_review\s*:\s*([^\s]+)\s*$", re.MULTILINE)
DATE_RE = re.compile(r"\*\*?Date:?\*?\*?\s*(\d{4}-\d{2}-\d{2})", re.MULTILINE | re.IGNORECASE)

BEGIN_MARKER = "<!-- BEGIN AUTO -->"
END_MARKER = "<!-- END AUTO -->"


def _read_initiative(folder: Path) -> dict[str, str] | None:
    m = INITIATIVE_DIR_RE.match(folder.name)
    if not m:
        return None
    seq = m.group(1)
    slug = m.group(2)
    roadmap = folder / "master-roadmap.md"
    if not roadmap.is_file():
        return {
            "seq": seq, "slug": slug, "title": "(no master-roadmap.md)",
            "status": "unknown", "date": "—", "folder": folder.name,
        }
    text = roadmap.read_text(encoding="utf-8")
    # Strip frontmatter for H1 + Status + Date scans (these often appear in body).
    fm_match = FRONTMATTER_RE.match(text)
    body = text[fm_match.end():] if fm_match else text
    fm_block = fm_match.group(1) if fm_match else ""

    h1 = H1_RE.search(body)
    title = h1.group(1).strip() if h1 else slug

    status_match = STATUS_RE.search(body)
    status = status_match.group(1).strip().rstrip(".") if status_match else "open"
    # Trim noisy markup.
    status = re.sub(r"\s+", " ", status)
    if len(status) > 80:
        status = status[:77] + "..."

    # Date: prefer frontmatter last_review; else body Date: line.
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
        "status": status, "date": date, "folder": folder.name,
    }


def _scan_initiatives() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for p in sorted(PLANNING_DIR.iterdir()):
        if not p.is_dir() or p.name.startswith(".") or p.name == "99-proposals":
            continue
        row = _read_initiative(p)
        if row is not None:
            rows.append(row)
    rows.sort(key=lambda r: r["seq"])
    return rows


def _render_table(rows: list[dict[str, str]]) -> str:
    lines = [
        "| Seq | Folder | Status | Last review | Title |",
        "|:---:|:-------|:-------|:-----------:|:------|",
    ]
    for r in rows:
        # Trim title to keep table readable.
        title = r["title"]
        if len(title) > 90:
            title = title[:87] + "..."
        lines.append(
            f"| **{r['seq']}** | [`{r['folder']}/`]({r['folder']}/) | "
            f"{r['status']} | {r['date']} | {title} |"
        )
    return "\n".join(lines) + "\n"


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
    table = _render_table(rows)
    new_text = _splice_into_dashboard(table)

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
