"""Initiative 31 P5.2 — Tests for SOURCING_REGISTER.csv schema + validator."""
from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "SOURCING_REGISTER.csv"
TOPIC_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "TOPIC_REGISTRY.csv"

VENDOR_ID_RE = re.compile(r"^VENDOR-[A-Z][A-Z0-9-]{2,40}$")
DISTANCE_BANDS = {"N1", "N2", "N3", "N4"}


def _topic_ids() -> set[str]:
    with TOPIC_CSV.open(encoding="utf-8", newline="") as fh:
        return {(r.get("topic_id") or "").strip() for r in csv.DictReader(fh)}


def test_sourcing_csv_exists():
    assert CSV_PATH.is_file(), f"missing {CSV_PATH}"


def test_sourcing_header_matches_contract():
    from akos.hlk_sourcing_register_csv import SOURCING_REGISTER_FIELDNAMES

    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        assert tuple(reader.fieldnames or ()) == SOURCING_REGISTER_FIELDNAMES


def test_sourcing_distance_bands_present():
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            for col in ("distance_band_at_first_contact", "current_distance_band"):
                band = (row.get(col) or "").strip()
                assert band in DISTANCE_BANDS, f"row {row['vendor_id']}: invalid {col}={band!r}"


def test_topic_sourcing_register_registered():
    assert "topic_sourcing_register" in _topic_ids()


def test_validate_sourcing_register_script_passes():
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "validate_sourcing_register.py")],
        cwd=str(REPO_ROOT),
        capture_output=True, text=True, timeout=30,
    )
    assert proc.returncode == 0, f"rc={proc.returncode}\nstdout={proc.stdout}\nstderr={proc.stderr}"


def test_outbound_brief_template_exists_for_three_locales():
    base = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Operations" / "PMO" / "sourcing-briefs"
    for loc in ("en", "es", "fr"):
        path = base / f"TEMPLATE_OUTBOUND_BRIEF_{loc}.md"
        assert path.is_file(), f"missing template for locale {loc}: {path}"
