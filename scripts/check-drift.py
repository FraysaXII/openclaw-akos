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

from akos.io import (
    AGENT_WORKSPACES,
    MANAGED_OPENCLAW_PLUGIN_IDS,
    REPO_ROOT,
    load_json,
    resolve_mcporter_paths,
    resolve_openclaw_home,
)
from akos.log import setup_logging
from akos.policy import CapabilityMatrix
from akos.tools import classify_gateway_tool_id

logger = logging.getLogger("akos.drift")

REQUIRED_WORKSPACE_FILES = ["SOUL.md"]
EXPECTED_SCAFFOLD_FILES = ["IDENTITY.md", "MEMORY.md", "HEARTBEAT.md"]
CAPABILITIES_PATH = REPO_ROOT / "config" / "agent-capabilities.json"
TEMPLATE_CONFIG_PATH = REPO_ROOT / "config" / "openclaw.json.example"

RESTRICTED_EXEC_ROLES = {"orchestrator", "architect"}


def check_agent_workspaces(oc_home: Path) -> list[dict]:
    """Check that all 5 agent workspaces exist with required files."""
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

    raw_example = example_path.read_text(encoding="utf-8")
    expected_resolved = resolve_mcporter_paths(raw_example).strip()
    deployed_raw = mcporter_path.read_text(encoding="utf-8")
    deployed_resolved = resolve_mcporter_paths(deployed_raw).strip()
    if expected_resolved != deployed_resolved:
        issues.append({
            "type": "mcp_config_drift",
            "detail": "Deployed mcporter.json content differs from resolved repo example",
        })
    return issues


def check_legacy_langfuse_env_files() -> list[dict]:
    """Reject reintroduction of legacy repo-local Langfuse secret files."""
    issues: list[dict] = []
    for legacy_path in [
        REPO_ROOT / "config" / "eval" / "langfuse.env",
        REPO_ROOT / "config" / "eval" / "langfuse.env.example",
    ]:
        if legacy_path.exists():
            issues.append({
                "type": "legacy_langfuse_env_present",
                "path": str(legacy_path),
            })
    return issues


