"""Tests for POLICY_REGISTER.csv (Initiative 32 P4)."""

from __future__ import annotations

import csv
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "POLICY_REGISTER.csv"
TOPIC_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "TOPIC_REGISTRY.csv"
ORG_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "baseline_organisation.csv"
VALIDATOR = REPO_ROOT / "scripts" / "validate_policy_register.py"


@pytest.fixture(scope="module")
def rows() -> list[dict]:
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def test_csv_exists() -> None:
    assert CSV_PATH.is_file(), f"missing {CSV_PATH}"


def test_header_matches_contract() -> None:
    sys.path.insert(0, str(REPO_ROOT))
    from akos.hlk_policy_register_csv import POLICY_REGISTER_FIELDNAMES

    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        assert reader.fieldnames == list(POLICY_REGISTER_FIELDNAMES)


def test_policy_id_format_and_uniqueness(rows: list[dict]) -> None:
    pattern = re.compile(r"^POL-[A-Z0-9-]{4,80}$")
    seen: set[str] = set()
    for r in rows:
        pid = r["policy_id"]
        assert pattern.match(pid), f"policy_id {pid!r} does not match {pattern.pattern}"
        assert pid not in seen, f"duplicate policy_id {pid!r}"
        seen.add(pid)


def test_policy_class_in_enum(rows: list[dict]) -> None:
    sys.path.insert(0, str(REPO_ROOT))
    from akos.hlk_policy_register_csv import VALID_POLICY_CLASSES

    for r in rows:
        assert r["policy_class"] in VALID_POLICY_CLASSES, (
            f"{r['policy_id']}: policy_class {r['policy_class']!r} not in {sorted(VALID_POLICY_CLASSES)}"
        )


def test_cadence_in_enum(rows: list[dict]) -> None:
    sys.path.insert(0, str(REPO_ROOT))
    from akos.hlk_policy_register_csv import VALID_CADENCES

    for r in rows:
        assert r["cadence"] in VALID_CADENCES, (
            f"{r['policy_id']}: cadence {r['cadence']!r} not in {sorted(VALID_CADENCES)}"
        )


def test_owner_role_resolves_to_baseline_org(rows: list[dict]) -> None:
    with ORG_PATH.open(encoding="utf-8", newline="") as fh:
        org_roles = {r["role_name"].strip() for r in csv.DictReader(fh)}
    for r in rows:
        assert r["owner_role"] in org_roles, (
            f"{r['policy_id']}: owner_role {r['owner_role']!r} not in baseline_organisation.csv"
        )


def test_dates_parse_and_next_after_last(rows: list[dict]) -> None:
    pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    for r in rows:
        assert pattern.match(r["last_review"]), f"{r['policy_id']}: last_review not YYYY-MM-DD"
        assert pattern.match(r["next_review"]), f"{r['policy_id']}: next_review not YYYY-MM-DD"
        ly, lm, ld = (int(x) for x in r["last_review"].split("-"))
        ny, nm, nd = (int(x) for x in r["next_review"].split("-"))
        assert date(ny, nm, nd) >= date(ly, lm, ld), (
            f"{r['policy_id']}: next_review < last_review"
        )


def test_topic_ids_resolve(rows: list[dict]) -> None:
    with TOPIC_PATH.open(encoding="utf-8", newline="") as fh:
        topic_ids = {r["topic_id"].strip() for r in csv.DictReader(fh)}
    for r in rows:
        for tid in (r["topic_ids"] or "").split(";"):
            tid = tid.strip()
            if not tid:
                continue
            assert tid in topic_ids, f"{r['policy_id']}: topic_id {tid!r} not in TOPIC_REGISTRY.csv"


def test_topic_policy_register_row_exists() -> None:
    """P4-A4: topic_policy_register row added to TOPIC_REGISTRY.csv."""
    with TOPIC_PATH.open(encoding="utf-8", newline="") as fh:
        topic_ids = {r["topic_id"].strip() for r in csv.DictReader(fh)}
    assert "topic_policy_register" in topic_ids


def test_seed_covers_all_4_i32_policy_classes(rows: list[dict]) -> None:
    """Per the I32 P4 plan: seed covers RLS + service_role_rotation + redaction + pii_scope.
    I45 P4 added cost_ceiling as a 5th class; this test now asserts the I32 4 are present
    (superset is OK)."""
    classes = {r["policy_class"] for r in rows}
    i32_required = {"rls", "service_role_rotation", "redaction", "pii_scope"}
    missing = i32_required - classes
    assert not missing, f"expected I32 P4 classes present; missing: {missing}"


def test_seed_includes_i32_self_referential_row(rows: list[dict]) -> None:
    """P4 is self-referential: the policy register's own RLS rule is a policy_register row."""
    ids = {r["policy_id"] for r in rows}
    assert "POL-RLS-POLICY-REGISTER-MIRROR-I32" in ids


def test_seed_includes_i26_quarterly_service_role_rotation(rows: list[dict]) -> None:
    """The I26 P2 cadence is the only service_role_rotation row in the seed."""
    rotations = [r for r in rows if r["policy_class"] == "service_role_rotation"]
    assert len(rotations) >= 1
    assert any(r["cadence"] == "quarterly" for r in rotations)


def test_seed_includes_brand_jargon_redaction(rows: list[dict]) -> None:
    """The BRAND_JARGON_AUDIT redaction rule is a redaction-class row."""
    reds = [r for r in rows if r["policy_class"] == "redaction"]
    assert len(reds) >= 1
    assert any("BRAND_JARGON_AUDIT" in r["policy_text"] for r in reds)


def test_validator_script_exits_zero() -> None:
    r = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=30,
    )
    assert r.returncode == 0, (
        f"validate_policy_register.py exited {r.returncode}; stdout: {r.stdout}"
    )
    assert "PASS" in r.stdout


def test_validator_runs_under_dispatcher() -> None:
    r = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "validate_hlk.py")],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=120,
    )
    assert r.returncode == 0
    assert "POLICY_REGISTER: PASS" in r.stdout
