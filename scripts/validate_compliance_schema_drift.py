#!/usr/bin/env python3
"""Verify every canonical compliance CSV header matches its akos.* fieldnames SSOT.

Generalizes ``scripts/check_process_list_header.py`` (which checks one CSV) to the
full set of canonical compliance CSVs that have a sibling ``akos/hlk_<csv>_csv.py``
fieldnames module. Catches the class of bug RCA'd in the 2026-05-11 release-gate
hygiene pass: a canonical CSV mutated (new column appended) but a downstream
consumer (sync script tuple / mirror DDL / Pydantic model) was not updated in
lockstep, causing silent test failures or runtime data loss.

Per ``.cursor/rules/akos-governance-remediation.mdc`` Design-for-Invariance principle:
the fieldnames tuple is the single source of truth; the CSV header must match
it, and every downstream consumer imports from the tuple rather than hardcoding
its own copy.

Usage (repo root):

    py scripts/validate_compliance_schema_drift.py
    py scripts/validate_compliance_schema_drift.py --json

Exit codes:
    0 — every registered CSV header matches its SSOT tuple
    1 — at least one drift detected (operator must reconcile)
    2 — internal error (missing module / import failure)
"""

from __future__ import annotations

import argparse
import csv
import importlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


# Registry of canonical CSVs that carry an akos.* fieldnames SSOT. Each entry is
# (csv_path_relative_to_repo_root, akos_module_name, fieldnames_attribute_name).
#
# When a new canonical CSV ships with a sibling akos/hlk_<csv>_csv.py module,
# append a row here so this validator covers it. Per the cursor-rule sync row
# in akos-docs-config-sync.mdc, edits to either side require updating both.
_REGISTRY: tuple[tuple[str, str, str], ...] = (
    (
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv",
        "akos.hlk_process_csv",
        "PROCESS_LIST_FIELDNAMES",
    ),
    (
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv",
        "akos.hlk_baseline_org_csv",
        "BASELINE_ORGANISATION_FIELDNAMES",
    ),
    # I81 P2 T1 (D-IH-81-Q under D-IH-81-G umbrella, 2026-05-23): moved to finops/ per I22 forward layout.
    (
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/finops/FINOPS_COUNTERPARTY_REGISTER.csv",
        "akos.hlk_finops_counterparty_csv",
        "FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES",
    ),
    (
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/GOI_POI_REGISTER.csv",
        "akos.hlk_goipoi_csv",
        "GOIPOI_REGISTER_FIELDNAMES",
    ),
    (
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/advops/ADVISER_ENGAGEMENT_DISCIPLINES.csv",
        "akos.hlk_adviser_disciplines_csv",
        "ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES",
    ),
    (
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/advops/ADVISER_OPEN_QUESTIONS.csv",
        "akos.hlk_adviser_questions_csv",
        "ADVISER_OPEN_QUESTIONS_FIELDNAMES",
    ),
    (
        # I81 P2 T3 (D-IH-81-S under D-IH-81-G umbrella, 2026-05-23): moved + renamed to advops/FILED_INSTRUMENTS.csv.
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/advops/FILED_INSTRUMENTS.csv",
        "akos.hlk_filed_instruments_csv",
        "FILED_INSTRUMENTS_FIELDNAMES",
    ),
    (
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PROGRAM_REGISTRY.csv",
        "akos.hlk_program_registry_csv",
        "PROGRAM_REGISTRY_FIELDNAMES",
    ),
    (
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/TOPIC_REGISTRY.csv",
        "akos.hlk_topic_registry_csv",
        "TOPIC_REGISTRY_FIELDNAMES",
    ),
    (
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PERSONA_REGISTRY.csv",
        "akos.hlk_persona_registry_csv",
        "PERSONA_REGISTRY_FIELDNAMES",
    ),
    (
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PERSONA_SCENARIO_REGISTRY.csv",
        "akos.hlk_persona_scenario_csv",
        "PERSONA_SCENARIO_REGISTRY_FIELDNAMES",
    ),
    (
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv",
        "akos.hlk_channel_touchpoint_registry_csv",
        "CHANNEL_TOUCHPOINT_REGISTRY_FIELDNAMES",
    ),
    (
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/SOURCING_REGISTER.csv",
        "akos.hlk_sourcing_register_csv",
        "SOURCING_REGISTER_FIELDNAMES",
    ),
    (
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/SKILL_REGISTRY.csv",
        "akos.hlk_skill_registry_csv",
        "SKILL_REGISTRY_FIELDNAMES",
    ),
    (
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/TOUCHPOINT_KIT_CELL_REGISTRY.csv",
        "akos.hlk_touchpoint_kit_cell_csv",
        "TOUCHPOINT_KIT_CELL_FIELDNAMES",
    ),
    (
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/POLICY_REGISTER.csv",
        "akos.hlk_policy_register_csv",
        "POLICY_REGISTER_FIELDNAMES",
    ),
    (
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPO_HEALTH_SNAPSHOT.csv",
        "akos.hlk_repo_health_csv",
        "REPO_HEALTH_SNAPSHOT_FIELDNAMES",
    ),
    (
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPOSITORY_REGISTRY.csv",
        "akos.hlk_repository_registry_csv",
        "REPOSITORY_REGISTRY_FIELDNAMES",
    ),
    (
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv",
        "akos.hlk_initiative_registry_csv",
        "INITIATIVE_REGISTRY_FIELDNAMES",
    ),
    (
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv",
        "akos.hlk_ops_register_csv",
        "OPS_REGISTER_FIELDNAMES",
    ),
    (
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/CYCLE_REGISTER.csv",
        "akos.hlk_cycle_register_csv",
        "CYCLE_REGISTER_FIELDNAMES",
    ),
    (
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv",
        "akos.hlk_decision_register_csv",
        "DECISION_REGISTER_FIELDNAMES",
    ),
    # I73 P1 (D-IH-73-C sibling-dimension; D-IH-73-D 7-class taxonomy).
    (
        "docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv",
        "akos.hlk_engagement_model_csv",
        "ENGAGEMENT_MODEL_FIELDNAMES",
    ),
    # I84 P3 (D-IH-84-F 18-column schema + 8 enum frozensets; substrate doctrine canonical).
    (
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv",
        "akos.hlk_substrate_registry_csv",
        "SUBSTRATE_REGISTRY_FIELDNAMES",
    ),
)


