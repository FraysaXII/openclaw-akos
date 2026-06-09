#!/usr/bin/env python3
"""Operational cohesion doctrine self-consistency runbook (I86 Wave I Lane I-B; D-IH-86-AN).

Paired SOP: docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/SOP-PMO_OPERATIONAL_COHESION_INDEX_RENDER_001.md
Paired doctrine: [`OPERATIONAL_COHESION_DOCTRINE.md`](../docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/OPERATIONAL_COHESION_DOCTRINE.md)
Catalog: docs/references/hlk/v3.0/Admin/O5-1/Operations/canonicals/OPERATIONS_PROCESS_CATALOG.yaml (operational_cohesion_index_render)
per [`akos-executable-process-catalog.mdc`](../.cursor/rules/akos-executable-process-catalog.mdc)
RULE 1 (every executable process needs a paired human-readable doctrine /
SOP + agent-facing runbook). Implements the validate-on-CI + index-emit
contract that backstops the dual-surface routing contract codified by
D-IH-86-AM + D-IH-86-AN.

process_list item_id: ``ops_pmo_dtp_cohesion_quarterly_001`` (D-IH-86-AN).
Discovered by ``scripts/validate_process_list_pairing.py`` via this script's
filename + the item_id reference in this docstring.

Subcommands:

- ``validate`` (default; load-bearing) — self-consistency check. Verifies
  every ``linked_canonicals:`` frontmatter path exists on disk, every J-*
  audience code in the doctrine body matches a row in
  ``AUDIENCE_REGISTRY.csv``, and every ``governance_rules:`` entry resolves
  under ``.cursor/rules/``. Exit 0 on clean / exit 1 on any failure.
- ``index`` (optional; v1 emits a derived stub) — writes a derived
  audience-pivoted routing-index markdown to
  ``artifacts/cohesion/index-<YYYYMMDD>.md`` for landing-page consumption.

Both subcommands accept ``--dry-run`` (no writes; prints intent) and
``--json-log`` (structured JSON logging via ``akos.log.setup_logging``).

Compliance with ``CONTRIBUTING.md`` §"Python Code Standards":
- Type hints on every function signature + return type.
- Structured logging via ``akos.log.setup_logging`` (not bare ``print()``
  for state changes; banners stay on stdout for human readability).
- Cross-platform ``pathlib.Path`` everywhere.
- Stdlib-only (no third-party deps; YAML parsing is done with the standard
  ``yaml`` package already installed under the AKOS Python environment).
"""

from __future__ import annotations

import argparse
import csv
import logging
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.log import setup_logging  # noqa: E402

DOCTRINE_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1"
    / "Operations" / "PMO" / "canonicals" / "OPERATIONAL_COHESION_DOCTRINE.md"
)
AUDIENCE_REGISTRY_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People"
    / "Compliance" / "canonicals" / "dimensions" / "AUDIENCE_REGISTRY.csv"
)
CURSOR_RULES_DIR = REPO_ROOT / ".cursor" / "rules"
COHESION_ARTIFACTS_DIR = REPO_ROOT / "artifacts" / "cohesion"

# Match audience codes like J-OP, J-IN, J-ENISA (1-6 uppercase letters).
# Word boundary on the left side prevents matching mid-token suffixes;
# negative lookahead on the right blocks tokens like J-OPERATOR that start
# with a known code but extend further.
AUDIENCE_CODE_RE = re.compile(r"\bJ-[A-Z]{2,6}\b(?![A-Z])")

logger = logging.getLogger("akos.render_operational_cohesion_index")


@dataclass(frozen=True)
class DoctrineFrontmatter:
    """Parsed frontmatter slice this runbook depends on."""

    linked_canonicals: tuple[str, ...]
    governance_rules: tuple[str, ...]


@dataclass
class ValidationReport:
    """Accumulator for validation findings."""

    missing_canonicals: list[str] = field(default_factory=list)
    unknown_audience_codes: list[str] = field(default_factory=list)
    missing_rules: list[str] = field(default_factory=list)

    @property
    def is_clean(self) -> bool:
        return (
            not self.missing_canonicals
            and not self.unknown_audience_codes
            and not self.missing_rules
        )


def parse_doctrine_frontmatter(doctrine_path: Path) -> tuple[DoctrineFrontmatter, str]:
    """Split a markdown file into its YAML frontmatter + body.

    Returns a tuple of (DoctrineFrontmatter, body_str). Raises ValueError
    when the file lacks frontmatter delimiters or when required keys are
    missing.
    """
    text = doctrine_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(
            f"{doctrine_path} does not start with YAML frontmatter (`---`)"
        )

    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError(
            f"{doctrine_path} frontmatter is not terminated by `\\n---\\n`"
        )

    fm_text = text[4:end]
    body = text[end + 5:]

    parsed = yaml.safe_load(fm_text) or {}
    if not isinstance(parsed, dict):
        raise ValueError(
            f"{doctrine_path} frontmatter did not parse to a mapping"
        )

    linked = parsed.get("linked_canonicals") or []
    rules = parsed.get("governance_rules") or []
    if not isinstance(linked, list):
        raise ValueError("`linked_canonicals` must be a YAML list")
    if not isinstance(rules, list):
        raise ValueError("`governance_rules` must be a YAML list")

    return (
        DoctrineFrontmatter(
            linked_canonicals=tuple(str(p) for p in linked),
            governance_rules=tuple(str(r) for r in rules),
        ),
        body,
    )


def extract_audience_codes(body: str) -> set[str]:
    """Return the set of unique `J-*` audience codes appearing in the body."""
    return set(AUDIENCE_CODE_RE.findall(body))


