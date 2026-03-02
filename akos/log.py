"""Structured logging for AKOS scripts.

Provides a JSON formatter whose fields align with config/logging.json,
and a setup function that scripts call once at startup.

Usage in scripts:
    from akos.log import setup_logging
    setup_logging(json_output=args.json_log)
    logger = logging.getLogger(__name__)
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    """Emit log records as single-line JSON matching config/logging.json fields."""

    def format(self, record: logging.LogRecord) -> str:
        entry: dict = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "agent_role": getattr(record, "agent_role", "system"),
            "tool_name": getattr(record, "tool_name", None),
            "workspace": getattr(record, "workspace", None),
            "outcome": record.getMessage(),
        }
        return json.dumps({k: v for k, v in entry.items() if v is not None})


class HumanFormatter(logging.Formatter):
    """Coloured single-line output for interactive terminals."""

    COLORS = {
        "DEBUG": "\033[37m",
        "INFO": "\033[36m",
        "WARNING": "\033[93m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[91m",
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, "")
        tag = f"{color}[{record.levelname}]{self.RESET}"
        return f"{tag} {record.getMessage()}"


def setup_logging(json_output: bool = False, level: int = logging.INFO) -> None:
    """Configure the root logger for AKOS scripts.

    Args:
        json_output: When True, emit structured JSON (for CI / log aggregation).
                     When False, emit coloured human-readable output.
        level: Logging level (default INFO).
    """
    root = logging.getLogger()
    root.setLevel(level)

    if root.handlers:
        root.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter() if json_output else HumanFormatter())
    root.addHandler(handler)
