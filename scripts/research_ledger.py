#!/usr/bin/env python3
"""Unified research ledger engine — bootstrap / append / validate / census.

Replaces one-off *_ledger_bootstrap.py and *_ledger_append.py scripts.
Paired SOP target: SOP-RESEARCH_ACTION_001 (mint at Automation OS D4).

Usage:
    py scripts/research_ledger.py bootstrap --pack akos-automation-os-governance-2026-06-10 --tranche R1
    py scripts/research_ledger.py validate --pack akos-automation-os-governance-2026-06-10
    py scripts/research_ledger.py normalize-prongs --pack akos-automation-os-governance-2026-06-10
    py scripts/research_ledger.py census --pack akos-automation-os-governance-2026-06-10 --dry-run
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.research_ledger_ops import (  # noqa: E402
    append_validated,
    ledger_path,
    load_rows,
    load_runbook_prong_map,
    normalize_ledger_prong_rows,
    pack_dir,
    rel_url,
    resolve_prong_for_script,
    write_rows,
)

ONE_OFF_SCRIPTS = (
    "holistic_agentic_r1_ledger_bootstrap.py",
    "holistic_agentic_r2_ledger_append.py",
    "holistic_agentic_r3_ledger_append.py",
    "i94_p4_ops_research_ledger_bootstrap.py",
    "i93_p7_hygiene_apply.py",
    "i94_p3_placement_updates.py",
    "i94_area09_process_list_tranche.py",
)

GOVERNED_PRIORITY = (
    "verify.py",
    "release-gate.py",
    "validate_research_action.py",
    "validate_hlk.py",
    "research_radar_sweep.py",
    "inter_wave_regression_sweep.py",
    "synthesis_before_tranche_check.py",
    "validate_process_list_pairing.py",
    "validate_research_radar.py",
    "validate_intelligenceops_register.py",
    "techops_reliability_check.py",
    "dataops_quality_check.py",
    "check-drift.py",
    "bootstrap.py",
    "doctor.py",
)


def _manifest_path(pack_root: Path, tranche: str) -> Path:
    return pack_root / "tranches" / f"{tranche.lower()}-manifest.json"


def _load_manifest(pack_root: Path, tranche: str) -> dict:
    path = _manifest_path(pack_root, tranche)
    if not path.is_file():
        raise SystemExit(f"manifest not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _census_rows(
    repo_root: Path,
    manifest: dict,
    tranche: str,
    runbook_map: dict[str, str],
) -> list[dict[str, str]]:
    census = manifest.get("census", {})
    if not census.get("enabled"):
        return []
    scripts_dir = repo_root / "scripts"
    prefix = manifest["id_prefix"]
    topic = census.get("topic_cluster", "corp_runtime_script")
    max_rows = int(census.get("max_rows", 25))
    start_seq = int(census.get("start_seq", 1))
    ordered: list[Path] = []
    for name in ONE_OFF_SCRIPTS:
        p = scripts_dir / name
        if p.is_file():
            ordered.append(p)
    for name in GOVERNED_PRIORITY:
        p = scripts_dir / name
        if p.is_file() and p not in ordered:
            ordered.append(p)
    for p in sorted(scripts_dir.glob("*.py")):
        if p.name.startswith("_"):
            continue
        if p not in ordered:
            ordered.append(p)
    rows: list[dict[str, str]] = []
    seq = start_seq
    for path in ordered:
        if len(rows) >= max_rows:
            break
        name = path.name
        script_rel = f"scripts/{name}"
        prong, binding = resolve_prong_for_script(script_rel, runbook_map=runbook_map)
        anti = ""
        if name in ONE_OFF_SCRIPTS:
            anti = f"replaces-one-off:{name}; ICS:Load-bearing; "
        rows.append(
            {
                "source_id": f"SRC-{prefix}I-{seq:03d}",
                "prong": prong,
                "topic_cluster": topic,
                "source_title_or_owner": name,
                "url": rel_url(repo_root, path),
                "format": "internal_canonical",
                "source_category": "CORPINT",
                "source_level": "5.1",
                "holistika_reliability_score": "5",
                "external_perceived_credibility_score": "2",
                "control_confidence_level": "Safe",
                "decision_use": "def-script-census",
                "notes": (
                    f"{anti}{binding}; R1 script census; impacts: automation registry; "
                    f"impacted-by: TECH_AUTOMATION_REGISTRY"
                ),
            }
        )
        seq += 1
    return rows


def cmd_bootstrap(pack_slug: str, tranche: str) -> int:
    pack_root = pack_dir(REPO_ROOT, pack_slug)
    manifest = _load_manifest(pack_root, tranche)
    path = ledger_path(pack_root)
    prior = load_rows(path)
    candidates: list[dict[str, str]] = []
    candidates.extend(manifest.get("rows", []))
    runbook_map = load_runbook_prong_map(REPO_ROOT)
    candidates.extend(_census_rows(REPO_ROOT, manifest, tranche, runbook_map))
    merged, add_corp, add_osint = append_validated(
        prior,
        candidates,
        id_prefix=manifest["id_prefix"],
        corpint_target=int(manifest["corpint_target"]),
        osint_target=int(manifest["osint_target"]),
    )
    write_rows(path, merged)
    corp_t, osint_t = int(manifest["corpint_target"]), int(manifest["osint_target"])
    print(f"Wrote {path}")
    print(
        f"  prior={len(prior)} + corpint={add_corp} + osint={add_osint} "
        f"= total={len(merged)} (targets {corp_t}/{osint_t})"
    )
    return 0


def cmd_validate(pack_slug: str) -> int:
    import importlib.util

    path = ledger_path(pack_dir(REPO_ROOT, pack_slug))
    val_path = REPO_ROOT / "scripts/validate_research_action.py"
    spec = importlib.util.spec_from_file_location("validate_research_action", val_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load validator: {val_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    ok, messages, summary = mod.validate_source_ledger(path)
    for msg in messages:
        print(msg, file=sys.stderr)
    if ok and summary:
        print(
            f"PASS: {summary.source_count} rows; "
            f"topics={len(summary.topic_clusters)}; "
            f"control_confidence={summary.control_confidence_counts}"
        )
    return 0 if ok else 1


def cmd_normalize_prongs(pack_slug: str, dry_run: bool) -> int:
    pack_root = pack_dir(REPO_ROOT, pack_slug)
    path = ledger_path(pack_root)
    prior = load_rows(path)
    if not prior:
        raise SystemExit(f"ledger empty or missing: {path}")
    normalized, changed = normalize_ledger_prong_rows(prior)
    if dry_run:
        print(f"dry-run: {path} would rewrite {changed}/{len(prior)} prong cells")
        return 0
    write_rows(path, normalized)
    print(f"Wrote {path} — normalized {changed}/{len(prior)} prong cells to BL-*")
    return cmd_validate(pack_slug)


def cmd_census(pack_slug: str, dry_run: bool) -> int:
    pack_root = pack_dir(REPO_ROOT, pack_slug)
    manifest = _load_manifest(pack_root, "R1")
    rows = _census_rows(REPO_ROOT, manifest, "R1", load_runbook_prong_map(REPO_ROOT))
    print(f"census rows: {len(rows)}")
    for row in rows[:10]:
        print(f"  {row['source_id']} {row['source_title_or_owner']}")
    if len(rows) > 10:
        print(f"  ... +{len(rows) - 10} more")
    if dry_run:
        print("(dry-run — no write)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Research ledger engine")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_boot = sub.add_parser("bootstrap", help="Bootstrap/append tranche from manifest")
    p_boot.add_argument("--pack", required=True, help="Pack folder slug under docs/wip/intelligence/")
    p_boot.add_argument("--tranche", required=True, help="Tranche id e.g. R1")

    p_val = sub.add_parser("validate", help="Validate pack ledger")
    p_val.add_argument("--pack", required=True)

    p_norm = sub.add_parser(
        "normalize-prongs",
        help="Rewrite ledger prong column to baseline BL-* consumer IDs",
    )
    p_norm.add_argument("--pack", required=True)
    p_norm.add_argument("--dry-run", action="store_true")

    p_cen = sub.add_parser("census", help="Preview script census rows")
    p_cen.add_argument("--pack", required=True)
    p_cen.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()
    if args.cmd == "bootstrap":
        return cmd_bootstrap(args.pack, args.tranche)
    if args.cmd == "validate":
        return cmd_validate(args.pack)
    if args.cmd == "normalize-prongs":
        return cmd_normalize_prongs(args.pack, args.dry_run)
    if args.cmd == "census":
        return cmd_census(args.pack, args.dry_run)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
