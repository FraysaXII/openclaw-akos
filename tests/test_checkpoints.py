"""Tests for akos.checkpoints -- workspace snapshot/restore."""

from __future__ import annotations

from pathlib import Path

import pytest

from akos.checkpoints import create_checkpoint, list_checkpoints, restore_checkpoint


@pytest.fixture()
def workspace(tmp_path: Path) -> Path:
    ws = tmp_path / "workspace"
    ws.mkdir()
    (ws / "file1.txt").write_text("hello", encoding="utf-8")
    (ws / "file2.txt").write_text("world", encoding="utf-8")
    sub = ws / "subdir"
    sub.mkdir()
    (sub / "nested.txt").write_text("nested", encoding="utf-8")
    return ws


class TestCreateCheckpoint:
    def test_creates_tarball(self, workspace: Path):
        info = create_checkpoint("test-snap", workspace)
        assert info.name == "test-snap"
        assert info.size_bytes > 0
        assert Path(info.path).exists()

    def test_checkpoint_dir_created(self, workspace: Path):
        create_checkpoint("snap", workspace)
        assert (workspace / ".checkpoints").is_dir()

    def test_missing_workspace_raises(self, tmp_path: Path):
        with pytest.raises(FileNotFoundError):
            create_checkpoint("snap", tmp_path / "nonexistent")


class TestRestoreCheckpoint:
    def test_restores_files(self, workspace: Path):
        create_checkpoint("restore-test", workspace)
        (workspace / "file1.txt").write_text("modified", encoding="utf-8")
        (workspace / "newfile.txt").write_text("extra", encoding="utf-8")

        assert restore_checkpoint("restore-test", workspace)
        assert (workspace / "file1.txt").read_text(encoding="utf-8") == "hello"
        assert not (workspace / "newfile.txt").exists()

    def test_restore_nonexistent_returns_false(self, workspace: Path):
        assert not restore_checkpoint("does-not-exist", workspace)

    def test_preserves_checkpoint_dir(self, workspace: Path):
        create_checkpoint("preserve-test", workspace)
        restore_checkpoint("preserve-test", workspace)
        assert (workspace / ".checkpoints").exists()


class TestListCheckpoints:
    def test_empty_workspace_returns_empty(self, workspace: Path):
        assert list_checkpoints(workspace) == []

    def test_lists_created_checkpoints(self, workspace: Path):
        create_checkpoint("alpha", workspace)
        create_checkpoint("beta", workspace)
        items = list_checkpoints(workspace)
        assert len(items) == 2
        names = {c.name for c in items}
        assert "alpha" in names
        assert "beta" in names

    def test_newest_first(self, workspace: Path):
        import time
        create_checkpoint("first", workspace)
        time.sleep(1.1)
        create_checkpoint("second", workspace)
        items = list_checkpoints(workspace)
        assert items[0].name == "second"
