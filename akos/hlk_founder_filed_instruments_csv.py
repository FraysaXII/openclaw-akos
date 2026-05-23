"""DEPRECATION SHIM — renamed to akos/hlk_filed_instruments_csv.py at I81 P2 T3.

Provides backward-compatible imports for one initiative cycle (removal
scheduled at I81 P9 closure per D-IH-81-S under D-IH-81-G umbrella,
2026-05-23). New code should import directly from
``akos.hlk_filed_instruments_csv``.

The CSV moved from
``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/FOUNDER_FILED_INSTRUMENTS.csv``
to
``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/advops/FILED_INSTRUMENTS.csv``
in the same atomic commit; the Supabase mirror table renamed from
``compliance.founder_filed_instruments_mirror`` to
``compliance.filed_instruments_mirror`` via
``supabase/migrations/20260523000000_i81_p2_t3_alter_filed_instruments_mirror.sql``.
"""

from __future__ import annotations

from akos.hlk_filed_instruments_csv import (
    FILED_INSTRUMENTS_FIELDNAMES as FOUNDER_FILED_INSTRUMENTS_FIELDNAMES,
)

__all__ = ["FOUNDER_FILED_INSTRUMENTS_FIELDNAMES"]
