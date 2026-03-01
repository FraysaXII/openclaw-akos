"""Unit tests for all JSON configuration files in config/.

Run after the config/ batch is created:
    python -m pytest tests/validate_configs.py -v
"""

import json
import pathlib

import pytest

from conftest import (
    CONFIG_DIR,
    EXPECTED_MCP_SERVERS,
    INTELLIGENCE_MATRIX_PROPERTIES,
)


def _load_json(path: pathlib.Path) -> dict | list:
    """Load and parse a JSON file, failing with a clear message on error."""
    text = path.read_text(encoding="utf-8")
    return json.loads(text)


# ---------------------------------------------------------------------------
# Generic: every .json file must parse
# ---------------------------------------------------------------------------

class TestAllJsonFilesParse:
    def test_all_json_files_are_valid(self, config_dir):
        json_files = list(config_dir.rglob("*.json"))
        assert len(json_files) > 0, "No JSON files found in config/"
        for f in json_files:
            try:
                _load_json(f)
            except json.JSONDecodeError as exc:
                pytest.fail(f"{f.name} is not valid JSON: {exc}")

    def test_example_json_files_are_valid(self, config_dir):
        example_files = list(config_dir.rglob("*.json.example"))
        for f in example_files:
            try:
                _load_json(f)
            except json.JSONDecodeError as exc:
                pytest.fail(f"{f.name} is not valid JSON: {exc}")


# ---------------------------------------------------------------------------
# openclaw.json.example (T-1.2)
# ---------------------------------------------------------------------------

class TestOpenclawConfig:
    @pytest.fixture(autouse=True)
    def _load(self, config_dir):
        self.data = _load_json(config_dir / "openclaw.json.example")

    def test_has_gateway_block(self):
        assert "gateway" in self.data

    def test_gateway_host_is_localhost(self):
        assert self.data["gateway"]["host"] == "127.0.0.1"

    def test_gateway_port_is_18789(self):
        assert self.data["gateway"]["port"] == 18789

    def test_has_workspaces(self):
        assert "workspaces" in self.data
        assert len(self.data["workspaces"]) > 0

    def test_deep_research_workspace_exists(self):
        assert "deep_research" in self.data["workspaces"]


# ---------------------------------------------------------------------------
# mcporter.json.example (T-2.3 through T-2.6)
# ---------------------------------------------------------------------------

class TestMcporterConfig:
    @pytest.fixture(autouse=True)
    def _load(self, config_dir):
        self.data = _load_json(config_dir / "mcporter.json.example")

    def test_has_mcp_servers(self):
        assert "mcpServers" in self.data

    def test_has_exactly_three_servers(self):
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
    def _load(self, config_dir):
        self.data = _load_json(config_dir / "permissions.json")

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
    def _load(self, config_dir):
        self.data = _load_json(config_dir / "logging.json")

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
    def _load(self, config_dir):
        self.data = _load_json(config_dir / "intelligence-matrix-schema.json")

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
    @pytest.fixture(autouse=True)
    def _load(self, config_dir):
        self.data = _load_json(config_dir / "eval" / "baselines.json")

    def test_has_exactly_four_metrics(self):
        assert len(self.data) == 4

    def test_each_metric_has_required_fields(self):
        required = {"metric_id", "target_value", "unit", "evaluation_window"}
        for entry in self.data:
            missing = required - set(entry.keys())
            assert len(missing) == 0, f"{entry.get('metric_id', '?')} missing: {missing}"


# ---------------------------------------------------------------------------
# alerts.json (T-5.3)
# ---------------------------------------------------------------------------

class TestAlertsConfig:
    @pytest.fixture(autouse=True)
    def _load(self, config_dir):
        self.data = _load_json(config_dir / "eval" / "alerts.json")

    def test_has_at_least_three_alerts(self):
        assert len(self.data) >= 3

    def test_each_alert_has_required_fields(self):
        required = {"alert_id", "condition", "severity"}
        for entry in self.data:
            missing = required - set(entry.keys())
            assert len(missing) == 0, f"{entry.get('alert_id', '?')} missing: {missing}"

    def test_has_critical_severity_alerts(self):
        severities = {a["severity"] for a in self.data}
        assert "critical" in severities
