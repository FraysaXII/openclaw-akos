"""Initiative 49 — deterministic priority score for PERSONA_SCENARIO_REGISTRY rows.

Formula (plan): ``priority_score = (Reach × Impact) / Effort``

- **Reach**: persona tier-weight × scenario-class-weight
  (tier ``1→3``, ``2→2``, ``3→1``; class weights encoded below).
- **Impact**: PASS=2, GROUND=3, ESCALATE=3, REFUSE=2 (expected_outcome_class).
- **Effort**: derived from difficulty_class (surrogate when max_tool_calls not in CSV).

Rows with ``safety_lane=true`` pin to backlog top downstream (sort helper); they
still carry a numeric score for tie-break diagnostics.
"""

from __future__ import annotations

import csv
import shutil
from pathlib import Path

IMPACT_WEIGHT: dict[str, float] = {
    "PASS": 2.0,
    "GROUND": 3.0,
    "ESCALATE": 3.0,
    "REFUSE": 2.0,
}

DIFFICULTY_EFFORT: dict[str, float] = {
    "trivial": 2.0,
    "moderate": 3.0,
    "hard": 5.0,
    "impossible": 6.0,
}

TIER_WEIGHT: dict[str, float] = {"1": 3.0, "2": 2.0, "3": 1.0}

# Scenario-class Reach multipliers per Initiative 49 plan wording.
CLASS_REACH_WEIGHT: dict[str, float] = {
    "lookup": 3.0,
    "multihop": 3.0,
    "cross_axis": 2.0,
    "benchmark": 1.0,
    "adversarial": 2.0,
    "recovery": 2.0,
    "cannot_answer": 2.0,
}


def tier_reach_multiplier(tier: str) -> float:
    t = (tier or "").strip()
    return TIER_WEIGHT.get(t, 1.0)


def scenario_class_reach_multiplier(scenario_class: str) -> float:
    c = (scenario_class or "").strip()
    return CLASS_REACH_WEIGHT.get(c, 2.0)


def compute_persona_scenario_priority_score(row: dict[str, str]) -> float:
    """Emit a deterministic float priority for one registry row dictionary."""
    reach = tier_reach_multiplier(row.get("tier", "") or "") * scenario_class_reach_multiplier(
        row.get("scenario_class") or ""
    )
    oc = (row.get("expected_outcome_class") or "").strip().upper()
    impact = IMPACT_WEIGHT.get(oc, 2.0)
    diff = (row.get("difficulty_class") or "").strip().lower()
    effort = DIFFICULTY_EFFORT.get(diff, 3.5)
    if effort <= 0:
        effort = 1.0
    return float((reach * impact) / effort)


def format_priority(score: float) -> str:
    """Stable string for CSV (fixed precision)."""
    return f"{score:.6f}"


def rewrite_persona_registry_priority_scores(
    csv_path: str | Path,
    *,
    dry_run: bool = False,
) -> tuple[int, int]:
    """Recompute ``priority_score`` for every row; leave other columns unchanged.

    Returns ``(row_count, rows_changed_or_would_change)``. Uses rename-on-write for atomicity.
    """
    from akos.hlk_persona_scenario_csv import PERSONA_SCENARIO_REGISTRY_FIELDNAMES

    p = Path(csv_path)
    if not p.is_file():
        raise FileNotFoundError(str(csv_path))

    with p.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames = list(reader.fieldnames or [])
        if fieldnames != list(PERSONA_SCENARIO_REGISTRY_FIELDNAMES):
            raise ValueError("CSV header mismatch; run migrate_persona_registry_i49_columns.py")
        rows = list(reader)

    changed = 0
    for r in rows:
        new_s = format_priority(compute_persona_scenario_priority_score(r))
        old = (r.get("priority_score") or "").strip()
        r["priority_score"] = new_s
        if old != new_s:
            changed += 1

    if dry_run:
        return len(rows), changed

    tmp = p.with_suffix(p.suffix + ".tmp")
    try:
        with tmp.open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(PERSONA_SCENARIO_REGISTRY_FIELDNAMES), extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
        shutil.move(str(tmp), str(p))
    finally:
        if tmp.exists():
            tmp.unlink(missing_ok=True)

    return len(rows), changed
