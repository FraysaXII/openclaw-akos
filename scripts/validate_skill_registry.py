#!/usr/bin/env python3
"""Initiative 32 P2 — Validator for SKILL_REGISTRY.csv.

Schema enforcement:
- Required header matches ``SKILL_REGISTRY_FIELDNAMES``.
- ``skill_id`` matches ``^SKILL-[A-Z0-9-]{4,80}-V\\d+$``; unique.
- ``agents_supported`` (semicolon list) — each agent id is in
  ``KNOWN_AGENT_IDS`` or equals ``shared``.
- ``axes_consumed`` (semicolon list) — each axis is in ``VALID_AXES``.
- ``tools_required`` (semicolon list, may be empty) — informational FK to
  ``config/agent-capabilities.json`` allowed_tools (warning only, not fatal,
  because Cursor agent tools are dynamic).
- ``version`` matches ``^\\d+\\.\\d+\\.\\d+$``.
- ``owner_role`` resolves against ``baseline_organisation.csv``.
- ``eval_baseline_pct`` parses as float in ``[0.0, 100.0]``.
- ``tenant_scope`` matches ``^shared$`` (D-IH-32-J: only `shared` until I34).
- ``lifecycle_status`` is in ``VALID_LIFECYCLE_STATUSES``.
- ``topic_ids`` (semicolon list) — each id resolves to ``TOPIC_REGISTRY.csv``.
- ``description`` is non-empty.

Usage::

    py scripts/validate_skill_registry.py
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_skill_registry_csv import (
    KNOWN_AGENT_IDS,
    SHARED_AGENT_ID,
    SKILL_REGISTRY_FIELDNAMES,
    VALID_AXES,
    VALID_LIFECYCLE_STATUSES,
)
from akos.io import REPO_ROOT

CSV_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "SKILL_REGISTRY.csv"
ORG_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "baseline_organisation.csv"
TOPIC_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "TOPIC_REGISTRY.csv"
AGENT_CAPS = REPO_ROOT / "config" / "agent-capabilities.json"

SKILL_ID_RE = re.compile(r"^SKILL-[A-Z0-9-]{4,80}-V\d+$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
TENANT_SCOPE_RE = re.compile(r"^shared$")  # D-IH-32-J: only 'shared' valid until I34


def _load_csv_set(path: Path, key: str) -> set[str]:
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        return {(row.get(key) or "").strip() for row in csv.DictReader(fh) if row.get(key)}


def _load_agent_tools() -> set[str]:
    """Load all allowed_tools across all agent roles from agent-capabilities.json."""
    if not AGENT_CAPS.is_file():
        return set()
    try:
        data = json.loads(AGENT_CAPS.read_text(encoding="utf-8"))
    except Exception:
        return set()
    tools: set[str] = set()
    for role_def in (data.get("roles") or {}).values():
        for tool in role_def.get("allowed_tools") or []:
            tools.add(tool)
    return tools


def _split_semi(value: str) -> list[str]:
    return [s.strip() for s in (value or "").split(";") if s.strip()]


def main() -> int:
    print("\n  SKILL_REGISTRY Validator")
    print("  " + "=" * 40)
    if not CSV_PATH.is_file():
        print("  SKIP: SKILL_REGISTRY.csv not present")
        return 0

    org_roles = _load_csv_set(ORG_CSV, "role_name")
    topic_ids = _load_csv_set(TOPIC_CSV, "topic_id")
    agent_tools = _load_agent_tools()

    errors: list[str] = []
    warnings: list[str] = []
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != list(SKILL_REGISTRY_FIELDNAMES):
            print("  FAIL: header mismatch")
            print(f"    expected: {list(SKILL_REGISTRY_FIELDNAMES)}")
            print(f"    got:      {reader.fieldnames}")
            return 1
        rows = list(reader)

    seen: set[str] = set()
    for i, r in enumerate(rows, start=2):
        sid = (r.get("skill_id") or "").strip()
        if not sid:
            errors.append(f"row {i}: skill_id empty")
            continue
        if not SKILL_ID_RE.match(sid):
            errors.append(f"row {i}: skill_id {sid!r} does not match {SKILL_ID_RE.pattern}")
        if sid in seen:
            errors.append(f"row {i}: skill_id {sid!r} duplicated")
        seen.add(sid)

        # name non-empty
        if not (r.get("name") or "").strip():
            errors.append(f"{sid}: name empty")

        # agents_supported FK
        agents = _split_semi(r.get("agents_supported") or "")
        if not agents:
            errors.append(f"{sid}: agents_supported is empty")
        for agent in agents:
            if agent != SHARED_AGENT_ID and agent not in KNOWN_AGENT_IDS:
                errors.append(
                    f"{sid}: agent {agent!r} not in KNOWN_AGENT_IDS "
                    f"({sorted(KNOWN_AGENT_IDS)}) or {SHARED_AGENT_ID!r}"
                )

        # axes_consumed enum
        axes = _split_semi(r.get("axes_consumed") or "")
        if not axes:
            errors.append(f"{sid}: axes_consumed is empty")
        for ax in axes:
            if ax not in VALID_AXES:
                errors.append(f"{sid}: axis {ax!r} not in VALID_AXES ({sorted(VALID_AXES)})")

        # tools_required (warning only — Cursor agent tools are dynamic)
        for tool in _split_semi(r.get("tools_required") or ""):
            if agent_tools and tool not in agent_tools:
                # Don't fail on Cursor agent tool names like 'Shell', 'Read', 'Write'
                # which are not in agent-capabilities.json (those govern openclaw runtime tools).
                if tool not in {"Shell", "Read", "Write"}:
                    warnings.append(
                        f"{sid}: tool {tool!r} not in agent-capabilities.json allowed_tools "
                        f"(informational; Cursor tools are dynamic)"
                    )

        # version semver
        version = (r.get("version") or "").strip()
        if not SEMVER_RE.match(version):
            errors.append(f"{sid}: version {version!r} does not match semver ^\\d+\\.\\d+\\.\\d+$")

        # owner_role FK
        owner = (r.get("owner_role") or "").strip()
        if not owner:
            errors.append(f"{sid}: owner_role empty")
        elif org_roles and owner not in org_roles:
            errors.append(f"{sid}: owner_role {owner!r} not in baseline_organisation.csv")

        # eval_baseline_pct float in [0, 100]
        ebp_raw = (r.get("eval_baseline_pct") or "").strip()
        if not ebp_raw:
            errors.append(f"{sid}: eval_baseline_pct empty")
        else:
            try:
                ebp = float(ebp_raw)
                if ebp < 0.0 or ebp > 100.0:
                    errors.append(f"{sid}: eval_baseline_pct {ebp} out of range [0.0, 100.0]")
            except ValueError:
                errors.append(f"{sid}: eval_baseline_pct {ebp_raw!r} not parseable as float")

        # tenant_scope regex
        tenant = (r.get("tenant_scope") or "").strip()
        if not TENANT_SCOPE_RE.match(tenant):
            errors.append(
                f"{sid}: tenant_scope {tenant!r} must match ^shared$ "
                f"(D-IH-32-J: only 'shared' valid until Initiative 34)"
            )

        # lifecycle_status enum
        lc = (r.get("lifecycle_status") or "").strip()
        if lc not in VALID_LIFECYCLE_STATUSES:
            errors.append(
                f"{sid}: lifecycle_status {lc!r} not in {sorted(VALID_LIFECYCLE_STATUSES)}"
            )

        # topic_ids FK
        for tid in _split_semi(r.get("topic_ids") or ""):
            if topic_ids and tid not in topic_ids:
                errors.append(f"{sid}: topic_id {tid!r} not in TOPIC_REGISTRY.csv")

        # description non-empty
        if not (r.get("description") or "").strip():
            errors.append(f"{sid}: description empty")

    print(f"  Rows validated: {len(rows)}")
    print(f"  Skills:         {len(seen)}")

    if warnings:
        print("  Warnings (informational):")
        for w in warnings[:5]:
            print(f"    - {w}")
        if len(warnings) > 5:
            print(f"    ... and {len(warnings) - 5} more")

    if errors:
        print(f"  FAIL: {len(errors)} errors")
        for e in errors[:10]:
            print(f"    - {e}")
        if len(errors) > 10:
            print(f"    ... and {len(errors) - 10} more")
        return 1

    print("  PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
