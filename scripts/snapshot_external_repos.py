#!/usr/bin/env python3
"""Initiative 32 P7 (D-IH-32-L) — pull-based snapshot of external Holistika repos.

Reads each external repo's local clone, derives compliance signals, and writes
one row per repo to ``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPO_HEALTH_SNAPSHOT.csv``.

Default clone roots (override via env ``AKOS_EXTERNAL_REPO_ROOTS`` — JSON map):
- boilerplate: ``c:\\Users\\Shadow\\cd_shadow\\root_cd\\boilerplate``
- hlk-erp:     ``c:\\Users\\Shadow\\cd_shadow\\root_cd\\hlk-erp``
- kirbe:       ``c:\\Users\\Shadow\\cd_shadow\\root_cd\\kirbe``

Cadence: weekly (cron) + on-demand. Per D-IH-32-L the snapshot is pull-based;
external repos push nothing to AKOS authoring surfaces. Per R-32-14, staleness
of the local clone is visible via ``commit_sha_at_snapshot``; operator runs
``git pull`` in each clone before snapshotting if a fresh probe is needed.

Usage::

    py scripts/snapshot_external_repos.py             # writes REPO_HEALTH_SNAPSHOT.csv
    py scripts/snapshot_external_repos.py --check-only # dry-run; print rows, no write
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_repo_health_csv import REPO_HEALTH_SNAPSHOT_FIELDNAMES
from akos.io import REPO_ROOT

CSV_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "REPO_HEALTH_SNAPSHOT.csv"
MIRROR_TEMPLATE = REPO_ROOT / ".cursor" / "rules" / "akos-mirror-template.mdc"

DEFAULT_REPO_ROOTS: dict[str, Path] = {
    # Keys are repo_slug values from REPOSITORIES_REGISTRY.md (validator FK).
    # Override the operator-side path map via env AKOS_EXTERNAL_REPO_ROOTS (JSON).
    "boilerplate": Path(r"c:\Users\Shadow\cd_shadow\root_cd\boilerplate"),
    "hlk-erp": Path(r"c:\Users\Shadow\cd_shadow\root_cd\hlk-erp"),
    "kirbe-platform": Path(r"c:\Users\Shadow\cd_shadow\root_cd\kirbe"),
}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
LANGUAGE_FIELD_RE = re.compile(r"^language\s*:\s*(en|es|fr)\s*$", re.MULTILINE)

# Brand-jargon forbidden tokens per BRAND_JARGON_AUDIT.md §4 (subset; conservative).
JARGON_TOKENS: tuple[str, ...] = (
    "AKOS",
    "topic_",
    "plane",
    "RBAC",
    "RLS",
    "pgvector",
    "TODO[OPERATOR-",
    "_dtp_",
    "MADEIRA",
)


def _resolve_repo_roots() -> dict[str, Path]:
    override = os.environ.get("AKOS_EXTERNAL_REPO_ROOTS")
    if override:
        try:
            data = json.loads(override)
            return {k: Path(v) for k, v in data.items()}
        except Exception:
            pass
    return DEFAULT_REPO_ROOTS


def _git_short_sha(repo_path: Path) -> str:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--short=12", "HEAD"],
            capture_output=True, text=True, cwd=repo_path, timeout=2,
        )
        if r.returncode == 0:
            return r.stdout.strip()
    except Exception:
        pass
    return "unknown"


def _count_cursor_rules(repo_path: Path) -> int:
    rules_dir = repo_path / ".cursor" / "rules"
    if not rules_dir.is_dir():
        return 0
    return sum(1 for _ in rules_dir.glob("*.mdc"))


def _has_external_repo_contract(repo_path: Path) -> bool:
    return (repo_path / "EXTERNAL_REPO_CONTRACT.md").is_file()


def _has_akos_mirror_rule(repo_path: Path) -> bool:
    return (repo_path / ".cursor" / "rules" / "akos-mirror.mdc").is_file()


def _language_frontmatter_pct(repo_path: Path, sample_limit: int = 200) -> float:
    """Scan up to sample_limit .md files; report % declaring `language: en|es|fr`."""
    md_files: list[Path] = []
    for p in repo_path.rglob("*.md"):
        # Skip vendor / build / cache dirs.
        rel = p.relative_to(repo_path).as_posix()
        if any(seg in rel for seg in ("node_modules/", ".next/", ".venv/", "dist/", "build/", ".git/")):
            continue
        md_files.append(p)
        if len(md_files) >= sample_limit:
            break
    if not md_files:
        return 0.0
    with_lang = 0
    for f in md_files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        m = FRONTMATTER_RE.match(text)
        if not m:
            continue
        if LANGUAGE_FIELD_RE.search(m.group(1)):
            with_lang += 1
    return round(100.0 * with_lang / len(md_files), 2)


def _brand_jargon_violations(repo_path: Path, sample_limit: int = 200) -> int:
    """Scan up to sample_limit .md files; count files containing any JARGON_TOKEN."""
    files_scanned = 0
    violations = 0
    for p in repo_path.rglob("*.md"):
        rel = p.relative_to(repo_path).as_posix()
        if any(seg in rel for seg in ("node_modules/", ".next/", ".venv/", "dist/", "build/", ".git/")):
            continue
        files_scanned += 1
        if files_scanned > sample_limit:
            break
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if any(tok in text for tok in JARGON_TOKENS):
            violations += 1
    return violations


def _embedded_obsidian_present(repo_path: Path) -> bool:
    """Boilerplate-specific watch per D-IH-32-N."""
    candidates = [
        repo_path / "app" / "dashboard" / "applications" / "kms" / "obsidian-holistika-main",
    ]
    return any(c.is_dir() for c in candidates)


def _ci_workflow_present(repo_path: Path) -> bool:
    return (repo_path / ".github" / "workflows" / "ci.yml").is_file()


def _dependabot_present(repo_path: Path) -> bool:
    return (repo_path / ".github" / "dependabot.yml").is_file() or (repo_path / ".github" / "dependabot.yaml").is_file()


def _codeowners_present(repo_path: Path) -> bool:
    return (repo_path / ".github" / "CODEOWNERS").is_file() or (repo_path / "CODEOWNERS").is_file()


def _license_present(repo_path: Path) -> bool:
    for name in ("LICENSE", "LICENSE.md", "LICENSE.txt"):
        if (repo_path / name).is_file():
            return True
    return False


def _akos_mirror_sha256_match(repo_path: Path) -> str:
    """Return 'true' / 'false' / '' when N/A (rule absent)."""
    consumer = repo_path / ".cursor" / "rules" / "akos-mirror.mdc"
    if not consumer.is_file() or not MIRROR_TEMPLATE.is_file():
        return ""
    h_consumer = hashlib.sha256(consumer.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
    h_template = hashlib.sha256(MIRROR_TEMPLATE.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
    return "true" if h_consumer == h_template else "false"


def _secret_rotation_oldest_age_days(repo_path: Path) -> int:
    """Return age (days) of the oldest tracked secret, or -1 when unknown."""
    runbook = repo_path / "docs" / "runbooks" / "secrets-rotation.md"
    if not runbook.is_file():
        return -1
    try:
        text = runbook.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return -1
    today = date.today()
    ages: list[int] = []
    fm = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if fm:
        for m in re.finditer(r"^\s*-\s+name:\s*(\S+)\s*\n\s+last_rotated:\s*(\d{4}-\d{2}-\d{2})", fm.group(1), re.MULTILINE):
            try:
                d = datetime.strptime(m.group(2), "%Y-%m-%d").date()
                ages.append((today - d).days)
            except ValueError:
                continue
    if not ages:
        return -1
    return max(ages)


def _row_for(repo_slug: str, repo_path: Path, snapshot_date: str) -> dict[str, str]:
    if not repo_path.is_dir():
        return {
            "repo_slug": repo_slug,
            "snapshot_date": snapshot_date,
            "commit_sha_at_snapshot": "unknown",
            "cursor_rule_count": "0",
            "has_external_repo_contract": "false",
            "has_akos_mirror_rule": "false",
            "language_frontmatter_compliance_pct": "0.0",
            "brand_jargon_violations": "0",
            "embedded_obsidian_snapshot_present": "false",
            "ci_workflow_present": "false",
            "dependabot_present": "false",
            "codeowners_present": "false",
            "license_present": "false",
            "akos_mirror_sha256_match": "",
            "secret_rotation_oldest_age_days": "-1",
            "notes": f"local clone not found at {repo_path}",
        }
    return {
        "repo_slug": repo_slug,
        "snapshot_date": snapshot_date,
        "commit_sha_at_snapshot": _git_short_sha(repo_path),
        "cursor_rule_count": str(_count_cursor_rules(repo_path)),
        "has_external_repo_contract": str(_has_external_repo_contract(repo_path)).lower(),
        "has_akos_mirror_rule": str(_has_akos_mirror_rule(repo_path)).lower(),
        "language_frontmatter_compliance_pct": str(_language_frontmatter_pct(repo_path)),
        "brand_jargon_violations": str(_brand_jargon_violations(repo_path)),
        "embedded_obsidian_snapshot_present": str(_embedded_obsidian_present(repo_path)).lower(),
        "ci_workflow_present": str(_ci_workflow_present(repo_path)).lower(),
        "dependabot_present": str(_dependabot_present(repo_path)).lower(),
        "codeowners_present": str(_codeowners_present(repo_path)).lower(),
        "license_present": str(_license_present(repo_path)).lower(),
        "akos_mirror_sha256_match": _akos_mirror_sha256_match(repo_path),
        "secret_rotation_oldest_age_days": str(_secret_rotation_oldest_age_days(repo_path)),
        "notes": "scanned by snapshot_external_repos.py",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Snapshot external Holistika repos for REPO_HEALTH_SNAPSHOT.csv")
    parser.add_argument("--check-only", action="store_true", help="Dry-run; print rows, do not write CSV.")
    args = parser.parse_args()

    print("\n  REPO_HEALTH_SNAPSHOT — external repo health scanner")
    print("  " + "=" * 60)

    snapshot_date = date.today().isoformat()
    repo_roots = _resolve_repo_roots()
    rows: list[dict[str, str]] = []
    for slug, path in sorted(repo_roots.items()):
        row = _row_for(slug, path, snapshot_date)
        rows.append(row)
        print(
            f"  {slug:14s} sha={row['commit_sha_at_snapshot']:14s} "
            f"contract={row['has_external_repo_contract']:5s} "
            f"akos_mirror={row['has_akos_mirror_rule']:5s} "
            f"lang_pct={row['language_frontmatter_compliance_pct']:6s} "
            f"jargon={row['brand_jargon_violations']:4s} "
            f"obsidian={row['embedded_obsidian_snapshot_present']}"
        )

    if args.check_only:
        print(f"\n  --check-only: would write {len(rows)} rows to {CSV_PATH.relative_to(REPO_ROOT)}")
        return 0

    # Write the snapshot CSV (overwrite; weekly cadence treats each run as a full replacement;
    # the audit trail lives in compliance.repo_health_snapshot_mirror's append-only history).
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CSV_PATH.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(REPO_HEALTH_SNAPSHOT_FIELDNAMES))
        writer.writeheader()
        writer.writerows(rows)
    print(f"\n  wrote {len(rows)} rows to {CSV_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
