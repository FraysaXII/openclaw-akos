"""LLM-as-judge 3-axis scoring (Initiative 47 P12; D-IH-47-J).

Per RICE B + D-IH-47-J: scores agent responses on 3 axes, each 1-5:
- ``brand_voice``  - adherence to BRAND_VOICE_FOUNDATION + BRAND_JARGON_AUDIT
- ``citation``     - every claim cites a canonical path (docs/references/hlk/...)
- ``persona_fit``  - response register matches persona's typical_languages +
  typical_distance_band per PERSONA_REGISTRY

Pass threshold per axis is sourced from POLICY_REGISTER rows of class
``judge_threshold`` (default 4/5).

## Cost discipline (R-47-11)

- ``--judge-cost-cap`` CLI flag (default $0.01/scenario)
- Per-scenario cost is tracked in ``JudgeResult.cost_usd``
- Aggregate cap enforced by ``aggregate_judge_cost_under_cap()``
- Skipping a scenario when over cap returns ``JudgeResult(skipped=True, ...)``

## Drift discipline (R-47-10)

- Judge model id is captured in JudgeResult.model_id
- Operator pins judge model via ``AKOS_JUDGE_MODEL`` env var (default 'offline')
- Re-baselining is logged via decision-log entries (operator policy)

## Live vs offline mode

This module ships with TWO score paths:
- ``score_response_offline(response, scenario)`` — deterministic; runs in CI;
  uses substring + heuristic checks; cost = 0
- ``score_response_live(response, scenario, persona, model_id)`` — placeholder;
  raises NotImplementedError until operator pins the live API contract
  (Anthropic Messages API / OpenAI Chat Completions / etc.) and approves
  the first live cost burn

Tier B GitHub Action workflow_dispatch can opt-in to live mode via
``AKOS_RECORD_LIVE=1 AKOS_JUDGE_MODEL=<model_id>`` env vars.
"""

from __future__ import annotations

import csv
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
POLICY_CSV = (
    REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "POLICY_REGISTER.csv"
)

JUDGE_AXES: tuple[str, str, str] = ("brand_voice", "citation", "persona_fit")
DEFAULT_PASS_THRESHOLD = 4
DEFAULT_COST_CAP_USD = 0.01

# Policy row IDs for thresholds (3 rows added to POLICY_REGISTER in P12)
POLICY_IDS: dict[str, str] = {
    "brand_voice": "POL-EVAL-JUDGE-THRESHOLD-BRAND-VOICE-V1",
    "citation": "POL-EVAL-JUDGE-THRESHOLD-CITATION-V1",
    "persona_fit": "POL-EVAL-JUDGE-THRESHOLD-PERSONA-FIT-V1",
}


@dataclass
class JudgeResult:
    """One scenario's judge verdict across 3 axes."""

    scenario_id: str
    persona_id: str | None = None
    scores: dict[str, int] = field(default_factory=dict)  # axis -> 1-5
    pass_per_axis: dict[str, bool] = field(default_factory=dict)
    overall_pass: bool = False
    model_id: str = "offline"
    cost_usd: float = 0.0
    latency_ms: int = 0
    skipped: bool = False
    skip_reason: str = ""
    notes: str = ""


def load_judge_thresholds() -> dict[str, int]:
    """Load per-axis pass thresholds from POLICY_REGISTER. Default to 4 if missing.

    Threshold encoded in policy_text via ``min_pass_score=N`` substring per
    POLICY_REGISTER convention (cf I45 P4 cost_ceiling rows).
    """
    out: dict[str, int] = {axis: DEFAULT_PASS_THRESHOLD for axis in JUDGE_AXES}
    if not POLICY_CSV.is_file():
        return out
    with POLICY_CSV.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            policy_id = (row.get("policy_id") or "").strip()
            for axis, pid in POLICY_IDS.items():
                if policy_id == pid:
                    text = row.get("policy_text") or ""
                    m = re.search(r"min_pass_score=(\d+)", text)
                    if m:
                        try:
                            out[axis] = int(m.group(1))
                        except (ValueError, TypeError):
                            pass
    return out


# ──────────────────────────────────────────────────────────────────────────────
# Offline scoring (deterministic; CI-safe)
# ──────────────────────────────────────────────────────────────────────────────


def _heuristic_brand_voice(response: str) -> int:
    """Score 1-5 on brand voice adherence using deterministic substring rules.

    - 5: response uses governance terminology (Holistik Ops, Founder, Compliance)
    - 4: respectful + concise (no marketing fluff)
    - 3: neutral
    - 2: casual / unprofessional
    - 1: violates BRAND_JARGON_AUDIT (e.g., 'guys', 'awesome', 'super exciting')
    """
    if not response:
        return 1
    lower = response.lower()
    # Negative signals (jargon violations)
    forbidden = ("hey guys", "awesome", "super exciting", "lol", "you guys", "totally")
    if any(f in lower for f in forbidden):
        return 1
    # Strong positive signals (governance terminology)
    governance = ("holistik ops", "founder", "compliance", "system owner", "pmo")
    score = 3
    if any(g in lower for g in governance):
        score = 5
    elif "qualification" in lower or "escalate" in lower or "reference" in lower:
        score = 4
    return score


