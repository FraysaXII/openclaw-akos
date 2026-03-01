"""Unit tests for prompt files in prompts/.

Run after the prompts/ batch is created:
    python -m pytest tests/validate_prompts.py -v
"""

import pathlib

import pytest

from conftest import PROMPTS_DIR


def _read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# ARCHITECT_PROMPT.md (T-4.1)
# ---------------------------------------------------------------------------

class TestArchitectPrompt:
    @pytest.fixture(autouse=True)
    def _load(self):
        self.text = _read(PROMPTS_DIR / "ARCHITECT_PROMPT.md")

    def test_file_not_empty(self):
        assert len(self.text.strip()) > 0

    def test_enforces_read_only(self):
        assert "read-only" in self.text

    def test_mandates_sequential_thinking(self):
        assert "sequential_thinking" in self.text

    def test_references_thought_variable(self):
        assert "thought" in self.text

    def test_references_thought_number(self):
        assert "thoughtNumber" in self.text

    def test_references_total_thoughts(self):
        assert "totalThoughts" in self.text

    def test_references_next_thought_needed(self):
        assert "nextThoughtNeeded" in self.text

    def test_references_is_revision(self):
        assert "isRevision" in self.text

    def test_references_revises_thought(self):
        assert "revisesThought" in self.text

    def test_prohibits_write_file(self):
        assert "write_file" in self.text, "Must mention write_file to prohibit it"
        lines_with_write = [
            line for line in self.text.splitlines()
            if "write_file" in line
        ]
        for line in lines_with_write:
            assert any(w in line.lower() for w in ["must not", "forbidden", "not"]), \
                f"write_file mentioned without prohibition context: {line.strip()}"

    def test_prohibits_shell_exec(self):
        assert "shell_exec" in self.text, "Must mention shell_exec to prohibit it"

    def test_references_intelligence_matrix(self):
        assert "intelligence-matrix-schema" in self.text or "Intelligence Matrix" in self.text

    def test_references_permissions_config(self):
        assert "permissions.json" in self.text


# ---------------------------------------------------------------------------
# EXECUTOR_PROMPT.md (T-4.2)
# ---------------------------------------------------------------------------

class TestExecutorPrompt:
    @pytest.fixture(autouse=True)
    def _load(self):
        self.text = _read(PROMPTS_DIR / "EXECUTOR_PROMPT.md")

    def test_file_not_empty(self):
        assert len(self.text.strip()) > 0

    def test_references_plan_document(self):
        assert "plan" in self.text.lower()

    def test_requires_reading_plan_first(self):
        assert "Plan Document" in self.text

    def test_enforces_hitl(self):
        assert "HITL" in self.text

    def test_references_requires_approval(self):
        assert "requires_approval" in self.text

    def test_references_permissions_config(self):
        assert "permissions.json" in self.text

    def test_has_abort_protocol(self):
        assert "abort" in self.text.lower() or "halt" in self.text.lower()

    def test_mentions_idempotency(self):
        assert "idempoten" in self.text.lower()

    def test_mentions_verification(self):
        assert "verif" in self.text.lower()

    def test_is_read_write_mode(self):
        assert "read-write" in self.text
