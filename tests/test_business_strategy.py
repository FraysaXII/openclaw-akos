"""Tests for the Initiative 29 P4 Business Strategy SSOT layer.

Covers:
- Each strategy artifact under
  ``docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/business-strategy/``
  has the required frontmatter keys.
- Each artifact's ``topic_ids`` resolves into ``TOPIC_REGISTRY.csv``.
- Deck-bound artifacts have a ``## Deck-bound facts`` block with at least
  one fenced code block.
- ``POC_TO_COMMERCIAL_MAP.csv`` schema (header + per-row contract).
- ``scripts/sync_deck_from_strategy.py --check-only`` succeeds.
"""
from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
STRATEGY_DIR = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Operations"
    / "PMO" / "business-strategy"
)
TOPIC_REGISTRY = (
    REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "TOPIC_REGISTRY.csv"
)
POC_CSV = (
    REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "POC_TO_COMMERCIAL_MAP.csv"
)
SYNC_SCRIPT = REPO_ROOT / "scripts" / "sync_deck_from_strategy.py"

EXPECTED_ARTIFACTS = {
    "README.md",
    "STRATEGY_DECISION_LOG.md",
    "MARKET_THESIS.md",
    "COMPETITIVE_LANDSCAPE.md",
    "PRICING_MODEL.md",
    "CHANNEL_STRATEGY.md",
    "SALES_MOTION.md",
    "UNIT_ECONOMICS.md",
    "BOOTSTRAPPING_PLAN.md",
    "INVESTMENT_THESIS.md",
}

