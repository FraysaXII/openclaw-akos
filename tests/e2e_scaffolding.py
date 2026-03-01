"""End-to-end validation of the full scaffolding structure.

Run as the final check before committing:
    python -m pytest tests/e2e_scaffolding.py -v
"""

import json
import pathlib
import re

import pytest

from conftest import (
    REPO_ROOT,
    CONFIG_DIR,
    EXPECTED_SCAFFOLDING_FILES,
    SECRET_PATTERNS,
    SOP_TASK_FILE_MAP,
)


# ---------------------------------------------------------------------------
# All expected files exist and are non-empty
# ---------------------------------------------------------------------------

class TestFileTreeCompleteness:
    def test_all_expected_files_exist(self):
        missing = [f for f in EXPECTED_SCAFFOLDING_FILES if not f.exists()]
        assert len(missing) == 0, f"Missing files: {[str(m.relative_to(REPO_ROOT)) for m in missing]}"

    def test_no_file_is_empty(self):
        empty = [
            f for f in EXPECTED_SCAFFOLDING_FILES
            if f.exists() and f.stat().st_size == 0
        ]
        assert len(empty) == 0, f"Empty files: {[str(e.relative_to(REPO_ROOT)) for e in empty]}"


# ---------------------------------------------------------------------------
# Cross-reference consistency
# ---------------------------------------------------------------------------

class TestCrossReferences:
    def test_permissions_tools_appear_in_architect_prompt(self):
        perms = json.loads((CONFIG_DIR / "permissions.json").read_text(encoding="utf-8"))
        architect = (REPO_ROOT / "prompts" / "ARCHITECT_PROMPT.md").read_text(encoding="utf-8")

        for tool in perms["requires_approval"][:5]:
            assert tool in architect, \
                f"Architect prompt should reference '{tool}' (from requires_approval) to prohibit it"

    def test_permissions_tools_appear_in_executor_prompt(self):
        perms = json.loads((CONFIG_DIR / "permissions.json").read_text(encoding="utf-8"))
        executor = (REPO_ROOT / "prompts" / "EXECUTOR_PROMPT.md").read_text(encoding="utf-8")

        assert "requires_approval" in executor
        for tool in perms["requires_approval"][:3]:
            assert tool in executor, \
                f"Executor prompt should reference '{tool}' (from requires_approval)"


# ---------------------------------------------------------------------------
# .gitignore alignment
# ---------------------------------------------------------------------------

class TestGitignoreAlignment:
    @pytest.fixture(autouse=True)
    def _load(self):
        self.gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")

    def test_openclaw_json_is_gitignored(self):
        assert "openclaw.json" in self.gitignore

    def test_example_files_are_not_blocked(self):
        """The .gitignore pattern 'openclaw.json' should not block
        'openclaw.json.example' since git matching is exact-name for
        non-glob patterns."""
        assert "openclaw.json.example" not in self.gitignore

    def test_env_files_are_gitignored(self):
        assert ".env" in self.gitignore

    def test_mcporter_dir_is_gitignored(self):
        assert ".mcporter/" in self.gitignore


# ---------------------------------------------------------------------------
# No secrets in committed files
# ---------------------------------------------------------------------------

class TestNoSecrets:
    def test_no_secret_patterns_in_scaffolding(self):
        violations = []
        for f in EXPECTED_SCAFFOLDING_FILES:
            if not f.exists():
                continue
            try:
                content = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for pattern in SECRET_PATTERNS:
                if pattern in content:
                    if "your-" in content[max(0, content.index(pattern) - 30):content.index(pattern)]:
                        continue
                    if "placeholder" in content.lower():
                        continue
                    violations.append(f"{f.relative_to(REPO_ROOT)}: contains '{pattern}'")
        assert len(violations) == 0, f"Potential secrets found: {violations}"


# ---------------------------------------------------------------------------
# SOP task coverage
# ---------------------------------------------------------------------------

class TestSopTaskCoverage:
    def test_every_create_file_task_has_output(self):
        missing = {
            task_id: str(path.relative_to(REPO_ROOT))
            for task_id, path in SOP_TASK_FILE_MAP.items()
            if not path.exists()
        }
        assert len(missing) == 0, f"SOP tasks without output files: {missing}"


# ---------------------------------------------------------------------------
# JSON structural integrity across all config files
# ---------------------------------------------------------------------------

class TestJsonIntegrity:
    def test_all_json_configs_parse(self):
        json_files = list(CONFIG_DIR.rglob("*.json"))
        json_files += list(CONFIG_DIR.rglob("*.json.example"))
        for f in json_files:
            try:
                json.loads(f.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                pytest.fail(f"{f.relative_to(REPO_ROOT)} failed to parse: {exc}")
