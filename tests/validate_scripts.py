"""Unit tests for shell scripts in scripts/.

Run after the scripts/ batch is created:
    python -m pytest tests/validate_scripts.py -v
"""

import pathlib

import pytest

from conftest import SCRIPTS_DIR


def _read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# vet-install.sh (T-3.2)
# ---------------------------------------------------------------------------

class TestVetInstallScript:
    @pytest.fixture(autouse=True)
    def _load(self):
        self.path = SCRIPTS_DIR / "vet-install.sh"
        self.text = _read(self.path)
        self.lines = self.text.splitlines()

    def test_file_not_empty(self):
        assert len(self.text.strip()) > 0

    def test_shebang_is_correct(self):
        assert self.lines[0] == "#!/usr/bin/env bash"

    def test_references_safe_install(self):
        assert "safe-install.sh" in self.text

    def test_checks_skillvet_directory_exists(self):
        assert "skillvet" in self.text
        has_existence_check = (
            "! -d" in self.text
            or "! -f" in self.text
            or "test -d" in self.text
            or "test -f" in self.text
        )
        assert has_existence_check, "Missing existence check for skillvet directory"

    def test_exits_on_missing_argument(self):
        assert "$#" in self.text or "argc" in self.text.lower(), \
            "Should validate that a skill slug argument was provided"

    def test_uses_strict_mode(self):
        assert "set -e" in self.text or "set -euo pipefail" in self.text
