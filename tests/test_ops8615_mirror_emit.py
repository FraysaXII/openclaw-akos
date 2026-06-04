"""OPS-86-15 mirror emit pack (I93 P6)."""

from __future__ import annotations

from pathlib import Path

import pytest

from akos.hlk_dataops_quality import I93_P6_MIRROR_MIGRATION_BASENAME, OPS_86_15_MIRROR_TARGETS

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
