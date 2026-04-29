#!/usr/bin/env python3
"""Validate HLK KM visual manifests under v3.0/_assets/**/*.manifest.md.

Checks YAML frontmatter for required keys, author_role in org baseline, raster path
relative to manifest exists, and optional SHA-256 match.

Usage: py scripts/validate_hlk_km_manifests.py
"""

from __future__ import annotations

import csv
import hashlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT

HLK_COMPLIANCE = REPO_ROOT / "docs" / "references" / "hlk" / "compliance"
ORG_CSV = HLK_COMPLIANCE / "baseline_organisation.csv"
ASSETS_ROOT = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "_assets"


def load_org_roles() -> set[str]:
    with open(ORG_CSV, encoding="utf-8", newline="") as f:
        return {row["role_name"].strip() for row in csv.DictReader(f) if row.get("role_name")}


def extract_frontmatter_block(text: str) -> tuple[str, str] | tuple[None, str]:
    if not text.startswith("---"):
        return None, "missing opening ---"
    end = text.find("\n---", 3)
    if end == -1:
        return None, "missing closing ---"
    return text[3:end].strip(), ""


def scalar_line(block: str, key: str) -> str | None:
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", block, re.MULTILINE)
    if not m:
        return None
    return m.group(1).strip().strip('"')


def raster_relative(block: str) -> str | None:
    m = re.search(r"^\s*raster:\s*(\S+)", block, re.MULTILINE)
    if not m:
        return None
    rel = m.group(1).strip().strip('"')
    if rel == "null":
        return None
    return rel


def sha256_expected(block: str) -> str | None:
    m = re.search(r'^file_sha256:\s*("?)([a-fA-F0-9]{64})\1', block, re.MULTILINE)
    if m:
        return m.group(2).lower()
    m2 = re.search(r"^file_sha256:\s*<", block, re.MULTILINE)
    if m2:
        return None
    return None


def validate_manifest(path: Path, org_names: set[str]) -> list[str]:
    errors: list[str] = []
    rel_path = path.relative_to(REPO_ROOT)
    text = path.read_text(encoding="utf-8")
    block, err = extract_frontmatter_block(text)
    if block is None:
        return [f"{rel_path}: {err}"]

    if not re.search(r"^paths:", block, re.MULTILINE):
        errors.append(f"{rel_path}: missing `paths:`")
    elif not re.search(r"^\s*raster:\s*\S+", block, re.MULTILINE):
        errors.append(f"{rel_path}: missing indented `raster:` under paths")

    checks = [
        ("source_id", r"^source_id:\s*\S"),
        ("output_type", r"^output_type:\s*\d"),
        ("title", r"^title:\s*\S"),
        ("created", r"^created:\s*\S"),
        ("author_role", r"^author_role:\s*\S"),
        ("topic_ids", r"^topic_ids:"),
        ("summary", r"^summary:\s*\S"),
        ("access_level", r"^access_level:\s*\S"),
        ("artifact_role", r"^artifact_role:\s*\S"),
        ("intellectual_kind", r"^intellectual_kind:\s*\S"),
    ]
    for label, pat in checks:
        if not re.search(pat, block, re.MULTILINE):
            errors.append(f"{rel_path}: missing or invalid `{label}`")

    owner = scalar_line(block, "author_role")
    if owner and owner not in org_names:
        errors.append(f"{rel_path}: author_role '{owner}' not in baseline org")

    ot_raw = scalar_line(block, "output_type")
    if ot_raw is not None:
        try:
            ot = int(ot_raw)
            if ot != 1:
                errors.append(f"{rel_path}: output_type should be 1 for visual manifests, got {ot}")
        except ValueError:
            errors.append(f"{rel_path}: output_type not integer")

    rel_raster = raster_relative(block)
    if rel_raster is None:
        errors.append(f"{rel_path}: could not parse indented `raster:` under paths")
    else:
        raster_abs = (path.parent / rel_raster).resolve()
        if not raster_abs.is_file():
            errors.append(f"{rel_path}: raster missing at {raster_abs.relative_to(REPO_ROOT)}")
        else:
            sha_expect = sha256_expected(block)
            if sha_expect:
                actual = hashlib.sha256(raster_abs.read_bytes()).hexdigest().lower()
                if actual != sha_expect:
                    errors.append(
                        f"{rel_path}: file_sha256 mismatch for {raster_abs.name} "
                        f"(expected {sha_expect[:16]}..., got {actual[:16]}...)"
                    )

    return errors


def load_topic_registry_ids() -> set[str]:
    """Initiative 25 P1: load topic_id set from canonical TOPIC_REGISTRY.csv.

    Returns empty set when the CSV is absent (Initiative 25 not yet shipped),
    in which case manifest topic_ids are not FK-checked.
    """
    csv_path = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "TOPIC_REGISTRY.csv"
    if not csv_path.is_file():
        return set()
    import csv as _csv

    with csv_path.open(encoding="utf-8", newline="") as fh:
        return {row["topic_id"].strip() for row in _csv.DictReader(fh) if row.get("topic_id")}


def manifest_topic_ids(block: str) -> list[str]:
    """Parse manifest YAML-ish topic_ids list values (one per line: ``  - topic_xxx``)."""
    out: list[str] = []
    in_block = False
    for line in block.splitlines():
        if re.match(r"^topic_ids:\s*", line):
            in_block = True
            # inline ``topic_ids: [a, b]`` form
            inline = line.split(":", 1)[1].strip()
            if inline.startswith("["):
                inner = inline.strip("[]")
                out.extend([s.strip().strip('"').strip("'") for s in inner.split(",") if s.strip()])
                in_block = False
            continue
        if in_block:
            m = re.match(r"^\s*-\s*(\S.*?)\s*$", line)
            if m:
                out.append(m.group(1).strip().strip('"').strip("'"))
            elif line.strip() and not line.startswith(" ") and not line.startswith("\t"):
                in_block = False
    return out


def main() -> int:
    print("\n  HLK KM manifest validator")
    print("  " + "=" * 40)
    if not ASSETS_ROOT.is_dir():
        print("  No _assets directory; skip.")
        return 0
    org_names = load_org_roles()
    registered_topic_ids = load_topic_registry_ids()
    manifests = sorted(ASSETS_ROOT.rglob("*.manifest.md"))
    if not manifests:
        print("  No *.manifest.md under _assets; skip.")
        return 0
    all_err: list[str] = []
    for m in manifests:
        errs = validate_manifest(m, org_names)
        # Initiative 25 P1 (D-IH-12): FK-resolve manifest topic_ids into TOPIC_REGISTRY.
        # SKIPs gracefully when the CSV is absent.
        if registered_topic_ids:
            try:
                block = m.read_text(encoding="utf-8")
                rel_path = m.relative_to(REPO_ROOT)
                for tid in manifest_topic_ids(block):
                    if tid and tid not in registered_topic_ids:
                        errs.append(
                            f"{rel_path}: topic_ids[{tid!r}] not found in TOPIC_REGISTRY.csv "
                            "(canonical SSOT per D-IH-12)"
                        )
            except Exception:  # noqa: BLE001 — manifest read failures already surfaced above
                pass
        rel = m.relative_to(REPO_ROOT)
        status = "PASS" if not errs else "FAIL"
        print(f"  {rel}  {status}")
        all_err.extend(errs)
    for e in all_err[:30]:
        print(f"    - {e}")
    if len(all_err) > 30:
        print(f"    ... and {len(all_err) - 30} more")
    print()
    if all_err:
        print(f"  OVERALL: FAIL ({len(all_err)} errors)")
        return 1
    print("  OVERALL: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