def check_managed_openclaw_plugins(oc_home: Path) -> list[dict]:
    """Check that repo-managed OpenClaw plugins are deployed and enabled."""
    issues: list[dict] = []
    oc_config = oc_home / "openclaw.json"
    if not oc_config.exists():
        issues.append({
            "type": "missing_openclaw_config",
            "expected": str(oc_config),
        })
        return issues

    live = load_json(oc_config)
    plugins_cfg = live.get("plugins", {})
    plugin_entries = plugins_cfg.get("entries", {})
    plugin_allow = plugins_cfg.get("allow", [])
    if not isinstance(plugin_entries, dict):
        issues.append({
            "type": "invalid_plugin_entries",
            "detail": "plugins.entries must be an object",
        })
        return issues

    source_root = REPO_ROOT / "openclaw-plugins"
    deployed_root = oc_home / "extensions"

    for plugin_id in MANAGED_OPENCLAW_PLUGIN_IDS:
        source_dir = source_root / plugin_id
        target_dir = deployed_root / plugin_id
        entry = plugin_entries.get(plugin_id, {})

        if not isinstance(plugin_allow, list) or plugin_id not in plugin_allow:
            issues.append({
                "type": "plugin_not_trusted",
                "plugin": plugin_id,
            })

        if not isinstance(entry, dict) or entry.get("enabled") is not True:
            issues.append({
                "type": "plugin_not_enabled",
                "plugin": plugin_id,
            })

        if not source_dir.is_dir():
            issues.append({
                "type": "missing_plugin_source",
                "plugin": plugin_id,
                "expected": str(source_dir),
            })
            continue

        if not target_dir.is_dir():
            issues.append({
                "type": "missing_plugin_deploy",
                "plugin": plugin_id,
                "expected": str(target_dir),
            })
            continue

        for src_path in sorted(source_dir.rglob("*")):
            if not src_path.is_file():
                continue
            rel_path = src_path.relative_to(source_dir)
            dest_path = target_dir / rel_path
            if not dest_path.exists():
                issues.append({
                    "type": "missing_plugin_file",
                    "plugin": plugin_id,
                    "file": rel_path.as_posix(),
                    "expected": str(dest_path),
                })
                continue
            if dest_path.read_bytes() != src_path.read_bytes():
                issues.append({
                    "type": "plugin_file_drift",
                    "plugin": plugin_id,
                    "file": rel_path.as_posix(),
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


def _categories_to_profile(allowed_categories: list[str]) -> str:
    """Map AKOS allowed_categories to OpenClaw profile name."""
    if "write" in allowed_categories or "shell" in allowed_categories or "shell_limited" in allowed_categories:
        return "coding"
    return "minimal"


def _resolve_runtime_profile(policy) -> str:
    """Resolve the gateway runtime profile for a role policy."""
    if getattr(policy, "runtime_profile", None):
        return str(policy.runtime_profile)
    return _categories_to_profile(policy.allowed_categories)


def check_tool_profiles(oc_home: Path) -> list[dict]:
    """Check that per-agent tool profiles match capability matrix and gateway config is sane."""
    issues: list[dict] = []
    oc_config = oc_home / "openclaw.json"
    if not oc_config.exists():
        return issues

    live = load_json(oc_config)
    agents = live.get("agents", {}).get("list", [])
    tools_cfg = live.get("tools", {})
    expected_cfg = load_json(TEMPLATE_CONFIG_PATH) if TEMPLATE_CONFIG_PATH.exists() else {}
    expected_agents = expected_cfg.get("agents", {}).get("list", [])
    expected_by_id = {
        agent.get("id", ""): agent
        for agent in expected_agents
        if isinstance(agent, dict) and agent.get("id")
    }

    actual_agent_ids = {
        agent.get("id", "")
        for agent in agents
        if isinstance(agent, dict) and agent.get("id")
    }
    expected_agent_ids = set(expected_by_id)
    if expected_agent_ids and actual_agent_ids != expected_agent_ids:
        issues.append({
            "type": "agent_inventory_drift",
            "expected": sorted(expected_agent_ids),
            "actual": sorted(actual_agent_ids),
        })

    live_a2a_allow = (tools_cfg.get("agentToAgent") or {}).get("allow", [])
    expected_a2a_allow = (expected_cfg.get("tools", {}).get("agentToAgent") or {}).get("allow", [])
    if isinstance(live_a2a_allow, list) and isinstance(expected_a2a_allow, list):
        if set(live_a2a_allow) != set(expected_a2a_allow):
            issues.append({
                "type": "a2a_allowlist_drift",
                "expected": sorted(set(expected_a2a_allow)),
                "actual": sorted(set(live_a2a_allow)),
            })

    if not CAPABILITIES_PATH.exists():
        return issues

    matrix = CapabilityMatrix.load(CAPABILITIES_PATH)

    for agent in agents:
        agent_id = agent.get("id", "")
        policy = matrix.get_policy(agent_id)
        if not policy:
            continue

        expected_profile = _resolve_runtime_profile(policy)
        tools_block = agent.get("tools") or {}
        actual_profile = tools_block.get("profile")

        expected_agent = expected_by_id.get(agent_id, {})
        expected_tools_block = expected_agent.get("tools") if isinstance(expected_agent, dict) else None
        if isinstance(expected_tools_block, dict) and tools_block != expected_tools_block:
            issues.append({
                "type": "tool_block_drift",
                "agent": agent_id,
                "expected": expected_tools_block,
                "actual": tools_block,
            })

        if actual_profile != expected_profile:
            issues.append({
                "type": "tool_profile_mismatch",
                "agent": agent_id,
                "expected": expected_profile,
                "actual": actual_profile,
            })

        if "allow" in tools_block:
            issues.append({
                "type": "legacy_allow_key",
                "agent": agent_id,
            })

        also_allow = tools_block.get("alsoAllow", [])
        if isinstance(also_allow, list):
            unknown = sorted(
                str(tool) for tool in also_allow
                if classify_gateway_tool_id(str(tool)) == "unknown"
            )
            if unknown:
                issues.append({
                    "type": "unknown_tool_ids",
                    "agent": agent_id,
                    "tools": unknown,
                })
        elif also_allow:
            issues.append({
                "type": "invalid_also_allow_type",
                "agent": agent_id,
                "actual_type": type(also_allow).__name__,
            })

        if agent_id.lower() in RESTRICTED_EXEC_ROLES:
            exec_cfg = tools_cfg.get("exec") or {}
            security = exec_cfg.get("security", "")
            if security == "full":
                issues.append({
                    "type": "exec_security_too_permissive",
                    "agent": agent_id,
                    "detail": "Orchestrator/Architect must not have exec.security 'full'",
                })

    loop_det = tools_cfg.get("loopDetection") or {}
    if not loop_det.get("enabled", True):
        issues.append({
            "type": "loop_detection_disabled",
            "detail": "tools.loopDetection.enabled must be true",
        })

    a2a = tools_cfg.get("agentToAgent") or {}
    if not a2a.get("enabled", True):
        issues.append({
            "type": "agent_to_agent_disabled",
            "detail": "tools.agentToAgent.enabled must be true",
        })

    return issues


def run_drift_check() -> list[dict]:
    """Run all drift checks and return combined issues."""
    oc_home = resolve_openclaw_home()
    issues: list[dict] = []
    issues.extend(check_agent_workspaces(oc_home))
    issues.extend(check_mcp_config(oc_home))
    issues.extend(check_legacy_langfuse_env_files())
    issues.extend(check_managed_openclaw_plugins(oc_home))
    issues.extend(check_permissions(oc_home))
    issues.extend(check_tool_profiles(oc_home))
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
