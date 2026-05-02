"""Initiative 49 — saved dossier scope for MADEIRA management rollup.

Preset values mirror ``render_uat_dossier.py --filter madeira`` composition:
persona roster, initiative roster, MADEIRA lookup skill replay filter.
"""

from __future__ import annotations

from dataclasses import replace

from akos.dossier.run import DEFAULT_TREND_WINDOW, DossierFilter

MADEIRA_DOSSIER_SKILL_ID = "skill_madeira_lookup_v1"

# Comma-separated rosters stored in ``DossierFilter`` scalar fields for manifest + CLI threading.
MADEIRA_DOSSIER_INITIATIVE_IDS = "02,17,32,45,46,47,49"

MADEIRA_DOSSIER_PERSONA_IDS = (
    "PERSONA-INVESTOR-COLD,PERSONA-INVESTOR-WARM,PERSONA-ADVISOR-REFERRAL,"
    "PERSONA-CUSTOMER-KIRBE-PROSPECT,OPERATOR"
)


def dossier_filter_madeira_preset(
    *,
    since: str | None = None,
    trend_window: int = DEFAULT_TREND_WINDOW,
) -> DossierFilter:
    """Return ``DossierFilter`` populated with MADEIRA preset (flavor + roster)."""
    base = DossierFilter(since=(since or None), trend_window=trend_window)
    return replace(
        base,
        flavor="madeira",
        initiative=MADEIRA_DOSSIER_INITIATIVE_IDS,
        persona_id=MADEIRA_DOSSIER_PERSONA_IDS,
        skill_id=MADEIRA_DOSSIER_SKILL_ID,
    )


def persona_id_set(persona_csv: str | None) -> set[str]:
    """Split comma-separated ``--persona`` / preset roster."""
    if not persona_csv:
        return set()
    return {p.strip() for p in persona_csv.split(",") if p.strip()}


def single_persona_for_cli(persona_csv: str | None) -> str | None:
    """Return persona id when only one is requested.

    CLIs (`eval.py --persona`, `calibrate_scenarios.py --persona`) match a single
    id exactly; when the dossier filter carries a CSV roster (MADEIRA preset),
    the section gather code drops the CLI filter and post-filters rows instead.
    """
    if not persona_csv:
        return None
    parts = [p.strip() for p in persona_csv.split(",") if p.strip()]
    if len(parts) == 1:
        return parts[0]
    return None

