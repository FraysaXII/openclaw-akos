#!/usr/bin/env python3
"""Test AKOS API endpoints and HLK tools for UAT."""
import json, urllib.request, sys

BASE = "http://127.0.0.1:8420"
results = []

def test(name, path, expected_status=200):
    try:
        req = urllib.request.Request(f"{BASE}{path}")
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode())
        ok = resp.status == expected_status
        results.append((name, "PASS" if ok else "FAIL", resp.status, data))
        return data
    except Exception as e:
        results.append((name, "FAIL", str(e)[:80], {}))
        return {}

# Core health
test("API Health", "/health")
test("API Status", "/status")
test("Agent List", "/agents")

# HLK domain tools
areas = test("HLK Areas", "/hlk/areas")
roles = test("HLK Roles search", "/hlk/roles?query=CEO")
processes = test("HLK Processes search", "/hlk/processes?query=marketing")
gaps = test("HLK Gaps", "/hlk/gaps")

# Finance tools
test("Finance Quote", "/finance/quote/AAPL")
test("Finance Search", "/finance/search?q=Apple")

# Routing
test("Intent Classify", "/routing/classify?q=restructure+the+finance+area")

print()
print("=" * 70)
print("  AKOS API UAT Results")
print("=" * 70)
for name, status, code, data in results:
    indicator = "PASS" if status == "PASS" else "FAIL"
    print(f"  [{indicator}] {name:30s} status={code}")
    if isinstance(data, dict) and data.get("status"):
        print(f"         response.status={data['status']}")
    if isinstance(data, dict) and data.get("roles"):
        print(f"         roles returned: {len(data['roles'])}")
    if isinstance(data, dict) and data.get("processes"):
        print(f"         processes returned: {len(data['processes'])}")
    if isinstance(data, dict) and data.get("areas"):
        print(f"         areas: {data['areas'][:5]}...")

print()
failures = [r for r in results if r[1] == "FAIL"]
print(f"Total: {len(results)} tests, {len(results)-len(failures)} passed, {len(failures)} failed")
if failures:
    print(f"\nFailed tests:")
    for name, _, code, _ in failures:
        print(f"  - {name}: {code}")
    sys.exit(1)
else:
    print("\nAll AKOS API tests PASS.")
