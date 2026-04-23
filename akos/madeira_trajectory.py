"""Pure helpers for Madeira session trajectory assertions (golden JSONL fixtures)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def parse_session_jsonl(path: Path) -> list[dict[str, Any]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[dict[str, Any]] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        out.append(json.loads(line))
    return out


def tool_names_from_session(events: list[dict[str, Any]]) -> list[str]:
    """Collect toolCall names in document order (Madeira / OpenClaw session JSONL)."""
    names: list[str] = []
    for ev in events:
        msg = ev.get("message")
        if not isinstance(msg, dict) or msg.get("role") != "assistant":
            continue
        blocks = msg.get("content")
        if not isinstance(blocks, list):
            continue
        for block in blocks:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "toolCall":
                n = block.get("name")
                if n:
                    names.append(str(n))
    return names


def final_assistant_text(events: list[dict[str, Any]]) -> str:
    """Return concatenated text from the last assistant message with text blocks."""
    last_text = ""
    for ev in events:
        msg = ev.get("message")
        if not isinstance(msg, dict) or msg.get("role") != "assistant":
            continue
        blocks = msg.get("content")
        if not isinstance(blocks, list):
            continue
        parts: list[str] = []
        for block in blocks:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(str(block.get("text", "")))
        if parts:
            last_text = "\n".join(parts).strip()
    return last_text


def assert_tools_before_first_text(events: list[dict[str, Any]], *, required: list[str]) -> None:
    """Fail if any ``required`` tool is absent, or if assistant text appears before first HLK tool."""
    tools = tool_names_from_session(events)
    for name in required:
        if name not in tools:
            raise AssertionError(f"missing required tool {name!r}; got {tools}")
    first_hlk_idx: int | None = None
    for i, t in enumerate(tools):
        if t.startswith("hlk_"):
            first_hlk_idx = i
            break
    if first_hlk_idx is None:
        raise AssertionError(f"expected an hlk_* tool in trajectory; got {tools}")
    # Heuristic: first assistant text chunk should not precede first tool in the event stream
    saw_text_before_tool = False
    saw_tool = False
    for ev in events:
        msg = ev.get("message")
        if not isinstance(msg, dict) or msg.get("role") != "assistant":
            continue
        blocks = msg.get("content")
        if not isinstance(blocks, list):
            continue
        for block in blocks:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "text" and str(block.get("text", "")).strip():
                if not saw_tool:
                    saw_text_before_tool = True
            if block.get("type") == "toolCall":
                saw_tool = True
    if saw_text_before_tool:
        raise AssertionError("assistant text appeared before first tool call (expected tool-first for HLK lookup)")