def load_audience_registry_codes(registry_path: Path) -> set[str]:
    """Return the set of `audience_code` values from AUDIENCE_REGISTRY.csv."""
    if not registry_path.exists():
        raise FileNotFoundError(
            f"AUDIENCE_REGISTRY.csv not found at {registry_path}"
        )
    codes: set[str] = set()
    with registry_path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            code = (row.get("audience_code") or "").strip()
            if code:
                codes.add(code)
    return codes


def validate_doctrine(
    doctrine_path: Path,
    registry_path: Path,
    rules_dir: Path,
) -> ValidationReport:
    """Run the three self-consistency checks codified in D-IH-86-AN."""
    frontmatter, body = parse_doctrine_frontmatter(doctrine_path)
    report = ValidationReport()

    for rel_path in frontmatter.linked_canonicals:
        abs_path = REPO_ROOT / rel_path
        if not abs_path.exists():
            report.missing_canonicals.append(rel_path)

    known_codes = load_audience_registry_codes(registry_path)
    found_codes = extract_audience_codes(body)
    for code in sorted(found_codes):
        if code not in known_codes:
            report.unknown_audience_codes.append(code)

    for rule_name in frontmatter.governance_rules:
        rule_path = rules_dir / rule_name
        if not rule_path.exists():
            report.missing_rules.append(rule_name)

    return report


def render_index(
    doctrine_path: Path,
    output_dir: Path,
    *,
    dry_run: bool,
) -> Path:
    """Emit a derived per-audience routing index stub.

    v1 emits a minimal "regenerated from <doctrine_path>" pointer; v2+ may
    parse the §4 routing matrix and pivot it per-audience. Today the
    load-bearing runbook surface is `validate`; this subcommand exists so
    the contract in §8 of the doctrine is honoured.
    """
    today = date.today().isoformat().replace("-", "")
    output_path = output_dir / f"index-{today}.md"

    stub = (
        f"# Operational cohesion index ({today})\n\n"
        f"> Regenerated from [`OPERATIONAL_COHESION_DOCTRINE.md`]"
        f"(../../docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/OPERATIONAL_COHESION_DOCTRINE.md)\n"
        f"> via `scripts/render_operational_cohesion_index.py index`.\n\n"
        f"This is a v1 stub. The load-bearing surface for cohesion governance\n"
        f"is the doctrine itself + the `validate` subcommand of this runbook.\n"
        f"Future v2 will pivot the §4 routing matrix per audience class.\n"
    )

    if dry_run:
        logger.info(
            "[dry-run] would write %d bytes to %s", len(stub), output_path
        )
        return output_path

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path.write_text(stub, encoding="utf-8")
    logger.info("wrote cohesion index stub to %s", output_path)
    return output_path


def _report_to_stdout(report: ValidationReport) -> None:
    """Pretty-print a validation report to stdout for operator review."""
    if report.is_clean:
        print("validate: PASS — operational cohesion doctrine is self-consistent.")
        return

    print("validate: FAIL — operational cohesion doctrine has drift findings:")
    if report.missing_canonicals:
        print(f"  missing linked_canonicals ({len(report.missing_canonicals)}):")
        for path in report.missing_canonicals:
            print(f"    - {path}")
    if report.unknown_audience_codes:
        print(
            f"  unknown audience codes ({len(report.unknown_audience_codes)}) "
            f"not in AUDIENCE_REGISTRY.csv:"
        )
        for code in report.unknown_audience_codes:
            print(f"    - {code}")
    if report.missing_rules:
        print(f"  missing governance_rules ({len(report.missing_rules)}):")
        for rule in report.missing_rules:
            print(f"    - {rule}")


def cmd_validate(args: argparse.Namespace) -> int:
    """Entry point for the `validate` subcommand."""
    setup_logging(json_output=args.json_log)
    logger.info("validate: parsing %s", DOCTRINE_PATH)

    if not DOCTRINE_PATH.exists():
        logger.error("doctrine canonical not found at %s", DOCTRINE_PATH)
        return 1

    try:
        report = validate_doctrine(
            DOCTRINE_PATH, AUDIENCE_REGISTRY_PATH, CURSOR_RULES_DIR
        )
    except (ValueError, FileNotFoundError) as exc:
        logger.error("validate failed: %s", exc)
        return 1

    _report_to_stdout(report)
    return 0 if report.is_clean else 1


def cmd_index(args: argparse.Namespace) -> int:
    """Entry point for the `index` subcommand."""
    setup_logging(json_output=args.json_log)
    logger.info("index: emitting cohesion index stub")

    if not DOCTRINE_PATH.exists():
        logger.error("doctrine canonical not found at %s", DOCTRINE_PATH)
        return 1

    render_index(DOCTRINE_PATH, COHESION_ARTIFACTS_DIR, dry_run=args.dry_run)
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="render_operational_cohesion_index",
        description=(
            "Operational cohesion doctrine self-consistency runbook "
            "(D-IH-86-AN). Default subcommand: validate."
        ),
    )
    subparsers = parser.add_subparsers(dest="command")

    val = subparsers.add_parser(
        "validate",
        help="Self-consistency check (linked_canonicals + J-* codes + governance_rules)",
    )
    val.add_argument("--dry-run", action="store_true", help="No-op for validate")
    val.add_argument("--json-log", action="store_true", help="Structured JSON logging")
    val.set_defaults(func=cmd_validate)

    idx = subparsers.add_parser(
        "index",
        help="Emit derived per-audience routing index (v1 stub)",
    )
    idx.add_argument("--dry-run", action="store_true", help="Print intent only")
    idx.add_argument("--json-log", action="store_true", help="Structured JSON logging")
    idx.set_defaults(func=cmd_index)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        # No subcommand → default to validate.
        args = parser.parse_args(["validate"] + (argv or []))
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
