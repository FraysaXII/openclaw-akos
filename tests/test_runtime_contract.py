from types import SimpleNamespace

import akos.runtime as runtime
from akos.runtime import (
    parse_gateway_status_output,
    parse_windows_netstat_listening_pids,
)


def test_normalizes_unknown_to_healthy_when_probe_and_listener_are_healthy() -> None:
    output = """
Runtime: unknown
RPC probe: ok
Listening: 127.0.0.1:18789
"""
    snap = parse_gateway_status_output(output)
    assert snap.raw_runtime == "unknown"
    assert snap.rpc_probe == "ok"
    assert snap.normalized_runtime == "healthy"


def test_keeps_unknown_without_healthy_probe_evidence() -> None:
    output = """
Runtime: unknown
RPC probe: unreachable
Listening: not listening
"""
    snap = parse_gateway_status_output(output)
    assert snap.normalized_runtime == "unknown"


def test_marks_non_unknown_with_bad_probe_as_degraded() -> None:
    output = """
Runtime: running
RPC probe: timeout
Listening: not listening
"""
    snap = parse_gateway_status_output(output)
    assert snap.normalized_runtime == "degraded"


def test_resolve_openclaw_cli_prefers_windows_shim(monkeypatch) -> None:
    mapping = {
        "openclaw": None,
        "openclaw.cmd": r"C:\Users\Shadow\AppData\Roaming\npm\openclaw.cmd",
        "openclaw.exe": None,
    }
    monkeypatch.setattr(runtime.shutil, "which", lambda name: mapping.get(name))

    assert runtime.resolve_openclaw_cli() == mapping["openclaw.cmd"]


def test_recover_gateway_service_succeeds_with_http_and_rpc(monkeypatch) -> None:
    calls: list[list[str]] = []

    def fake_run(args, *, timeout=120, capture=True, check=False):
        calls.append(args)
        return SimpleNamespace(success=True, stdout="", stderr="", returncode=0)

    monkeypatch.setattr(runtime, "resolve_openclaw_cli", lambda: "openclaw.cmd")
    monkeypatch.setattr(runtime.proc, "run", fake_run)
    monkeypatch.setattr(runtime, "probe_gateway_http", lambda *_, **__: True)
    monkeypatch.setattr(runtime, "probe_gateway_rpc", lambda *_, **__: True)
    monkeypatch.setattr(
        runtime,
        "get_gateway_status_snapshot",
        lambda *_, **__: runtime.GatewayStatusSnapshot(
            raw_runtime="unknown",
            rpc_probe="ok",
            listening="127.0.0.1:18789",
            normalized_runtime="healthy",
        ),
    )

    result = runtime.recover_gateway_service(repair=True)

    assert result.success is True
    assert calls[0][:2] == ["openclaw.cmd", "doctor"]
    assert any(cmd[:3] == ["openclaw.cmd", "gateway", "start"] for cmd in calls)


def test_recover_gateway_service_fails_without_cli(monkeypatch) -> None:
    monkeypatch.setattr(runtime, "resolve_openclaw_cli", lambda: None)
    result = runtime.recover_gateway_service(repair=True)

    assert result.success is False
    assert "CLI not found" in result.detail


def test_parse_windows_netstat_listening_pids_finds_port() -> None:
    sample = """
  TCP    127.0.0.1:18789       0.0.0.0:0              LISTENING       5264
  TCP    0.0.0.0:135           0.0.0.0:0              LISTENING       1236
"""
    assert parse_windows_netstat_listening_pids(sample, 18789) == [5264]


def test_parse_windows_netstat_listening_pids_ignores_similar_port() -> None:
    sample = """
  TCP    0.0.0.0:187890        0.0.0.0:0              LISTENING       99
"""
    assert parse_windows_netstat_listening_pids(sample, 18789) == []


def test_parse_windows_netstat_listening_pids_dedupes() -> None:
    sample = """
  TCP    127.0.0.1:18789       0.0.0.0:0              LISTENING       42
  TCP    [::1]:18789           [::]:0                 LISTENING       42
"""
    assert parse_windows_netstat_listening_pids(sample, 18789) == [42]
