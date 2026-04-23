"""config/verification-profiles.json + akos/verification_profiles.py SSOT tests."""

from __future__ import annotations

from akos import verification_profiles as vp
from akos.io import REPO_ROOT


def test_governance_rubric_suites_order_and_ids() -> None:
    out = vp.governance_rubric_suites()
    assert out == [
        "pathc-research-spine",
        "madeira-operator-coverage",
    ]


def test_list_profile_ids() -> None:
    ids = vp.list_profile_ids()
    assert "pre_commit" in ids
    assert "compliance_mirror_emit" in ids
    assert "optional_executor_harness" in ids


def test_compliance_mirror_emit_resolves() -> None:
    steps = list(vp.iter_profile_steps("compliance_mirror_emit"))
    assert [s.step_id for s in steps] == [
        "compliance_mirror_count_only",
        "compliance_mirror_write_sql",
    ]
    for s in steps:
        cmd = vp.resolve_argv(s.argv, repo_root=REPO_ROOT)
        assert "sync_compliance_mirrors_from_csv.py" in cmd[1].replace("\\", "/")


def test_iter_pre_commit_resolves() -> None:
    steps = list(vp.iter_profile_steps("pre_commit"))
    assert {s.step_id for s in steps} >= {
        "strict_inventory",
        "drift",
        "test_all",
        "browser_smoke",
        "api_madeira_smoke",
        "release_gate",
    }
    for s in steps:
        cmd = vp.resolve_argv(s.argv, repo_root=REPO_ROOT)
        assert cmd[0]
        assert "pytest" in cmd or "scripts" in cmd[1].replace("\\", "/")


def test_registry_path_exists() -> None:
    p = vp.registry_path()
    assert p.is_file(), p
