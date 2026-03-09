"""Runtime status normalization for OpenClaw gateway diagnostics."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

RuntimeState = Literal["healthy", "degraded", "unknown"]


@dataclass(frozen=True)
class GatewayStatusSnapshot:
    """Normalized view of ``openclaw gateway status`` output."""

    raw_runtime: str
    rpc_probe: str
    listening: str
    normalized_runtime: RuntimeState


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
