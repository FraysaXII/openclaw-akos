"""P13.4 (D-W13-D) + I70 P8.5 (D-IH-70-AD) — Tests for the GOI/POI optional
schema-extension columns: `related_party` (P13.4) and `stance` (I70 P8.5).

Covers:
- The `related_party` column is present in the canonical CSV header.
- The `stance` column is present in the canonical CSV header AND is the LAST
  NON-review-stamp column (the forward-compatible-append invariant moved from
  related_party to stance after I70 P8.5; then the I71 P4 follow-up
  D-IH-71-R appended the 4-column review-stamp suffix at the very end of every
  mirrored canonical CSV — see `scripts/validate_review_stamps.py
  REVIEW_STAMP_COLUMNS` — so stance is now the last column BEFORE that
  suffix, not the absolute last column).
- The `GOIPOI_REGISTER_FIELDNAMES` tuple includes both columns; stance sits
  immediately before the review-stamp suffix.
- Default-empty values are backwards-compatible for every Initiative 21 / 22 /
  24 / 31 / P13.4 row.
- The `GOI-CUS-ASES-2026` row carries `related_party=true` per the P13.4 tranche.
- Every row's `stance` value is in the enum {'', 'ally', 'neutral', 'enemy', 'unknown'}.
- The validator script (`scripts/validate_goipoi_register.py`) exits 0 with the
  expanded enum (P13.4 + I70 P8.5).
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


def test_stance_column_present_and_last_before_review_stamp_suffix():
    """I70 P8.5 (D-IH-70-AD) — `stance` is the new last column for
    forward-compatible appends; the invariant moved from related_party to
    stance when the v2.7 ally/neutral/enemy doctrine landed in v3.1.

    I71 P4 follow-up (D-IH-71-R) — the review-stamp 4-tuple
    (`last_review_at`, `last_review_by`, `last_review_decision_id`,
    `methodology_version_at_review`) was appended to every mirrored canonical
    CSV (see `scripts/validate_review_stamps.py` `REVIEW_STAMP_COLUMNS`), so
    `stance` is no longer the absolute last column — it's the last column
    BEFORE the review-stamp suffix. Renamed from
    `test_stance_column_present_and_last` in the post-I71 release-gate hygiene
    pass; assertion semantics adjusted to recognize the review-stamp doctrine
    while preserving the forward-compatible-append intent for the stance row.
    """
    sys.path.insert(0, str(REPO_ROOT))
    from scripts.validate_review_stamps import REVIEW_STAMP_COLUMNS

    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        header = next(reader)
    assert "stance" in header, "stance column missing from GOI_POI_REGISTER.csv header"
    suffix_len = len(REVIEW_STAMP_COLUMNS)
    assert tuple(header[-suffix_len:]) == REVIEW_STAMP_COLUMNS, (
        f"GOI_POI_REGISTER.csv must end with the review-stamp suffix "
        f"{REVIEW_STAMP_COLUMNS}; got trailing columns={tuple(header[-suffix_len:])!r}"
    )
    assert header[-(suffix_len + 1)] == "stance", (
        f"stance should be the LAST column BEFORE the review-stamp suffix "
        f"(forward-compatible-append invariant per I70 P8.5 + I71 P4 D-IH-71-R); "
        f"got header[-{suffix_len + 1}]={header[-(suffix_len + 1)]!r}"
    )


def test_fieldnames_tuple_includes_related_party_and_stance():
    sys.path.insert(0, str(REPO_ROOT))
    from akos.hlk_goipoi_csv import GOIPOI_REGISTER_FIELDNAMES
    from scripts.validate_review_stamps import REVIEW_STAMP_COLUMNS

    assert "related_party" in GOIPOI_REGISTER_FIELDNAMES, (
        "GOIPOI_REGISTER_FIELDNAMES does not include 'related_party'"
    )
    assert "stance" in GOIPOI_REGISTER_FIELDNAMES, (
        "GOIPOI_REGISTER_FIELDNAMES does not include 'stance' (I70 P8.5 D-IH-70-AD)"
    )
    suffix_len = len(REVIEW_STAMP_COLUMNS)
    assert GOIPOI_REGISTER_FIELDNAMES[-suffix_len:] == REVIEW_STAMP_COLUMNS, (
        f"GOIPOI_REGISTER_FIELDNAMES must end with the review-stamp suffix "
        f"{REVIEW_STAMP_COLUMNS}; got trailing entries="
        f"{GOIPOI_REGISTER_FIELDNAMES[-suffix_len:]!r}"
    )
    assert GOIPOI_REGISTER_FIELDNAMES[-(suffix_len + 1)] == "stance", (
        "stance must be the last entry in GOIPOI_REGISTER_FIELDNAMES BEFORE "
        "the review-stamp suffix (forward-compatible appends per I70 P8.5 + "
        "I71 P4 D-IH-71-R)"
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


def test_stance_enum_valid():
    """Every row's `stance` value must be in the enum
    {'', 'ally', 'neutral', 'enemy', 'unknown'} (I70 P8.5 D-IH-70-AD)."""
    rows = _rows()
    valid = {"", "ally", "neutral", "enemy", "unknown"}
    for row in rows:
        stance = (row.get("stance") or "").strip().lower()
        assert stance in valid, (
            f"row {row['ref_id']}: invalid stance={stance!r}; "
            f"expected one of {sorted(valid)}"
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
