"""Tests for the Intent-Ranked Regression model + runbook (I88 / D-IH-88-F candidate)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from akos.hlk_intent_ranked_regression import (
    ICS_MAX,
    INTENT_TIERS,
    INTENT_TIERS_BY_ID,
    REGRESSION_SURFACES,
    rank_surfaces,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_seven_intent_tiers_unique() -> None:
    assert len(INTENT_TIERS) == 7
    assert len({t.tier_id for t in INTENT_TIERS}) == 7


def test_every_surface_serves_known_tiers() -> None:
    for s in REGRESSION_SURFACES:
        assert s.served_tiers, f"{s.surface_id} serves no tier"
        for t in s.served_tiers:
            assert t in INTENT_TIERS_BY_ID, f"{s.surface_id} -> unknown {t}"


def test_ics_within_bounds() -> None:
    for s in REGRESSION_SURFACES:
        ics = s.ics(INTENT_TIERS_BY_ID)
        assert 0 < ics <= ICS_MAX


def test_severity_first_leads_sweep_order() -> None:
    ranked = rank_surfaces()
    sev = [i for i, (s, _) in enumerate(ranked) if s.severity_first]
    non_sev = [i for i, (s, _) in enumerate(ranked) if not s.severity_first]
    if sev and non_sev:
        assert max(sev) < min(non_sev), "severity-first surfaces must lead"


def test_ranking_is_deterministic() -> None:
    a = [s.surface_id for s, _ in rank_surfaces()]
    b = [s.surface_id for s, _ in rank_surfaces()]
    assert a == b


def test_finops_substrate_is_severity_first() -> None:
    # S-04 (commercial + fiscal substrate) must be severity-first and rank highly.
    ranked = rank_surfaces()
    top3 = {s.surface_id for s, _ in ranked[:3]}
    assert "S-04" in top3


def test_runbook_self_test_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/intent_ranked_regression.py", "--self-test"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_runbook_rank_emits_table() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/intent_ranked_regression.py", "--rank"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "ICS" in result.stdout and "S-04" in result.stdout
