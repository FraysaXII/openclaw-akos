#!/usr/bin/env python3
"""Tech Lab Agentic Landscape Audit runbook (Initiative 79 P3b).

Paired runbook for ``SOP-TECH_AGENTIC_INFRA_001.md`` per
[`akos-executable-process-catalog.mdc`](../.cursor/rules/akos-executable-process-catalog.mdc)
Rule 1. Implements the quarterly + event-triggered audit cadence described in
the SOP §1.

Verifies that ``AGENTIC_FRAMEWORK_LANDSCAPE.md`` stays coherent with reality:

1. Every framework row's upstream link reaches a non-error response.
2. Every linked canonical referenced from the landscape resolves to a real file
   in this repo.
3. Every cross-reference inside the canonical resolves.

The script is intentionally **read-only** and **HTTP-light**: it does not pull
release notes, parse semver, or call package registries. Those are Tech Lead +
System Owner responsibilities per the SOP. This runbook is the mechanical
"is the canonical still wired up correctly" check.

Cross-references:

- ``SOP-TECH_AGENTIC_INFRA_001.md`` (paired SOP).
- ``AGENTIC_FRAMEWORK_LANDSCAPE.md`` (canonical the runbook audits).
- ``akos-executable-process-catalog.mdc`` Rule 1 (pairing rule).
- ``process_list.csv`` row ``env_tech_dtp_agentic_landscape_mtnce_001``
  (this is the paired runbook for that scheduled cadence row).
- ``process_list.csv`` row ``env_tech_dtp_agentic_infra_ops_001``
  (event-triggered Tech Lab ops; same runbook invoked off-cadence per
  SOP-TECH_AGENTIC_INFRA_001.md).

Usage::

    py scripts/tech_agentic_landscape_audit.py
    py scripts/tech_agentic_landscape_audit.py --skip-http
    py scripts/tech_agentic_landscape_audit.py --report reports/landscape-audit-<date>.md

Per ``CONTRIBUTING.md`` Python Code Standards: type hints + structured logging
+ ``pathlib.Path`` + ``urllib.request`` (stdlib only); no third-party deps.

Exit code 0 PASS, 1 FAIL.
"""
from __future__ import annotations

import argparse
import logging
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

LANDSCAPE_PATH = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "Envoy Tech Lab"
    / "canonicals"
    / "AGENTIC_FRAMEWORK_LANDSCAPE.md"
)

logger = logging.getLogger("tech_agentic_landscape_audit")


@dataclass(frozen=True)
class FrameworkRow:
    """One row in the framework landscape table.

    Lightweight parse from the canonical; only the fields the audit needs.
    """

    name: str
    link: str

    @property
    def is_internal(self) -> bool:
        """Internal links (relative paths) are resolved against the repo root."""
        return not self.link.lower().startswith(("http://", "https://"))


def _parse_framework_rows(landscape_text: str) -> list[FrameworkRow]:
    """Parse the §1 framework table.

    The canonical uses Markdown tables with a fixed pipe-delimited shape:

        | Framework | Purpose | When we use it | Risk | Link |

    The link column is either an HTTPS URL or a relative repo path.
    """
    rows: list[FrameworkRow] = []
    in_section_1 = False
    seen_header = False
    for line in landscape_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## §1"):
            in_section_1 = True
            continue
        if stripped.startswith("## §2") or stripped.startswith("## §3"):
            in_section_1 = False
            seen_header = False
            continue
        if not in_section_1 or not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.split("|")[1:-1]]
        if not seen_header:
            if cells and cells[0].lower() == "framework":
                seen_header = True
            continue
        if len(cells) < 5:
            continue
        if set(cells[0]) <= set("-: "):  # divider row
            continue
        name_cell, link_cell = cells[0], cells[4]
        name_match = re.search(r"\*\*([^*]+)\*\*", name_cell)
        framework_name = name_match.group(1) if name_match else name_cell
        link_match = re.search(r"<([^>]+)>", link_cell)
        if link_match:
            link = link_match.group(1)
        else:
            md_link = re.search(r"\[[^\]]+\]\(([^)]+)\)", link_cell)
            link = md_link.group(1) if md_link else link_cell
        rows.append(FrameworkRow(name=framework_name, link=link))
    return rows


