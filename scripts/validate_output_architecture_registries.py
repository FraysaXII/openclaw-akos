#!/usr/bin/env python3
"""Validate OUTPUT_TYPE_REGISTRY + ARTIFACT_CLASS_REGISTRY + COMPONENT_PRIMITIVE_REGISTRY.

Composite validator covering all 3 layers of the 4-layer output architecture
(Initiative 86 Wave K + L; per D-IH-86-BB + D-IH-86-BG):

- Layer 1: OUTPUT_TYPE_REGISTRY.csv  (medium / shape)
- Layer 2: ARTIFACT_CLASS_REGISTRY.csv  (named purpose)
- Layer 3: COMPONENT_PRIMITIVE_REGISTRY.csv  (Shadcn-shape granular primitives)

Per layer:
- Header drift gate against Pydantic FIELDNAMES tuple in akos/.
- Per-row Pydantic instantiation (frozen models with Literal enums + slug regex).
- Slug uniqueness within registry.

Cross-FK gates (this is what the composite validator adds vs 3 separate scripts):
- ARTIFACT_CLASS.output_type_codes  (semicolon-list) FK-resolves into
  OUTPUT_TYPE_REGISTRY.output_type_code (Layer 2 -> Layer 1).
- COMPONENT_PRIMITIVE.parent_artifact_class_codes  (semicolon-list) FK-resolves
  into ARTIFACT_CLASS_REGISTRY.artifact_class_code (Layer 3 -> Layer 2).
- ARTIFACT_CLASS.typical_audience_codes  (semicolon-list) FK-resolves into
  AUDIENCE_REGISTRY.audience_code  (Layer 2 -> external registry).
- ARTIFACT_CLASS.last_review_decision_id + OUTPUT_TYPE.last_review_decision_id +
  COMPONENT_PRIMITIVE.last_review_decision_id  FK-resolves into
  DECISION_REGISTER.csv.
- ARTIFACT_CLASS.render_targets ; OUTPUT_TYPE.render_targets each token must be
  in VALID_RENDER_TARGETS (pdf / web / erp / mail / slide / broadcast).

Wired into ``scripts/validate_hlk.py`` dispatcher and
``config/verification-profiles.json`` profile ``pre_commit``.

Exit codes:
    0 - PASS (all 3 layers valid + cross-FKs resolved).
    1 - FAIL (per-layer schema or cross-FK error).
"""

from __future__ import annotations

import argparse
import csv
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_artifact_class_registry_csv import (  # noqa: E402
    ARTIFACT_CLASS_REGISTRY_FIELDNAMES,
    ArtifactClassRegistryRow,
)
from akos.hlk_component_primitive_registry_csv import (  # noqa: E402
    COMPONENT_PRIMITIVE_REGISTRY_FIELDNAMES,
    ComponentPrimitiveRegistryRow,
    VALID_KINDS,
)
from akos.hlk_output_type_registry_csv import (  # noqa: E402
    OUTPUT_TYPE_REGISTRY_FIELDNAMES,
    OutputTypeRegistryRow,
    VALID_RENDER_TARGETS,
)
from akos.io import REPO_ROOT  # noqa: E402
from akos.log import setup_logging  # noqa: E402

logger = logging.getLogger("akos.output_architecture_registries")

CANONICAL_DIM_DIR = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance"
    / "canonicals" / "dimensions"
)
OUTPUT_TYPE_CSV = CANONICAL_DIM_DIR / "OUTPUT_TYPE_REGISTRY.csv"
ARTIFACT_CLASS_CSV = CANONICAL_DIM_DIR / "ARTIFACT_CLASS_REGISTRY.csv"
COMPONENT_PRIMITIVE_CSV = CANONICAL_DIM_DIR / "COMPONENT_PRIMITIVE_REGISTRY.csv"
AUDIENCE_CSV = CANONICAL_DIM_DIR / "AUDIENCE_REGISTRY.csv"
DECISION_CSV = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance"
    / "canonicals" / "DECISION_REGISTER.csv"
)


