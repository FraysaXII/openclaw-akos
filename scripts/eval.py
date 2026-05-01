#!/usr/bin/env python3
"""Initiative 45 P1 — Unified eval CLI.

Replaces three drifting entry points with one:
- ``scripts/run-evals.py``   → ``py scripts/eval.py --mode rubric``
- ``scripts/eval_per_skill.py`` → ``py scripts/eval.py --mode canary``
- ``%TEMP%/madeira_uat_inproc.py`` → ``py scripts/eval.py --mode smoke``
- (new in P2) ``py scripts/eval.py replay --skill <id>`` for cassette replay
- (new in P7) ``py scripts/eval.py promote --skill <id>`` for graduation gate

The old scripts remain as backward-compat shims that print a deprecation warning
and dispatch into this CLI. Per the I45 master-roadmap they stay for at least
one release cycle before removal.

Usage::

    py scripts/eval.py --mode all                       # smoke + canary + rubric
    py scripts/eval.py --mode canary --json
    py scripts/eval.py --mode rubric --suite pathc-research-spine
    py scripts/eval.py --mode rubric --governance-rubric
    py scripts/eval.py --mode canary --current SKILL-MADEIRA-LOOKUP-V1=88.0
    py scripts/eval.py --mode replay --skill SKILL-MADEIRA-LOOKUP-V1   # P2 stub
    py scripts/eval.py list                                            # discover
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.eval_harness import list_suite_ids
from akos.eval_harness.v2 import VALID_MODES, run_modes


def _parse_overrides(args: list[str]) -> dict[str, float]:
    out: dict[str, float] = {}
    for a in args or []:
        if "=" not in a:
            continue
        sid, pct = a.split("=", 1)
        try:
            out[sid.strip()] = float(pct.strip())
        except ValueError:
            continue
    return out


def cmd_list() -> int:
    print("\n  AKOS eval surface (v2)")
    print("  " + "=" * 60)
    suites = list_suite_ids()
    print(f"\n  Suites under tests/evals/suites/ ({len(suites)}):")
    for s in suites:
        print(f"    - {s}")

    skill_csv = (
        Path(__file__).resolve().parent.parent
        / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "SKILL_REGISTRY.csv"
    )
    if skill_csv.is_file():
        import csv

        with skill_csv.open(encoding="utf-8", newline="") as fh:
            skills = [r["skill_id"] for r in csv.DictReader(fh)]
        print(f"\n  Skills in SKILL_REGISTRY.csv ({len(skills)}):")
        for s in skills:
            print(f"    - {s}")
    else:
        print("\n  Skills: SKILL_REGISTRY.csv not found")

    cassette_root = Path(__file__).resolve().parent.parent / "tests" / "evals" / "cassettes"
    if cassette_root.is_dir():
        cassettes = sorted(cassette_root.glob("*/*.jsonl"))
        print(f"\n  Cassettes under tests/evals/cassettes/ ({len(cassettes)}):")
        for c in cassettes[:20]:
            print(f"    - {c.relative_to(cassette_root.parent.parent.parent)}")
        if len(cassettes) > 20:
            print(f"    ... and {len(cassettes) - 20} more")
    else:
        print("\n  Cassettes: tests/evals/cassettes/ not yet created (P2)")
    print()
    return 0


def cmd_record(args: argparse.Namespace) -> int:
    """Record a cassette. Two paths:

    - --kind classify_request (default): deterministic; no LLM; safe without AKOS_RECORD_LIVE
    - --kind live_llm: real LLM call; requires AKOS_RECORD_LIVE=1 (P6 fills in the actual LLM call)
    """
    import os
    from akos.eval_harness.cassette import (
        record_classify_request_cassette,
        record_live_llm_cassette,
    )

    if not args.prompt:
        print("  [eval record] --prompt is required (the input text to capture)", file=sys.stderr)
        return 2

    if args.kind == "live_llm":
        if os.environ.get("AKOS_RECORD_LIVE", "") != "1":
            print(
                "  [eval record] --kind live_llm requires AKOS_RECORD_LIVE=1 (cost-control guard).\n"
                f"  Set the env var, then re-run: py scripts/eval.py record --skill {args.skill} ...",
                file=sys.stderr,
            )
            return 2
        try:
            path = record_live_llm_cassette(
                skill_id=args.skill,
                probe_id=args.probe,
                prompt=args.prompt,
                recorded_by=args.by or "operator",
                model_id=args.model_id or "unknown",
                model_tier=args.model_tier or "flagship",
                golden_rubric={
                    "contains": args.contains or [],
                    "forbidden": args.forbidden or [],
                },
            )
        except PermissionError as e:
            print(f"  [eval record] {e}", file=sys.stderr)
            return 2
    else:
        path = record_classify_request_cassette(
            skill_id=args.skill,
            probe_id=args.probe,
            prompt=args.prompt,
            recorded_by=args.by or "operator",
        )

    print(f"  [eval record] wrote {path}", file=sys.stderr)
    return 0


def cmd_promote(args: argparse.Namespace) -> int:
    # P7 deliverable. Stub here for CLI completeness.
    print(
        f"  [eval promote] P7 stub: would gate skill={args.skill} on "
        f"(3x Tier A green, 1x Tier B within 14d, adversarial pass, non-empty routing_condition). "
        f"Implementation lands in P7.",
        file=sys.stderr,
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="eval.py",
        description="AKOS unified eval CLI (Initiative 45 P1)",
    )
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("list", help="discover suites + skills + cassettes")

    p_record = sub.add_parser("record", help="record a cassette (deterministic safe; live_llm requires AKOS_RECORD_LIVE=1)")
    p_record.add_argument("--skill", required=True, help="skill_id to record")
    p_record.add_argument("--probe", required=True, help="probe_id (filename stem)")
    p_record.add_argument("--prompt", required=True, help="input text to capture")
    p_record.add_argument(
        "--kind",
        choices=("classify_request", "live_llm"),
        default="classify_request",
        help="cassette type (default: classify_request, deterministic, no LLM)",
    )
    p_record.add_argument("--by", default="", help="recorded_by handle")
    p_record.add_argument("--model-id", default="", help="model id (for live_llm)")
    p_record.add_argument("--model-tier", default="", help="model tier (for live_llm)")
    p_record.add_argument("--contains", action="append", help="golden_rubric contains list (live_llm)")
    p_record.add_argument("--forbidden", action="append", help="golden_rubric forbidden list (live_llm)")

    p_promote = sub.add_parser("promote", help="enforce skill graduation gate (P7)")
    p_promote.add_argument("--skill", required=True)
    p_promote.add_argument("--override", action="store_true")
    p_promote.add_argument("--reason", default="")

    parser.add_argument(
        "--mode",
        action="append",
        choices=VALID_MODES,
        help="mode(s) to run; pass multiple times for multi-mode (default: --mode all)",
    )
    parser.add_argument("--suite", action="append", default=[], help="rubric: filter by suite_id")
    parser.add_argument(
        "--governance-rubric",
        action="store_true",
        help="rubric: only suites in eval_rubric_governance_suites",
    )
    parser.add_argument("--threshold", type=float, default=2.0, help="canary 2 threshold (pp)")
    parser.add_argument(
        "--current",
        action="append",
        default=[],
        help="canary: override current score (--current SKILL-ID=PCT, repeatable)",
    )
    parser.add_argument("--replay-skill", default=None, help="replay: filter to one skill_id")
    parser.add_argument("--json", action="store_true", help="emit JSON scorecard to stdout")
    parser.add_argument(
        "--exit-on-fail",
        action="store_true",
        default=True,
        help="exit 1 if overall_status=fail (default: enabled)",
    )
    parser.add_argument(
        "--no-exit-on-fail", dest="exit_on_fail", action="store_false", help="always exit 0"
    )

    args = parser.parse_args()

    if args.cmd == "list":
        return cmd_list()
    if args.cmd == "record":
        return cmd_record(args)
    if args.cmd == "promote":
        return cmd_promote(args)

    modes = args.mode or ["all"]
    sc = run_modes(
        modes,
        suite_ids=args.suite or None,
        governance_only=args.governance_rubric,
        threshold_pp=args.threshold,
        overrides=_parse_overrides(args.current),
        replay_skill=args.replay_skill,
    )

    if args.json:
        sys.stdout.write(sc.to_json())
        sys.stdout.write("\n")
    else:
        sys.stdout.write(sc.to_markdown())

    return 1 if (args.exit_on_fail and sc.overall_status == "fail") else 0


if __name__ == "__main__":
    sys.exit(main())
