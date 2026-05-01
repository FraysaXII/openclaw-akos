"""Initiative 46 P3 — tests for the GraphRAG PoC scaffold."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
GOLDEN_PATH = REPO_ROOT / "config" / "graphrag" / "golden_queries.json"
POC_SCRIPT = REPO_ROOT / "scripts" / "graphrag_poc.py"


def _run_cli(*args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    import os

    cli_env = os.environ.copy()
    cli_env["AKOS_EVAL_NO_DEPRECATION_WARN"] = "1"
    if env:
        cli_env.update(env)
    return subprocess.run(
        [sys.executable, str(POC_SCRIPT), *args],
        capture_output=True,
        text=True,
        timeout=60,
        cwd=REPO_ROOT,
        env=cli_env,
    )


# ── Golden queries config ────────────────────────────────────────────────────


def test_golden_queries_file_exists() -> None:
    assert GOLDEN_PATH.is_file(), "config/graphrag/golden_queries.json must exist"


def test_golden_queries_has_at_least_20() -> None:
    data = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    assert len(data["queries"]) >= 20


def test_golden_queries_target_madeira_lookup() -> None:
    data = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    assert data["_skill_id"] == "SKILL-MADEIRA-LOOKUP-V1"


def test_every_golden_query_has_required_fields() -> None:
    data = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    for i, q in enumerate(data["queries"]):
        assert "id" in q, f"queries[{i}] missing id"
        assert "query" in q, f"queries[{i}] missing query"
        assert "expected_keywords" in q, f"queries[{i}] missing expected_keywords"
        assert "intent" in q, f"queries[{i}] missing intent"
        assert isinstance(q["expected_keywords"], list), f"queries[{i}].expected_keywords must be array"


def test_golden_query_ids_are_unique() -> None:
    data = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    ids = [q["id"] for q in data["queries"]]
    assert len(ids) == len(set(ids)), "duplicate query ids in golden_queries.json"


def test_golden_query_intents_cover_multihop_and_multimode() -> None:
    """The 20 queries should exercise both single-hop (role/process lookup)
    and multi-hop (graph traversal) intents — the reason GraphRAG would help."""
    data = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    intents = {q["intent"] for q in data["queries"]}
    assert "multihop" in intents
    assert "graph_traversal" in intents
    assert "role_lookup" in intents


# ── PoC scaffold (CLI) ───────────────────────────────────────────────────────


def test_poc_validate_config_passes() -> None:
    p = _run_cli("--validate-config")
    assert p.returncode == 0
    assert "PASS" in p.stdout


def test_poc_dry_run_exits_zero() -> None:
    p = _run_cli("--dry-run")
    assert p.returncode == 0
    assert "DRY RUN" in p.stdout
    assert "no LLM cost incurred" in p.stdout


def test_poc_dry_run_lists_skill_under_test() -> None:
    p = _run_cli("--dry-run")
    assert "SKILL-MADEIRA-LOOKUP-V1" in p.stdout


def test_poc_live_without_env_guard_exits_2() -> None:
    p = _run_cli(env={"AKOS_GRAPHRAG_POC_LIVE": ""})
    assert p.returncode == 2
    assert "AKOS_GRAPHRAG_POC_LIVE=1" in p.stderr
    assert "R-46-1" in p.stderr


def test_poc_live_with_env_guard_emits_scaffold_notice() -> None:
    p = _run_cli(env={"AKOS_GRAPHRAG_POC_LIVE": "1"})
    assert p.returncode == 0
    assert "LIVE MODE" in p.stderr
    # Confirm the scaffold notice points operator at the actual implementation gate
    assert "neo4j-graphrag-python" in p.stderr or "operator" in p.stderr.lower()


def test_poc_max_spend_flag_appears_in_dry_run() -> None:
    p = _run_cli("--dry-run", "--max-spend", "12.34")
    assert p.returncode == 0
    assert "$12.34" in p.stdout


# ── Module-level (validate_config helper) ────────────────────────────────────


def test_validate_config_helper_catches_missing_query_field() -> None:
    """Direct unit test of the validate_config helper."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import importlib.util
    spec = importlib.util.spec_from_file_location("graphrag_poc", str(POC_SCRIPT))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    bad_data = {"queries": [{"id": "x", "query": "?"}]}  # missing expected_keywords + intent
    errors = mod.validate_config(bad_data)
    assert len(errors) > 0
    assert any("expected_keywords" in e for e in errors)
    assert any("intent" in e for e in errors)


def test_validate_config_helper_catches_few_queries() -> None:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import importlib.util
    spec = importlib.util.spec_from_file_location("graphrag_poc", str(POC_SCRIPT))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    bad_data = {"queries": [{"id": "x", "query": "?", "expected_keywords": [], "intent": "x"}]}
    errors = mod.validate_config(bad_data)
    assert any(">=20" in e for e in errors)
