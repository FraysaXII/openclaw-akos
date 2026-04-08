#!/usr/bin/env python3
"""Apply HLK branding to the live openclaw.json config."""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from akos.io import resolve_openclaw_home, load_json, save_json

oc_path = resolve_openclaw_home() / "openclaw.json"
cfg = load_json(oc_path)

cfg.setdefault("gateway", {})["controlUi"] = {"title": "HLK Intelligence Platform"}

for agent in cfg.get("agents", {}).get("list", []):
    aid = agent.get("id", "")
    identity = agent.setdefault("identity", {})
    if aid == "orchestrator":
        agent["name"] = "HLK Orchestrator"
        identity["name"] = "HLK Orchestrator"
        identity["emoji"] = "\U0001f3db\ufe0f"
    elif aid == "architect":
        agent["name"] = "HLK Architect"
        identity["name"] = "HLK Architect"
    elif aid == "executor":
        agent["name"] = "HLK Executor"
        identity["name"] = "HLK Executor"
    elif aid == "verifier":
        agent["name"] = "HLK Verifier"
        identity["name"] = "HLK Verifier"

save_json(oc_path, cfg)
title = cfg["gateway"]["controlUi"]["title"]
print(f"Applied HLK branding to {oc_path}")
print(f"Gateway title: {title}")
agents = [a["name"] for a in cfg.get("agents", {}).get("list", [])]
print(f"Agent names: {agents}")
