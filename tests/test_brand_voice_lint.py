"""Initiative 49 P12 — offline brand-voice lint tests."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def _load_module():
    p = REPO_ROOT / "scripts" / "lint_brand_voice_offline.py"
    spec = importlib.util.spec_from_file_location("scripts.lint_brand_voice_offline", p)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["scripts.lint_brand_voice_offline"] = mod
    spec.loader.exec_module(mod)
    return mod


brand_lint = _load_module()


def test_lint_text_flags_internal_codenames(tmp_path: Path) -> None:
    p = tmp_path / "external.md"
    p.write_text(
        "Operators consult AKOS daily.\n"
        "Look up topic_external_adviser_handoff for context.\n"
        "GOI-LEG-001 is described internally.\n",
        encoding="utf-8",
    )
    violations = brand_lint.lint_file(p)
    categories = {v.category for v in violations}
    assert any("internal_codename" in c for c in categories)
    patterns = {v.pattern for v in violations}
    assert r"\bAKOS\b" in patterns
    assert r"\btopic_[A-Za-z0-9_]+" in patterns


def test_lint_text_flags_stack_jargon_methodology_and_operator_tokens(tmp_path: Path) -> None:
    p = tmp_path / "external.md"
    p.write_text(
        "Backed by RBAC and pgvector with Mermaid diagrams.\n"
        "Built on the 4-layer methodology with TODO[OPERATOR-CONFIRM] markers.\n"
        "Internal review uses [OPERATOR] notes.\n",
        encoding="utf-8",
    )
    violations = brand_lint.lint_file(p)
    categories = {v.category for v in violations}
    assert "stack_jargon_§4.2" in categories
    assert "methodology_shorthand_§4.3" in categories
    assert "operator_token_§4.4" in categories


def test_lint_clean_text_returns_no_violations(tmp_path: Path) -> None:
    p = tmp_path / "clean.md"
    p.write_text(
        "Holistika delivers structured research and engineering as a service.\n"
        "Plain Spanish for the recipient; semantic search powers the platform.\n",
        encoding="utf-8",
    )
    assert brand_lint.lint_file(p) == []


def test_main_returns_1_on_violations(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    p = tmp_path / "ext.md"
    p.write_text("Refer to AKOS.\n", encoding="utf-8")
    rc = brand_lint.main([str(p), "--quiet"])
    assert rc == 1


def test_main_returns_0_when_clean(tmp_path: Path) -> None:
    p = tmp_path / "ext.md"
    p.write_text("Plain prose only.\n", encoding="utf-8")
    rc = brand_lint.main([str(p), "--quiet"])
    assert rc == 0


def test_main_json_emits_violation_payload(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    p = tmp_path / "ext.md"
    p.write_text("Refer to AKOS or RBAC.\n", encoding="utf-8")
    rc = brand_lint.main([str(p), "--json"])
    assert rc == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["violation_count"] >= 2
    assert any(v["pattern"] == r"\bAKOS\b" for v in payload["violations"])


def test_main_with_no_paths_returns_two(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(brand_lint, "default_targets", lambda: [])
    rc = brand_lint.main(["--quiet"])
    assert rc == 2


def test_default_targets_returns_paths_under_repo() -> None:
    paths = brand_lint.default_targets()
    for p in paths:
        assert p.is_file()


def test_frontmatter_block_is_skipped(tmp_path: Path) -> None:
    p = tmp_path / "ext.md"
    p.write_text(
        "---\n"
        "program_id: PRJ-HOL-FOUNDING-2026\n"
        "topic_ids:\n"
        "  - topic_external\n"
        "---\n"
        "Plain external prose.\n",
        encoding="utf-8",
    )
    assert brand_lint.lint_file(p) == []


def test_yaml_comment_lines_are_skipped(tmp_path: Path) -> None:
    p = tmp_path / "ext.yaml"
    p.write_text(
        "# This comment mentions TODO[OPERATOR] and AKOS for explanatory purposes.\n"
        "title: Holistika dossier\n",
        encoding="utf-8",
    )
    assert brand_lint.lint_file(p) == []


def test_inline_backtick_paths_are_skipped(tmp_path: Path) -> None:
    p = tmp_path / "ext.md"
    p.write_text(
        "Refer to `path/to/PRJ-HOL-FOUNDING-2026/file.md` for context.\n"
        "Plain prose continues here.\n",
        encoding="utf-8",
    )
    assert brand_lint.lint_file(p) == []


def test_pre_commit_step_present_in_verification_profile() -> None:
    """Initiative 49 P12: brand_voice_lint_smoke must be wired into pre_commit."""
    import json as _json
    payload = _json.loads((REPO_ROOT / "config" / "verification-profiles.json").read_text(encoding="utf-8"))
    step_ids = [s["id"] for s in payload["profiles"]["pre_commit"]["steps"]]
    assert "brand_voice_lint_smoke" in step_ids
