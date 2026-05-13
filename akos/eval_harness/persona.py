"""Per-persona aggregator + filtering helpers (Initiative 47 P10).

Bridges PERSONA_SCENARIO_REGISTRY.csv (the I47 P1 SSOT) to the unified
``Scorecard`` shape from ``akos.eval_harness.v2``. Used by:
- ``scripts/eval.py --mode persona`` (P10)
- ``scripts/eval.py --calibrate`` (P10 difficulty meta-eval)
- ``scripts/calibrate_scenarios.py`` (P10 batch calibration)
- ``scripts/eval.py --persona <id>`` filter flag (P10)
- Tier B GitHub Action persona matrix dim (P14)

Public API:
- ``load_persona_scenarios(path) -> list[dict]``
- ``filter_scenarios(scenarios, *, persona_id=None, difficulty_class=None,
  scenario_class=None, skill_id=None, tier=None) -> list[dict]``
- ``aggregate_by_persona(rows: list[ScoreRow]) -> dict[str, dict[str, int]]``
- ``calibration_distribution(rows: list[ScoreRow]) -> dict[str, dict[str, int]]``
"""

from __future__ import annotations

import csv
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_REGISTRY = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions"
    / "PERSONA_SCENARIO_REGISTRY.csv"
)

# Calibration target distribution per D-IH-47-C. Values are percentage points.
CALIBRATION_TARGET = {
    "trivial": 10.0,
    "moderate": 40.0,
    "hard": 40.0,
    "impossible": 10.0,
}
CALIBRATION_TOLERANCE_PP = 5.0  # +/- 5 percentage points per D-IH-47-C


def load_persona_scenarios(path: Path | None = None) -> list[dict[str, str]]:
    """Load all rows from PERSONA_SCENARIO_REGISTRY.csv as dicts."""
    csv_path = path or DEFAULT_REGISTRY
    if not csv_path.is_file():
        return []
    with csv_path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def filter_scenarios(
    scenarios: list[dict[str, str]],
    *,
    persona_id: str | None = None,
    difficulty_class: str | None = None,
    scenario_class: str | None = None,
    skill_id: str | None = None,
    tier: str | None = None,
    lifecycle: str = "active",
) -> list[dict[str, str]]:
    """Filter scenarios by any of the 5 typed dimensions + lifecycle.

    Defaults to ``lifecycle='active'`` so deprecated rows are excluded
    unless the caller passes ``lifecycle=''``.
    """
    out = scenarios
    if lifecycle:
        out = [r for r in out if (r.get("lifecycle_status") or "active") == lifecycle]
    if persona_id is not None:
        out = [r for r in out if r.get("persona_id") == persona_id]
    if difficulty_class is not None:
        out = [r for r in out if r.get("difficulty_class") == difficulty_class]
    if scenario_class is not None:
        out = [r for r in out if r.get("scenario_class") == scenario_class]
    if skill_id is not None:
        out = [r for r in out if r.get("skill_id") == skill_id]
    if tier is not None:
        out = [r for r in out if r.get("tier") == tier]
    return list(out)


def aggregate_by_persona(rows: list[Any]) -> dict[str, dict[str, int]]:
    """Aggregate ``ScoreRow`` instances by persona_id.

    Returns ``{persona_id: {status_count_dict, difficulty_count_dict, total}}``.
    Rows without ``persona_id`` are aggregated under key ``'__no_persona__'``.
    """
    by: dict[str, list[Any]] = {}
    for r in rows:
        pid = getattr(r, "persona_id", None) or "__no_persona__"
        by.setdefault(pid, []).append(r)
    out: dict[str, dict[str, int]] = {}
    for pid, group in by.items():
        statuses = Counter(getattr(r, "status", "?") for r in group)
        diffs = Counter(getattr(r, "difficulty_class", None) or "?" for r in group)
        out[pid] = {
            "total": len(group),
            "PASS": statuses.get("PASS", 0),
            "FAIL": statuses.get("FAIL", 0),
            "SKIP": statuses.get("SKIP", 0),
            "trivial": diffs.get("trivial", 0),
            "moderate": diffs.get("moderate", 0),
            "hard": diffs.get("hard", 0),
            "impossible": diffs.get("impossible", 0),
        }
    return out


@dataclass
class CalibrationResult:
    """One persona's measured-vs-target difficulty distribution.

    I51 P3 D-IH-51-A: ``target`` is the per-persona ``target_difficulty_band``
    when set on that persona's CSV rows; otherwise the global D-IH-47-C
    default. ``target_source`` is ``persona`` or ``global``.
    """

    persona_id: str
    total: int
    counts: dict[str, int]            # raw counts per difficulty class
    pct: dict[str, float]             # percentages per difficulty class
    deltas_pp: dict[str, float]       # measured - target (signed)
    within_tolerance: dict[str, bool] # per-class within ±tolerance_pp
    overall_pass: bool                # all classes within tolerance
    target: dict[str, float] = None   # type: ignore[assignment]  # I51 P3
    target_source: str = "global"      # I51 P3 — "persona" or "global"


