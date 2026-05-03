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
    model_id: str | None = None,
    cost_cap_usd: float = DEFAULT_COST_CAP_USD,
    member_scorer: "MemberScorer | None" = None,
) -> JudgeResult:
    """Live LLM-judge scoring via :class:`JudgeRoster` (I52 P2; D-IH-52-A).

    Behaviour by env:

    - ``AKOS_JUDGE_ROSTER`` set      -> route through :class:`JudgeRoster`
      (multi-model consensus per :class:`prompts/judge/JUDGE_ROSTER_V1.md`).
    - ``AKOS_JUDGE_ROSTER`` unset    -> NotImplementedError (preserves the
      I47/P12 contract: never silently fall through to single-model live mode).

    The ``member_scorer`` kwarg is the test-injection seam; production callers
    leave it ``None`` and the default scorer dispatches per-provider via
    :func:`_default_member_scorer`. Tests inject a deterministic stub.
    """
    roster_env = os.environ.get("AKOS_JUDGE_ROSTER", "").strip()
    if not roster_env:
        raise NotImplementedError(
            "Live LLM-judge scoring requires AKOS_JUDGE_ROSTER env var "
            "(comma-separated model_ids per prompts/judge/JUDGE_ROSTER_V1.md). "
            "Use score_response_offline() for CI runs without a roster."
        )
    roster = JudgeRoster.from_env()
    return roster.score(
        response,
        scenario,
        persona=persona,
        cost_cap_usd=cost_cap_usd,
        member_scorer=member_scorer,
    )


# ──────────────────────────────────────────────────────────────────────────────
# Multi-model judge dispatcher (I52 P2; D-IH-52-A / D-IH-52-B)
# ──────────────────────────────────────────────────────────────────────────────

JUDGE_ROSTER_ENV = "AKOS_JUDGE_ROSTER"
JUDGE_ROSTER_CHEAP_ENV = "AKOS_JUDGE_ROSTER_CHEAP"
JUDGE_MODE_ENV = "AKOS_JUDGE_MODE"  # consensus | per_axis | tiered (default consensus)
VALID_JUDGE_MODES: tuple[str, ...] = ("consensus", "per_axis", "tiered")
DEFAULT_JUDGE_MODE = "consensus"


@dataclass
class MemberScore:
    """One roster member's raw output for one scenario."""

    model_id: str
    scores: dict[str, int]  # axis -> 1-5
    notes: dict[str, str] = field(default_factory=dict)
    cost_usd: float = 0.0
    latency_ms: int = 0
    fallback_offline: bool = False
    raw_error: str = ""


# A MemberScorer takes (model_id, response, scenario, persona) and returns a
# MemberScore. Production default dispatches per-provider; tests inject a stub.
from typing import Callable

MemberScorer = Callable[[str, str, dict, "dict | None"], MemberScore]


def _default_member_scorer(
    model_id: str,
    response: str,
    scenario: dict,
    persona: dict | None,
) -> MemberScore:
    """Default member scorer: per-provider API call + graceful offline fallback.

    Behaviour:

    - ``offline:*``                    -> offline heuristic (cost = 0)
    - ``deterministic:*``              -> offline heuristic (cost = 0)
    - ``anthropic:*`` / ``openai:*``   -> if matching API key env present, call
      API with :file:`prompts/judge/JUDGE_PROMPT_V1.md`; otherwise fall back to
      offline heuristic and set ``fallback_offline=True``.

    The actual HTTP call is intentionally NOT implemented in this module — it
    is wired in :func:`_call_member_via_api` (P2 follow-up). For now the live
    path falls through to offline with ``fallback_offline=True`` so cassette
    capture, schema, and tests are exercised without burning credentials. The
    operator activates real API calls in P3 by setting ``AKOS_JUDGE_LIVE_API=1``
    AND providing the per-provider API key.
    """
    if model_id.startswith("offline:") or model_id.startswith("deterministic:"):
        offline = score_response_offline(response, scenario, persona)
        return MemberScore(
            model_id=model_id,
            scores=dict(offline.scores),
            notes={axis: "offline-heuristic" for axis in JUDGE_AXES},
            cost_usd=0.0,
            latency_ms=offline.latency_ms,
            fallback_offline=False,
        )

    api_live = os.environ.get("AKOS_JUDGE_LIVE_API") == "1"
    has_creds = (
        (model_id.startswith("anthropic:") and bool(os.environ.get("ANTHROPIC_API_KEY")))
        or (model_id.startswith("openai:") and bool(os.environ.get("OPENAI_API_KEY")))
    )

    if api_live and has_creds:
        try:
            return _call_member_via_api(model_id, response, scenario, persona)
        except Exception as exc:  # noqa: BLE001 - intentional broad fallback
            offline = score_response_offline(response, scenario, persona)
            return MemberScore(
                model_id=model_id,
                scores=dict(offline.scores),
                notes={axis: "fallback-offline-api-error" for axis in JUDGE_AXES},
                cost_usd=0.0,
                latency_ms=offline.latency_ms,
                fallback_offline=True,
                raw_error=f"{type(exc).__name__}: {exc}",
            )

    offline = score_response_offline(response, scenario, persona)
    reason = "no-api-key" if not has_creds else "no-live-api-flag"
    return MemberScore(
        model_id=model_id,
        scores=dict(offline.scores),
        notes={axis: f"fallback-offline-{reason}" for axis in JUDGE_AXES},
        cost_usd=0.0,
        latency_ms=offline.latency_ms,
        fallback_offline=True,
    )


