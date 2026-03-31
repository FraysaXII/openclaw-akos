"""Unit tests for all JSON configuration files in config/.

Leverages Pydantic models from akos.models for schema validation where
applicable, retaining explicit checks for fields Pydantic doesn't cover.

Run after the config/ batch is created:
    python -m pytest tests/validate_configs.py -v
"""

import json
import pathlib
import re

import pytest

from conftest import (
    CONFIG_DIR,
    EXPECTED_MCP_SERVERS,
    INTELLIGENCE_MATRIX_PROPERTIES,
)

from akos.models import (
    AgentEntry,
    AgentIdentity,
    OpenClawConfig,
    load_alerts,
    load_baselines,
)
from akos.io import load_json


def _load(path: pathlib.Path) -> dict | list:
    return load_json(path)


# ---------------------------------------------------------------------------
# Generic: every .json file must parse
# ---------------------------------------------------------------------------

class TestAllJsonFilesParse:
    def test_all_json_files_are_valid(self, config_dir):
        json_files = list(config_dir.rglob("*.json"))
        assert len(json_files) > 0, "No JSON files found in config/"
        for f in json_files:
            try:
                _load(f)
            except json.JSONDecodeError as exc:
                pytest.fail(f"{f.name} is not valid JSON: {exc}")

    def test_example_json_files_are_valid(self, config_dir):
        example_files = list(config_dir.rglob("*.json.example"))
        for f in example_files:
            try:
                _load(f)
            except json.JSONDecodeError as exc:
                pytest.fail(f"{f.name} is not valid JSON: {exc}")


# ---------------------------------------------------------------------------
# openclaw.json.example -- Pydantic partial validation + targeted checks
# ---------------------------------------------------------------------------

class TestOpenclawConfig:
    @pytest.fixture(autouse=True)
    def _setup(self, config_dir):
        self.data = _load(config_dir / "openclaw.json.example")

    def test_validates_via_pydantic(self):
        config = OpenClawConfig.model_validate(self.data)
        assert config.gateway.host == "127.0.0.1"
        assert config.gateway.port == 18789

    def test_has_at_least_two_agents(self):
        assert len(self.data["agents"]["list"]) >= 2

    def test_architect_agent_defined(self):
        ids = {a["id"] for a in self.data["agents"]["list"]}
        assert "architect" in ids

    def test_executor_agent_defined(self):
        ids = {a["id"] for a in self.data["agents"]["list"]}
        assert "executor" in ids

    def test_identity_is_object_via_pydantic(self):
        for agent_data in self.data["agents"]["list"]:
            entry = AgentEntry.model_validate(agent_data)
            assert isinstance(entry.identity, AgentIdentity)
            assert entry.identity.name

    def test_verbose_default_is_enabled(self):
        defaults = self.data["agents"]["defaults"]
        assert defaults.get("verboseDefault") in ("on", "full")

    def test_thinking_default_is_off_for_ollama(self):
        defaults = self.data["agents"]["defaults"]
        assert defaults.get("thinkingDefault") == "off"

    def test_has_bindings(self):
        assert "bindings" in self.data
        assert isinstance(self.data["bindings"], list)

    def test_has_permissions_reference(self):
        assert "permissions" in self.data


# ---------------------------------------------------------------------------
# mcporter.json.example (T-2.3 through T-2.6)
# ---------------------------------------------------------------------------

class TestMcporterConfig:
    @pytest.fixture(autouse=True)
    def _setup(self, config_dir):
        self.data = _load(config_dir / "mcporter.json.example")

    def test_has_mcp_servers(self):
        assert "mcpServers" in self.data

    def test_has_expected_mcp_servers(self):
        assert set(self.data["mcpServers"].keys()) == EXPECTED_MCP_SERVERS

    def test_each_server_has_command(self):
        for name, server in self.data["mcpServers"].items():
            assert "command" in server, f"{name} is missing 'command' key"

    def test_sequential_thinking_env(self):
        env = self.data["mcpServers"]["sequential-thinking"].get("env", {})
        assert env.get("DISABLE_THOUGHT_LOGGING") == "false"

    def test_playwright_output_dir(self):
        args = self.data["mcpServers"]["playwright"]["args"]
        assert "--output-dir" in args

    def test_github_token_placeholder(self):
        env = self.data["mcpServers"]["github"].get("env", {})
        assert "GITHUB_TOKEN" in env


# ---------------------------------------------------------------------------
# permissions.json (T-3.3)
# ---------------------------------------------------------------------------

