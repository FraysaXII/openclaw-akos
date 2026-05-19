#!/usr/bin/env python3
"""GitHub repo inventory + classification runbook (I86 Wave H; D-IH-86-AF).

Paired with `SOP-TECH_APPLICATION_GOVERNANCE_001.md` per
[`akos-executable-process-catalog.mdc`](../.cursor/rules/akos-executable-process-catalog.mdc)
RULE 1 (every executable process needs a paired human-readable SOP +
agent-facing runbook). Implements the quarterly inventory sweep, per-row
classification, and drift audit that closes the 92.7% unmanaged-repo gap
surfaced by Lane F-GITHUB inventory report (2026-05-19).

process_list item_id: ``env_tech_dtp_app_governance_quarterly_001`` (D-IH-86-AE).
Discovered by ``scripts/validate_process_list_pairing.py`` via the
``inventory_github*.py`` glob + this item_id reference in the docstring.

Subcommands:

- ``sweep`` — Fetch ``gh repo list FraysaXII --json …``; diff against current
  ``REPOSITORY_REGISTRY.csv`` state; write a drift report at
  ``artifacts/inventory/repo-inventory-<YYYYMMDD>.md``. Read-only against the
  canonical CSV.
- ``classify --repo <slug> --app-class <value>`` — Set ``app_class`` on a single
  row via Pydantic round-trip (validates the row before write).
- ``audit`` — Run ``scripts/validate_repository_registry.py --strict-app-class``
  to surface any rows missing ``app_class`` or ``governance_status``. Read-only.

All subcommands accept ``--dry-run`` (no writes; prints what would happen) and
``--json-log`` (structured JSON logging via ``akos.log.setup_logging``).

Compliance with ``CONTRIBUTING.md`` §"Python Code Standards":
- Pydantic models in ``akos/hlk_repository_registry_csv.py`` (no hand-written
  assert chains for JSON parsing).
- Type hints on every function signature + return type.
- Structured logging via ``akos.log.setup_logging`` (not ``print()`` for
  state changes; ``print()`` only used for human-facing CLI banners).
- ``akos.process.run`` for subprocess shell-out (with explicit timeout; never
  bare ``subprocess.run``).
- Cross-platform ``pathlib.Path`` everywhere.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Literal

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_repository_registry_csv import (  # noqa: E402
    REPOSITORY_REGISTRY_FIELDNAMES,
    VALID_APP_CLASS,
    RepositoryRegistryRow,
)
from akos.log import setup_logging  # noqa: E402
from akos.process import CommandResult, run  # noqa: E402

CSV_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People"
    / "Compliance" / "canonicals" / "REPOSITORY_REGISTRY.csv"
)
DEFAULT_ORG = "FraysaXII"
DEFAULT_LIMIT = 200
INVENTORY_DIR = REPO_ROOT / "artifacts" / "inventory"
VALIDATOR_SCRIPT = REPO_ROOT / "scripts" / "validate_repository_registry.py"

logger = logging.getLogger("akos.inventory_github_repos")


@dataclass(frozen=True)
class GhRepoSnapshot:
    """Snapshot of one repo from `gh repo list ... --json ...`."""

    name: str
    url: str
    visibility: str           # PUBLIC | PRIVATE | INTERNAL
    is_archived: bool
    is_fork: bool
    primary_language: str | None
    created_at: str           # YYYY-MM-DD
    pushed_at: str            # YYYY-MM-DD
    topics: tuple[str, ...]


@dataclass
class InventoryDiff:
    """Result of diffing a fresh GH snapshot against the registry CSV."""

    new_repos: list[GhRepoSnapshot]
    ghost_slugs: list[str]
    changed: list[tuple[str, dict[str, str]]]
    at: date


def _iso_date(value: str) -> str:
    """Coerce a GH ISO-8601 timestamp (e.g. '2026-05-19T12:34:56Z') to YYYY-MM-DD.

    Returns empty string if the input is empty or malformed.
    """
    if not value:
        return ""
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()
    except (ValueError, TypeError):
        return value[:10] if len(value) >= 10 else ""


def parse_gh_repo_list(raw_json: str) -> list[GhRepoSnapshot]:
    """Parse the JSON output of ``gh repo list ... --json …`` into snapshots.

    Tolerates missing fields per the gh CLI's habit of omitting empty values;
    raises ValueError on malformed JSON or non-list payload.
    """
    if not raw_json.strip():
        return []
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        raise ValueError(f"gh repo list output is not valid JSON: {exc}") from exc
    if not isinstance(data, list):
        raise ValueError(f"gh repo list payload must be a JSON array, got {type(data).__name__}")

    snapshots: list[GhRepoSnapshot] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        name = (item.get("name") or "").strip()
        if not name:
            continue
        primary_language = item.get("primaryLanguage")
        if isinstance(primary_language, dict):
            lang_value: str | None = (primary_language.get("name") or "") or None
        else:
            lang_value = None
        topics_raw = item.get("repositoryTopics") or []
        topics: list[str] = []
        if isinstance(topics_raw, list):
            for t in topics_raw:
                if isinstance(t, dict):
                    label = (t.get("name") or "").strip()
                elif isinstance(t, str):
                    label = t.strip()
                else:
                    label = ""
                if label:
                    topics.append(label)
        snapshots.append(
            GhRepoSnapshot(
                name=name,
                url=(item.get("url") or "").strip(),
                visibility=(item.get("visibility") or "").strip().upper(),
                is_archived=bool(item.get("isArchived", False)),
                is_fork=bool(item.get("isFork", False)),
                primary_language=lang_value,
                created_at=_iso_date(item.get("createdAt") or ""),
                pushed_at=_iso_date(item.get("pushedAt") or ""),
                topics=tuple(topics),
            )
        )
    return snapshots


def fetch_github_inventory(
    org: str = DEFAULT_ORG,
    limit: int = DEFAULT_LIMIT,
    runner=run,
) -> list[GhRepoSnapshot]:
    """Call ``gh repo list <org> --limit <N> --json …`` and parse the result.

    The ``runner`` parameter is injectable so tests can stub ``akos.process.run``.
    Returns an empty list (and logs a warning) when the ``gh`` CLI is not
    installed or the call fails — this is a soft failure mode so the SOP's
    quarterly cadence still produces a readable drift report without blocking
    CI when ``gh`` is unavailable in a sandbox.
    """
    fields = (
        "name,url,visibility,isArchived,isFork,primaryLanguage,"
        "createdAt,pushedAt,repositoryTopics"
    )
    args = ["gh", "repo", "list", org, "--limit", str(limit), "--json", fields]
    logger.info("fetching gh inventory: org=%s limit=%d", org, limit)
    result: CommandResult = runner(args, timeout=120)
    if not result.success:
        logger.warning("gh repo list failed (rc=%d): %s", result.returncode, result.stderr.strip())
        return []
    try:
        return parse_gh_repo_list(result.stdout)
    except ValueError as exc:
        logger.error("failed to parse gh output: %s", exc)
        return []


def load_registry_rows(csv_path: Path = CSV_PATH) -> list[dict[str, str]]:
    """Load REPOSITORY_REGISTRY.csv rows; returns empty list if CSV missing."""
    if not csv_path.is_file():
        logger.warning("registry CSV missing at %s", csv_path)
        return []
    with csv_path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != list(REPOSITORY_REGISTRY_FIELDNAMES):
            logger.error(
                "registry CSV header drift: expected %d cols, got %s",
                len(REPOSITORY_REGISTRY_FIELDNAMES),
                reader.fieldnames,
            )
            return []
        return [dict(row) for row in reader if (row.get("repo_slug") or "").strip()]


def diff_against_registry(
    snapshots: list[GhRepoSnapshot],
    rows: list[dict[str, str]],
    at: date | None = None,
) -> InventoryDiff:
    """Compute set differences between GH snapshots and registry rows.

    Cross-reference happens on the *github_url* field because slug naming on the
    AKOS side may differ from the GH repo name (e.g. ``kirbe`` GH repo registers
    as ``kirbe-platform`` slug; ``openclaw-akos`` GH repo aliases to
    ``akos-telemetry-ci``). URL-keying avoids false positives on these aliases.
    """
    at = at or date.today()
    snap_by_url: dict[str, GhRepoSnapshot] = {s.url: s for s in snapshots if s.url}
    rows_by_url: dict[str, dict[str, str]] = {}
    for r in rows:
        url = (r.get("github_url") or "").strip()
        if url:
            rows_by_url.setdefault(url, r)

    new_repos = [s for url, s in snap_by_url.items() if url not in rows_by_url]
    ghost_slugs = [
        (r.get("repo_slug") or "").strip()
        for url, r in rows_by_url.items()
        if url not in snap_by_url
    ]
    changed: list[tuple[str, dict[str, str]]] = []
    for url, row in rows_by_url.items():
        snap = snap_by_url.get(url)
        if not snap:
            continue
        deltas: dict[str, str] = {}
        if snap.visibility and snap.visibility != (row.get("github_visibility") or "").strip():
            deltas["github_visibility"] = snap.visibility
        if snap.pushed_at and snap.pushed_at != (row.get("pushed_at") or "").strip():
            deltas["pushed_at"] = snap.pushed_at
        if snap.primary_language and snap.primary_language != (row.get("primary_language") or "").strip():
            deltas["primary_language"] = snap.primary_language
        if deltas:
            changed.append(((row.get("repo_slug") or "").strip(), deltas))
    return InventoryDiff(
        new_repos=sorted(new_repos, key=lambda s: s.name),
        ghost_slugs=sorted(g for g in ghost_slugs if g),
        changed=sorted(changed, key=lambda c: c[0]),
        at=at,
    )


def classify_default(snapshot: GhRepoSnapshot) -> Literal["research", "experiment", "template", "fork", "archive", "uncategorized"]:
    """Suggest a default `app_class` for a freshly-discovered repo.

    Heuristic order (matches Lane F report §2.1 inventory pattern):
    1. ``is_archived=true`` → ``archive``.
    2. ``is_fork=true`` → ``fork``.
    3. Name pattern matches template signals (``boilerplate``, ``-kit``,
       ``-starter``, ``-template``) → ``template``.
    4. Otherwise → ``experiment`` (lowest-touch default; operator can promote
       to ``research`` or ``production`` later).
    """
    if snapshot.is_archived:
        return "archive"
    if snapshot.is_fork:
        return "fork"
    lower = snapshot.name.lower()
    template_markers = ("boilerplate", "-kit", "-starter", "-template", "starter-")
    if any(marker in lower for marker in template_markers):
        return "template"
    return "experiment"


def render_drift_report(diff: InventoryDiff, org: str = DEFAULT_ORG) -> str:
    """Render the inventory drift report as markdown."""
    lines: list[str] = []
    lines.append(f"# GitHub repo inventory — {org} — {diff.at.isoformat()}")
    lines.append("")
    lines.append(
        "Produced by `scripts/inventory_github_repos.py sweep` per "
        "`SOP-TECH_APPLICATION_GOVERNANCE_001` (I86 Wave H; D-IH-86-AF)."
    )
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- New repos (in GH, not in registry): **{len(diff.new_repos)}**")
    lines.append(f"- Ghost slugs (in registry, not in GH): **{len(diff.ghost_slugs)}**")
    lines.append(f"- Changed metadata: **{len(diff.changed)}**")
    lines.append("")
    lines.append("## New repos")
    lines.append("")
    if not diff.new_repos:
        lines.append("_None._")
    else:
        lines.append("| name | visibility | pushed_at | suggested app_class |")
        lines.append("|---|---|---|---|")
        for s in diff.new_repos:
            lines.append(
                f"| `{s.name}` | {s.visibility or '?'} | {s.pushed_at or '?'} | "
                f"`{classify_default(s)}` |"
            )
    lines.append("")
    lines.append("## Ghost slugs")
    lines.append("")
    if not diff.ghost_slugs:
        lines.append("_None._")
    else:
        for slug in diff.ghost_slugs:
            lines.append(f"- `{slug}` — registry row points at a URL not in current GH org")
    lines.append("")
    lines.append("## Changed metadata")
    lines.append("")
    if not diff.changed:
        lines.append("_None._")
    else:
        for slug, deltas in diff.changed:
            cells = ", ".join(f"{k}={v!r}" for k, v in sorted(deltas.items()))
            lines.append(f"- `{slug}`: {cells}")
    lines.append("")
    return "\n".join(lines)


def write_drift_report(report: str, at: date, dry_run: bool = False) -> Path:
    """Write the rendered drift report to artifacts/inventory/repo-inventory-<date>.md."""
    out_path = INVENTORY_DIR / f"repo-inventory-{at.strftime('%Y%m%d')}.md"
    if dry_run:
        logger.info("dry-run: would write %d bytes to %s", len(report), out_path)
        return out_path
    INVENTORY_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")
    logger.info("wrote drift report: %s", out_path)
    return out_path


def update_app_class(
    csv_path: Path,
    slug: str,
    app_class: str,
    dry_run: bool = False,
) -> bool:
    """Write one cell (`app_class`) for one repo in the registry CSV.

    Validates the row via Pydantic round-trip before writing. Returns True on
    success, False if the row was not found or validation failed.
    """
    if app_class not in VALID_APP_CLASS:
        logger.error(
            "app_class %r not in %s",
            app_class,
            sorted(VALID_APP_CLASS),
        )
        return False
    if not csv_path.is_file():
        logger.error("registry CSV missing at %s", csv_path)
        return False

    with csv_path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = [dict(r) for r in reader]
        header = list(reader.fieldnames or [])
    if header != list(REPOSITORY_REGISTRY_FIELDNAMES):
        logger.error("registry CSV header drift: %s", header)
        return False

    target = None
    for r in rows:
        if (r.get("repo_slug") or "").strip() == slug:
            target = r
            break
    if target is None:
        logger.error("repo_slug %r not found in registry", slug)
        return False

    target["app_class"] = app_class
    target["last_inventory_at"] = date.today().isoformat()

    # Pydantic round-trip validation (per RepositoryRegistryRow).
    try:
        payload = {k: (v or "") for k, v in target.items() if k}
        # Coerce booleans for Pydantic when present.
        for bool_col in ("codeowners_present", "branch_protection_enabled"):
            raw = payload.get(bool_col) or ""
            if raw in ("true", "false"):
                payload[bool_col] = raw == "true"
            elif raw == "":
                payload[bool_col] = None
        # Coerce optional date fields: empty string → None for Pydantic pattern checks.
        for date_col in ("created_at", "pushed_at", "last_inventory_at"):
            if payload.get(date_col) == "":
                payload[date_col] = None
        for opt_col in ("github_visibility", "primary_language", "governance_status"):
            if payload.get(opt_col) == "":
                payload[opt_col] = None
        RepositoryRegistryRow.model_validate(payload)
    except Exception as exc:  # noqa: BLE001 — surface any Pydantic error for the operator
        logger.error("Pydantic validation failed for row %r: %s", slug, exc)
        return False

    if dry_run:
        logger.info(
            "dry-run: would set app_class=%s on slug=%s (last_inventory_at=%s)",
            app_class, slug, target["last_inventory_at"],
        )
        return True

    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=REPOSITORY_REGISTRY_FIELDNAMES)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    logger.info("wrote app_class=%s on slug=%s", app_class, slug)
    return True


def cmd_sweep(args: argparse.Namespace) -> int:
    """Subcommand entry: sweep GH inventory + write drift report."""
    snapshots = fetch_github_inventory(org=args.org, limit=args.limit)
    if not snapshots:
        logger.warning("no snapshots returned; producing empty drift report")
    rows = load_registry_rows()
    diff = diff_against_registry(snapshots, rows)
    report = render_drift_report(diff, org=args.org)
    out_path = write_drift_report(report, at=diff.at, dry_run=args.dry_run)
    print(f"  Drift report: {out_path}")
    print(f"  New repos:    {len(diff.new_repos)}")
    print(f"  Ghost slugs:  {len(diff.ghost_slugs)}")
    print(f"  Changed meta: {len(diff.changed)}")
    return 0


def cmd_classify(args: argparse.Namespace) -> int:
    """Subcommand entry: set app_class on one row."""
    ok = update_app_class(CSV_PATH, args.repo, args.app_class, dry_run=args.dry_run)
    return 0 if ok else 1


def cmd_audit(args: argparse.Namespace) -> int:
    """Subcommand entry: run validate_repository_registry.py with --strict-app-class."""
    if not VALIDATOR_SCRIPT.is_file():
        logger.error("validator script missing at %s", VALIDATOR_SCRIPT)
        return 1
    cli_args = [sys.executable, str(VALIDATOR_SCRIPT), "--strict-app-class"]
    if args.dry_run:
        logger.info("dry-run: would invoke %s", " ".join(cli_args))
        return 0
    result = run(cli_args, timeout=60)
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    return result.returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="inventory_github_repos.py",
        description=(
            "Quarterly GitHub inventory sweep + classification + audit per "
            "SOP-TECH_APPLICATION_GOVERNANCE_001 (I86 Wave H; D-IH-86-AF)."
        ),
    )
    parser.add_argument("--dry-run", action="store_true", default=False, help="No writes; print intended actions.")
    parser.add_argument("--json-log", action="store_true", default=False, help="Structured JSON logging.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sweep = sub.add_parser("sweep", help="Fetch GH inventory + diff vs registry.")
    sweep.add_argument("--org", default=DEFAULT_ORG, help=f"GitHub org (default: {DEFAULT_ORG}).")
    sweep.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help=f"Max repos to list (default: {DEFAULT_LIMIT}).")
    sweep.set_defaults(func=cmd_sweep)

    classify = sub.add_parser("classify", help="Set app_class on one row.")
    classify.add_argument("--repo", required=True, help="repo_slug to classify.")
    classify.add_argument(
        "--app-class",
        required=True,
        choices=sorted(VALID_APP_CLASS),
        help="Target app_class value.",
    )
    classify.set_defaults(func=cmd_classify)

    audit = sub.add_parser("audit", help="Run validator with --strict-app-class.")
    audit.set_defaults(func=cmd_audit)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    setup_logging(json_output=args.json_log)
    print("\n  inventory_github_repos.py")
    print("  " + "=" * 40)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
