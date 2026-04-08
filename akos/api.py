"""FastAPI control plane for AKOS.

Exposes REST endpoints for system health, model switching, RunPod
management, agent status, metrics, alerts, and a live log WebSocket.

Launch: ``python scripts/serve-api.py --port 8420``
"""

from __future__ import annotations

import asyncio
import importlib.util
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any

import httpx
from fastapi import Depends, FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from akos.finance import FinanceService
from akos.io import (
    AGENT_WORKSPACES,
    REPO_ROOT,
    load_json,
    resolve_openclaw_home,
)
from akos.models import RunPodEndpointConfig, load_tiers
from akos.runpod_provider import RunPodProvider
from akos.state import load_state
from akos.telemetry import LangfuseReporter

logger = logging.getLogger("akos.api")

app = FastAPI(
    title="HLK Operations Platform",
    version="0.4.1",
    description="REST API for the Holistika Intelligence Platform (AKOS)",
    openapi_tags=[
        {"name": "Health", "description": "System health and readiness"},
        {"name": "Agents", "description": "Agent listing, policy, and capability audit"},
        {"name": "Runtime", "description": "Runtime drift and environment switching"},
        {"name": "Context", "description": "Context pinning for agent focus"},
        {"name": "RunPod", "description": "RunPod GPU infrastructure management"},
        {"name": "Metrics", "description": "DX baselines, cost tracking, and alerts"},
        {"name": "Prompts", "description": "Prompt assembly and deployment"},
        {"name": "Checkpoints", "description": "Workspace snapshot management"},
        {"name": "Finance", "description": "Read-only finance research endpoints"},
        {"name": "HLK", "description": "HLK organisation, process, and compliance registry"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── API Key Authentication ────────────────────────────────────────────

_api_key: str | None = os.environ.get("AKOS_API_KEY")


def _check_api_key(request: Request) -> None:
    """Enforce bearer token auth when AKOS_API_KEY is set."""
    if not _api_key:
        return
    if request.url.path == "/health":
        return
    auth_header = request.headers.get("authorization", "")
    if not auth_header.startswith("Bearer ") or auth_header[7:] != _api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

# ── Lazy singletons ─────────────────────────────────────────────────

_runpod: RunPodProvider | None = None
_reporter: LangfuseReporter | None = None
_finance: FinanceService | None = None


def _get_runpod() -> RunPodProvider:
    global _runpod
    if _runpod is None:
        config_path = REPO_ROOT / "config" / "environments" / "gpu-runpod.json"
        rpconfig = None
        if config_path.exists():
            raw = load_json(config_path)
            rp_block = raw.get("runpod")
            if rp_block:
                rpconfig = RunPodEndpointConfig.model_validate(rp_block)
        _runpod = RunPodProvider(rpconfig)
    return _runpod


def _get_reporter() -> LangfuseReporter:
    global _reporter
    if _reporter is None:
        _reporter = LangfuseReporter()
    return _reporter


def _get_finance() -> FinanceService:
    global _finance
    if _finance is None:
        _finance = FinanceService()
    return _finance


# ── Request/Response Models ──────────────────────────────────────────


class SwitchRequest(BaseModel):
    environment: str
    dry_run: bool = False


class ScaleRequest(BaseModel):
    min_workers: int = Field(ge=0)
    max_workers: int = Field(ge=1)


class AssembleRequest(BaseModel):
    variant: str | None = None


class HealthResponse(BaseModel):
    status: str
    gateway: str
    runpod: str
    vllm: str
    langfuse: str
    uptime_seconds: float


class StatusResponse(BaseModel):
    environment: str
    model: str
    tier: str
    variant: str
    last_switch: str
    last_switch_success: bool
    hint: str | None = None


class AgentInfo(BaseModel):
    id: str
    name: str
    workspace: str
    soul_md_exists: bool
    soul_md_chars: int


# ── Startup timestamp ───────────────────────────────────────────────

_start_time = time.monotonic()

if not _api_key:
    logger.warning(
        "AKOS_API_KEY not set -- API endpoints are unauthenticated. "
        "Set AKOS_API_KEY env var for production use."
    )


# ── Health ───────────────────────────────────────────────────────────


async def _gateway_health() -> str:
    """Probe the OpenCLAW gateway health endpoint."""
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            resp = await client.get("http://127.0.0.1:18789/api/health")
            if resp.status_code == 200:
                return "up"
            return f"degraded (HTTP {resp.status_code})"
    except httpx.ConnectError:
        return "unreachable"
    except Exception as exc:
        return f"error ({type(exc).__name__})"


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def get_health() -> HealthResponse:
    gateway_status = await _gateway_health()

    rp = _get_runpod()
    rp_status = "disabled"
    if rp.enabled:
        health = rp.health_check()
        rp_status = "healthy" if health.healthy else "unhealthy"

    vllm_url = os.environ.get("VLLM_RUNPOD_URL", "")
    vllm_status = "not-configured"
    if vllm_url:
        from akos.runpod_provider import RunPodProvider
        probe = RunPodProvider.probe_vllm_health(vllm_url, timeout=3.0)
        vllm_status = "healthy" if probe.healthy else "unhealthy"

    reporter = _get_reporter()
    lf_status = "enabled" if reporter.enabled else "disabled"

    return HealthResponse(
        status="ok",
        gateway=gateway_status,
        runpod=rp_status,
        vllm=vllm_status,
        langfuse=lf_status,
        uptime_seconds=time.monotonic() - _start_time,
    )


# ── Status ───────────────────────────────────────────────────────────


@app.get("/status", response_model=StatusResponse, dependencies=[Depends(_check_api_key)], tags=["Health"])
async def get_status() -> StatusResponse:
    oc_home = resolve_openclaw_home()
    state = load_state(oc_home)
    hint = None
    if not state.activeEnvironment:
        hint = "No environment selected. Run: py scripts/switch-model.py dev-local"
    return StatusResponse(
        environment=state.activeEnvironment or "unknown",
        model=state.activeModel or "unknown",
        tier=state.activeTier or "unknown",
        variant=state.activeVariant or "unknown",
        last_switch=state.lastSwitchTimestamp or "",
        last_switch_success=state.lastSwitchSuccess,
        hint=hint,
    )


# ── Agents ───────────────────────────────────────────────────────────


@app.get("/agents", response_model=list[AgentInfo], dependencies=[Depends(_check_api_key)], tags=["Agents"])
async def list_agents() -> list[AgentInfo]:
    oc_home = resolve_openclaw_home()
    agents: list[AgentInfo] = []
    for agent_name, ws_dir in AGENT_WORKSPACES.items():
        ws_path = oc_home / ws_dir
        soul = ws_path / "SOUL.md"
        agents.append(
            AgentInfo(
                id=agent_name.lower(),
                name=agent_name,
                workspace=str(ws_path),
                soul_md_exists=soul.exists(),
                soul_md_chars=len(soul.read_text(encoding="utf-8")) if soul.exists() else 0,
            )
        )
    return agents


# ── Runtime Drift ────────────────────────────────────────────────────


@app.get(
    "/runtime/drift",
    dependencies=[Depends(_check_api_key)],
    tags=["Runtime"],
    summary="Detect runtime drift",
    description="Compares the repo's intended state (agent count, workspace files, MCP servers, permissions) against the live runtime and reports mismatches.",
)
async def runtime_drift() -> dict[str, Any]:
    """Compare repo intended state against live runtime."""
    mod = _load_check_drift_module()
    if mod is not None:
        issues = mod.run_drift_check()
        return {"drift_detected": len(issues) > 0, "issues": issues}
    return {"error": "check-drift.py not found"}


def _load_check_drift_module():
    """Load the drift-check script as a module for API reuse."""
    spec = importlib.util.spec_from_file_location(
        "check_drift", REPO_ROOT / "scripts" / "check-drift.py"
    )
    if not spec or not spec.loader:
        return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _get_agent_capability_drift_issues(agent_id: str) -> list[dict[str, Any]]:
    """Return drift issues relevant to one agent role."""
    mod = _load_check_drift_module()
    if mod is None:
        return [{
            "type": "drift_probe_unavailable",
            "agent": agent_id,
            "detail": "check-drift.py not found",
        }]

    normalized_agent = agent_id.lower()
    issues = mod.run_drift_check()
    relevant: list[dict[str, Any]] = []
    for issue in issues:
        issue_agent = str(issue.get("agent", "")).lower()
        if issue_agent == normalized_agent:
            relevant.append(issue)
            continue

        if issue.get("type") == "agent_inventory_drift":
            actual = {str(name).lower() for name in issue.get("actual", [])}
            expected = {str(name).lower() for name in issue.get("expected", [])}
            if normalized_agent not in actual or normalized_agent not in expected:
                relevant.append(issue)

    return relevant


# ── Policy Audit ─────────────────────────────────────────────────────


@app.get("/agents/{agent_id}/policy", dependencies=[Depends(_check_api_key)], tags=["Agents"])
async def agent_policy(agent_id: str) -> dict[str, Any]:
    """Return the effective capability policy for an agent role."""
    from akos.policy import CapabilityMatrix
    matrix = CapabilityMatrix.load()
    policy = matrix.get_policy(agent_id)
    if not policy:
        return {"error": f"Unknown agent role: {agent_id}", "available": list(matrix.roles.keys())}
    return {
        "role": policy.role,
        "description": policy.description,
        "allowed_tools": policy.allowed_tools,
        "denied_tools": policy.denied_tools,
        "allowed_categories": policy.allowed_categories,
        "runtime_profile": policy.runtime_profile,
    }


@app.get("/agents/{agent_id}/capability-drift", dependencies=[Depends(_check_api_key)], tags=["Agents"])
async def agent_capability_drift(agent_id: str) -> dict[str, Any]:
    """Check if an agent's runtime tools match its policy."""
    from akos.policy import CapabilityMatrix
    matrix = CapabilityMatrix.load()
    policy = matrix.get_policy(agent_id)
    if not policy:
        return {"error": f"Unknown agent role: {agent_id}"}
    issues = _get_agent_capability_drift_issues(agent_id)
    return {
        "role": policy.role,
        "runtime_profile": policy.runtime_profile,
        "drift_issues": issues,
        "policy_enforced": len(issues) == 0,
    }


# ── Model Switching ──────────────────────────────────────────────────


@app.post("/switch", dependencies=[Depends(_check_api_key)], tags=["Runtime"])
async def switch_environment(req: SwitchRequest) -> dict[str, Any]:
    from akos.io import deep_merge, deploy_soul_prompts, get_variant_for_model, save_json

    envs_dir = REPO_ROOT / "config" / "environments"
    overlay_path = envs_dir / f"{req.environment}.json"
    if not overlay_path.exists():
        available = [p.stem for p in envs_dir.glob("*.json")]
        return {"error": f"Environment not found: {req.environment}", "available": available}

    overlay = load_json(overlay_path)
    tiers_path = REPO_ROOT / "config" / "model-tiers.json"
    registry = load_tiers(tiers_path)

    model_id = overlay.get("agents", {}).get("defaults", {}).get("model", {}).get("primary", "")
    variant = get_variant_for_model(registry, model_id, default="full")
    tier_result = registry.lookup_tier(model_id)
    tier_name = tier_result[0] if tier_result else "unknown"

    if req.dry_run:
        return {
            "dry_run": True,
            "environment": req.environment,
            "model": model_id,
            "tier": tier_name,
            "variant": variant,
        }

    oc_home = resolve_openclaw_home()
    oc_config = oc_home / "openclaw.json"
    if oc_config.exists():
        existing = load_json(oc_config)
        merged = deep_merge(existing, overlay)
        save_json(oc_config, merged)

    assembled = REPO_ROOT / "prompts" / "assembled"
    try:
        deploy_soul_prompts(assembled, variant, oc_home)
    except FileNotFoundError as exc:
        return {"error": str(exc)}

    from akos.state import record_switch
    record_switch(oc_home, environment=req.environment, model=model_id, tier=tier_name, variant=variant, success=True)

    return {
        "switched": True,
        "environment": req.environment,
        "model": model_id,
        "tier": tier_name,
        "variant": variant,
    }


# ── RunPod ───────────────────────────────────────────────────────────


@app.get("/runpod/health", dependencies=[Depends(_check_api_key)], tags=["RunPod"])
async def runpod_health() -> dict[str, Any]:
    rp = _get_runpod()
    if not rp.enabled:
        return {"enabled": False}
    health = rp.health_check()
    return {
        "enabled": True,
        "healthy": health.healthy,
        "workers_ready": health.workers_ready,
        "workers_running": health.workers_running,
        "queue_depth": health.queue_depth,
    }


@app.post("/runpod/scale", dependencies=[Depends(_check_api_key)], tags=["RunPod"])
async def runpod_scale(req: ScaleRequest) -> dict[str, Any]:
    rp = _get_runpod()
    if not rp.enabled:
        return {"error": "RunPod provider not enabled"}
    success = rp.scale(req.min_workers, req.max_workers)
    return {"scaled": success, "min": req.min_workers, "max": req.max_workers}


# ── Context Pinning ──────────────────────────────────────────────────


class PinRequest(BaseModel):
    path: str
    label: str | None = None


_pinned_context: list[dict[str, str]] = []


@app.post("/context/pin", dependencies=[Depends(_check_api_key)], tags=["Context"])
async def pin_context(req: PinRequest) -> dict[str, Any]:
    """Pin a file or resource for agent context focus."""
    entry = {"path": req.path, "label": req.label or req.path}
    if entry not in _pinned_context:
        _pinned_context.append(entry)
    return {"pinned": True, "total": len(_pinned_context), "items": _pinned_context}


@app.delete("/context/pin", dependencies=[Depends(_check_api_key)], tags=["Context"])
async def unpin_context(req: PinRequest) -> dict[str, Any]:
    """Remove a pinned context entry."""
    entry = {"path": req.path, "label": req.label or req.path}
    if entry in _pinned_context:
        _pinned_context.remove(entry)
    return {"unpinned": True, "total": len(_pinned_context), "items": _pinned_context}


@app.get("/context/pins", dependencies=[Depends(_check_api_key)], tags=["Context"])
async def list_pins() -> dict[str, Any]:
    """List all pinned context entries."""
    return {"total": len(_pinned_context), "items": _pinned_context}


# ── Request Routing ────────────────────────────────────────────────────


@app.get("/routing/classify", dependencies=[Depends(_check_api_key)], tags=["Runtime"])
async def classify_routing_request(q: str = "") -> dict[str, Any]:
    """Classify a user request into a deterministic flagship route."""
    if not q.strip():
        raise HTTPException(400, "Query parameter 'q' is required")
    from akos.intent import classify_request
    return classify_request(q)


# ── Metrics & Alerts ─────────────────────────────────────────────────


@app.get("/metrics", dependencies=[Depends(_check_api_key)], tags=["Metrics"])
async def get_metrics() -> dict[str, Any]:
    baselines_path = REPO_ROOT / "config" / "eval" / "baselines.json"
    if not baselines_path.exists():
        return {"baselines": []}
    raw = load_json(baselines_path)
    return {"baselines": raw}


@app.get("/metrics/cost", dependencies=[Depends(_check_api_key)], tags=["Metrics"])
async def get_cost_metrics() -> dict[str, Any]:
    """Cost breakdown by agent and environment (placeholder for Langfuse integration)."""
    return {
        "note": "Cost tracking requires Langfuse integration. Set LANGFUSE_* in process env or ~/.openclaw/.env.",
        "breakdown": {
            "by_agent": {},
            "by_environment": {},
            "by_model": {},
            "total_estimated": 0.0,
        },
    }


@app.get("/alerts", dependencies=[Depends(_check_api_key)], tags=["Metrics"])
async def get_alerts() -> dict[str, Any]:
    alerts_path = REPO_ROOT / "config" / "eval" / "alerts.json"
    if not alerts_path.exists():
        return {"alerts": []}
    raw = load_json(alerts_path)
    return {"alerts": raw}


# ── Prompt Assembly ──────────────────────────────────────────────────


@app.post("/prompts/assemble", dependencies=[Depends(_check_api_key)], tags=["Prompts"])
async def assemble_prompts(req: AssembleRequest) -> dict[str, Any]:
    import subprocess
    cmd = ["py", str(REPO_ROOT / "scripts" / "assemble-prompts.py")]
    if req.variant:
        cmd.extend(["--variant", req.variant])
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return {
        "success": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


# ── Checkpoints ──────────────────────────────────────────────────────


class CheckpointRequest(BaseModel):
    name: str
    workspace: str


class RestoreRequest(BaseModel):
    name: str
    workspace: str


@app.post("/checkpoints", dependencies=[Depends(_check_api_key)], tags=["Checkpoints"])
async def create_checkpoint_endpoint(req: CheckpointRequest) -> dict[str, Any]:
    from akos.checkpoints import create_checkpoint
    try:
        info = create_checkpoint(req.name, Path(req.workspace))
        return {
            "created": True,
            "name": info.name,
            "path": info.path,
            "size_bytes": info.size_bytes,
        }
    except FileNotFoundError as exc:
        return {"error": str(exc)}


@app.get("/checkpoints", dependencies=[Depends(_check_api_key)], tags=["Checkpoints"])
async def list_checkpoints_endpoint(workspace: str) -> dict[str, Any]:
    from akos.checkpoints import list_checkpoints
    items = list_checkpoints(Path(workspace))
    return {
        "checkpoints": [
            {
                "name": c.name,
                "created_at": c.created_at,
                "size_bytes": c.size_bytes,
                "path": c.path,
            }
            for c in items
        ]
    }


@app.post("/checkpoints/restore", dependencies=[Depends(_check_api_key)], tags=["Checkpoints"])
async def restore_checkpoint_endpoint(req: RestoreRequest) -> dict[str, Any]:
    from akos.checkpoints import restore_checkpoint
    success = restore_checkpoint(req.name, Path(req.workspace))
    return {"restored": success, "name": req.name}


# ── Live Log WebSocket ──────────────────────────────────────────────


# ── HLK Registry Endpoints ──────────────────────────────────────────────


@app.get("/finance/quote/{ticker}", tags=["Finance"], dependencies=[Depends(_check_api_key)])
def finance_quote(ticker: str):
    """Return a quote bundle for one ticker symbol."""
    return _get_finance().get_quote(ticker).model_dump(exclude_none=True)


@app.get("/finance/search", tags=["Finance"], dependencies=[Depends(_check_api_key)])
def finance_search(q: str = ""):
    """Resolve a company name or partial ticker to matching symbols."""
    if not q.strip():
        raise HTTPException(400, "Query parameter 'q' is required")
    return _get_finance().search_ticker(q).model_dump(exclude_none=True)


@app.get("/finance/sentiment", tags=["Finance"], dependencies=[Depends(_check_api_key)])
def finance_sentiment(tickers: str = ""):
    """Return recent news sentiment for one or more ticker symbols."""
    if not tickers.strip():
        raise HTTPException(400, "Query parameter 'tickers' is required")
    return _get_finance().get_sentiment(tickers).model_dump(exclude_none=True)


@app.get("/hlk/roles", tags=["HLK"], dependencies=[Depends(_check_api_key)])
def hlk_roles():
    """Return all roles in the HLK baseline organisation."""
    from akos.hlk import get_hlk_registry
    reg = get_hlk_registry()
    return {"status": "ok", "roles": [r.model_dump() for r in reg._roles], "role_count": len(reg._roles)}


@app.get("/hlk/roles/{role_name}", tags=["HLK"], dependencies=[Depends(_check_api_key)])
def hlk_role(role_name: str):
    """Look up a single role by name."""
    from akos.hlk import get_hlk_registry
    return get_hlk_registry().get_role(role_name).model_dump()


@app.get("/hlk/roles/{role_name}/chain", tags=["HLK"], dependencies=[Depends(_check_api_key)])
def hlk_role_chain(role_name: str):
    """Traverse the reports_to chain from a role up to Admin."""
    from akos.hlk import get_hlk_registry
    return get_hlk_registry().get_role_chain(role_name).model_dump()


@app.get("/hlk/areas", tags=["HLK"], dependencies=[Depends(_check_api_key)])
def hlk_areas():
    """Return area summary with role counts."""
    from akos.hlk import get_hlk_registry
    return get_hlk_registry().list_areas().model_dump()


@app.get("/hlk/areas/{area}", tags=["HLK"], dependencies=[Depends(_check_api_key)])
def hlk_area_roles(area: str):
    """Return all roles in a given area."""
    from akos.hlk import get_hlk_registry
    return get_hlk_registry().get_area_roles(area).model_dump()


@app.get("/hlk/processes", tags=["HLK"], dependencies=[Depends(_check_api_key)])
def hlk_projects():
    """Return project summary with child counts."""
    from akos.hlk import get_hlk_registry
    return get_hlk_registry().get_project_summary().model_dump()


@app.get("/hlk/processes/{item_id}", tags=["HLK"], dependencies=[Depends(_check_api_key)])
def hlk_process(item_id: str):
    """Look up a single process item by ID."""
    from akos.hlk import get_hlk_registry
    return get_hlk_registry().get_process(item_id).model_dump()


@app.get("/hlk/processes/{item_name}/tree", tags=["HLK"], dependencies=[Depends(_check_api_key)])
def hlk_process_tree(item_name: str):
    """Return all direct children of a process item."""
    from akos.hlk import get_hlk_registry
    return get_hlk_registry().get_process_tree(item_name).model_dump()


@app.get("/hlk/gaps", tags=["HLK"], dependencies=[Depends(_check_api_key)])
def hlk_gaps():
    """Identify items with missing metadata, TBD owners, or empty descriptions."""
    from akos.hlk import get_hlk_registry
    return get_hlk_registry().get_gaps().model_dump()


@app.get("/hlk/search", tags=["HLK"], dependencies=[Depends(_check_api_key)])
def hlk_search(q: str = ""):
    """Fuzzy search across roles and processes."""
    if not q.strip():
        raise HTTPException(400, "Query parameter 'q' is required")
    from akos.hlk import get_hlk_registry
    return get_hlk_registry().search(q).model_dump()


@app.websocket("/logs")
async def log_stream(websocket: WebSocket) -> None:
    """Stream gateway log entries as JSON over WebSocket."""
    await websocket.accept()
    import tempfile
    from datetime import date

    log_path = Path(tempfile.gettempdir()) / "openclaw" / f"openclaw-{date.today().isoformat()}.log"

    try:
        if not log_path.exists():
            await websocket.send_json({"info": f"Waiting for {log_path}"})
            while not log_path.exists():
                await asyncio.sleep(2)

        with open(log_path, "r", encoding="utf-8", errors="replace") as f:
            f.seek(0, 2)
            while True:
                line = f.readline()
                if line:
                    line = line.strip()
                    if line:
                        try:
                            entry = json.loads(line)
                            await websocket.send_json(entry)
                        except json.JSONDecodeError:
                            await websocket.send_json({"raw": line})
                else:
                    await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass
