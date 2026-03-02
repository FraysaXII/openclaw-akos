"""Safe subprocess execution for AKOS scripts.

Wraps subprocess.run with timeouts, structured error capture,
and integration with akos.log.
"""

from __future__ import annotations

import logging
import subprocess
from dataclasses import dataclass

logger = logging.getLogger("akos.process")


@dataclass
class CommandResult:
    """Structured outcome of a subprocess invocation."""
    success: bool
    stdout: str
    stderr: str
    returncode: int


def run(
    args: list[str],
    *,
    timeout: int = 120,
    capture: bool = True,
    check: bool = False,
) -> CommandResult:
    """Execute a command with timeout and structured error handling.

    Args:
        args: Command and arguments (e.g. ["ollama", "pull", "qwen3:8b"]).
        timeout: Maximum seconds before the command is killed.
        capture: Whether to capture stdout/stderr (True) or let them stream.
        check: If True, raise on non-zero exit (like subprocess check=True).

    Returns:
        CommandResult with success flag, captured output, and return code.
    """
    cmd_str = " ".join(args)
    logger.info("Running: %s", cmd_str)

    try:
        result = subprocess.run(
            args,
            capture_output=capture,
            text=True,
            timeout=timeout,
            check=check,
        )
        success = result.returncode == 0
        if not success:
            logger.warning("Command exited %d: %s", result.returncode, cmd_str)
        return CommandResult(
            success=success,
            stdout=result.stdout or "",
            stderr=result.stderr or "",
            returncode=result.returncode,
        )
    except subprocess.TimeoutExpired:
        logger.error("Command timed out after %ds: %s", timeout, cmd_str)
        return CommandResult(success=False, stdout="", stderr=f"timeout after {timeout}s", returncode=-1)
    except FileNotFoundError:
        logger.error("Command not found: %s", args[0])
        return CommandResult(success=False, stdout="", stderr=f"not found: {args[0]}", returncode=-1)
    except subprocess.CalledProcessError as exc:
        logger.error("Command failed (exit %d): %s", exc.returncode, cmd_str)
        return CommandResult(
            success=False,
            stdout=exc.stdout or "",
            stderr=exc.stderr or "",
            returncode=exc.returncode,
        )
