"""Impeccable bridge Pydantic chassis for I77 P2.

Backs ``scripts/generate_impeccable_bridges.py`` (coverage reporter) +
``scripts/validate_impeccable_bridge_drift.py`` (drift gate) with typed
schemas + parser helpers that read:

- ``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/
  CANONICAL_REGISTRY.csv`` — filters brand-canonical rows
  (``owning_area=Marketing`` + ``owning_role=Brand`` + non-SOP).
- ``PRODUCT.md`` + ``DESIGN.md`` + ``BASELINE_REALITY.md`` at workspace root —
  Impeccable bridge files governed by ``SOP-HLK_TOOLING_STANDARDS_001.md``
  §3.7 (thin-redirect pattern).

The chassis mirrors the I71 P1 ``akos/brand_voice_register.py`` Pydantic
pattern: ``model_config = ConfigDict(frozen=True, extra="forbid")``;
field-validators where invariants matter; parser helpers tolerate file
absence and return ``[]`` rather than raising.

Decisions: D-IH-77-A (charter ratification), D-IH-77-B (Strand A scope:
3 bridges + 15+ canonicals), D-IH-77-C (Strand B posture: generator +
drift gate; soft-30d-then-strict; this chassis). Forward at P2
inline-ratify: D-IH-77-F (strictness ladder verdict) + D-IH-77-G
(generator overwrite mode).
"""

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

# -----------------------------------------------------------------------------
# Type aliases
# -----------------------------------------------------------------------------

BridgeName = Literal["PRODUCT", "DESIGN", "BASELINE_REALITY"]
StrictnessLevel = Literal["soft", "strict", "off"]
CanonicalArtifactType = Literal["md", "csv", "yaml", "sop"]

# -----------------------------------------------------------------------------
# Canonical paths + constants
# -----------------------------------------------------------------------------

WORKSPACE_BRIDGE_FILENAMES: dict[BridgeName, str] = {
    "PRODUCT": "PRODUCT.md",
    "DESIGN": "DESIGN.md",
    "BASELINE_REALITY": "BASELINE_REALITY.md",
}

CANONICAL_REGISTRY_PATH: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/"
    "CANONICAL_REGISTRY.csv"
)

BRAND_CANONICALS_DIR_PREFIX: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/"
)

# Brand canonicals that are bridge-irrelevant: SOPs (procedural; consumed by
# operators not Impeccable design output) + bridge-consumers themselves
# (the new BASELINE_REALITY.md row registered at I77 P1) + non-prose data
# canonicals (SERVICE_OFFERING_CATALOG.md is prose but registered separately).
EXCLUDED_CANONICAL_IDS: frozenset[str] = frozenset(
    {
        "impeccable_bridge_baseline_reality",  # self-reference avoidance
        "brand_validators_readme",  # I71 P1 Pack A1 _validators/ folder README; meta-doc, not brand SSOT
    }
)

EXCLUDED_ARTIFACT_TYPES: frozenset[str] = frozenset({"sop"})


# Generator-fence markers (per C-77-1 default = fenced-regenerable-sections;
# preserves operator prose outside fences; P2 writes only inside fences when
# --write is invoked; default mode is --check only per master-roadmap §P2).
GENERATOR_FENCE_START: str = "<!-- impeccable-bridge-generator:start -->"
GENERATOR_FENCE_END: str = "<!-- impeccable-bridge-generator:end -->"


# -----------------------------------------------------------------------------
# Pydantic models
# -----------------------------------------------------------------------------


