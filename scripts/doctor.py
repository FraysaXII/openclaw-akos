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
import os
import platform
import socket
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import akos.process as proc
from akos.io import (
    AGENT_WORKSPACES,
    MANAGED_OPENCLAW_PLUGIN_IDS,
    REPO_ROOT,
    load_json,
    load_runtime_env,
    resolve_openclaw_home,
    set_process_env_defaults,
)
from akos.log import setup_logging
from akos.policy import CapabilityMatrix
from akos.runtime import (
    GATEWAY_HTTP_URL,
    GatewayRecoveryResult,
    RuntimeState,
    get_gateway_status_snapshot,
    probe_gateway_http,
    probe_gateway_rpc,
    recover_gateway_service,
    resolve_openclaw_cli,
)
from akos.tools import classify_gateway_tool_id

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
        try:
            with socket.create_connection(("127.0.0.1", 18789), timeout=5):
                return "PASS", "Gateway TCP listener reachable at 127.0.0.1:18789 (HTTP probe unavailable)"
        except OSError:
            return "FAIL", f"Gateway not reachable at {GATEWAY_URL}"


def check_gateway_runtime_contract() -> list[tuple[str, str]]:
    """Normalize runtime semantics from openclaw gateway status output."""
    checks: list[tuple[str, str]] = []
    samples: list[RuntimeState] = []
    cli = resolve_openclaw_cli()
    if not cli:
        checks.append(("WARN", "gateway status probe unavailable: openclaw CLI not found in PATH"))
        return checks

    for _ in range(3):
        http_ok = probe_gateway_http()
        rpc_ok = probe_gateway_rpc(cli)
        snapshot = get_gateway_status_snapshot(cli)

        if http_ok and rpc_ok:
            samples.append("healthy")
            checks.append((
                "PASS",
                "Gateway runtime healthy via direct HTTP + RPC probes"
                + (
                    f" (raw={snapshot.raw_runtime}, rpc_probe={snapshot.rpc_probe}, listening={snapshot.listening})"
                    if snapshot is not None
                    else " (status probe unavailable)"
                ),
            ))
            continue

        if snapshot is None:
            checks.append((
                "WARN",
                "Gateway status probe unavailable and direct HTTP/RPC probes are not healthy",
            ))
            return checks

        samples.append(snapshot.normalized_runtime)
        if snapshot.normalized_runtime == "unknown":
            checks.append((
                "WARN",
                "Gateway runtime remains unknown "
                f"(raw={snapshot.raw_runtime}, rpc_probe={snapshot.rpc_probe}, listening={snapshot.listening})",
            ))
        elif snapshot.normalized_runtime == "healthy":
            checks.append((
                "PASS",
                "Gateway runtime normalized to healthy "
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


def check_gateway_rpc_health() -> tuple[str, str]:
    """Check the gateway RPC plane directly via ``gateway call health``."""
    cli = resolve_openclaw_cli()
    if not cli:
        return "WARN", "gateway RPC health probe unavailable: openclaw CLI not found in PATH"
    if probe_gateway_rpc(cli):
        return "PASS", "Gateway RPC health reachable via `openclaw gateway call health`"
    return "WARN", "Gateway RPC health probe failed"


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


def check_managed_openclaw_plugins(oc_home: Path) -> list[tuple[str, str]]:
    """Verify repo-managed OpenClaw plugins are enabled and deployed."""
    results: list[tuple[str, str]] = []
    oc_config = oc_home / "openclaw.json"
    if not oc_config.is_file():
        results.append(("WARN", "openclaw.json not found; skipping plugin deployment checks"))
        return results

    try:
        live = load_json(oc_config)
    except (json.JSONDecodeError, OSError):
        results.append(("FAIL", "openclaw.json unreadable or invalid JSON"))
        return results

    plugins_cfg = live.get("plugins", {})
    plugin_entries = plugins_cfg.get("entries", {})
    plugin_allow = plugins_cfg.get("allow", [])
    if not isinstance(plugin_entries, dict):
        results.append(("FAIL", "plugins.entries must be an object in openclaw.json"))
        return results

    source_root = REPO_ROOT / "openclaw-plugins"
    deployed_root = oc_home / "extensions"

    for plugin_id in MANAGED_OPENCLAW_PLUGIN_IDS:
        if isinstance(plugin_allow, list) and plugin_id in plugin_allow:
            results.append(("PASS", f"Managed OpenClaw plugin trusted via plugins.allow: {plugin_id}"))
        else:
            results.append(("FAIL", f"Managed OpenClaw plugin missing from plugins.allow: {plugin_id}"))

        entry = plugin_entries.get(plugin_id, {})
        if isinstance(entry, dict) and entry.get("enabled") is True:
            results.append(("PASS", f"Managed OpenClaw plugin enabled: {plugin_id}"))
        else:
            results.append(("FAIL", f"Managed OpenClaw plugin disabled or missing in config: {plugin_id}"))

        source_dir = source_root / plugin_id
        target_dir = deployed_root / plugin_id
        if not source_dir.is_dir():
            results.append(("FAIL", f"Repo-managed OpenClaw plugin source missing: {source_dir}"))
            continue
        if not target_dir.is_dir():
            results.append(("FAIL", f"Managed OpenClaw plugin not deployed: {target_dir}"))
            continue

        missing: list[str] = []
        drifted: list[str] = []
        for src_path in sorted(source_dir.rglob("*")):
            if not src_path.is_file():
                continue
            rel_path = src_path.relative_to(source_dir)
            dest_path = target_dir / rel_path
            if not dest_path.exists():
                missing.append(rel_path.as_posix())
                continue
            if dest_path.read_bytes() != src_path.read_bytes():
                drifted.append(rel_path.as_posix())

        if missing or drifted:
            details = []
            if missing:
                details.append(f"missing: {', '.join(missing)}")
            if drifted:
                details.append(f"drifted: {', '.join(drifted)}")
            results.append(("FAIL", f"Managed OpenClaw plugin out of sync: {plugin_id} ({'; '.join(details)})"))
        else:
            results.append(("PASS", f"Managed OpenClaw plugin synced: {plugin_id}"))

    return results


def _runtime_env_value(key: str, oc_home: Path) -> str:
    """Read a runtime env var from process env first, then ~/.openclaw/.env."""
    value = os.environ.get(key, "")
    if value:
        return value
    env_path = oc_home / ".env"
    if env_path.is_file():
        from akos.io import load_env_file

        return load_env_file(env_path).get(key, "")
    return ""


def check_ollama_readiness(oc_home: Path) -> list[tuple[str, str]]:
    """Check local Ollama availability when the active model uses ollama."""
    results: list[tuple[str, str]] = []
    oc_config = oc_home / "openclaw.json"
    if not oc_config.is_file():
        return results
    try:
        cfg = load_json(oc_config)
    except (json.JSONDecodeError, OSError):
        return [("WARN", "Ollama readiness skipped: openclaw.json unreadable")]

    primary = (
        cfg.get("agents", {})
        .get("defaults", {})
        .get("model", {})
        .get("primary", "")
    )
    if not isinstance(primary, str) or not primary.startswith("ollama/"):
        return results

    try:
        req = urllib.request.Request("http://127.0.0.1:11434/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=5):
            return [("PASS", "Local Ollama reachable at http://127.0.0.1:11434")]
    except (urllib.error.URLError, OSError):
        return [(
            "WARN",
            "Local Ollama not reachable at http://127.0.0.1:11434 "
            "(the gateway may still run if it already knows the configured model, "
            "but provider discovery and local inference can degrade)",
        )]


def check_runpod_readiness() -> list[tuple[str, str]]:
    """Check RunPod/vLLM readiness: API key, endpoint, or direct pod health."""
    results: list[tuple[str, str]] = []
    oc_home = resolve_openclaw_home()

    gpu_config = REPO_ROOT / "config" / "environments" / "gpu-runpod.json"
    pod_config = REPO_ROOT / "config" / "environments" / "gpu-runpod-pod.json"
    if gpu_config.is_file():
        results.append(("PASS", f"RunPod serverless config: {gpu_config.name}"))
    if pod_config.is_file():
        results.append(("PASS", f"RunPod dedicated pod config: {pod_config.name}"))
    if not gpu_config.is_file() and not pod_config.is_file():
        results.append(("WARN", "No RunPod config found (optional for local-only)"))
        return results

    api_key = _runtime_env_value("RUNPOD_API_KEY", oc_home)
    if api_key and api_key != "YOUR_RUNPOD_API_KEY":
        results.append(("PASS", "RUNPOD_API_KEY is set"))
    else:
        results.append(("SKIP", "RUNPOD_API_KEY not set (required for serverless only)"))

    vllm_url = _runtime_env_value("VLLM_RUNPOD_URL", oc_home)
    placeholder_urls = {
        "http://YOUR_POD_IP:8000/v1",
        "http://localhost:8000/v1",
    }
    if vllm_url and vllm_url not in placeholder_urls:
        from akos.runpod_provider import RunPodProvider
        probe = RunPodProvider.probe_vllm_health(vllm_url, timeout=5.0)
        if probe.healthy:
            results.append(("PASS", f"vLLM endpoint healthy: {vllm_url}"))
        else:
            results.append(("FAIL", f"vLLM endpoint unreachable: {vllm_url}"))
    else:
        results.append(("SKIP", "VLLM_RUNPOD_URL not set (set after pod/endpoint setup)"))

    return results


def check_langfuse_readiness() -> list[tuple[str, str]]:
    """Check Langfuse credentials and connectivity."""
    import os
    results: list[tuple[str, str]] = []

    legacy_example = REPO_ROOT / "config" / "eval" / "langfuse.env.example"
    legacy_real = REPO_ROOT / "config" / "eval" / "langfuse.env"
    if legacy_example.exists() or legacy_real.exists():
        results.append((
            "FAIL",
            "Legacy Langfuse env files detected under config/eval/. "
            "Langfuse secrets must live in ~/.openclaw/.env and non-secret settings in openclaw diagnostics.",
        ))
        return results

    pub = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
    sec = os.environ.get("LANGFUSE_SECRET_KEY", "")
    host = os.environ.get("LANGFUSE_HOST", "")
    if not pub or pub.startswith("your-") or not sec or sec.startswith("your-"):
        env = load_runtime_env(resolve_openclaw_home())
        set_process_env_defaults(env)
        pub = env.get("LANGFUSE_PUBLIC_KEY", pub)
        sec = env.get("LANGFUSE_SECRET_KEY", sec)
        host = env.get("LANGFUSE_HOST", host)

    if pub and not pub.startswith("your-") and sec and not sec.startswith("your-"):
        results.append(("PASS", "Langfuse credentials configured"))
        if host:
            results.append(("PASS", f"Langfuse host configured: {host}"))
        from akos.telemetry import LangfuseReporter
        reporter = LangfuseReporter(environment="doctor-probe")
        if reporter.enabled:
            results.append(("PASS", "Langfuse SDK initialized successfully"))
        else:
            results.append(("WARN", "Langfuse SDK failed to initialize (check host/keys)"))
    else:
        results.append(("SKIP", "Langfuse credentials not set (optional, telemetry disabled)"))

    return results


def check_windows_docker_hints() -> list[tuple[str, str]]:
    """Non-fatal hints for Path B on Windows (Docker Desktop / WSL2)."""
    if platform.system().lower() != "windows":
        return []

    out: list[tuple[str, str]] = []
    dv = proc.run(["docker", "--version"], timeout=10, capture=True, check=False)
    if dv.success and dv.stdout.strip():
        line = dv.stdout.strip().splitlines()[0]
        out.append(("WARN", f"Windows: Docker CLI present ({line[:120]})"))
    else:
        out.append((
            "WARN",
            "Windows: Docker CLI not found. For strict sandbox + exec per SSOT, install Docker Desktop 4.58+ "
            "and/or use WSL2 for the gateway (see USER_GUIDE strict sandbox on Windows).",
        ))

    wsl = proc.run(["wsl", "--status"], timeout=12, capture=True, check=False)
    if wsl.success:
        out.append(("WARN", "Windows: WSL reported healthy (optional Linux gateway path)"))
    else:
        out.append((
            "WARN",
            "Windows: WSL not detected or not healthy. Consider `wsl --install` for a Linux OpenClaw gateway.",
        ))

    return out


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


def _resolve_runtime_profile(policy) -> str:
    """Resolve the gateway runtime profile for a role policy."""
    if getattr(policy, "runtime_profile", None):
        return str(policy.runtime_profile)
    return _categories_to_profile(policy.allowed_categories)


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
            expected_profile = _resolve_runtime_profile(policy)
            tools_block = agent.get("tools") or {}
            actual_profile = tools_block.get("profile")
            if actual_profile == expected_profile:
                results.append(("PASS", f"Tool profile aligned: {agent_id} ({expected_profile})"))
            else:
                results.append(("FAIL", f"Tool profile mismatch: {agent_id} (expected {expected_profile}, got {actual_profile})"))

            if "allow" in tools_block:
                results.append(("FAIL", f"Legacy tools.allow detected for {agent_id}; use alsoAllow"))

            also_allow = tools_block.get("alsoAllow", [])
            if also_allow and not isinstance(also_allow, list):
                results.append(("FAIL", f"tools.alsoAllow must be a list for {agent_id}"))
            elif isinstance(also_allow, list):
                unknown = sorted(
                    str(tool) for tool in also_allow
                    if classify_gateway_tool_id(str(tool)) == "unknown"
                )
                if unknown:
                    results.append(("FAIL", f"Unknown tool IDs in {agent_id}.tools.alsoAllow: {', '.join(unknown)}"))
                else:
                    results.append(("PASS", f"Tool IDs recognized for {agent_id}.tools.alsoAllow"))

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
    results.append(check_gateway_rpc_health())
    results.extend(check_gateway_runtime_contract())
    results.extend(check_sensitive_key_signals(oc_home))
    results.extend(check_workspaces(oc_home))
    results.extend(check_soul_md(oc_home))
    results.append(check_mcporter())
    results.extend(check_managed_openclaw_plugins(oc_home))
    results.extend(check_ollama_readiness(oc_home))
    results.extend(check_gateway_tool_config(oc_home))
    results.extend(check_runpod_readiness())
    results.extend(check_langfuse_readiness())
    results.append(check_permissions())
    results.extend(check_windows_docker_hints())

    return results


def _print_gateway_recovery_failed_hints(recovery: GatewayRecoveryResult) -> None:
    """Operator hints when upstream repair/start did not yield HTTP+RPC health."""
    print()
    print("  Gateway repair - last probe state:")
    print(f"    HTTP GET {GATEWAY_HTTP_URL}: {'reachable' if recovery.http_ready else 'not reachable'}")
    print(f"    RPC (`openclaw gateway call health`): {'ok' if recovery.rpc_ready else 'failed (non-zero exit)'}")
    if recovery.cli_path:
        print(f"    OpenClaw CLI: {recovery.cli_path}")
    print()
    print("  Typical causes (upstream OpenClaw / Node, not AKOS Python):")
    print("    - Gateway process exits on config/env error - run: openclaw gateway logs")
    print("    - Port 18789 still owned by a stale Node process - Windows: netstat -ano | findstr :18789")
    print("    - Scheduled-task gateway not running - try: openclaw dashboard  or  openclaw gateway start")
    print("    - Re-onboard if install is broken: openclaw onboard --install-daemon")
    print("  See docs/USER_GUIDE.md (OpenClaw gateway / port 18789) and docs/uat/rollback_guide.md if needed.")
    print()
    if recovery.recovery_hints:
        print("  AKOS gateway recovery hints (from status + RPC + optional log tail):")
        for line in recovery.recovery_hints.splitlines():
            print(f"    {line}")
        print()


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="AKOS environment health checker")
    parser.add_argument("--json-log", action="store_true", help="JSON logging output")
    parser.add_argument(
        "--repair-gateway",
        action="store_true",
        help="Attempt upstream OpenClaw gateway repair/start before running checks",
    )
    parser.add_argument(
        "--force-gateway-repair",
        action="store_true",
        help="Pass aggressive repair mode to upstream OpenClaw doctor when repairing the gateway",
    )
    args = parser.parse_args()

    setup_logging(json_output=args.json_log)

    preflight: list[tuple[str, str]] = []
    recovery: GatewayRecoveryResult | None = None
    if args.repair_gateway:
        recovery = recover_gateway_service(repair=True, force=args.force_gateway_repair)
        if recovery.success:
            preflight.append(("PASS", recovery.detail))
        else:
            preflight.append(("FAIL", recovery.detail))

    results = run_doctor()
    results = preflight + results

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
        if recovery is not None and not recovery.success:
            _print_gateway_recovery_failed_hints(recovery)
        print("\n  Some checks FAILED. Fix the issues above and re-run.\n")
        sys.exit(1)
    else:
        print("\n  All critical checks passed.\n")
        print("  Next: py scripts/serve-api.py   # control plane; auto graph explorer when Neo4j env is real")
        print("        (CI / headless: --no-graph-explorer or AKOS_GRAPH_EXPLORER=0)\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