def _call_member_via_api(
    model_id: str,
    response: str,
    scenario: dict,
    persona: dict | None,
) -> MemberScore:
    """Per-provider live API dispatch (placeholder; activated in P3).

    Raises NotImplementedError until P3 calibration burn approves the API
    contract for each provider. Until then, the default scorer routes around
    this function via the offline-fallback path so test infrastructure works.
    """
    raise NotImplementedError(
        f"Live API call for {model_id!r} not yet wired; activate in I52 P3 "
        "calibration burn or inject a MemberScorer stub for tests."
    )


@dataclass
class JudgeRoster:
    """Multi-model judge roster + composition mode dispatcher (D-IH-52-A/B).

    Members are ordered: position 1 wins ties under consensus mode.
    """

    members: list[str] = field(default_factory=list)
    mode: str = DEFAULT_JUDGE_MODE
    per_axis_routing: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_env(
        cls,
        *,
        env_name: str = JUDGE_ROSTER_ENV,
        mode_env_name: str = JUDGE_MODE_ENV,
    ) -> "JudgeRoster":
        roster_str = os.environ.get(env_name, "").strip()
        if not roster_str:
            raise ValueError(
                f"{env_name} env var is empty; cannot construct JudgeRoster. "
                "See prompts/judge/JUDGE_ROSTER_V1.md for the contract."
            )
        members = [m.strip() for m in roster_str.split(",") if m.strip()]
        if len(members) < 1:
            raise ValueError(f"{env_name} resolved to 0 members.")
        mode = os.environ.get(mode_env_name, DEFAULT_JUDGE_MODE).strip().lower()
        if mode not in VALID_JUDGE_MODES:
            raise ValueError(
                f"{mode_env_name}={mode!r} not in {VALID_JUDGE_MODES}; "
                "see prompts/judge/JUDGE_ROSTER_V1.md."
            )
        return cls(members=members, mode=mode)

    def fingerprint(self) -> str:
        """Stable cassette-attached id for the roster + mode (preserves order)."""
        if self.mode == "per_axis" and self.per_axis_routing:
            axis_part = "|".join(
                f"{a}={self.per_axis_routing.get(a, '?')}" for a in JUDGE_AXES
            )
            return f"roster[{','.join(self.members)}]/mode={self.mode}/{axis_part}"
        return f"roster[{','.join(self.members)}]/mode={self.mode}"

    def score(
        self,
        response: str,
        scenario: dict,
        *,
        persona: dict | None = None,
        cost_cap_usd: float = DEFAULT_COST_CAP_USD,
        member_scorer: MemberScorer | None = None,
    ) -> JudgeResult:
        scorer = member_scorer or _default_member_scorer
        scenario_id = scenario.get("scenario_id", "")
        persona_id = scenario.get("persona_id") or (
            persona.get("persona_id") if persona else None
        )
        thresholds = load_judge_thresholds()

        member_scores: list[MemberScore] = []
        for model_id in self.members:
            ms = scorer(model_id, response, scenario, persona)
            member_scores.append(ms)

        if self.mode == "consensus":
            scores = _compose_consensus(member_scores)
        elif self.mode == "per_axis":
            scores = _compose_per_axis(member_scores, self.per_axis_routing)
        elif self.mode == "tiered":
            scores = _compose_tiered(member_scores)
        else:  # pragma: no cover - guarded by from_env
            scores = _compose_consensus(member_scores)

        pass_per_axis = {
            axis: scores[axis] >= thresholds[axis] for axis in JUDGE_AXES
        }
        total_cost = sum(ms.cost_usd for ms in member_scores)
        any_fallback = any(ms.fallback_offline for ms in member_scores)

        notes_parts: list[str] = [self.fingerprint()]
        if any_fallback:
            fallbacks = [
                ms.model_id for ms in member_scores if ms.fallback_offline
            ]
            notes_parts.append(f"fallback-offline:{','.join(fallbacks)}")

        return JudgeResult(
            scenario_id=scenario_id,
            persona_id=persona_id,
            scores=scores,
            pass_per_axis=pass_per_axis,
            overall_pass=all(pass_per_axis.values()),
            model_id=self.fingerprint(),
            cost_usd=total_cost,
            latency_ms=max((ms.latency_ms for ms in member_scores), default=0),
            notes="; ".join(notes_parts),
        )


