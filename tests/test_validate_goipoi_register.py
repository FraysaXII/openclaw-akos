"""P13.4 (D-W13-D) — Tests for the GOI/POI `related_party` column.

Covers:
- The new `related_party` column is present in the canonical CSV header.
- The `GOIPOI_REGISTER_FIELDNAMES` tuple includes `related_party` as the last column.
- Default-empty values are backwards-compatible for every Initiative 21 / 22 / 24 / 31 row.
- The new `GOI-CUS-ASES-2026` row carries `related_party=true` per the P13.4 tranche.
- The validator script (`scripts/validate_goipoi_register.py`) exits 0 with the expanded enum.
"""
from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals"
    / "dimensions"
    / "GOI_POI_REGISTER.csv"
)


def _rows() -> list[dict[str, str]]:
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def test_related_party_column_present_in_header():
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        header = next(reader)
    assert "related_party" in header, "related_party column missing from GOI_POI_REGISTER.csv header"
    assert header[-1] == "related_party", (
        f"related_party should be the LAST column for forward-compatible appends; got header={header[-1]!r}"
    )


def test_fieldnames_tuple_includes_related_party():
    sys.path.insert(0, str(REPO_ROOT))
    from akos.hlk_goipoi_csv import GOIPOI_REGISTER_FIELDNAMES

    assert "related_party" in GOIPOI_REGISTER_FIELDNAMES, (
        "GOIPOI_REGISTER_FIELDNAMES does not include 'related_party'"
    )
    assert GOIPOI_REGISTER_FIELDNAMES[-1] == "related_party", (
        "related_party must be the last entry in GOIPOI_REGISTER_FIELDNAMES (forward-compatible appends)"
    )


def test_related_party_default_empty_backward_compat():
    """Initiative 21 / 22 / 24 / 31 rows must keep `related_party=''` (the
    backwards-compatible default). Only rows the operator explicitly flags get
    'true' or 'false'. This invariant lets future ALTER migrations stay additive."""
    rows = _rows()
    legacy_prefixes = (
        "GOI-ADV-",
        "GOI-BNK-",
        "POI-BNK-",
        "POI-LEG-",
        "POI-ADV-",
        "GOI-PRT-",
        "POI-PRT-",
        "GOI-CUS-SUEZ-",
        "POI-CUS-SUEZ-",
    )
    for row in rows:
        ref_id = row["ref_id"]
        if any(ref_id.startswith(p) for p in legacy_prefixes):
            related = (row.get("related_party") or "").strip()
            assert related == "", (
                f"row {ref_id}: legacy row should have empty related_party (backwards-compat); got {related!r}"
            )


def test_related_party_enum_valid():
    """Every row's `related_party` value must be in the enum {'', 'true', 'false'}."""
    rows = _rows()
    valid = {"", "true", "false"}
    for row in rows:
        related = (row.get("related_party") or "").strip().lower()
        assert related in valid, (
            f"row {row['ref_id']}: invalid related_party={related!r}; "
            f"expected one of {sorted(valid)}"
        )


def test_goi_cus_ases_2026_is_related_party():
    """The Asesoría Hostelería row added in P13.4 is the canonical first
    related-party row in the register."""
    rows = _rows()
    ases = [r for r in rows if r["ref_id"] == "GOI-CUS-ASES-2026"]
    assert ases, "GOI-CUS-ASES-2026 row not found in GOI_POI_REGISTER.csv"
    assert len(ases) == 1, f"expected exactly one GOI-CUS-ASES-2026 row, got {len(ases)}"
    row = ases[0]
    assert row["class"] == "client_org", (
        f"GOI-CUS-ASES-2026: class should be 'client_org', got {row['class']!r}"
    )
    assert (row.get("related_party") or "").strip().lower() == "true", (
        f"GOI-CUS-ASES-2026: related_party should be 'true', got {row.get('related_party')!r}"
    )


def test_validate_goipoi_register_script_passes():
    """The extended validator must exit 0 with the related_party enum addition."""
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "validate_goipoi_register.py")],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0, (
        f"validate_goipoi_register.py failed: rc={proc.returncode}\n"
        f"stdout={proc.stdout}\nstderr={proc.stderr}"
    )
