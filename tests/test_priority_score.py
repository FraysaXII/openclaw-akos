"""Initiative 49 — PERSONA_SCENARIO_REGISTRY priority_score determinism."""

from __future__ import annotations

import csv
import shutil
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_persona_scenario_csv import PERSONA_SCENARIO_REGISTRY_FIELDNAMES
from akos.hlk_persona_scenario_priority import (
    compute_persona_scenario_priority_score,
    format_priority,
    rewrite_persona_registry_priority_scores,
)


def _minimal_row(**overrides: str) -> dict[str, str]:
    base = {fn: "" for fn in PERSONA_SCENARIO_REGISTRY_FIELDNAMES}
    base.update(
        {
            "scenario_id": "SCN-ZZ-TEST-V1",
            "persona_id": "OPERATOR",
            "skill_id": "SKILL-MADEIRA-LOOKUP-V1",
            "tier": "1",
            "scenario_class": "lookup",
            "difficulty_class": "moderate",
            "expected_outcome_class": "GROUND",
        },
    )
    base.update(overrides)
    return base


def test_compute_priority_formula_reach_impact_effort() -> None:
    r = _minimal_row(
        tier="1",
        scenario_class="lookup",
        expected_outcome_class="GROUND",
        difficulty_class="moderate",
    )
    assert compute_persona_scenario_priority_score(r) == pytest.approx(9.0)


def test_format_priority_stable_string() -> None:
    assert format_priority(13.5) == "13.500000"


def test_rewrite_is_idempotent_on_copy(tmp_path: Path) -> None:
    shutil.copy(REPO_ROOT / "docs/references/hlk/compliance/dimensions/PERSONA_SCENARIO_REGISTRY.csv", tmp_path / "P.csv")
    csv_p = tmp_path / "P.csv"
    n, _ = rewrite_persona_registry_priority_scores(csv_p)
    n2, delta2 = rewrite_persona_registry_priority_scores(csv_p)

    assert n >= 300
    assert n == n2
    assert delta2 == 0

    with csv_p.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    for r in rows:
        ps = (r.get("priority_score") or "").strip()
        assert ps
        float(ps.replace(",", "."))
