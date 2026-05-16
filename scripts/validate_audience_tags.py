"""Validate ``audience:`` YAML frontmatter against AUDIENCE_REGISTRY.csv (I85 P2).

Per **D-IH-85-A** (FK index pattern) + **D-IH-85-B** (YAML list multi-audience
encoding) + **D-IH-85-D** (J-OP exclusion — operator-only audience cannot be
composed with external audiences in the same surface's ``audience:`` list).

Scope (this validator):

1. Scan every markdown file under repo for YAML frontmatter containing
   ``audience:``.
2. For each file with an ``audience:`` field, parse the value (either a YAML
   list or a single string).
3. FK-validate each ``J-*`` code against ``AUDIENCE_REGISTRY.csv``
   ``audience_code`` column. Unknown codes are reported as **error**.
4. Enforce **J-OP exclusion** (D-IH-85-D): if J-OP appears alongside any other
   J-* code in the same list, report **error** — J-OP is operator-only and is
   exclusionary by design.
5. Recognise both ``audience: J-IN`` (single) and ``audience: [J-IN, J-CU]``
   (list) syntax.

Scope (NOT this validator):

- This validator does NOT enforce that every external surface CARRIES an
  ``audience:`` tag. That sweep is gated by D-IH-85-C operator-tranche
  approval and lands in I85 P4 (SOP promotion) after operator ratification of
  the surface-class tranches.
- This validator is wired into ``release-gate.py`` as INFO row (advisory
  only; never blocks) until the sweep completes; promotes to PASS/FAIL at
  I85 P4 closure per the master-roadmap.

Exit code: 0 PASS, 1 FAIL.
"""
from __future__ import annotations

import csv
import logging
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos import log  # noqa: E402

log.setup_logging()
logger = logging.getLogger(__name__)

REGISTRY_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1"
    / "People" / "Compliance" / "canonicals" / "dimensions"
    / "AUDIENCE_REGISTRY.csv"
)

SCAN_GLOBS: tuple[str, ...] = (
    "BASELINE_REALITY.md",
    "PRODUCT.md",
    "DESIGN.md",
    "docs/references/hlk/v3.0/_assets/advops/**/*.md",
    "docs/references/hlk/v3.0/_assets/touchpoint_kits/**/*.md",
    "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/**/*.md",
)

SKIP_PATTERNS: tuple[re.Pattern, ...] = (
    re.compile(r"\.objections\.md$"),
    re.compile(r"\.counterparty-brief\.md$"),
    re.compile(r"^_template"),
    re.compile(r"/templates?/"),
    re.compile(r"/_candidates/"),
)

FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
AUDIENCE_FIELD_PATTERN = re.compile(
    r"^audience\s*:\s*(.+?)$",
    re.MULTILINE,
)
AUDIENCE_LIST_INLINE = re.compile(r"^\s*\[(.+?)\]\s*$")
AUDIENCE_CODE_PATTERN = re.compile(r"J-[A-Z]{2,8}")


def _load_valid_audience_codes() -> tuple[set[str], dict[str, str]]:
    """Return (valid_codes, code_to_register_side_map) from AUDIENCE_REGISTRY.csv."""
    codes: set[str] = set()
    register_sides: dict[str, str] = {}
    if not REGISTRY_PATH.exists():
        logger.error("AUDIENCE_REGISTRY.csv missing at %s", REGISTRY_PATH)
        return codes, register_sides
    with REGISTRY_PATH.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            code = (row.get("audience_code") or "").strip()
            if code:
                codes.add(code)
                register_sides[code] = (row.get("register_side") or "").strip()
    return codes, register_sides


def _should_skip(path: Path) -> bool:
    rel = path.as_posix()
    return any(pattern.search(rel) for pattern in SKIP_PATTERNS)


def _extract_frontmatter_audience(text: str) -> list[str] | None:
    """Return list of audience codes from file frontmatter, or None if no audience field."""
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        return None
    frontmatter = match.group(1)
    audience_match = AUDIENCE_FIELD_PATTERN.search(frontmatter)
    if not audience_match:
        return None
    raw_value = audience_match.group(1).strip()
    list_match = AUDIENCE_LIST_INLINE.match(raw_value)
    if list_match:
        codes = [c.strip() for c in list_match.group(1).split(",")]
        return [c for c in codes if c]
    if raw_value.startswith("J-"):
        return [raw_value.split()[0]]
    return AUDIENCE_CODE_PATTERN.findall(raw_value) or None


def _iter_target_files() -> list[Path]:
    files: list[Path] = []
    for glob_pattern in SCAN_GLOBS:
        for path in REPO_ROOT.glob(glob_pattern):
            if path.is_file() and path.suffix == ".md" and not _should_skip(path):
                files.append(path)
    seen: set[Path] = set()
    deduped: list[Path] = []
    for path in files:
        if path not in seen:
            deduped.append(path)
            seen.add(path)
    return deduped


def validate() -> int:
    valid_codes, _register_sides = _load_valid_audience_codes()
    if not valid_codes:
        logger.error("FAIL: AUDIENCE_REGISTRY.csv empty or unreadable")
        return 1

    errors: list[str] = []
    files_scanned = 0
    files_with_audience = 0

    for path in _iter_target_files():
        files_scanned += 1
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            logger.warning("skip unreadable %s: %s", path.relative_to(REPO_ROOT), exc)
            continue

        audience_codes = _extract_frontmatter_audience(text)
        if audience_codes is None:
            continue

        files_with_audience += 1
        rel_path = path.relative_to(REPO_ROOT).as_posix()

        for code in audience_codes:
            if code not in valid_codes:
                errors.append(
                    f"{rel_path}: unknown audience code '{code}' "
                    f"(not in AUDIENCE_REGISTRY.csv)"
                )

        if "J-OP" in audience_codes and len(audience_codes) > 1:
            external_codes = [c for c in audience_codes if c != "J-OP"]
            errors.append(
                f"{rel_path}: J-OP exclusion violated — J-OP composed with "
                f"{external_codes} (D-IH-85-D: J-OP is operator-only and "
                f"exclusionary)"
            )

    if errors:
        for error in errors:
            logger.error("%s", error)
        logger.error(
            "FAIL: validate_audience_tags — %d error(s); scanned %d file(s); "
            "%d carried audience: frontmatter",
            len(errors),
            files_scanned,
            files_with_audience,
        )
        return 1

    logger.info(
        "PASS: validate_audience_tags — scanned %d file(s); %d carried "
        "audience: frontmatter; all FK-resolved + J-OP exclusion clean",
        files_scanned,
        files_with_audience,
    )
    return 0


def main() -> int:
    return validate()


if __name__ == "__main__":
    sys.exit(main())