class TestPermissionsConfig:
    @pytest.fixture(autouse=True)
    def _setup(self, config_dir):
        self.data = _load(config_dir / "permissions.json")

    def test_has_autonomous_array(self):
        assert isinstance(self.data.get("autonomous"), list)
        assert len(self.data["autonomous"]) > 0

    def test_has_requires_approval_array(self):
        assert isinstance(self.data.get("requires_approval"), list)
        assert len(self.data["requires_approval"]) > 0

    def test_no_overlap_between_tiers(self):
        autonomous = set(self.data["autonomous"])
        approval = set(self.data["requires_approval"])
        overlap = autonomous & approval
        assert len(overlap) == 0, f"Tools in both tiers: {overlap}"


# ---------------------------------------------------------------------------
# logging.json (T-3.5)
# ---------------------------------------------------------------------------

class TestLoggingConfig:
    @pytest.fixture(autouse=True)
    def _setup(self, config_dir):
        self.data = _load(config_dir / "logging.json")

    def test_has_output_directory(self):
        assert "output_directory" in self.data

    def test_format_is_json(self):
        assert self.data["format"] == "json"

    def test_has_fields(self):
        assert isinstance(self.data.get("fields"), list)
        assert len(self.data["fields"]) > 0

    def test_has_soc_risk_indicators(self):
        indicators = self.data.get("soc_risk_indicators", [])
        assert "chmod" in indicators
        assert "canvas.eval" in indicators


# ---------------------------------------------------------------------------
# intelligence-matrix-schema.json (T-4.3)
# ---------------------------------------------------------------------------

class TestIntelligenceMatrixSchema:
    @pytest.fixture(autouse=True)
    def _setup(self, config_dir):
        self.data = _load(config_dir / "intelligence-matrix-schema.json")

    def test_is_json_schema(self):
        assert "$schema" in self.data

    def test_has_all_required_properties(self):
        props = set(self.data.get("properties", {}).keys())
        missing = INTELLIGENCE_MATRIX_PROPERTIES - props
        assert len(missing) == 0, f"Missing properties: {missing}"

    def test_required_field_lists_all_properties(self):
        required = set(self.data.get("required", []))
        assert required == INTELLIGENCE_MATRIX_PROPERTIES

    def test_pestel_has_six_values(self):
        pestel = self.data["properties"]["pestel_category"]
        assert len(pestel.get("enum", [])) == 6

    def test_ssot_verified_is_boolean(self):
        assert self.data["properties"]["ssot_verified"]["type"] == "boolean"


# ---------------------------------------------------------------------------
# baselines.json (T-5.2)
# ---------------------------------------------------------------------------

class TestBaselinesConfig:
    def test_validates_via_pydantic(self, config_dir):
        baselines = load_baselines(config_dir / "eval" / "baselines.json")
        assert len(baselines) == 4

    def test_each_metric_has_required_fields(self, config_dir):
        baselines = load_baselines(config_dir / "eval" / "baselines.json")
        for b in baselines:
            assert b.metric_id
            assert b.unit


# ---------------------------------------------------------------------------
# alerts.json (T-5.3)
# ---------------------------------------------------------------------------

class TestAlertsConfig:
    def test_validates_via_pydantic(self, config_dir):
        alerts = load_alerts(config_dir / "eval" / "alerts.json")
        assert len(alerts) >= 3

    def test_has_critical_severity_alerts(self, config_dir):
        alerts = load_alerts(config_dir / "eval" / "alerts.json")
        severities = {a.severity for a in alerts}
        assert "critical" in severities


# ---------------------------------------------------------------------------
# eu-ai-act-checklist.json (T-3.7)
# ---------------------------------------------------------------------------

class TestEuAiActChecklist:
    @pytest.fixture(autouse=True)
    def _load(self, config_dir):
        self.data = load_json(config_dir / "compliance" / "eu-ai-act-checklist.json")

    def test_has_three_requirements(self):
        assert len(self.data["requirements"]) == 3

    def test_each_requirement_has_evidence(self):
        for req in self.data["requirements"]:
            assert len(req["evidence"]) >= 1, \
                f"{req['requirement_id']} has no evidence items"

    def test_each_evidence_has_verification_date(self):
        for req in self.data["requirements"]:
            for ev in req["evidence"]:
                assert "verification_date" in ev, \
                    f"{req['requirement_id']}/{ev['task_id']}: missing verification_date"
                assert ev["verification_date"], \
                    f"{req['requirement_id']}/{ev['task_id']}: verification_date is empty"

    def test_each_evidence_has_verification_method(self):
        for req in self.data["requirements"]:
            for ev in req["evidence"]:
                assert "verification_method" in ev, \
                    f"{req['requirement_id']}/{ev['task_id']}: missing verification_method"

    def test_overall_status_is_valid(self):
        assert self.data["overall_status"] in ("compliant", "partial", "non-compliant")

    def test_langfuse_evidence_present(self):
        aia1 = self.data["requirements"][0]
        files = [ev["file"] for ev in aia1["evidence"]]
        assert "akos/telemetry.py" in files, \
            "EU-AIA-1 should reference Langfuse telemetry as evidence"


