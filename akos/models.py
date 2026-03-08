"""Pydantic models for all AKOS configuration schemas.

Provides runtime type safety, JSON Schema generation, and validation
for model-tiers.json, openclaw.json, environment overlays, alerts, and baselines.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, model_validator

# ── Constrained types ───────────────────────────────────────────────────

ThinkingLevel = Literal["off", "low", "medium", "high"]
PromptVariant = Literal["compact", "standard", "full"]
VerboseLevel = Literal["off", "on", "full"]
TierName = Literal["small", "medium", "large", "sota"]
AlertSeverity = Literal["low", "medium", "high", "critical"]


# ── Model Tier Registry (config/model-tiers.json) ──────────────────────

class TierConfig(BaseModel):
    contextBudget: int = Field(gt=0)
    thinkingDefault: ThinkingLevel
    promptVariant: PromptVariant
    description: str
    models: list[str] = Field(min_length=1)


class OverlayEntry(BaseModel):
    """A single overlay specification.  May carry an ``agents`` filter."""

    file: str
    agents: list[str] | None = None


def _normalize_overlay(raw: str | dict) -> OverlayEntry:
    """Accept both ``"OVERLAY_X.md"`` and ``{"file": "...", "agents": [...]}``."""
    if isinstance(raw, str):
        return OverlayEntry(file=raw)
    return OverlayEntry.model_validate(raw)


class ModelTiersRegistry(BaseModel):
    tiers: dict[TierName, TierConfig]
    variantOverlays: dict[PromptVariant, list[str | dict]]

    def overlays_for(self, variant: str, agent: str) -> list[str]:
        """Return overlay filenames applicable to *agent* in *variant*."""
        raw_list = self.variantOverlays.get(variant, [])
        result: list[str] = []
        for raw in raw_list:
            entry = _normalize_overlay(raw)
            if entry.agents is None or agent in entry.agents:
                result.append(entry.file)
        return result

    def lookup_tier(self, model_id: str) -> tuple[str, TierConfig] | None:
        """Find the tier a model belongs to. Returns (tier_name, config) or None."""
        for name, tier in self.tiers.items():
            if model_id in tier.models:
                return name, tier
        return None

    @model_validator(mode="after")
    def _no_duplicate_models(self) -> ModelTiersRegistry:
        all_models: list[str] = []
        for tier in self.tiers.values():
            all_models.extend(tier.models)
        if len(all_models) != len(set(all_models)):
            seen: set[str] = set()
            dupes = [m for m in all_models if m in seen or seen.add(m)]  # type: ignore[func-returns-value]
            raise ValueError(f"Duplicate models across tiers: {dupes}")
        return self


# ── OpenCLAW Config (config/openclaw.json.example) ─────────────────────

class AgentIdentity(BaseModel):
    name: str
    theme: str = ""
    emoji: str = ""


class AgentEntry(BaseModel):
    id: str
    name: str
    workspace: str
    identity: AgentIdentity
    tools: AgentToolProfile | None = None


class ModelRef(BaseModel):
    primary: str


class AgentsDefaults(BaseModel):
    model: ModelRef
    thinkingDefault: ThinkingLevel = "off"
    verboseDefault: VerboseLevel = "on"
    workspace: str | None = None
    memorySearch: dict | None = None


class AgentBlock(BaseModel):
    defaults: AgentsDefaults
    agents: list[AgentEntry] = Field(default_factory=list, alias="list")

    model_config = {"populate_by_name": True}


class GatewayConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 18789


# ── Gateway runtime wiring (v0.5.0) ───────────────────────────────────

class AgentToolProfile(BaseModel):
    """Per-agent tool profile (profile name, allowlist, denylist)."""

    profile: str = "coding"
    allow: list[str] | None = None
    deny: list[str] | None = None


class ExecConfig(BaseModel):
    """Exec security configuration."""

    security: Literal["deny", "allowlist", "full"] = "allowlist"
    ask: str = "on-miss"
    host: str = "sandbox"


class LoopDetectionConfig(BaseModel):
    """Gateway-level loop / repetition circuit breaker."""

    enabled: bool = True
    warningThreshold: int = Field(default=10, ge=1)
    criticalThreshold: int = Field(default=20, ge=1)
    globalCircuitBreakerThreshold: int = Field(default=30, ge=1)


class AgentToAgentConfig(BaseModel):
    """Agent-to-agent routing configuration."""

    enabled: bool = True
    targetAllowlist: list[str] = Field(default_factory=list)


class SessionConfig(BaseModel):
    """Session policy (scope, reset, typing)."""

    scope: str = "per-sender"
    reset: dict = Field(default_factory=lambda: {"mode": "idle", "idleMinutes": 60})
    agentToAgent: dict = Field(default_factory=lambda: {"pingPongTurns": 3})
    typing: dict = Field(default_factory=lambda: {"mode": "thinking"})


class BrowserConfig(BaseModel):
    """Browser automation and SSRF policy."""

    enabled: bool = True
    headless: bool = True
    defaultProfile: str = "akos"
    ssrfPolicy: dict = Field(default_factory=lambda: {"dangerouslyAllowPrivateNetwork": False})


class OpenClawConfig(BaseModel):
    """Partial model covering the fields AKOS manages in openclaw.json."""
    gateway: GatewayConfig = Field(default_factory=GatewayConfig)
    agents: AgentBlock
    bindings: list[dict] = Field(default_factory=list)


# ── Environment Overlays (config/environments/*.json) ──────────────────

class OverlayDefaults(BaseModel):
    model: ModelRef
    thinkingDefault: ThinkingLevel
    verboseDefault: VerboseLevel = "on"


class OverlayAgents(BaseModel):
    defaults: OverlayDefaults


class RunPodHealthCheckConfig(BaseModel):
    intervalSeconds: int = Field(default=60, gt=0)
    unhealthyThreshold: int = Field(default=3, gt=0)


class RunPodEndpointConfig(BaseModel):
    """Schema for the ``runpod`` block in gpu-runpod.json."""

    gpuIds: list[str] = Field(default_factory=lambda: ["AMPERE_80"])
    templateName: str = "akos-vllm"
    vllmImage: str = "runpod/worker-v1-vllm:stable-cuda12.8.0"
    modelName: str = "deepseek-ai/DeepSeek-R1-0528-Distill-Qwen-70B"
    maxModelLen: int = Field(default=131072, gt=0)
    activeWorkers: int = Field(default=0, ge=0)
    maxWorkers: int = Field(default=2, ge=1)
    idleTimeoutSeconds: int = Field(default=300, ge=0)
    envVars: dict[str, str] = Field(default_factory=dict)
    healthCheck: RunPodHealthCheckConfig = Field(
        default_factory=RunPodHealthCheckConfig
    )


class EnvironmentOverlay(BaseModel):
    agents: OverlayAgents
    runpod: RunPodEndpointConfig | None = None


# ── Eval: Alerts (config/eval/alerts.json) ─────────────────────────────

class Alert(BaseModel):
    alert_id: str
    description: str
    condition: str
    evaluation_window: str
    severity: AlertSeverity
    sop_reference: str = ""
    action: str = ""

    def matches_realtime(self, log_entry: dict) -> bool:
        """Evaluate whether a single log entry triggers this alert.

        Supports a small DSL:
          - ``tool_name == 'X'``
          - ``command CONTAINS 'X'``
          - ``target_path STARTS_WITH 'X'``
          - ``target_path CONTAINS 'X'``
        """
        if self.evaluation_window != "real-time":
            return False
        return _eval_condition(self.condition, log_entry)


class Baseline(BaseModel):
    metric_id: str
    description: str = ""
    target_value: float | None = None
    comparator: str = ">="
    unit: str = "ratio"
    evaluation_window: str = "7d"
    sop_reference: str = ""

    def passes(self, value: float) -> bool:
        """Return True if *value* satisfies this baseline threshold."""
        if self.target_value is None:
            return True
        ops = {
            ">=": lambda v, t: v >= t,
            "<=": lambda v, t: v <= t,
            ">": lambda v, t: v > t,
            "<": lambda v, t: v < t,
            "==": lambda v, t: v == t,
            "maximize": lambda _v, _t: True,
        }
        check = ops.get(self.comparator)
        if check is None:
            return True
        return check(value, self.target_value)


# ── Helpers for loading validated configs ───────────────────────────────

def load_tiers(path: Path) -> ModelTiersRegistry:
    """Load and validate config/model-tiers.json."""
    from akos.io import load_json
    return ModelTiersRegistry.model_validate(load_json(path))


def load_alerts(path: Path) -> list[Alert]:
    """Load and validate config/eval/alerts.json."""
    from akos.io import load_json
    raw = load_json(path)
    return [Alert.model_validate(a) for a in raw]


def load_baselines(path: Path) -> list[Baseline]:
    """Load and validate config/eval/baselines.json."""
    from akos.io import load_json
    raw = load_json(path)
    return [Baseline.model_validate(b) for b in raw]


# ── Private: condition DSL evaluator ────────────────────────────────────

def _eval_condition(condition: str, entry: dict) -> bool:
    """Minimal evaluator for alert condition strings."""
    parts = [p.strip() for p in condition.split(" AND ")]
    for part in parts:
        if not _eval_single(part, entry):
            return False
    return True


def _eval_single(expr: str, entry: dict) -> bool:
    if " CONTAINS " in expr:
        field, value = expr.split(" CONTAINS ", 1)
        return value.strip("'\"") in str(entry.get(field.strip(), ""))
    if " STARTS_WITH " in expr:
        field, value = expr.split(" STARTS_WITH ", 1)
        return str(entry.get(field.strip(), "")).startswith(value.strip("'\""))
    if " == " in expr:
        field, value = expr.split(" == ", 1)
        return str(entry.get(field.strip(), "")) == value.strip("'\"")
    return False
