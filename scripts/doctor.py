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
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import akos.process as proc
from akos.io import AGENT_WORKSPACES, REPO_ROOT, load_json, resolve_openclaw_home
from akos.log import setup_logging
from akos.policy import CapabilityMatrix
from akos.runtime import RuntimeState, parse_gateway_status_output

logger = logging.getLogger("akos.doctor")

GATEWAY_URL = "http://127.0.0.1:18789"
CAPABILITIES_PATH = REPO_ROOT / "config" / "agent-capabilities.json"
RESTRICTED_EXEC_ROLES = {"orchestrator", "architect"}
SENSITIVE_KEY_NAMES = {
    "apikey",
    "api_key",
    "token",
    "authtoken",
    "accesstoken",
    "refreshtoken",
    "idtoken",
    "secret",
    "password",
}
KNOWN_RUNTIME_MANAGED_TOKEN_PATHS = {
    "gateway.auth.token",
    "gateway.remote.token",
}


def check_gateway() -> tuple[str, str]:
    """Check if the OpenCLAW gateway is reachable."""
    try:
        req = urllib.request.Request(GATEWAY_URL, method="GET")
        with urllib.request.urlopen(req, timeout=5):
            return "PASS", f"Gateway reachable at {GATEWAY_URL}"
    except (urllib.error.URLError, OSError):
        return "FAIL", f"Gateway not reachable at {GATEWAY_URL}"


def check_gateway_runtime_contract() -> list[tuple[str, str]]:
    """Normalize runtime semantics from openclaw gateway status output."""
    checks: list[tuple[str, str]] = []
    samples: list[RuntimeState] = []
    cli = _resolve_openclaw_cli()
    if not cli:
        checks.append(("WARN", "gateway status probe unavailable: openclaw CLI not found in PATH"))
        return checks

    for _ in range(3):
        result = proc.run([cli, "gateway", "status"], timeout=20)
        if not result.success:
            detail = result.stderr.strip() or f"exit {result.returncode}"
            checks.append(("WARN", f"gateway status probe unavailable: {detail}"))
            return checks

        snapshot = parse_gateway_status_output(result.stdout)
        samples.append(snapshot.normalized_runtime)

        if snapshot.normalized_runtime == "healthy":
            checks.append((
                "PASS",
                "Gateway runtime normalized to healthy "
                f"(raw={snapshot.raw_runtime}, rpc_probe={snapshot.rpc_probe}, listening={snapshot.listening})",
            ))
        elif snapshot.normalized_runtime == "unknown":
            checks.append((
                "WARN",
                "Gateway runtime remains unknown "
                f"(raw={snapshot.raw_runtime}, rpc_probe={snapshot.rpc_probe}, listening={snapshot.listening})",
            ))
        else:
            checks.append((
                "FAIL",
                "Gateway runtime degraded "
                f"(raw={snapshot.raw_runtime}, rpc_probe={snapshot.rpc_probe}, listening={snapshot.listening})",
            ))

    first = samples[0]
    if all(state == first for state in samples):
        checks.append(("PASS", f"Runtime status deterministic across repeated probes ({first})"))
    else:
        checks.append(("FAIL", f"Runtime status non-deterministic across probes ({samples})"))

    return checks


def _resolve_openclaw_cli() -> str | None:
    """Resolve OpenClaw executable across OS-specific wrappers."""
    for candidate in ("openclaw", "openclaw.cmd", "openclaw.exe"):
        found = shutil.which(candidate)
        if found:
            return found
    return None


def _iter_sensitive_paths(obj: object, prefix: str = "") -> list[tuple[str, object]]:
    """Collect key-paths that look sensitive without exposing values."""
    hits: list[tuple[str, object]] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            path = f"{prefix}.{key}" if prefix else key
            key_l = "".join(ch for ch in key.lower() if ch.isalnum() or ch == "_")
            if key_l in SENSITIVE_KEY_NAMES:
                hits.append((path, value))
            hits.extend(_iter_sensitive_paths(value, path))
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            hits.extend(_iter_sensitive_paths(item, f"{prefix}[{idx}]"))
    return hits


def _is_env_backed(value: object) -> bool:
    if isinstance(value, str):
        return "${" in value or value.startswith("$import:")
    if isinstance(value, dict):
        source = value.get("source")
        key_id = value.get("id")
        return source == "env" and isinstance(key_id, str) and len(key_id) > 0
    return False


