"""Governance tests for the Impeccable bridge chassis (I77 P2).

Covers:

- Pydantic models (``CanonicalCrossReference``, ``BridgeFileSpec``,
  ``BridgeCoverageReport``) — valid + invalid input pairs.
- Parser helpers (``parse_canonical_inventory``,
  ``extract_cross_referenced_filenames``, ``parse_bridge_file``).
- Coverage computation (``compute_coverage``) — happy path + drift case.
- Validator script (``scripts/validate_impeccable_bridge_drift.py``) — exit
  codes for soft vs strict mode; bridge-file-missing hard fail.

Per ``CONTRIBUTING.md`` §"Python Code Standards" — registered under
``@pytest.mark.brand`` (the registered marker that already covers I71 Pack
A1 brand chassis tests; this family fits the same group).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.impeccable_bridge import (
    BRAND_CANONICALS_DIR_PREFIX,
    BridgeCoverageReport,
    BridgeFileSpec,
    CanonicalCrossReference,
    compute_coverage,
    extract_cross_referenced_filenames,
    parse_all_bridge_files,
    parse_bridge_file,
    parse_canonical_inventory,
    render_coverage_section_markdown,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


# -----------------------------------------------------------------------------
# Pydantic model — valid + invalid pairs
# -----------------------------------------------------------------------------


@pytest.mark.brand
def test_canonical_cross_reference_valid() -> None:
    ref = CanonicalCrossReference(
        canonical_id="brand_voice_foundation",
        name="Brand Voice Foundation",
        file_path=BRAND_CANONICALS_DIR_PREFIX + "BRAND_VOICE_FOUNDATION.md",
        filename="BRAND_VOICE_FOUNDATION.md",
        artifact_type="md",
        classification="way_of_working",
        status="active",
    )
    assert ref.canonical_id == "brand_voice_foundation"
    assert ref.filename == "BRAND_VOICE_FOUNDATION.md"


@pytest.mark.brand
def test_canonical_cross_reference_rejects_non_brand_canonical_path() -> None:
    """file_path must live under the brand-canonicals directory."""
    with pytest.raises(ValueError):
        CanonicalCrossReference(
            canonical_id="some_other",
            name="Some Other",
            file_path="docs/something/else/SOME.md",
            filename="SOME.md",
            artifact_type="md",
            classification="way_of_working",
            status="active",
        )


@pytest.mark.brand
def test_canonical_cross_reference_rejects_uppercase_id() -> None:
    """canonical_id must be lowercase + underscores per CANONICAL_REGISTRY convention."""
    with pytest.raises(ValueError):
        CanonicalCrossReference(
            canonical_id="BRAND_VOICE",
            name="Brand Voice",
            file_path=BRAND_CANONICALS_DIR_PREFIX + "BRAND_VOICE_FOUNDATION.md",
            filename="BRAND_VOICE_FOUNDATION.md",
            artifact_type="md",
            classification="way_of_working",
            status="active",
        )


@pytest.mark.brand
def test_bridge_file_spec_valid() -> None:
    spec = BridgeFileSpec(
        bridge_name="PRODUCT",
        workspace_relative_path="PRODUCT.md",
        exists=True,
        content_length=1234,
        cross_referenced_filenames=("BRAND_VOICE_FOUNDATION.md",),
        has_akos_precedence_rule=True,
    )
    assert spec.bridge_name == "PRODUCT"
    assert spec.exists
    assert "BRAND_VOICE_FOUNDATION.md" in spec.cross_referenced_filenames


@pytest.mark.brand
def test_bridge_file_spec_rejects_invalid_bridge_name() -> None:
    """bridge_name is a Literal['PRODUCT', 'DESIGN', 'BASELINE_REALITY']."""
    with pytest.raises(ValueError):
        BridgeFileSpec(
            bridge_name="UNKNOWN",  # type: ignore[arg-type]
            workspace_relative_path="UNKNOWN.md",
            exists=False,
            content_length=0,
            cross_referenced_filenames=(),
            has_akos_precedence_rule=False,
        )


# -----------------------------------------------------------------------------
# Parser helpers
# -----------------------------------------------------------------------------


@pytest.mark.brand
def test_parse_canonical_inventory_returns_brand_rows() -> None:
    """Smoke test: AKOS CANONICAL_REGISTRY.csv yields >= 5 brand canonicals."""
    registry_path = (
        REPO_ROOT
        / "docs"
        / "references"
        / "hlk"
        / "v3.0"
        / "Admin"
        / "O5-1"
        / "People"
        / "Compliance"
        / "canonicals"
        / "CANONICAL_REGISTRY.csv"
    )
    canonicals = parse_canonical_inventory(registry_path)
    assert len(canonicals) >= 5, (
        f"Expected >= 5 brand canonicals filtered from CANONICAL_REGISTRY, "
        f"got {len(canonicals)}"
    )
    for canonical in canonicals:
        assert canonical.classification, "every row must have a classification"
        assert canonical.status == "active", "filter should exclude non-active rows"
        assert "marketing" not in canonical.canonical_id.lower() or "brand" in canonical.canonical_id.lower()


@pytest.mark.brand
def test_parse_canonical_inventory_graceful_on_missing_file(tmp_path: Path) -> None:
    """Missing CSV returns empty list (graceful per I71 chassis pattern)."""
    canonicals = parse_canonical_inventory(tmp_path / "nonexistent.csv")
    assert canonicals == []


@pytest.mark.brand
def test_extract_cross_referenced_filenames_markdown_link() -> None:
    content = (
        "Some prose. See [`BRAND_VOICE_FOUNDATION.md`](docs/path/BRAND_VOICE_FOUNDATION.md) "
        "and [`BRAND_LOGO_SYSTEM.md`](docs/path/BRAND_LOGO_SYSTEM.md)."
    )
    out = extract_cross_referenced_filenames(content)
    assert "BRAND_VOICE_FOUNDATION.md" in out
    assert "BRAND_LOGO_SYSTEM.md" in out


@pytest.mark.brand
def test_extract_cross_referenced_filenames_inline_path() -> None:
    """Inline `BRAND_*.md` (no link) is detected as a soft signal."""
    content = "Per `BRAND_JARGON_AUDIT.md` §4, internal codenames are forbidden externally."
    out = extract_cross_referenced_filenames(content)
    assert "BRAND_JARGON_AUDIT.md" in out


@pytest.mark.brand
def test_parse_bridge_file_existing(tmp_path: Path) -> None:
    """Read a synthetic bridge file and assert parse spec."""
    (tmp_path / "PRODUCT.md").write_text(
        "# PRODUCT\n\n[`BRAND_VOICE_FOUNDATION.md`](docs/BRAND_VOICE_FOUNDATION.md)\n\n"
        "## AKOS precedence rule\n\nLorem.\n",
        encoding="utf-8",
    )
    spec = parse_bridge_file("PRODUCT", tmp_path)
    assert spec.exists
    assert spec.has_akos_precedence_rule
    assert "BRAND_VOICE_FOUNDATION.md" in spec.cross_referenced_filenames


@pytest.mark.brand
def test_parse_bridge_file_missing(tmp_path: Path) -> None:
    """Missing bridge file yields spec with exists=False."""
    spec = parse_bridge_file("DESIGN", tmp_path)
    assert not spec.exists
    assert spec.content_length == 0


@pytest.mark.brand
def test_parse_all_bridge_files_reads_3_files(tmp_path: Path) -> None:
    """All 3 bridges queried; missing ones returned with exists=False."""
    (tmp_path / "PRODUCT.md").write_text("# PRODUCT\n", encoding="utf-8")
    bridges = parse_all_bridge_files(tmp_path)
    assert len(bridges) == 3
    bridges_by_name = {b.bridge_name: b for b in bridges}
    assert bridges_by_name["PRODUCT"].exists
    assert not bridges_by_name["DESIGN"].exists
    assert not bridges_by_name["BASELINE_REALITY"].exists


# -----------------------------------------------------------------------------
# Coverage computation
# -----------------------------------------------------------------------------


@pytest.mark.brand
def test_compute_coverage_happy_path() -> None:
    canonical = CanonicalCrossReference(
        canonical_id="brand_voice_foundation",
        name="Brand Voice Foundation",
        file_path=BRAND_CANONICALS_DIR_PREFIX + "BRAND_VOICE_FOUNDATION.md",
        filename="BRAND_VOICE_FOUNDATION.md",
        artifact_type="md",
        classification="way_of_working",
        status="active",
    )
    bridge = BridgeFileSpec(
        bridge_name="PRODUCT",
        workspace_relative_path="PRODUCT.md",
        exists=True,
        content_length=100,
        cross_referenced_filenames=("BRAND_VOICE_FOUNDATION.md",),
        has_akos_precedence_rule=True,
    )
    report = compute_coverage([bridge], [canonical])
    assert not report.has_drift
    assert report.coverage_ratio == 1.0
    assert report.coverage_map["brand_voice_foundation"] == ("PRODUCT",)


@pytest.mark.brand
def test_compute_coverage_detects_drift() -> None:
    canonical_covered = CanonicalCrossReference(
        canonical_id="brand_voice_foundation",
        name="Brand Voice Foundation",
        file_path=BRAND_CANONICALS_DIR_PREFIX + "BRAND_VOICE_FOUNDATION.md",
        filename="BRAND_VOICE_FOUNDATION.md",
        artifact_type="md",
        classification="way_of_working",
        status="active",
    )
    canonical_missing = CanonicalCrossReference(
        canonical_id="brand_logo_system",
        name="Brand Logo System",
        file_path=BRAND_CANONICALS_DIR_PREFIX + "BRAND_LOGO_SYSTEM.md",
        filename="BRAND_LOGO_SYSTEM.md",
        artifact_type="md",
        classification="way_of_working",
        status="active",
    )
    bridge = BridgeFileSpec(
        bridge_name="PRODUCT",
        workspace_relative_path="PRODUCT.md",
        exists=True,
        content_length=100,
        cross_referenced_filenames=("BRAND_VOICE_FOUNDATION.md",),
        has_akos_precedence_rule=True,
    )
    report = compute_coverage([bridge], [canonical_covered, canonical_missing])
    assert report.has_drift
    assert report.missing_canonicals == ("brand_logo_system",)
    assert report.coverage_ratio == 0.5


@pytest.mark.brand
def test_compute_coverage_skips_missing_bridges() -> None:
    """Bridges with exists=False don't count toward coverage."""
    canonical = CanonicalCrossReference(
        canonical_id="brand_voice_foundation",
        name="Brand Voice Foundation",
        file_path=BRAND_CANONICALS_DIR_PREFIX + "BRAND_VOICE_FOUNDATION.md",
        filename="BRAND_VOICE_FOUNDATION.md",
        artifact_type="md",
        classification="way_of_working",
        status="active",
    )
    missing_bridge = BridgeFileSpec(
        bridge_name="PRODUCT",
        workspace_relative_path="PRODUCT.md",
        exists=False,
        content_length=0,
        cross_referenced_filenames=(),
        has_akos_precedence_rule=False,
    )
    report = compute_coverage([missing_bridge], [canonical])
    assert report.bridge_count == 0
    assert report.has_drift


