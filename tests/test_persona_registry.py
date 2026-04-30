"""Initiative 31 P2.1 — Tests for PERSONA_REGISTRY.csv schema + validator.

Covers:
- The CSV exists at the canonical location.
- The header matches ``PERSONA_REGISTRY_FIELDNAMES``.
- Every row's ``persona_id`` matches the documented regex.
- Every row's ``typical_distance_band`` is a valid band or band-range token.
- Every row's ``typical_channels`` resolves into ``CHANNEL_TOUCHPOINT_REGISTRY.csv``.
- Every row's ``linked_topic_ids`` resolves into ``TOPIC_REGISTRY.csv``.
- ``topic_persona_registry`` is registered in the topic registry.
- ``scripts/validate_persona_registry.py`` exits 0 on the canonical CSV.
"""
from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "PERSONA_REGISTRY.csv"
CHANNEL_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "CHANNEL_TOUCHPOINT_REGISTRY.csv"
TOPIC_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "TOPIC_REGISTRY.csv"

PERSONA_ID_RE = re.compile(r"^PERSONA-[A-Z][A-Z0-9-]{2,40}$")
DISTANCE_TOKEN_RE = re.compile(r"^N[1-4](-N[1-4])?$")


def _topic_ids() -> set[str]:
    with TOPIC_CSV.open(encoding="utf-8", newline="") as fh:
        return {(r.get("topic_id") or "").strip() for r in csv.DictReader(fh)}


def _channel_ids() -> set[str]:
    if not CHANNEL_CSV.is_file():
        return set()
    with CHANNEL_CSV.open(encoding="utf-8", newline="") as fh:
        return {(r.get("channel_id") or "").strip() for r in csv.DictReader(fh)}


def test_persona_csv_exists():
    assert CSV_PATH.is_file(), f"missing {CSV_PATH}"


def test_persona_header_matches_contract():
    from akos.hlk_persona_registry_csv import PERSONA_REGISTRY_FIELDNAMES

    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        assert tuple(reader.fieldnames or ()) == PERSONA_REGISTRY_FIELDNAMES


def test_persona_at_least_16_rows():
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) >= 16, f"expected >=16 personas, got {len(rows)}"


def test_persona_ids_match_regex_and_unique():
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    seen: set[str] = set()
    for row in rows:
        pid = (row.get("persona_id") or "").strip()
        assert PERSONA_ID_RE.match(pid), f"persona_id {pid!r} fails regex"
        assert pid not in seen, f"duplicate persona_id {pid!r}"
        seen.add(pid)


def test_persona_distance_bands_valid():
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            band = (row.get("typical_distance_band") or "").strip()
            assert DISTANCE_TOKEN_RE.match(band), f"row {row['persona_id']}: invalid distance {band!r}"


def test_persona_channel_fk_resolves():
    canonical = _channel_ids()
    if not canonical:
        return  # channel registry not yet created; covered by test_channel_touchpoint_registry
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            chans = (row.get("typical_channels") or "").strip()
            for cid in chans.split(";"):
                cid = cid.strip()
                if cid:
                    assert cid in canonical, (
                        f"persona {row['persona_id']}: channel_id {cid!r} not in CHANNEL_TOUCHPOINT_REGISTRY"
                    )


def test_persona_topic_fk_resolves():
    canonical = _topic_ids()
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            topics = (row.get("linked_topic_ids") or "").strip()
            for tid in topics.split(";"):
                tid = tid.strip()
                if tid:
                    assert tid in canonical, (
                        f"persona {row['persona_id']}: linked_topic_id {tid!r} not in TOPIC_REGISTRY"
                    )


def test_topic_persona_registry_registered():
    assert "topic_persona_registry" in _topic_ids()


def test_validate_persona_registry_script_passes():
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "validate_persona_registry.py")],
        cwd=str(REPO_ROOT),
        capture_output=True, text=True, timeout=30,
    )
    assert proc.returncode == 0, f"rc={proc.returncode}\nstdout={proc.stdout}\nstderr={proc.stderr}"
