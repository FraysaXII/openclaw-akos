#!/usr/bin/env python3
"""Apply I97 P6b-CSV economic columns to FINOPS + adapter registries (one-shot)."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_adapter_registry_csv import ADAPTER_REGISTRY_FIELDNAMES, REGISTRY_PATHS  # noqa: E402
from akos.hlk_finops_counterparty_csv import FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES  # noqa: E402
from akos.hlk_pricing_tier_registry_csv import (  # noqa: E402
    FINOPS_PERFORMANCE_OBLIGATION_REGISTRY_FIELDNAMES,
    PERF_OBLIGATION_CSV_PATH_RELATIVE,
)

FINOPS_CSV = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/finops"
    / "FINOPS_COUNTERPARTY_REGISTER.csv"
)

COUNTERPARTY_ASSET_REFS: dict[str, str] = {
    "finops_supabase": "DC-HOL-COMPLIANCE-MIRROR-001",
    "finops_stripe": "DC-HOL-GTM-CRM-001",
    "finops_neo4j": "DC-HOL-KM-TOPIC-001",
    "finops_sentry": "DC-HOL-TELEMETRY-OBS-001",
    "finops_langfuse": "DC-HOL-TELEMETRY-OBS-001",
    "finops_anthropic": "DC-HOL-AIC-RUNTIME-001",
    "finops_openai": "DC-HOL-AIC-RUNTIME-001",
    "finops_runpod": "DC-HOL-AIC-RUNTIME-001",
    "finops_cursor": "DC-HOL-AIC-RUNTIME-001",
}

PERF_OBLIGATION_ASSET_REFS: dict[str, str] = {
    "PO-FIN-HOL-PLATFORM-ACCESS": "DC-HOL-AIC-RUNTIME-001",
    "PO-FIN-HOL-METERED-USAGE": "DC-HOL-AIC-RUNTIME-001",
    "PO-FIN-HOL-SERVICE-OUTCOME": "DC-HOL-REVOPS-FINOPS-ENGAGEMENT-001",
    "PO-FIN-HOL-PARTNER-REVSHARE": "DC-HOL-REVOPS-FINOPS-ENGAGEMENT-001",
    "PO-FIN-HOL-TRIAL-ACCESS": "DC-HOL-AIC-RUNTIME-001",
}

REVOPS_HOOKS: dict[str, tuple[str, str]] = {
    "finops_bridge": ("medium", "vs_engagement_to_finops"),
    "people_engagement_handoff": ("medium", "vs_engagement_to_people"),
    "legal_template_fire": ("low", "vs_engagement_to_legal"),
    "madeira_revops_handoff": ("high", "vs_engagement_to_madeira"),
}


def _rewrite_csv(path: Path, fieldnames: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def patch_finops_counterparty() -> None:
    with FINOPS_CSV.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    for row in rows:
        cid = row.get("counterparty_id", "")
        row["information_asset_ref"] = COUNTERPARTY_ASSET_REFS.get(cid, "")
    _rewrite_csv(FINOPS_CSV, FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES, rows)


def patch_perf_obligations() -> None:
    path = REPO_ROOT / PERF_OBLIGATION_CSV_PATH_RELATIVE
    with path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    for row in rows:
        oid = row.get("obligation_id", "")
        row["information_asset_ref"] = PERF_OBLIGATION_ASSET_REFS.get(oid, "")
    _rewrite_csv(path, FINOPS_PERFORMANCE_OBLIGATION_REGISTRY_FIELDNAMES, rows)


def patch_adapter_registries() -> None:
    for cls_name, rel in REGISTRY_PATHS.items():
        path = REPO_ROOT / rel
        with path.open(encoding="utf-8", newline="") as fh:
            rows = list(csv.DictReader(fh))
        for row in rows:
            aid = row.get("adapter_id", "")
            if cls_name == "REVOPS" and aid in REVOPS_HOOKS:
                band, stream = REVOPS_HOOKS[aid]
                row["handoff_cost_band"] = band
                row["value_stream_id"] = stream
            else:
                row["handoff_cost_band"] = ""
                row["value_stream_id"] = ""
        _rewrite_csv(path, ADAPTER_REGISTRY_FIELDNAMES, rows)


def main() -> int:
    patch_finops_counterparty()
    patch_perf_obligations()
    patch_adapter_registries()
    print("I97 P6b-CSV register column backfill complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
