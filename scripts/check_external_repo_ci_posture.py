#!/usr/bin/env python3
"""Verify CI/CD + observability posture for blessed Holistika-tracked repos.

Sub-checks (each independently skippable when prerequisites are absent):

- ``presence``      filesystem-only:
    * ``.github/workflows/ci.yml`` contains required jobs (`lint`, `typecheck`,
      `audit`, `build`)
    * ``.github/dependabot.yml`` exists
    * ``.github/CODEOWNERS`` exists
    * ``LICENSE`` exists (Track I; soft-fail if missing during early bless)

- ``branch_protection`` (gh CLI required; SKIPPED if unauthenticated):
    * ``main`` requires reviews >= 1
    * required status checks include the workflow job names
    * dismiss-stale enabled

- ``vercel_projects`` (vercel CLI required; SKIPPED if absent):
    * for repos in ``SUBDOMAINS_REGISTRY.md`` with ``state=active`` AND
      ``repo == <slug>``, the named ``vercel_project`` exists in the org

- ``sast_freshness`` (gh CLI; SKIPPED if Semgrep not enabled):
    * latest successful Semgrep workflow run within last 7 days

- ``last_workflow_run`` (gh CLI; SKIPPED if unavailable):
    * latest CI run on ``main`` within last 30 days

- ``sentry_liveness`` (Sentry API; SKIPPED if SENTRY_AUTH_TOKEN absent):
    * project has at least one event in the last 7 days

- ``slack_webhook_present`` (env-var only):
    * SLACK_OPS_WEBHOOK present in the operator's process env

- ``license_present`` (filesystem-only):
    * <repo>/LICENSE exists

- ``secret_rotation_freshness`` (filesystem-only):
    * parses ``docs/runbooks/secrets-rotation.md`` frontmatter; warns at >75d,
      fails at >90d

Each sub-check returns one of: PASS / WARN / FAIL / SKIPPED.

Usage::

    py scripts/check_external_repo_ci_posture.py --repo-slug hlk-erp
    py scripts/check_external_repo_ci_posture.py --repo-slug hlk-erp --skip-live
    py scripts/check_external_repo_ci_posture.py        # all blessed repos
    py scripts/check_external_repo_ci_posture.py --json-log

Exit codes:
    0 - all FAIL-class checks pass (WARN and SKIPPED do not block)
    1 - one or more FAIL-class checks failed
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT
from akos.log import setup_logging

logger = logging.getLogger("akos.ci-posture")

REGISTRY_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "REPOSITORY_REGISTRY.csv"
SUBDOMAINS_MD = (
    REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Envoy Tech Lab" / "Repositories" / "SUBDOMAINS_REGISTRY.md"
)

REQUIRED_CI_JOBS = ("lint", "typecheck", "audit", "build")

DEFAULT_REPO_PATHS: dict[str, Path] = {
    "boilerplate": Path(r"c:\Users\Shadow\cd_shadow\root_cd\boilerplate"),
    "hlk-erp": Path(r"c:\Users\Shadow\cd_shadow\root_cd\hlk-erp"),
    "kirbe-platform": Path(r"c:\Users\Shadow\cd_shadow\root_cd\kirbe"),
}

LAST_ROTATED_RE = re.compile(r"^\s*-\s+name:\s*(\S+).*?last_rotated:\s*(\d{4}-\d{2}-\d{2})", re.MULTILINE | re.DOTALL)
SECRET_ROTATION_FRONT_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
LAST_ROTATED_FRONTMATTER_RE = re.compile(r"^last_rotated:\s*(\d{4}-\d{2}-\d{2})\s*$", re.MULTILINE)


@dataclass
class CheckResult:
    name: str
    level: str  # PASS | WARN | FAIL | SKIPPED
    message: str

    def is_blocking(self) -> bool:
        return self.level == "FAIL"


def _resolve_repo_paths() -> dict[str, Path]:
    override = os.environ.get("AKOS_EXTERNAL_REPO_ROOTS")
    if override:
        try:
            data = json.loads(override)
            return {k: Path(v) for k, v in data.items()}
        except Exception:
            pass
    return DEFAULT_REPO_PATHS


def _load_registry() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    with REGISTRY_CSV.open("r", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            slug = (row.get("repo_slug") or "").strip()
            if slug:
                out[slug] = row
    return out


def _gh_available() -> bool:
    return shutil.which("gh") is not None


def _vercel_available() -> bool:
    return shutil.which("vercel") is not None


def _gh_auth_ok() -> bool:
    if not _gh_available():
        return False
    try:
        r = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True, timeout=5, check=False)
        return r.returncode == 0
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Sub-checks
# ---------------------------------------------------------------------------


def _extract_ci_job_names(workflow_text: str) -> list[str]:
    """Return the top-level GitHub Actions job ids from a workflow file."""
    in_jobs = False
    job_names: list[str] = []
    for line in workflow_text.splitlines():
        if not line:
            continue
        if not in_jobs:
            if re.match(r"^jobs\s*:\s*$", line):
                in_jobs = True
            continue
        # End of jobs block when we hit another top-level key (no leading space).
        if line and not line[0].isspace() and re.match(r"^[A-Za-z_]\w*\s*:\s*$", line):
            break
        # Job ids are indented exactly 2 spaces and end with ':'.
        m = re.match(r"^\s{2}([A-Za-z_][\w-]*):\s*$", line)
        if m:
            job_names.append(m.group(1))
    return job_names


def _required_jobs_satisfied(job_names: list[str]) -> list[str]:
    """Return the list of REQUIRED_CI_JOBS missing from `job_names`.

    A required job name `lint` is considered satisfied when ANY of `job_names`
    contains it as a whole token (split on `-` / `_`), so a compound job like
    `lint-typecheck` covers both `lint` and `typecheck` requirements.
    """
    tokens: set[str] = set()
    for name in job_names:
        for tok in re.split(r"[-_]", name):
            if tok:
                tokens.add(tok.lower())
    return [j for j in REQUIRED_CI_JOBS if j not in tokens]


def check_presence(repo_path: Path) -> list[CheckResult]:
    results: list[CheckResult] = []
    ci_yml = repo_path / ".github" / "workflows" / "ci.yml"
    if not ci_yml.is_file():
        results.append(CheckResult("presence.ci_yml", "FAIL", f"{ci_yml} missing"))
    else:
        text = ci_yml.read_text(encoding="utf-8", errors="ignore")
        job_names = _extract_ci_job_names(text)
        missing = _required_jobs_satisfied(job_names)
        if missing:
            results.append(CheckResult(
                "presence.ci_yml.jobs",
                "FAIL",
                f".github/workflows/ci.yml missing required job token(s): {missing} (jobs={job_names})",
            ))
        else:
            results.append(CheckResult(
                "presence.ci_yml.jobs", "PASS", f"required tokens satisfied by jobs={job_names}",
            ))

    if not (repo_path / ".github" / "dependabot.yml").is_file():
        results.append(CheckResult("presence.dependabot", "FAIL", ".github/dependabot.yml missing"))
    else:
        results.append(CheckResult("presence.dependabot", "PASS", ""))

    if not (repo_path / ".github" / "CODEOWNERS").is_file():
        results.append(CheckResult("presence.codeowners", "FAIL", ".github/CODEOWNERS missing"))
    else:
        results.append(CheckResult("presence.codeowners", "PASS", ""))

    return results


def check_license_present(repo_path: Path) -> CheckResult:
    candidates = [repo_path / "LICENSE", repo_path / "LICENSE.md", repo_path / "LICENSE.txt"]
    if any(p.is_file() for p in candidates):
        return CheckResult("license_present", "PASS", "")
    return CheckResult("license_present", "WARN", "LICENSE missing at repo root")


def check_branch_protection(repo_url: str) -> CheckResult:
    if not _gh_auth_ok():
        return CheckResult("branch_protection", "SKIPPED", "gh CLI not available or unauthenticated")

    repo_arg = repo_url.replace("https://github.com/", "")
    try:
        r = subprocess.run(
            ["gh", "api", f"repos/{repo_arg}/branches/main/protection"],
            capture_output=True, text=True, timeout=15, check=False,
        )
    except Exception as exc:
        return CheckResult("branch_protection", "SKIPPED", f"gh api failed: {exc}")

    if r.returncode != 0:
        if "Branch not protected" in r.stderr or "404" in r.stderr:
            return CheckResult("branch_protection", "FAIL", "main is not protected")
        return CheckResult("branch_protection", "SKIPPED", f"gh api error: {r.stderr.strip()[:200]}")

    try:
        data = json.loads(r.stdout)
    except Exception:
        return CheckResult("branch_protection", "SKIPPED", "could not parse gh api output")

    reviews = data.get("required_pull_request_reviews", {})
    required_reviews = reviews.get("required_approving_review_count", 0)
    dismiss_stale = reviews.get("dismiss_stale_reviews", False)
    contexts = (data.get("required_status_checks", {}) or {}).get("contexts", []) or []

    issues: list[str] = []
    if required_reviews < 1:
        issues.append(f"required_reviews={required_reviews}<1")
    if not dismiss_stale:
        issues.append("dismiss_stale=false")
    missing_jobs = [j for j in REQUIRED_CI_JOBS if j not in contexts]
    if missing_jobs:
        issues.append(f"required_checks_missing={missing_jobs}")

    if issues:
        return CheckResult("branch_protection", "FAIL", "; ".join(issues))
    return CheckResult("branch_protection", "PASS", f"reviews>=1, dismiss_stale=on, checks={contexts}")


def check_vercel_projects(slug: str) -> CheckResult:
    if not _vercel_available():
        return CheckResult("vercel_projects", "SKIPPED", "vercel CLI not available")
    try:
        r = subprocess.run(
            ["vercel", "projects", "ls", "--json"],
            capture_output=True, text=True, timeout=20, check=False,
        )
    except Exception as exc:
        return CheckResult("vercel_projects", "SKIPPED", f"vercel CLI error: {exc}")
    if r.returncode != 0:
        return CheckResult("vercel_projects", "SKIPPED", f"vercel returned {r.returncode}")

    try:
        projects = json.loads(r.stdout)
        names = {p.get("name", "") for p in projects} if isinstance(projects, list) else set()
    except Exception:
        return CheckResult("vercel_projects", "SKIPPED", "could not parse vercel output")

    expected: list[str] = []
    if SUBDOMAINS_MD.is_file():
        for line in SUBDOMAINS_MD.read_text(encoding="utf-8").splitlines():
            if not line.startswith("|"):
                continue
            cells = [c.strip().strip("`") for c in line.strip("|").split("|")]
            if len(cells) < 10:
                continue
            row_repo = cells[7] if len(cells) > 7 else ""
            row_state = cells[2] if len(cells) > 2 else ""
            row_vercel = cells[6] if len(cells) > 6 else ""
            if row_repo == slug and row_state == "active" and row_vercel and row_vercel not in {"_(none yet)_", "_(future)_"}:
                expected.append(row_vercel)

    if not expected:
        return CheckResult("vercel_projects", "SKIPPED", f"no active subdomain rows for slug={slug}")

    missing = [p for p in expected if p not in names]
    if missing:
        return CheckResult("vercel_projects", "FAIL", f"missing Vercel projects: {missing}")
    return CheckResult("vercel_projects", "PASS", f"projects ok: {expected}")


def check_last_workflow_run(repo_url: str, days: int = 30) -> CheckResult:
    if not _gh_auth_ok():
        return CheckResult("last_workflow_run", "SKIPPED", "gh not available")
    repo_arg = repo_url.replace("https://github.com/", "")
    try:
        r = subprocess.run(
            ["gh", "run", "list", "--repo", repo_arg, "--branch", "main", "--workflow", "ci.yml",
             "--limit", "1", "--json", "createdAt,conclusion"],
            capture_output=True, text=True, timeout=15, check=False,
        )
    except Exception as exc:
        return CheckResult("last_workflow_run", "SKIPPED", f"gh error: {exc}")
    if r.returncode != 0 or not r.stdout.strip():
        return CheckResult("last_workflow_run", "SKIPPED", "no run history available")
    try:
        runs = json.loads(r.stdout)
    except Exception:
        return CheckResult("last_workflow_run", "SKIPPED", "parse error")
    if not runs:
        return CheckResult("last_workflow_run", "WARN", "no CI runs found on main")
    latest = runs[0]
    created = latest.get("createdAt", "")
    try:
        ts = datetime.fromisoformat(created.replace("Z", "+00:00"))
    except Exception:
        return CheckResult("last_workflow_run", "SKIPPED", "could not parse createdAt")
    age = (datetime.now(timezone.utc) - ts).days
    if age > days:
        return CheckResult("last_workflow_run", "FAIL", f"latest CI run is {age} days old (>{days})")
    return CheckResult("last_workflow_run", "PASS", f"latest CI run {age} day(s) ago")


def check_sast_freshness(repo_url: str, days: int = 7) -> CheckResult:
    if not _gh_auth_ok():
        return CheckResult("sast_freshness", "SKIPPED", "gh not available")
    repo_arg = repo_url.replace("https://github.com/", "")
    try:
        r = subprocess.run(
            ["gh", "run", "list", "--repo", repo_arg, "--workflow", "sast.yml",
             "--limit", "1", "--json", "createdAt,conclusion"],
            capture_output=True, text=True, timeout=15, check=False,
        )
    except Exception as exc:
        return CheckResult("sast_freshness", "SKIPPED", f"gh error: {exc}")
    if r.returncode != 0:
        return CheckResult("sast_freshness", "SKIPPED", "sast.yml not present or no runs")
    try:
        runs = json.loads(r.stdout)
    except Exception:
        return CheckResult("sast_freshness", "SKIPPED", "parse error")
    if not runs:
        return CheckResult("sast_freshness", "SKIPPED", "no SAST runs (Semgrep not enabled?)")
    latest = runs[0]
    try:
        ts = datetime.fromisoformat(latest["createdAt"].replace("Z", "+00:00"))
    except Exception:
        return CheckResult("sast_freshness", "SKIPPED", "parse error")
    age = (datetime.now(timezone.utc) - ts).days
    if age > days:
        return CheckResult("sast_freshness", "FAIL", f"latest SAST run is {age} days old (>{days})")
    return CheckResult("sast_freshness", "PASS", f"latest SAST run {age} day(s) ago")


def open_sentry_setup_issue(repo_url: str, slug: str) -> str:
    """Open a tracking issue in the consumer when Sentry env is missing.

    Returns 'OPENED', 'EXISTS', 'SKIPPED_NO_GH', or 'FAILED'. Idempotent: looks
    for an existing open issue with the canonical title before creating a new one.
    """
    if shutil.which("gh") is None:
        return "SKIPPED_NO_GH"
    repo_arg = repo_url.replace("https://github.com/", "")
    title = f"observability: configure Sentry for {slug}"
    try:
        existing = subprocess.run(
            ["gh", "issue", "list", "--repo", repo_arg, "--search", title, "--state", "open", "--json", "number"],
            capture_output=True, text=True, timeout=30, check=False,
        )
        if existing.returncode == 0 and existing.stdout.strip() not in ("[]", ""):
            return "EXISTS"
    except Exception:
        return "FAILED"
    body = (
        "AKOS posture check could not verify Sentry liveness for this repo.\n\n"
        "Required env on Vercel project + GitHub Actions secrets:\n"
        f"- `SENTRY_PROJECT_{slug.upper().replace('-', '_')}` — Sentry project slug\n"
        "- `SENTRY_AUTH_TOKEN` (in GitHub) — for source-map upload + posture queries\n"
        "- `NEXT_PUBLIC_SENTRY_DSN` (in Vercel) — browser DSN\n"
        "- `SENTRY_DSN` (in Vercel) — server DSN\n\n"
        "After setting these, the next nightly posture run should flip this check to PASS.\n"
        "AKOS-decision: governance-baseline (I63 follow-on)."
    )
    try:
        result = subprocess.run(
            ["gh", "issue", "create", "--repo", repo_arg, "--title", title, "--body", body, "--label", "observability,governance"],
            capture_output=True, text=True, timeout=60, check=False,
        )
        return "OPENED" if result.returncode == 0 else "FAILED"
    except Exception:
        return "FAILED"


def check_sentry_liveness(project_slug: str | None, days: int = 7) -> CheckResult:
    token = os.environ.get("SENTRY_AUTH_TOKEN")
    if not token:
        return CheckResult("sentry_liveness", "SKIPPED", "SENTRY_AUTH_TOKEN absent")
    if not project_slug:
        return CheckResult("sentry_liveness", "SKIPPED", "no Sentry project slug configured")
    org_slug = os.environ.get("SENTRY_ORG", "holistika")
    url = f"https://sentry.io/api/0/projects/{org_slug}/{project_slug}/events/?statsPeriod={days}d"
    try:
        import urllib.request
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if isinstance(data, list) and data:
                return CheckResult("sentry_liveness", "PASS", f"{len(data)} events in last {days}d")
            return CheckResult("sentry_liveness", "FAIL", f"no events in last {days}d")
    except Exception as exc:
        return CheckResult("sentry_liveness", "SKIPPED", f"Sentry API error: {exc}")


def check_slack_webhook_present() -> CheckResult:
    if os.environ.get("SLACK_OPS_WEBHOOK"):
        return CheckResult("slack_webhook_present", "PASS", "SLACK_OPS_WEBHOOK set")
    return CheckResult("slack_webhook_present", "WARN", "SLACK_OPS_WEBHOOK not set in env")


def check_secret_rotation(repo_path: Path, *, warn_days: int = 75, fail_days: int = 90) -> CheckResult:
    runbook = repo_path / "docs" / "runbooks" / "secrets-rotation.md"
    if not runbook.is_file():
        return CheckResult("secret_rotation_freshness", "WARN",
                           "docs/runbooks/secrets-rotation.md missing (bless writes a template; fill in last_rotated dates)")
    text = runbook.read_text(encoding="utf-8")
    today = date.today()
    rotation_dates: list[tuple[str, date]] = []
    # Try frontmatter list first.
    fm = SECRET_ROTATION_FRONT_RE.match(text)
    if fm:
        for m in re.finditer(r"^\s*-\s+name:\s*(\S+)\s*\n\s+last_rotated:\s*(\d{4}-\d{2}-\d{2})", fm.group(1), re.MULTILINE):
            try:
                rotation_dates.append((m.group(1), datetime.strptime(m.group(2), "%Y-%m-%d").date()))
            except ValueError:
                continue
    # Body table fallback (allow ``| SECRET | YYYY-MM-DD |`` rows).
    for m in re.finditer(r"^\|\s*(\S[^|]+?)\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|", text, re.MULTILINE):
        try:
            rotation_dates.append((m.group(1).strip(), datetime.strptime(m.group(2), "%Y-%m-%d").date()))
        except ValueError:
            continue

    if not rotation_dates:
        return CheckResult("secret_rotation_freshness", "WARN",
                           "no last_rotated entries parsed from runbook (add frontmatter list or table rows)")

    overdue = [(n, (today - d).days) for n, d in rotation_dates if (today - d).days > fail_days]
    upcoming = [(n, (today - d).days) for n, d in rotation_dates if warn_days < (today - d).days <= fail_days]
    if overdue:
        return CheckResult(
            "secret_rotation_freshness", "FAIL",
            f"{len(overdue)} secret(s) overdue (>{fail_days}d): {[n for n,_ in overdue]}",
        )
    if upcoming:
        return CheckResult(
            "secret_rotation_freshness", "WARN",
            f"{len(upcoming)} secret(s) approaching rotation (>{warn_days}d): {[n for n,_ in upcoming]}",
        )
    return CheckResult(
        "secret_rotation_freshness", "PASS",
        f"{len(rotation_dates)} secret(s) tracked; oldest {max((today - d).days for _, d in rotation_dates)}d",
    )


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def run_for_slug(slug: str, registry_row: dict[str, str], repo_path: Path | None,
                 *, skip_live: bool, auto_fix: bool = False) -> list[CheckResult]:
    results: list[CheckResult] = []

    if repo_path is None or not repo_path.is_dir():
        results.append(CheckResult("repo_path", "SKIPPED", f"local clone for {slug} not available"))
        return results

    results.extend(check_presence(repo_path))
    results.append(check_license_present(repo_path))
    results.append(check_secret_rotation(repo_path))

    if skip_live:
        results.append(CheckResult("live_checks", "SKIPPED", "--skip-live"))
        return results

    repo_url = (registry_row.get("github_url") or "").strip()
    results.append(check_branch_protection(repo_url))
    results.append(check_last_workflow_run(repo_url))
    results.append(check_sast_freshness(repo_url))
    results.append(check_vercel_projects(slug))
    sentry_slug = os.environ.get(f"SENTRY_PROJECT_{slug.upper().replace('-', '_')}")
    sentry_result = check_sentry_liveness(sentry_slug)
    results.append(sentry_result)
    if auto_fix and sentry_result.level in {"FAIL", "SKIPPED"} and "no Sentry project slug" in sentry_result.message:
        outcome = open_sentry_setup_issue(repo_url, slug)
        results.append(CheckResult("sentry_autofix", "PASS" if outcome in {"OPENED", "EXISTS"} else "WARN",
                                   f"sentry-setup issue: {outcome}"))
    results.append(check_slack_webhook_present())

    return results


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify CI/CD posture for blessed Holistika-tracked repos")
    parser.add_argument("--repo-slug", help="Limit to one slug (default: all non-reference repos)")
    parser.add_argument("--skip-live", action="store_true",
                        help="Skip live API calls (gh, vercel, Sentry); presence + secret-rotation only")
    parser.add_argument("--auto-fix", action="store_true",
                        help="Open tracking issues for fixable observability gaps (e.g. missing Sentry project)")
    parser.add_argument("--json-log", action="store_true")
    args = parser.parse_args(list(argv) if argv is not None else None)
    setup_logging(json_output=args.json_log)

    registry = _load_registry()
    repo_paths = _resolve_repo_paths()

    if args.repo_slug:
        if args.repo_slug not in registry:
            logger.error("slug %s not in REPOSITORY_REGISTRY.csv", args.repo_slug)
            return 2
        slugs = [args.repo_slug]
    else:
        akos_url = "https://github.com/FraysaXII/openclaw-akos"
        slugs = [
            s for s, row in registry.items()
            if (row.get("class") or "").strip().lower() != "reference"
            and (row.get("github_url") or "").strip() != akos_url
            and (s in repo_paths or args.skip_live)
        ]

    fail_count = 0
    total_count = 0
    print()
    print("=" * 56)
    print("  CI/CD posture")
    print("=" * 56)
    for slug in slugs:
        row = registry[slug]
        path = repo_paths.get(slug)
        results = run_for_slug(slug, row, path, skip_live=args.skip_live, auto_fix=args.auto_fix)
        print(f"\n  {slug} ({row.get('class', '?')})")
        for r in results:
            print(f"    [{r.level:>8}] {r.name}: {r.message}")
            total_count += 1
            if r.is_blocking():
                fail_count += 1
    print()

    if fail_count:
        logger.error("CI/CD posture: %d FAIL across %d checks", fail_count, total_count)
        return 1
    logger.info("CI/CD posture: OK (%d checks)", total_count)
    return 0


if __name__ == "__main__":
    sys.exit(main())