# ---------------------------------------------------------------------------
# resolve_mcporter_paths (idempotent path resolution)
# ---------------------------------------------------------------------------

from akos.io import resolve_mcporter_paths


class TestResolveMcporterPaths:
    TEMPLATE = (
        '{\n'
        '  "mcpServers": {\n'
        '    "playwright": {\n'
        '      "args": ["-y", "@playwright/mcp@latest", "--output-dir", "/opt/openclaw/workspace/exports"]\n'
        '    },\n'
        '    "filesystem": {\n'
        '      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/opt/openclaw/workspace"]\n'
        '    },\n'
        '    "akos": {\n'
        '      "args": ["scripts/mcp_akos_server.py"],\n'
        '      "_note": "Custom AKOS MCP"\n'
        '    },\n'
        '    "finance": {\n'
        '      "args": ["scripts/finance_mcp_server.py"],\n'
        '      "_note": "Finance research MCP"\n'
        '    }\n'
        '  }\n'
        '}'
    )

    def test_resolves_linux_placeholders(self):
        result = resolve_mcporter_paths(self.TEMPLATE)
        assert "/opt/openclaw/workspace/exports" not in result
        assert "/opt/openclaw/workspace" not in result
        assert "scripts/mcp_akos_server.py" not in result or "/" in result.split("scripts/mcp_akos_server.py")[0]

    def test_resolves_all_repo_scripts(self):
        result = resolve_mcporter_paths(self.TEMPLATE)
        assert "scripts/finance_mcp_server.py" not in result or "/" in result.split("scripts/finance_mcp_server.py")[0]

    def test_idempotent(self):
        first = resolve_mcporter_paths(self.TEMPLATE)
        second = resolve_mcporter_paths(first)
        assert first == second, "resolve_mcporter_paths must be idempotent"

    def test_preserves_note_keys(self):
        result = resolve_mcporter_paths(self.TEMPLATE)
        assert '"_note": "Custom AKOS MCP"' in result
        assert '"_note": "Finance research MCP"' in result


class TestSessionConfigExampleAlignment:
    """Verify openclaw.json.example session block matches SessionConfig model."""

    def test_session_uses_current_schema_keys(self, config_dir):
        data = load_json(config_dir / "openclaw.json.example")
        session = data["session"]
        assert "typingMode" in session, "session should use typingMode, not typing"
        assert "typing" not in session, "session should not have legacy typing key"
        a2a = session.get("agentToAgent", {})
        assert "maxPingPongTurns" in a2a, "session.agentToAgent should use maxPingPongTurns"
        assert "pingPongTurns" not in a2a, "session.agentToAgent should not have legacy pingPongTurns"


class TestStrictAkosInventoryContract:
    """Lock full-only provider and A2A inventory contract in the template."""

    def test_provider_ids_exact_match(self, config_dir):
        data = load_json(config_dir / "openclaw.json.example")
        providers = data["models"]["providers"]
        assert set(providers.keys()) == {
            "ollama",
            "ollama-gpu",
            "openai",
            "anthropic",
            "vllm-runpod",
        }

    def test_a2a_allowlist_exact_match(self, config_dir):
        data = load_json(config_dir / "openclaw.json.example")
        allow = data["tools"]["agentToAgent"]["allow"]
        assert set(allow) == {"orchestrator", "architect", "executor", "verifier"}

    def test_ollama_model_count(self, config_dir):
        data = load_json(config_dir / "openclaw.json.example")
        ollama_models = data["models"]["providers"]["ollama"]["models"]
        assert len(ollama_models) == 4, (
            f"Expected 4 Ollama models, got {len(ollama_models)}: "
            f"{[m['id'] for m in ollama_models]}"
        )


class TestEnvPlaceholderCoverage:
    """Every ${VAR} in openclaw.json.example must have a definition in all *.env.example files."""

    def test_all_env_placeholders_covered(self, config_dir):
        ssot_text = (config_dir / "openclaw.json.example").read_text(encoding="utf-8")
        required_vars = set(re.findall(r"\$\{(\w+)\}", ssot_text))
        assert len(required_vars) > 0, "No ${VAR} placeholders found in SSOT"

        env_dir = config_dir / "environments"
        env_files = sorted(env_dir.glob("*.env.example"))
        assert len(env_files) >= 3, f"Expected at least 3 .env.example files, got {len(env_files)}"

        for env_file in env_files:
            content = env_file.read_text(encoding="utf-8")
            defined_vars = set(re.findall(r"^(\w+)=", content, re.MULTILINE))
            missing = required_vars - defined_vars
            assert len(missing) == 0, (
                f"{env_file.name} is missing placeholders for: {sorted(missing)}"
            )
