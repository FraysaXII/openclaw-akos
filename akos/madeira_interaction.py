"""Madeira interaction mode: Ask vs Plan draft (read-only) control plane."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Literal

from akos.io import AGENT_WORKSPACES, REPO_ROOT

MadeiraInteractionMode = Literal["ask", "plan_draft"]

ASSEMBLED_DIR = REPO_ROOT / "prompts" / "assembled"
PLAN_OVERLAY_PATH = REPO_ROOT / "prompts" / "overlays" / "OVERLAY_MADEIRA_PLAN_DRAFT.md"
HANDOFF_SCHEMA_PATH = REPO_ROOT / "config" / "schemas" / "madeira-plan-handoff.schema.json"


def prompt_variant_for_madeira_mode(mode: str) -> str:
    """Return assemble variant filename segment for Madeira SOUL (compact vs standard)."""
    if mode == "plan_draft":
        return "standard"
    return "compact"


def validate_madeira_interaction_mode(raw: str) -> MadeiraInteractionMode:
    if raw not in ("ask", "plan_draft"):
        raise ValueError("madeiraInteractionMode must be 'ask' or 'plan_draft'")
    return raw  # type: ignore[return-value]


def apply_madeira_interaction_to_soul(
    oc_home: Path,
    *,
    mode: str,
    assembled_dir: Path | None = None,
) -> Path:
    """Write Madeira ``SOUL.md`` for *mode* after a full ``deploy_soul_prompts`` pass.

    Callers deploy all agents with the global tier variant first, then call this
    to swap Madeira to compact (ask) or standard + Plan overlay (plan_draft).
    """
    m = validate_madeira_interaction_mode(mode)
    base_dir = assembled_dir or ASSEMBLED_DIR
    madeira_variant = prompt_variant_for_madeira_mode(m)
    src = base_dir / f"MADEIRA_PROMPT.{madeira_variant}.md"
    if not src.exists():
        raise FileNotFoundError(
            f"Assembled Madeira prompt not found: {src}. Run: python scripts/assemble-prompts.py"
        )

    text = src.read_text(encoding="utf-8").rstrip()
    if m == "plan_draft" and PLAN_OVERLAY_PATH.is_file():
        text = text + "\n\n" + PLAN_OVERLAY_PATH.read_text(encoding="utf-8").rstrip()
    text = text + "\n"

    rel = AGENT_WORKSPACES["MADEIRA"]
    dest = oc_home / rel / "SOUL.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")
    return dest


def redeploy_all_souls_with_madeira_mode(
    oc_home: Path,
    *,
    global_variant: str,
    mode: str,
    assembled_dir: Path | None = None,
) -> list[Path]:
    """Run full deploy then patch Madeira for interaction economics."""
    from akos.io import deploy_soul_prompts

    base_dir = assembled_dir or ASSEMBLED_DIR
    out = deploy_soul_prompts(base_dir, global_variant, oc_home)
    apply_madeira_interaction_to_soul(oc_home, mode=mode, assembled_dir=base_dir)
    return out


def load_handoff_schema() -> dict[str, Any]:
    """Return parsed JSON Schema for Madeira plan handoffs."""
    return json.loads(HANDOFF_SCHEMA_PATH.read_text(encoding="utf-8"))


_JSON_FENCE_RE = re.compile(r"```(?:json)\s*\r?\n(.*?)```", re.DOTALL | re.IGNORECASE)


def extract_json_fences(markdown: str) -> list[str]:
    """Return raw JSON strings from fenced ```json blocks (plan draft answers)."""
    return [m.group(1).strip() for m in _JSON_FENCE_RE.finditer(markdown or "")]


def parse_first_handoff_json(markdown: str) -> dict[str, Any]:
    """Parse the first fenced JSON object from *markdown*.

    Raises ``ValueError`` if no fence or JSON is invalid.
    """
    blocks = extract_json_fences(markdown)
    if not blocks:
        raise ValueError("no_json_fence")
    try:
        data = json.loads(blocks[0])
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid_json:{exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("handoff_json_must_be_object")
    return data


def validate_plan_handoff_dict(obj: dict[str, Any], schema: dict[str, Any] | None = None) -> None:
    """Validate *obj* against the Madeira handoff schema (raises on failure)."""
    import jsonschema

    jsonschema.validate(instance=obj, schema=schema or load_handoff_schema())


def validate_plan_handoff_markdown(markdown: str, schema: dict[str, Any] | None = None) -> dict[str, Any]:
    """Extract first ```json fence and validate against schema; return parsed object."""
    obj = parse_first_handoff_json(markdown)
    validate_plan_handoff_dict(obj, schema)
    return obj