def _resolve_persona_target(
    rows: list[dict[str, str]],
    *,
    global_target: dict[str, float],
) -> tuple[dict[str, float], str]:
    """I51 P3 D-IH-51-A: resolve a persona's calibration target.

    Returns (target, source). Source is "persona" if any row of this persona
    carries a non-empty ``target_difficulty_band`` AND all rows agree;
    otherwise "global" (fall through to the D-IH-47-C default). Inconsistent
    rows trigger a fall-through to global — the validator script is the
    canonical enforcement point; this function is intentionally tolerant.
    """
    # Local import to avoid touching the module-level imports surface.
    from akos.hlk_persona_scenario_csv import parse_target_difficulty_band  # noqa: PLC0415

    seen: set[str] = set()
    for r in rows:
        seen.add((r.get("target_difficulty_band") or "").strip())
    seen.discard("")
    if len(seen) == 1:
        try:
            parsed = parse_target_difficulty_band(next(iter(seen)))
            if parsed is not None:
                return parsed, "persona"
        except ValueError:
            pass
    return global_target, "global"


def calibration_distribution(
    scenarios: list[dict[str, str]] | None = None,
    *,
    target: dict[str, float] | None = None,
    tolerance_pp: float = CALIBRATION_TOLERANCE_PP,
) -> dict[str, CalibrationResult]:
    """Compute per-persona calibration vs the D-IH-47-C target distribution.

    Returns ``{persona_id: CalibrationResult}`` plus an aggregate ``__overall__`` key.

    I51 P3 D-IH-51-A: when a persona carries a non-empty
    ``target_difficulty_band`` on its rows, that band is used in place of the
    global D-IH-47-C default. ``__overall__`` always uses the global default
    (the global aggregate continues to gate registry health independently of
    any per-persona overrides).
    """
    global_target = dict(target or CALIBRATION_TARGET)
    by_persona: dict[str, list[dict[str, str]]] = {}
    if scenarios is None:
        scenarios = load_persona_scenarios()
    for r in scenarios:
        if (r.get("lifecycle_status") or "active") != "active":
            continue
        pid = r.get("persona_id") or "__no_persona__"
        by_persona.setdefault(pid, []).append(r)
    # Add aggregate slot.
    by_persona["__overall__"] = list(scenarios)

    out: dict[str, CalibrationResult] = {}
    for pid, group in by_persona.items():
        if pid == "__overall__":
            group = [r for r in group if (r.get("lifecycle_status") or "active") == "active"]
            persona_target = global_target
            target_source = "global"
        else:
            persona_target, target_source = _resolve_persona_target(
                group, global_target=global_target,
            )
        total = len(group)
        if total == 0:
            continue
        counts = Counter(r.get("difficulty_class", "") for r in group)
        pct = {k: 100.0 * counts.get(k, 0) / total for k in persona_target}
        deltas = {k: pct[k] - persona_target[k] for k in persona_target}
        within = {k: abs(deltas[k]) <= tolerance_pp for k in persona_target}
        out[pid] = CalibrationResult(
            persona_id=pid,
            total=total,
            counts={k: counts.get(k, 0) for k in persona_target},
            pct=pct,
            deltas_pp=deltas,
            within_tolerance=within,
            overall_pass=all(within.values()),
            target=persona_target,
            target_source=target_source,
        )
    return out


def render_calibration_markdown(results: dict[str, CalibrationResult]) -> str:
    """Render a calibration summary in markdown for phase reports.

    I51 P3 D-IH-51-A: surfaces the per-persona target band and source, so
    readers can audit which personas use ``target_difficulty_band`` vs the
    D-IH-47-C global default.
    """
    lines = [
        "# Calibration distribution (I47 P10; D-IH-47-C target 40/40/10/10)",
        "",
        f"Tolerance: +/- {CALIBRATION_TOLERANCE_PP} percentage points per class",
        "Per-persona override: I51 P3 D-IH-51-A `target_difficulty_band` column",
        "",
        "| persona_id | total | t/m/h/i target | source | trivial% | moderate% | hard% | impossible% | within tol? |",
        "|:-----------|:-----:|:--------------:|:------:|:--------:|:---------:|:-----:|:-----------:|:-----------:|",
    ]
    # Sort: __overall__ first, then alphabetical.
    pids = sorted(results.keys(), key=lambda p: (p != "__overall__", p))
    for pid in pids:
        r = results[pid]
        flag = "YES" if r.overall_pass else "NO"
        tgt = r.target or CALIBRATION_TARGET
        target_str = (
            f"{int(tgt.get('trivial', 0))}/{int(tgt.get('moderate', 0))}/"
            f"{int(tgt.get('hard', 0))}/{int(tgt.get('impossible', 0))}"
        )
        lines.append(
            f"| {pid} | {r.total} | {target_str} | {r.target_source} | "
            f"{r.pct['trivial']:.1f} | "
            f"{r.pct['moderate']:.1f} | {r.pct['hard']:.1f} | "
            f"{r.pct['impossible']:.1f} | **{flag}** |"
        )
    return "\n".join(lines) + "\n"
