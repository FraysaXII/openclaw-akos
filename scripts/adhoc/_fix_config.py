#!/usr/bin/env python3
"""Remove unsupported controlUi key from live config."""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from akos.io import resolve_openclaw_home, load_json, save_json

oc_path = resolve_openclaw_home() / "openclaw.json"
cfg = load_json(oc_path)
gw = cfg.get("gateway", {})
if "controlUi" in gw:
    del gw["controlUi"]
    save_json(oc_path, cfg)
    print("Removed unsupported controlUi key from live config")
else:
    print("controlUi key not present")
print("Gateway config is now clean")
