"""Dynamic tool registry for AKOS.

Reads the mcporter config and permissions to expose available tools
with their HITL classification.  Used by prompt assembly and the API
to report which tools are available before runtime.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from akos.io import REPO_ROOT, load_json

logger = logging.getLogger("akos.tools")

MCPORTER_PATH = REPO_ROOT / "config" / "mcporter.json.example"
PERMISSIONS_PATH = REPO_ROOT / "config" / "permissions.json"

GATEWAY_CORE_TOOLS = frozenset({
    "read", "write", "edit", "apply_patch",
    "exec", "process",
    "web_search", "web_fetch",
    "memory_search", "memory_get",
    "sessions_list", "sessions_history", "sessions_send",
    "sessions_spawn", "subagents", "session_status",
    "browser", "canvas", "message", "cron",
    "gateway", "nodes", "agents_list", "image", "tts",
})

GATEWAY_PLUGIN_TOOLS = frozenset({
    "sequential_thinking",
    "finance_quote", "finance_search", "finance_sentiment",
    "hlk_role", "hlk_role_chain", "hlk_area", "hlk_process",
    "hlk_process_tree", "hlk_projects", "hlk_gaps", "hlk_search",
})


@dataclass
class ToolInfo:
    name: str
    server: str
    hitl_gate: str  # "autonomous" | "requires_approval" | "unknown"


class ToolRegistry:
    """Discovers tools from mcporter config and classifies them via permissions."""

    def __init__(
        self,
        mcporter_path: Path | None = None,
        permissions_path: Path | None = None,
    ) -> None:
        self._mcporter_path = mcporter_path or MCPORTER_PATH
        self._permissions_path = permissions_path or PERMISSIONS_PATH
        self._servers: dict[str, dict] = {}
        self._autonomous: set[str] = set()
        self._requires_approval: set[str] = set()
        self._load()

    def _load(self) -> None:
        if self._mcporter_path.exists():
            raw = load_json(self._mcporter_path)
            self._servers = raw.get("mcpServers", {})
        else:
            logger.warning("mcporter config not found: %s", self._mcporter_path)

        if self._permissions_path.exists():
            perms = load_json(self._permissions_path)
            self._autonomous = set(perms.get("autonomous", []))
            self._requires_approval = set(perms.get("requires_approval", []))
        else:
            logger.warning("Permissions config not found: %s", self._permissions_path)

    @property
    def server_names(self) -> list[str]:
        return list(self._servers.keys())

    def classify(self, tool_name: str) -> str:
        """Return the HITL gate for a tool: autonomous, requires_approval, or unknown."""
        if tool_name in self._autonomous:
            return "autonomous"
        if tool_name in self._requires_approval:
            return "requires_approval"
        return "unknown"

    def is_available(self, tool_name: str) -> bool:
        """Check if a tool is known (in either autonomous or requires_approval)."""
        return tool_name in self._autonomous or tool_name in self._requires_approval

    def all_tools(self) -> list[str]:
        """Return all known tool names sorted alphabetically."""
        return sorted(self._autonomous | self._requires_approval)

    def autonomous_tools(self) -> list[str]:
        return sorted(self._autonomous)

    def approval_tools(self) -> list[str]:
        return sorted(self._requires_approval)

    def server_info(self, server_name: str) -> dict | None:
        return self._servers.get(server_name)


def classify_gateway_tool_id(tool_name: str) -> str:
    """Classify a runtime tool identifier as core, plugin, or unknown."""
    if tool_name in GATEWAY_CORE_TOOLS:
        return "core"
    if tool_name in GATEWAY_PLUGIN_TOOLS:
        return "plugin"
    return "unknown"