def _load_codes(path: Path, code_column: str) -> set[str]:
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        return {
            (row.get(code_column) or "").strip()
            for row in csv.DictReader(fh)
            if row.get(code_column)
        }


def _split_semicolon_list(raw: str) -> list[str]:
    return [tok.strip() for tok in (raw or "").split(";") if tok.strip()]


def _validate_layer1_output_type(errors: list[str]) -> tuple[set[str], int]:
    if not OUTPUT_TYPE_CSV.is_file():
        errors.append(f"missing canonical: {OUTPUT_TYPE_CSV}")
        return set(), 0
    with OUTPUT_TYPE_CSV.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if list(reader.fieldnames or []) != list(OUTPUT_TYPE_REGISTRY_FIELDNAMES):
            errors.append(
                f"OUTPUT_TYPE_REGISTRY header drift: expected={list(OUTPUT_TYPE_REGISTRY_FIELDNAMES)} got={reader.fieldnames}"
            )
            return set(), 0
        rows = list(reader)

    seen: set[str] = set()
    for i, row in enumerate(rows, start=2):
        try:
            OutputTypeRegistryRow.model_validate(
                {k: (v or "") for k, v in row.items() if k}
            )
        except Exception as exc:
            errors.append(
                f"OUTPUT_TYPE row {i} ({row.get('output_type_code', '?')}): Pydantic validation failed: {exc}"
            )
            continue
        code = (row.get("output_type_code") or "").strip()
        if code in seen:
            errors.append(f"OUTPUT_TYPE row {i}: duplicate output_type_code {code!r}")
        seen.add(code)

        for token in _split_semicolon_list(row.get("render_targets", "")):
            if token not in VALID_RENDER_TARGETS:
                errors.append(
                    f"OUTPUT_TYPE row {i} ({code}): render_targets token {token!r} not in {sorted(VALID_RENDER_TARGETS)}"
                )

    return seen, len(rows)


def _validate_layer2_artifact_class(
    output_type_codes: set[str],
    audience_codes: set[str],
    decision_ids: set[str],
    errors: list[str],
) -> tuple[set[str], int]:
    if not ARTIFACT_CLASS_CSV.is_file():
        errors.append(f"missing canonical: {ARTIFACT_CLASS_CSV}")
        return set(), 0
    with ARTIFACT_CLASS_CSV.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if list(reader.fieldnames or []) != list(ARTIFACT_CLASS_REGISTRY_FIELDNAMES):
            errors.append(
                f"ARTIFACT_CLASS_REGISTRY header drift: expected={list(ARTIFACT_CLASS_REGISTRY_FIELDNAMES)} got={reader.fieldnames}"
            )
            return set(), 0
        rows = list(reader)

    seen: set[str] = set()
    for i, row in enumerate(rows, start=2):
        try:
            ArtifactClassRegistryRow.model_validate(
                {k: (v or "") for k, v in row.items() if k}
            )
        except Exception as exc:
            errors.append(
                f"ARTIFACT_CLASS row {i} ({row.get('artifact_class_code', '?')}): Pydantic validation failed: {exc}"
            )
            continue
        code = (row.get("artifact_class_code") or "").strip()
        if code in seen:
            errors.append(f"ARTIFACT_CLASS row {i}: duplicate artifact_class_code {code!r}")
        seen.add(code)

        for token in _split_semicolon_list(row.get("output_type_codes", "")):
            if output_type_codes and token not in output_type_codes:
                errors.append(
                    f"ARTIFACT_CLASS row {i} ({code}): output_type_codes token {token!r} not in OUTPUT_TYPE_REGISTRY"
                )

        for token in _split_semicolon_list(row.get("typical_audience_codes", "")):
            if audience_codes and token not in audience_codes:
                errors.append(
                    f"ARTIFACT_CLASS row {i} ({code}): typical_audience_codes token {token!r} not in AUDIENCE_REGISTRY"
                )

        rdid = (row.get("last_review_decision_id") or "").strip()
        if decision_ids and rdid and rdid not in decision_ids:
            errors.append(
                f"ARTIFACT_CLASS row {i} ({code}): last_review_decision_id {rdid!r} not in DECISION_REGISTER"
            )

    return seen, len(rows)


