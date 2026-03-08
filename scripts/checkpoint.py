#!/usr/bin/env python3
"""Checkpoint CLI -- create, list, and restore workspace snapshots.

Usage:
    py scripts/checkpoint.py create --name before-refactor
    py scripts/checkpoint.py list
    py scripts/checkpoint.py restore --name before-refactor
    py scripts/checkpoint.py create --name backup --workspace ~/.openclaw/workspace-architect
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.checkpoints import create_checkpoint, list_checkpoints, restore_checkpoint
from akos.io import resolve_openclaw_home
from akos.log import setup_logging


def _default_workspace() -> Path:
    return resolve_openclaw_home() / "workspace-executor"


def cmd_create(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace) if args.workspace else _default_workspace()
    try:
        info = create_checkpoint(args.name, workspace)
        print(f"\n  Checkpoint created: {info.name}")
        print(f"  Path: {info.path}")
        print(f"  Size: {info.size_bytes} bytes\n")
        return 0
    except FileNotFoundError as exc:
        print(f"\n  Error: {exc}\n")
        return 1


def cmd_list(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace) if args.workspace else _default_workspace()
    items = list_checkpoints(workspace)
    if not items:
        print("\n  No checkpoints found.\n")
        return 0
    print(f"\n  Checkpoints ({len(items)}):")
    print("  " + "-" * 50)
    for c in items:
        print(f"  {c.name:30s}  {c.created_at}  {c.size_bytes}B")
    print()
    return 0


def cmd_restore(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace) if args.workspace else _default_workspace()
    success = restore_checkpoint(args.name, workspace)
    if success:
        print(f"\n  Restored checkpoint: {args.name}\n")
        return 0
    print(f"\n  Checkpoint not found: {args.name}\n")
    return 1


def main() -> None:
    setup_logging()

    parser = argparse.ArgumentParser(description="AKOS Checkpoint CLI")
    sub = parser.add_subparsers(dest="command", help="Subcommand")

    p_create = sub.add_parser("create", help="Create a workspace checkpoint")
    p_create.add_argument("--name", required=True, help="Checkpoint name")
    p_create.add_argument("--workspace", default=None, help="Workspace path (default: executor)")

    p_list = sub.add_parser("list", help="List available checkpoints")
    p_list.add_argument("--workspace", default=None, help="Workspace path (default: executor)")

    p_restore = sub.add_parser("restore", help="Restore a checkpoint")
    p_restore.add_argument("--name", required=True, help="Checkpoint name to restore")
    p_restore.add_argument("--workspace", default=None, help="Workspace path (default: executor)")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    handlers = {"create": cmd_create, "list": cmd_list, "restore": cmd_restore}
    sys.exit(handlers[args.command](args))


if __name__ == "__main__":
    main()
