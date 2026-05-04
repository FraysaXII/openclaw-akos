#!/usr/bin/env python3
"""Detailed live axe-core audit for OPS-54-1 cycles (Initiative 54).

Companion to ``scripts/browser-smoke.py --axe`` which surfaces only
aggregate counts. This helper runs axe-core against
``AXE_IN_SCOPE_SURFACES`` from ``browser-smoke.py`` and dumps the full
violation report (rule_id, impact, help URL, affected nodes, target
selectors) plus a screenshot per surface for the UAT report.

Output (gitignored under ``artifacts/uat/i54-live-a11y/<ts>/``):

    findings.json     — array of {scenario, surface, counts, violations[]}
    <scenario>.png    — viewport screenshot per surface
    findings.md       — human-readable summary, copy-pasteable into UAT report

Usage:

    py scripts/audit_a11y_live.py
    py scripts/audit_a11y_live.py --headed         # show the browser
    py scripts/audit_a11y_live.py --engine msedge  # pin browser engine

Requires both gateways live (FastAPI 8420 + OpenClaw 18789); see
``docs/USER_GUIDE.md`` § Two-gateway boot.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import platform
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def _import_browser_smoke():
    """Late-import shim because browser-smoke.py uses a hyphen in its name."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "_browser_smoke", str(ROOT / "scripts" / "browser-smoke.py")
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load scripts/browser-smoke.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _impact_counts(violations: list[dict]) -> dict[str, int]:
    counts = {"critical": 0, "serious": 0, "moderate": 0, "minor": 0, "unknown": 0}
    for v in violations or []:
        impact = (v.get("impact") or "unknown").lower()
        counts[impact if impact in counts else "unknown"] += 1
    return counts


def _normalise_violation(v: dict) -> dict:
    return {
        "rule_id": v.get("id"),
        "impact": v.get("impact"),
        "help": v.get("help"),
        "help_url": v.get("helpUrl"),
        "tags": v.get("tags", []),
        "node_count": len(v.get("nodes", [])),
        "first_target": (v.get("nodes", [{}])[0].get("target") if v.get("nodes") else None),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Live axe-core detail audit (OPS-54-1)")
    parser.add_argument("--headed", action="store_true", help="show the browser")
    parser.add_argument("--engine", default=None, help="msedge | chromium | firefox")
    parser.add_argument("--out-dir", default=None, help="override artifact dir")
    args = parser.parse_args()

    bs = _import_browser_smoke()  # type: ignore[no-redef]
    if not bs.PLAYWRIGHT_AVAILABLE:
        print("Playwright not installed", file=sys.stderr)
        return 2
    if not bs.AXE_AVAILABLE:
        print("axe-playwright-python not installed (pip install -r requirements-dev.txt)", file=sys.stderr)
        return 2

    ts = dt.datetime.now().strftime("%Y%m%dT%H%M%S")
    out_dir = Path(args.out_dir) if args.out_dir else ROOT / "artifacts" / "uat" / "i54-live-a11y" / ts
    out_dir.mkdir(parents=True, exist_ok=True)

    from playwright.sync_api import sync_playwright  # type: ignore
    from axe_playwright_python.sync_playwright import Axe  # type: ignore

    findings: list[dict] = []
    candidates = [args.engine] if args.engine else (
        ["msedge", "chromium", "firefox"] if platform.system() == "Windows" else ["chromium", "firefox"]
    )

    with sync_playwright() as p:
        browser = None
        for cand in candidates:
            try:
                browser = bs._launch_browser_with_engine(p, args.headed, cand)
                used_engine = cand
                break
            except Exception as e:
                print(f"  engine {cand} failed: {e}", file=sys.stderr)
        if browser is None:
            print("could not launch any browser engine", file=sys.stderr)
            return 3
        try:
            ctx = browser.new_context(ignore_https_errors=True)
            page = ctx.new_page()
            axe = Axe()
            for scenario_id, url_path in bs.AXE_IN_SCOPE_SURFACES:
                full_url = f"{bs.API_URL}{url_path}"
                page.goto(full_url, wait_until="domcontentloaded", timeout=15000)
                page.screenshot(path=str(out_dir / f"{scenario_id}.png"), full_page=False)
                report = axe.run(page)
                violations = (
                    getattr(report, "violations", None)
                    or report.response.get("violations", [])
                    or []
                )
                findings.append({
                    "scenario": scenario_id,
                    "url": full_url,
                    "counts": _impact_counts(violations),
                    "violations": [_normalise_violation(v) for v in violations],
                    "engine": used_engine,
                })
        finally:
            browser.close()

    (out_dir / "findings.json").write_text(json.dumps(findings, indent=2), encoding="utf-8")

    md_lines = ["# OPS-54-1 live a11y audit (detail)", "", f"- Run timestamp: `{ts}`", f"- Engine: `{used_engine}`", f"- Python: `{platform.python_version()}`", f"- OS: `{platform.platform()}`", ""]
    for f in findings:
        c = f["counts"]
        md_lines.append(f"## {f['scenario']} — {f['url']}")
        md_lines.append("")
        md_lines.append(f"- Counts: **{c['critical']} Critical / {c['serious']} Serious / {c['moderate']} Moderate / {c['minor']} Minor**")
        md_lines.append(f"- Screenshot: `{f['scenario']}.png`")
        md_lines.append("")
        if f["violations"]:
            md_lines.append("| Rule ID | Impact | Nodes | Help |")
            md_lines.append("|:--------|:-------|------:|:-----|")
            for v in f["violations"]:
                md_lines.append(f"| `{v['rule_id']}` | {v['impact']} | {v['node_count']} | [{v['help']}]({v['help_url']}) |")
            md_lines.append("")
    (out_dir / "findings.md").write_text("\n".join(md_lines), encoding="utf-8")

    print(f"wrote {out_dir/'findings.json'}")
    print(f"wrote {out_dir/'findings.md'}")
    print(f"wrote {len(findings)} screenshot(s) to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
