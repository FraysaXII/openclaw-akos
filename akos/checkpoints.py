"""Workspace checkpoint/snapshot support for AKOS.

Provides reversible execution via tarball snapshots of agent workspaces.
Inspired by Replit's snapshot engine and Windsurf's named checkpoints.
"""

from __future__ import annotations

import logging
import shutil
import tarfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

logger = logging.getLogger("akos.checkpoints")


@dataclass
class CheckpointInfo:
    name: str
    workspace: str
    created_at: str
    size_bytes: int
    path: str


def _checkpoints_dir(workspace_path: Path) -> Path:
    return workspace_path / ".checkpoints"


def create_checkpoint(name: str, workspace_path: Path) -> CheckpointInfo:
    """Create a tarball snapshot of the workspace (excluding .checkpoints itself)."""
    ws = Path(workspace_path)
    if not ws.exists():
        raise FileNotFoundError(f"Workspace not found: {ws}")

    ckpt_dir = _checkpoints_dir(ws)
    ckpt_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    safe_name = name.replace(" ", "_").replace("/", "_")
    tar_name = f"{safe_name}_{timestamp}.tar.gz"
    tar_path = ckpt_dir / tar_name

    with tarfile.open(tar_path, "w:gz") as tar:
        for item in ws.iterdir():
            if item.name == ".checkpoints":
                continue
            tar.add(item, arcname=item.name)

    size = tar_path.stat().st_size
    logger.info("Checkpoint created: %s (%d bytes)", tar_path, size)

    return CheckpointInfo(
        name=name,
        workspace=str(ws),
        created_at=timestamp,
        size_bytes=size,
        path=str(tar_path),
    )


def restore_checkpoint(name: str, workspace_path: Path) -> bool:
    """Restore the most recent checkpoint matching *name*.

    Clears the workspace (except .checkpoints) and extracts the tarball.
    """
    ws = Path(workspace_path)
    ckpt_dir = _checkpoints_dir(ws)
    if not ckpt_dir.exists():
        logger.error("No checkpoints directory: %s", ckpt_dir)
        return False

    safe_name = name.replace(" ", "_").replace("/", "_")
    matches = sorted(ckpt_dir.glob(f"{safe_name}_*.tar.gz"), reverse=True)
    if not matches:
        logger.error("No checkpoint found matching: %s", name)
        return False

    tar_path = matches[0]
    logger.info("Restoring checkpoint: %s", tar_path)

    for item in ws.iterdir():
        if item.name == ".checkpoints":
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(ws, filter="data")

    logger.info("Restored workspace from %s", tar_path.name)
    return True


def list_checkpoints(workspace_path: Path) -> list[CheckpointInfo]:
    """List all checkpoints for a workspace, newest first."""
    ws = Path(workspace_path)
    ckpt_dir = _checkpoints_dir(ws)
    if not ckpt_dir.exists():
        return []

    result: list[CheckpointInfo] = []
    for tar_path in sorted(ckpt_dir.glob("*.tar.gz"), reverse=True):
        stem = tar_path.stem.replace(".tar", "")
        parts = stem.rsplit("_", 1)
        name = parts[0] if len(parts) > 1 else stem
        ts = parts[1] if len(parts) > 1 else ""
        result.append(
            CheckpointInfo(
                name=name,
                workspace=str(ws),
                created_at=ts,
                size_bytes=tar_path.stat().st_size,
                path=str(tar_path),
            )
        )
    return result
