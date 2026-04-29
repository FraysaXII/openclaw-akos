"""Tests for scripts/render_km_diagrams.py --all + --dry-run (Initiative 25 P8).

Locks in the batch-render contract:
- `_discover_mmd_sources` returns sorted list of `.mmd` paths under a root.
- `--dry-run` does not invoke mmdc / mermaid.ink (no PNG/SVG writes).
- `--all` requires no positional path; `--all` + path is rejected.
- `--all` walks `docs/references/hlk/v3.0/_assets/`.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "render_km_diagrams.py"


@pytest.fixture(scope="module")
def render_km_module():
    spec = importlib.util.spec_from_file_location(
        "render_km_diagrams_under_test", SCRIPT_PATH
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["render_km_diagrams_under_test"] = module
    spec.loader.exec_module(module)
    return module


def test_discover_mmd_sources_handles_missing_root(render_km_module, tmp_path):
    out = render_km_module._discover_mmd_sources(tmp_path / "nope")
    assert out == []


def test_discover_mmd_sources_finds_mmd_files(render_km_module, tmp_path):
    (tmp_path / "a.mmd").write_text("flowchart LR\nA --> B\n", encoding="utf-8")
    (tmp_path / "b.mmd").write_text("flowchart LR\nC --> D\n", encoding="utf-8")
    (tmp_path / "skip.png").write_text("not mmd", encoding="utf-8")
    out = render_km_module._discover_mmd_sources(tmp_path)
    names = sorted(p.name for p in out)
    assert names == ["a.mmd", "b.mmd"]


def test_discover_mmd_sources_recursive(render_km_module, tmp_path):
    nested = tmp_path / "plane" / "PRJ-X" / "topic"
    nested.mkdir(parents=True)
    (nested / "deep.mmd").write_text("flowchart LR\n", encoding="utf-8")
    out = render_km_module._discover_mmd_sources(tmp_path)
    assert len(out) == 1
    assert out[0].name == "deep.mmd"


def test_discover_mmd_sources_returns_sorted(render_km_module, tmp_path):
    (tmp_path / "z.mmd").write_text("", encoding="utf-8")
    (tmp_path / "a.mmd").write_text("", encoding="utf-8")
    (tmp_path / "m.mmd").write_text("", encoding="utf-8")
    out = render_km_module._discover_mmd_sources(tmp_path)
    names = [p.name for p in out]
    assert names == sorted(names)


def test_discover_mmd_skips_git_dir(render_km_module, tmp_path):
    git_dir = tmp_path / ".git" / "objects"
    git_dir.mkdir(parents=True)
    (git_dir / "sneaky.mmd").write_text("", encoding="utf-8")
    (tmp_path / "real.mmd").write_text("", encoding="utf-8")
    out = render_km_module._discover_mmd_sources(tmp_path)
    names = [p.name for p in out]
    assert names == ["real.mmd"]


def test_render_one_dry_run_does_not_write(render_km_module, tmp_path, capsys):
    src = tmp_path / "test.mmd"
    src.write_text("flowchart LR\nA --> B\n", encoding="utf-8")
    rc = render_km_module._render_one(
        src,
        update_manifest=False,
        prefer_mermaid_ink=False,
        dry_run=True,
    )
    captured = capsys.readouterr()
    assert rc == 0
    assert "[dry-run]" in captured.out
    # Confirm no .png / .svg written:
    assert not (tmp_path / "test.png").exists()
    assert not (tmp_path / "test.svg").exists()


def test_render_one_rejects_missing_source(render_km_module, tmp_path):
    rc = render_km_module._render_one(
        tmp_path / "missing.mmd",
        update_manifest=False,
        prefer_mermaid_ink=False,
        dry_run=True,
    )
    assert rc == 2


def test_main_rejects_all_with_source(render_km_module, capsys):
    rc = render_km_module.main(["fake.mmd", "--all"])
    captured = capsys.readouterr()
    assert rc == 2
    assert "--all cannot be combined" in captured.err


def test_main_rejects_no_source_no_all(render_km_module, capsys):
    rc = render_km_module.main([])
    captured = capsys.readouterr()
    assert rc == 2
    assert "provide a .mmd path or pass --all" in captured.err


def test_main_all_dry_run_walks_repo(render_km_module, capsys):
    """--all + --dry-run on the real repo enumerates the committed .mmd files."""
    rc = render_km_module.main(["--all", "--dry-run"])
    captured = capsys.readouterr()
    # Either we found .mmd files (PASS) or there are none (also OK).
    assert rc == 0
    # If anything was discovered, the announce line must appear:
    if "discovered" in captured.out:
        assert "[dry-run]" in captured.out
