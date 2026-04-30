"""Tests for the Initiative 29 P2 ``FIGMA_FILES_REGISTRY.md`` registry.

Covers:
- The registry file exists at the canonical location.
- The registry table has the expected columns.
- Every row's ``figma_url`` matches the Figma design URL pattern.
- Every row's ``topic_ids`` (semicolon-separated) resolves into ``TOPIC_REGISTRY.csv``.
- Every row's ``linked_yaml_ssot`` (when not ``-``) resolves to a real file in the repo.
- The class column uses one of the canonical values.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY = (
    REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Envoy Tech Lab"
    / "Repositories" / "FIGMA_FILES_REGISTRY.md"
)
TOPIC_REGISTRY = (
    REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "TOPIC_REGISTRY.csv"
)

EXPECTED_COLUMNS = (
    "file_slug", "figma_url", "team_key", "class",
    "primary_owner_role", "topic_ids", "linked_yaml_ssot", "notes",
)
ALLOWED_CLASSES = {"deck", "design-system", "prototype", "library"}

FIGMA_URL_RE = re.compile(r"^https://www\.figma\.com/design/[A-Za-z0-9]+(?:/[^|]*)?$")
TBD_URL_RE = re.compile(r"^https://www\.figma\.com/design/<TBD>$")  # reserved-slot pattern

# Markdown table row pattern: pipe-delimited cells.
TABLE_ROW_RE = re.compile(r"^\|\s*([^|]+?)\s*\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*`?([^|]+?)`?\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$", re.MULTILINE)


def _load_topic_ids() -> set[str]:
    with TOPIC_REGISTRY.open(encoding="utf-8", newline="") as fh:
        return {row["topic_id"].strip() for row in csv.DictReader(fh) if row.get("topic_id")}


def _parse_registry_rows(text: str) -> list[dict[str, str]]:
    """Parse the markdown table rows. Returns one dict per data row."""
    lines = text.splitlines()
    in_table = False
    header_seen = False
    rows: list[dict[str, str]] = []
    cols: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|") and "file_slug" in stripped.lower():
            cols = [c.strip() for c in stripped.strip("|").split("|")]
            in_table = True
            header_seen = True
            continue
        if header_seen and re.match(r"^\|[\s\-|]+\|$", stripped):
            continue  # header separator
        if in_table:
            if not stripped.startswith("|"):
                in_table = False
                continue
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if len(cells) == len(cols):
                rows.append(dict(zip(cols, cells)))
    return rows


def test_registry_exists():
    assert REGISTRY.is_file(), f"missing {REGISTRY}"


def test_registry_columns():
    text = REGISTRY.read_text(encoding="utf-8")
    rows = _parse_registry_rows(text)
    assert rows, "no data rows in registry"
    for col in EXPECTED_COLUMNS:
        assert col in rows[0], (
            f"registry missing column {col!r}; got columns: {list(rows[0].keys())}"
        )


def test_registry_has_at_least_one_real_row():
    text = REGISTRY.read_text(encoding="utf-8")
    rows = _parse_registry_rows(text)
    real = [r for r in rows if "TBD" not in r.get("figma_url", "")]
    assert real, "registry must carry at least one non-TBD figma file row"


def test_registry_figma_url_format():
    text = REGISTRY.read_text(encoding="utf-8")
    rows = _parse_registry_rows(text)
    for r in rows:
        url = r["figma_url"].strip("`").strip()
        # Allow TBD placeholder for reserved slots.
        if TBD_URL_RE.match(url):
            continue
        assert FIGMA_URL_RE.match(url), (
            f"row {r.get('file_slug', '<unknown>')}: invalid figma_url {url!r}"
        )


def test_registry_class_in_allowed_set():
    text = REGISTRY.read_text(encoding="utf-8")
    rows = _parse_registry_rows(text)
    for r in rows:
        cls = r["class"].strip()
        assert cls in ALLOWED_CLASSES, (
            f"row {r.get('file_slug', '<unknown>')}: class {cls!r} not in {ALLOWED_CLASSES}"
        )


def test_registry_topic_ids_resolve_against_topic_registry():
    text = REGISTRY.read_text(encoding="utf-8")
    rows = _parse_registry_rows(text)
    canonical = _load_topic_ids()
    for r in rows:
        topic_field = r["topic_ids"].strip()
        # Topic field uses backticks around individual ids.
        for raw in re.findall(r"`([a-z0-9_]+)`", topic_field):
            assert raw in canonical, (
                f"row {r.get('file_slug', '<unknown>')}: topic_id {raw!r} "
                f"not in TOPIC_REGISTRY.csv"
            )


def test_registry_linked_yaml_ssot_resolves():
    """When linked_yaml_ssot is set (not '—' / '-'), it must resolve to a real file."""
    text = REGISTRY.read_text(encoding="utf-8")
    rows = _parse_registry_rows(text)
    # Extract linked_yaml_ssot from raw row text since markdown links wrap it.
    for r in rows:
        cell = r["linked_yaml_ssot"].strip()
        if cell in ("—", "-", ""):
            continue
        # cell may be a markdown link: [text](path)
        m = re.search(r"\[[^\]]+\]\(([^)]+)\)", cell)
        if m:
            path_str = m.group(1)
            # Strip URL fragment / query if any.
            path_str = path_str.split("#", 1)[0].split("?", 1)[0]
            # Drop leading ../ traversals — registry uses relative paths.
            candidate = (REGISTRY.parent / path_str).resolve()
            assert candidate.is_file(), (
                f"row {r.get('file_slug', '<unknown>')}: linked_yaml_ssot path "
                f"{path_str!r} does not resolve to a file"
            )
