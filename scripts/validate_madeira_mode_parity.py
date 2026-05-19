"""Validate MADEIRA_MODE_PARITY.md against the canonical Pydantic registry per I76 P1.

Paired runbook for `docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/MADEIRA_MODE_PARITY.md`
per `akos-executable-process-catalog.mdc` RULE 1. Sister validator pattern: scripts/validate_locale_orthography.py.

Usage:
    py scripts/validate_madeira_mode_parity.py [--strict]

Exit codes:
    0 - all 5 canonical modes parse from the SOP and match CANONICAL_REGISTRY.
    1 - mode missing / extra / mismatched (rbac_posture or persistence_default).
    2 - file structure unparseable (e.g., §3.1 table not found).
"""
from __future__ import annotations

import argparse
import logging
import re
import sys
from pathlib import Path

from akos.hlk_madeira_mode import (
    CANONICAL_MODE_SPECS,
    MadeiraModeSpec,
)
from akos.log import setup_logging

LOG = logging.getLogger("validate_madeira_mode_parity")


REPO_ROOT = Path(__file__).resolve().parent.parent
SOP_PATH = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "Envoy Tech Lab"
    / "canonicals"
    / "MADEIRA_MODE_PARITY.md"
)


_TABLE_HEADER_RE = re.compile(
    r"mode_id\s*\|\s*name\s*\|\s*added_by\s*\|\s*rbac_posture\s*\|\s*persistence_default"
)
_TABLE_ROW_RE = re.compile(
    r"^\s*(?P<mode_id>[a-z]+)\s*\|\s*"
    r"(?P<name>[A-Za-z]+)\s*\|\s*"
    r"(?P<added_by>[A-Z0-9 ]+)\s*\|\s*"
    r"(?P<rbac_posture>[a-z+\- ]+?)\s*\|\s*"
    r"(?P<persistence_default>[a-z\- ]+?)\s*$"
)


def parse_mode_table(sop_text: str) -> list[MadeiraModeSpec]:
    """Parse the §3.1 mode-enum table from the canonical SOP markdown."""
    lines = sop_text.splitlines()
    in_table = False
    parsed: list[MadeiraModeSpec] = []
    for line in lines:
        if not in_table and _TABLE_HEADER_RE.search(line):
            in_table = True
            continue
        if in_table:
            if line.strip().startswith("---"):
                continue
            if not line.strip() or line.strip().startswith("```") or line.strip().startswith("#"):
                break
            match = _TABLE_ROW_RE.match(line)
            if not match:
                continue
            try:
                parsed.append(
                    MadeiraModeSpec(
                        mode_id=match.group("mode_id"),  # type: ignore[arg-type]
                        name=match.group("name"),
                        added_by=match.group("added_by").strip(),  # type: ignore[arg-type]
                        rbac_posture=match.group("rbac_posture").strip(),  # type: ignore[arg-type]
                        persistence_default=match.group("persistence_default").strip(),  # type: ignore[arg-type]
                    )
                )
            except Exception as exc:
                LOG.error("row failed to parse as MadeiraModeSpec: %r (%s)", line, exc)
                raise
    return parsed


def validate(sop_path: Path, strict: bool = False) -> int:
    if not sop_path.is_file():
        LOG.error("canonical SOP not found at %s", sop_path)
        return 2
    sop_text = sop_path.read_text(encoding="utf-8")
    try:
        parsed_specs = parse_mode_table(sop_text)
    except Exception:
        return 2
    if not parsed_specs:
        LOG.error("§3.1 mode-enum table found no parseable rows; SOP structure invalid")
        return 2

    canonical_by_id = {s.mode_id: s for s in CANONICAL_MODE_SPECS}
    parsed_by_id = {s.mode_id: s for s in parsed_specs}

    missing = set(canonical_by_id) - set(parsed_by_id)
    extra = set(parsed_by_id) - set(canonical_by_id)
    mismatched: list[tuple[str, str, MadeiraModeSpec, MadeiraModeSpec]] = []
    for mode_id, canonical in canonical_by_id.items():
        if mode_id in parsed_by_id:
            parsed = parsed_by_id[mode_id]
            if canonical != parsed:
                mismatched.append((mode_id, "mismatch", canonical, parsed))

    if missing:
        LOG.error("modes missing from §3.1 table: %s", sorted(missing))
    if extra:
        LOG.error("modes in §3.1 table not in canonical registry: %s", sorted(extra))
    for mode_id, _, canonical, parsed in mismatched:
        LOG.error(
            "mode %s mismatch:\n  canonical: rbac=%s persistence=%s\n  parsed:    rbac=%s persistence=%s",
            mode_id,
            canonical.rbac_posture,
            canonical.persistence_default,
            parsed.rbac_posture,
            parsed.persistence_default,
        )

    if missing or extra or mismatched:
        LOG.error("MADEIRA mode parity FAILED — %d findings", len(missing) + len(extra) + len(mismatched))
        return 1

    LOG.info(
        "MADEIRA mode parity PASS — 5 canonical modes match SOP §3.1 (%s)",
        ", ".join(sorted(canonical_by_id)),
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--strict", action="store_true", help="Reserved for future stricter checks (currently a no-op).")
    args = parser.parse_args()
    setup_logging()
    return validate(SOP_PATH, strict=args.strict)


if __name__ == "__main__":
    sys.exit(main())
