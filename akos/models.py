"""Pydantic models for all AKOS configuration schemas.

Provides runtime type safety, JSON Schema generation, and validation
for model-tiers.json, openclaw.json, environment overlays, alerts,
baselines, finance response envelopes, and HLK domain models.
"""

from __future__ import annotations

import warnings
from datetime import datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

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
    fallbacks: list[str] = Field(default_factory=list)


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


class ControlUiConfig(BaseModel):
    title: str = "HLK Intelligence Platform"


class GatewayConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 18789
    controlUi: ControlUiConfig = Field(default_factory=ControlUiConfig)


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

    model_config = ConfigDict(populate_by_name=True)
    enabled: bool = True
    allow: list[str] = Field(default_factory=list, alias="targetAllowlist")


class SessionConfig(BaseModel):
    """Session policy (scope, reset, typing)."""

    scope: str = "per-sender"
    reset: dict = Field(default_factory=lambda: {"mode": "idle", "idleMinutes": 60})
    agentToAgent: dict = Field(default_factory=lambda: {"maxPingPongTurns": 3})
    typingMode: str = "thinking"


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
    vllmImage: str = "runpod/worker-v1-vllm:v2.14.0"
    modelName: str = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B"
    maxModelLen: int = Field(default=131072, gt=0)
    activeWorkers: int = Field(default=0, ge=0)
    maxWorkers: int = Field(default=2, ge=1)
    idleTimeoutSeconds: int = Field(default=300, ge=0)
    envVars: dict[str, str] = Field(default_factory=dict)
    healthCheck: RunPodHealthCheckConfig = Field(
        default_factory=RunPodHealthCheckConfig
    )

    @model_validator(mode="after")
    def _check_tool_parser_consistency(self) -> RunPodEndpointConfig:
        auto_tool = self.envVars.get("ENABLE_AUTO_TOOL_CHOICE", "").lower()
        has_parser = "TOOL_CALL_PARSER" in self.envVars
        if auto_tool == "true" and not has_parser:
            warnings.warn(
                "ENABLE_AUTO_TOOL_CHOICE is true but TOOL_CALL_PARSER is not set; "
                "tool calls will silently fail",
                stacklevel=2,
            )
        return self

    @model_validator(mode="after")
    def _check_tensor_parallel_vs_gpus(self) -> RunPodEndpointConfig:
        tp_str = self.envVars.get("TENSOR_PARALLEL_SIZE")
        if tp_str is not None:
            try:
                tp = int(tp_str)
            except ValueError:
                tp = 1
            if tp > len(self.gpuIds):
                warnings.warn(
                    f"TENSOR_PARALLEL_SIZE={tp} exceeds len(gpuIds)={len(self.gpuIds)}; "
                    "sharding is misconfigured",
                    stacklevel=2,
                )
        return self

    @model_validator(mode="after")
    def _normalize_runpod_worker_compat(self) -> RunPodEndpointConfig:
        quant = self.envVars.get("QUANTIZATION", "").lower()
        dtype = self.envVars.get("DTYPE", "").lower()
        if quant == "awq" and dtype != "float16":
            warnings.warn(
                "RunPod AWQ deployments require DTYPE=float16; forcing DTYPE=float16",
                stacklevel=2,
            )
            self.envVars["DTYPE"] = "float16"

        image = self.vllmImage.lower()
        kv_dtype = self.envVars.get("KV_CACHE_DTYPE", "").lower()
        if image.startswith("runpod/worker-v1-vllm") and kv_dtype == "fp8":
            warnings.warn(
                "runpod/worker-v1-vllm with KV_CACHE_DTYPE=fp8 may fail startup "
                "(FlashInfer JIT requires nvcc). Forcing KV_CACHE_DTYPE=auto and "
                "VLLM_ATTENTION_BACKEND=TRITON_ATTN",
                stacklevel=2,
            )
            self.envVars["KV_CACHE_DTYPE"] = "auto"
            self.envVars.setdefault("VLLM_ATTENTION_BACKEND", "TRITON_ATTN")
        return self


