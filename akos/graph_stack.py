"""Graph explorer + Neo4j mirror supervision for ``scripts/serve-api.py``.

Streamlit runs only as a **child process** of the API launcher (never inside the
OpenClaw gateway). Mirror auto-sync uses fingerprinted canonical CSV inputs,
``validate_hlk.py`` before writes, and a global lock. Health snapshots are read
by ``GET /health`` via ``graph_health_payload()``.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import subprocess
import sys
import threading
import time
import webbrowser
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from akos.io import REPO_ROOT, resolve_openclaw_home
from akos.process import run as run_process

logger = logging.getLogger("akos.graph_stack")

_SUPERVISOR: GraphStackSupervisor | None = None

_CANONICAL_CSVS: tuple[Path, ...] = (
    REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "baseline_organisation.csv",
    REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "process_list.csv",
)


def set_graph_stack_supervisor(sup: GraphStackSupervisor | None) -> None:
    global _SUPERVISOR
    _SUPERVISOR = sup


def get_graph_stack_supervisor() -> GraphStackSupervisor | None:
    return _SUPERVISOR


def graph_health_payload() -> tuple[dict[str, Any], dict[str, Any]]:
    if _SUPERVISOR is None:
        return (
            {
                "state": "not_supervised",
                "url": None,
                "pid": None,
                "last_exit_code": None,
            },
            {
                "in_sync": None,
                "last_ok": None,
                "fingerprint_short": None,
                "pending": False,
                "last_error": None,
            },
        )
    return _SUPERVISOR.health_payload()


def fingerprint_canonical_csvs() -> str:
    """Stable SHA-256 over whitelisted canonical CSV contents (order fixed)."""
    h = hashlib.sha256()
    for path in _CANONICAL_CSVS:
        h.update(path.as_posix().encode("utf-8"))
        h.update(b"\0")
        if path.is_file():
            h.update(path.read_bytes())
        else:
            h.update(b"<missing>")
        h.update(b"\n")
    return h.hexdigest()


def _state_path() -> Path:
    return resolve_openclaw_home() / ".akos-neo4j-sync-state.json"


def _load_sync_state() -> dict[str, Any]:
    p = _state_path()
    if not p.is_file():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _save_sync_state(data: dict[str, Any]) -> None:
    p = _state_path()
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    except OSError as exc:
        logger.warning("Could not persist Neo4j sync state to %s: %s", p, exc)


@dataclass
class ExplorerRuntime:
    proc: subprocess.Popen[str] | None = None
    url: str | None = None
    skip_reason: str | None = None
    last_exit_code: int | None = None


@dataclass
class MirrorRuntime:
    last_fp: str | None = None
    last_ok_iso: str | None = None
    last_error: str | None = None
    pending: bool = False
    thread: threading.Thread | None = None
    stop: threading.Event = field(default_factory=threading.Event)


class GraphStackSupervisor:
    """Starts optional Streamlit explorer + background mirror sync."""

    def __init__(
        self,
        *,
        api_host: str,
        api_port: int,
        on_sync_success: Callable[[], None] | None = None,
    ) -> None:
        self._api_host = api_host
        self._api_port = api_port
        self._on_sync_success = on_sync_success
        self._explorer = ExplorerRuntime()
        self._mirror = MirrorRuntime()
        self._sync_lock = threading.Lock()
        self._last_graph_kick_monotonic = 0.0

    def explorer_public_url(self) -> str | None:
        return self._explorer.url

    def health_payload(self) -> tuple[dict[str, Any], dict[str, Any]]:
        ex = self._explorer
        if ex.skip_reason:
            state = ex.skip_reason
        elif ex.proc is None:
            state = "not_started"
        elif ex.proc.poll() is None:
            state = "running"
        else:
            state = "exited"
            ex.last_exit_code = ex.proc.returncode

        geo = {
            "state": state,
            "url": ex.url,
            "pid": ex.proc.pid if ex.proc and ex.proc.poll() is None else None,
            "last_exit_code": ex.last_exit_code if ex.proc and ex.proc.poll() is not None else None,
        }
        cur_fp = fingerprint_canonical_csvs()
        disk = _load_sync_state()
        ref_fp = self._mirror.last_fp or disk.get("fingerprint")
        mir = {
            "in_sync": (ref_fp == cur_fp) if ref_fp else None,
            "last_ok": self._mirror.last_ok_iso or disk.get("last_ok"),
            "fingerprint_short": cur_fp[:12] if cur_fp else None,
            "pending": self._mirror.pending,
            "last_error": self._mirror.last_error,
        }
        return geo, mir

    def start_explorer_if_enabled(self, *, no_graph_explorer: bool, open_browser: bool) -> None:
        if no_graph_explorer or os.environ.get("AKOS_GRAPH_EXPLORER", "").strip() in {"0", "false", "False"}:
            self._explorer.skip_reason = "disabled"
            logger.info("Graph explorer: skipped (AKOS_GRAPH_EXPLORER=0 or --no-graph-explorer)")
            return

        from akos.hlk_neo4j import get_neo4j_driver, neo4j_env_non_placeholder

        if not neo4j_env_non_placeholder():
            self._explorer.skip_reason = "skipped_unset_or_placeholder"
            logger.info("Graph explorer: skipped (NEO4J_URI/PASSWORD unset or placeholder-like)")
            return

        drv = get_neo4j_driver()
        if drv is None:
            self._explorer.skip_reason = "skipped_driver"
            logger.info("Graph explorer: skipped (Neo4j driver unavailable)")
            return
        try:
            drv.verify_connectivity()
        except Exception as exc:
            self._explorer.skip_reason = "skipped_unreachable"
            logger.info("Graph explorer: skipped (Neo4j unreachable: %s)", type(exc).__name__)
            return
        finally:
            try:
                drv.close()
            except Exception:
                pass

        port = int(os.environ.get("AKOS_GRAPH_EXPLORER_PORT", "8730"))
        api_url = f"http://{self._api_host}:{self._api_port}"
        if self._api_host in {"0.0.0.0", "::"}:
            api_url = f"http://127.0.0.1:{self._api_port}"

        script = REPO_ROOT / "scripts" / "hlk_graph_explorer.py"
        cmd = [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(script),
            "--server.headless",
            "true",
            "--server.address",
            "127.0.0.1",
            "--server.port",
            str(port),
            "--browser.gatherUsageStats",
            "false",
        ]
        env = os.environ.copy()
        env["AKOS_API_URL"] = api_url
        try:
            self._explorer.proc = subprocess.Popen(
                cmd,
                cwd=str(REPO_ROOT),
                env=env,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except OSError as exc:
            self._explorer.skip_reason = "spawn_failed"
            logger.warning("Graph explorer: spawn failed: %s", exc)
            return

        self._explorer.url = f"http://127.0.0.1:{port}"
        logger.info("Graph explorer: started pid=%s url=%s", self._explorer.proc.pid, self._explorer.url)
        if open_browser:

            def _open_later() -> None:
                time.sleep(2.0)
                webbrowser.open(self._explorer.url or "")

            threading.Thread(target=_open_later, daemon=True).start()

    def start_mirror_autosync_if_enabled(self) -> None:
        if os.environ.get("AKOS_NEO4J_AUTO_SYNC", "1").strip() in {"0", "false", "False"}:
            logger.info("Neo4j mirror autosync: disabled (AKOS_NEO4J_AUTO_SYNC=0)")
            return

        from akos.hlk_neo4j import neo4j_env_non_placeholder

        if not neo4j_env_non_placeholder():
            return

        interval = float(os.environ.get("AKOS_NEO4J_SYNC_POLL_SECONDS", "300"))
        if os.environ.get("AKOS_NEO4J_SYNC_WATCH", "").strip() in {"1", "true", "True"}:
            interval = min(interval, 60.0)

        st = _load_sync_state()
        self._mirror.last_fp = st.get("fingerprint")
        self._mirror.last_ok_iso = st.get("last_ok")

        def _loop() -> None:
            self._maybe_sync_once()
            while not self._mirror.stop.wait(timeout=interval):
                self._maybe_sync_once()

        self._mirror.thread = threading.Thread(target=_loop, name="akos-neo4j-sync", daemon=True)
        self._mirror.thread.start()
        logger.info("Neo4j mirror autosync: background thread started (interval=%ss)", interval)

    def kick_mirror_sync(self) -> None:
        """Best-effort sync from API hot path (non-blocking thread)."""
        threading.Thread(target=self._maybe_sync_once, name="akos-neo4j-sync-kick", daemon=True).start()

    def kick_mirror_sync_debounced(self, min_interval_s: float = 120.0) -> None:
        """Rate-limited mirror kick (e.g. from ``/hlk/graph/summary``) to nudge after CSV drift."""
        now = time.monotonic()
        if now - self._last_graph_kick_monotonic < min_interval_s:
            return
        self._last_graph_kick_monotonic = now
        self.kick_mirror_sync()

    def _maybe_sync_once(self) -> None:
        if not self._sync_lock.acquire(blocking=False):
            self._mirror.pending = True
            return
        self._mirror.pending = False
        try:
            cur = fingerprint_canonical_csvs()
            state = _load_sync_state()
            prev = state.get("fingerprint")
            if prev == cur:
                self._mirror.last_fp = cur
                return

            self._mirror.last_error = None
            val = run_process(
                [sys.executable, str(REPO_ROOT / "scripts" / "validate_hlk.py")],
                timeout=600,
                capture=True,
            )
            if not val.success:
                self._mirror.last_error = "validate_hlk_failed"
                logger.warning("Neo4j mirror sync: aborted (validate_hlk.py exit %s)", val.returncode)
                return

            extra: list[str] = []
            if os.environ.get("AKOS_NEO4J_SYNC_WITH_DOCUMENTS", "").strip() in {"1", "true", "True"}:
                extra.append("--with-documents")

            sync = run_process(
                [sys.executable, str(REPO_ROOT / "scripts" / "sync_hlk_neo4j.py"), *extra],
                timeout=3600,
                capture=True,
            )
            if not sync.success:
                self._mirror.last_error = "sync_failed"
                logger.warning("Neo4j mirror sync: sync_hlk_neo4j.py exit %s", sync.returncode)
                return

            now = datetime.now(timezone.utc).isoformat()
            _save_sync_state({"fingerprint": cur, "last_ok": now, "last_error": None})
            self._mirror.last_fp = cur
            self._mirror.last_ok_iso = now
            if self._on_sync_success:
                self._on_sync_success()
            logger.info("Neo4j mirror sync: completed fingerprint=%s…", cur[:12])
        finally:
            self._sync_lock.release()

    def shutdown(self) -> None:
        self._mirror.stop.set()
        if self._mirror.thread and self._mirror.thread.is_alive():
            self._mirror.thread.join(timeout=2.0)
        proc = self._explorer.proc
        if proc is None or proc.poll() is not None:
            return
        try:
            proc.terminate()
            proc.wait(timeout=8)
        except subprocess.TimeoutExpired:
            try:
                proc.kill()
            except OSError:
                pass
        except OSError:
            pass
