"""Eval suite manifest + rubric harness tests."""

from __future__ import annotations

import json
from pathlib import Path

from akos.eval_harness import load_suite, score_rubric_task

REPO_ROOT = Path(__file__).resolve().parent.parent
SUITES = REPO_ROOT / "tests" / "evals" / "suites"


def test_pathc_suite_manifest_schema():
    man_path = SUITES / "pathc-research-spine" / "manifest.json"
    assert man_path.is_file()
    man = json.loads(man_path.read_text(encoding="utf-8"))
    assert man.get("suite_id") == "pathc-research-spine"
    assert man.get("version")
    assert man.get("schema_version")
    assert man.get("last_reviewed")
    assert isinstance(man.get("dimension_coverage"), list)


def test_pathc_tasks_load_and_rubric():
    manifest, tasks = load_suite("pathc-research-spine")
    assert manifest["suite_id"] == "pathc-research-spine"
    assert len(tasks) >= 3
    for t in tasks:
        status, reasons = score_rubric_task(t, str(t.get("golden_answer", "")))
        assert status == "PASS", (t.get("id"), reasons)


def test_madeira_operator_coverage_manifest():
    man_path = SUITES / "madeira-operator-coverage" / "manifest.json"
    assert man_path.is_file()
    man = json.loads(man_path.read_text(encoding="utf-8"))
    assert man.get("suite_id") == "madeira-operator-coverage"
    assert man.get("schema_version")
    assert man.get("last_reviewed")
    assert isinstance(man.get("dimension_coverage"), list)


def test_madeira_operator_coverage_tasks_rubric():
    manifest, tasks = load_suite("madeira-operator-coverage")
    assert manifest["suite_id"] == "madeira-operator-coverage"
    assert len(tasks) >= 8
    for t in tasks:
        status, reasons = score_rubric_task(t, str(t.get("golden_answer", "")))
        assert status == "PASS", (t.get("id"), reasons)


def test_pathc_public_task_fails_on_fake_url():
    task = {
        "rubric": {
            "contains": ["browser"],
            "forbidden": ["http://made-up-holistika.internal"],
        },
    }
    bad = "Opened http://made-up-holistika.internal in browser"
    status, reasons = score_rubric_task(task, bad)
    assert status == "FAIL"
    assert any("forbidden" in r for r in reasons)
