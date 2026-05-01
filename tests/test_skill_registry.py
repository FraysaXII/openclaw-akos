"""Tests for SKILL_REGISTRY.csv (Initiative 32 P2).

Locks the 7th-canonical-dimension contract:
- Header matches SKILL_REGISTRY_FIELDNAMES.
- 5 seed rows shipped (per the I32 plan acceptance criterion).
- Every row's skill_id matches ^SKILL-[A-Z0-9-]{4,80}-V\\d+$ and is unique.
- Every agents_supported entry resolves to KNOWN_AGENT_IDS or the 'shared' pseudo-agent.
- Every axes_consumed entry is in VALID_AXES.
- Every tenant_scope is exactly 'shared' (D-IH-32-J).
- Every owner_role resolves to baseline_organisation.csv.
- Validator passes against the shipped CSV and against the dispatcher.
- topic_skill_registry row exists in TOPIC_REGISTRY.csv.
"""

from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "SKILL_REGISTRY.csv"
TOPIC_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "TOPIC_REGISTRY.csv"
ORG_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "baseline_organisation.csv"
VALIDATOR = REPO_ROOT / "scripts" / "validate_skill_registry.py"


@pytest.fixture(scope="module")
def rows() -> list[dict]:
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def test_csv_exists() -> None:
    assert CSV_PATH.is_file(), f"missing {CSV_PATH}"


def test_header_matches_contract(rows: list[dict]) -> None:
    sys.path.insert(0, str(REPO_ROOT))
    from akos.hlk_skill_registry_csv import SKILL_REGISTRY_FIELDNAMES

    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        assert reader.fieldnames == list(SKILL_REGISTRY_FIELDNAMES), (
            f"header mismatch:\n  expected: {list(SKILL_REGISTRY_FIELDNAMES)}\n  got:      {reader.fieldnames}"
        )


def test_seed_count_at_least_five(rows: list[dict]) -> None:
    """I32 P2 acceptance: at least 5 seed rows."""
    assert len(rows) >= 5, f"expected at least 5 seed rows, got {len(rows)}"


def test_skill_id_format_and_uniqueness(rows: list[dict]) -> None:
    pattern = re.compile(r"^SKILL-[A-Z0-9-]{4,80}-V\d+$")
    seen: set[str] = set()
    for r in rows:
        sid = r["skill_id"]
        assert pattern.match(sid), f"skill_id {sid!r} does not match {pattern.pattern}"
        assert sid not in seen, f"duplicate skill_id {sid!r}"
        seen.add(sid)


def test_seed_rows_cover_each_documented_agent(rows: list[dict]) -> None:
    """The plan calls for 1 row per existing agent + 1 shared utility skill."""
    agents_seen: set[str] = set()
    for r in rows:
        for agent in (r["agents_supported"] or "").split(";"):
            agents_seen.add(agent.strip())
    expected = {"madeira", "architect", "executor", "verifier", "shared"}
    missing = expected - agents_seen
    assert not missing, f"plan called for skills covering agents {expected}; missing {missing}"


def test_agents_supported_in_known_set(rows: list[dict]) -> None:
    sys.path.insert(0, str(REPO_ROOT))
    from akos.hlk_skill_registry_csv import KNOWN_AGENT_IDS, SHARED_AGENT_ID

    valid = KNOWN_AGENT_IDS | {SHARED_AGENT_ID}
    for r in rows:
        for agent in (r["agents_supported"] or "").split(";"):
            agent = agent.strip()
            if not agent:
                continue
            assert agent in valid, f"{r['skill_id']}: agent {agent!r} not in {sorted(valid)}"


def test_axes_consumed_in_valid_set(rows: list[dict]) -> None:
    sys.path.insert(0, str(REPO_ROOT))
    from akos.hlk_skill_registry_csv import VALID_AXES

    for r in rows:
        for ax in (r["axes_consumed"] or "").split(";"):
            ax = ax.strip()
            if not ax:
                continue
            assert ax in VALID_AXES, f"{r['skill_id']}: axis {ax!r} not in {sorted(VALID_AXES)}"


def test_tenant_scope_only_shared_d_ih_32_j(rows: list[dict]) -> None:
    """D-IH-32-J: tenant_scope must be exactly 'shared' until I34."""
    for r in rows:
        assert r["tenant_scope"] == "shared", (
            f"{r['skill_id']}: tenant_scope {r['tenant_scope']!r} must be 'shared' (D-IH-32-J)"
        )


def test_eval_baseline_pct_parses_in_range(rows: list[dict]) -> None:
    for r in rows:
        ebp = float(r["eval_baseline_pct"])
        assert 0.0 <= ebp <= 100.0, f"{r['skill_id']}: eval_baseline_pct {ebp} out of [0, 100]"


def test_owner_role_resolves_to_baseline_org(rows: list[dict]) -> None:
    with ORG_PATH.open(encoding="utf-8", newline="") as fh:
        org_roles = {r["role_name"].strip() for r in csv.DictReader(fh)}
    for r in rows:
        assert r["owner_role"] in org_roles, (
            f"{r['skill_id']}: owner_role {r['owner_role']!r} not in baseline_organisation.csv"
        )


def test_topic_ids_resolve_to_topic_registry(rows: list[dict]) -> None:
    with TOPIC_PATH.open(encoding="utf-8", newline="") as fh:
        topic_ids = {r["topic_id"].strip() for r in csv.DictReader(fh)}
    for r in rows:
        for tid in (r["topic_ids"] or "").split(";"):
            tid = tid.strip()
            if not tid:
                continue
            assert tid in topic_ids, f"{r['skill_id']}: topic_id {tid!r} not in TOPIC_REGISTRY.csv"


def test_topic_skill_registry_row_exists() -> None:
    """P2-A5: topic_skill_registry row added to TOPIC_REGISTRY.csv."""
    with TOPIC_PATH.open(encoding="utf-8", newline="") as fh:
        topic_ids = {r["topic_id"].strip() for r in csv.DictReader(fh)}
    assert "topic_skill_registry" in topic_ids, (
        "topic_skill_registry row not found in TOPIC_REGISTRY.csv (P2-A5)"
    )


def test_validator_script_exits_zero() -> None:
    """The validator runs cleanly against the shipped CSV."""
    r = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=30,
    )
    assert r.returncode == 0, f"validate_skill_registry.py exited {r.returncode}; stdout: {r.stdout}; stderr: {r.stderr}"
    assert "PASS" in r.stdout


def test_validator_runs_under_dispatcher() -> None:
    """The validator is wired into validate_hlk.py dispatcher."""
    r = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "validate_hlk.py")],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=120,
    )
    assert r.returncode == 0, f"validate_hlk.py exited {r.returncode}"
    assert "SKILL_REGISTRY: PASS" in r.stdout, "SKILL_REGISTRY not dispatched by validate_hlk.py"
