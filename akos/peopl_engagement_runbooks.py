"""Thin shared helpers for I73 People Operations engagement runbooks.

Scripts embed ``process_list.csv`` ``item_id`` strings so
``scripts/validate_process_list_pairing.py`` can discover runbooks under
``scripts/peopl_engagement*.py``.
"""

from __future__ import annotations

import logging


def log_runbook_pairing(logger: logging.Logger, *, script: str, sop_path: str, item_id: str) -> None:
    """Emit a single INFO line citing Rule-1 SOP + process_list pairing."""
    logger.info("peopl_engagement_runbook pairing script=%s sop=%s item_id=%s", script, sop_path, item_id)
