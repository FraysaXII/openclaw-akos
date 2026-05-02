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
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

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
    """I45 P7: enforce 4-criteria graduation gate for shared->tenant promotion."""
    import json
    from akos.eval_harness.promotion import evaluate_promotion

    if args.override and not args.reason.strip():
        print(
            "  [eval promote] --override requires --reason '<text>' for audit trail (R-45-9)",
            file=sys.stderr,
        )
        return 2

    verdict = evaluate_promotion(
        args.skill,
        override=args.override,
        override_reason=args.reason,
        decided_by="operator",
    )

    if args.json:
        json.dump(verdict.to_dict(), sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
    else:
        print(f"\n  Promotion verdict: {args.skill}")
        print("  " + "=" * 60)
        for c in verdict.criteria:
            marker = {"PASS": " [+]", "FAIL": " [X]", "SKIP": " [~]", "OVERRIDE": " [!]"}.get(c.status, " [?]")
            print(f"{marker} {c.name:32s} [{c.status}] {c.reason}")
        print()
        print(f"  OVERALL: {verdict.overall}")
        if verdict.overall == "OVERRIDE":
            print(f"  WARNING: operator override; audit row will be written to compliance.eval_run")

    if verdict.overall == "FAIL":
        return 1
    return 0


def main() -> int:
    # I45 P8: env bootstrap is the CLI's responsibility (not the runner's).
    # Loading ~/.openclaw/.env here ensures classify_request etc. have access
    # to operator secrets (Ollama URL, Langfuse, Neo4j) WITHOUT polluting
    # pytest sessions that import the runner directly.
    try:
        from akos.io import bootstrap_openclaw_process_env
        bootstrap_openclaw_process_env()
    except Exception:
        pass  # soft-fail; env may not be available in CI

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

    p_promote = sub.add_parser("promote", help="enforce skill graduation gate (P7): 4-criteria check")
    p_promote.add_argument("--skill", required=True, help="skill_id to evaluate for promotion")
    p_promote.add_argument("--override", action="store_true", help="bypass all 4 criteria (requires --reason)")
    p_promote.add_argument("--reason", default="", help="audit reason; mandatory with --override (R-45-9)")
    p_promote.add_argument("--json", action="store_true", help="emit verdict as JSON")

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
    parser.add_argument(
        "--enforce-cost",
        action="store_true",
        help="canary: enforce per-skill cost ceilings from POLICY_REGISTER (D-IH-45-D)",
    )
    parser.add_argument(
        "--tier",
        choices=("A", "B"),
        default="A",
        help="A=offline (replay+canary; default; CI-friendly); B=live LLM regression (requires AKOS_RECORD_LIVE=1; emits eval_run mirror row)",
    )
    parser.add_argument(
        "--max-spend",
        type=float,
        default=None,
        help="Tier B cost ceiling kill switch (USD per run; defaults to MAX_TIER_B_USD env var or 5.0)",
    )
    parser.add_argument(
        "--regression-pp",
        type=float,
        default=5.0,
        help="Tier B hard-fail threshold in pp vs cassette baseline (default 5.0)",
    )
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
    # I47 P10 (D-IH-47-F): per-persona scorecard filter + difficulty meta-eval
    parser.add_argument(
        "--persona",
        default="",
        help="I47 P10: filter scorecard rows to one persona_id (e.g. PERSONA-INVESTOR-COLD).",
    )
    parser.add_argument(
        "--difficulty",
        default="",
        choices=["", "trivial", "moderate", "hard", "impossible"],
        help="I47 P10: filter scorecard rows to one difficulty class.",
    )
    parser.add_argument(
        "--calibrate",
        action="store_true",
        help="I47 P10: emit calibration distribution (vs D-IH-47-C 40/40/10/10) and exit.",
    )
    # I47 P12 (D-IH-47-J): LLM-judge cost cap
    parser.add_argument(
        "--judge-cost-cap",
        type=float,
        default=0.01,
        help="I47 P12: cap LLM-judge cost per scenario in USD (default 0.01).",
    )
    parser.add_argument(
        "--no-judge",
        action="store_true",
        help="I47 P12: skip the LLM-judge axis evaluation (default: enabled when judge.py present).",
    )

    args = parser.parse_args()

    if args.cmd == "list":
        return cmd_list()
    if args.cmd == "record":
        return cmd_record(args)
    if args.cmd == "promote":
        return cmd_promote(args)

    # I47 P10: --calibrate exits early after rendering distribution
    if args.calibrate:
        from akos.eval_harness.persona import (
            calibration_distribution,
            render_calibration_markdown,
        )
        results = calibration_distribution()
        sys.stdout.write(render_calibration_markdown(results))
        return 0 if all(r.overall_pass for r in results.values()) else 0  # warn-only by default

    modes = args.mode or ["all"]
    # Tier B preflight: if --tier B without AKOS_RECORD_LIVE=1, refuse and explain.
    import os
    if args.tier == "B" and os.environ.get("AKOS_RECORD_LIVE", "") != "1":
        print(
            "  [eval --tier B] AKOS_RECORD_LIVE=1 is required for live LLM cassette\n"
            "  recording / replay against Tier B models. This is a cost-control guard\n"
            "  per D-IH-45-C + R-45-3.\n"
            "  Tier A (default) replays existing deterministic cassettes without LLM cost.",
            file=sys.stderr,
        )
        return 2

    # Tier B kill switch — best effort budget cap surface (the real spend tracking
    # will land when live LLM cassettes populate Langfuse via I46 P3 PoC + P6 here).
    max_spend = args.max_spend
    if max_spend is None:
        try:
            max_spend = float(os.environ.get("MAX_TIER_B_USD", "5.0"))
        except ValueError:
            max_spend = 5.0
    if args.tier == "B":
        print(
            f"  [eval --tier B] Live regression mode. Cost ceiling: ${max_spend:.2f} per run.\n"
            f"  Hard-fail threshold: {args.regression_pp:+.1f}pp vs cassette baseline.",
            file=sys.stderr,
        )

    sc = run_modes(
        modes,
        suite_ids=args.suite or None,
        governance_only=args.governance_rubric,
        threshold_pp=args.threshold,
        overrides=_parse_overrides(args.current),
        replay_skill=args.replay_skill,
        enforce_cost=args.enforce_cost,
    )

    # I47 P10 (D-IH-47-F): post-run persona / difficulty filter
    if args.persona or args.difficulty:
        kept = []
        for r in sc.rows:
            pid = getattr(r, "persona_id", None)
            diff = getattr(r, "difficulty_class", None)
            if args.persona and pid != args.persona:
                continue
            if args.difficulty and diff != args.difficulty:
                continue
            kept.append(r)
        sc.rows = kept
        sc.metadata["i47_filter"] = {
            "persona_id": args.persona or None,
            "difficulty_class": args.difficulty or None,
            "rows_after_filter": len(kept),
        }

    # Tier B post-run: enforce regression threshold + spend ceiling
    if args.tier == "B":
        # Roll-up cost across all rows
        total_cost = sum((r.get("cost_usd") or 0.0) if isinstance(r, dict) else (r.cost_usd or 0.0) for r in sc.rows)
        if total_cost > max_spend:
            print(
                f"  [eval --tier B] BUDGET EXCEEDED: total ${total_cost:.4f} > ceiling ${max_spend:.2f}\n"
                f"  Killing run.",
                file=sys.stderr,
            )
            sc.overall_status = "fail"
            sc.metadata["tier_b_killed_for_budget"] = True
        # Hard-fail any row whose delta_pp regression exceeds --regression-pp
        for r in sc.rows:
            dp = r.delta_pp if hasattr(r, "delta_pp") else None
            if dp is not None and dp < -args.regression_pp:
                r.status = "FAIL"
                r.failures = list(r.failures or []) + [f"tier_b_regression:{dp:+.1f}pp>-{args.regression_pp:.1f}pp"]
                sc.overall_status = "fail"

    # I47 P13 item 4 (D-IH-47-G): live-write Scorecard rows to
    # compliance.eval_run. Best-effort; silently no-ops when SUPABASE_URL +
    # SUPABASE_SERVICE_ROLE_KEY env vars are unset.
    try:
        from akos.eval_harness.eval_run_writer import write_scorecard_rows
        try:
            git_sha = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=str(REPO_ROOT), text=True, timeout=3
            ).strip()
        except Exception:
            git_sha = "unknown"
        write_stats = write_scorecard_rows(sc, source_git_sha=git_sha)
        sc.metadata["eval_run_writer"] = write_stats
    except Exception as exc:  # pragma: no cover (defensive; writer is advisory)
        sc.metadata["eval_run_writer_error"] = str(exc)[:200]

    if args.json:
        sys.stdout.write(sc.to_json())
        sys.stdout.write("\n")
    else:
        sys.stdout.write(sc.to_markdown())

    return 1 if (args.exit_on_fail and sc.overall_status == "fail") else 0


if __name__ == "__main__":
    sys.exit(main())
