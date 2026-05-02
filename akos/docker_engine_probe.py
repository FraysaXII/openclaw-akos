"""Fast Docker engine socket/pipe probe for sandbox preflight (Initiative 49 P4).

Avoids shelling to the ``docker`` CLI. Used by ``scripts/doctor.py --docker-sandbox``
and optional Playwright preflight in ``scripts/browser-smoke.py``.
"""

from __future__ import annotations

import socket
import sys
from pathlib import Path
from urllib.parse import urlparse

__all__ = ["probe_docker_engine"]


def _docker_host_unix_path() -> str | None:
    raw = (sys.environ.get("DOCKER_HOST") or "").strip()
    if not raw:
        return None
    if raw.startswith("unix://"):
        return urlparse(raw).path or None
    return None


def _unix_socket_candidates() -> list[Path]:
    host_path = _docker_host_unix_path()
    if host_path:
        return [Path(host_path)]
    return [Path("/var/run/docker.sock"), Path.home() / ".docker/run/docker.sock"]


def _probe_unixish(*, timeout_sec: float) -> tuple[bool, str]:
    last_err = "no Docker UNIX socket file found"
    for cand in _unix_socket_candidates():
        try:
            if not cand.is_socket():
                last_err = f"path exists but is not a socket: {cand}"
                continue
        except OSError as e:
            last_err = f"{cand}: {e}"
            continue
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(timeout_sec)
            try:
                sock.connect(str(cand))
            finally:
                sock.close()
            return True, f"Docker UNIX socket reachable ({cand})"
        except OSError as e:
            last_err = f"{cand}: {e}"
            continue
    return (
        False,
        f"Docker UNIX socket not reachable ({last_err}). "
        "Start Docker Desktop / engine; see USER_GUIDE section 14.3b.",
    )



def _probe_windows_pipe(*, timeout_sec: float) -> tuple[bool, str]:
    """``\\\\.\\pipe\\docker_engine`` when the Docker Desktop engine is listening."""
    del timeout_sec  # CreateFileW is effectively instant; reserved for API symmetry
    try:
        import ctypes
        from ctypes import wintypes
    except ImportError:
        return False, "Docker pipe probe unavailable (ctypes missing)"

    GENERIC_READ = 0x80000000
    GENERIC_WRITE = 0x40000000
    OPEN_EXISTING = 3
    INVALID_HANDLE_VALUE = wintypes.HANDLE(-1).value

    k32 = ctypes.windll.kernel32
    k32.CreateFileW.argtypes = [
        wintypes.LPCWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.LPVOID,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.HANDLE,
    ]
    k32.CreateFileW.restype = wintypes.HANDLE
    k32.CloseHandle.argtypes = [wintypes.HANDLE]
    k32.CloseHandle.restype = wintypes.BOOL

    pipe = r"\\.\pipe\docker_engine"
    h = k32.CreateFileW(pipe, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, None)
    if h == INVALID_HANDLE_VALUE:
        return False, (
            "Docker engine pipe not reachable (start Docker Desktop). "
            "See docs/USER_GUIDE.md section 14.3b (strict sandbox on Windows)."
        )
    k32.CloseHandle(h)
    return True, f"Docker engine pipe reachable ({pipe})"


def probe_docker_engine(*, timeout_sec: float = 2.0) -> tuple[bool, str]:
    """Return ``(True, detail)`` when the local Docker engine IPC endpoint answers.

    **Windows:** named pipe ``docker_engine``.

    **POSIX:** first existing UNIX socket among ``DOCKER_HOST`` (``unix://…``) or
    ``/var/run/docker.sock`` or ``~/.docker/run/docker.sock``.
    """
    if sys.platform == "win32":
        return _probe_windows_pipe(timeout_sec=timeout_sec)
    return _probe_unixish(timeout_sec=timeout_sec)