def check_sensitive_key_signals(oc_home: Path) -> list[tuple[str, str]]:
    """Classify sensitive-key schema signals as informational vs actionable."""
    checks: list[tuple[str, str]] = []
    oc_config = oc_home / "openclaw.json"
    if not oc_config.is_file():
        return [("WARN", "Sensitive-key scan skipped: openclaw.json not found")]

    try:
        config = load_json(oc_config)
    except (json.JSONDecodeError, OSError):
        return [("FAIL", "Sensitive-key scan failed: openclaw.json unreadable or invalid JSON")]

    sensitive_paths = _iter_sensitive_paths(config)
    if not sensitive_paths:
        return [("PASS", "Sensitive-key scan: no sensitive key-paths detected")]

    for path, value in sensitive_paths:
        if path in KNOWN_RUNTIME_MANAGED_TOKEN_PATHS:
            checks.append((
                "PASS",
                f"[config/schema] info: runtime-managed sensitive key-path detected ({path})",
            ))
        elif _is_env_backed(value):
            checks.append(("PASS", f"[config/schema] info: env-backed sensitive key-path detected ({path})"))
        else:
            checks.append((
                "WARN",
                "[config/schema] action: sensitive key-path is not env-backed "
                f"({path}); move to env reference or secret manager",
            ))
    return checks


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


def _categories_to_profile(allowed_categories: list[str]) -> str:
    """Map AKOS allowed_categories to OpenClaw profile name."""
    if "write" in allowed_categories or "shell" in allowed_categories or "shell_limited" in allowed_categories:
        return "coding"
    return "minimal"


def check_gateway_tool_config(oc_home: Path) -> list[tuple[str, str]]:
    """Check tool profiles, exec security, loop detection, browser SSRF policy."""
    results: list[tuple[str, str]] = []
    oc_config = oc_home / "openclaw.json"
    if not oc_config.is_file():
        results.append(("WARN", "openclaw.json not found; run bootstrap first"))
        return results

    try:
        live = load_json(oc_config)
    except (json.JSONDecodeError, OSError):
        results.append(("FAIL", "openclaw.json unreadable or invalid JSON"))
        return results

    agents = live.get("agents", {}).get("list", [])
    tools_cfg = live.get("tools", {})
    browser_cfg = live.get("browser", {})

    if CAPABILITIES_PATH.exists():
        matrix = CapabilityMatrix.load(CAPABILITIES_PATH)
        for agent in agents:
            agent_id = agent.get("id", "")
            policy = matrix.get_policy(agent_id)
            if not policy:
                continue
            expected_profile = _categories_to_profile(policy.allowed_categories)
            tools_block = agent.get("tools") or {}
            actual_profile = tools_block.get("profile")
            if actual_profile == expected_profile:
                results.append(("PASS", f"Tool profile aligned: {agent_id} ({expected_profile})"))
            else:
                results.append(("FAIL", f"Tool profile mismatch: {agent_id} (expected {expected_profile}, got {actual_profile})"))

        for agent in agents:
            agent_id = agent.get("id", "").lower()
            if agent_id in RESTRICTED_EXEC_ROLES:
                exec_cfg = tools_cfg.get("exec") or {}
                security = exec_cfg.get("security", "")
                if security != "full":
                    results.append(("PASS", f"Exec security OK: {agent_id} ({security})"))
                else:
                    results.append(("FAIL", f"Exec security too permissive for {agent_id}: must not be 'full'"))
    else:
        results.append(("WARN", "agent-capabilities.json not found; skipping tool profile checks"))

    if tools_cfg.get("loopDetection", {}).get("enabled", True):
        results.append(("PASS", "Loop detection enabled"))
    else:
        results.append(("FAIL", "Loop detection disabled (tools.loopDetection.enabled should be true)"))

    ssrf = browser_cfg.get("ssrfPolicy", {})
    if ssrf.get("dangerouslyAllowPrivateNetwork") is True:
        results.append(("FAIL", "Browser SSRF policy allows private network (dangerouslyAllowPrivateNetwork is true)"))
    else:
        results.append(("PASS", "Browser SSRF policy restricts private network"))

    return results


def run_doctor() -> list[tuple[str, str]]:
    """Run all health checks and return (level, message) pairs."""
    oc_home = resolve_openclaw_home()
    results: list[tuple[str, str]] = []

    results.append(check_gateway())
    results.extend(check_gateway_runtime_contract())
    results.extend(check_sensitive_key_signals(oc_home))
    results.extend(check_workspaces(oc_home))
    results.extend(check_soul_md(oc_home))
    results.append(check_mcporter())
    results.extend(check_gateway_tool_config(oc_home))
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
