#!/usr/bin/env python3
"""Intent-Ranked Regression runbook (either-seat).

Emits the operator's regression surfaces ordered by **Intent Criticality Score**
(ICS) so a sweep checks the highest-stakes surfaces first. This is the *execution
seat* half of the discipline; the *thinking seat* half (judgment + disposition) is
``.cursor/skills/intent-ranked-regression-craft/SKILL.md``.

Pydantic SSOT: ``akos/hlk_intent_ranked_regression.py``
Draft cursor rule: ``.cursor/rules/akos-intent-ranked-regression.mdc``
Report worked example: ``docs/wip/planning/88-cross-area-ops-wiring-review-discipline/reports/intent-ranked-regression-2026-06-05.md``

CLI::

    py scripts/intent_ranked_regression.py --rank        # ranked sweep order + probe cmds
    py scripts/intent_ranked_regression.py --tiers       # the intent corpus + weights
    py scripts/intent_ranked_regression.py --self-test   # validate the model (pre_commit)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_intent_ranked_regression import (  # noqa: E402
    ICS_MAX,
    ICS_WEIGHTS,
    INTENT_TIERS,
    INTENT_TIERS_BY_ID,
    REGRESSION_SURFACES,
    IntentTier,
    RegressionSurface,
    rank_surfaces,
)


def print_tiers() -> int:
    print("Intent tiers (operator-intent corpus; value 1-5, evidenced)\n")
    print("| Tier | Value | Horizon | Intent |")
    print("| --- | :---: | --- | --- |")
    for t in sorted(INTENT_TIERS, key=lambda x: (-x.value, x.tier_id)):
        print(f"| {t.tier_id} | {t.value} | {t.horizon} | {t.name} |")
    return 0


def print_rank() -> int:
    ranked = rank_surfaces()
    w = ICS_WEIGHTS
    print(
        f"Intent-Ranked Regression — sweep order (ICS = {w['intent_value']}*intent "
        f"+ {w['time_criticality']}*time + {w['risk_reduction']}*risk "
        f"+ {w['detection_gap']}*detection_gap; max {ICS_MAX}; ! = severity-first)\n"
    )
    print("| # | Surface | ICS | IV | TC | RR | DG | ! | Probe |")
    print("| :-: | --- | :-: | :-: | :-: | :-: | :-: | :-: | --- |")
    for i, (s, ics) in enumerate(ranked, start=1):
        iv = s.intent_value(INTENT_TIERS_BY_ID)
        flag = "!" if s.severity_first else ""
        probe = s.probe_cmd.split(";")[0] if s.probe_cmd else "(judgment-only)"
        print(
            f"| {i} | {s.surface_id} {s.name} | {ics} | {iv} | "
            f"{s.time_criticality} | {s.risk_reduction} | {s.detection_gap} | {flag} | `{probe}` |"
        )
    return 0


def run_self_test() -> int:
    # All tiers + surfaces construct (Pydantic validated at import).
    if len(INTENT_TIERS) != 7:
        print(f"FAIL: expected 7 intent tiers, got {len(INTENT_TIERS)}")
        return 1
    if len(REGRESSION_SURFACES) < 10:
        print(f"FAIL: expected >=10 regression surfaces, got {len(REGRESSION_SURFACES)}")
        return 1
    # Every served tier resolves.
    for s in REGRESSION_SURFACES:
        for t in s.served_tiers:
            if t not in INTENT_TIERS_BY_ID:
                print(f"FAIL: {s.surface_id} references unknown tier {t!r}")
                return 1
    # Ranking is deterministic + severity-first surfaces lead.
    ranked = rank_surfaces()
    if len(ranked) != len(REGRESSION_SURFACES):
        print("FAIL: ranking dropped surfaces")
        return 1
    sev_positions = [i for i, (s, _) in enumerate(ranked) if s.severity_first]
    non_sev_positions = [i for i, (s, _) in enumerate(ranked) if not s.severity_first]
    if sev_positions and non_sev_positions and max(sev_positions) > min(non_sev_positions):
        print("FAIL: severity-first surfaces must lead the sweep order")
        return 1
    # ICS within bounds.
    for s, ics in ranked:
        if not (0 < ics <= ICS_MAX):
            print(f"FAIL: {s.surface_id} ICS {ics} out of bounds (0, {ICS_MAX}]")
            return 1
    # Re-rank is stable.
    if [s.surface_id for s, _ in ranked] != [s.surface_id for s, _ in rank_surfaces()]:
        print("FAIL: ranking is not deterministic")
        return 1
    print(
        f"PASS (self-test): {len(INTENT_TIERS)} tiers, {len(REGRESSION_SURFACES)} surfaces, "
        f"ICS_MAX={ICS_MAX}, severity-first leads"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rank", action="store_true", help="print ICS-ranked sweep order")
    parser.add_argument("--tiers", action="store_true", help="print the intent corpus")
    parser.add_argument("--self-test", action="store_true", help="validate the model (pre_commit)")
    args = parser.parse_args()
    if args.self_test:
        return run_self_test()
    if args.tiers:
        return print_tiers()
    if args.rank:
        return print_rank()
    print("INFO: use --rank, --tiers, or --self-test")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
