"""Initiative 31 P3 — Tests for CHANNEL_TOUCHPOINT_REGISTRY.csv schema + validator."""
from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "CHANNEL_TOUCHPOINT_REGISTRY.csv"
PERSONA_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "PERSONA_REGISTRY.csv"
TOPIC_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "TOPIC_REGISTRY.csv"

CHANNEL_ID_RE = re.compile(r"^CHAN-[A-Z][A-Z0-9-]{2,40}$")
DISTANCE_TOKEN_RE = re.compile(r"^N[1-4](-N[1-4])?$")


def _topic_ids() -> set[str]:
    with TOPIC_CSV.open(encoding="utf-8", newline="") as fh:
        return {(r.get("topic_id") or "").strip() for r in csv.DictReader(fh)}


def _persona_ids() -> set[str]:
    if not PERSONA_CSV.is_file():
        return set()
    with PERSONA_CSV.open(encoding="utf-8", newline="") as fh:
        return {(r.get("persona_id") or "").strip() for r in csv.DictReader(fh)}


def test_channel_csv_exists():
    assert CSV_PATH.is_file(), f"missing {CSV_PATH}"


def test_channel_header_matches_contract():
    from akos.hlk_channel_touchpoint_registry_csv import CHANNEL_TOUCHPOINT_REGISTRY_FIELDNAMES

    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        assert tuple(reader.fieldnames or ()) == CHANNEL_TOUCHPOINT_REGISTRY_FIELDNAMES


def test_channel_at_least_10_rows():
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) >= 10, f"expected >=10 channels, got {len(rows)}"


def test_channel_ids_match_regex_and_unique():
    seen: set[str] = set()
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            cid = (row.get("channel_id") or "").strip()
            assert CHANNEL_ID_RE.match(cid), f"channel_id {cid!r} fails regex"
            assert cid not in seen, f"duplicate channel_id {cid!r}"
            seen.add(cid)


def test_channel_distance_bands_valid():
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            band = (row.get("typical_distance_band_inbound") or "").strip()
            assert DISTANCE_TOKEN_RE.match(band), f"row {row['channel_id']}: invalid distance {band!r}"


def test_channel_persona_fk_resolves():
    canonical = _persona_ids()
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            personas = (row.get("typical_personas") or "").strip()
            for pid in personas.split(";"):
                pid = pid.strip()
                if pid:
                    assert pid in canonical, (
                        f"channel {row['channel_id']}: typical_persona {pid!r} not in PERSONA_REGISTRY"
                    )


def test_topic_channel_touchpoint_registry_registered():
    assert "topic_channel_touchpoint_registry" in _topic_ids()


def test_validate_channel_touchpoint_registry_script_passes():
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "validate_channel_touchpoint_registry.py")],
        cwd=str(REPO_ROOT),
        capture_output=True, text=True, timeout=30,
    )
    assert proc.returncode == 0, f"rc={proc.returncode}\nstdout={proc.stdout}\nstderr={proc.stderr}"
