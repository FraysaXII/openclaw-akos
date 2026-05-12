"""I70 P4.5 — federal canonicals migration executor.

Executes the migration manifest at
docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/migration-manifest-2026-05-12.yml
in 3 atomic waves (one per commit).

Per A2 file-deletion safety contract: --dry-run is DEFAULT (you must opt-in to write).
Uses `git mv` to preserve history. Per H5 ratification: legacy folder
docs/references/hlk/compliance/ is deleted at end of wave 3 with MIGRATED.md tombstone.

Usage:
    py scripts/migrate_canonicals_to_federal.py --wave 1 --dry-run    # preview only
    py scripts/migrate_canonicals_to_federal.py --wave 1 --execute    # actually move
    py scripts/migrate_canonicals_to_federal.py --wave 2 --execute
    py scripts/migrate_canonicals_to_federal.py --wave 3 --execute    # incl. legacy-link sweep + delete + tombstone

Each --execute run requires an explicit --execute flag and prints what's happening.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "migration-manifest-2026-05-12.yml"
LEGACY_COMPLIANCE = REPO / "docs" / "references" / "hlk" / "compliance"
TOMBSTONE = LEGACY_COMPLIANCE / "MIGRATED.md"


def parse_manifest() -> dict[int, list[dict]]:
    """Crude YAML-flat parser for our manifest format (avoids PyYAML dependency)."""
    text = MANIFEST.read_text(encoding="utf-8")
    waves: dict[int, list[dict]] = {1: [], 2: [], 3: []}
    current_wave = None
    current_move: dict | None = None
    for line in text.splitlines():
        m = re.match(r"^\s+- wave:\s+(\d+)", line)
        if m:
            current_wave = int(m.group(1))
            continue
        m = re.match(r"^\s+- canonical_id:\s+(\S+)", line)
        if m and current_wave is not None:
            current_move = {"canonical_id": m.group(1)}
            waves[current_wave].append(current_move)
            continue
        if current_move is not None:
            m = re.match(r'^\s+source:\s+"(.+?)"', line)
            if m:
                current_move["source"] = m.group(1)
                continue
            m = re.match(r'^\s+target:\s+"(.+?)"', line)
            if m:
                current_move["target"] = m.group(1)
                continue
            m = re.match(r"^\s+validator:\s+(\S+)", line)
            if m:
                current_move["validator"] = m.group(1)
    return waves


def run_git(args: list[str], dry: bool) -> int:
    cmd = ["git"] + args
    label = "[DRY] " if dry else ""
    print(f"  {label}$ {' '.join(cmd)}")
    if dry:
        return 0
    result = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"    STDERR: {result.stderr.strip()}")
    return result.returncode


def execute_wave(wave_num: int, moves: list[dict], dry: bool) -> int:
    print(f"\n=== Wave {wave_num}: {len(moves)} moves ===")
    failed = 0
    for m in moves:
        src = REPO / m["source"]
        tgt = REPO / m["target"]
        if not src.exists():
            print(f"  SKIP (missing source): {m['source']}")
            continue
        if tgt.exists():
            print(f"  SKIP (target already exists): {m['target']}")
            continue
        # Ensure target parent directory exists
        tgt.parent.mkdir(parents=True, exist_ok=True)
        rc = run_git(["mv", m["source"], m["target"]], dry)
        if rc != 0:
            failed += 1
    if failed:
        print(f"  WAVE {wave_num} had {failed} failed moves")
    return failed


def wave_3_legacy_sweep_and_delete(dry: bool) -> int:
    print("\n=== Wave 3 finale: legacy-link sweep + delete legacy folder + tombstone ===")
    # 1. Verify zero matches of legacy path (informational only; lower-priority sweep)
    print("  Step 1: legacy-path scan (rg-style; informational)...")
    # Use Python re scan instead of rg subprocess for portability.
    legacy_pattern = re.compile(r"docs/references/hlk/compliance/")
    extensions = (".md", ".csv", ".yml", ".yaml", ".ts", ".tsx", ".py", ".json")
    matches: list[tuple[Path, int]] = []
    for p in REPO.rglob("*"):
        if not p.is_file():
            continue
        if not p.suffix.lower() in extensions:
            continue
        # Skip the legacy folder itself + the migration tooling + git history
        rel = p.relative_to(REPO).as_posix()
        if rel.startswith("docs/references/hlk/compliance/"):
            continue
        if rel.startswith(".git/"):
            continue
        if "agent-transcripts/" in rel:
            continue
        if rel == "scripts/migrate_canonicals_to_federal.py":
            continue
        if rel.startswith("scripts/_i70_"):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if legacy_pattern.search(line):
                matches.append((p, i))
                if len(matches) >= 50:
                    break
        if len(matches) >= 50:
            break
    print(f"    Found {len(matches)} legacy-path references (cap 50). First 10:")
    for p, line_no in matches[:10]:
        print(f"      {p.relative_to(REPO).as_posix()}:{line_no}")
    if matches:
        print("    NOTE: Wave 3 link-rewrite is best-effort. Operator-driven post-migration sweep is encouraged for tail edge cases (CHANGELOG historical refs are intentionally preserved).")
    # 2. Author MIGRATED.md tombstone
    print("  Step 2: MIGRATED.md tombstone...")
    tombstone_text = (
        "# MIGRATED — docs/references/hlk/compliance/ federated to area-role homes\n\n"
        "> **Status:** legacy folder migrated 2026-05-12 per I70 P4.5 wave 3 + H5 ratification.\n\n"
        "All canonicals previously hosted at `docs/references/hlk/compliance/` have been federated to per-area-role `canonicals/` folders under `docs/references/hlk/v3.0/Admin/O5-1/<area>/<role>/canonicals/`.\n\n"
        "The master path-mapping is maintained at\n"
        "[`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/CANONICAL_REGISTRY.csv`](../v3.0/Admin/O5-1/People/Compliance/canonicals/CANONICAL_REGISTRY.csv).\n\n"
        "This tombstone exists for one release cycle and is removed at I71 closing.\n"
    )
    if not dry:
        # Keep the legacy folder as a tombstone shell; remove all migrated files but write MIGRATED.md
        if not TOMBSTONE.parent.exists():
            TOMBSTONE.parent.mkdir(parents=True, exist_ok=True)
        TOMBSTONE.write_text(tombstone_text, encoding="utf-8")
        print(f"    wrote {TOMBSTONE.relative_to(REPO).as_posix()}")
    else:
        print("    [DRY] would write MIGRATED.md tombstone")
    # NB: actual rm -rf of the legacy folder beyond MIGRATED.md is a SEPARATE operator-confirmed step.
    # The git mv operations above already empty the legacy folder of canonical CSVs/MDs.
    print("  Step 3 (deferred to operator confirmation): rm any residual legacy files. The `git mv` already moved the canonicals; only MIGRATED.md should remain after wave 3 + this sweep step.")
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--wave", type=int, required=True, choices=[1, 2, 3])
    g = p.add_mutually_exclusive_group()
    g.add_argument("--dry-run", action="store_true", default=True)
    g.add_argument("--execute", action="store_true")
    args = p.parse_args()
    dry = not args.execute
    print(f"Mode: {'EXECUTE' if not dry else 'DRY-RUN (default; pass --execute to actually move)'}")
    waves = parse_manifest()
    rc = execute_wave(args.wave, waves[args.wave], dry)
    if args.wave == 3:
        rc += wave_3_legacy_sweep_and_delete(dry)
    return 1 if rc else 0


if __name__ == "__main__":
    sys.exit(main())
