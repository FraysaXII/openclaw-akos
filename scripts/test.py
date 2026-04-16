#!/usr/bin/env python3
"""Friendly test runner for AKOS.

Usage:
    py scripts/test.py              # run all 300+ tests
    py scripts/test.py api          # FastAPI endpoints + E2E pipeline
    py scripts/test.py security     # alerts, permissions, config validation
    py scripts/test.py runpod       # RunPod provider (mocked SDK)
    py scripts/test.py prompts      # prompt structure + assembly
    py scripts/test.py models       # Pydantic model schemas
    py scripts/test.py checkpoints  # workspace snapshot/restore
    py scripts/test.py scaffolding  # file tree integrity + secrets scan
    py scripts/test.py e2e          # full system wiring
    py scripts/test.py uat          # start live API server for Swagger testing
    py scripts/test.py graph        # HLK graph lane (pytest -m graph)
    py scripts/test.py --list       # show all available groups
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TESTS_DIR = REPO_ROOT / "tests"

GROUPS: dict[str, dict] = {
    "all": {
        "description": "Full pytest sweep of tests/ (all *.py including validate_*, e2e_scaffolding); excludes scripts-only CLIs unless they have tests",
        "files": [],
    },
    "api": {
        "description": "FastAPI control plane endpoints",
        "files": ["test_api.py", "test_e2e_pipeline.py"],
    },
    "security": {
        "description": "Alerts, permissions, config validation",
        "files": ["test_akos_alerts.py", "validate_configs.py"],
    },
    "runpod": {
        "description": "RunPod provider operations (mocked SDK)",
        "files": ["test_runpod_provider.py"],
    },
    "prompts": {
        "description": "Prompt structure, content, and assembly",
        "files": ["validate_prompts.py", "validate_multimodel.py"],
    },
    "models": {
        "description": "Pydantic model schemas (valid + invalid)",
        "files": ["test_akos_models.py"],
    },
    "checkpoints": {
        "description": "Workspace snapshot create/restore/list",
        "files": ["test_checkpoints.py"],
    },
    "scaffolding": {
        "description": "File tree integrity, secrets scan, SOP coverage",
        "files": ["e2e_scaffolding.py"],
    },
    "e2e": {
        "description": "Full system wiring (agents, tools, overlays)",
        "files": ["test_e2e_pipeline.py"],
    },
    "configs": {
        "description": "JSON integrity + cross-file references",
        "files": ["validate_configs.py", "validate_multimodel.py"],
    },
    "evals": {
        "description": "Eval suite manifests + rubric harness",
        "files": ["test_eval_harness.py"],
    },
    "drift": {
        "description": "Runtime drift detection (repo vs live state)",
        "files": [],
    },
    "live": {
        "description": "Live provider smoke tests (requires AKOS_LIVE_SMOKE=1)",
        "files": ["test_live_smoke.py"],
    },
    "browser": {
        "description": "Browser smoke tests (gateway + API; use --playwright for DOM checks)",
        "files": [],
    },
    "telemetry": {
        "description": "Langfuse telemetry lifecycle and trace taxonomy",
        "files": ["test_telemetry.py"],
    },
    "router": {
        "description": "FailoverRouter threshold, recovery, multi-provider routing",
        "files": ["test_router.py"],
    },
    "hlk": {
        "description": "HLK domain models, registry service, API endpoints, and process CSV SSOT helpers",
        "files": ["test_hlk.py", "test_hlk_process_csv.py"],
    },
    "graph": {
        "description": "HLK graph lane: CSV graph model, vault links, REST /hlk/graph/* (pytest -m graph). "
        "Bolt + graph: `python -m pytest -m \"graph and neo4j\"` with NEO4J_URI and NEO4J_PASSWORD set.",
        "files": [],
        "pytest_extra": ["-m", "graph"],
    },
    "validate-hlk": {
        "description": "HLK canonical vault integrity validation (standalone)",
        "files": [],
    },
    "kirbe": {
        "description": "KiRBe sync daemon dry-run helper",
        "files": ["test_kirbe_sync_daemon.py"],
    },
}


def list_groups() -> None:
    print()
    print("  Available test groups:")
    print("  " + "-" * 56)
    for name, info in GROUPS.items():
        extra = info.get("pytest_extra") or []
        suffix = f"  [pytest: {' '.join(extra)}]" if extra else ""
        print(f"  {name:16s}  {info['description']}{suffix}")
    print()
    print("  When-to-run hints:")
    print("    graph        — after touching akos/hlk_graph_model.py, hlk_vault_links, /hlk/graph/*, serve-api graph supervisor")
    print("    hlk          — after touching compliance CSVs (run validate_hlk.py before commit per PRECEDENCE)")
    print("    api          — after akos/api.py or control-plane contract changes")
    print()
    print("  Usage: py scripts/test.py <group>")
    print("         py scripts/test.py uat       (live Swagger server)")
    print()


def run_tests(group: str, extra_args: list[str]) -> int:
    info = GROUPS[group]
    files = info["files"]
    pytest_extra = list(info.get("pytest_extra") or [])

    cmd = [sys.executable, "-m", "pytest"]
    cmd.extend(pytest_extra)
    if files:
        cmd.extend([str(TESTS_DIR / f) for f in files])
    else:
        cmd.append(str(TESTS_DIR))
    cmd.extend(extra_args)

    print(f"\n  Running: {group} -- {info['description']}\n", flush=True)
    return subprocess.call(cmd, cwd=str(REPO_ROOT))


def run_uat() -> None:
    print()
    print("  Starting AKOS Control Plane for UAT...")
    print("  " + "-" * 50)
    print("  Swagger UI:   http://127.0.0.1:8420/docs")
    print("  Health check:  http://127.0.0.1:8420/health")
    print("  Agents list:   http://127.0.0.1:8420/agents")
    print()
    print("  Open the Swagger URL in your browser, then:")
    print("    1. Click any endpoint row to expand it")
    print("    2. Click 'Try it out'")
    print("    3. Click 'Execute'")
    print("    4. Verify the Server response")
    print()
    print("  Press Ctrl+C to stop.")
    print()

    cmd = [
        sys.executable, str(REPO_ROOT / "scripts" / "serve-api.py"),
        "--port", "8420",
    ]
    try:
        subprocess.call(cmd, cwd=str(REPO_ROOT))
    except KeyboardInterrupt:
        print("\n  Server stopped.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AKOS test runner -- friendly commands for all test groups",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  py scripts/test.py           # all tests\n"
               "  py scripts/test.py api       # API + E2E\n"
               "  py scripts/test.py security  # alerts + configs\n"
               "  py scripts/test.py uat       # live Swagger server\n"
               "  py scripts/test.py --list    # show all groups\n",
    )
    parser.add_argument(
        "group",
        nargs="?",
        default="all",
        help="Test group to run (default: all). Use --list to see options.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        dest="show_list",
        help="Show all available test groups",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output (passes -v to pytest)",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Minimal output (passes -q to pytest)",
    )

    args, extra = parser.parse_known_args()

    if args.show_list:
        list_groups()
        return

    if args.group == "uat":
        run_uat()
        return

    if args.group == "drift":
        print("\n  Running: drift -- Runtime drift detection\n")
        drift_script = REPO_ROOT / "scripts" / "check-drift.py"
        sys.exit(subprocess.call([sys.executable, str(drift_script)], cwd=str(REPO_ROOT)))

    if args.group == "browser":
        print("\n  Running: browser -- Browser smoke tests\n")
        browser_script = REPO_ROOT / "scripts" / "browser-smoke.py"
        browser_args = [sys.executable, str(browser_script)]
        if "--playwright" in extra:
            browser_args.append("--playwright")
        if "--headed" in extra:
            browser_args.append("--headed")
        sys.exit(subprocess.call(browser_args, cwd=str(REPO_ROOT)))

    if args.group not in GROUPS:
        print(f"\n  Unknown group: '{args.group}'")
        list_groups()
        sys.exit(1)

    extra_args = list(extra)
    if args.verbose:
        extra_args.append("-v")
    if args.quiet:
        extra_args.append("-q")
    if not any(x in extra_args for x in ["-v", "-q", "--tb"]):
        extra_args.append("-v")

    sys.exit(run_tests(args.group, extra_args))


if __name__ == "__main__":
    main()
