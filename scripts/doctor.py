#!/usr/bin/env python3
"""AKOS environment health checker.

Validates that the local runtime environment has all required components
configured and accessible: gateway, workspaces, prompts, MCP config,
RunPod config, Langfuse config, and permissions.

Usage:
    py scripts/doctor.py
    py scripts/doctor.py --json-log
"""

from __future__ import annotations

import json
import logging
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import AGENT_WORKSPACES, REPO_ROOT, load_json, resolve_openclaw_home
from akos.log import setup_logging

logger = logging.getLogger("akos.doctor")

GATEWAY_URL = "http://127.0.0.1:18789"


def check_gateway() -> tuple[str, str]:
    """Check if the OpenCLAW gateway is reachable."""
    try:
        req = urllib.request.Request(GATEWAY_URL, method="GET")
        with urllib.request.urlopen(req, timeout=5):
            return "PASS", f"Gateway reachable at {GATEWAY_URL}"
    except (urllib.error.URLError, OSError):
        return "FAIL", f"Gateway not reachable at {GATEWAY_URL}"


def check_workspaces(oc_home: Path) -> list[tuple[str, str]]:
    """Check that all 4 agent workspace directories exist."""
    results: list[tuple[str, str]] = []
    for agent_name, ws_dir_name in AGENT_WORKSPACES.items():
        ws_path = oc_home / ws_dir_name
        if ws_path.is_dir():
            results.append(("PASS", f"Workspace exists: {agent_name} ({ws_path})"))
        else:
            results.append(("FAIL", f"Workspace missing: {agent_name} (expected {ws_path})"))
    return results


def check_soul_md(oc_home: Path) -> list[tuple[str, str]]:
    """Check that SOUL.md exists in each agent workspace."""
    results: list[tuple[str, str]] = []
    for agent_name, ws_dir_name in AGENT_WORKSPACES.items():
        soul_path = oc_home / ws_dir_name / "SOUL.md"
        if soul_path.is_file():
            results.append(("PASS", f"SOUL.md present: {agent_name}"))
        else:
            results.append(("WARN", f"SOUL.md missing: {agent_name} ({soul_path})"))
    return results


def check_mcporter() -> tuple[str, str]:
    """Check that mcporter.json exists."""
    mcporter_path = Path.home() / ".mcporter" / "mcporter.json"
    if mcporter_path.is_file():
        return "PASS", f"mcporter.json found at {mcporter_path}"
    return "FAIL", f"mcporter.json not found (expected {mcporter_path})"


def check_runpod_config() -> tuple[str, str]:
    """Check that RunPod GPU configuration is present."""
    gpu_config = REPO_ROOT / "config" / "gpu-runpod.json"
    if gpu_config.is_file():
        return "PASS", f"RunPod config found: {gpu_config}"
    return "WARN", "RunPod config not found: config/gpu-runpod.json (optional for local-only setups)"


def check_langfuse_config() -> tuple[str, str]:
    """Check that Langfuse env example is present."""
    langfuse_path = REPO_ROOT / "config" / "eval" / "langfuse.env.example"
    if langfuse_path.is_file():
        return "PASS", f"Langfuse config found: {langfuse_path}"
    return "WARN", "Langfuse config not found: config/eval/langfuse.env.example"


def check_permissions() -> tuple[str, str]:
    """Check that permissions.json exists and is structurally valid."""
    perm_path = REPO_ROOT / "config" / "permissions.json"
    if not perm_path.is_file():
        return "FAIL", "permissions.json not found"
    try:
        data = load_json(perm_path)
        if not isinstance(data, dict):
            return "FAIL", "permissions.json is not a JSON object"
        if "autonomous" not in data or "requires_approval" not in data:
            return "FAIL", "permissions.json missing 'autonomous' or 'requires_approval' keys"
        return "PASS", "permissions.json valid"
    except (json.JSONDecodeError, OSError) as exc:
        return "FAIL", f"permissions.json parse error: {exc}"


def run_doctor() -> list[tuple[str, str]]:
    """Run all health checks and return (level, message) pairs."""
    oc_home = resolve_openclaw_home()
    results: list[tuple[str, str]] = []

    results.append(check_gateway())
    results.extend(check_workspaces(oc_home))
    results.extend(check_soul_md(oc_home))
    results.append(check_mcporter())
    results.append(check_runpod_config())
    results.append(check_langfuse_config())
    results.append(check_permissions())

    return results


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="AKOS environment health checker")
    parser.add_argument("--json-log", action="store_true", help="JSON logging output")
    args = parser.parse_args()

    setup_logging(json_output=args.json_log)

    results = run_doctor()

    pass_count = sum(1 for level, _ in results if level == "PASS")
    fail_count = sum(1 for level, _ in results if level == "FAIL")
    warn_count = sum(1 for level, _ in results if level == "WARN")

    print()
    print("=" * 64)
    print("  AKOS Doctor -- Environment Health Check")
    print("=" * 64)
    print()
    print(f"  {'Status':<8} {'Check'}")
    print(f"  {'------':<8} {'-----'}")
    for level, message in results:
        print(f"  {level:<8} {message}")
    print()
    print("-" * 64)
    print(f"  PASS: {pass_count}  |  FAIL: {fail_count}  |  WARN: {warn_count}")
    print("-" * 64)

    if fail_count > 0:
        print("\n  Some checks FAILED. Fix the issues above and re-run.\n")
        sys.exit(1)
    else:
        print("\n  All critical checks passed.\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
