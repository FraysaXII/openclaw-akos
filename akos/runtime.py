"""Runtime status normalization for OpenClaw gateway diagnostics."""

from __future__ import annotations

import logging
import os
import re
import shutil
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Literal

import akos.process as proc

logger = logging.getLogger("akos.runtime")

RuntimeState = Literal["healthy", "degraded", "unknown"]
GATEWAY_HTTP_URL = "http://127.0.0.1:18789"
GATEWAY_LISTEN_PORT = 18789


def parse_windows_netstat_listening_pids(stdout: str, port: int) -> list[int]:
    """Return unique PIDs that have a TCP listener on ``port`` (Windows ``netstat -ano`` output).

    Parses the standard English locale table where the last column is PID and
    ``LISTENING`` appears on the line. Used to clear orphan Node gateways that
    survived ``gateway stop`` and still hold port 18789.
    """
    if port <= 0 or port > 65535:
        return []
    # Avoid matching :18789 inside :187890 — require no trailing digit on the port.
    port_token = re.compile(rf":{port}(?!\d)(?:\s|$)")
    pids: set[int] = set()
    for raw in stdout.splitlines():
        line = raw.strip()
        if "LISTENING" not in line:
            continue
        if not port_token.search(line):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        try:
            pid = int(parts[-1])
        except ValueError:
            continue
        if pid > 0:
            pids.add(pid)
    return sorted(pids)


def windows_release_stale_gateway_listeners(port: int = GATEWAY_LISTEN_PORT) -> list[int]:
    """On Windows, terminate processes listening on TCP ``port`` (orphan gateways).

    Returns PIDs successfully targeted by ``taskkill``. No-op on non-Windows.
    """
    if os.name != "nt":
        return []
    result = proc.run(["cmd", "/c", "netstat -ano"], timeout=45)
    if not result.success:
        logger.warning("netstat failed; cannot auto-release port %s: %s", port, result.stderr)
        return []
    pids = parse_windows_netstat_listening_pids(result.stdout, port)
    killed: list[int] = []
    for pid in pids:
        tk = proc.run(["taskkill", "/F", "/PID", str(pid)], timeout=45)
        if tk.success:
            killed.append(pid)
            logger.warning("Released stale listener PID %s on port %s", pid, port)
    return killed


@dataclass(frozen=True)
class GatewayStatusSnapshot:
    """Normalized view of ``openclaw gateway status`` output."""

    raw_runtime: str
    rpc_probe: str
    listening: str
    normalized_runtime: RuntimeState


@dataclass(frozen=True)
class GatewayRecoveryResult:
    """Outcome of an automated gateway repair/start attempt."""

    success: bool
    detail: str
    http_ready: bool = False
    rpc_ready: bool = False
    cli_path: str | None = None
    status: GatewayStatusSnapshot | None = None


def parse_gateway_status_output(output: str) -> GatewayStatusSnapshot:
    """Parse and normalize gateway status output from OpenClaw CLI.

    Rules:
    - If RPC probe is ``ok`` and a listening socket is present, runtime is ``healthy``.
    - If raw runtime is ``unknown`` without healthy probe/listener evidence, remain ``unknown``.
    - Any explicit non-healthy probe/listener combination is ``degraded``.
    """

    runtime_match = re.search(r"^Runtime:\s*(.+)$", output, flags=re.MULTILINE)
    rpc_match = re.search(r"^RPC probe:\s*(.+)$", output, flags=re.MULTILINE)
    listen_match = re.search(r"^Listening:\s*(.+)$", output, flags=re.MULTILINE)

    raw_runtime = (runtime_match.group(1).strip() if runtime_match else "").lower()
    rpc_probe = (rpc_match.group(1).strip() if rpc_match else "").lower()
    listening = listen_match.group(1).strip() if listen_match else ""

    rpc_ok = rpc_probe == "ok"
    has_listener = bool(listening and listening.lower() != "not listening")

    if rpc_ok and has_listener:
        normalized_runtime: RuntimeState = "healthy"
    elif raw_runtime == "unknown":
        normalized_runtime = "unknown"
    else:
        normalized_runtime = "degraded"

    return GatewayStatusSnapshot(
        raw_runtime=raw_runtime or "unknown",
        rpc_probe=rpc_probe or "unknown",
        listening=listening or "unknown",
        normalized_runtime=normalized_runtime,
    )


def resolve_openclaw_cli() -> str | None:
    """Resolve OpenClaw executable across OS-specific wrappers."""
    for candidate in ("openclaw", "openclaw.cmd", "openclaw.exe"):
        found = shutil.which(candidate)
        if found:
            return found
    return None


def probe_gateway_http(url: str = GATEWAY_HTTP_URL, *, timeout: float = 5.0) -> bool:
    """Return True when the gateway serves HTTP on the expected loopback URL."""
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout):
            return True
    except (urllib.error.URLError, OSError):
        return False


def probe_gateway_rpc(cli: str, *, timeout: int = 20) -> bool:
    """Return True when ``openclaw gateway call health`` succeeds."""
    result = proc.run([cli, "gateway", "call", "health"], timeout=timeout)
    return result.success


def get_gateway_status_snapshot(cli: str, *, timeout: int = 20) -> GatewayStatusSnapshot | None:
    """Return normalized gateway status from the OpenClaw CLI, when available."""
    result = proc.run([cli, "gateway", "status"], timeout=timeout)
    if not result.success:
        return None
    return parse_gateway_status_output(result.stdout)


def recover_gateway_service(
    *,
    repair: bool = True,
    force: bool = False,
    timeout_seconds: int = 90,
) -> GatewayRecoveryResult:
    """Attempt deterministic gateway recovery through upstream OpenClaw commands."""
    cli = resolve_openclaw_cli()
    if not cli:
        return GatewayRecoveryResult(success=False, detail="openclaw CLI not found", cli_path=None)

    if repair:
        doctor_args = [cli, "doctor", "--repair", "--yes"]
        if force:
            doctor_args.append("--force")
        proc.run(doctor_args, timeout=180)

    proc.run([cli, "gateway", "stop"], timeout=60)
    if os.name == "nt":
        windows_release_stale_gateway_listeners()

    start = proc.run([cli, "gateway", "start"], timeout=120)
    if not start.success:
        if os.name == "nt":
            windows_release_stale_gateway_listeners()
        proc.run([cli, "gateway", "restart"], timeout=120)

    deadline = time.monotonic() + timeout_seconds
    last_http = False
    last_rpc = False
    last_status: GatewayStatusSnapshot | None = None
    while time.monotonic() < deadline:
        last_http = probe_gateway_http()
        last_rpc = probe_gateway_rpc(cli)
        last_status = get_gateway_status_snapshot(cli)
        if last_http and last_rpc:
            return GatewayRecoveryResult(
                success=True,
                detail="gateway recovered via upstream doctor/start flow",
                http_ready=last_http,
                rpc_ready=last_rpc,
                cli_path=cli,
                status=last_status,
            )
        time.sleep(5)

    detail = (
        "gateway recovery did not reach healthy HTTP+RPC state "
        f"(http_ready={last_http}, rpc_ready={last_rpc})"
    )
    return GatewayRecoveryResult(
        success=False,
        detail=detail,
        http_ready=last_http,
        rpc_ready=last_rpc,
        cli_path=cli,
        status=last_status,
    )