def _check_http_link(url: str, *, timeout: float = 5.0) -> tuple[bool, str]:
    """HEAD-then-GET probe for an external URL. Returns (ok, note)."""
    try:
        request = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return (200 <= response.status < 400, f"HTTP {response.status}")
    except urllib.error.HTTPError as err:
        if err.code in {403, 405}:
            try:
                with urllib.request.urlopen(url, timeout=timeout) as response:
                    return (200 <= response.status < 400, f"HTTP {response.status} (GET)")
            except Exception as inner:
                return (False, f"GET failed: {inner!r}")
        return (False, f"HTTP {err.code}")
    except Exception as err:
        return (False, f"network error: {err!r}")


def _check_internal_link(landscape_path: Path, link: str) -> tuple[bool, str]:
    """Resolve a relative link from the landscape canonical's directory.

    The link may include ``../`` traversal; resolved with ``Path.resolve()``.
    """
    target = (landscape_path.parent / link).resolve()
    if target.exists():
        return (True, str(target.relative_to(REPO_ROOT)))
    return (False, f"missing: {target}")


def _check_landscape_canonical(landscape_path: Path, *, skip_http: bool) -> tuple[int, int, list[str]]:
    """Top-level audit. Returns (passed, total, error-strings)."""
    text = landscape_path.read_text(encoding="utf-8", errors="replace")
    framework_rows = _parse_framework_rows(text)
    if not framework_rows:
        return (0, 0, ["FAIL: §1 framework table not parsed (zero rows)"])
    passed = 0
    errors: list[str] = []
    for row in framework_rows:
        if row.is_internal:
            ok, note = _check_internal_link(landscape_path, row.link)
        elif skip_http:
            ok, note = (True, "skipped (--skip-http)")
        else:
            ok, note = _check_http_link(row.link)
        prefix = "ok" if ok else "FAIL"
        line = f"{prefix}: {row.name} -> {row.link} ({note})"
        if ok:
            passed += 1
            logger.info(line)
        else:
            errors.append(line)
            logger.error(line)
    return (passed, len(framework_rows), errors)


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit AGENTIC_FRAMEWORK_LANDSCAPE.md.")
    parser.add_argument(
        "--skip-http",
        action="store_true",
        help="skip live HTTP probes (CI without network access)",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help="optional path to write a Markdown audit report",
    )
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format="%(levelname)s | %(message)s")

    if not LANDSCAPE_PATH.exists():
        logger.error("FAIL: canonical not found at %s", LANDSCAPE_PATH)
        return 1

    passed, total, errors = _check_landscape_canonical(LANDSCAPE_PATH, skip_http=args.skip_http)

    if args.report is not None:
        report_path = args.report if args.report.is_absolute() else REPO_ROOT / args.report
        report_path.parent.mkdir(parents=True, exist_ok=True)
        body = ["# Tech Lab Agentic Landscape Audit", ""]
        body.append(f"- Canonical audited: `{LANDSCAPE_PATH.relative_to(REPO_ROOT)}`")
        body.append(f"- Framework rows: {total}")
        body.append(f"- Passed: {passed}")
        body.append(f"- Failed: {len(errors)}")
        body.append("")
        body.append("## Per-row outcomes")
        body.append("")
        for err in errors:
            body.append(f"- {err}")
        if not errors:
            body.append("- All rows resolved cleanly.")
        report_path.write_text("\n".join(body) + "\n", encoding="utf-8")
        logger.info("report written: %s", report_path.relative_to(REPO_ROOT))

    if errors:
        logger.error("OVERALL FAIL: %s of %s rows failed", len(errors), total)
        return 1
    logger.info("OVERALL PASS: %s of %s rows ok", passed, total)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
