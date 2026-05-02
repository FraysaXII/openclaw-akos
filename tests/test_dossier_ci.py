"""Initiative 48 P8 — CI workflow wiring."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_eval_tier_b_workflow_has_dossier_steps() -> None:
    yml = REPO_ROOT / ".github" / "workflows" / "eval-tier-b.yml"
    text = yml.read_text(encoding="utf-8")
    assert "Render UAT dossier" in text
    assert "scripts/render_uat_dossier.py" in text
    assert "uat-dossier-" in text


def test_dossier_on_pr_workflow_gated_by_repo_var() -> None:
    yml = REPO_ROOT / ".github" / "workflows" / "dossier-on-pr.yml"
    text = yml.read_text(encoding="utf-8")
    assert "AKOS_DOSSIER_ON_PR" in text
    assert "github-script" in text
    assert "--gh-pr-comment" in text


def test_extract_gh_pr_comment_truncates() -> None:
    import importlib.util

    path = REPO_ROOT / "scripts" / "render_uat_dossier.py"
    spec = importlib.util.spec_from_file_location("_render_uat_dossier_test_mod", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    extract = mod._extract_gh_pr_comment_body

    md = "## Section 1 — Executive summary\n\nhello\n\n## Section 2 — X\n\nmore"
    out = extract(md)
    assert "Executive summary" in out
    assert "## Section 2" not in out
    assert len(out) <= 65000