class PodConfig(BaseModel):
    """Schema for the ``pod`` block in gpu-runpod-pod.json (dedicated pods)."""

    mode: Literal["dedicated"] = "dedicated"
    healthEndpoint: str = "/health"
    vllmPort: int = Field(default=8080, gt=0)
    envVars: dict[str, str] = Field(default_factory=dict)
    modelName: str = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B"
    maxModelLen: int = Field(default=131072, gt=0)
    gpuType: str = Field(default="NVIDIA A100-SXM4-80GB", description="RunPod GPU type ID for pod creation")
    gpuCount: int = Field(default=2, ge=1, description="Number of GPUs; also sets tensor-parallel-size")
    containerImage: str = Field(default="vllm/vllm-openai:v0.16.0")
    containerDiskGb: int = Field(default=100, ge=20)
    volumeGb: int = Field(default=200, ge=50)

    @model_validator(mode="after")
    def _sync_tensor_parallel_with_gpu_count(self) -> PodConfig:
        """TENSOR_PARALLEL_SIZE must equal gpuCount to avoid the world-size error."""
        self.envVars["TENSOR_PARALLEL_SIZE"] = str(self.gpuCount)
        return self

    @model_validator(mode="after")
    def _normalize_awq_dtype(self) -> PodConfig:
        quant = self.envVars.get("QUANTIZATION", "").lower()
        dtype = self.envVars.get("DTYPE", "").lower()
        if quant == "awq" and dtype != "float16":
            warnings.warn(
                "AWQ quantization requires DTYPE=float16; forcing DTYPE=float16",
                stacklevel=2,
            )
            self.envVars["DTYPE"] = "float16"
        return self

    def build_vllm_command(self) -> list[str]:
        """Build CMD args for the ``vllm/vllm-openai`` container image.

        The image has ``ENTRYPOINT ["python3", "-m", "vllm.entrypoints.openai.api_server"]``,
        so dockerStartCmd must be ``["--model", "<hf_id>", "--host", ...]``.
        """
        env = self.envVars
        args = [
            "--model", self.modelName,
            "--host", "0.0.0.0",
            "--port", str(self.vllmPort),
            "--max-model-len", str(self.maxModelLen),
            "--served-model-name", env.get("OPENAI_SERVED_MODEL_NAME_OVERRIDE", self.modelName.split("/")[-1]),
            "--dtype", env.get("DTYPE", "bfloat16"),
            "--gpu-memory-utilization", env.get("GPU_MEMORY_UTILIZATION", "0.92"),
            "--kv-cache-dtype", env.get("KV_CACHE_DTYPE", "fp8"),
            "--tensor-parallel-size", str(self.gpuCount),
        ]
        if env.get("QUANTIZATION"):
            args.extend(["--quantization", env["QUANTIZATION"]])
        if env.get("ENFORCE_EAGER", "").lower() == "true":
            args.append("--enforce-eager")
        if env.get("ENABLE_PREFIX_CACHING", "").lower() == "true":
            args.append("--enable-prefix-caching")
        if env.get("ENABLE_CHUNKED_PREFILL", "").lower() == "true":
            args.append("--enable-chunked-prefill")
        if env.get("ENABLE_AUTO_TOOL_CHOICE", "").lower() == "true":
            args.append("--enable-auto-tool-choice")
            if env.get("TOOL_CALL_PARSER"):
                args.extend(["--tool-call-parser", env["TOOL_CALL_PARSER"]])
        if env.get("REASONING_PARSER"):
            args.extend(["--reasoning-parser", env["REASONING_PARSER"]])
        if env.get("CHAT_TEMPLATE"):
            args.extend(["--chat-template", env["CHAT_TEMPLATE"]])
        if env.get("MAX_NUM_BATCHED_TOKENS"):
            args.extend(["--max-num-batched-tokens", env["MAX_NUM_BATCHED_TOKENS"]])
        args.extend(["--max-num-seqs", env.get("MAX_NUM_SEQS", "128")])
        return args


class OpenStackInstanceConfig(BaseModel):
    """Schema for the ``openstack`` block in gpu-shadow.json."""

    region: str = Field(default="FRDUN02", description="ShadowPC OpenStack region")
    authUrl: str = Field(default="", description="Keystone v3 auth URL")
    flavor: str = Field(default="", description="Nova flavor for guaranteed instances")
    spotFlavor: str = Field(default="", description="Nova flavor for spot/preemptible instances")
    image: str = Field(default="Ubuntu 22.04 LTS", description="Glance image name or ID")
    network: str = Field(default="default", description="Neutron network name or ID")
    securityGroup: str = Field(default="akos-vllm", description="Security group name")
    vllmPort: int = Field(default=8080, gt=0)
    gpuType: str = Field(default="RTX A4500", description="GPU type for display/catalog")
    gpuCount: int = Field(default=4, ge=1, description="Number of GPUs in the flavor")
    gpuVramGb: int = Field(default=20, gt=0, description="VRAM per GPU in GB")
    volumeGb: int = Field(default=200, ge=50)
    envVars: dict[str, str] = Field(default_factory=dict)
    modelName: str = "casperhansen/deepseek-r1-distill-llama-70b-awq"
    maxModelLen: int = Field(default=32768, gt=0)


