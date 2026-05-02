"""Initiative 48 P3 — subprocess CLI orchestrator (live mode).

Per dossier-section-spec.md mode behavior matrix, live mode invokes the
following CLIs and feeds their stdout/exit-code into the corresponding
Section. Per-CLI failure marks SectionData.placeholder=True with stderr
in the error field; NEVER crashes the dossier (R-48-1 graceful degradation).

Cost discipline (D-IH-48-L): live mode has bounded cost (no Tier B); tier-b
mode (P3+) requires AKOS_DOSSIER_TIER_B=1 and uses --tier B flag on eval.py.

Public API:
- ``run_cli(cmd, timeout, env_extra=None) -> CliResult``
- ``CliResult`` dataclass (cmd + exit_code + stdout + stderr + duration_seconds + timed_out)
- per-section live invocations:
  - ``run_validate_hlk()`` -> CliResult
  - ``run_eval_mode_all_json()`` -> CliResult + parsed Scorecard
  - ``run_eval_mode_adversarial_json()`` -> CliResult
  - ``run_calibrate_scenarios()`` -> CliResult
  - ``run_graphrag_drift_canary()`` -> CliResult
  - ``run_agent_memory_trigger_watcher()`` -> CliResult
  - ``run_recovery_chaos_dry_run()`` -> CliResult
  - ``run_lint_cassette_pii()`` -> CliResult
"""

from __future__ import annotations

import json
import logging
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger("akos.dossier.runner")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

DEFAULT_CLI_TIMEOUT_SECONDS = 60
LONG_CLI_TIMEOUT_SECONDS = 180  # validate_hlk + eval --mode all can take ~30-60s


@dataclass
class CliResult:
    """One CLI invocation outcome."""

    cmd: list[str]
    exit_code: int = 0
    stdout: str = ""
    stderr: str = ""
    duration_seconds: float = 0.0
    timed_out: bool = False
    parsed_json: dict[str, Any] | None = None
    error_class: str = ""  # "" | "TIMEOUT" | "EXIT_NONZERO" | "EXCEPTION" | "PARSE_ERROR"

    @property
    def ok(self) -> bool:
        return self.exit_code == 0 and not self.timed_out and not self.error_class


def run_cli(
    cmd: list[str],
    *,
    timeout: float = DEFAULT_CLI_TIMEOUT_SECONDS,
    env_extra: dict[str, str] | None = None,
    parse_stdout_json: bool = False,
    cwd: Path | None = None,
) -> CliResult:
    """Run ``cmd`` as a subprocess; capture stdout/stderr; never raise.

    Per R-48-1: graceful degradation. Any failure (timeout / non-zero exit /
    exception) returns a CliResult with error_class set; caller's Section
    converts to SectionData.placeholder=True.
    """
    import os
    full_env = dict(os.environ)
    if env_extra:
        full_env.update(env_extra)

    started = time.perf_counter()
    result = CliResult(cmd=list(cmd))
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd or REPO_ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=full_env,
            timeout=timeout,
        )
        result.exit_code = proc.returncode
        result.stdout = proc.stdout or ""
        result.stderr = proc.stderr or ""
        if proc.returncode != 0:
            result.error_class = "EXIT_NONZERO"
        if parse_stdout_json and result.stdout:
            try:
                result.parsed_json = json.loads(result.stdout)
            except json.JSONDecodeError as exc:
                result.error_class = "PARSE_ERROR"
                result.stderr += f"\n[runner] JSON parse failed: {exc}"
    except subprocess.TimeoutExpired as exc:
        result.timed_out = True
        result.exit_code = -1
        result.error_class = "TIMEOUT"
        result.stderr = f"[runner] timed out after {timeout}s: {exc}"
    except Exception as exc:  # pragma: no cover (defensive)
        result.exit_code = -1
        result.error_class = "EXCEPTION"
        result.stderr = f"[runner] subprocess error: {exc!r}"
    finally:
        result.duration_seconds = time.perf_counter() - started
    return result


# ──────────────────────────────────────────────────────────────────────────────
# Per-section live invocations
# ──────────────────────────────────────────────────────────────────────────────


def run_validate_hlk() -> CliResult:
    """Section 2 — invoke validate_hlk.py for OVERALL PASS verdict."""
    return run_cli(
        [sys.executable, str(REPO_ROOT / "scripts" / "validate_hlk.py")],
        timeout=LONG_CLI_TIMEOUT_SECONDS,
    )