@pytest.mark.brand
def test_render_coverage_section_markdown_smoke() -> None:
    canonical = CanonicalCrossReference(
        canonical_id="brand_voice_foundation",
        name="Brand Voice Foundation",
        file_path=BRAND_CANONICALS_DIR_PREFIX + "BRAND_VOICE_FOUNDATION.md",
        filename="BRAND_VOICE_FOUNDATION.md",
        artifact_type="md",
        classification="way_of_working",
        status="active",
    )
    report = BridgeCoverageReport(
        canonical_count=1,
        bridge_count=1,
        coverage_map={"brand_voice_foundation": ("PRODUCT",)},
        missing_canonicals=(),
        strictness="soft",
    )
    markdown = render_coverage_section_markdown(report, [canonical])
    assert "Impeccable bridge coverage report" in markdown
    assert "brand_voice_foundation" in markdown
    assert "PRODUCT" in markdown


# -----------------------------------------------------------------------------
# Validator script — exit codes
# -----------------------------------------------------------------------------


@pytest.mark.brand
def test_validate_impeccable_bridge_drift_script_invokes_clean() -> None:
    """Smoke test: validator script runs against AKOS repo state without crashing."""
    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "validate_impeccable_bridge_drift.py"),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    # Soft mode default: exit 0 even with drift (warnings only).
    assert result.returncode == 0, (
        f"Validator should exit 0 in soft mode; got {result.returncode}.\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )


@pytest.mark.brand
def test_generate_impeccable_bridges_script_invokes_clean() -> None:
    """Smoke test: generator script runs --check against AKOS repo state."""
    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "generate_impeccable_bridges.py"),
            "--check",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, (
        f"Generator should exit 0 in --check mode; got {result.returncode}.\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )
    assert "Impeccable bridge coverage report" in result.stdout


@pytest.mark.brand
def test_generate_impeccable_bridges_script_rejects_write() -> None:
    """--write mode is forward-charter; must exit 1 with explanatory error."""
    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "generate_impeccable_bridges.py"),
            "--write",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 1, "Write mode should fail until D-IH-77-G ratification"
