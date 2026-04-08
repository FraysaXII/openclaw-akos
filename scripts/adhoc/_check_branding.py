#!/usr/bin/env python3
"""Check current branding state in live config."""
import json
from pathlib import Path

cfg_path = Path.home() / ".openclaw" / "openclaw.json"
cfg = json.loads(cfg_path.read_text("utf-8"))

gw = cfg.get("gateway", {})
print(f"Gateway config keys: {list(gw.keys())}")
print(f"controlUi present: {'controlUi' in gw}")
print()

agents = cfg.get("agents", {}).get("list", [])
for a in agents:
    i = a.get("identity", {})
    name = i.get("name", "")
    emoji = i.get("emoji", "")
    aid = a.get("id", "")
    display = a.get("name", "")
    print(f"  {aid:15s}  display={display:40s}  emoji={emoji}")

print()
print(f"Config file: {cfg_path}")
print(f"OpenCLAW version: check gateway UI header")

# Check if openclaw supports updating
import shutil
oc_bin = shutil.which("openclaw")
print(f"openclaw binary: {oc_bin or 'NOT FOUND'}")
