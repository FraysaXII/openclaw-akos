"""Unit tests for prompt files in prompts/.

Validates that base prompts contain essential behavioral directives.
Overlay-specific content (sequential thinking fields, intelligence matrix)
is tested only in the full assembled variants.

Run after the prompts/ batch is created:
    python -m pytest tests/validate_prompts.py -v
"""

import pathlib

import pytest

from conftest import PROMPTS_DIR


def _read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# ARCHITECT_PROMPT.md (T-4.1) -- compact variant (base)
# ---------------------------------------------------------------------------

class TestArchitectPrompt:
    @pytest.fixture(autouse=True)
    def _load(self):
        self.text = _read(PROMPTS_DIR / "ARCHITECT_PROMPT.md")

    def test_file_not_empty(self):
        assert len(self.text.strip()) > 0

    def test_enforces_read_only(self):
        assert "read-only" in self.text

    def test_references_sequential_thinking(self):
        assert "sequential_thinking" in self.text

    def test_prohibits_dangerous_tools(self):
        for tool in ["write_file", "delete_file", "shell_exec"]:
            assert tool in self.text, f"Must mention {tool} to prohibit it"

    def test_has_response_modes(self):
        assert "Conversational" in self.text
        assert "Analysis" in self.text
        assert "Handoff" in self.text

    def test_has_progress_directives(self):
        assert "MUST" in self.text
        assert "tool call" in self.text.lower()

    def test_has_plan_document_section(self):
        assert "Plan Document" in self.text

    def test_has_data_governance(self):
        assert "Data Governance" in self.text


# ---------------------------------------------------------------------------
# EXECUTOR_PROMPT.md (T-4.2) -- compact variant (base)
# ---------------------------------------------------------------------------

class TestExecutorPrompt:
    @pytest.fixture(autouse=True)
    def _load(self):
        self.text = _read(PROMPTS_DIR / "EXECUTOR_PROMPT.md")

    def test_file_not_empty(self):
        assert len(self.text.strip()) > 0

    def test_references_plan_document(self):
        assert "Plan Document" in self.text

    def test_requires_reading_plan_first(self):
        assert "MUST read" in self.text

    def test_enforces_hitl(self):
        assert "HITL" in self.text

    def test_references_requires_approval(self):
        assert "requires_approval" in self.text

    def test_has_abort_protocol(self):
        assert "Abort" in self.text or "halt" in self.text.lower()

    def test_has_progress_directives(self):
        assert "MUST emit" in self.text

    def test_has_execution_report(self):
        assert "Execution Report" in self.text

    def test_is_read_write_mode(self):
        assert "read-write" in self.text


# ---------------------------------------------------------------------------
# MADEIRA_PROMPT.md -- compact variant (base)
# ---------------------------------------------------------------------------

class TestMadeiraPrompt:
    @pytest.fixture(autouse=True)
    def _load(self):
        self.text = _read(PROMPTS_DIR / "MADEIRA_PROMPT.md")

    def test_file_not_empty(self):
        assert len(self.text.strip()) > 0

    def test_has_startup_reads(self):
        for required in ["IDENTITY.md", "USER.md", "WORKFLOW_AUTO.md", "MEMORY.md"]:
            assert required in self.text
        assert "memory/YYYY-MM-DD.md" in self.text

    def test_never_emits_no_reply(self):
        assert "Never emit `NO_REPLY`" in self.text

    def test_enforces_anti_fabrication(self):
        assert "Never invent names, UUIDs, workstreams" in self.text
        assert "Never expose internal tool" in self.text

    def test_uses_hlk_tools_not_workspace_files(self):
        assert "Treat `hlk_*` tools as the only retrieval path" in self.text
        assert "Do NOT claim that `baseline_organisation.csv` or `process_list.csv` is missing from `workspace-madeira`" in self.text

    def test_same_turn_search_recovery(self):
        assert "call `hlk_search` in the SAME turn before any user-visible reply" in self.text
        assert "Do not ask the user whether you should search" in self.text

    def test_support_tools_are_context_only(self):
        assert "`read` -- startup and workspace-context reads only" in self.text
        assert "`memory_get`, `memory_search` -- supporting session context only" in self.text
        assert "`akos_route_request`" in self.text

    def test_role_answer_contract(self):
        assert "you MUST call `hlk_role` first" in self.text
        assert "include the canonical role name, access level, reports_to, area, and entity" in self.text
        assert "Never cite `hlk_role`, `hlk_search`, `best_role`, or the raw query string" in self.text

    def test_search_and_escalation_stay_user_facing(self):
        assert "perform the search silently" in self.text
        assert "Do NOT brainstorm restructuring options" in self.text
        assert "FIRST sentence" in self.text
        assert "ask it only AFTER the escalation note" in self.text
        assert "you MAY call `akos_route_request`" in self.text or "If the route is unclear or mixed, you MAY call `akos_route_request`" in self.text

    def test_finance_mode_is_procedural(self):
        assert "you MAY call `akos_route_request` on the raw user request first" in self.text
        assert "If the user gives a company name or partial symbol, call `finance_search` first" in self.text
        assert "call `finance_quote` in the SAME turn before replying" in self.text
        assert "Always surface the data source, freshness, and any warnings" in self.text

    def test_has_escalation_boundary(self):
        assert "Escalate to the Orchestrator" in self.text
        assert "Do NOT attempt write operations yourself" in self.text

    def test_cites_canonical_hlk_sources(self):
        assert "baseline_organisation.csv" in self.text
        assert "process_list.csv" in self.text


# ---------------------------------------------------------------------------
# Base prompt structure
# ---------------------------------------------------------------------------

class TestBasePrompts:
    def test_architect_base_exists(self):
        assert (PROMPTS_DIR / "base" / "ARCHITECT_BASE.md").exists()

    def test_executor_base_exists(self):
        assert (PROMPTS_DIR / "base" / "EXECUTOR_BASE.md").exists()

    def test_bases_contain_must_directives(self):
        for base_file in (PROMPTS_DIR / "base").glob("*.md"):
            content = base_file.read_text(encoding="utf-8")
            assert "MUST" in content, f"{base_file.name} should contain MUST directives"

    def test_base_prompts_use_read_tool_not_legacy_read_file(self):
        for base_file in (PROMPTS_DIR / "base").glob("*.md"):
            content = base_file.read_text(encoding="utf-8")
            assert "read_file(" not in content, f"{base_file.name} should use the `read` tool name"

    def test_verifier_is_not_labeled_read_write(self):
        verifier_text = _read(PROMPTS_DIR / "VERIFIER_PROMPT.md")
        assert "read-write validator" not in verifier_text
        assert "read-focused validator" in verifier_text