def _compose_consensus(member_scores: list[MemberScore]) -> dict[str, int]:
    """Per-axis majority vote; ties broken by position-1 (first member)."""
    out: dict[str, int] = {}
    for axis in JUDGE_AXES:
        values = [ms.scores.get(axis, DEFAULT_PASS_THRESHOLD) for ms in member_scores]
        if not values:
            out[axis] = DEFAULT_PASS_THRESHOLD
            continue
        # Majority: pick the most-frequent value; tie-break by position-1 value.
        from collections import Counter

        counter = Counter(values)
        top_count = max(counter.values())
        winners = [v for v, c in counter.items() if c == top_count]
        if len(winners) == 1:
            out[axis] = winners[0]
        else:
            # Tie-break: position-1 (member_scores[0]) value, if it's a winner
            position1_value = values[0]
            out[axis] = position1_value if position1_value in winners else min(winners)
    return out


def _compose_per_axis(
    member_scores: list[MemberScore],
    per_axis_routing: dict[str, str],
) -> dict[str, int]:
    """Each axis routed to a specific roster member; missing routes fall back to position-1."""
    by_model = {ms.model_id: ms for ms in member_scores}
    fallback = member_scores[0] if member_scores else None
    out: dict[str, int] = {}
    for axis in JUDGE_AXES:
        target = per_axis_routing.get(axis)
        ms = by_model.get(target) if target else None
        if ms is None and fallback is not None:
            ms = fallback
        out[axis] = (
            ms.scores.get(axis, DEFAULT_PASS_THRESHOLD)
            if ms is not None
            else DEFAULT_PASS_THRESHOLD
        )
    return out


def _compose_tiered(member_scores: list[MemberScore]) -> dict[str, int]:
    """Cost-aware tiered escalation (placeholder; D-IH-52-B activation gated to P3).

    At I52 P2 launch, tiered mode collapses to position-1's scores. The full
    escalation logic (cheap first; flagship if cheap members disagree) lands in
    P3 calibration burn once we have alignment data per axis.
    """
    if not member_scores:
        return {axis: DEFAULT_PASS_THRESHOLD for axis in JUDGE_AXES}
    return dict(member_scores[0].scores)


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
    member_scorer: MemberScorer | None = None,
) -> JudgeResult:
    """Operator-facing dispatcher.

    Decision tree (in order):

    1. If ``AKOS_RECORD_LIVE`` is not ``"1"``       -> offline (CI default).
    2. Else if ``AKOS_JUDGE_ROSTER`` env is set      -> :class:`JudgeRoster`
       (multi-model consensus per I52 P2; D-IH-52-A).
    3. Else if ``AKOS_JUDGE_MODEL`` env is set       -> :func:`score_response_live`
       single-model fallback (preserves I47/P12 contract; raises
       NotImplementedError until roster-or-model env is set).
    4. Else                                          -> offline.

    The ``member_scorer`` kwarg is the test-injection seam; production callers
    leave it ``None``.
    """
    if os.environ.get("AKOS_RECORD_LIVE") != "1":
        return score_response_offline(response, scenario, persona)
    if os.environ.get(JUDGE_ROSTER_ENV, "").strip():
        roster = JudgeRoster.from_env()
        return roster.score(
            response,
            scenario,
            persona=persona,
            cost_cap_usd=cost_cap_usd,
            member_scorer=member_scorer,
        )
    judge_model = (model_id or os.environ.get("AKOS_JUDGE_MODEL") or "offline").lower()
    if judge_model == "offline":
        return score_response_offline(response, scenario, persona)
    return score_response_live(
        response,
        scenario,
        persona,
        model_id=judge_model,
        cost_cap_usd=cost_cap_usd,
        member_scorer=member_scorer,
    )
