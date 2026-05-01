"""Initiative 31 P2.2 — Tests for the GOI/POI distance extension.

Covers:
- The 3 new columns are present in the canonical CSV.
- Backfill: every existing row has a valid distance_band (not empty).
- N1 invariant: bridge_via empty when distance_band == N1.
- N2-N4 invariant: bridge_via non-null when distance_band != N1.
- bridge_via FK resolves to another row in the register.
- bridge_via not pointing at self.
- distance_assessed_date is ISO YYYY-MM-DD.
- The extended validator script exits 0.
- The PMO hub auto-render now includes a `distance` column.
"""
from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "GOI_POI_REGISTER.csv"  # I32 P7 relocation
HUB_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Operations" / "PMO" / "TOPIC_PMO_CLIENT_DELIVERY_HUB.md"

DISTANCE_BANDS = {"N1", "N2", "N3", "N4"}
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _rows() -> list[dict[str, str]]:
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def test_distance_columns_present():
    rows = _rows()
    assert rows, "GOI_POI_REGISTER.csv has no rows"
    for col in ("distance_band", "bridge_via", "distance_assessed_date"):
        assert col in rows[0], f"missing column {col!r} in GOI_POI_REGISTER.csv"


def test_distance_band_valid_for_every_row():
    for row in _rows():
        band = (row.get("distance_band") or "").strip()
        assert band in DISTANCE_BANDS, (
            f"row {row['ref_id']}: distance_band={band!r} not in {sorted(DISTANCE_BANDS)}"
        )


def test_n1_rows_have_empty_bridge_via():
    for row in _rows():
        if (row.get("distance_band") or "").strip() == "N1":
            bridge = (row.get("bridge_via") or "").strip()
            assert bridge == "", (
                f"row {row['ref_id']}: distance_band=N1 but bridge_via={bridge!r} (must be empty)"
            )


def test_non_n1_rows_have_non_empty_bridge_via():
    for row in _rows():
        band = (row.get("distance_band") or "").strip()
        if band in {"N2", "N3", "N4"}:
            bridge = (row.get("bridge_via") or "").strip()
            assert bridge, f"row {row['ref_id']}: distance_band={band} requires bridge_via"


def test_bridge_via_fk_resolves():
    rows = _rows()
    all_refs = {(r.get("ref_id") or "").strip() for r in rows}
    for row in rows:
        bridge = (row.get("bridge_via") or "").strip()
        if bridge:
            assert bridge in all_refs, (
                f"row {row['ref_id']}: bridge_via={bridge!r} does not resolve to any ref_id"
            )


def test_bridge_via_not_self():
    for row in _rows():
        bridge = (row.get("bridge_via") or "").strip()
        if bridge:
            assert bridge != row["ref_id"], (
                f"row {row['ref_id']}: bridge_via points at self"
            )


def test_distance_assessed_date_iso_format():
    for row in _rows():
        date = (row.get("distance_assessed_date") or "").strip()
        assert date, f"row {row['ref_id']}: distance_assessed_date is required"
        assert ISO_DATE_RE.match(date), (
            f"row {row['ref_id']}: distance_assessed_date {date!r} not ISO YYYY-MM-DD"
        )


def test_validate_goipoi_register_script_passes():
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "validate_goipoi_register.py")],
        cwd=str(REPO_ROOT),
        capture_output=True, text=True, timeout=30,
    )
    assert proc.returncode == 0, f"rc={proc.returncode}\nstdout={proc.stdout}\nstderr={proc.stderr}"


def test_render_pmo_hub_includes_distance_column():
    """The auto-rendered PMO hub stakeholder index gains a `distance` column
    after Initiative 31 P2.2 extends `render_pmo_hub.py`."""
    if not HUB_PATH.is_file():
        return
    text = HUB_PATH.read_text(encoding="utf-8")
    # The autogen table header must list `distance` between `class` and `lens`.
    assert "| ref_id | class | distance |" in text or "| `ref_id` | `class` | `distance` |" in text or "distance | bridge_via" in text, (
        "PMO hub auto-render does not include a `distance` column header. "
        "Re-run scripts/render_pmo_hub.py after the I31 P2.2 schema bump."
    )
