"""Initiative 48 P1 — DossierRun dataclass + DossierFilter + assemble().

The run aggregator: instantiates 12 Section subclasses in fixed order
(D-IH-48-D), invokes their gather() / render_markdown() / render_html() /
metrics_for_trend() methods, builds the manifest (sha256 + git_sha + UTC).

Per dossier-section-spec.md Section 1, the executive summary is COMPUTED
LAST (after all other sections have gathered) but RENDERED FIRST. We
implement this by running gather() in section order 2-12, then 1, then
rendering in order 1-12.

Modes per D-IH-48-C:
- snapshot: read cache when fresh per D-IH-48-E; PLACEHOLDER otherwise
- live: re-run CLIs regardless of cache
- tier-b: re-run with Tier B (env-gated AKOS_DOSSIER_TIER_B=1; per D-IH-48-L)
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger("akos.dossier.run")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ARTIFACTS_BASE = REPO_ROOT / "artifacts" / "uat-dossier"

VALID_MODES = ("snapshot", "live", "tier-b")
VALID_FORMATS = ("md", "pdf", "html", "all")
DEFAULT_MAX_STALENESS_HOURS = 24
DEFAULT_MAX_DOSSIER_USD = 2.0  # D-IH-48-L
DEFAULT_TREND_WINDOW = 10  # P7 / Section 11


@dataclass
class DossierFilter:
    """Per-run filter for --initiative / --persona / --since (P6)."""

    initiative: str | None = None  # e.g. "47"
    persona_id: str | None = None  # e.g. "PERSONA-INVESTOR-COLD"
    since: str | None = None  # ISO date "YYYY-MM-DD"
    trend_window: int = DEFAULT_TREND_WINDOW  # P7 Section 11 history depth


@dataclass
class DossierSectionResult:
    """One section's gather() + render outputs."""

    section_id: int  # 1..12 per dossier-section-spec.md
    name: str
    status: str = "PASS"  # PASS|FAIL|SKIP|WARN|INFO
    markdown: str = ""
    html: str = ""
    metrics: dict[str, Any] = field(default_factory=dict)
    data_age_seconds: float | None = None
    placeholder: bool = False  # True when section emitted PLACEHOLDER text per dossier-section-spec.md
    error: str = ""


@dataclass
class DossierRun:
    """One dossier render invocation. Aggregates 12 sections + manifest."""

    run_id: str = field(default_factory=lambda: f"dossier-{uuid.uuid4().hex[:12]}")
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    git_sha: str = "unknown"
    mode: str = "snapshot"  # snapshot|live|tier-b
    formats: tuple[str, ...] = ("md",)
    filter: DossierFilter = field(default_factory=DossierFilter)
    section_results: list[DossierSectionResult] = field(default_factory=list)
    manifest: dict[str, Any] = field(default_factory=dict)
    overall_status: str = "PASS"  # PASS|FAIL
    elapsed_ms: int = 0

    def add(self, result: DossierSectionResult) -> None:
        self.section_results.append(result)
        if result.status == "FAIL":
            self.overall_status = "FAIL"

    def section_by_id(self, section_id: int) -> DossierSectionResult | None:
        for r in self.section_results:
            if r.section_id == section_id:
                return r
        return None

    def to_markdown(self) -> str:
        """Assemble the full dossier markdown body. Sections render in 1..12 order
        per D-IH-48-D regardless of internal gather() order."""
        lines = [
            "# AKOS Operator UAT Dossier",
            "",
            f"- run_id: `{self.run_id}`",
            f"- started_at: {self.started_at}",
            f"- git_sha: `{self.git_sha}`",
            f"- mode: **{self.mode}**",
            f"- formats: {', '.join(self.formats)}",
            f"- overall_status: **{self.overall_status}**",
            f"- elapsed_ms: {self.elapsed_ms}",
            "",
        ]
        if self.filter.initiative or self.filter.persona_id or self.filter.since:
            lines.append("## Filter")
            lines.append("")
            if self.filter.initiative:
                lines.append(f"- initiative: `{self.filter.initiative}`")
            if self.filter.persona_id:
                lines.append(f"- persona_id: `{self.filter.persona_id}`")
            if self.filter.since:
                lines.append(f"- since: `{self.filter.since}`")
            lines.append("")
        for section_id in range(1, 13):
            result = self.section_by_id(section_id)
            if result is None:
                lines.append(f"## Section {section_id} — (not assembled)")
                lines.append("")
                continue
            lines.append(result.markdown.rstrip())
            lines.append("")
        return "\n".join(lines).rstrip() + "\n"

    def to_manifest(self, *, md_text: str | None = None,
                    pdf_path: Path | None = None,
                    html_text: str | None = None,
                    screenshots: list[Path] | None = None,
                    extra: dict[str, Any] | None = None) -> dict[str, Any]:
        """Build the manifest dict (sha256 + section metrics + run config)."""
        m: dict[str, Any] = {
            "run_id": self.run_id,
            "started_at": self.started_at,
            "git_sha": self.git_sha,
            "mode": self.mode,
            "formats": list(self.formats),
            "overall_status": self.overall_status,
            "elapsed_ms": self.elapsed_ms,
            "filter": {
                "initiative": self.filter.initiative,
                "persona_id": self.filter.persona_id,
                "since": self.filter.since,
            },
            "section_count": len(self.section_results),
            "section_metrics": {
                f"section_{r.section_id:02d}": {
                    "name": r.name,
                    "status": r.status,
                    "data_age_seconds": r.data_age_seconds,
                    "placeholder": r.placeholder,
                    "metrics": r.metrics,
                }
                for r in self.section_results
            },
            "files": {},
        }
        if md_text is not None:
            m["files"]["dossier.md"] = {
                "sha256": hashlib.sha256(md_text.encode("utf-8")).hexdigest(),
                "char_count": len(md_text),
            }
        if pdf_path is not None and pdf_path.is_file():
            m["files"]["dossier.pdf"] = {
                "sha256": hashlib.sha256(pdf_path.read_bytes()).hexdigest(),
                "byte_count": pdf_path.stat().st_size,
            }
        if html_text is not None:
            m["files"]["dossier.html"] = {
                "sha256": hashlib.sha256(html_text.encode("utf-8")).hexdigest(),
                "char_count": len(html_text),
            }
        if screenshots:
            m["files"]["screenshots"] = [
                {"path": str(p.relative_to(REPO_ROOT) if p.is_absolute() else p),
                 "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                for p in screenshots if p.is_file()
            ]
        if extra:
            m.update(extra)
        self.manifest = m
        return m

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True, default=str)


def resolve_run_dir(run: DossierRun, *, base: Path = ARTIFACTS_BASE) -> Path:
    """Compute the per-run artifact directory: artifacts/uat-dossier/uat-dossier-<UTC>/."""
    ts = datetime.fromisoformat(run.started_at.replace("Z", "+00:00")).strftime("%Y%m%dT%H%M%SZ")
    out = base / f"uat-dossier-{ts}"
    return out


def resolve_max_dossier_usd() -> float:
    """Read MAX_DOSSIER_USD env (D-IH-48-L). Default $2/run."""
    raw = (os.environ.get("MAX_DOSSIER_USD") or "").strip()
    if not raw:
        return DEFAULT_MAX_DOSSIER_USD
    try:
        return float(raw)
    except (ValueError, TypeError):
        return DEFAULT_MAX_DOSSIER_USD


def is_tier_b_opted_in() -> bool:
    """D-IH-48-L: AKOS_DOSSIER_TIER_B=1 required for tier-b mode."""
    return (os.environ.get("AKOS_DOSSIER_TIER_B") or "").strip() == "1"