def _heuristic_citation(response: str) -> int:
    """Score 1-5 on citation discipline.

    - 5: response cites docs/references/hlk/ path
    - 4: response cites a specific FILE.md or section header
    - 3: response references a registry or policy by ID
    - 2: vague citation ('our docs')
    - 1: no citation
    """
    if not response:
        return 1
    if "docs/references/hlk/" in response or ".md" in response:
        return 5
    if re.search(r"\b(POL-|SKILL-|PERSONA-|CHAN-|TOPIC-|ROLE-|PROC-|SOP-)[A-Z0-9-]+\b", response):
        return 4
    if re.search(r"\bregistry\b|\bpolicy\b|\bSOP\b", response, re.IGNORECASE):
        return 3
    if "our docs" in response.lower() or "documentation" in response.lower():
        return 2
    return 1


def _heuristic_persona_fit(response: str, persona: dict | None) -> int:
    """Score 1-5 on persona-fit.

    - 5: register matches persona's typical_distance_band + typical_languages
    - 4: appropriate formality
    - 3: neutral
    - 2: register mismatch (over-formal cold or over-casual warm)
    - 1: persona-context-blind (asks "who are you" of a known bridge person)
    """
    if not response:
        return 1
    if persona is None:
        return 3
    # Heuristic: response acknowledges qualification gate when persona has one
    qual_gate = (persona.get("qualification_gate") or "").lower()
    if qual_gate and "confirm" in qual_gate:
        if "qualification" in response.lower() or "confirm" in response.lower():
            return 5
        return 3
    # Distance-band hint: cold personas should escalate; warm should acknowledge
    distance = (persona.get("typical_distance_band") or "")
    if distance.startswith("N3") or distance.startswith("N4"):
        if "escalate" in response.lower() or "qualification" in response.lower():
            return 5
        return 3
    return 4


def score_response_offline(
    response: str,
    scenario: dict,
    persona: dict | None = None,
) -> JudgeResult:
    """Deterministic offline scoring; runs in CI; cost = 0."""
    scenario_id = scenario.get("scenario_id", "")
    persona_id = scenario.get("persona_id") or (persona.get("persona_id") if persona else None)
    thresholds = load_judge_thresholds()

    scores = {
        "brand_voice": _heuristic_brand_voice(response),
        "citation": _heuristic_citation(response),
        "persona_fit": _heuristic_persona_fit(response, persona),
    }
    pass_per_axis = {axis: scores[axis] >= thresholds[axis] for axis in JUDGE_AXES}
    return JudgeResult(
        scenario_id=scenario_id,
        persona_id=persona_id,
        scores=scores,
        pass_per_axis=pass_per_axis,
        overall_pass=all(pass_per_axis.values()),
        model_id="offline",
        cost_usd=0.0,
        latency_ms=0,
        notes="offline-heuristic",
    )


def score_response_live(
    response: str,
    scenario: dict,
    persona: dict | None = None,
    *,
    model_id: str = "claude-3-5-haiku-20241022",
    cost_cap_usd: float = DEFAULT_COST_CAP_USD,
) -> JudgeResult:
    """Live LLM-judge scoring (placeholder; not yet wired).

    Activated when operator pins the live API contract and approves the first
    cost burn. Until then, raises NotImplementedError so callers know the live
    path is gated.
    """
    raise NotImplementedError(
        "Live LLM-judge scoring is gated until operator pins the API contract. "
        "Use score_response_offline() for CI runs. Tracked as D-IH-47-J follow-up."
    )


# ──────────────────────────────────────────────────────────────────────────────
# Cost cap aggregation
# ──────────────────────────────────────────────────────────────────────────────


def aggregate_judge_cost_under_cap(
    results: list[JudgeResult],
    *,
    per_scenario_cap_usd: float = DEFAULT_COST_CAP_USD,
    overall_cap_usd: float | None = None,
) -> tuple[bool, float, list[str]]:
    """Verify all judge results stayed under the per-scenario cap.

    Returns ``(within_cap, total_cost_usd, violations)``.
    """
    violations: list[str] = []
    total = 0.0
    for r in results:
        if r.cost_usd > per_scenario_cap_usd:
            violations.append(
                f"{r.scenario_id}: ${r.cost_usd:.4f} > ${per_scenario_cap_usd:.4f}"
            )
        total += r.cost_usd
    if overall_cap_usd is not None and total > overall_cap_usd:
        violations.append(f"OVERALL: ${total:.4f} > ${overall_cap_usd:.4f}")
    return (len(violations) == 0, total, violations)


# ──────────────────────────────────────────────────────────────────────────────
# Operator-facing dispatch
# ──────────────────────────────────────────────────────────────────────────────


def score_response(
    response: str,
    scenario: dict,
    persona: dict | None = None,
    *,
    model_id: str | None = None,
    cost_cap_usd: float = DEFAULT_COST_CAP_USD,
) -> JudgeResult:
    """Dispatcher: chooses offline vs live based on AKOS_JUDGE_MODEL env var."""
    judge_model = (model_id or os.environ.get("AKOS_JUDGE_MODEL") or "offline").lower()
    if judge_model == "offline" or os.environ.get("AKOS_RECORD_LIVE") != "1":
        return score_response_offline(response, scenario, persona)
    return score_response_live(
        response, scenario, persona, model_id=judge_model, cost_cap_usd=cost_cap_usd
    )
