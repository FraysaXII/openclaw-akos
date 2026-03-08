#!/usr/bin/env python3
"""Runtime drift detection for AKOS.

Compares the repository's intended state (agent count, MCP servers,
permissions, workspace files) against the live runtime and reports
mismatches. Exit code 0 = no drift, 1 = drift detected.

Usage:
    py scripts/check-drift.py
    py scripts/check-drift.py --json
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import AGENT_WORKSPACES, REPO_ROOT, load_json, resolve_openclaw_home
from akos.log import setup_logging

logger = logging.getLogger("akos.drift")

REQUIRED_WORKSPACE_FILES = ["SOUL.md"]
EXPECTED_SCAFFOLD_FILES = ["IDENTITY.md", "MEMORY.md", "HEARTBEAT.md"]


def check_agent_workspaces(oc_home: Path) -> list[dict]:
    """Check that all 4 agent workspaces exist with required files."""
    issues: list[dict] = []
    for agent_name, ws_dir_name in AGENT_WORKSPACES.items():
        ws_path = oc_home / ws_dir_name
        if not ws_path.exists():
            issues.append({
                "type": "missing_workspace",
                "agent": agent_name,
                "expected": str(ws_path),
            })
            continue
        for required_file in REQUIRED_WORKSPACE_FILES:
            fpath = ws_path / required_file
            if not fpath.exists():
                issues.append({
                    "type": "missing_file",
                    "agent": agent_name,
                    "file": required_file,
                    "expected": str(fpath),
                })
    return issues


def check_mcp_config(oc_home: Path) -> list[dict]:
    """Check that mcporter.json exists and has expected servers."""
    issues: list[dict] = []
    mcporter_path = Path.home() / ".mcporter" / "mcporter.json"
    if not mcporter_path.exists():
        issues.append({
            "type": "missing_mcp_config",
            "expected": str(mcporter_path),
        })
        return issues

    example_path = REPO_ROOT / "config" / "mcporter.json.example"
    if not example_path.exists():
        return issues

    deployed = load_json(mcporter_path)
    expected = load_json(example_path)

    deployed_servers = set(deployed.get("mcpServers", {}).keys())
    expected_servers = set(expected.get("mcpServers", {}).keys())

    missing = expected_servers - deployed_servers
    for server in sorted(missing):
        issues.append({
            "type": "missing_mcp_server",
            "server": server,
        })
    return issues


def check_permissions(oc_home: Path) -> list[dict]:
    """Check that permissions.json exists and is valid."""
    issues: list[dict] = []
    perm_path = REPO_ROOT / "config" / "permissions.json"
    if not perm_path.exists():
        issues.append({"type": "missing_permissions_config"})
        return issues

    perms = load_json(perm_path)
    if "autonomous" not in perms or "requires_approval" not in perms:
        issues.append({
            "type": "malformed_permissions",
            "detail": "Missing 'autonomous' or 'requires_approval' keys",
        })
    return issues


def run_drift_check() -> list[dict]:
    """Run all drift checks and return combined issues."""
    oc_home = resolve_openclaw_home()
    issues: list[dict] = []
    issues.extend(check_agent_workspaces(oc_home))
    issues.extend(check_mcp_config(oc_home))
    issues.extend(check_permissions(oc_home))
    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="AKOS runtime drift detector")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--json-log", action="store_true", help="JSON logging")
    args = parser.parse_args()

    setup_logging(json_output=args.json_log)

    issues = run_drift_check()

    if args.json:
        print(json.dumps({"drift_detected": len(issues) > 0, "issues": issues}, indent=2))
    else:
        if not issues:
            print("\n  No drift detected. Runtime matches repo state.\n")
        else:
            print(f"\n  Drift detected: {len(issues)} issue(s)\n")
            for i, issue in enumerate(issues, 1):
                print(f"  {i}. [{issue['type']}] {json.dumps({k: v for k, v in issue.items() if k != 'type'})}")
            print()

    sys.exit(1 if issues else 0)


if __name__ == "__main__":
    main()
