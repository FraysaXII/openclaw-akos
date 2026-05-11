"""Drift safeguard: the SOP body and the Python constants must agree.

Specifically:
* Every method id listed in `SOP-ENG_ESTIMATION_DISCIPLINE_001.md` §3 table
  has a matching key in `akos.engagement_estimation.METHODS`.
* Every method id in `METHODS` has a row in §3 table.
* The min/par/max effort triangle in §3 matches the `EstimationMethod.effort_hours` triangle.
* Every multiplier id in §5 has a matching `MULTIPLIERS[mid].factor` in Python (and vice-versa).

Failure means the SOP body and the runtime constants have drifted; one of
them is wrong. The fix is to update the side that should follow.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.engagement_estimation import METHODS, MULTIPLIERS

SOP = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "Operations"
    / "Engagement"
    / "SOP-ENG_ESTIMATION_DISCIPLINE_001.md"
)

METHOD_ROW_RE = re.compile(
    r"^\|\s*`(?P<mid>[a-z_]+)`\s*\|[^|]+\|\s*(?P<lo>\d+)\s*/\s*(?P<par>\d+)\s*/\s*(?P<hi>\d+)\s*\|",
    re.MULTILINE,
)
MULTIPLIER_ROW_RE = re.compile(
    r"^\|\s*`(?P<mid>[a-z_]+)`\s*\|[^|]+\|\s*(?P<factor>\d+\.\d+)\s*\|",
    re.MULTILINE,
)


def _sop_text() -> str:
    if not SOP.exists():
        pytest.skip(f"SOP not found: {SOP}")
    return SOP.read_text(encoding="utf-8")


def test_sop_method_ids_match_python_methods() -> None:
    text = _sop_text()
    sop_ids = {m.group("mid") for m in METHOD_ROW_RE.finditer(text)}
    py_ids = set(METHODS.keys())
    assert sop_ids == py_ids, (
        f"SOP §3 method ids {sorted(sop_ids)} != METHODS keys {sorted(py_ids)}"
    )


def test_sop_method_effort_triples_match_python() -> None:
    text = _sop_text()
    for m in METHOD_ROW_RE.finditer(text):
        mid = m.group("mid")
        lo, par, hi = int(m.group("lo")), int(m.group("par")), int(m.group("hi"))
        method = METHODS[mid]
        eh = method.effort_hours
        assert (eh.min, eh.par, eh.max) == (lo, par, hi), (
            f"method {mid}: SOP says ({lo}, {par}, {hi}); "
            f"Python says ({eh.min}, {eh.par}, {eh.max})"
        )


def test_sop_multiplier_ids_match_python() -> None:
    text = _sop_text()
    sop_section = text.split("## 5. Multipliers", 1)[-1].split("## 6.", 1)[0]
    sop_ids = {m.group("mid") for m in MULTIPLIER_ROW_RE.finditer(sop_section)}
    py_ids = set(MULTIPLIERS.keys())
    assert sop_ids == py_ids, (
        f"SOP §5 multiplier ids {sorted(sop_ids)} != MULTIPLIERS keys {sorted(py_ids)}"
    )


def test_sop_multiplier_factors_match_python() -> None:
    text = _sop_text()
    sop_section = text.split("## 5. Multipliers", 1)[-1].split("## 6.", 1)[0]
    for m in MULTIPLIER_ROW_RE.finditer(sop_section):
        mid = m.group("mid")
        factor = float(m.group("factor"))
        py_factor = MULTIPLIERS[mid].factor
        assert abs(factor - py_factor) < 1e-9, (
            f"multiplier {mid}: SOP says {factor}; Python says {py_factor}"
        )
