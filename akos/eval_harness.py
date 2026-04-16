"""Shared eval suite loading and rubric scoring (used by ``scripts/run-evals.py`` and tests)."""

from __future__ import annotations

import json
from pathlib import Path

EVALS_DIR = Path(__file__).resolve().parent.parent / "tests" / "evals"
SUITES_DIR = EVALS_DIR / "suites"


def load_suite(suite_id: str) -> tuple[dict, list[dict]]:
    root = SUITES_DIR / suite_id
    manifest_path = root / "manifest.json"
    tasks_path = root / "tasks.json"
    if not manifest_path.is_file() or not tasks_path.is_file():
        raise FileNotFoundError(f"Suite not found: {suite_id}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    tasks = json.loads(tasks_path.read_text(encoding="utf-8"))
    if not isinstance(tasks, list):
        raise ValueError("tasks.json must be a JSON array")
    return manifest, tasks


def score_rubric_task(task: dict, answer: str) -> tuple[str, list[str]]:
    rubric = task.get("rubric") or {}
    failures: list[str] = []
    text = answer or ""
    for needle in rubric.get("contains", []) or []:
        if str(needle) not in text:
            failures.append(f"missing_contains:{needle}")
    for bad in rubric.get("forbidden", []) or []:
        if str(bad) in text:
            failures.append(f"forbidden_present:{bad}")
    return ("PASS", []) if not failures else ("FAIL", failures)


def list_suite_ids() -> list[str]:
    if not SUITES_DIR.is_dir():
        return []
    return sorted(p.name for p in SUITES_DIR.iterdir() if (p / "manifest.json").is_file() and (p / "tasks.json").is_file())