class CanonicalCrossReference(BaseModel):
    """One brand canonical row that a bridge should cross-reference.

    Loaded from ``CANONICAL_REGISTRY.csv`` rows filtered to brand corpus
    (``owning_area=Marketing`` + ``owning_role=Brand`` + non-SOP +
    non-excluded-id). Each row tells the drift gate which file MUST appear
    in ≥ 1 bridge cross-reference.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    canonical_id: str = Field(min_length=1, pattern=r"^[a-z0-9_]+$")
    name: str = Field(min_length=1)
    file_path: str = Field(min_length=1)
    filename: str = Field(min_length=1)
    artifact_type: CanonicalArtifactType
    classification: str = Field(min_length=1)
    status: str = Field(min_length=1)

    @field_validator("file_path")
    @classmethod
    def file_path_under_brand_canonicals(cls, v: str) -> str:
        normalised = v.replace("\\", "/")
        if not normalised.startswith(BRAND_CANONICALS_DIR_PREFIX):
            raise ValueError(
                f"file_path {v!r} must live under {BRAND_CANONICALS_DIR_PREFIX!r}"
            )
        return v


class BridgeFileSpec(BaseModel):
    """One Impeccable bridge file at workspace root.

    The 3 bridges (PRODUCT.md / DESIGN.md / BASELINE_REALITY.md) are thin
    redirects per SOP-HLK_TOOLING_STANDARDS_001.md §3.7. Each carries a
    set of cross-references (filenames like ``BRAND_VOICE_FOUNDATION.md``)
    extracted from the bridge content at run time.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    bridge_name: BridgeName
    workspace_relative_path: str = Field(min_length=1)
    exists: bool
    content_length: int = Field(ge=0)
    cross_referenced_filenames: tuple[str, ...]
    has_akos_precedence_rule: bool


