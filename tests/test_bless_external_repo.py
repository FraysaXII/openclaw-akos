"""Tests for scripts/bless_external_repo.py.

Covers: registry loading, slug validation, reference-class skip, idempotency,
sha256 stamping, hand-edit detection, force overwrite, and dry-run safety.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "bless_external_repo.py"


def _load() -> object:
    spec = importlib.util.spec_from_file_location("_bless_external_repo_test", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture()
def bless():
    return _load()


@pytest.fixture()
def fake_repo(tmp_path: Path) -> Path:
    """Minimal fake consumer repo layout."""
    root = tmp_path / "fake-repo"
    root.mkdir()
    (root / "package.json").write_text('{"name":"fake","version":"0.1.0"}', encoding="utf-8")
    (root / ".cursor" / "rules").mkdir(parents=True)
    return root


@pytest.fixture()
def repo_meta(bless) -> object:
    """A platform-class RepoMeta synthesised in-test (decoupled from CSV)."""
    return bless.RepoMeta(
        slug="hlk-erp",
        github_url="https://github.com/FraysaXII/hlk-erp",
        repo_class="platform",
        primary_owner_role="System Owner",
        vault_doc_root="docs/references/hlk/v3.0/Envoy Tech Lab/HLK-ERP/",
        lifecycle_status="active",
    )


# ---------------------------------------------------------------------------
# Registry loading
# ---------------------------------------------------------------------------


def test_load_registry_real_csv_has_hlk_erp(bless):
    registry = bless.load_registry()
    assert "hlk-erp" in registry
    assert registry["hlk-erp"].repo_class == "platform"


def test_load_registry_handles_missing_optional_columns(bless, tmp_path):
    csv_path = tmp_path / "REPOSITORY_REGISTRY.csv"
    csv_path.write_text(
        "repo_slug,github_url,class,primary_owner_role,topic_ids,vault_doc_root,api_spec_pointer,api_topic_id,lifecycle_status,notes\n"
        "x-repo,https://example.com/x,internal,System Owner,,,,,,active,test row\n",
        encoding="utf-8",
    )
    registry = bless.load_registry(csv_path)
    assert registry["x-repo"].consumes_compliance_types is False
    assert registry["x-repo"].consumes_mirrors == ()
    assert registry["x-repo"].relative_path == ""


def test_load_registry_parses_i63_columns(bless, tmp_path):
    """I63 P4 canonical columns: consumes_mirrors uses ';' as separator (not ','),
    and 'local_path' is the column name (renamed from the v1 proposal's 'path')."""
    csv_path = tmp_path / "REPOSITORY_REGISTRY.csv"
    csv_path.write_text(
        "repo_slug,github_url,class,primary_owner_role,topic_ids,vault_doc_root,api_spec_pointer,api_topic_id,lifecycle_status,notes,consumes_compliance_types,consumes_mirrors,local_path\n"
        "y-repo,https://example.com/y,platform,System Owner,,,,,active,test,yes,persona_registry_mirror;skill_registry_mirror,../root_cd/y-repo\n",
        encoding="utf-8",
    )
    registry = bless.load_registry(csv_path)
    meta = registry["y-repo"]
    assert meta.consumes_compliance_types is True
    assert "persona_registry_mirror" in meta.consumes_mirrors
    assert "skill_registry_mirror" in meta.consumes_mirrors
    assert meta.relative_path == "../root_cd/y-repo"


# ---------------------------------------------------------------------------
# Reference-class skip
# ---------------------------------------------------------------------------


def test_reference_class_repo_is_skipped(bless, fake_repo, monkeypatch):
    meta = bless.RepoMeta(
        slug="boilerplate",
        github_url="https://example.com/b",
        repo_class="reference",
        primary_owner_role="Brand Manager",
        vault_doc_root="",
        lifecycle_status="reference",
    )
    results = bless.bless_repo(repo_meta=meta, repo_path=fake_repo, dry_run=False)
    assert results["overall"] == "SKIPPED_REFERENCE"
    assert not (fake_repo / "EXTERNAL_REPO_CONTRACT.md").exists()
    assert not (fake_repo / ".cursor" / "rules" / "akos-mirror.mdc").exists()


# ---------------------------------------------------------------------------
# Copy fidelity + sha256 stamp
# ---------------------------------------------------------------------------


def test_first_run_writes_artifacts_and_stamps(bless, fake_repo, repo_meta):
    results = bless.bless_repo(repo_meta=repo_meta, repo_path=fake_repo)
    assert results["overall"] == "OK"
    mirror = fake_repo / ".cursor" / "rules" / "akos-mirror.mdc"
    contract = fake_repo / "EXTERNAL_REPO_CONTRACT.md"
    contributing = fake_repo / "CONTRIBUTING.md"
    pr = fake_repo / ".github" / "PULL_REQUEST_TEMPLATE.md"
    stamp = fake_repo / ".cursor" / "rules" / ".akos-mirror.sha256"
    for p in (mirror, contract, contributing, pr, stamp):
        assert p.is_file(), f"{p} not written"
    assert results["akos-mirror.mdc"] == "WROTE"
    assert len(stamp.read_text().strip()) == 64


def test_idempotent_second_run_no_writes(bless, fake_repo, repo_meta):
    bless.bless_repo(repo_meta=repo_meta, repo_path=fake_repo)
    results = bless.bless_repo(repo_meta=repo_meta, repo_path=fake_repo)
    assert results["akos-mirror.mdc"] == "SKIPPED_UNCHANGED"
    assert results["EXTERNAL_REPO_CONTRACT.md"] == "SKIPPED_UNCHANGED"


# ---------------------------------------------------------------------------
# Hand-edit detection + force
# ---------------------------------------------------------------------------


def test_hand_edit_to_managed_file_is_refused_without_force(bless, fake_repo, repo_meta):
    bless.bless_repo(repo_meta=repo_meta, repo_path=fake_repo)
    contract = fake_repo / "EXTERNAL_REPO_CONTRACT.md"
    body = contract.read_text(encoding="utf-8")
    contract.write_text(body + "\n# locally edited\n", encoding="utf-8")

    results = bless.bless_repo(repo_meta=repo_meta, repo_path=fake_repo, force=False)
    assert results["EXTERNAL_REPO_CONTRACT.md"] == "REFUSED_HAND_EDIT"
    assert "locally edited" in contract.read_text(encoding="utf-8")


def test_force_overwrites_hand_edited_file(bless, fake_repo, repo_meta):
    bless.bless_repo(repo_meta=repo_meta, repo_path=fake_repo)
    contract = fake_repo / "EXTERNAL_REPO_CONTRACT.md"
    contract.write_text("LOCAL OVERRIDE", encoding="utf-8")

    results = bless.bless_repo(repo_meta=repo_meta, repo_path=fake_repo, force=True)
    assert results["EXTERNAL_REPO_CONTRACT.md"] == "WROTE"
    assert "LOCAL OVERRIDE" not in contract.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Dry-run safety
# ---------------------------------------------------------------------------


def test_dry_run_writes_nothing(bless, fake_repo, repo_meta):
    results = bless.bless_repo(repo_meta=repo_meta, repo_path=fake_repo, dry_run=True)
    assert "DRY_WROTE" in results.values()
    assert not (fake_repo / "EXTERNAL_REPO_CONTRACT.md").exists()
    assert not (fake_repo / ".cursor" / "rules" / "akos-mirror.mdc").exists()


# ---------------------------------------------------------------------------
# Drift detection (sha256 mismatch with template)
# ---------------------------------------------------------------------------


def test_drift_when_template_changes_triggers_update(bless, fake_repo, repo_meta, monkeypatch):
    bless.bless_repo(repo_meta=repo_meta, repo_path=fake_repo)
    mirror = fake_repo / ".cursor" / "rules" / "akos-mirror.mdc"
    original = mirror.read_text(encoding="utf-8")
    edited = original + "\n# old comment\n"
    mirror.write_text(edited, encoding="utf-8")
    stamp = fake_repo / ".cursor" / "rules" / ".akos-mirror.sha256"
    stamp.write_text(bless.sha256_text(edited) + "\n", encoding="utf-8")

    results = bless.bless_repo(repo_meta=repo_meta, repo_path=fake_repo, force=False)
    assert results["akos-mirror.mdc"] in {"WROTE", "REFUSED_HAND_EDIT"}


def test_render_template_substitutes_placeholders(bless, repo_meta):
    rendered = bless.render_template("slug={{REPO_SLUG}} class={{REPO_CLASS}}", repo_meta)
    assert "slug=hlk-erp" in rendered
    assert "class=platform" in rendered


# ---------------------------------------------------------------------------
# Stack detection
# ---------------------------------------------------------------------------


def test_detect_stack_node_only(bless, fake_repo):
    s = bless.detect_stack(fake_repo)
    assert s["is_node"] is True
    assert s["is_python"] is False
    assert s["has_supabase_migrations"] is False


def test_detect_stack_supabase_migrations_dir(bless, fake_repo):
    (fake_repo / "supabase" / "migrations").mkdir(parents=True)
    s = bless.detect_stack(fake_repo)
    assert s["has_supabase_migrations"] is True


# ---------------------------------------------------------------------------
# CLI smoke (subprocess against the real registry)
# ---------------------------------------------------------------------------


def test_cli_unknown_slug_returns_2(bless):
    rc = bless.main(["--repo-slug", "nonexistent-slug", "--repo-path", str(REPO_ROOT)])
    assert rc == 2


def test_cli_dry_run_against_hlk_erp_succeeds(bless, tmp_path):
    erp_root = Path(r"c:\Users\Shadow\cd_shadow\root_cd\hlk-erp")
    if not erp_root.is_dir():
        pytest.skip("hlk-erp working tree not available on this machine")
    rc = bless.main(["--repo-slug", "hlk-erp", "--repo-path", str(erp_root), "--dry-run"])
    assert rc == 0