def _validate_layer3_component_primitive(
    artifact_class_codes: set[str],
    decision_ids: set[str],
    errors: list[str],
) -> tuple[set[str], int]:
    if not COMPONENT_PRIMITIVE_CSV.is_file():
        errors.append(f"missing canonical: {COMPONENT_PRIMITIVE_CSV}")
        return set(), 0
    with COMPONENT_PRIMITIVE_CSV.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if list(reader.fieldnames or []) != list(COMPONENT_PRIMITIVE_REGISTRY_FIELDNAMES):
            errors.append(
                f"COMPONENT_PRIMITIVE_REGISTRY header drift: expected={list(COMPONENT_PRIMITIVE_REGISTRY_FIELDNAMES)} got={reader.fieldnames}"
            )
            return set(), 0
        rows = list(reader)

    seen: set[str] = set()
    for i, row in enumerate(rows, start=2):
        try:
            ComponentPrimitiveRegistryRow.model_validate(
                {k: (v or "") for k, v in row.items() if k}
            )
        except Exception as exc:
            errors.append(
                f"COMPONENT_PRIMITIVE row {i} ({row.get('component_primitive_code', '?')}): Pydantic validation failed: {exc}"
            )
            continue
        code = (row.get("component_primitive_code") or "").strip()
        if code in seen:
            errors.append(f"COMPONENT_PRIMITIVE row {i}: duplicate component_primitive_code {code!r}")
        seen.add(code)

        for token in _split_semicolon_list(row.get("kind", "")):
            if token not in VALID_KINDS:
                errors.append(
                    f"COMPONENT_PRIMITIVE row {i} ({code}): kind token {token!r} not in {sorted(VALID_KINDS)}"
                )

        for token in _split_semicolon_list(row.get("parent_artifact_class_codes", "")):
            if artifact_class_codes and token not in artifact_class_codes:
                errors.append(
                    f"COMPONENT_PRIMITIVE row {i} ({code}): parent_artifact_class_codes token {token!r} not in ARTIFACT_CLASS_REGISTRY"
                )

        rdid = (row.get("last_review_decision_id") or "").strip()
        if decision_ids and rdid and rdid not in decision_ids:
            errors.append(
                f"COMPONENT_PRIMITIVE row {i} ({code}): last_review_decision_id {rdid!r} not in DECISION_REGISTER"
            )

    return seen, len(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-log", action="store_true", help="emit structured logs")
    args = parser.parse_args(argv)
    setup_logging(json_output=args.json_log)

    print("\n  Output-architecture registries validator (I86 Wave K + L; D-IH-86-BB + D-IH-86-BG)")
    print("  " + "=" * 70)

    audience_codes = _load_codes(AUDIENCE_CSV, "audience_code")
    decision_ids = _load_codes(DECISION_CSV, "decision_id")

    errors: list[str] = []
    output_type_codes, ot_count = _validate_layer1_output_type(errors)
    artifact_class_codes, ac_count = _validate_layer2_artifact_class(
        output_type_codes, audience_codes, decision_ids, errors
    )
    _, cp_count = _validate_layer3_component_primitive(
        artifact_class_codes, decision_ids, errors
    )

    print(f"  Layer 1 OUTPUT_TYPE rows:        {ot_count}")
    print(f"  Layer 2 ARTIFACT_CLASS rows:     {ac_count}")
    print(f"  Layer 3 COMPONENT_PRIMITIVE rows:{cp_count}")
    print(f"  AUDIENCE codes loaded:           {len(audience_codes)}")
    print(f"  DECISION_REGISTER ids loaded:    {len(decision_ids)}")

    if errors:
        print(f"  FAIL: {len(errors)} issue(s)")
        for err in errors[:30]:
            print(f"    - {err}")
        if len(errors) > 30:
            print(f"    ... and {len(errors) - 30} more")
        return 1
    print("  PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
