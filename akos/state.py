"""Deployment state tracking for AKOS model switching.

Maintains a small JSON file (~/.openclaw/.akos-state.json) that records
the last successful switch, enabling rollback on failure.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from akos.io import load_json, save_json

logger = logging.getLogger("akos.state")

STATE_FILENAME = ".akos-state.json"


class AkosState(BaseModel):
    """Tracks the currently active environment/model deployment."""
    activeEnvironment: str = ""
    activeModel: str = ""
    activeTier: str = ""
    activeVariant: str = ""
    lastSwitchTimestamp: str = ""
    lastSwitchSuccess: bool = False


def load_state(oc_home: Path) -> AkosState:
    """Load state from disk, returning defaults if the file doesn't exist."""
    state_path = oc_home / STATE_FILENAME
    if not state_path.exists():
        return AkosState()
    try:
        data = load_json(state_path)
        return AkosState.model_validate(data)
    except Exception as exc:
        logger.warning("Could not load state file, using defaults: %s", exc)
        return AkosState()


def save_state(oc_home: Path, state: AkosState) -> None:
    """Persist state to disk."""
    state_path = oc_home / STATE_FILENAME
    state_path.parent.mkdir(parents=True, exist_ok=True)
    save_json(state_path, state.model_dump())
    logger.info("State saved: %s", state_path)


def record_switch(
    oc_home: Path,
    *,
    environment: str,
    model: str,
    tier: str,
    variant: str,
    success: bool,
) -> AkosState:
    """Record the outcome of a model switch."""
    state = AkosState(
        activeEnvironment=environment,
        activeModel=model,
        activeTier=tier,
        activeVariant=variant,
        lastSwitchTimestamp=datetime.now(timezone.utc).isoformat(),
        lastSwitchSuccess=success,
    )
    save_state(oc_home, state)
    return state
