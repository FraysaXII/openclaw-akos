"""CLI-facing spike runner with Langfuse + research-action fixture validation."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

from akos.langgraph_spike.graph import SUBSTRATE_ADAPTER_ID, run_spike_graph
from akos.models import LangfuseTraceContext

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FIXTURE = (
    REPO_ROOT
    / "docs/wip/intelligence/madeira-brand-capability-harmonization-v32-alpha-2026-06-14/source-ledger.csv"
)


@dataclass
class SpikeRunResult:
    status: str
    engine: str
    substrate_adapter_id: str
    capability_ids: list[str]
    sources_ingested: int
    sources_rated: int
    synthesis_summary: str
    mcp_read_posture: str
    mcp_tool: str
    research_action_validation: str
    langfuse_enabled: bool
    elapsed_ms: int
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def _validate_fixture(path: Path) -> str:
    script = REPO_ROOT / "scripts/validate_research_action.py"
    if not script.is_file():
        return "SKIP:validate_script_missing"
    proc = subprocess.run(
        [sys.executable, str(script), "--source-ledger", str(path)],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        timeout=120,
        check=False,
    )
    if proc.returncode == 0:
        return "PASS"
    tail = (proc.stderr or proc.stdout or "")[-400:]
    return f"FAIL:{tail.strip()[:200]}"


def _emit_langfuse(state: dict, *, fixture_path: Path) -> bool:
    try:
        from akos.telemetry import LangfuseReporter
    except ImportError:
        return False

    ctx = LangfuseTraceContext(
        alpha_scenario="scenario_b_research",
        substrate_adapter_id=SUBSTRATE_ADAPTER_ID,
        cache_read_tokens="0",
        cache_write_tokens="0",
        eval_suite="langgraph_spike",
    )
    meta = ctx.to_metadata()
    meta["fixture_path"] = str(fixture_path.name)
    meta["sources_ingested"] = str(state.get("sources_ingested", 0))
    meta["mcp_read_posture"] = str(state.get("mcp_read_posture", ""))

    reporter = LangfuseReporter()
    if not reporter.enabled:
        return False

    with reporter._client.start_as_current_observation(  # noqa: SLF001 — spike uses same pattern as telemetry
        as_type="span",
        name="langgraph_spike_run",
        metadata=meta,
    ):
        pass
    reporter.shutdown()
    return True


def run_research_action_spike(
    fixture_path: Path | None = None,
    *,
    emit_langfuse: bool = True,
    require_langgraph: bool = False,
) -> SpikeRunResult:
    path = fixture_path or DEFAULT_FIXTURE
    if not path.is_file():
        return SpikeRunResult(
            status="FAIL",
            engine="none",
            substrate_adapter_id=SUBSTRATE_ADAPTER_ID,
            capability_ids=[],
            sources_ingested=0,
            sources_rated=0,
            synthesis_summary="",
            mcp_read_posture="",
            mcp_tool="",
            research_action_validation="FAIL:fixture_missing",
            langfuse_enabled=False,
            elapsed_ms=0,
            notes=[f"fixture not found: {path}"],
        )

    t0 = time.perf_counter()
    notes: list[str] = []
    state, engine = run_spike_graph(path)
    if engine == "mock":
        notes.append("LangGraph package not installed; used deterministic mock graph.")
    if require_langgraph and engine != "langgraph":
        notes.append(
            "require_langgraph: FAIL — real LangGraph package required "
            "(shadow box needs Python 3.13 per .python-version; see SRC-MBH-EXT-040)."
        )

    validation = _validate_fixture(path)
    langfuse_ok = False
    if emit_langfuse:
        langfuse_ok = _emit_langfuse(state, fixture_path=path)
        if not langfuse_ok:
            notes.append("Langfuse no-op (credentials absent or package missing).")

    elapsed = int((time.perf_counter() - t0) * 1000)
    status = "PASS" if validation == "PASS" and state.get("sources_ingested", 0) > 0 else "FAIL"
    if require_langgraph and engine != "langgraph":
        status = "FAIL"

    return SpikeRunResult(
        status=status,
        engine=engine,
        substrate_adapter_id=str(state.get("substrate_adapter_id", SUBSTRATE_ADAPTER_ID)),
        capability_ids=list(state.get("capability_ids") or []),
        sources_ingested=int(state.get("sources_ingested", 0)),
        sources_rated=int(state.get("sources_rated", 0)),
        synthesis_summary=str(state.get("synthesis_summary", "")),
        mcp_read_posture=str(state.get("mcp_read_posture", "")),
        mcp_tool=str(state.get("mcp_tool", "")),
        research_action_validation=validation,
        langfuse_enabled=langfuse_ok,
        elapsed_ms=elapsed,
        notes=notes,
    )


def write_evidence_artifact(result: SpikeRunResult, out_dir: Path | None = None) -> Path:
    target = out_dir or (REPO_ROOT / "artifacts" / "langgraph-spike")
    target.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    path = target / f"langgraph-spike-{stamp}.json"
    path.write_text(json.dumps(result.to_dict(), indent=2), encoding="utf-8")
    return path