REQUIRED_FRONTMATTER_KEYS = {
    "status", "role_owner", "area", "entity", "program_id", "plane",
    "topic_ids", "artifact_role", "intellectual_kind", "authority", "last_review",
}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _load_frontmatter(text: str) -> dict[str, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    out: dict[str, str] = {}
    for line in m.group(1).splitlines():
        line = line.rstrip()
        if not line or line.startswith("  - "):
            continue
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def _load_topic_ids() -> set[str]:
    with TOPIC_REGISTRY.open(encoding="utf-8", newline="") as fh:
        return {row["topic_id"].strip() for row in csv.DictReader(fh) if row.get("topic_id")}


# ---- Folder shape ----------------------------------------------------------

def test_strategy_folder_exists():
    assert STRATEGY_DIR.is_dir(), f"missing folder: {STRATEGY_DIR}"


def test_all_expected_artifacts_present():
    actual = {p.name for p in STRATEGY_DIR.glob("*.md")}
    missing = EXPECTED_ARTIFACTS - actual
    assert not missing, f"missing strategy artifacts: {missing}"


# ---- Frontmatter contract --------------------------------------------------

@pytest.mark.parametrize("name", sorted(EXPECTED_ARTIFACTS))
def test_artifact_has_required_frontmatter(name: str):
    path = STRATEGY_DIR / name
    text = path.read_text(encoding="utf-8")
    fm = _load_frontmatter(text)
    missing_keys = REQUIRED_FRONTMATTER_KEYS - set(fm.keys())
    assert not missing_keys, (
        f"{name}: missing frontmatter keys {missing_keys}"
    )


# ---- Topic-registry FK -----------------------------------------------------

def test_every_strategy_topic_id_resolves():
    """Each strategy file's first topic_id (after the 'topic_ids:' key) must
    appear in TOPIC_REGISTRY.csv. The README and decision log are exempt
    only if their topic_ids list is empty."""
    canonical = _load_topic_ids()
    for path in STRATEGY_DIR.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        # Find the first '  - topic_xxx' line under topic_ids:
        m = re.search(
            r"^topic_ids:\s*\n(?:  - (\S+)\n)+",
            text,
            re.MULTILINE,
        )
        if not m:
            continue  # informational artifact w/o topic_ids
        # Capture all bullet points
        bullets = re.findall(r"^  - (\S+)\s*$", text[m.start():m.end()+200], re.MULTILINE)
        for tid in bullets:
            tid = tid.strip().strip('"').strip("'")
            assert tid in canonical, (
                f"{path.name}: topic_id {tid!r} not found in TOPIC_REGISTRY.csv "
                f"({sorted(canonical)[:5]}...)"
            )


def test_business_strategy_parent_topic_present():
    canonical = _load_topic_ids()
    assert "topic_business_strategy" in canonical, (
        "topic_business_strategy not registered as a parent topic"
    )


def test_eleven_business_strategy_topics_registered():
    """Initiative 29 P4 added 11 topics: parent + 10 children
    (incl. POC CSV topic)."""
    canonical = _load_topic_ids()
    expected_children = {
        "topic_business_strategy",
        "topic_market_thesis",
        "topic_competitive_landscape",
        "topic_pricing_model",
        "topic_channel_strategy",
        "topic_sales_motion",
        "topic_unit_economics",
        "topic_bootstrapping_plan",
        "topic_investment_thesis",
        "topic_strategy_decisions",
        "topic_poc_commercial_map",
    }
    missing = expected_children - canonical
    assert not missing, f"missing business-strategy topics: {missing}"


# ---- Deck-bound contract ---------------------------------------------------

DECK_BOUND_HEADING_RE = re.compile(r"^## Deck-bound facts\s*$", re.MULTILINE)
FENCED_CODE_RE = re.compile(r"```(?:[a-zA-Z]*)?\s*\n.*?\n```", re.DOTALL)


@pytest.mark.parametrize("name", [
    "MARKET_THESIS.md", "COMPETITIVE_LANDSCAPE.md", "PRICING_MODEL.md",
    "CHANNEL_STRATEGY.md", "SALES_MOTION.md", "UNIT_ECONOMICS.md",
    "BOOTSTRAPPING_PLAN.md", "INVESTMENT_THESIS.md",
])
def test_deck_bound_artifact_has_facts_block(name: str):
    path = STRATEGY_DIR / name
    text = path.read_text(encoding="utf-8")
    m = DECK_BOUND_HEADING_RE.search(text)
    assert m, f"{name}: missing '## Deck-bound facts' heading"
    after = text[m.end():]
    assert FENCED_CODE_RE.search(after), (
        f"{name}: '## Deck-bound facts' heading present but no fenced code block follows"
    )


# ---- POC CSV ---------------------------------------------------------------

def test_poc_csv_exists():
    assert POC_CSV.is_file(), f"missing {POC_CSV}"


def test_poc_csv_schema():
    expected_cols = (
        "poc_id", "delivery_name", "partner_or_buyer_ref", "domain",
        "engagement_type", "revenue_band", "recurring", "case_study_status",
        "linked_topic_ids", "notes",
    )
    with POC_CSV.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        assert tuple(reader.fieldnames or ()) == expected_cols, (
            f"POC CSV header mismatch: got {reader.fieldnames}, expected {expected_cols}"
        )
        rows = list(reader)
    assert len(rows) >= 5, f"expected >=5 POC rows, got {len(rows)}"
    for row in rows:
        assert row["poc_id"], "empty poc_id"
        assert row["delivery_name"], "empty delivery_name"
        assert row["linked_topic_ids"], (
            f"row {row['poc_id']} has no linked_topic_ids"
        )


def test_poc_csv_topic_ids_resolve():
    canonical = _load_topic_ids()
    with POC_CSV.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            for tid in row["linked_topic_ids"].split(";"):
                tid = tid.strip()
                if not tid:
                    continue
                assert tid in canonical, (
                    f"POC row {row['poc_id']}: linked_topic_id {tid!r} "
                    f"not in TOPIC_REGISTRY.csv"
                )


# ---- Sync script -----------------------------------------------------------

def test_sync_script_exists():
    assert SYNC_SCRIPT.is_file(), f"missing {SYNC_SCRIPT}"


def test_sync_script_check_only_succeeds():
    """sync_deck_from_strategy.py --check-only must exit 0 when the
    contracts hold."""
    proc = subprocess.run(
        [sys.executable, str(SYNC_SCRIPT)],
        cwd=str(REPO_ROOT),
        capture_output=True, text=True, timeout=30,
    )
    assert proc.returncode == 0, (
        f"sync_deck_from_strategy --check-only failed: rc={proc.returncode}\n"
        f"stderr={proc.stderr}\nstdout={proc.stdout}"
    )
    assert "check-only complete" in proc.stdout