def _read_header(csv_path: Path) -> list[str] | None:
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        try:
            return next(reader)
        except StopIteration:
            return None


def _check_one(csv_rel: str, module_name: str, attr_name: str) -> dict:
    result: dict = {
        "csv": csv_rel,
        "module": module_name,
        "attr": attr_name,
        "status": "fail",
        "detail": "",
    }
    csv_path = REPO_ROOT / csv_rel
    if not csv_path.is_file():
        result["detail"] = f"csv not found: {csv_path}"
        return result
    try:
        mod = importlib.import_module(module_name)
    except ImportError as exc:
        result["detail"] = f"import error: {exc}"
        return result
    if not hasattr(mod, attr_name):
        result["detail"] = f"{module_name} has no attribute {attr_name}"
        return result
    expected = list(getattr(mod, attr_name))
    actual = _read_header(csv_path)
    if actual is None:
        result["detail"] = "csv is empty (no header row)"
        return result
    if actual == expected:
        result["status"] = "pass"
        result["detail"] = f"{len(actual)} columns aligned"
        return result
    missing_from_csv = [c for c in expected if c not in actual]
    extra_in_csv = [c for c in actual if c not in expected]
    parts: list[str] = []
    if missing_from_csv:
        parts.append(f"columns in SSOT tuple but absent from CSV: {missing_from_csv}")
    if extra_in_csv:
        parts.append(f"columns in CSV but absent from SSOT tuple: {extra_in_csv}")
    if not parts:
        parts.append(f"column order drift (expected {expected}; got {actual})")
    result["detail"] = "; ".join(parts)
    return result


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true", help="emit one JSON object per registered CSV")
    args = ap.parse_args(argv)

    rows = [_check_one(csv_rel, mod, attr) for csv_rel, mod, attr in _REGISTRY]
    failed = [r for r in rows if r["status"] != "pass"]

    if args.json:
        for r in rows:
            print(json.dumps(r))
    else:
        print(f"validate_compliance_schema_drift: checked {len(rows)} canonical CSVs against akos.* SSOT tuples")
        for r in rows:
            marker = "OK" if r["status"] == "pass" else "FAIL"
            print(f"  [{marker}] {r['csv']:<80s} -> {r['module']}.{r['attr']}  {r['detail']}")
        if failed:
            print(f"\nFAIL: {len(failed)} canonical CSV(s) drifted from their akos.* SSOT")
            print("hint: either update the CSV header to match the tuple, or extend the tuple to match the new column set.")
            print("      every downstream consumer (sync script / mirror DDL / Pydantic model) reads from the tuple.")
        else:
            print(f"\nPASS: every canonical CSV header aligns with its akos.* SSOT tuple")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
