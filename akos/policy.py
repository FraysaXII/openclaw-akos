"""Role-based capability policy engine for AKOS.

Reads the capability matrix from config/agent-capabilities.json and
generates per-agent tool availability profiles. Enforces role safety
at the config layer, not just at the prompt layer.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from akos.io import REPO_ROOT, load_json

logger = logging.getLogger("akos.policy")

CAPABILITIES_PATH = REPO_ROOT / "config" / "agent-capabilities.json"


class RolePolicy(BaseModel):
    """Effective policy for a single agent role."""

    role: str
    description: str
    allowed_tools: list[str] = Field(default_factory=list)
    denied_tools: list[str] = Field(default_factory=list)
    allowed_categories: list[str] = Field(default_factory=list)
    runtime_profile: str | None = None


class CapabilityMatrix(BaseModel):
    """The full capability matrix for all agent roles."""

    roles: dict[str, RolePolicy] = Field(default_factory=dict)

    @classmethod
    def load(cls, path: Path | None = None) -> CapabilityMatrix:
        """Load the capability matrix from JSON config."""
        config_path = path or CAPABILITIES_PATH
        if not config_path.exists():
            logger.warning("Capability matrix not found at %s", config_path)
            return cls()

        raw = load_json(config_path)
        roles_raw = raw.get("roles", {})
        roles: dict[str, RolePolicy] = {}
        for role_id, role_data in roles_raw.items():
            roles[role_id] = RolePolicy(role=role_id, **role_data)
        return cls(roles=roles)

    def get_policy(self, role_id: str) -> RolePolicy | None:
        """Get the effective policy for a specific agent role."""
        return self.roles.get(role_id.lower())

    def check_drift(self, role_id: str, runtime_tools: list[str]) -> list[dict[str, Any]]:
        """Compare runtime tool list against policy and return drift issues."""
        policy = self.get_policy(role_id)
        if not policy:
            return [{"type": "unknown_role", "role": role_id}]

        issues: list[dict[str, Any]] = []
        denied_set = set(policy.denied_tools)
        for tool in runtime_tools:
            if tool in denied_set:
                issues.append({
                    "type": "denied_tool_enabled",
                    "role": role_id,
                    "tool": tool,
                })
        return issues
