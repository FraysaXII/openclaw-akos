"""Operator-facing UAT Dossier package (Initiative 48).

Public API for assembling a brand-aligned multi-format dossier (markdown +
PDF + HTML) that aggregates the existing CLI ecosystem (validate_hlk + eval +
calibrate + drift canary + chaos + trigger + judge + Tier B) into a single
timestamped artifact.

Phases (per docs/wip/planning/48-operator-dossier/master-roadmap.md):
- P1 (this commit): module skeleton (DossierRun + Section ABC + 12 subclasses
  + sparkline + html_render scaffold)
- P2: snapshot mode aggregator (offline; reads existing artifacts)
- P3: live mode (subprocess CLI orchestrator + opt-in screenshots)
- P4: PDF mode (reuse akos.hlk_pdf_render.render_pdf_branded)
- P5: HTML mode (brand CSS variables + collapsible details + inline SVG sparklines)
- P6: per-initiative + per-persona + --since scoping
- P7: trend storage (compliance.dossier_run mirror) + 4 sparklines
- P8: CI integration (Tier B trailing dossier step)
- P9: closure
"""

from __future__ import annotations

from akos.dossier.run import DossierFilter, DossierRun, DossierSectionResult
from akos.dossier.sections import (
    SECTION_CLASSES,
    Section,
    SectionData,
    Section01ExecutiveSummary,
    Section02SchemaGovernance,
    Section03EvalHealth,
    Section04PersonaCalibration,
    Section05Adversarial,
    Section06Recovery,
    Section07DriftCanaries,
    Section08OperationalHealth,
    Section09ExternalRepos,
    Section10GovernanceDebt,
    Section11TrendLines,
    Section12Appendix,
)
from akos.dossier.sparkline import INSUFFICIENT_DATA_PLACEHOLDER, render_sparkline_svg

__all__ = [
    "DossierRun",
    "DossierFilter",
    "DossierSectionResult",
    "Section",
    "SectionData",
    "SECTION_CLASSES",
    "Section01ExecutiveSummary",
    "Section02SchemaGovernance",
    "Section03EvalHealth",
    "Section04PersonaCalibration",
    "Section05Adversarial",
    "Section06Recovery",
    "Section07DriftCanaries",
    "Section08OperationalHealth",
    "Section09ExternalRepos",
    "Section10GovernanceDebt",
    "Section11TrendLines",
    "Section12Appendix",
    "render_sparkline_svg",
    "INSUFFICIENT_DATA_PLACEHOLDER",
]
