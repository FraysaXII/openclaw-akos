"""Shared fixtures for OpenCLAW-AKOS scaffolding validation tests."""

import pathlib
import sys

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

# Ensure the akos package is importable from tests
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

CONFIG_DIR = REPO_ROOT / "config"
PROMPTS_DIR = REPO_ROOT / "prompts"
SCRIPTS_DIR = REPO_ROOT / "scripts"

EXPECTED_MCP_SERVERS = {"sequential-thinking", "playwright", "github", "memory", "filesystem", "fetch"}

AUTONOMOUS_TOOLS = {
    "read_file", "list_directory", "web_search", "sequential_thinking",
    "browser_snapshot", "browser_screenshot", "mcporter_list",
    "git_status", "git_diff", "git_log",
    "memory_retrieve", "memory_list",
    "fetch_get", "filesystem_read", "filesystem_list",
}

REQUIRES_APPROVAL_TOOLS = {
    "write_file", "delete_file", "shell_exec", "browser_navigate",
    "browser_click", "browser_type", "browser_console_exec", "element_interact",
    "git_push", "git_commit", "canvas_eval",
    "network_download", "system_config_change",
    "memory_store", "memory_delete",
    "fetch_post", "filesystem_write", "filesystem_delete",
}

INTELLIGENCE_MATRIX_PROPERTIES = {
    "fact_id", "source_credibility", "direct_impact",
    "indirect_impact", "pestel_category", "generational_filter",
    "ssot_verified",
}

EXPECTED_SCAFFOLDING_FILES = [
    CONFIG_DIR / "openclaw.json.example",
    CONFIG_DIR / "mcporter.json.example",
    CONFIG_DIR / "permissions.json",
    CONFIG_DIR / "logging.json",
    CONFIG_DIR / "splunk" / "inputs.conf",
    CONFIG_DIR / "eval" / "langfuse.env.example",
    CONFIG_DIR / "eval" / "baselines.json",
    CONFIG_DIR / "eval" / "alerts.json",
    CONFIG_DIR / "intelligence-matrix-schema.json",
    CONFIG_DIR / "compliance" / "eu-ai-act-checklist.json",
    PROMPTS_DIR / "ARCHITECT_PROMPT.md",
    PROMPTS_DIR / "EXECUTOR_PROMPT.md",
    SCRIPTS_DIR / "vet-install.sh",
]

SECRET_PATTERNS = ["sk-", "ghp_", "Bearer ", "-----BEGIN"]

SOP_TASK_FILE_MAP = {
    "T-1.2": CONFIG_DIR / "openclaw.json.example",
    "T-2.3": CONFIG_DIR / "mcporter.json.example",
    "T-2.4": CONFIG_DIR / "mcporter.json.example",
    "T-2.5": CONFIG_DIR / "mcporter.json.example",
    "T-2.6": CONFIG_DIR / "mcporter.json.example",
    "T-2.7": PROMPTS_DIR / "ARCHITECT_PROMPT.md",
    "T-3.2": SCRIPTS_DIR / "vet-install.sh",
    "T-3.3": CONFIG_DIR / "permissions.json",
    "T-3.5": CONFIG_DIR / "logging.json",
    "T-3.6": CONFIG_DIR / "splunk" / "inputs.conf",
    "T-3.7": CONFIG_DIR / "compliance" / "eu-ai-act-checklist.json",
    "T-4.1": PROMPTS_DIR / "ARCHITECT_PROMPT.md",
    "T-4.2": PROMPTS_DIR / "EXECUTOR_PROMPT.md",
    "T-4.3": CONFIG_DIR / "intelligence-matrix-schema.json",
    "T-5.1": CONFIG_DIR / "eval" / "langfuse.env.example",
    "T-5.2": CONFIG_DIR / "eval" / "baselines.json",
    "T-5.3": CONFIG_DIR / "eval" / "alerts.json",
}


@pytest.fixture
def repo_root():
    return REPO_ROOT


@pytest.fixture
def config_dir():
    return CONFIG_DIR


@pytest.fixture
def prompts_dir():
    return PROMPTS_DIR


@pytest.fixture
def scripts_dir():
    return SCRIPTS_DIR