def run_eval_mode_all_json(
    *, persona: str | None = None, replay_skill: str | None = None,
) -> CliResult:
    """Section 3 — invoke eval.py --mode all --json with optional persona / skill replay filter."""
    cmd = [sys.executable, str(REPO_ROOT / "scripts" / "eval.py"),
           "--mode", "all", "--json", "--no-exit-on-fail"]
    if persona:
        cmd.extend(["--persona", persona])
    if replay_skill:
        cmd.extend(["--replay-skill", replay_skill])
    return run_cli(cmd, timeout=LONG_CLI_TIMEOUT_SECONDS, parse_stdout_json=True)


def run_eval_mode_adversarial_json() -> CliResult:
    """Section 5 — invoke eval.py --mode adversarial --json."""
    return run_cli(
        [sys.executable, str(REPO_ROOT / "scripts" / "eval.py"),
         "--mode", "adversarial", "--json", "--no-exit-on-fail"],
        timeout=LONG_CLI_TIMEOUT_SECONDS,
        parse_stdout_json=True,
    )


def run_calibrate_scenarios(*, persona: str | None = None) -> CliResult:
    """Section 4 — invoke scripts/calibrate_scenarios.py --quiet."""
    cmd = [sys.executable, str(REPO_ROOT / "scripts" / "calibrate_scenarios.py"), "--quiet"]
    if persona:
        cmd.extend(["--persona", persona])
    return run_cli(cmd, timeout=DEFAULT_CLI_TIMEOUT_SECONDS)


def run_graphrag_drift_canary() -> CliResult:
    """Section 7 — invoke scripts/graphrag_drift_canary.py."""
    return run_cli(
        [sys.executable, str(REPO_ROOT / "scripts" / "graphrag_drift_canary.py"),
         "--csv-only"],
        timeout=DEFAULT_CLI_TIMEOUT_SECONDS,
    )


def run_agent_memory_trigger_watcher() -> CliResult:
    """Section 8 — invoke scripts/agent_memory_trigger_watcher.py --quiet."""
    return run_cli(
        [sys.executable, str(REPO_ROOT / "scripts" / "agent_memory_trigger_watcher.py"), "--quiet"],
        timeout=DEFAULT_CLI_TIMEOUT_SECONDS,
    )


def run_recovery_chaos_dry_run() -> CliResult:
    """Section 6 — invoke scripts/recovery_chaos_runner.py --dry-run.

    Always uses --dry-run; live chaos NEVER auto-runs from dossier (R-47-13;
    even with AKOS_REAL_CHAOS_OK=1 the dossier path stays dry-run by design).
    """
    return run_cli(
        [sys.executable, str(REPO_ROOT / "scripts" / "recovery_chaos_runner.py"),
         "--scenario", "neo4j-password-rotation", "--dry-run",
         "--non-interactive", "--confirm-test-host", "test-throwaway-instance.databases.neo4j.io"],
        timeout=DEFAULT_CLI_TIMEOUT_SECONDS,
        env_extra={
            "AKOS_REAL_CHAOS_OK": "1",  # gate-1 bypass for dry-run only
            "NEO4J_URI": "neo4j+s://test-throwaway-instance.databases.neo4j.io:7687",
        },
    )


def run_lint_cassette_pii() -> CliResult:
    """Section 5 (companion) — invoke scripts/lint_cassette_pii.py for adversarial section."""
    return run_cli(
        [sys.executable, str(REPO_ROOT / "scripts" / "lint_cassette_pii.py")],
        timeout=DEFAULT_CLI_TIMEOUT_SECONDS,
    )


def take_browser_screenshots(out_dir: Path) -> list[Path]:
    """P3 opt-in --screenshots: best-effort browser capture via Cursor MCP.

    NOTE: actual Cursor browser MCP invocation is operator-driven (this agent
    invokes it at UAT time, not the dossier subprocess). For P3 we create the
    screenshots/ subdir + a placeholder note explaining the operator workflow;
    when the operator runs the dossier with --screenshots in an MCP-aware
    context (e.g. via this agent), they can drop captured PNGs into screenshots/
    AFTER dossier renders.

    Returns the list of PNG paths in the screenshots/ directory (empty if none yet).
    """
    screenshots_dir = out_dir / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    note = screenshots_dir / "README.md"
    note.write_text(
        "# Screenshots directory (Initiative 48 P3 --screenshots opt-in)\n"
        "\n"
        "Drop browser captures (PNG) into this directory. The HTML dossier will\n"
        "embed them under Section 1 (Executive summary) via `<img src=\"screenshots/<name>.png\">`.\n"
        "\n"
        "Capture flow when this agent runs the dossier:\n"
        "1. browser_lock + browser_navigate to OpenClaw Control SPA\n"
        "2. browser_take_screenshot (saved to %TEMP%)\n"
        "3. Copy the PNG into this directory\n"
        "\n"
        "Operator-only flow (no MCP): use any screen-capture tool; save PNGs here.\n",
        encoding="utf-8",
    )
    return sorted(screenshots_dir.glob("*.png"))