class BridgeCoverageReport(BaseModel):
    """Drift-gate result: which brand canonicals are covered by which bridges.

    Per-canonical coverage map (canonical_id → list of bridges that cite it).
    Empty bridge list for a canonical means "missing from all bridges" =
    drift hit. The validator surfaces hits as soft warnings (default per
    D-IH-77-C soft-30d-then-strict) or hard fails (when ``AKOS_IMPECCABLE_
    BRIDGE_DRIFT_STRICT=1`` env override fires).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    canonical_count: int = Field(ge=0)
    bridge_count: int = Field(ge=0)
    coverage_map: dict[str, tuple[BridgeName, ...]]
    missing_canonicals: tuple[str, ...]
    strictness: StrictnessLevel

    @property
    def has_drift(self) -> bool:
        return bool(self.missing_canonicals)

    @property
    def coverage_ratio(self) -> float:
        if self.canonical_count == 0:
            return 1.0
        covered = self.canonical_count - len(self.missing_canonicals)
        return covered / self.canonical_count


# -----------------------------------------------------------------------------
# Parser helpers (tolerate file absence; return empty containers on miss)
# -----------------------------------------------------------------------------


def parse_canonical_inventory(
    registry_path: Path,
) -> list[CanonicalCrossReference]:
    """Parse brand-canonical rows from CANONICAL_REGISTRY.csv.

    Filters: ``owning_area=Marketing`` + ``owning_role=Brand`` +
    ``artifact_type not in EXCLUDED_ARTIFACT_TYPES`` +
    ``canonical_id not in EXCLUDED_CANONICAL_IDS``. Returns empty list when
    the registry file is absent (graceful skip; matches I71 chassis pattern).

    Rows with ``status != 'active'`` are excluded — only active brand
    canonicals are bridge-required; archived rows are forward-charter cleanup.
    """
    if not registry_path.exists():
        return []
    out: list[CanonicalCrossReference] = []
    with registry_path.open("r", encoding="utf-8", newline="") as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            if row.get("owning_area", "").strip() != "Marketing":
                continue
            if row.get("owning_role", "").strip() != "Brand":
                continue
            artifact_type = row.get("artifact_type", "").strip().lower()
            if artifact_type in EXCLUDED_ARTIFACT_TYPES:
                continue
            canonical_id = row.get("canonical_id", "").strip()
            if canonical_id in EXCLUDED_CANONICAL_IDS:
                continue
            if row.get("status", "").strip() != "active":
                continue
            file_path = row.get("file_path", "").strip()
            if not file_path:
                continue
            try:
                filename = file_path.replace("\\", "/").rsplit("/", 1)[-1]
                out.append(
                    CanonicalCrossReference(
                        canonical_id=canonical_id,
                        name=row.get("name", "").strip(),
                        file_path=file_path,
                        filename=filename,
                        artifact_type=artifact_type,  # type: ignore[arg-type]
                        classification=row.get("classification", "").strip(),
                        status=row.get("status", "").strip(),
                    )
                )
            except (ValueError, KeyError):
                # Tolerate malformed rows; other validators will catch them.
                continue
    return out


_CROSS_REF_LINK_RE = re.compile(
    r"\[`([^`\]]+\.(?:md|csv|yaml|yml))`\]"
    r"\(([^)]+)\)"
)
_CROSS_REF_INLINE_PATH_RE = re.compile(
    r"`([A-Z][A-Z0-9_]+\.md)`"
)


def extract_cross_referenced_filenames(content: str) -> set[str]:
    """Extract referenced canonical filenames from bridge content.

    Two patterns matched:
    1. Markdown links of shape ``[`FILENAME.md`](path)`` (the dominant
       bridge convention per SOP §3.7).
    2. Inline backticks ``\\`BRAND_*.md\\`\\`` for canonical names mentioned
       outside a link (rare; allowed as a soft signal).

    Returns lowercase-folded basenames (filename only; no directory) so
    coverage check is path-prefix-tolerant.
    """
    out: set[str] = set()
    for match in _CROSS_REF_LINK_RE.finditer(content):
        backtick_text = match.group(1).strip()
        out.add(backtick_text.rsplit("/", 1)[-1])
    for match in _CROSS_REF_INLINE_PATH_RE.finditer(content):
        out.add(match.group(1).strip())
    return out


_AKOS_PRECEDENCE_HEADER_RE = re.compile(
    r"##\s+AKOS precedence rule",
    re.MULTILINE,
)


def parse_bridge_file(
    bridge_name: BridgeName,
    workspace_root: Path,
) -> BridgeFileSpec:
    """Read a workspace-root bridge file and return its spec.

    Returns a spec with ``exists=False`` when the file is missing (graceful;
    the drift gate surfaces this as a hard error since all 3 bridges are
    expected to exist post-I77 P1).
    """
    filename = WORKSPACE_BRIDGE_FILENAMES[bridge_name]
    path = workspace_root / filename
    if not path.exists():
        return BridgeFileSpec(
            bridge_name=bridge_name,
            workspace_relative_path=filename,
            exists=False,
            content_length=0,
            cross_referenced_filenames=(),
            has_akos_precedence_rule=False,
        )
    content = path.read_text(encoding="utf-8")
    cross_refs = extract_cross_referenced_filenames(content)
    return BridgeFileSpec(
        bridge_name=bridge_name,
        workspace_relative_path=filename,
        exists=True,
        content_length=len(content),
        cross_referenced_filenames=tuple(sorted(cross_refs)),
        has_akos_precedence_rule=bool(_AKOS_PRECEDENCE_HEADER_RE.search(content)),
    )


def parse_all_bridge_files(workspace_root: Path) -> list[BridgeFileSpec]:
    """Parse all 3 bridge files (PRODUCT / DESIGN / BASELINE_REALITY)."""
    return [
        parse_bridge_file("PRODUCT", workspace_root),
        parse_bridge_file("DESIGN", workspace_root),
        parse_bridge_file("BASELINE_REALITY", workspace_root),
    ]


# -----------------------------------------------------------------------------
# Coverage computation
# -----------------------------------------------------------------------------


def compute_coverage(
    bridges: list[BridgeFileSpec],
    canonicals: list[CanonicalCrossReference],
    strictness: StrictnessLevel = "soft",
) -> BridgeCoverageReport:
    """Compute which canonicals are covered by which bridges.

    Per-canonical, the coverage map names the bridges that cite the
    canonical's filename. A canonical absent from all 3 bridges is a
    drift hit (added to ``missing_canonicals``).

    ``strictness`` is metadata only; the caller (drift-gate script)
    decides whether to FAIL or WARN based on it + env overrides.
    """
    coverage_map: dict[str, tuple[BridgeName, ...]] = {}
    missing: list[str] = []
    for canonical in canonicals:
        citing_bridges: list[BridgeName] = []
        for bridge in bridges:
            if not bridge.exists:
                continue
            if canonical.filename in bridge.cross_referenced_filenames:
                citing_bridges.append(bridge.bridge_name)
        coverage_map[canonical.canonical_id] = tuple(citing_bridges)
        if not citing_bridges:
            missing.append(canonical.canonical_id)
    return BridgeCoverageReport(
        canonical_count=len(canonicals),
        bridge_count=sum(1 for b in bridges if b.exists),
        coverage_map=coverage_map,
        missing_canonicals=tuple(missing),
        strictness=strictness,
    )


def render_coverage_section_markdown(
    report: BridgeCoverageReport,
    canonicals: list[CanonicalCrossReference],
) -> str:
    """Render a markdown section listing per-bridge coverage.

    Used by ``scripts/generate_impeccable_bridges.py --check`` for
    operator-facing output. Per C-77-1 default (fenced-regenerable-
    sections), this output could be inserted between
    ``GENERATOR_FENCE_START`` / ``GENERATOR_FENCE_END`` markers when
    ``--write`` mode is invoked (forward-charter; P2 ships --check only).
    """
    lines: list[str] = []
    lines.append(f"# Impeccable bridge coverage report")
    lines.append("")
    lines.append(
        f"Coverage: {report.canonical_count - len(report.missing_canonicals)}"
        f"/{report.canonical_count} brand canonicals cited by >= 1 bridge"
        f" ({report.coverage_ratio:.1%}); strictness={report.strictness}."
    )
    lines.append("")
    canonicals_by_id = {c.canonical_id: c for c in canonicals}
    lines.append("## Per-canonical coverage")
    lines.append("")
    lines.append("| Canonical | Filename | Cited by |")
    lines.append("|:---|:---|:---|")
    for canonical_id, bridge_tuple in sorted(report.coverage_map.items()):
        canonical = canonicals_by_id.get(canonical_id)
        if not canonical:
            continue
        cited_by = ", ".join(bridge_tuple) if bridge_tuple else "**MISSING**"
        lines.append(
            f"| `{canonical.canonical_id}` | `{canonical.filename}` | {cited_by} |"
        )
    lines.append("")
    if report.missing_canonicals:
        lines.append("## Missing from all bridges (drift hits)")
        lines.append("")
        for canonical_id in report.missing_canonicals:
            canonical = canonicals_by_id.get(canonical_id)
            if not canonical:
                continue
            lines.append(
                f"- `{canonical.canonical_id}` "
                f"({canonical.filename}) — "
                f"recommend adding to PRODUCT.md or DESIGN.md or BASELINE_REALITY.md."
            )
    return "\n".join(lines)


__all__ = [
    # Type aliases
    "BridgeName",
    "StrictnessLevel",
    "CanonicalArtifactType",
    # Constants
    "WORKSPACE_BRIDGE_FILENAMES",
    "CANONICAL_REGISTRY_PATH",
    "BRAND_CANONICALS_DIR_PREFIX",
    "EXCLUDED_CANONICAL_IDS",
    "EXCLUDED_ARTIFACT_TYPES",
    "GENERATOR_FENCE_START",
    "GENERATOR_FENCE_END",
    # Pydantic models
    "CanonicalCrossReference",
    "BridgeFileSpec",
    "BridgeCoverageReport",
    # Parser helpers
    "parse_canonical_inventory",
    "extract_cross_referenced_filenames",
    "parse_bridge_file",
    "parse_all_bridge_files",
    # Coverage computation
    "compute_coverage",
    "render_coverage_section_markdown",
]
