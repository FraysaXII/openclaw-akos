"""Initiative 48 P4 — Brand-aligned PDF mode (D-IH-48-H + D-IH-48-H1).

Thin wrapper around ``akos.hlk_pdf_render.render_pdf_branded`` (I27 P1; the
proven WeasyPrint -> fpdf2 -> pandoc -> sidecar fallback chain). Reuses the
existing brand tokens (BRAND_TOKENS_LIGHT/DARK; single SSOT vs
BRAND_VISUAL_PATTERNS.md).

Per D-IH-48-H1: ``profile="dossier"`` is reused (no new profile added; the
existing ENISA cover layout adapts cleanly to UAT context by passing run_id
as program_id and "UAT Dossier" as discipline).

Public API:
- ``render_dossier_pdf(run, md_text, out_path) -> int``
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path

from akos.dossier.run import DossierRun
from akos.hlk_pdf_render import render_pdf_branded

logger = logging.getLogger("akos.dossier.pdf_render")

DOSSIER_TITLE = "AKOS Operator UAT Dossier"
DOSSIER_SUBTITLE_BY_MODE = {
    "snapshot": "Snapshot mode (offline aggregator)",
    "live": "Live mode (CLI orchestrator)",
    "tier-b": "Tier B mode (live LLM regression)",
}


def render_dossier_pdf(run: DossierRun, md_text: str, out_path: Path) -> int:
    """Render the dossier markdown body to a brand-aligned PDF.

    Per D-IH-48-H1: reuse existing ``profile="dossier"`` from
    ``akos.hlk_pdf_render.render_pdf_branded``; pass run_id as program_id and
    "UAT Dossier" as discipline so the cover band shows the right context.

    Returns ``0`` on success (including soft-success when WeasyPrint+fpdf2+
    pandoc all unavailable; in that case a markdown sidecar is written next
    to ``out_path`` per the existing fallback chain).
    """
    subtitle = DOSSIER_SUBTITLE_BY_MODE.get(run.mode, run.mode)
    issue_date = _iso_date_from_started_at(run.started_at)
    status_label = f"overall_status: {run.overall_status}"

    return render_pdf_branded(
        md_text=md_text,
        out_path=out_path,
        profile="dossier",  # D-IH-48-H1: reuse existing profile
        title=DOSSIER_TITLE,
        subtitle=subtitle,
        program_id=run.run_id,
        discipline="UAT Dossier",
        issue_date=issue_date,
        status_label=status_label,
        source_label="akos.dossier.pdf_render",
    )


def _iso_date_from_started_at(started_at_iso: str) -> str:
    """Extract YYYY-MM-DD from the ISO 8601 started_at; fallback to today UTC."""
    try:
        # started_at is already ISO; strip the time portion.
        dt = datetime.fromisoformat(started_at_iso.replace("Z", "+00:00"))
        return dt.date().isoformat()
    except (ValueError, TypeError):
        return datetime.now(timezone.utc).date().isoformat()
