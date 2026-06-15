"""Tests for OpenClaw operator-local config normalization."""

from __future__ import annotations

from akos.openclaw_config import normalize_openclaw_config_dict


def test_maps_legacy_strict_sandbox_mode_to_all() -> None:
    cfg = {"agents": {"defaults": {"sandbox": {"mode": "strict"}}}, "tools": {"exec": {"host": "sandbox"}}}
    out, notes = normalize_openclaw_config_dict(cfg)
    assert out["agents"]["defaults"]["sandbox"]["mode"] == "all"
    assert any("strict" in n for n in notes)


def test_sandbox_off_forces_exec_host_gateway() -> None:
    cfg = {"agents": {"defaults": {"sandbox": {"mode": "off"}}}, "tools": {"exec": {"host": "sandbox"}}}
    out, notes = normalize_openclaw_config_dict(cfg)
    assert out["tools"]["exec"]["host"] == "gateway"
    assert notes


def test_invalid_sandbox_mode_falls_back_to_off(monkeypatch) -> None:
    monkeypatch.setattr(
        "akos.openclaw_config.probe_docker_engine",
        lambda **_: (False, "no docker"),
    )
    cfg = {"agents": {"defaults": {"sandbox": {"mode": "bogus"}}}, "tools": {"exec": {"host": "node"}}}
    out, notes = normalize_openclaw_config_dict(cfg)
    assert out["agents"]["defaults"]["sandbox"]["mode"] == "off"
    assert out["tools"]["exec"]["host"] == "gateway"
    assert notes
