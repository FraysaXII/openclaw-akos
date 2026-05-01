"""Tests for TOUCHPOINT_KIT_CELL_REGISTRY.csv (Initiative 32 P3).

Locks the cell-registry contract and the keystone FS-vs-CSV drift invariant:
- Header matches TOUCHPOINT_KIT_CELL_FIELDNAMES.
- Seed count matches filesystem cell count (15 today; 8 distinct persona x channel combos).
- Every cell_id matches ^CELL-[A-Z0-9-]{4,80}-(EN|ES|FR)$ and is unique.
- persona_id, channel_id, topic_ids resolve to their canonical CSVs.
- language is in {en, es, fr}; distance bands in {N1, N2, N3, N4}.
- template_path exists on disk for every row (FS-drift gate).
- **Planted-phantom regression** (the keystone invariant test):
  the validator detects an injected CSV row that points at a non-existent file
  AND a CSV row that omits a real on-disk file.
- Validator passes against the shipped CSV and against the dispatcher.
"""

from __future__ import annotations

import csv
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "TOUCHPOINT_KIT_CELL_REGISTRY.csv"
TOPIC_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "TOPIC_REGISTRY.csv"
PERSONA_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "PERSONA_REGISTRY.csv"
CHANNEL_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "CHANNEL_TOUCHPOINT_REGISTRY.csv"
VALIDATOR = REPO_ROOT / "scripts" / "validate_touchpoint_kit_cells.py"
TKIT_ROOT = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "_assets" / "touchpoint-kit"


@pytest.fixture(scope="module")
def rows() -> list[dict]:
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def test_csv_exists() -> None:
    assert CSV_PATH.is_file(), f"missing {CSV_PATH}"


def test_header_matches_contract() -> None:
    sys.path.insert(0, str(REPO_ROOT))
    from akos.hlk_touchpoint_kit_cell_csv import TOUCHPOINT_KIT_CELL_FIELDNAMES

    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        assert reader.fieldnames == list(TOUCHPOINT_KIT_CELL_FIELDNAMES), (
            f"header mismatch:\n  expected: {list(TOUCHPOINT_KIT_CELL_FIELDNAMES)}\n  got:      {reader.fieldnames}"
        )


def test_cell_id_format_and_uniqueness(rows: list[dict]) -> None:
    pattern = re.compile(r"^CELL-[A-Z0-9-]{4,80}-(EN|ES|FR)$")
    seen: set[str] = set()
    for r in rows:
        cid = r["cell_id"]
        assert pattern.match(cid), f"cell_id {cid!r} does not match {pattern.pattern}"
        assert cid not in seen, f"duplicate cell_id {cid!r}"
        seen.add(cid)


def test_persona_id_resolves(rows: list[dict]) -> None:
    with PERSONA_PATH.open(encoding="utf-8", newline="") as fh:
        persona_ids = {r["persona_id"].strip() for r in csv.DictReader(fh)}
    for r in rows:
        assert r["persona_id"] in persona_ids, (
            f"{r['cell_id']}: persona_id {r['persona_id']!r} not in PERSONA_REGISTRY.csv"
        )


def test_channel_id_resolves(rows: list[dict]) -> None:
    with CHANNEL_PATH.open(encoding="utf-8", newline="") as fh:
        channel_ids = {r["channel_id"].strip() for r in csv.DictReader(fh)}
    for r in rows:
        assert r["channel_id"] in channel_ids, (
            f"{r['cell_id']}: channel_id {r['channel_id']!r} not in CHANNEL_TOUCHPOINT_REGISTRY.csv"
        )


def test_language_in_allowed_set(rows: list[dict]) -> None:
    sys.path.insert(0, str(REPO_ROOT))
    from akos.hlk_touchpoint_kit_cell_csv import ALLOWED_LANGUAGES

    for r in rows:
        assert r["language"] in ALLOWED_LANGUAGES, (
            f"{r['cell_id']}: language {r['language']!r} not in {sorted(ALLOWED_LANGUAGES)}"
        )


def test_distance_bands_valid(rows: list[dict]) -> None:
    sys.path.insert(0, str(REPO_ROOT))
    from akos.hlk_touchpoint_kit_cell_csv import VALID_DISTANCE_BANDS

    for r in rows:
        for band in (r["distance_variants_in_file"] or "").split(";"):
            band = band.strip()
            if not band:
                continue
            assert band in VALID_DISTANCE_BANDS, (
                f"{r['cell_id']}: distance band {band!r} not in {sorted(VALID_DISTANCE_BANDS)}"
            )


def test_template_path_exists_for_every_row(rows: list[dict]) -> None:
    """FS-drift gate: every CSV row points at a real file on disk."""
    for r in rows:
        abs_path = REPO_ROOT / r["template_path"]
        assert abs_path.is_file(), (
            f"{r['cell_id']}: template_path {r['template_path']!r} not on disk (FS-drift)"
        )


def test_topic_ids_resolve(rows: list[dict]) -> None:
    with TOPIC_PATH.open(encoding="utf-8", newline="") as fh:
        topic_ids = {r["topic_id"].strip() for r in csv.DictReader(fh)}
    for r in rows:
        for tid in (r["topic_ids"] or "").split(";"):
            tid = tid.strip()
            if not tid:
                continue
            assert tid in topic_ids, f"{r['cell_id']}: topic_id {tid!r} not in TOPIC_REGISTRY.csv"


