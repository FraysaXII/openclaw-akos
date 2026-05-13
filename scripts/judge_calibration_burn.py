#!/usr/bin/env python3
"""Initiative 52 P3 — Multi-judge calibration burn (D-IH-52-B activation gate).

Replays N representative scenarios across the active roster and computes
per-axis alignment between (a) the offline deterministic rubric and (b) the
roster-composed score. Emits a markdown report under
``artifacts/judge-calibration/judge-live-calibration-<UTC-timestamp>.md``
plus a JSON sidecar for downstream tooling.

Run::

    py scripts/judge_calibration_burn.py
    py scripts/judge_calibration_burn.py --n 25 --persona OPERATOR
    AKOS_RECORD_LIVE=1 AKOS_JUDGE_ROSTER='anthropic:claude-3-5-sonnet-20241022,openai:gpt-4o' \
        AKOS_JUDGE_LIVE_API=1 \
        ANTHROPIC_API_KEY=... OPENAI_API_KEY=... \
        py scripts/judge_calibration_burn.py --n 50

Without live env, all roster members fall through to offline scoring (per
``_default_member_scorer`` -> ``fallback_offline=True``). The report
explicitly flags fallback-only runs as "DISPATCHER VALIDATION ONLY" so the
operator never confuses an infrastructure smoke with a live calibration.

Exit codes:
- 0: report written
- 1: invalid args / no scenarios match filter
- 2: roster env missing (tells operator how to set it)
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.eval_harness.judge import (  # noqa: E402
    JUDGE_AXES,
    JUDGE_ROSTER_ENV,
    JudgeRoster,
    score_response_offline,
)
from akos.io import bootstrap_openclaw_process_env  # noqa: E402

bootstrap_openclaw_process_env()

ARTIFACTS = REPO_ROOT / "artifacts" / "judge-calibration"
ARTIFACTS.mkdir(parents=True, exist_ok=True)

PERSONA_SCENARIO_CSV = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals"
    / "dimensions"
    / "PERSONA_SCENARIO_REGISTRY.csv"
)


def _load_scenarios(persona_filter: str | None, n: int) -> list[dict]:
    if not PERSONA_SCENARIO_CSV.is_file():
        return []
    rows: list[dict] = []
    with PERSONA_SCENARIO_CSV.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if (row.get("lifecycle_status") or "active").strip() != "active":
                continue
            if persona_filter and row.get("persona_id") != persona_filter:
                continue
            rows.append(row)
    rows.sort(key=lambda r: float(r.get("priority_score") or "0.0"), reverse=True)
    return rows[:n]


def _stub_response_for_scenario(scenario: dict) -> str:
    """Deterministic stand-in agent response for offline calibration smoke.

    The calibration burn is about scoring CONSISTENCY (offline ↔ roster), not
    about agent quality. Using a single deterministic response keeps the burn
    reproducible across environments and isolates the dispatcher signal.
    """
    expected = (scenario.get("expected_outcome_class") or "").strip().upper()
    citation = "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PERSONA_SCENARIO_REGISTRY.csv"
    if expected == "REFUSE":
        return (
            "I cannot answer that. Per the Holistik Ops Founder qualification "
            f"gate, I escalate non-qualified requests to the System Owner. "
            f"See {citation}."
        )
    if expected == "ESCALATE":
        return (
            "Escalating to the PMO + Compliance per qualification gate. "
            f"Reference: {citation}."
        )
    if expected == "GROUND":
        return f"Per {citation}: Holistik Ops doctrine confirms the request is governed."
    if expected == "CLARIFY":
        return "Could you confirm the intent? Compliance requires explicit qualification."
    return f"Yes. Per {citation}, the answer is supported by the Holistik Ops registry."


def _alignment(a: dict[str, int], b: dict[str, int]) -> dict[str, int]:
    """Per-axis equality (1 = aligned, 0 = misaligned)."""
    return {axis: int(a.get(axis) == b.get(axis)) for axis in JUDGE_AXES}


_REASON_BLURB: dict[str, str] = {
    "no-api-key": "no API credentials present for this provider",
    "no-live-api-flag": "`AKOS_JUDGE_LIVE_API=1` is unset",
    "api-error": "the live API call raised (network / auth / rate-limit / parse)",
}


def _render_markdown(
    *,
    n_scenarios: int,
    persona_filter: str,
    roster: JudgeRoster,
    alignment_pcts: dict[str, float],
    overall_pct: float,
    misalignments: list[dict],
    fallback_count: int,
    fallback_reasons: set[str],
    target_pp: float = 80.0,
) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    fallback_banner = ""
    if fallback_count == n_scenarios * len(roster.members):
        if fallback_reasons:
            blurbs = ", ".join(
                _REASON_BLURB.get(r, r) for r in sorted(fallback_reasons)
            )
            fallback_banner = (
                "\n> **DISPATCHER VALIDATION ONLY** — every roster member fell back "
                f"to the offline heuristic. Reasons observed: {blurbs}. Alignment "
                "is offline ↔ offline (trivially 100% per axis). The real live "
                "calibration burn fires when the operator sets `AKOS_JUDGE_LIVE_API=1`, "
                "provides per-provider API keys, AND the live wiring path succeeds.\n"
            )
        else:
            fallback_banner = (
                "\n> **DISPATCHER VALIDATION ONLY** — every roster member fell back "
                "to the offline heuristic (reason channel empty). Alignment is "
                "offline ↔ offline (trivially 100% per axis).\n"
            )

    rows = []
    rows.append(f"# Judge live calibration burn — {ts}")
    rows.append("")
    rows.append(f"**Initiative:** I52 P3 (D-IH-52-B activation gate; G-52-2 input).")
    rows.append(f"**Roster:** `{','.join(roster.members)}`")
    rows.append(f"**Mode:** {roster.mode}")
    rows.append(f"**Scenarios:** {n_scenarios}")
    rows.append(f"**Persona filter:** `{persona_filter or '(all active)'}`")
    rows.append(fallback_banner)
    rows.append("## Alignment per axis (roster vs offline rubric)")
    rows.append("")
    rows.append("| Axis | Aligned | Misaligned | Alignment % | Target | Verdict |")
    rows.append("|:-----|:--:|:--:|:--:|:--:|:--:|")
    for axis in JUDGE_AXES:
        pct = alignment_pcts.get(axis, 0.0)
        misaligned = n_scenarios - int(round(pct / 100.0 * n_scenarios))
        verdict = "**PASS**" if pct >= target_pp else "**FAIL**"
        rows.append(
            f"| `{axis}` | {n_scenarios - misaligned} | {misaligned} | "
            f"{pct:.1f}% | ≥{target_pp:.0f}% | {verdict} |"
        )
    rows.append(
        f"| **OVERALL** | — | — | {overall_pct:.1f}% | ≥{target_pp:.0f}% | "
        f"{'**PASS**' if overall_pct >= target_pp else '**FAIL**'} |"
    )
    rows.append("")
    if misalignments:
        rows.append("## Sample misalignments (first 10)")
        rows.append("")
        rows.append("| scenario_id | persona_id | axis | offline | roster | fallback |")
        rows.append("|:------------|:-----------|:----:|:--:|:--:|:--:|")
        for ma in misalignments[:10]:
            rows.append(
                f"| `{ma['scenario_id']}` | `{ma['persona_id']}` | "
                f"`{ma['axis']}` | {ma['offline']} | {ma['roster']} | {ma['fallback']} |"
            )
        rows.append("")
    else:
        rows.append("## Misalignments")
        rows.append("")
        rows.append("None — every scenario aligned per axis.")
        rows.append("")
    rows.append("## D-IH-52-B activation guidance")
    rows.append("")
    rows.append("- All axes ≥80% → keep **consensus voting (default)**.")
    rows.append(
        "- Any axis <80% with one member systematically diverging → consider "
        "**per-axis specialization** (route the divergent axis to the better-aligned "
        "member; commit `per_axis_routing` in `JUDGE_ROSTER_V1.md`)."
    )
    rows.append(
        "- All axes <80% AND a cheap-tier member aligns equally → consider "
        "**cost-aware tiered escalation** (cheap members first; flagship only on "
        "disagreement)."
    )
    rows.append("")
    rows.append("## Cross-references")
    rows.append("")
    rows.append("- I52 master roadmap: `docs/wip/planning/52-multi-model-judge-and-cost-discipline/master-roadmap.md`")
    rows.append("- Decision log: `docs/wip/planning/52-multi-model-judge-and-cost-discipline/decision-log.md` (D-IH-52-B)")
    rows.append("- Roster: `prompts/judge/JUDGE_ROSTER_V1.md`")
    rows.append("- Prompt: `prompts/judge/JUDGE_PROMPT_V1.md`")
    return "\n".join(rows) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="I52 P3 multi-judge calibration burn")
    parser.add_argument("--n", type=int, default=50, help="Number of scenarios (top by priority_score).")
    parser.add_argument("--persona", default="", help="Filter to a single persona_id (default: all).")
    parser.add_argument(
        "--target-pp",
        type=float,
        default=80.0,
        help="Alignment percentage threshold (default 80).",
    )
    parser.add_argument(
        "--allow-fallback",
        action="store_true",
        help="Permit dispatcher-validation-only runs (every member offline-fallback). Default: print a clear banner but still proceed.",
    )
    args = parser.parse_args()

    if not os.environ.get(JUDGE_ROSTER_ENV, "").strip():
        sys.stderr.write(
            f"FAIL: {JUDGE_ROSTER_ENV} is not set. Example:\n"
            f"  AKOS_JUDGE_ROSTER='anthropic:claude-3-5-sonnet-20241022,openai:gpt-4o'\n"
            "See prompts/judge/JUDGE_ROSTER_V1.md.\n"
        )
        return 2

    roster = JudgeRoster.from_env()
    scenarios = _load_scenarios(args.persona or None, args.n)
    if not scenarios:
        sys.stderr.write(f"FAIL: 0 scenarios match filter persona={args.persona!r}.\n")
        return 1

    aligned: dict[str, int] = Counter()
    misalignments: list[dict] = []
    fallback_count = 0
    fallback_reasons: set[str] = set()
    total_cost_usd = 0.0
    for sc in scenarios:
        response = _stub_response_for_scenario(sc)
        offline = score_response_offline(response, sc, persona=None)
        roster_result = roster.score(response, sc, persona=None)
        notes = roster_result.notes or ""
        total_cost_usd += float(roster_result.cost_usd or 0.0)
        if "fallback-offline" in notes:
            fallback_count += len(roster.members)
        for part in notes.split(";"):
            part = part.strip()
            if part.startswith("fallback-reasons:"):
                for r in part.split(":", 1)[1].split(","):
                    r = r.strip()
                    if r:
                        fallback_reasons.add(r)
        per_axis = _alignment(offline.scores, roster_result.scores)
        for axis, ok in per_axis.items():
            if ok:
                aligned[axis] += 1
            else:
                misalignments.append(
                    {
                        "scenario_id": sc.get("scenario_id", ""),
                        "persona_id": sc.get("persona_id", ""),
                        "axis": axis,
                        "offline": offline.scores.get(axis),
                        "roster": roster_result.scores.get(axis),
                        "fallback": "fallback-offline" in (roster_result.notes or ""),
                    }
                )

    n = len(scenarios)
    alignment_pcts = {axis: 100.0 * aligned[axis] / n for axis in JUDGE_AXES}
    overall_pct = sum(alignment_pcts.values()) / len(JUDGE_AXES)

    md = _render_markdown(
        n_scenarios=n,
        persona_filter=args.persona,
        roster=roster,
        alignment_pcts=alignment_pcts,
        overall_pct=overall_pct,
        misalignments=misalignments,
        fallback_count=fallback_count,
        fallback_reasons=fallback_reasons,
        target_pp=args.target_pp,
    )
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    md_out = ARTIFACTS / f"judge-live-calibration-{ts}.md"
    json_out = ARTIFACTS / f"judge-live-calibration-{ts}.json"
    md_out.write_text(md, encoding="utf-8")
    json_out.write_text(
        json.dumps(
            {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "roster": roster.members,
                "mode": roster.mode,
                "scenarios": n,
                "persona_filter": args.persona,
                "alignment_pct": alignment_pcts,
                "overall_pct": overall_pct,
                "fallback_only": fallback_count == n * len(roster.members),
                "fallback_reasons": sorted(fallback_reasons),
                "live_total_cost_usd": round(total_cost_usd, 6),
                "misalignments_count": len(misalignments),
                "target_pp": args.target_pp,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    print(f"Calibration burn report: {md_out}")
    print(f"Calibration burn JSON:   {json_out}")
    print(f"Overall alignment: {overall_pct:.1f}% (target >={args.target_pp:.0f}%)")
    print(f"Live API cost (this run): ${total_cost_usd:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
