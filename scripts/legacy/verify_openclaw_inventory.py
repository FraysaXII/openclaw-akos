#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

# --------------------------
# EDIT THIS INVENTORY
# --------------------------
EXPECTED = {
    "providers": {
        "ollama": {"model_ids": {"qwen3:8b", "llama3.1:8b", "deepseek-r1:14b", "nomic-embed-text"}},
        "ollama-gpu": {"model_ids": {"qwen3:32b"}},
        "openai": {"model_ids": set()},
        "anthropic": {"model_ids": set()},
        "vllm-runpod": {"model_ids": {"deepseek-r1-70b"}},
        "vllm-shadow": {"model_ids": {"deepseek-r1-70b"}},
    },
    # exact agent IDs expected
    "agents": {"orchestrator", "architect", "executor", "verifier", "madeira"},
    # exact A2A allowlist expected
    "a2a_allow": {"orchestrator", "architect", "executor", "verifier", "madeira"},
    # optional: expected default model string
    "default_primary_model": "ollama/deepseek-r1:14b",
}

LEGACY_KEYS_SHOULD_NOT_EXIST = [
    ("tools.agentToAgent.targetAllowlist", ["tools", "agentToAgent", "targetAllowlist"]),
    ("messages.suppressToolErrorWarnings", ["messages", "suppressToolErrorWarnings"]),
    ("session.agentToAgent.pingPongTurns", ["session", "agentToAgent", "pingPongTurns"]),
    ("session.typing", ["session", "typing"]),
]

REPO_ROOT = Path(__file__).resolve().parents[2]


def get_in(d: dict[str, Any], path: list[str]) -> tuple[bool, Any]:
    cur: Any = d
    for p in path:
        if not isinstance(cur, dict) or p not in cur:
            return False, None
        cur = cur[p]
    return True, cur


def passfail(name: str, ok: bool, detail: str = "") -> bool:
    tag = "PASS" if ok else "FAIL"
    print(f"[{tag}] {name}" + (f" :: {detail}" if detail else ""))
    return ok


def expected_default_primary_model() -> str:
    """Resolve the expected default model for the active AKOS environment.

    Provider inventory is always strict/full, but the active default model is
    environment-specific after a real `switch-model.py <env>` run.
    """
    default = str(EXPECTED["default_primary_model"])
    state_path = Path.home() / ".openclaw" / ".akos-state.json"
    if not state_path.exists():
        return default

    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except Exception:
        return default

    env_name = state.get("activeEnvironment")
    if not isinstance(env_name, str) or not env_name:
        return default

    overlay_path = REPO_ROOT / "config" / "environments" / f"{env_name}.json"
    if not overlay_path.exists():
        return default

    try:
        overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
    except Exception:
        return default

    model = (
        overlay.get("agents", {})
        .get("defaults", {})
        .get("model", {})
        .get("primary")
    )
    return model if isinstance(model, str) and model else default


def main() -> int:
    config_path = Path.home() / ".openclaw" / "openclaw.json"
    if len(sys.argv) > 1:
        config_path = Path(sys.argv[1])

    if not config_path.exists():
        print(f"[FAIL] config file missing :: {config_path}")
        return 2

    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[FAIL] invalid JSON :: {e}")
        return 2

    all_ok = True

    # 1) providers presence/exact set
    ok, providers = get_in(data, ["models", "providers"])
    all_ok &= passfail("models.providers exists", ok)
    if not ok or not isinstance(providers, dict):
        return 1

    actual_provider_ids = set(providers.keys())
    expected_provider_ids = set(EXPECTED["providers"].keys())
    missing_provider_ids = sorted(expected_provider_ids - actual_provider_ids)
    extra_provider_ids = sorted(actual_provider_ids - expected_provider_ids)
    all_ok &= passfail(
        "provider IDs exact match",
        actual_provider_ids == expected_provider_ids,
        (
            f"expected={sorted(expected_provider_ids)} actual={sorted(actual_provider_ids)} "
            f"missing={missing_provider_ids} extra={extra_provider_ids}"
        ),
    )

    # 2) model ID inventory per provider + required model fields
    required_model_fields = {"id", "name", "reasoning", "input", "contextWindow", "maxTokens", "cost"}

    for pid, spec in EXPECTED["providers"].items():
        pobj = providers.get(pid)
        exists = isinstance(pobj, dict)
        all_ok &= passfail(f"provider exists: {pid}", exists)
        if not exists:
            continue

        models = pobj.get("models", [])
        models_ok = isinstance(models, list)
        all_ok &= passfail(f"{pid}.models is list", models_ok)
        if not models_ok:
            continue

        actual_ids = {m.get("id") for m in models if isinstance(m, dict) and "id" in m}
        expected_ids = set(spec["model_ids"])
        all_ok &= passfail(
            f"{pid} model IDs exact match",
            actual_ids == expected_ids,
            f"expected={sorted(expected_ids)} actual={sorted(actual_ids)}",
        )

        for m in models:
            if not isinstance(m, dict):
                all_ok &= passfail(f"{pid} model entry is object", False, f"got type={type(m).__name__}")
                continue
            mid = m.get("id", "<missing-id>")
            missing = sorted(required_model_fields - set(m.keys()))
            all_ok &= passfail(f"{pid}:{mid} required fields present", len(missing) == 0, f"missing={missing}")

    # 3) agent inventory
    ok, agent_list = get_in(data, ["agents", "list"])
    all_ok &= passfail("agents.list exists", ok and isinstance(agent_list, list))
    if ok and isinstance(agent_list, list):
        actual_agents = {a.get("id") for a in agent_list if isinstance(a, dict) and "id" in a}
        expected_agents = set(EXPECTED["agents"])
        all_ok &= passfail(
            "agent IDs exact match",
            actual_agents == expected_agents,
            f"expected={sorted(expected_agents)} actual={sorted(actual_agents)}",
        )

    # 4) A2A allowlist exact check
    ok, a2a_allow = get_in(data, ["tools", "agentToAgent", "allow"])
    all_ok &= passfail("tools.agentToAgent.allow exists", ok and isinstance(a2a_allow, list))
    if ok and isinstance(a2a_allow, list):
        actual = set(a2a_allow)
        expected = set(EXPECTED["a2a_allow"])
        all_ok &= passfail(
            "tools.agentToAgent.allow exact match",
            actual == expected,
            f"expected={sorted(expected)} actual={sorted(actual)}",
        )
    elif not ok:
        all_ok &= passfail(
            "tools.agentToAgent legacy targetAllowlist absent",
            not get_in(data, ["tools", "agentToAgent", "targetAllowlist"])[0],
            "if legacy key exists, run `openclaw doctor --fix`",
        )

    # 5) default primary model
    ok, primary = get_in(data, ["agents", "defaults", "model", "primary"])
    expected_primary = expected_default_primary_model()
    all_ok &= passfail(
        "agents.defaults.model.primary expected value",
        ok and primary == expected_primary,
        f"expected={expected_primary} actual={primary if ok else '<missing>'}",
    )

    # 6) schema migration checks: legacy keys must be absent
    for label, path in LEGACY_KEYS_SHOULD_NOT_EXIST:
        exists, _ = get_in(data, path)
        all_ok &= passfail(f"legacy key absent: {label}", not exists)

    print()
    print("OVERALL:", "PASS" if all_ok else "FAIL")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())