def test_topic_touchpoint_kit_cell_registry_row_exists() -> None:
    """P3-A4: topic_touchpoint_kit_cell_registry row added to TOPIC_REGISTRY.csv."""
    with TOPIC_PATH.open(encoding="utf-8", newline="") as fh:
        topic_ids = {r["topic_id"].strip() for r in csv.DictReader(fh)}
    assert "topic_touchpoint_kit_cell_registry" in topic_ids


def test_csv_count_matches_filesystem() -> None:
    """Every (persona/channel/intro_message_<lang>.md) on disk must appear in CSV."""
    fs_files: set[tuple[str, str, str]] = set()
    for persona_dir in TKIT_ROOT.iterdir():
        if not persona_dir.is_dir() or not persona_dir.name.startswith("PERSONA-"):
            continue
        for channel_dir in persona_dir.iterdir():
            if not channel_dir.is_dir() or not channel_dir.name.startswith("CHAN-"):
                continue
            for f in channel_dir.iterdir():
                m = re.match(r"^intro_message_(en|es|fr)\.md$", f.name)
                if m:
                    fs_files.add((persona_dir.name, channel_dir.name, m.group(1)))
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        csv_files = {(r["persona_id"], r["channel_id"], r["language"]) for r in csv.DictReader(fh)}
    assert csv_files == fs_files, (
        f"FS-vs-CSV drift: missing in CSV {fs_files - csv_files}, phantom in CSV {csv_files - fs_files}"
    )


def test_validator_script_exits_zero() -> None:
    r = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=30,
    )
    assert r.returncode == 0, (
        f"validate_touchpoint_kit_cells.py exited {r.returncode}; stdout: {r.stdout}; stderr: {r.stderr}"
    )
    assert "PASS" in r.stdout


def test_validator_runs_under_dispatcher() -> None:
    r = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "validate_hlk.py")],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=120,
    )
    assert r.returncode == 0
    assert "TOUCHPOINT_KIT_CELL_REGISTRY: PASS" in r.stdout


def test_planted_phantom_csv_row_is_caught(tmp_path: Path) -> None:
    """KEYSTONE INVARIANT: validator catches a CSV row whose template_path
    points at a non-existent file (phantom in CSV)."""
    sys.path.insert(0, str(REPO_ROOT))
    from akos.hlk_touchpoint_kit_cell_csv import TOUCHPOINT_KIT_CELL_FIELDNAMES

    # Stage a working copy of the CSV with one phantom row appended.
    staged_csv = tmp_path / "TOUCHPOINT_KIT_CELL_REGISTRY.csv"
    shutil.copy(CSV_PATH, staged_csv)
    with staged_csv.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(TOUCHPOINT_KIT_CELL_FIELDNAMES))
        writer.writerow({
            "cell_id": "CELL-PHANTOM-NOT-ON-DISK-EN",
            "persona_id": "PERSONA-INVESTOR-COLD",
            "channel_id": "CHAN-LINKEDIN-DM",
            "language": "en",
            "topic_ids": "topic_holistik_ops_discovery",
            "template_path": "docs/references/hlk/v3.0/_assets/touchpoint-kit/PERSONA-PHANTOM/CHAN-PHANTOM/intro_message_en.md",
            "distance_variants_in_file": "N4",
            "lifecycle_status": "active",
            "last_review": "2026-04-30",
            "notes": "planted phantom for regression test; not a real cell",
        })

    # Swap the live CSV with the phantom one for the duration of this test.
    backup = tmp_path / "real.csv"
    shutil.copy(CSV_PATH, backup)
    try:
        shutil.copy(staged_csv, CSV_PATH)
        r = subprocess.run(
            [sys.executable, str(VALIDATOR)],
            capture_output=True, text=True, cwd=REPO_ROOT, timeout=30,
        )
        assert r.returncode != 0, (
            "validator did not catch planted phantom row; output:\n" + r.stdout
        )
        assert "FS-drift" in r.stdout or "not found on disk" in r.stdout
    finally:
        shutil.copy(backup, CSV_PATH)


def test_planted_missing_csv_row_is_caught(tmp_path: Path) -> None:
    """KEYSTONE INVARIANT: validator catches a real on-disk file that has no
    matching CSV row (missing in CSV)."""
    # Stage a working copy of the CSV with one row removed (the first row after
    # the header). The corresponding file remains on disk.
    backup = tmp_path / "real.csv"
    shutil.copy(CSV_PATH, backup)
    try:
        with CSV_PATH.open(encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            fieldnames = list(reader.fieldnames or [])
            all_rows = list(reader)
        # Remove the first row (its file stays on disk -> drift).
        kept = all_rows[1:]
        with CSV_PATH.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(kept)
        r = subprocess.run(
            [sys.executable, str(VALIDATOR)],
            capture_output=True, text=True, cwd=REPO_ROOT, timeout=30,
        )
        assert r.returncode != 0, (
            "validator did not catch missing CSV row for on-disk file; output:\n" + r.stdout
        )
        assert "FS-drift" in r.stdout
    finally:
        shutil.copy(backup, CSV_PATH)
