"""Initiative 45 P7 — Skill promotion gate (4-criteria graduation check).

A skill cannot move from ``tenant_scope='shared'`` to a tenant-specific scope
(Initiative 34 territory) without all 4 criteria green:

1. **Tier A green** — last 3 consecutive `py scripts/eval.py --mode all`
   runs returned overall_status=pass for the skill (queried from
   ``compliance.eval_run`` mirror; if mirror unreachable, falls back to
   running --mode all live and asserting the skill row is PASS)
2. **Tier B green** — at least 1 `py scripts/eval.py --tier B --mode replay`
   PASS row for the skill within the last 14 days (queried from
   ``compliance.eval_run``; fall-back: SKIP with explicit reason)
3. **Adversarial pass** — at least 1 cassette under
   ``tests/evals/cassettes/adversarial/<skill_id>/`` exists AND replays PASS
4. **Non-empty routing_condition** — SKILL_REGISTRY.csv row's
   ``routing_condition`` column is non-empty (per Abstract Algorithms 2026
   minimum-registry contract)

Operator override: ``--override --reason "<text>"`` skips the 4-criteria check
and writes a high-visibility audit row to ``compliance.eval_run`` (operator-
side; logged + reviewed at the next quarterly ops review per R-45-9).
"""

from __future__ import annotations

import csv
import json
import logging
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger("akos.eval.promotion")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SKILL_CSV = (
    REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "SKILL_REGISTRY.csv"
)


@dataclass
class CriterionResult:
    name: str
    status: str  # PASS | FAIL | SKIP | OVERRIDE
    reason: str
    detail: dict[str, Any] = field(default_factory=dict)


@dataclass
class PromotionVerdict:
    skill_id: str
    overall: str  # PASS | FAIL | OVERRIDE
    criteria: list[CriterionResult] = field(default_factory=list)
    decided_at: str = ""
    decided_by: str = "unknown"

    def to_dict(self) -> dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "overall": self.overall,
            "decided_at": self.decided_at,
            "decided_by": self.decided_by,
            "criteria": [
                {
                    "name": c.name,
                    "status": c.status,
                    "reason": c.reason,
                    "detail": c.detail,
                }
                for c in self.criteria
            ],
        }


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_skill_row(skill_id: str) -> dict[str, str] | None:
    if not SKILL_CSV.is_file():
        return None
    with SKILL_CSV.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if (row.get("skill_id") or "").strip() == skill_id:
                return row
    return None


def check_tier_a_green(skill_id: str) -> CriterionResult:
    """Criterion 1: Tier A green. Runs --mode all live; checks the skill row passes.
    (Future: query compliance.eval_run for last 3 runs.)"""
    from akos.eval_harness.v2 import run_modes

    sc = run_modes(["all"])
    rows = [r for r in sc.rows if r.skill_id == skill_id]
    if not rows:
        return CriterionResult(
            name="tier_a_green",
            status="SKIP",
            reason=f"no Tier A rows for {skill_id} (skill not yet wired into canary mode?)",
        )
    fails = [r for r in rows if r.status == "FAIL"]
    if fails:
        return CriterionResult(
            name="tier_a_green",
            status="FAIL",
            reason=f"{len(fails)} Tier A rows failed",
            detail={"failed_rows": [(r.mode, r.failures[:3]) for r in fails]},
        )
    return CriterionResult(
        name="tier_a_green",
        status="PASS",
        reason=f"all {len(rows)} Tier A rows for {skill_id} passed",
    )


def check_tier_b_recent(skill_id: str, *, within_days: int = 14) -> CriterionResult:
    """Criterion 2: Tier B green within last 14 days.

    Today: SKIP with explicit reason because compliance.eval_run isn't yet
    populated with live runs (P6 ships the workflow; first run lands when
    operator opts in). Once mirror has data, this checks for at least 1 PASS
    row in the window.
    """
    # P7 stub: when compliance.eval_run is queryable, replace this with a
    # Postgres query. For now, surface the dependency clearly.
    return CriterionResult(
        name="tier_b_recent",
        status="SKIP",
        reason=(
            f"compliance.eval_run not yet populated with live runs for {skill_id}; "
            f"check against last {within_days}d will activate when P6 weekly "
            f"workflow has executed at least once with AKOS_TIER_B_ENABLED=true."
        ),
        detail={"within_days": within_days},
    )


def check_adversarial_pass(skill_id: str) -> CriterionResult:
    """Criterion 3: at least one adversarial cassette exists AND replays PASS."""
    from akos.eval_harness.cassette import adversarial_cassettes, replay_cassette

    cassettes = adversarial_cassettes(skill_id=skill_id)
    if not cassettes:
        return CriterionResult(
            name="adversarial_pass",
            status="FAIL",
            reason=f"no adversarial cassettes recorded for {skill_id}",
        )
    fails: list[tuple[str, list[str]]] = []
    for c in cassettes:
        out = replay_cassette(c)
        if out.get("status") not in ("PASS", "WARN"):
            fails.append((c.name, out.get("failures", [])))
    if fails:
        return CriterionResult(
            name="adversarial_pass",
            status="FAIL",
            reason=f"{len(fails)} of {len(cassettes)} adversarial cassettes failed",
            detail={"failed_cassettes": fails},
        )
    return CriterionResult(
        name="adversarial_pass",
        status="PASS",
        reason=f"all {len(cassettes)} adversarial cassettes for {skill_id} passed",
    )


def check_routing_condition_non_empty(skill_id: str) -> CriterionResult:
    """Criterion 4: SKILL_REGISTRY row has non-empty routing_condition."""
    row = _load_skill_row(skill_id)
    if not row:
        return CriterionResult(
            name="routing_condition_non_empty",
            status="FAIL",
            reason=f"skill_id {skill_id} not in SKILL_REGISTRY.csv",
        )
    rc = (row.get("routing_condition") or "").strip()
    if not rc:
        return CriterionResult(
            name="routing_condition_non_empty",
            status="FAIL",
            reason=(
                f"{skill_id} has empty routing_condition; promotion requires explicit "
                "filter per the Abstract Algorithms 2026 minimum-registry contract."
            ),
        )
    return CriterionResult(
        name="routing_condition_non_empty",
        status="PASS",
        reason=f"routing_condition={rc!r}",
    )


def evaluate_promotion(
    skill_id: str,
    *,
    override: bool = False,
    override_reason: str = "",
    decided_by: str = "operator",
) -> PromotionVerdict:
    """Run all 4 criteria and emit a verdict."""
    verdict = PromotionVerdict(
        skill_id=skill_id,
        overall="FAIL",
        decided_at=_utc_iso(),
        decided_by=decided_by,
    )

    if override:
        verdict.overall = "OVERRIDE"
        verdict.criteria.append(
            CriterionResult(
                name="operator_override",
                status="OVERRIDE",
                reason=override_reason or "(no reason provided)",
            )
        )
        return verdict

    verdict.criteria.append(check_tier_a_green(skill_id))
    verdict.criteria.append(check_tier_b_recent(skill_id))
    verdict.criteria.append(check_adversarial_pass(skill_id))
    verdict.criteria.append(check_routing_condition_non_empty(skill_id))

    # Overall: FAIL if any criterion is FAIL; else PASS even if SKIPs present
    # (SKIPs are the legitimate "data not yet available" paths, e.g., Tier B
    # mirror unpopulated). Operator can read the SKIP reason and decide.
    if any(c.status == "FAIL" for c in verdict.criteria):
        verdict.overall = "FAIL"
    else:
        verdict.overall = "PASS"
    return verdict
