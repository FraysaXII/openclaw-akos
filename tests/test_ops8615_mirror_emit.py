"""OPS-86-15 mirror emit pack (I93 P6)."""

from __future__ import annotations

from pathlib import Path

import pytest

from akos.hlk_dataops_quality import (
    I93_P6_MIRROR_MIGRATION_BASENAME,
    I93_P6_OPS8615_UPSERT_ARTIFACT,
    OPS_86_15_MIRROR_TARGETS,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.mark.hlk
def test_p6_migration_exists() -> None:
    path = REPO_ROOT / "supabase" / "migrations" / I93_P6_MIRROR_MIGRATION_BASENAME
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    for _csv, table, _sym in OPS_86_15_MIRROR_TARGETS:
        assert table in text


@pytest.mark.hlk
def test_sync_script_declares_emitters() -> None:
    sync = (REPO_ROOT / "scripts" / "sync_compliance_mirrors_from_csv.py").read_text(encoding="utf-8")
    for _csv, _table, sym in OPS_86_15_MIRROR_TARGETS:
        assert sym in sync
    assert "--ops8615-gap-mirrors-only" in sync
    assert "I93_P6_OPS8615_UPSERT_ARTIFACT" in sync


@pytest.mark.hlk
def test_ops8615_default_artifact_path_under_repo() -> None:
    path = REPO_ROOT / I93_P6_OPS8615_UPSERT_ARTIFACT
    assert path.parent.name == "artifacts"
    assert path.name == "ops8615-mirror-upsert.sql"
