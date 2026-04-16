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
from pathlib import Path
from typing import Literal

import akos.process as proc

logger = logging.getLogger("akos.runtime")

RuntimeState = Literal["healthy", "degraded", "unknown"]
GATEWAY_HTTP_URL = "http://127.0.0.1:18789"
GATEWAY_LISTEN_PORT = 18789
GATEWAY_RECOVERY_INITIAL_SLEEP_SEC = 12
GATEWAY_RECOVERY_POLL_SEC = 5

_LOG_HINT_LINE = re.compile(
    r"(?i)(pricing|bootstrap|timeout|1006|abnormal|error|gateway call failed|model-pricing|model.pricing)"
)
_FILE_LOG_PATH = re.compile(r"(?im)^File\s+logs?\s*:\s*(.+)$")


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
    recovery_hints: str = ""


def _combine_cmd_text(stdout: str | None, stderr: str | None) -> str:
    parts = [p for p in ((stdout or "").strip(), (stderr or "").strip()) if p]
    return "\n".join(parts)


def extract_openclaw_file_log_path(status_stdout: str) -> str | None:
    """Return the path printed by ``openclaw gateway status`` (``File log(s):``), if any."""
    m = _FILE_LOG_PATH.search(status_stdout or "")
    if not m:
        return None
    path = m.group(1).strip().strip('"').strip("'")
    return path or None


def read_gateway_log_tail_for_diagnostics(
    path: str,
    *,
    max_bytes: int = 16000,
    max_lines: int = 48,
) -> str:
    """Read a tail of the gateway file log, returning only keyword-bearing lines (SOC: no full log dump)."""
    try:
        p = Path(path)
        if not p.is_file():
            return ""
        size = p.stat().st_size
        with p.open("rb") as f:
            if size > max_bytes:
                f.seek(-max_bytes, os.SEEK_END)
            chunk = f.read().decode("utf-8", errors="replace")
    except OSError:
        return ""
    lines = [ln.strip() for ln in chunk.splitlines() if _LOG_HINT_LINE.search(ln)]
    if len(lines) > max_lines:
        lines = lines[-max_lines:]
    return "\n".join(lines)


def build_gateway_recovery_operator_hints(
    status_stdout: str,
    rpc_detail: str,
    log_filtered_tail: str,
    *,
    http_ready: bool,
    rpc_ready: bool,
) -> str:
    """Turn status, RPC capture, and filtered log lines into a short operator-facing block."""
    corpus = "\n".join([status_stdout, rpc_detail, log_filtered_tail]).lower()
    bullets: list[str] = []

    pricing_ctx = "pricing" in corpus and (
        "bootstrap" in corpus or "model-pricing" in corpus or "model_pricing" in corpus
    )
    if pricing_ctx and ("timeout" in corpus or "aborted" in corpus):
        bullets.append(
            "AKOS diagnosis: model pricing bootstrap timed out (upstream OpenClaw). "
            "Allow outbound HTTPS from this host, stabilize network, then retry; see OpenClaw release notes "
            "or issues for offline or cached pricing options."
        )
    if "1006" in (status_stdout + rpc_detail) or "abnormal closure" in corpus:
        bullets.append(
            "AKOS diagnosis: WebSocket code 1006 (abnormal closure) usually means the gateway dropped the RPC "
            "channel during startup or exited. Inspect the gateway log path from `openclaw gateway status` for "
            "the first ERROR after `gateway start`."
        )
    if not bullets and not http_ready and not rpc_ready:
        bullets.append(
            "Neither HTTP nor RPC reached a healthy state. Confirm the gateway process stays up after "
            "`gateway start` and review upstream `openclaw gateway logs`."
        )
    elif not bullets and log_filtered_tail:
        bullets.append(
            "Keyword-filtered lines from the OpenClaw log tail are included below (paths are local operator context)."
        )

    parts: list[str] = []
    if bullets:
        parts.extend(f"- {b}" for b in bullets)
    if log_filtered_tail:
        parts.append("OpenClaw log (keyword lines, tail region):")
        parts.append(log_filtered_tail)
    return "\n".join(parts).strip()


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


def probe_gateway_rpc_detail(cli: str, *, timeout: int = 20) -> tuple[bool, str]:
    """Return success flag and a short combined stdout/stderr capture for diagnostics."""
    result = proc.run([cli, "gateway", "call", "health"], timeout=timeout)
    blob = _combine_cmd_text(result.stdout, result.stderr)
    if len(blob) > 700:
        blob = "... " + blob[-700:]
    return result.success, blob


def probe_gateway_rpc(cli: str, *, timeout: int = 20) -> bool:
    """Return True when ``openclaw gateway call health`` succeeds."""
    ok, _ = probe_gateway_rpc_detail(cli, timeout=timeout)
    return ok


def fetch_gateway_status(cli: str, *, timeout: int = 20) -> tuple[GatewayStatusSnapshot | None, str]:
    """Return normalized gateway status and raw stdout (or combined output on CLI failure)."""
    result = proc.run([cli, "gateway", "status"], timeout=timeout)
    if not result.success:
        return None, _combine_cmd_text(result.stdout, result.stderr)
    out = (result.stdout or "").strip()
    return parse_gateway_status_output(result.stdout), out


def get_gateway_status_snapshot(cli: str, *, timeout: int = 20) -> GatewayStatusSnapshot | None:
    """Return normalized gateway status from the OpenClaw CLI, when available."""
    snap, _ = fetch_gateway_status(cli, timeout=timeout)
    return snap


def recover_gateway_service(
    *,
    repair: bool = True,
    force: bool = False,
    timeout_seconds: int = 150,
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

    time.sleep(GATEWAY_RECOVERY_INITIAL_SLEEP_SEC)

    deadline = time.monotonic() + timeout_seconds
    last_http = False
    last_rpc = False
    last_status: GatewayStatusSnapshot | None = None
    last_status_stdout = ""
    last_rpc_detail = ""
    while time.monotonic() < deadline:
        last_http = probe_gateway_http()
        rpc_ok, last_rpc_detail = probe_gateway_rpc_detail(cli)
        last_rpc = rpc_ok
        snap, raw = fetch_gateway_status(cli)
        last_status = snap
        if raw:
            last_status_stdout = raw
        if last_http and last_rpc:
            return GatewayRecoveryResult(
                success=True,
                detail="gateway recovered via upstream doctor/start flow",
                http_ready=last_http,
                rpc_ready=last_rpc,
                cli_path=cli,
                status=last_status,
            )
        time.sleep(GATEWAY_RECOVERY_POLL_SEC)

    detail = (
        "gateway recovery did not reach healthy HTTP+RPC state "
        f"(http_ready={last_http}, rpc_ready={last_rpc})"
    )
    log_path = extract_openclaw_file_log_path(last_status_stdout)
    log_tail = read_gateway_log_tail_for_diagnostics(log_path) if log_path else ""
    hints = build_gateway_recovery_operator_hints(
        last_status_stdout,
        last_rpc_detail,
        log_tail,
        http_ready=last_http,
        rpc_ready=last_rpc,
    )
    return GatewayRecoveryResult(
        success=False,
        detail=detail,
        http_ready=last_http,
        rpc_ready=last_rpc,
        cli_path=cli,
        status=last_status,
        recovery_hints=hints,
    )
