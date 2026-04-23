"""Tests for Madeira interaction mode and plan handoff schema."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

pytestmark = pytest.mark.madeira

from akos.madeira_interaction import (
    apply_madeira_interaction_to_soul,
    load_handoff_schema,
    parse_first_handoff_json,
    prompt_variant_for_madeira_mode,
    validate_madeira_interaction_mode,
    validate_plan_handoff_dict,
    validate_plan_handoff_markdown,
)
from akos.state import AkosState, load_state, record_switch, save_state


def test_prompt_variant_for_madeira_mode() -> None:
    assert prompt_variant_for_madeira_mode("ask") == "compact"
    assert prompt_variant_for_madeira_mode("plan_draft") == "standard"


def test_validate_madeira_interaction_mode_rejects_unknown() -> None:
    with pytest.raises(ValueError, match="ask"):
        validate_madeira_interaction_mode("run")


def test_handoff_schema_has_required_fields() -> None:
    schema = load_handoff_schema()
    assert schema.get("title") == "MadeiraPlanHandoff"
    req = set(schema.get("required", []))
    assert {"schema_version", "non_canonical", "goal", "citations"}.issubset(req)


def test_record_switch_preserves_madeira_mode(tmp_path: Path) -> None:
    save_state(tmp_path, AkosState(madeiraInteractionMode="plan_draft"))
    record_switch(
        tmp_path,
        environment="dev-local",
        model="ollama/x",
        tier="small",
        variant="compact",
        success=True,
    )
    assert load_state(tmp_path).madeiraInteractionMode == "plan_draft"


def test_example_handoff_matches_required_keys() -> None:
    schema = load_handoff_schema()
    req = set(schema.get("required", []))
    example = {
        "schema_version": "1.0",
        "non_canonical": True,
        "goal": "g",
        "assumptions": ["a"],
        "citations": [{"asset": "process_list.csv", "note": "n"}],
        "verification_matrix_ref": "docs/DEVELOPER_CHECKLIST.md",
        "suggested_swarm": "Orchestrator → Architect",
    }
    assert req <= set(example.keys())


def test_apply_madeira_plan_draft_appends_overlay(tmp_path: Path) -> None:
    assembled = Path(__file__).resolve().parent.parent / "prompts" / "assembled"
    std = assembled / "MADEIRA_PROMPT.standard.md"
    if not std.is_file():
        pytest.skip("assembled prompts missing; run scripts/assemble-prompts.py")
    apply_madeira_interaction_to_soul(tmp_path, mode="plan_draft", assembled_dir=assembled)
    soul = tmp_path / "workspace-madeira" / "SOUL.md"
    assert soul.is_file()
    text = soul.read_text(encoding="utf-8")
    assert "Plan draft mode" in text


def test_apply_madeira_ask_uses_compact(tmp_path: Path) -> None:
    assembled = Path(__file__).resolve().parent.parent / "prompts" / "assembled"
    comp = assembled / "MADEIRA_PROMPT.compact.md"
    if not comp.is_file():
        pytest.skip("assembled prompts missing")
    apply_madeira_interaction_to_soul(tmp_path, mode="ask", assembled_dir=assembled)
    soul = tmp_path / "workspace-madeira" / "SOUL.md"
    body = soul.read_text(encoding="utf-8")
    assert "# Madeira Agent" in body


@patch("akos.api.resolve_openclaw_home")
def test_api_madeira_interaction_mode_get(mock_home, tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    from akos.api import app

    mock_home.return_value = tmp_path
    save_state(tmp_path, AkosState(madeiraInteractionMode="plan_draft", activeVariant="standard"))
    client = TestClient(app)
    resp = client.get("/agents/madeira/interaction-mode")
    assert resp.status_code == 200
    data = resp.json()
    assert data["madeiraInteractionMode"] == "plan_draft"
    assert data["madeiraPromptVariant"] == "standard"
    assert data["planOverlayActive"] is True


@patch("akos.madeira_interaction.redeploy_all_souls_with_madeira_mode")
@patch("akos.api.resolve_openclaw_home")
def test_api_madeira_interaction_mode_post_no_redeploy(mock_home, mock_redeploy, tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    from akos.api import app
    from akos.state import load_state

    mock_home.return_value = tmp_path
    save_state(tmp_path, AkosState())
    client = TestClient(app)
    resp = client.post(
        "/agents/madeira/interaction-mode",
        json={"mode": "plan_draft", "redeploy": False},
    )
    assert resp.status_code == 200
    assert resp.json()["madeiraInteractionMode"] == "plan_draft"
    assert resp.json()["redeployed"] is False
    mock_redeploy.assert_not_called()
    assert load_state(tmp_path).madeiraInteractionMode == "plan_draft"


def test_validate_plan_handoff_markdown_round_trip() -> None:
    md = """# Plan

Draft (non-canonical — promote via Orchestrator swarm before execution).

```json
{
  "schema_version": "1.0",
  "non_canonical": true,
  "goal": "Add FINOPS tranche",
  "assumptions": ["Operator approval"],
  "citations": [{"asset": "process_list.csv", "note": "SSOT"}],
  "verification_matrix_ref": "docs/DEVELOPER_CHECKLIST.md",
  "suggested_swarm": "Orchestrator"
}
```
"""
    obj = validate_plan_handoff_markdown(md)
    assert obj["schema_version"] == "1.0"
    assert obj["non_canonical"] is True


def test_validate_plan_handoff_dict_rejects_extra_keys() -> None:
    schema = load_handoff_schema()
    bad = {
        "schema_version": "1.0",
        "non_canonical": True,
        "goal": "g",
        "assumptions": [],
        "citations": [{"asset": "process_list.csv", "note": "n"}],
        "verification_matrix_ref": "docs/DEVELOPER_CHECKLIST.md",
        "suggested_swarm": "Orchestrator",
        "extra_field": "nope",
    }
    import jsonschema

    with pytest.raises(jsonschema.ValidationError):
        validate_plan_handoff_dict(bad, schema)


def test_parse_first_handoff_json_errors() -> None:
    with pytest.raises(ValueError, match="no_json_fence"):
        parse_first_handoff_json("no fence here")


def test_madeira_role_denies_shell_in_capabilities() -> None:
    import json as _json

    from akos.io import REPO_ROOT

    raw = _json.loads((REPO_ROOT / "config" / "agent-capabilities.json").read_text(encoding="utf-8"))
    madeira = raw["roles"]["madeira"]
    assert "shell_exec" in madeira["denied_tools"]
    assert "write_file" in madeira["denied_tools"]