class EnvironmentOverlay(BaseModel):
    agents: OverlayAgents
    runpod: RunPodEndpointConfig | None = None
    pod: PodConfig | None = None
    openstack: OpenStackInstanceConfig | None = None


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


# ── Finance Response Envelope ───────────────────────────────────────────

FinanceStatus = Literal["ok", "degraded", "not_found", "rate_limited", "error"]


class QuoteData(BaseModel):
    """Normalized quote bundle returned by finance_quote."""

    ticker: str
    last_price: float | None = None
    change_amount: float | None = None
    change_percent: float | None = None
    day_high: float | None = None
    day_low: float | None = None
    open_price: float | None = None
    previous_close: float | None = None
    volume: int | None = None
    market_cap: float | None = None
    currency: str = "USD"
    exchange: str = ""


class SearchResult(BaseModel):
    """A single ticker match returned by finance_search."""

    ticker: str
    name: str
    match_reason: str = ""
    exchange: str = ""
    asset_type: str = ""


class SentimentItem(BaseModel):
    """A single sentiment entry from news analysis."""

    headline: str
    sentiment: str = ""
    relevance: float | None = None
    source: str = ""


class FinanceResponse(BaseModel):
    """Schema-locked envelope for all finance tool responses.

    The MCP server serialises this to JSON; the agent turns it into
    natural language.  Tests and the service layer share this contract.
    """

    status: FinanceStatus
    source: str = ""
    as_of: datetime | None = None
    freshness: str = ""
    warnings: list[str] = Field(default_factory=list)
    quotes: list[QuoteData] | None = None
    search_results: list[SearchResult] | None = None
    sentiment: list[SentimentItem] | None = None
    error_detail: str = ""


# ── HLK Domain Models ───────────────────────────────────────────────────

AccessLevel = Literal[0, 1, 2, 3, 4, 5, 6]
ConfidenceLevel = Literal[1, 2, 3]
SourceCategory = Literal["OSINT", "HUMINT", "SIGINT", "CORPINT", "MOTINT", "TBD"]
ProcessGranularity = Literal["project", "workstream", "process", "task"]
HlkStatus = Literal["ok", "not_found", "error"]


class OrgRole(BaseModel):
    """A single role from the HLK baseline organisation."""

    org_uuid: str = ""
    role_name: str
    role_description: str = ""
    role_full_description: str = ""
    access_level: int = 0
    reports_to: str = ""
    area: str = ""
    entity: str = ""
    org_id: str = ""
    sop_url: str = ""
    responsible_processes: str = ""
    components_used: str = ""


class ProcessItem(BaseModel):
    """A single item from the HLK process list."""

    type: str = "Internal"
    orientation: str = "Employee"
    entity: str = ""
    area: str = ""
    role_parent_1: str = ""
    role_owner: str = ""
    item_parent_2: str = ""
    item_parent_1: str = ""
    item_name: str = ""
    item_id: str = ""
    item_granularity: str = ""
    time_hours_par: str = ""
    description: str = ""
    instructions: str = ""
    addundum_extras: str = ""
    confidence: str = ""
    count_name: str = ""
    frequency: str = ""
    quality: str = ""


class HlkResponse(BaseModel):
    """Schema-locked envelope for all HLK registry responses.

    Mirrors the FinanceResponse pattern: a status field, optional typed
    payloads, warnings for degraded results, and an error_detail string.
    """

    status: HlkStatus
    roles: list[OrgRole] | None = None
    processes: list[ProcessItem] | None = None
    best_role: OrgRole | None = None
    best_process: ProcessItem | None = None
    role_count: int | None = None
    process_count: int | None = None
    normalized_query: str = ""
    resolution_strategy: str = ""
    warnings: list[str] = Field(default_factory=list)
    error_detail: str = ""


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

