"""Evidence-class gate SSOT (I90 P4 — D-IH-90-EVIDENCE-GATE).

Binds claim types to required proof so shape-PASS cannot substitute for operator intent.
Planning charter: docs/wip/planning/90-routing-and-wiring/reports/evidence-class-gate-charter-2026-06-14.md
"""

from __future__ import annotations

import re
from typing import Literal

EVIDENCE_GATE_WATERSHED_ISO_DATE = "2026-06-14"
INITIATIVE_CLOSURE_EVIDENCE_WATERSHED = "2026-06-14"

EvidenceClass = Literal[
    "git_shape",
    "url_verify",
    "live_probe",
    "browser_experiential",
    "operator_ratify",
    "meta_regression",
]

VALID_EVIDENCE_CLASSES: frozenset[str] = frozenset(
    {
        "git_shape",
        "url_verify",
        "live_probe",
        "browser_experiential",
        "operator_ratify",
        "meta_regression",
    }
)

# Synthetic hash-padding on vendor doc URLs (I100 ledger audit).
URL_HASH_PADDING_RE = re.compile(r"#\d+$")

ACIM_EVIDENCE_IN_NOTES_RE = re.compile(
    r"evidence_class\s*=\s*([a-z_]+)",
    re.IGNORECASE,
)
ACIM_PROOF_IN_NOTES_RE = re.compile(
    r"evidence_proof_ref\s*=\s*(\S+)",
    re.IGNORECASE,
)


def is_url_hash_padding(url: str) -> bool:
    """True when external URL uses fake #N fragment padding."""
    return bool(URL_HASH_PADDING_RE.search((url or "").strip()))


def normalize_url_for_dedupe(url: str) -> str:
    return (url or "").split("#")[0].strip()


def parse_acim_evidence_from_notes(notes: str) -> tuple[str | None, str | None]:
    """Extract evidence_class and evidence_proof_ref from ACIM notes field."""
    ec = ACIM_EVIDENCE_IN_NOTES_RE.search(notes or "")
    pr = ACIM_PROOF_IN_NOTES_RE.search(notes or "")
    evidence_class = ec.group(1).lower() if ec else None
    proof_ref = pr.group(1) if pr else None
    return evidence_class, proof_ref


def acim_has_evidence_proof(
    *,
    notes: str,
    realisation_refs: str,
    tool_catalog_ref: str,
) -> bool:
    """Implemented+confirmed rows must cite proof (notes token, realisation, or tool path)."""
    _, proof_from_notes = parse_acim_evidence_from_notes(notes)
    if proof_from_notes:
        return True
    if (realisation_refs or "").strip():
        return True
    ref = (tool_catalog_ref or "").strip()
    if ref and ("/" in ref or ref.endswith(".md") or ref.startswith("scripts/")):
        return True
    return False


def is_on_or_after_watershed(iso_date: str | None, watershed: str = EVIDENCE_GATE_WATERSHED_ISO_DATE) -> bool:
    if not iso_date:
        return True  # fail-closed when date missing on forward artifacts
    return str(iso_date).strip() >= watershed
