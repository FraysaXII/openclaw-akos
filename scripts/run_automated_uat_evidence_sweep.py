#!/usr/bin/env python3
"""Automated closure-UAT + evidence-class sweep (Operations PMO paired runbook).

Composite AC-AUTOMATION for SOP-PMO_EVIDENCE_CLASS_GATE_001:
  1. validate_uat_report --all (forward reports)
  2. validate_evidence_class_gate (initiative closure cross-check)
  3. Write artifacts/evidence-gate/uat-sweep-YYYY-MM-DD.json summary

Usage:
    py scripts/run_automated_uat_evidence_sweep.py
    py scripts/run_automated_uat_evidence_sweep.py --self-test
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ARTIFACT_DIR = REPO_ROOT / "artifacts" / "evidence-gate"


def _run(argv: list[str]) -> tuple[int, str]:
    env = os.environ.copy()
    # Windows cp1252 consoles crash on Unicode in validator output (e.g. >= in docstrings).
    env.setdefault("PYTHONIOENCODING", "utf-8")
    proc = subprocess.run(
        [sys.executable, *argv],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, out.strip()


def run_sweep(*, strict: bool = False) -> tuple[int, dict]:
    steps: list[dict] = []
    overall_ok = True

    uat_argv = ["scripts/validate_uat_report.py", "--all"]
    if strict:
        uat_argv.append("--strict")
    code, out = _run(uat_argv)
    steps.append({"id": "validate_uat_report_all", "exit_code": code, "tail": out[-2000:]})
    overall_ok &= code == 0

    code, out = _run(["scripts/validate_evidence_class_gate.py"])
    steps.append({"id": "validate_evidence_class_gate", "exit_code": code, "tail": out[-1000:]})
    overall_ok &= code == 0

    code, out = _run(["scripts/validate_evidence_class_registry.py"])
    steps.append({"id": "validate_evidence_class_registry", "exit_code": code, "tail": out[-1000:]})
    overall_ok &= code == 0

    summary = {
        "sweep_date": date.today().isoformat(),
        "overall": "PASS" if overall_ok else "FAIL",
        "steps": steps,
        "evidence_proof_ref_hint": "artifacts/evidence-gate/uat-sweep-*.json",
    }
    return (0 if overall_ok else 1), summary


def self_test() -> int:
    code, _ = _run(["scripts/validate_evidence_class_gate.py", "--self-test"])
    return code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--strict", action="store_true", help="Fail on WARN in UAT --all")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()

    code, summary = run_sweep(strict=args.strict)
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = ARTIFACT_DIR / f"uat-sweep-{summary['sweep_date']}.json"
    out_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    if not args.quiet:
        print(f"{'PASS' if code == 0 else 'FAIL'}: automated UAT evidence sweep -> {out_path.relative_to(REPO_ROOT).as_posix()}")
        for step in summary["steps"]:
            print(f"  - {step['id']}: exit {step['exit_code']}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
